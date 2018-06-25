#encoding:UTF-8
#author:justry

import os
import cv2
import math
import numpy as np
import matplotlib.pyplot as plt
import functools
from PIL import Image, ImageDraw, ImageFont
from scipy.spatial import ConvexHull
from scipy.ndimage.interpolation import rotate

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
FONT_PATH = "%s/fonts/" % CURRENT_DIR

class Line(object):
    def __init__(self, label, coord):
        self.label = label
        self.coord = np.array(coord)
        self.w, self.h = self.get_wh(coord)
        self.end_flag = False
        self.hash_ = hash(self.coord.tostring())
        
    def get_wh(self, coord):
        box = minimum_bounding_rectangle(np.array(coord))
        p0p1 = np.sqrt(np.sum(np.square(box[0] - box[1])))
        p2p1 = np.sqrt(np.sum(np.square(box[2] - box[1])))
        return (p0p1, p2p1) if p0p1 > p2p1 else (p2p1, p0p1)
    
    def distance(self, other):
        return np.sqrt(np.sum(np.square(self.coord[-1] - other.coord[0])))
    
    def coparagraph(self, other, h_factor=0.15, w_factor=2, dis_factor=2.5):
        if self.end_flag:
            return False
        h_ = self.h / other.h
        w_ = self.w - other.w
        start = self.coord[-1, 0] - other.coord[0, 0]
        end_ = self.coord[2, 0] - other.coord[1, 0]
        if '.' == self.label[-1] or '。' == self.label[-1]:
            return False
        if h_ > 1+h_factor or h_ < 1-h_factor:
            return False
        if end_ < -w_factor * self.h:
            return False
        if w_ > w_factor * self.h:
            other.end_flag = True
        dis = self.distance(other)
        if dis > dis_factor * self.h:
            return False
        return True
    
    def find_nearest(self, others):
        ret = others[0]
        nearest = 1e9
        for other in others: 
            dis = self.distance(other)
            if nearest > dis:
                nearest = dis
                ret = other
        return ret

def move_average(l, n=10):
    ret = np.cumsum(l, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def get_background_color(img, n=10):
    bg_color = []
    h, w = img.shape[:2]
    thresh = int(h*0.15)
    for i in range(img.shape[-1]):
        axis0 = img[:thresh, :, i]
        axis1 = img[-thresh:, :, i]
        axis = np.concatenate([axis0, axis1])
        hist = np.histogram(axis, bins=256)
        ms = move_average(hist[0], n)
        color = np.where(ms==np.max(ms))[0][0]+5
        bg_color.append(color)
    return bg_color

def get_background(img, n=10):
    bg_color = get_background_color(img, n)
    bg = np.zeros(img.shape, dtype=np.uint8)
    bg[:, :] = bg_color
    return bg
    

def get_wha(polys):
    polys = np.array(polys)
    angle = math.degrees(math.atan2(polys[0, 1]-polys[1, 1],
                                    polys[1, 0]-polys[0, 0]))
    return (int(np.sqrt(np.sum(np.square(polys[0] - polys[1])))),
            int(np.sqrt(np.sum(np.square(polys[1] - polys[2])))),
            angle)
    
def get_character_size(s):
    try:
        row_l=len(s)
        utf8_l=len(s.encode('utf-8'))
        return (utf8_l-row_l)/2+row_l
    except:
        return None
    return None

def get_transform_perspective(img, box):
    w = box[1][0] - box[0][0]
    h = box[3][1] - box[0][1]
    box = np.float32([(box[0][0], box[0][1]), (box[1][0], box[1][1]),
                      (box[3][0], box[3][1]), (box[2][0], box[2][1])])
    dst = np.float32([[0, 0], [w, 0], [0, h], [w, h]])
    size_x, size_y, channel = img.shape
    w, h = dst[3]
    M = cv2.getPerspectiveTransform(box, dst)  # rect  dst
    warped = cv2.warpPerspective(img, M, (w, h))
    return warped

def get_rectangle_from_boxes(boxes):
    points = np.reshape(np.array(boxes), (-1, 2))
    return minimum_bounding_rectangle(points)


def minimum_bounding_rectangle(points):
    """
    Find the smallest bounding rectangle for a set of points.
    Returns a set of points representing the corners of the bounding box.

    :param points: an nx2 matrix of coordinates
    :rval: an nx2 matrix of coordinates
    """
    pi2 = np.pi/2.

    # get the convex hull for the points
    hull_points = points[ConvexHull(points).vertices]

    # calculate edge angles
    edges = np.zeros((len(hull_points)-1, 2))
    edges = hull_points[1:] - hull_points[:-1]

    angles = np.zeros((len(edges)))
    angles = np.arctan2(edges[:, 1], edges[:, 0])

    angles = np.abs(np.mod(angles, pi2))
    angles = np.unique(angles)

    # find rotation matrices
    # XXX both work
    rotations = np.vstack([
        np.cos(angles),
        np.cos(angles-pi2),
        np.cos(angles+pi2),
        np.cos(angles)]).T
    rotations = rotations.reshape((-1, 2, 2))

    # apply rotations to the hull
    rot_points = np.dot(rotations, hull_points.T)

    # find the bounding points
    min_x = np.nanmin(rot_points[:, 0], axis=1)
    max_x = np.nanmax(rot_points[:, 0], axis=1)
    min_y = np.nanmin(rot_points[:, 1], axis=1)
    max_y = np.nanmax(rot_points[:, 1], axis=1)

    # find the box with the best area
    areas = (max_x - min_x) * (max_y - min_y)
    best_idx = np.argmin(areas)

    # return the best box
    x1 = max_x[best_idx]
    x2 = min_x[best_idx]
    y1 = max_y[best_idx]
    y2 = min_y[best_idx]
    r = rotations[best_idx]

    rval = np.zeros((4, 2))
    rval[0] = np.dot([x1, y2], r)
    rval[1] = np.dot([x2, y2], r)
    rval[2] = np.dot([x2, y1], r)
    rval[3] = np.dot([x1, y1], r)
    
    adds = np.apply_along_axis(lambda x:np.sum(x), -1, rval)
    index = np.where(adds==np.min(adds))[0][0]
    rval = np.concatenate([rval, rval])
    rval = rval[index:index+4]
    
    ret = rval
    if rval[1, 0] < rval[3, 0]:
        ret = np.zeros_like(rval)
        ret[0] = rval[0]
        ret[1] = rval[3]
        ret[2] = rval[2]
        ret[3] = rval[1]
    ret[ret<0] = 0
    
    return ret

def sorted_result(result):
    y = [i[-1][0][-1] for i in result]
    ret = sorted(zip(result, y), key=lambda x:x[-1])
    return [i[0] for i in ret]

def get_paragraphs(result):
    result = sorted_result(result)
    result = [Line(*i) for i in result]
    paras = []
    lines = []
    while len(result):
        end_flag = False
        current_line = result.pop(0)
        lines.append(current_line)
        while not end_flag:
            if len(result) == 0:
                end_flag = True
                paras.append(lines)
                lines = []
                break
            nearest_line = current_line.find_nearest(result)
            if current_line.coparagraph(nearest_line):
                lines.append(nearest_line)
                result.remove(nearest_line)
                current_line = nearest_line
            else:
                end_flag = True
                paras.append(lines)
                lines = []
    return paras

def put_chinese(img, result, translate=False):
    # change the color
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    # pil image
    pil_im = Image.fromarray(img)
    #font = ImageFont.truetype(os.path.join(FONT_PATH, 'simhei.ttf'), 20, encoding='utf-8')
    font_size = functools.partial(
        ImageFont.truetype,
        font=os.path.join(FONT_PATH, 'simhei.ttf'),
        encoding='utf-8'
    )
    h_raw, w_raw = img.shape[:2]
    for i, j in result[0]:
        if i:
            j = np.clip(j, [0, 0], [w_raw, h_raw])
            chr_size_zh = get_character_size(i)
            if translate:
                i = get_trans(i)
            #i = get_trans(i)
            #draw.text((int(j[0][0]), int(j[0][1])-20), i, (0, 0, 255), font=font_size(size=20))
            w, h, angle = get_wha(j)
            sub_img = get_transform_perspective(img, j)
            bg_color = get_background_color(sub_img)
            bg_color[-1] = 256
            #fill the background
            #write the txt
            txt = Image.new('RGBA', (w, h))
            draw = ImageDraw.Draw(txt)
            chr_size = get_character_size(i)
            if chr_size*1.0/chr_size_zh < 2 or chr_size_zh <= 2:
                size = int(min(h, w*1.9/chr_size))
                draw.rectangle(((0, 0), (w, h)), fill=tuple(bg_color))
                draw.text((0, 0), i, (0, 0, 0), font=font_size(size=size))
            else:
                size = int(min(h/2.0, w*3.8/chr_size))
                draw.rectangle(((0, 0), (w, h)), fill=tuple(bg_color))
                s = i.split(' ')
                mid = len(s)//2
                draw.text((0, 0), ' '.join(s[:mid]), (0, 0, 0), font=font_size(size=size))
                draw.text((0, size), ' '.join(s[mid:]), (0, 0, 0), font=font_size(size=size))
            w_ = txt.rotate(angle, expand=1)
            pil_im.paste(w_, (int(j[0][0]), int(j[1][1])), w_)
    img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGBA2BGR)
    return img

def put_para_chinese(img, result, translate=False, is_ch=True):
    # change the color
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
    # pil image
    pil_im = Image.fromarray(img)
    #font = ImageFont.truetype(os.path.join(FONT_PATH, 'simhei.ttf'), 20, encoding='utf-8')
    font_size = functools.partial(
        ImageFont.truetype,
        font=os.path.join(FONT_PATH, 'simhei.ttf'),
        encoding='utf-8'
    )
    for para in result:
        max_char_length = max([get_character_size(i[0]) for i in para])
        boxes = [i[1] for i in para]
        line_ws = []
        line_hs = []
        line_angles = []
        for i in para:
            line_w, line_h, line_angle = get_wha(i[1])
            line_ws.append(line_w)
            line_hs.append(line_h)
            line_angles.append(line_angle)
        para_box = get_rectangle_from_boxes(boxes)
        para_w, para_h, para_angle = get_wha(para_box)
        size = int(min(np.mean(line_hs), para_w*1.9/max_char_length))
        if translate:
            if is_ch:
                strings = ''.join([i[0] for i in para])
            else:
                strings = ' '.join([i[0] for i in para])
            strings = get_trans(strings)
            if is_ch:
                strings = strings.replace(" ' ", "'").replace(" ,", ",")
                strings = divide_sentence(strings, 2*int(para_w/size), not is_ch)
            else:
                strings = divide_sentence(strings, int(para_w/size), not is_ch)
        else:
            strings = [i[0] for i in para]
        if is_ch and translate:
            step = int(0.9*para_h / len(strings))
        else:
            step = int(para_h / len(strings))
        para_txt = Image.new('RGBA', (para_w, para_h))
        para_draw = ImageDraw.Draw(para_txt)
        sub_img = get_transform_perspective(img, para_box)
        bg_color = get_background_color(sub_img)
        bg_color[-1] = 256
        para_draw.rectangle(((0, 0), (para_w, para_h)), fill=tuple(bg_color))
        cnt = 0
        for i in strings:
            para_draw.text((0, cnt*step), i, (0, 0, 0), font=font_size(size=size))
            cnt += 1
        w_ = para_txt.rotate(para_angle, expand=1)
        pil_im.paste(w_, (int(para_box[0][0]), int(para_box[1][1])), w_)
    img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGBA2BGR)
    return img

def divide_sentence(s, line_cnt, is_ch=True):
    ret = []
    if is_ch:
        length = get_character_size(s)
        #line_l = length//line_cnt
        line_content = ''
        line_length = 0
        for i in s:
            line_content += i
            line_length = get_character_size(line_content)
            if line_length >= line_cnt:
                ret.append(line_content)
                line_content = ''
                line_length = 0
        if line_content:
            ret.append(line_content)
    else:
        length = get_character_size(s)
        #line_l = length//line_cnt
        line_content = []
        line_length = 0
        for i in s.split(' '):
            line_content.append(i)
            line_length = get_character_size(' '.join(line_content))
            if line_length >= line_cnt:
                ret.append(' '.join(line_content))
                line_content = []
                line_length = 0
        if len(line_content):
            ret.append(' '.join(line_content))
    return ret

if __name__ == '__main__':
    result = [[('iOS应用安全攻防实战',
                [[59.78621747551866, 135.6218263159274], 
                 [623.0198774792955, 140.36444230925], 
                 [622.5361483972592, 205.96141667028007], 
                 [59.3024898667437, 201.2188002004075]]), 
               ('如果你是一位具有Objective-C基础的应用开发者,这本书绝对是', 
                [[29.937588670403223, 235.68372050507926],
                 [1008.7678876639076, 244.22465668463232],
                 [1008.4558937736791, 284.4474900116233],
                 [29.62560211344037, 275.90655654599124]]),
               ('必需的——你所在的公司的ioS应用受攻击的可能性很大。这是因',
                [[21.464731635544343, 283.9499203885403],
                 [1004.5434579667772, 293.12195413213755],
                 [1004.2168908807222, 332.53181071609686],
                 [21.13816748925485, 323.3597748746859]]),
               ('为恶意攻击者现在使用一系列的工具,采用大多数程序员想不到',
                [[18.48238868222818, 330.12592132287995],
                 [995.3862736524919, 340.36429732466587],
                 [995.0238025737668, 379.19391233981946],
                 [18.1199128375185, 368.9555358539589]]),
               ('的方式进行逆向工程、跟踪和操纵应用。',
                [[59.749779215163784, 378.39637585858077],
                 [630.7081300076288, 384.3652410025017],
                 [630.3593772886742, 422.4070989428931],
                 [59.40102660885193, 416.438235430183]]),
               ('本书演示了多重ioS攻击方式,以及黑客们常用的工具和技术。你',
                [[55.202472240421116, 444.7308286486711],
                 [1001.4626857773266, 453.5754762063096],
                 [1001.1462504335094, 491.55744956489866],
                 [54.88603393245798, 482.71280199507487]]),
               ('可以从中学到保护应用的最佳方式,并且意识到和你的对手一样',
                [[44.81755084192809, 490.6068985668154],
                 [1009.4158453957203, 500.2019509319676],
                 [1009.0842780778581, 537.6940400844132],
                 [44.4859809828404, 528.0989832354753]]),
               ('理解和制定策略是多么重要。', 
                [[72.64875559314909, 537.7814486436074],
                 [473.69897336260436, 542.3185402986978],
                 [473.3424947798676, 578.040367373251],
                 [72.29227667197705, 573.5032775536531]]),
               ('检查显示应用中的微小漏洞,并避免在你的应用中出现同',
                [[140.16627429363186, 649.4546436716881],
                 [983.183645833079, 655.2670686804829],
                 [982.9761192275284, 689.8251447027932],
                 [139.95874176421742, 684.0127187376789]]),
               ('样的问题',
                [[157.60315042568607, 694.5492474933042],
                 [290.644940661628, 696.7117061856619],
                 [290.17326988898833, 729.7414346584416],
                 [157.13147477630673, 727.5789718047422]]),
               ('了解黑客如何通过代码注入感染的恶意程序',
                [[148.02778127049254, 751.7979527825186],
                 [750.2451472157366, 757.6832631071813],
                 [749.9600611154035, 790.6081909646178],
                 [147.74269477127615, 784.7228600075663]]),
               ('明白攻击者如何破解iOS密钥链和数据加密保护',
                [[145.07227055453976, 807.2233978694995], 
                 [803.750952871624, 814.6835511081048], 
                 [803.4206347545048, 847.8970977065591], 
                 [144.7419521216653, 840.436938081801]]), 
               ('n 使用调试器和自定义注入代码操控运行时Objective-C环境', 
                [[124.26701386340649, 862.9982491818829], 
                 [948.8992683769468, 871.2516054018769], 
                 [948.6009123475542, 904.6407379081452], 
                 [123.96865673059138, 896.3873805634769]]), 
               ('阻止攻击者劫持SSL会话和窃取数据流量', 
                [[144.1352424347252, 919.5385101042737], 
                 [720.0371168624229, 923.6567408649897], 
                 [719.8263458972665, 957.0946510510526], 
                 [143.92446802032302, 952.9764185783987]]), 
               ('安全地删除文件,并设计应用防止数据泄露', 
                [[139.18068249067494, 974.1856387090969], 
                 [757.3012800142311, 977.5978412804883], 
                 [757.1293268311946, 1012.8984851378375], 
                 [139.00872473158856, 1009.4862932349774]]), 
               ('■ 避免滥用调试,验证运行时库健全性,确保你的代码难以', 
                [[112.5294071280699, 1028.1280363524183], 
                 [967.668869842545, 1032.9847891672234], 
                 [967.5030054661829, 1067.6054464502333], 
                 [112.3635401746273, 1062.748698845908]]), 
               ('跟踪', 
                [[154.49259692772642, 1075.2820829837196], 
                 [225.0455592472421, 1074.966180509873], 
                 [225.1787522703269, 1109.476272781877], 
                 [154.62578995079846, 1109.792198144039]]), 
               ('OREILLYi', 
                [[685.1707395853338, 1474.260249835699], 
                 [1025.997601820871, 1473.2971015163027], 
                 [1026.1985607254067, 1553.9594113085916], 
                 [685.3717000789063, 1554.9225765823273]]), 
               ('图书分类:]信息安全>软件应用安全', 
                [[80.87229028324565, 1490.4309834012388], 
                 [503.4172765014459, 1480.4010920448138], 
                 [504.164170027917, 1516.263827122492], 
                 [81.61918313957469, 1526.2937270622847]]), 
               ('策划编辑:刘皎', 
                [[75.9521638402578, 1551.8400842342512], 
                 [276.9328529270003, 1546.7236568913847], 
                 [277.6698538061396, 1579.8438171292607], 
                 [76.68916374602362, 1584.9602551786256]]), 
               ('oreilly.com.cn', 
                [[693.4957442938465, 1555.1961008359567], 
                 [922.7602481780436, 1554.2248203089978], 
                 [922.9001527177799, 1592.0473357052067], 
                 [693.6356373910484, 1593.0186040254232]]), 
               ('责任编辑:李利健', 
                [[80.32604739722194, 1595.8481913851215], 
                 [309.380100084802, 1587.1962290592155], 
                 [310.4045184182995, 1618.000163870049], 
                 [81.35046975404106, 1626.6521338247928]]), 
               ('o瓶瘾微m', 
                [[827.7756177494589, 1657.5252555716593], 
                 [968.3821381401983, 1656.0197350681071], 
                 [968.699227403604, 1689.7666636369588], 
                 [828.0927008818059, 1691.2722233776153]]), 
               ('i@博文视点Broadview', 
                [[817.084542565747, 1701.7058090808168], 
                 [1023.4529881642062, 1697.3440011867806], 
                 [1023.9042416927556, 1721.5254579418572], 
                 [817.5357703447334, 1725.8872658352986]]), 
               ('BroadvieW', 
                [[170.66749069319965, 1705.5105259685852], 
                 [390.48508154043003, 1697.9873965307927], 
                 [391.4740317118885, 1730.7285038342402], 
                 [171.6564407573717, 1738.251688057182]]), 
               ('博文视点Broadview', 
                [[544.6505123233422, 1713.9257839153977], 
                 [720.2128561515256, 1707.759219186892], 
                 [720.9374030396848, 1731.2216243731293], 
                 [545.3750449064054, 1737.3882196198347]]), 
               ('ma', 
                [[79.4916527226064, 1750.1662837452902], 
                 [148.87357277047354, 1747.411188014487], 
                 [149.6656287530718, 1770.1009796186336], 
                 [80.28371138747086, 1772.8561669041233]]), 
               ("O'Reilly Media, Inc.授权电子工业出版社出版", 
                [[72.1035909397013, 1829.996417369044], 
                 [583.5022667944296, 1800.279066803084], 
                 [584.7620936839265, 1825.0530773391097], 
                 [73.36341863533805, 1854.7704222954894]]), 
               ('此简体中文版仅限于中国大陆(不包含中国香港、澳门特别行政区和中国台湾地区)销售发行', 
                [[23.222638980093958, 1878.977494377602], 
                 [888.9488203018128, 1828.0093986574345], 
                 [890.2356646646866, 1852.923527464592], 
                 [24.509485591847643, 1903.8916410463619]]), 
               ('iwAmthorized Edition for sale in the mainland of China(excluding Hong Kong,MacaosARanc泛iM4n', 
                [[-15.745226437460351, 1909.366934384874], 
                 [1013.358054502944, 1855.1177064803398], 
                 [1014.388022769067, 1877.5772771510788], 
                 [-14.715261418797317, 1931.8265725171505]])]]
    paras = get_paragraphs(result[0])
    for i in paras:
        print(len(i))
    print('end')