#encoding:UTF-8

from PyQt5 import QtWidgets  
class LoginDialog(QtWidgets.QDialog):   
    def __init__(self, parent=None):   
        QtWidgets.QDialog.__init__(self, parent)   
        self.setWindowTitle('login')  
        self.user = QtWidgets.QLineEdit(self)   
        self.user.move(10, 20)   
        self.user.setText('admin')   
        self.pwd = QtWidgets.QLineEdit(self)   
        self.pwd.move(10, 60)   
        self.pwd.setText('admin')   
        self.pwd.setEchoMode(QtWidgets.QLineEdit.Password)   
        self.loginBtn = QtWidgets.QPushButton('Login', self)   
        self.loginBtn.move(100, 90)   
        self.loginBtn.clicked.connect(self.login) # 绑定方法判断用户名和密码    
    def login(self):   
        if self.user.text() == 'admin' and self.pwd.text() == 'admin':   
            # 如果用户名和密码正确，关闭对话框，accept()关闭后，如果增加一个取消按钮调用reject()    
            self.accept()   
        else:   
            QtWidgets.QMessageBox.critical(self, 'Error', 'User name or password error')   
  
if __name__ == '__main__':   
    import sys   
    app = QtWidgets.QApplication(sys.argv)   
    dialog = LoginDialog()   
    if dialog.exec_():   
        win = QtWidgets.QMainWindow()   
        win.setWindowTitle('MainWindow')  
        win.show()   
        sys.exit(app.exec_())   