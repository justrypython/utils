#encoding:UTF-8

import ocrorot
reload(ocrorot)

sk = ocrorot.SkewEstimator("logskew-000015808-000132.pt")
sk.model

print('end')