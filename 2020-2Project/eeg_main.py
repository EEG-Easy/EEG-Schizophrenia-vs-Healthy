import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import csv
import pymysql
import sys
from sklearn import svm

import pandas as pd
import numpy as np

from mne import EpochsArray
from mne.channels import read_montage
from mne.epochs import concatenate_epochs
from mne import create_info
from mne.viz.topomap import _prepare_topo_plot, plot_topomap
from mne.decoding import CSP
from glob import glob

import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from scipy.signal import welch
from mne import pick_types

import Image_rc

drId = ""
patId = ""
name = ""
fnc_data = ""
sbm_data = ""
eeg_data = ""
come_date = ""


conn = pymysql.connect(host='localhost', user='root', password='', db='mydb', local_infile=1)


# col_names = pd.read_csv('eeg/columnLabels.csv')
# ch_names = list(col_names.columns[4:])
# ch_type = ['eeg'] * 64
#
# sfreq = 1024
# montage = read_montage('standard_1005', ch_names)
# info = create_info(ch_names, sfreq, ch_type, montage)
#
# def creat_mne_epoch_object(fname, info):
#     info['description'] = 'dataset from ' + fname
#     tmin = -1.5
#
#     data = pd.read_csv(fname, header=None)
#     npdata = np.array(data)
#
#     onsets = np.array(np.where(npdata[:, 3] == 1537))
#     conditions = npdata[npdata[:, 3] == 1537, 2]
#     events = np.squeeze(np.dstack((onsets.flatten(), np.zeros(conditions.shape), conditions)))
#
#     EEGdata = npdata.reshape(len(conditions), 3072, 68)
#     EEGdata = EEGdata[:, :, 4:]
#     EEGdata = np.swapaxes(EEGdata, 1, 2)
#
#     event_id = dict(button_tone=1, playback_tone=2, button_alone=3)
#     custom_epochs = EpochsArray(EEGdata, info=info, events=events.astype('int'), tmin=tmin, event_id=event_id)
#     return custom_epochs


# def load_data(train=True, sbm_only=False, fnc_only=False):
#     if train:
#         fnc = "train/train_FNC.csv"
#         sbm = "train/train_SBM.csv"
#     else:
#         fnc = "test/subject%s_test_FNC.csv" % patId
#         sbm = "test/subject%s_test_SBM.csv" % patId
#
#     with open(fnc, 'r') as f:
#         train_fnc = list(csv.reader(f))
#     fnc_header = train_fnc[0]
#     fnc_data = np.array([np.array(list(map(float, i))) for i in train_fnc[1:]])
#     ids = np.array(fnc_data[:, 0], dtype=int)
#
#     with open(sbm, 'r') as f:
#         train_sbm = list(csv.reader(f))
#     sbm_header = train_sbm[0]
#     sbm_data = np.array([np.array(list(map(float, i))) for i in train_sbm[1:]])
#     fnc_data = fnc_data[:, 1:]
#     sbm_data = sbm_data[:, 1:]
#     data = np.column_stack((sbm_data, fnc_data))
#
#     if not train:
#         return ids, data
#
#     with open("train/train_labels.csv", 'r') as f:
#         next(f)
#         labels = np.array([int(i[1]) for i in csv.reader(f)])
#     if sbm_only:
#         return ids, sbm_data, labels
#     elif fnc_only:
#         return ids, fnc_data, labels
#     else:
#         return ids, data, labels
#
# def get_name(thing):
#     if hasattr(thing, "steps"):
#         return "_".join([i[0] for i in thing.steps])
#     else:
#         return thing.__repr__().split("(")[0]
#
# def write_predictions(clf):
#     ids, data = load_data(False)
#     preds = get_score(clf, data)
#     with open(get_name(clf) + ".csv", 'w') as f:
#         w = csv.writer(f)
#         w.writerow(["ID", "Probability"])
#         for item in zip(ids, preds):
#             w.writerow(item)
#     return preds
#
# def write_results(clf):
#     ids, data = load_data(False)
#     result = get_result(clf, data)
#     return result
#
# def get_score(clf, data):
#     try:
#         out = clf.decision_function(data).ravel()
#     except AttributeError:
#         try:
#             out = clf.predict_proba(data)[:, 1]
#         except AttributeError:
#             out = clf.predict(data)
#     return out
#
# def get_result(clf, data):
#     result = clf.predict(data)  # 0, 1 판별 코드
#     return result


class Ui_LoginWindow(object):

    def openMain(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow(self.window)                # +++ self.window
        self.ui.setupUi2(self.window)
        LoginWindow.hide()
        self.window.show()

    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(649, 470)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginWindow.sizePolicy().hasHeightForWidth())
        LoginWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        LoginWindow.setWindowIcon(icon)
        LoginWindow.setStyleSheet("background-color: rgb(49, 49, 49);")
        self.centralwidget = QtWidgets.QWidget(LoginWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Logo = QtWidgets.QLabel(self.centralwidget)
        self.Logo.setGeometry(QtCore.QRect(100, 30, 441, 151))
        self.Logo.setStyleSheet("background-image: url(:/Image/Logo.png)")
        self.Logo.setText("")
        self.Logo.setObjectName("Logo")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(79, 199, 492, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.IDLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.IDLayout.setContentsMargins(0, 0, 0, 0)
        self.IDLayout.setSpacing(10)
        self.IDLayout.setObjectName("IDLayout")
        self.IDLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.IDLabel.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.IDLabel.setObjectName("IDLabel")
        self.IDLayout.addWidget(self.IDLabel)
        self.IDEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.IDEdit.sizePolicy().hasHeightForWidth())
        self.IDEdit.setSizePolicy(sizePolicy)
        self.IDEdit.setMinimumSize(QtCore.QSize(415, 0))
        self.IDEdit.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;\n"
"color: rgb(255, 255, 255);\n"
"")
        self.IDEdit.setText("")
        self.IDEdit.setObjectName("IDEdit")
        self.IDLayout.addWidget(self.IDEdit)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(79, 239, 491, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.PWLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.PWLayout.setContentsMargins(0, 0, 0, 0)
        self.PWLayout.setSpacing(10)
        self.PWLayout.setObjectName("PWLayout")
        self.PWLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.PWLabel.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.PWLabel.setObjectName("PWLabel")
        self.PWLayout.addWidget(self.PWLabel)
        self.PWEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PWEdit.sizePolicy().hasHeightForWidth())
        self.PWEdit.setSizePolicy(sizePolicy)
        self.PWEdit.setMinimumSize(QtCore.QSize(415, 0))
        self.PWEdit.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;\n"
"color: rgb(255, 255, 255);\n"
"")
        self.PWEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PWEdit.setObjectName("PWEdit")
        self.PWLayout.addWidget(self.PWEdit)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(79, 289, 491, 36))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.LoginLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.LoginLayout.setContentsMargins(0, 0, 0, 0)
        self.LoginLayout.setSpacing(15)
        self.LoginLayout.setObjectName("LoginLayout")
        self.LoginErrorMsg = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        self.LoginErrorMsg.setEnabled(True)
        self.LoginErrorMsg.setStyleSheet("font: 8pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 32, 32);")
        self.LoginErrorMsg.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.LoginErrorMsg.setObjectName("LoginErrorMsg")
        self.LoginLayout.addWidget(self.LoginErrorMsg)
        self.LoginSubmitButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.LoginSubmitButton.sizePolicy().hasHeightForWidth())
        self.LoginSubmitButton.setSizePolicy(sizePolicy)
        self.LoginSubmitButton.setMinimumSize(QtCore.QSize(182, 0))
        self.LoginSubmitButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.LoginSubmitButton.setStyleSheet("QPushButton {\n"
"font: 9pt \"KoPub돋움체 Medium\";\n"
"color: #fff;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 2, stop: 0 rgb(65, 65, 65), stop: 1 rgb(49, 49, 49));\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"border-color: rgb(116, 116, 116);\n"
"min-width: 10em;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"color: #FFF;\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.LoginSubmitButton.setObjectName("LoginSubmitButton")
        self.LoginLayout.addWidget(self.LoginSubmitButton)
        self.DivideLine = QtWidgets.QFrame(self.centralwidget)
        self.DivideLine.setGeometry(QtCore.QRect(30, 330, 581, 20))
        self.DivideLine.setStyleSheet("")
        self.DivideLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.DivideLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.DivideLine.setObjectName("DivideLine")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(80, 360, 491, 34))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.FindAcctLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.FindAcctLayout.setContentsMargins(0, 0, 0, 0)
        self.FindAcctLayout.setSpacing(15)
        self.FindAcctLayout.setObjectName("FindAcctLayout")
        self.FindAcctLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.FindAcctLabel.setStyleSheet("font: 8pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.FindAcctLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.FindAcctLabel.setObjectName("FindAcctLabel")
        self.FindAcctLayout.addWidget(self.FindAcctLabel)
        self.FindAcctButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.FindAcctButton.sizePolicy().hasHeightForWidth())
        self.FindAcctButton.setSizePolicy(sizePolicy)
        self.FindAcctButton.setMinimumSize(QtCore.QSize(182, 0))
        self.FindAcctButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FindAcctButton.setStyleSheet("QPushButton {\n"
"font: 9pt \"KoPub돋움체 Medium\";\n"
"color: #fff;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 2, stop: 0 rgb(65, 65, 65), stop: 1 rgb(49, 49, 49));\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"border-color: rgb(116, 116, 116);\n"
"min-width: 10em;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"color: #FFF;\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.FindAcctButton.setObjectName("FindAcctButton")
        self.FindAcctLayout.addWidget(self.FindAcctButton)
        self.horizontalLayoutWidget_5 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_5.setGeometry(QtCore.QRect(80, 400, 491, 34))
        self.horizontalLayoutWidget_5.setObjectName("horizontalLayoutWidget_5")
        self.CreatAcctLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_5)
        self.CreatAcctLayout.setContentsMargins(0, 0, 0, 0)
        self.CreatAcctLayout.setSpacing(15)
        self.CreatAcctLayout.setObjectName("CreatAcctLayout")
        self.CreatAcctLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_5)
        self.CreatAcctLabel.setStyleSheet("font: 8pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.CreatAcctLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.CreatAcctLabel.setObjectName("CreatAcctLabel")
        self.CreatAcctLayout.addWidget(self.CreatAcctLabel)
        self.CreatAcctButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_5)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CreatAcctButton.sizePolicy().hasHeightForWidth())
        self.CreatAcctButton.setSizePolicy(sizePolicy)
        self.CreatAcctButton.setMinimumSize(QtCore.QSize(182, 0))
        self.CreatAcctButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CreatAcctButton.setStyleSheet("QPushButton {\n"
"font: 9pt \"KoPub돋움체 Medium\";\n"
"color: #fff;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4, radius: 2, stop: 0 rgb(65, 65, 65), stop: 1 rgb(49, 49, 49));\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"border-color: rgb(116, 116, 116);\n"
"min-width: 10em;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"color: #FFF;\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.CreatAcctButton.setObjectName("CreatAcctButton")
        self.CreatAcctLayout.addWidget(self.CreatAcctButton)
        LoginWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(LoginWindow)
        self.LoginSubmitButton.clicked.connect(self.login_clicked)  # 로그인 이벤트 처리
        # self.FindAcctButton.clicked.connect(self.find_acct_clicked)
        # self.CreatAcctButton.clicked.connect(self.create_acct_clicked)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "Login"))
        self.IDLabel.setText(_translate("LoginWindow", "  계정 ID"))
        self.PWLabel.setText(_translate("LoginWindow", "비밀번호"))
        self.LoginErrorMsg.setToolTip(_translate("LoginWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.LoginErrorMsg.setWhatsThis(_translate("LoginWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.LoginErrorMsg.setText(_translate("LoginWindow", ""))
        self.LoginSubmitButton.setText(_translate("LoginWindow", "로그인"))
        self.FindAcctLabel.setText(_translate("LoginWindow", "로그인 할 수 없습니까?"))
        self.FindAcctButton.setText(_translate("LoginWindow", "ID / 비밀번호 찾기"))
        self.CreatAcctLabel.setText(_translate("LoginWindow", "계정이 없습니까?"))
        self.CreatAcctButton.setText(_translate("LoginWindow", "새 계정 만들기"))

    # 로그인 이벤트 처리
    def login_clicked(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        msg = self.LoginErrorMsg

        # 빈 정보를 입력했을 때
        if not self.IDEdit.text() or not self.PWEdit.text():
            msg.setText(_translate("LoginWindow", "로그인 정보를 입력하세요."))
        # 입력 값과 DB의 계정 정보 비교
        else:
            with conn.cursor() as curs:
                sql = "select * from mydb.doctor_info WHERE dr_id = '%s'" % self.IDEdit.text()
                curs.execute(sql)
                rs = curs.fetchall()
                # ID 틀렸을 시
                if not rs:
                    msg.setText(_translate("LoginWindow", "로그인 정보가 틀립니다."))
                else:
                    for row in rs:
                        # PW 틀렸을 시
                        if self.PWEdit.text() != row[1]:
                            msg.setText(_translate("LoginWindow", "비밀번호가 틀립니다."))
                        # 로그인 성공
                        else:
                            msg.setText(_translate("LoginWindow", "로그인 성공!"))
                            self.IDEdit.setText(_translate("LoginWindow", ""))
                            global drId
                            drId = row[0]
                            self.openMain()


class Ui_MainWindow(object):
    def __init__(self, window2, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)
        self.window2 = window2

    def setupUi2(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.showMaximized()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/Image/Icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(49, 49, 49);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.UserImage = QtWidgets.QLabel(self.centralwidget)
        self.UserImage.setGeometry(QtCore.QRect(40, 160, 131, 162))
        self.UserImage.setStyleSheet("background-image: url(:/Image/Camera Icon.png)")
        self.UserImage.setText("")
        self.UserImage.setObjectName("UserImage")
        self.HorizontalLine = QtWidgets.QFrame(self.centralwidget)
        self.HorizontalLine.setGeometry(QtCore.QRect(20, 80, 1881, 20))
        self.HorizontalLine.setStyleSheet("")
        self.HorizontalLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.HorizontalLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HorizontalLine.setObjectName("HorizontalLine")
        self.Logo = QtWidgets.QLabel(self.centralwidget)
        self.Logo.setGeometry(QtCore.QRect(30, 20, 151, 51))
        self.Logo.setStyleSheet("background-image: url(:/Image/Logo(s).png)")
        self.Logo.setText("")
        self.Logo.setObjectName("Logo")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(340, 30, 401, 44))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.MenuLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.MenuLayout.setContentsMargins(0, 0, 0, 0)
        self.MenuLayout.setObjectName("MenuLayout")
        self.PatRegBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.PatRegBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PatRegBtn.setStyleSheet("QPushButton {\n"
"font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"}\n"
"QPushButton:hover {\n"
"color: rgb(85, 170, 255);\n"
"}")
        self.PatRegBtn.setObjectName("PatRegBtn")
        self.MenuLayout.addWidget(self.PatRegBtn)
        self.PatDiagBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.PatDiagBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PatDiagBtn.setStyleSheet("QPushButton {\n"
"font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"}\n"
"QPushButton:hover {\n"
"color: rgb(85, 170, 255);\n"
"}")
        self.PatDiagBtn.setObjectName("PatDiagBtn")
        self.MenuLayout.addWidget(self.PatDiagBtn)
        self.AccManBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.AccManBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AccManBtn.setStyleSheet("QPushButton {\n"
"font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"}\n"
"QPushButton:hover {\n"
"color: rgb(85, 170, 255);\n"
"}")
        self.AccManBtn.setCheckable(False)
        self.AccManBtn.setAutoRepeat(False)
        self.AccManBtn.setObjectName("AccManBtn")
        self.MenuLayout.addWidget(self.AccManBtn)
        self.VerticalLine = QtWidgets.QFrame(self.centralwidget)
        self.VerticalLine.setGeometry(QtCore.QRect(200, 90, 20, 971))
        self.VerticalLine.setFrameShape(QtWidgets.QFrame.VLine)
        self.VerticalLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.VerticalLine.setObjectName("VerticalLine")
        self.HomeWidget = QtWidgets.QWidget(self.centralwidget)
        self.HomeWidget.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        self.HomeWidget.setStyleSheet("")
        self.HomeWidget.setObjectName("HomeWidget")
        self.HomeLabel = QtWidgets.QLabel(self.HomeWidget)
        self.HomeLabel.setGeometry(QtCore.QRect(680, 0, 75, 31))
        self.HomeLabel.setStyleSheet("font: 13pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);")
        self.HomeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.HomeLabel.setObjectName("HomeLabel")
        self.HomeLine = QtWidgets.QFrame(self.HomeWidget)
        self.HomeLine.setGeometry(QtCore.QRect(10, 40, 1641, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HomeLine.sizePolicy().hasHeightForWidth())
        self.HomeLine.setSizePolicy(sizePolicy)
        self.HomeLine.setStyleSheet("")
        self.HomeLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.HomeLine.setLineWidth(0)
        self.HomeLine.setMidLineWidth(2)
        self.HomeLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.HomeLine.setObjectName("HomeLine")
        self.verticalLayoutWidget_4 = QtWidgets.QWidget(self.HomeWidget)
        self.verticalLayoutWidget_4.setGeometry(QtCore.QRect(361, 60, 720, 721))
        self.verticalLayoutWidget_4.setObjectName("verticalLayoutWidget_4")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ExpLabel_1 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.ExpLabel_1.setStyleSheet("font: 20pt \"12롯데마트드림Bold\";\n"
"color: rgb(85, 170, 255)")
        self.ExpLabel_1.setAlignment(QtCore.Qt.AlignCenter)
        self.ExpLabel_1.setObjectName("ExpLabel_1")
        self.verticalLayout.addWidget(self.ExpLabel_1)
        self.ExpLabel_2 = QtWidgets.QLabel(self.verticalLayoutWidget_4)
        self.ExpLabel_2.setStyleSheet("font: 11pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.ExpLabel_2.setObjectName("ExpLabel_2")
        self.verticalLayout.addWidget(self.ExpLabel_2)
        self.AccManWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.AccManWidget_2.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        self.AccManWidget_2.setStyleSheet("font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);")
        self.AccManWidget_2.setObjectName("AccManWidget_2")
        self.AccManLabel_2 = QtWidgets.QLabel(self.AccManWidget_2)
        self.AccManLabel_2.setGeometry(QtCore.QRect(660, 0, 101, 31))
        self.AccManLabel_2.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);")
        self.AccManLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.AccManLabel_2.setObjectName("AccManLabel_2")
        self.AccManLine_2 = QtWidgets.QFrame(self.AccManWidget_2)
        self.AccManLine_2.setGeometry(QtCore.QRect(10, 40, 1641, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AccManLine_2.sizePolicy().hasHeightForWidth())
        self.AccManLine_2.setSizePolicy(sizePolicy)
        self.AccManLine_2.setStyleSheet("")
        self.AccManLine_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.AccManLine_2.setLineWidth(0)
        self.AccManLine_2.setMidLineWidth(2)
        self.AccManLine_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.AccManLine_2.setObjectName("AccManLine_2")
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(self.AccManWidget_2)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(410, 100, 104, 651))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.UserInf = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.UserInf.setContentsMargins(0, 0, 0, 0)
        self.UserInf.setObjectName("UserInf")
        self.UserIDLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.UserIDLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.UserIDLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.UserIDLabel.setObjectName("UserIDLabel")
        self.UserInf.addWidget(self.UserIDLabel)
        self.UserPWLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.UserPWLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.UserPWLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.UserPWLabel.setObjectName("UserPWLabel")
        self.UserInf.addWidget(self.UserPWLabel)
        self.UserNameLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.UserNameLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.UserNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.UserNameLabel.setObjectName("UserNameLabel")
        self.UserInf.addWidget(self.UserNameLabel)
        self.UserAgeLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.UserAgeLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.UserAgeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.UserAgeLabel.setObjectName("UserAgeLabel")
        self.UserInf.addWidget(self.UserAgeLabel)
        self.UserGenLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.UserGenLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.UserGenLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.UserGenLabel.setObjectName("UserGenLabel")
        self.UserInf.addWidget(self.UserGenLabel)
        self.UserPhoneLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.UserPhoneLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.UserPhoneLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.UserPhoneLabel.setObjectName("UserPhoneLabel")
        self.UserInf.addWidget(self.UserPhoneLabel)
        self.UserHosLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.UserHosLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.UserHosLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.UserHosLabel.setObjectName("UserHosLabel")
        self.UserInf.addWidget(self.UserHosLabel)
        self.UserDepLabel = QtWidgets.QLabel(self.verticalLayoutWidget_3)
        self.UserDepLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.UserDepLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.UserDepLabel.setObjectName("UserDepLabel")
        self.UserInf.addWidget(self.UserDepLabel)
        self.UserWDBtn = QtWidgets.QPushButton(self.AccManWidget_2)
        self.UserWDBtn.setGeometry(QtCore.QRect(950, 790, 112, 34))
        self.UserWDBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.UserWDBtn.setStyleSheet("QPushButton {\n"
"font: 9pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"}\n"
"QPushButton:hover {\n"
"color: rgb(150, 150, 150);\n"
"}")
        self.UserWDBtn.setObjectName("UserWDBtn")
        self.Line = QtWidgets.QFrame(self.AccManWidget_2)
        self.Line.setGeometry(QtCore.QRect(930, 790, 20, 31))
        self.Line.setLineWidth(2)
        self.Line.setMidLineWidth(0)
        self.Line.setFrameShape(QtWidgets.QFrame.VLine)
        self.Line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.Line.setObjectName("Line")
        self.PWCheckLabel = QtWidgets.QLabel(self.AccManWidget_2)
        self.PWCheckLabel.setGeometry(QtCore.QRect(920, 195, 51, 50))
        self.PWCheckLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.PWCheckLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PWCheckLabel.setObjectName("PWCheckLabel")
        self.UserID = QtWidgets.QLineEdit(self.AccManWidget_2)
        self.UserID.setGeometry(QtCore.QRect(540, 113, 350, 50))
        self.UserID.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;")
        self.UserID.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.UserID.setReadOnly(True)
        self.UserID.setObjectName("UserID")
        self.UserPW = QtWidgets.QLineEdit(self.AccManWidget_2)
        self.UserPW.setGeometry(QtCore.QRect(540, 195, 350, 50))
        self.UserPW.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;")
        self.UserPW.setEchoMode(QtWidgets.QLineEdit.Password)
        self.UserPW.setObjectName("UserPW")
        self.UserPWCheck = QtWidgets.QLineEdit(self.AccManWidget_2)
        self.UserPWCheck.setGeometry(QtCore.QRect(990, 195, 300, 50))
        self.UserPWCheck.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;")
        self.UserPWCheck.setEchoMode(QtWidgets.QLineEdit.Password)
        self.UserPWCheck.setObjectName("UserPWCheck")
        self.UserPhone = QtWidgets.QLineEdit(self.AccManWidget_2)
        self.UserPhone.setGeometry(QtCore.QRect(540, 523, 350, 50))
        self.UserPhone.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;")
        self.UserPhone.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.UserPhone.setObjectName("UserPhone")
        self.UserHos = QtWidgets.QLineEdit(self.AccManWidget_2)
        self.UserHos.setGeometry(QtCore.QRect(540, 605, 350, 50))
        self.UserHos.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;")
        self.UserHos.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.UserHos.setObjectName("UserHos")
        self.UserDep = QtWidgets.QLineEdit(self.AccManWidget_2)
        self.UserDep.setGeometry(QtCore.QRect(540, 687, 350, 50))
        self.UserDep.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;")
        self.UserDep.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.UserDep.setObjectName("UserDep")
        self.UserName = QtWidgets.QLineEdit(self.AccManWidget_2)
        self.UserName.setGeometry(QtCore.QRect(540, 277, 350, 50))
        self.UserName.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;")
        self.UserName.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.UserName.setObjectName("UserName")
        self.UserMBtn = QtWidgets.QRadioButton(self.AccManWidget_2)
        self.UserMBtn.setGeometry(QtCore.QRect(540, 441, 175, 50))
        self.UserMBtn.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";")
        self.UserMBtn.setObjectName("UserMBtn")
        self.UserFBtn = QtWidgets.QRadioButton(self.AccManWidget_2)
        self.UserFBtn.setGeometry(QtCore.QRect(715, 441, 175, 50))
        self.UserFBtn.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";")
        self.UserFBtn.setObjectName("UserFBtn")
        self.AcctManErrMsg_2 = QtWidgets.QLabel(self.AccManWidget_2)
        self.AcctManErrMsg_2.setGeometry(QtCore.QRect(1305, 201, 250, 37))
        self.AcctManErrMsg_2.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                           "color: rgb(255, 32, 32);")
        self.AcctManErrMsg_2.setObjectName("AcctManErrMsg_2")

        self.UserBirth = QtWidgets.QLineEdit(self.AccManWidget_2)
        self.UserBirth.setGeometry(QtCore.QRect(540, 359, 350, 50))
        self.UserBirth.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
                                     "background-color: rgb(49, 49, 49);\n"
                                     "border: 1px solid rgb(198, 198, 198);\n"
                                     "border-radius: 3px;\n"
                                     "padding: 4px;")
        self.UserBirth.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.UserBirth.setObjectName("UserBirth")
        self.UserBirthErr = QtWidgets.QLabel(self.AccManWidget_2)
        self.UserBirthErr.setGeometry(QtCore.QRect(910, 373, 131, 18))
        self.UserBirthErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                        "color: rgb(255, 0, 0)")
        self.UserBirthErr.setObjectName("UserBirthErr")
        self.UserNameErr = QtWidgets.QLabel(self.AccManWidget_2)
        self.UserNameErr.setGeometry(QtCore.QRect(910, 293, 131, 18))
        self.UserNameErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                       "color: rgb(255, 0, 0)")
        self.UserNameErr.setObjectName("UserNameErr")
        self.UserPhoneErr = QtWidgets.QLabel(self.AccManWidget_2)
        self.UserPhoneErr.setGeometry(QtCore.QRect(910, 540, 131, 18))
        self.UserPhoneErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                        "color: rgb(255, 0, 0)")
        self.UserPhoneErr.setObjectName("UserPhoneErr")
        self.UserHosErr = QtWidgets.QLabel(self.AccManWidget_2)
        self.UserHosErr.setGeometry(QtCore.QRect(910, 620, 131, 18))
        self.UserHosErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 0, 0)")
        self.UserHosErr.setObjectName("UserHosErr")
        self.UserDepErr = QtWidgets.QLabel(self.AccManWidget_2)
        self.UserDepErr.setGeometry(QtCore.QRect(910, 703, 131, 18))
        self.UserDepErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 0, 0)")
        self.UserDepErr.setObjectName("UserDepErr")
        self.UserSubBtn_Cancel = QtWidgets.QPushButton(self.AccManWidget_2)
        self.UserSubBtn_Cancel.setGeometry(QtCore.QRect(720, 780, 170, 50))
        self.UserSubBtn_Cancel.setStyleSheet("QPushButton {\n"
"font: 12pt \"KoPub돋움체 Bold\";\n"
"color: #333;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
"min-width: 80px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"color: #FFF;\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.UserSubBtn_Cancel.setObjectName("UserSubBtn_Cancel")
        self.UserSubBtn_Ok = QtWidgets.QPushButton(self.AccManWidget_2)
        self.UserSubBtn_Ok.setGeometry(QtCore.QRect(540, 780, 170, 50))
        self.UserSubBtn_Ok.setStyleSheet("QPushButton {\n"
"font: 12pt \"KoPub돋움체 Bold\";\n"
"color: #333;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
"min-width: 80px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"color: #FFF;\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.UserSubBtn_Ok.setObjectName("UserSubBtn_Ok")
        self.PatRegWidget_1 = QtWidgets.QWidget(self.centralwidget)
        self.PatRegWidget_1.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        self.PatRegWidget_1.setStyleSheet("")
        self.PatRegWidget_1.setObjectName("PatRegWidget_1")
        self.PatRegLabel = QtWidgets.QLabel(self.PatRegWidget_1)
        self.PatRegLabel.setGeometry(QtCore.QRect(660, 0, 101, 31))
        self.PatRegLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);")
        self.PatRegLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PatRegLabel.setObjectName("PatRegLabel")
        self.PatRegLine = QtWidgets.QFrame(self.PatRegWidget_1)
        self.PatRegLine.setGeometry(QtCore.QRect(10, 40, 1641, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PatRegLine.sizePolicy().hasHeightForWidth())
        self.PatRegLine.setSizePolicy(sizePolicy)
        self.PatRegLine.setStyleSheet("")
        self.PatRegLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.PatRegLine.setLineWidth(0)
        self.PatRegLine.setMidLineWidth(2)
        self.PatRegLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.PatRegLine.setObjectName("PatRegLine")
        self.NewPatBtn = QtWidgets.QPushButton(self.PatRegWidget_1)
        self.NewPatBtn.setGeometry(QtCore.QRect(375, 285, 660, 120))
        self.NewPatBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.NewPatBtn.setStyleSheet("QPushButton {\n"
"font: 13pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"border-color: rgb(116, 116, 116);\n"
"min-width: 10em;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.NewPatBtn.setObjectName("NewPatBtn")
        self.NewPatImg = QtWidgets.QLabel(self.PatRegWidget_1)
        self.NewPatImg.setGeometry(QtCore.QRect(415, 320, 41, 46))
        self.NewPatImg.setStyleSheet("background-image: url(:/Image/NewPatImg.png);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.NewPatImg.setText("")
        self.NewPatImg.setObjectName("NewPatImg")
        self.ExiPatImg = QtWidgets.QLabel(self.PatRegWidget_1)
        self.ExiPatImg.setGeometry(QtCore.QRect(415, 513, 49, 46))
        self.ExiPatImg.setStyleSheet("background-image: url(:/Image/ExiPatImg.png);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.ExiPatImg.setText("")
        self.ExiPatImg.setObjectName("ExiPatImg")
        self.ExiPatNum = QtWidgets.QLineEdit(self.PatRegWidget_1)
        self.ExiPatNum.setGeometry(QtCore.QRect(615, 517, 250, 40))
        self.ExiPatNum.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-color: #FFF;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;")
        self.ExiPatNum.setObjectName("ExiPatNum")
        self.ExiPatLabel = QtWidgets.QLabel(self.PatRegWidget_1)
        self.ExiPatLabel.setGeometry(QtCore.QRect(375, 478, 660, 120))
        self.ExiPatLabel.setStyleSheet("font: 13pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"border-color: rgb(116, 116, 116);\n"
"min-width: 10em;\n"
"padding: 5px;")
        self.ExiPatLabel.setObjectName("ExiPatLabel")
        self.ExiPatBtn = QtWidgets.QPushButton(self.PatRegWidget_1)
        self.ExiPatBtn.setGeometry(QtCore.QRect(920, 517, 80, 40))
        self.ExiPatBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ExiPatBtn.setStyleSheet("QPushButton {\n"
"font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.ExiPatBtn.setObjectName("ExiPatBtn")
        self.PatSearErr = QtWidgets.QLabel(self.PatRegWidget_1)
        self.PatSearErr.setGeometry(QtCore.QRect(840, 620, 180, 18))
        self.PatSearErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                        "color: rgb(255, 0, 0)")
        self.PatSearErr.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.PatSearErr.setObjectName("PatSearErr")
        self.PatRegLabel.raise_()
        self.PatRegLine.raise_()
        self.NewPatBtn.raise_()
        self.NewPatImg.raise_()
        self.ExiPatLabel.raise_()
        self.ExiPatBtn.raise_()
        self.ExiPatNum.raise_()
        self.ExiPatImg.raise_()
        self.PatSearErr.raise_()
        self.PatRegWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.PatRegWidget_2.setEnabled(True)
        self.PatRegWidget_2.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.PatRegWidget_2.setFont(font)
        self.PatRegWidget_2.setStyleSheet("")
        self.PatRegWidget_2.setObjectName("PatRegWidget_2")
        self.PatBirth = QtWidgets.QDateEdit(self.PatRegWidget_2)
        self.PatBirth.setGeometry(QtCore.QRect(540, 316, 350, 50))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Bold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.PatBirth.setFont(font)
        self.PatBirth.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"border: 1px solid rgb(198, 198, 198);;\n"
"border-radius: 3px;")
        self.PatBirth.setFrame(False)
        self.PatBirth.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.PatBirth.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.PatBirth.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 1, 1), QtCore.QTime(0, 0, 0)))
        self.PatBirth.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(7999, 12, 31), QtCore.QTime(23, 59, 59)))
        self.PatBirth.setCalendarPopup(True)
        self.PatBirth.setObjectName("PatBirth")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.PatRegWidget_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(380, 140, 141, 561))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.NewPatInf = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.NewPatInf.setContentsMargins(0, 0, 0, 0)
        self.NewPatInf.setObjectName("NewPatInf")
        self.PatIDLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PatIDLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.PatIDLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PatIDLabel.setObjectName("PatIDLabel")
        self.NewPatInf.addWidget(self.PatIDLabel)
        self.PatNameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PatNameLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.PatNameLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PatNameLabel.setObjectName("PatNameLabel")
        self.NewPatInf.addWidget(self.PatNameLabel)
        self.PatDateLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PatDateLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.PatDateLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PatDateLabel.setObjectName("PatDateLabel")
        self.NewPatInf.addWidget(self.PatDateLabel)
        self.PatGenLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PatGenLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);")
        self.PatGenLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PatGenLabel.setObjectName("PatGenLabel")
        self.NewPatInf.addWidget(self.PatGenLabel)
        self.PatGroupLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PatGroupLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                            "color: rgb(255, 255, 255);")
        self.PatGroupLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.PatGroupLabel.setObjectName("PatGroupLabel")
        self.NewPatInf.addWidget(self.PatGroupLabel)
        self.PatPhoneLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PatPhoneLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                           "color: rgb(255, 255, 255);")
        self.PatPhoneLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.PatPhoneLabel.setObjectName("PatPhoneLabel")
        self.NewPatInf.addWidget(self.PatPhoneLabel)
        self.PatDocIDLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.PatDocIDLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                            "color: rgb(255, 255, 255);")
        self.PatDocIDLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.PatDocIDLabel.setObjectName("PatDocIDLabel")
        self.NewPatInf.addWidget(self.PatDocIDLabel)
        self.PatLabel = QtWidgets.QLabel(self.PatRegWidget_2)
        self.PatLabel.setGeometry(QtCore.QRect(645, 0, 131, 31))
        self.PatLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);")
        self.PatLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PatLabel.setObjectName("PatLabel")
        self.PatLine = QtWidgets.QFrame(self.PatRegWidget_2)
        self.PatLine.setGeometry(QtCore.QRect(10, 40, 1641, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PatLine.sizePolicy().hasHeightForWidth())
        self.PatLine.setSizePolicy(sizePolicy)
        self.PatLine.setStyleSheet("")
        self.PatLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.PatLine.setLineWidth(0)
        self.PatLine.setMidLineWidth(2)
        self.PatLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.PatLine.setObjectName("PatLine")
        self.PatPhone = QtWidgets.QLineEdit(self.PatRegWidget_2)
        self.PatPhone.setGeometry(QtCore.QRect(540, 557, 350, 50))
        self.PatPhone.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(49, 49, 49);\n"
                                    "border: 1px solid rgb(198, 198, 198);\n"
                                    "border-radius: 3px;\n"
                                    "padding: 4px;\n"
                                    "")
        self.PatPhone.setText("")
        self.PatPhone.setObjectName("PatPhone")
        self.PatNameErr = QtWidgets.QLabel(self.PatRegWidget_2)
        self.PatNameErr.setGeometry(QtCore.QRect(910, 250, 131, 18))
        self.PatNameErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 0, 0)")
        self.PatNameErr.setObjectName("PatNameErr")
        self.PatDocID = QtWidgets.QLineEdit(self.PatRegWidget_2)
        self.PatDocID.setGeometry(QtCore.QRect(540, 638, 350, 50))
        self.PatDocID.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "background-color: rgb(49, 49, 49);\n"
                                      "border: 1px solid rgb(198, 198, 198);\n"
                                      "border-radius: 3px;\n"
                                      "padding: 4px;\n"
                                      "")
        self.PatDocID.setReadOnly(True)
        self.PatDocID.setText("")
        self.PatDocID.setObjectName("PatDocID")
        self.PatPhoneErr = QtWidgets.QLabel(self.PatRegWidget_2)
        self.PatPhoneErr.setGeometry(QtCore.QRect(910, 572, 131, 18))
        self.PatPhoneErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                       "color: rgb(255, 0, 0)")
        self.PatPhoneErr.setObjectName("PatPhoneErr")
        self.PatDocIDErr = QtWidgets.QLabel(self.PatRegWidget_2)
        self.PatDocIDErr.setGeometry(QtCore.QRect(910, 653, 131, 18))
        self.PatDocIDErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                       "color: rgb(255, 0, 0)")
        self.PatDocIDErr.setObjectName("PatDocIDErr")
        self.frame = QtWidgets.QFrame(self.PatRegWidget_2)
        self.frame.setGeometry(QtCore.QRect(529, 381, 371, 80))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayoutWidget_8 = QtWidgets.QWidget(self.frame)
        self.horizontalLayoutWidget_8.setGeometry(QtCore.QRect(10, 10, 351, 61))
        self.horizontalLayoutWidget_8.setObjectName("horizontalLayoutWidget_8")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_8)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.PatMBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget_8)
        self.PatMBtn.setMinimumSize(QtCore.QSize(175, 50))
        self.PatMBtn.setMaximumSize(QtCore.QSize(175, 50))
        self.PatMBtn.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                   "color: rgb(255, 255, 255);")
        self.PatMBtn.setObjectName("PatMBtn")
        self.horizontalLayout_3.addWidget(self.PatMBtn)
        self.PatFBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget_8)
        self.PatFBtn.setMinimumSize(QtCore.QSize(175, 50))
        self.PatFBtn.setMaximumSize(QtCore.QSize(175, 50))
        self.PatFBtn.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                   "color: rgb(255, 255, 255);")
        self.PatFBtn.setObjectName("PatFBtn")
        self.horizontalLayout_3.addWidget(self.PatFBtn)
        self.frame_2 = QtWidgets.QFrame(self.PatRegWidget_2)
        self.frame_2.setGeometry(QtCore.QRect(529, 462, 381, 80))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayoutWidget_6 = QtWidgets.QWidget(self.frame_2)
        self.horizontalLayoutWidget_6.setGeometry(QtCore.QRect(10, 10, 351, 61))
        self.horizontalLayoutWidget_6.setObjectName("horizontalLayoutWidget_6")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.PatHCBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget_6)
        self.PatHCBtn.setMinimumSize(QtCore.QSize(100, 50))
        self.PatHCBtn.setMaximumSize(QtCore.QSize(100, 50))
        self.PatHCBtn.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                    "color: rgb(255, 255, 255);")
        self.PatHCBtn.setObjectName("PatHCBtn")
        self.horizontalLayout_4.addWidget(self.PatHCBtn)
        self.PatSZBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget_6)
        self.PatSZBtn.setMinimumSize(QtCore.QSize(100, 50))
        self.PatSZBtn.setMaximumSize(QtCore.QSize(100, 50))
        self.PatSZBtn.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                    "color: rgb(255, 255, 255);")
        self.PatSZBtn.setObjectName("PatSZBtn")
        self.horizontalLayout_4.addWidget(self.PatSZBtn)
        self.PatPenBtn = QtWidgets.QRadioButton(self.horizontalLayoutWidget_6)
        self.PatPenBtn.setMinimumSize(QtCore.QSize(150, 50))
        self.PatPenBtn.setMaximumSize(QtCore.QSize(150, 50))
        self.PatPenBtn.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                     "color: rgb(255, 255, 255);")
        self.PatPenBtn.setObjectName("PatPenBtn")
        self.horizontalLayout_4.addWidget(self.PatPenBtn)
        self.PatRegNum = QtWidgets.QLineEdit(self.PatRegWidget_2)
        self.PatRegNum.setGeometry(QtCore.QRect(540, 152, 350, 50))
        self.PatRegNum.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;\n"
"")
        self.PatRegNum.setText("")
        self.PatRegNum.setObjectName("PatRegNum")
        self.PatName = QtWidgets.QLineEdit(self.PatRegWidget_2)
        self.PatName.setGeometry(QtCore.QRect(540, 234, 350, 50))
        self.PatName.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(49, 49, 49);\n"
"border: 1px solid rgb(198, 198, 198);\n"
"border-radius: 3px;\n"
"padding: 4px;")
        self.PatName.setText("")
        self.PatName.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.PatName.setObjectName("PatName")
        self.PatOkBtn = QtWidgets.QPushButton(self.PatRegWidget_2)
        self.PatOkBtn.setGeometry(QtCore.QRect(540, 750, 170, 50))
        self.PatOkBtn.setStyleSheet("QPushButton {\n"
"font: 12pt \"KoPub돋움체 Bold\";\n"
"color: #333;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
"min-width: 80px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"color: #FFF;\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.PatOkBtn.setObjectName("PatOkBtn")
        self.PatOkBtn.clicked.connect(self.InsPatInfo)
        self.PatCanBtn = QtWidgets.QPushButton(self.PatRegWidget_2)
        self.PatCanBtn.setGeometry(QtCore.QRect(720, 750, 170, 50))
        self.PatCanBtn.setStyleSheet("QPushButton {\n"
"font: 12pt \"KoPub돋움체 Bold\";\n"
"color: #333;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
"min-width: 80px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"color: #FFF;\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.PatCanBtn.setObjectName("PatCanBtn")
        self.PatCanBtn.clicked.connect(self.PatRegWidget_1.show)
        self.PatCanBtn.clicked.connect(self.PatSearInitialize)
        self.PatNumErr = QtWidgets.QLabel(self.PatRegWidget_2)
        self.PatNumErr.setGeometry(QtCore.QRect(910, 170, 181, 18))
        self.PatNumErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                     "color: rgb(255, 0, 0)")
        self.PatNumErr.setObjectName("PatNumErr")

        self.PatBirth.raise_()
        self.verticalLayoutWidget.raise_()
        self.PatLabel.raise_()
        self.PatLine.raise_()
        self.PatPhone.raise_()
        self.PatName.raise_()
        self.PatOkBtn.raise_()
        self.PatCanBtn.raise_()
        self.PatMBtn.raise_()
        self.PatFBtn.raise_()
        self.PatHCBtn.raise_()
        self.PatSZBtn.raise_()
        self.PatPenBtn.raise_()
        self.PatDocID.raise_()
        self.PatRegNum.raise_()
        self.PatNumErr.raise_()
        self.PatNameErr.raise_()
        self.PatPhoneErr.raise_()
        self.PatDocIDErr.raise_()
        self.frame.raise_()
        self.frame_2.raise_()
        self.PatDiagWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.PatDiagWidget_2.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        self.PatDiagWidget_2.setObjectName("PatDiagWidget_2")
        self.AccuracayFrame = QtWidgets.QFrame(self.PatDiagWidget_2)
        self.AccuracayFrame.setGeometry(QtCore.QRect(670, 10, 981, 921))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Medium")
        self.AccuracayFrame.setFont(font)
        self.AccuracayFrame.setStyleSheet("border-style: outset;")
        self.AccuracayFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.AccuracayFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.AccuracayFrame.setObjectName("AccuracayFrame")
        self.eegGraphLabel = QtWidgets.QLabel(self.AccuracayFrame)
        self.eegGraphLabel.setGeometry(QtCore.QRect(500, 400, 475, 400))
        self.eegGraphLabel.setStyleSheet("background-color: #fff;")
        self.eegGraphLabel.setObjectName("eegGraphLabel")
        self.fig1 = plt.Figure()
        self.eegGraph = FigureCanvas(self.fig1)
        self.eegGraphLayout = QtWidgets.QHBoxLayout(self.eegGraphLabel)
        self.eegGraphLayout.addWidget(self.eegGraph)
        self.PO8_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.PO8_Btn.setGeometry(QtCore.QRect(347, 724, 38, 38))
        self.PO8_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PO8_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.PO8_Btn.setText("")
        self.PO8_Btn.setObjectName("PO8_Btn")
        self.F6_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.F6_Btn.setGeometry(QtCore.QRect(349, 472, 38, 38))
        self.F6_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F6_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.F6_Btn.setText("")
        self.F6_Btn.setObjectName("F6_Btn")
        self.P1_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.P1_Btn.setGeometry(QtCore.QRect(196, 665, 38, 38))
        self.P1_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P1_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.P1_Btn.setText("")
        self.P1_Btn.setObjectName("P1_Btn")
        self.C4_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.C4_Btn.setGeometry(QtCore.QRect(328, 572, 38, 38))
        self.C4_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.C4_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.C4_Btn.setText("")
        self.C4_Btn.setObjectName("C4_Btn")
        self.AF3_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.AF3_Btn.setGeometry(QtCore.QRect(173, 435, 38, 38))
        self.AF3_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AF3_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.AF3_Btn.setText("")
        self.AF3_Btn.setObjectName("AF3_Btn")
        self.FC2_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FC2_Btn.setGeometry(QtCore.QRect(285, 526, 38, 38))
        self.FC2_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FC2_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FC2_Btn.setText("")
        self.FC2_Btn.setObjectName("FC2_Btn")
        self.FT7_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FT7_Btn.setGeometry(QtCore.QRect(60, 514, 38, 38))
        self.FT7_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FT7_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FT7_Btn.setText("")
        self.FT7_Btn.setObjectName("FT7_Btn")
        self.F7_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.F7_Btn.setGeometry(QtCore.QRect(81, 462, 38, 38))
        self.F7_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F7_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.F7_Btn.setText("")
        self.F7_Btn.setObjectName("F7_Btn")
        self.C6_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.C6_Btn.setGeometry(QtCore.QRect(374, 572, 38, 38))
        self.C6_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.C6_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.C6_Btn.setText("")
        self.C6_Btn.setObjectName("C6_Btn")
        self.AF4_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.AF4_Btn.setGeometry(QtCore.QRect(300, 436, 38, 38))
        self.AF4_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AF4_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.AF4_Btn.setText("")
        self.AF4_Btn.setObjectName("AF4_Btn")
        self.F3_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.F3_Btn.setGeometry(QtCore.QRect(157, 477, 38, 38))
        self.F3_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F3_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.F3_Btn.setText("")
        self.F3_Btn.setObjectName("F3_Btn")
        self.FC3_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FC3_Btn.setGeometry(QtCore.QRect(148, 523, 38, 38))
        self.FC3_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FC3_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 180);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FC3_Btn.setText("")
        self.FC3_Btn.setObjectName("FC3_Btn")
        self.P2_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.P2_Btn.setGeometry(QtCore.QRect(272, 665, 38, 38))
        self.P2_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P2_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.P2_Btn.setText("")
        self.P2_Btn.setObjectName("P2_Btn")
        self.AF8_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.AF8_Btn.setGeometry(QtCore.QRect(346, 420, 38, 38))
        self.AF8_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AF8_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.AF8_Btn.setText("")
        self.AF8_Btn.setObjectName("AF8_Btn")
        self.AF7_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.AF7_Btn.setGeometry(QtCore.QRect(127, 421, 38, 38))
        self.AF7_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AF7_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.AF7_Btn.setText("")
        self.AF7_Btn.setObjectName("AF7_Btn")
        self.Fpz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.Fpz_Btn.setGeometry(QtCore.QRect(238, 385, 38, 38))
        self.Fpz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Fpz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.Fpz_Btn.setText("")
        self.Fpz_Btn.setObjectName("Fpz_Btn")
        self.CP3_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.CP3_Btn.setGeometry(QtCore.QRect(149, 620, 38, 38))
        self.CP3_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CP3_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.CP3_Btn.setText("")
        self.CP3_Btn.setObjectName("CP3_Btn")
        self.FC5_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FC5_Btn.setGeometry(QtCore.QRect(102, 519, 38, 38))
        self.FC5_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FC5_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FC5_Btn.setText("")
        self.FC5_Btn.setObjectName("FC5_Btn")
        self.F8_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.F8_Btn.setGeometry(QtCore.QRect(387, 462, 38, 38))
        self.F8_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F8_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.F8_Btn.setText("")
        self.F8_Btn.setObjectName("F8_Btn")
        self.F1_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.F1_Btn.setGeometry(QtCore.QRect(195, 479, 38, 38))
        self.F1_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F1_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 180);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.F1_Btn.setText("")
        self.F1_Btn.setObjectName("F1_Btn")
        self.F2_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.F2_Btn.setGeometry(QtCore.QRect(273, 479, 38, 38))
        self.F2_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F2_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 180);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.F2_Btn.setText("")
        self.F2_Btn.setObjectName("F2_Btn")
        self.Fp2_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.Fp2_Btn.setGeometry(QtCore.QRect(295, 395, 38, 38))
        self.Fp2_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Fp2_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.Fp2_Btn.setText("")
        self.Fp2_Btn.setObjectName("Fp2_Btn")
        self.C3_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.C3_Btn.setGeometry(QtCore.QRect(142, 572, 38, 38))
        self.C3_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.C3_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.C3_Btn.setText("")
        self.C3_Btn.setObjectName("C3_Btn")
        self.O2_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.O2_Btn.setGeometry(QtCore.QRect(294, 750, 38, 38))
        self.O2_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.O2_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.O2_Btn.setText("")
        self.O2_Btn.setObjectName("O2_Btn")
        self.CPz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.CPz_Btn.setGeometry(QtCore.QRect(238, 619, 38, 38))
        self.CPz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CPz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.CPz_Btn.setText("")
        self.CPz_Btn.setObjectName("CPz_Btn")
        self.Fp1_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.Fp1_Btn.setGeometry(QtCore.QRect(179, 394, 38, 38))
        self.Fp1_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Fp1_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.Fp1_Btn.setText("")
        self.Fp1_Btn.setObjectName("Fp1_Btn")
        self.Pz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.Pz_Btn.setGeometry(QtCore.QRect(234, 665, 38, 38))
        self.Pz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Pz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.Pz_Btn.setText("")
        self.Pz_Btn.setObjectName("Pz_Btn")
        self.C5_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.C5_Btn.setGeometry(QtCore.QRect(96, 572, 38, 38))
        self.C5_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.C5_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.C5_Btn.setText("")
        self.C5_Btn.setObjectName("C5_Btn")
        self.CP5_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.CP5_Btn.setGeometry(QtCore.QRect(102, 624, 38, 38))
        self.CP5_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CP5_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.CP5_Btn.setText("")
        self.CP5_Btn.setObjectName("CP5_Btn")
        self.POz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.POz_Btn.setGeometry(QtCore.QRect(238, 712, 38, 38))
        self.POz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.POz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.POz_Btn.setText("")
        self.POz_Btn.setObjectName("POz_Btn")
        self.P7_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.P7_Btn.setGeometry(QtCore.QRect(82, 681, 38, 38))
        self.P7_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P7_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.P7_Btn.setText("")
        self.P7_Btn.setObjectName("P7_Btn")
        self.PO3_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.PO3_Btn.setGeometry(QtCore.QRect(175, 708, 38, 38))
        self.PO3_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PO3_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.PO3_Btn.setText("")
        self.PO3_Btn.setObjectName("PO3_Btn")
        self.P3_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.P3_Btn.setGeometry(QtCore.QRect(158, 666, 38, 38))
        self.P3_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P3_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.P3_Btn.setText("")
        self.P3_Btn.setObjectName("P3_Btn")
        self.P6_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.P6_Btn.setGeometry(QtCore.QRect(348, 671, 38, 38))
        self.P6_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P6_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.P6_Btn.setText("")
        self.P6_Btn.setObjectName("P6_Btn")
        self.CP1_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.CP1_Btn.setGeometry(QtCore.QRect(192, 618, 38, 38))
        self.CP1_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CP1_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.CP1_Btn.setText("")
        self.CP1_Btn.setObjectName("CP1_Btn")
        self.FT8_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FT8_Btn.setGeometry(QtCore.QRect(417, 514, 38, 38))
        self.FT8_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FT8_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FT8_Btn.setText("")
        self.FT8_Btn.setObjectName("FT8_Btn")
        self.FC4_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FC4_Btn.setGeometry(QtCore.QRect(328, 523, 38, 38))
        self.FC4_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FC4_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FC4_Btn.setText("")
        self.FC4_Btn.setObjectName("FC4_Btn")
        self.FCz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FCz_Btn.setGeometry(QtCore.QRect(238, 526, 38, 38))
        self.FCz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FCz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 180);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FCz_Btn.setText("")
        self.FCz_Btn.setObjectName("FCz_Btn")
        self.CP4_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.CP4_Btn.setGeometry(QtCore.QRect(328, 620, 38, 38))
        self.CP4_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CP4_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.CP4_Btn.setText("")
        self.CP4_Btn.setObjectName("CP4_Btn")
        self.P8_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.P8_Btn.setGeometry(QtCore.QRect(386, 682, 38, 38))
        self.P8_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P8_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.P8_Btn.setText("")
        self.P8_Btn.setObjectName("P8_Btn")
        self.T7_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.T7_Btn.setGeometry(QtCore.QRect(49, 572, 38, 38))
        self.T7_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.T7_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.T7_Btn.setText("")
        self.T7_Btn.setObjectName("T7_Btn")
        self.PO7_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.PO7_Btn.setGeometry(QtCore.QRect(128, 723, 38, 38))
        self.PO7_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PO7_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.PO7_Btn.setText("")
        self.PO7_Btn.setObjectName("PO7_Btn")
        self.FC6_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FC6_Btn.setGeometry(QtCore.QRect(374, 519, 38, 38))
        self.FC6_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FC6_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FC6_Btn.setText("")
        self.FC6_Btn.setObjectName("FC6_Btn")
        self.Oz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.Oz_Btn.setGeometry(QtCore.QRect(235, 758, 38, 38))
        self.Oz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Oz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.Oz_Btn.setText("")
        self.Oz_Btn.setObjectName("Oz_Btn")
        self.Fz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.Fz_Btn.setGeometry(QtCore.QRect(234, 479, 38, 38))
        self.Fz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Fz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 180);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.Fz_Btn.setText("")
        self.Fz_Btn.setObjectName("Fz_Btn")
        self.C2_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.C2_Btn.setGeometry(QtCore.QRect(282, 572, 38, 38))
        self.C2_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.C2_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.C2_Btn.setText("")
        self.C2_Btn.setObjectName("C2_Btn")
        self.F5_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.F5_Btn.setGeometry(QtCore.QRect(119, 472, 38, 38))
        self.F5_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F5_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.F5_Btn.setText("")
        self.F5_Btn.setObjectName("F5_Btn")
        self.F4_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.F4_Btn.setGeometry(QtCore.QRect(311, 477, 38, 38))
        self.F4_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.F4_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.F4_Btn.setText("")
        self.F4_Btn.setObjectName("F4_Btn")
        self.TP7_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.TP7_Btn.setGeometry(QtCore.QRect(61, 630, 38, 38))
        self.TP7_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.TP7_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.TP7_Btn.setText("")
        self.TP7_Btn.setObjectName("TP7_Btn")
        self.PO4_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.PO4_Btn.setGeometry(QtCore.QRect(300, 708, 38, 38))
        self.PO4_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PO4_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.PO4_Btn.setText("")
        self.PO4_Btn.setObjectName("PO4_Btn")
        self.CP2_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.CP2_Btn.setGeometry(QtCore.QRect(284, 618, 38, 38))
        self.CP2_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CP2_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.CP2_Btn.setText("")
        self.CP2_Btn.setObjectName("CP2_Btn")
        self.O1_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.O1_Btn.setGeometry(QtCore.QRect(177, 749, 38, 38))
        self.O1_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.O1_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.O1_Btn.setText("")
        self.O1_Btn.setObjectName("O1_Btn")
        self.C1_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.C1_Btn.setGeometry(QtCore.QRect(188, 572, 38, 38))
        self.C1_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.C1_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.C1_Btn.setText("")
        self.C1_Btn.setObjectName("C1_Btn")
        self.ChannelSystemImg = QtWidgets.QLabel(self.AccuracayFrame)
        self.ChannelSystemImg.setGeometry(QtCore.QRect(30, 364, 451, 451))
        self.ChannelSystemImg.setStyleSheet("background-image: url(:/Image/channel1.png)")
        self.ChannelSystemImg.setText("")
        self.ChannelSystemImg.setObjectName("ChannelSystemImg")
        self.P5_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.P5_Btn.setGeometry(QtCore.QRect(120, 672, 38, 38))
        self.P5_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P5_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.P5_Btn.setText("")
        self.P5_Btn.setObjectName("P5_Btn")
        self.Cz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.Cz_Btn.setGeometry(QtCore.QRect(235, 572, 38, 38))
        self.Cz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.Cz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.Cz_Btn.setText("")
        self.Cz_Btn.setObjectName("Cz_Btn")
        self.TP8_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.TP8_Btn.setGeometry(QtCore.QRect(415, 630, 38, 38))
        self.TP8_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.TP8_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.TP8_Btn.setText("")
        self.TP8_Btn.setObjectName("TP8_Btn")
        self.FC1_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.FC1_Btn.setGeometry(QtCore.QRect(192, 526, 38, 38))
        self.FC1_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.FC1_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 180);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.FC1_Btn.setText("")
        self.FC1_Btn.setObjectName("FC1_Btn")
        self.AFz_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.AFz_Btn.setGeometry(QtCore.QRect(236, 433, 38, 38))
        self.AFz_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AFz_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(170, 0, 0, 180);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.AFz_Btn.setText("")
        self.AFz_Btn.setObjectName("AFz_Btn")
        self.CP6_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.CP6_Btn.setGeometry(QtCore.QRect(374, 624, 38, 38))
        self.CP6_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CP6_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.CP6_Btn.setText("")
        self.CP6_Btn.setObjectName("CP6_Btn")
        self.T8_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.T8_Btn.setGeometry(QtCore.QRect(422, 572, 38, 38))
        self.T8_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.T8_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.T8_Btn.setText("")
        self.T8_Btn.setObjectName("T8_Btn")
        self.P4_Btn = QtWidgets.QPushButton(self.AccuracayFrame)
        self.P4_Btn.setGeometry(QtCore.QRect(310, 666, 38, 38))
        self.P4_Btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.P4_Btn.setStyleSheet("QPushButton {\n"
"    background-color: rgba(200, 50, 0, 150);\n"
"    border-radius: 5px;\n"
"    border-style: outset;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgba(100, 100, 100, 150);\n"
"}")
        self.P4_Btn.setText("")
        self.P4_Btn.setObjectName("P4_Btn")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.AccuracayFrame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(505, 355, 216, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.ChannelName = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.ChannelName.setStyleSheet("font: 13pt \"KoPub돋움체 Bold\";\n"
                                       "color: rgb(255, 255, 255);\n")
        self.ChannelName.setObjectName("ChannelName")
        self.horizontalLayout_2.addWidget(self.ChannelName)
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        self.label.setStyleSheet("font: 13pt \"KoPub돋움체 Bold\";\n"
                                 "color: rgb(170, 0, 0)")
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.brainGraphLabel = QLabel(self.AccuracayFrame)
        self.brainGraphLabel.setGeometry(QtCore.QRect(20, 11, 1045, 300))
        self.brainGraphLabel.setStyleSheet("background-color: #fff;")
        self.brainGraphLabel.setObjectName("brainGraph")
        self.ChannelSystemImg.raise_()
        self.F6_Btn.raise_()
        self.P1_Btn.raise_()
        self.C4_Btn.raise_()
        self.AF3_Btn.raise_()
        self.FC2_Btn.raise_()
        self.FT7_Btn.raise_()
        self.F7_Btn.raise_()
        self.C6_Btn.raise_()
        self.PO8_Btn.raise_()
        self.AF4_Btn.raise_()
        self.F3_Btn.raise_()
        self.FC3_Btn.raise_()
        self.P2_Btn.raise_()
        self.AF8_Btn.raise_()
        self.AF7_Btn.raise_()
        self.CP3_Btn.raise_()
        self.FC5_Btn.raise_()
        self.Fpz_Btn.raise_()
        self.F8_Btn.raise_()
        self.F1_Btn.raise_()
        self.F2_Btn.raise_()
        self.C3_Btn.raise_()
        self.Fp2_Btn.raise_()
        self.CPz_Btn.raise_()
        self.O2_Btn.raise_()
        self.Fp1_Btn.raise_()
        self.Pz_Btn.raise_()
        self.C5_Btn.raise_()
        self.CP5_Btn.raise_()
        self.POz_Btn.raise_()
        self.P7_Btn.raise_()
        self.PO3_Btn.raise_()
        self.P3_Btn.raise_()
        self.P6_Btn.raise_()
        self.CP1_Btn.raise_()
        self.FC4_Btn.raise_()
        self.FT8_Btn.raise_()
        self.CP4_Btn.raise_()
        self.FCz_Btn.raise_()
        self.P8_Btn.raise_()
        self.PO7_Btn.raise_()
        self.T7_Btn.raise_()
        self.FC6_Btn.raise_()
        self.Oz_Btn.raise_()
        self.C2_Btn.raise_()
        self.Fz_Btn.raise_()
        self.F5_Btn.raise_()
        self.F4_Btn.raise_()
        self.PO4_Btn.raise_()
        self.TP7_Btn.raise_()
        self.CP2_Btn.raise_()
        self.O1_Btn.raise_()
        self.C1_Btn.raise_()
        self.TP8_Btn.raise_()
        self.Cz_Btn.raise_()
        self.P5_Btn.raise_()
        self.FC1_Btn.raise_()
        self.AFz_Btn.raise_()
        self.CP6_Btn.raise_()
        self.T8_Btn.raise_()
        self.P4_Btn.raise_()
        self.horizontalLayoutWidget_2.raise_()
        self.CannelFrame = QtWidgets.QFrame(self.PatDiagWidget_2)
        self.CannelFrame.setGeometry(QtCore.QRect(10, 10, 641, 921))
        self.CannelFrame.setStyleSheet("border-style: outset;")
        self.CannelFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.CannelFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.CannelFrame.setObjectName("CannelFrame")
        self.horizontalLayoutWidget_4 = QtWidgets.QWidget(self.CannelFrame)
        self.horizontalLayoutWidget_4.setGeometry(QtCore.QRect(160, 389, 419, 51))
        self.horizontalLayoutWidget_4.setObjectName("horizontalLayoutWidget_4")
        self.AccuracyLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_4)
        self.AccuracyLayout.setContentsMargins(0, 0, 0, 0)
        self.AccuracyLayout.setObjectName("AccuracyLayout")
        self.PerLabel_1 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PerLabel_1.sizePolicy().hasHeightForWidth())
        self.PerLabel_1.setSizePolicy(sizePolicy)
        self.PerLabel_1.setStyleSheet("font: 15pt \"KoPub돋움체 Bold\";\n"
"color: rgb(170, 0, 0)")
        self.PerLabel_1.setText("")
        self.PerLabel_1.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.PerLabel_1.setObjectName("PerLabel_1")
        self.AccuracyLayout.addWidget(self.PerLabel_1)
        self.PerLabel_2 = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PerLabel_2.sizePolicy().hasHeightForWidth())
        self.PerLabel_2.setSizePolicy(sizePolicy)
        self.PerLabel_2.setStyleSheet("font: 15pt \"KoPub돋움체 Bold\";\n"
"color: rgb(170, 0, 0)")
        self.PerLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.PerLabel_2.setObjectName("PerLabel_2")
        self.AccuracyLayout.addWidget(self.PerLabel_2)
        self.MsgLabel = QtWidgets.QLabel(self.horizontalLayoutWidget_4)
        self.MsgLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: #fff;")
        self.MsgLabel.setObjectName("MsgLabel")
        self.AccuracyLayout.addWidget(self.MsgLabel)
        self.horizontalLayoutWidget_7 = QtWidgets.QWidget(self.CannelFrame)
        self.horizontalLayoutWidget_7.setGeometry(QtCore.QRect(110, 449, 470, 51))
        self.horizontalLayoutWidget_7.setObjectName("horizontalLayoutWidget_7")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_7)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.DataRegBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        self.DataRegBtn.setEnabled(True)
        self.DataRegBtn.setMinimumSize(QtCore.QSize(150, 40))
        self.DataRegBtn.setMaximumSize(QtCore.QSize(150, 40))
        self.DataRegBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.DataRegBtn.setStyleSheet("QPushButton {\n"
                                      "font: 10pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 255, 255);\n"
                                      "background: rgb(49, 49, 49);\n"
                                      "border-style: outset;\n"
                                      "border-width: 1px;\n"
                                      "border-radius: 3px;\n"
                                      "padding: 5px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "border-color: #FFF;\n"
                                      "color: rgb(100, 100, 100)\n"
                                      "}")
        self.DataRegBtn.setObjectName("DataRegBtn")
        self.horizontalLayout.addWidget(self.DataRegBtn)
        self.ResultBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        self.ResultBtn.setEnabled(True)
        self.ResultBtn.setMinimumSize(QtCore.QSize(150, 40))
        self.ResultBtn.setMaximumSize(QtCore.QSize(150, 40))
        self.ResultBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ResultBtn.setStyleSheet("QPushButton {\n"
"font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"border-color: #FFF;\n"
"color: rgb(170, 0, 0)\n"
"}")
        self.ResultBtn.setObjectName("ResultBtn")
        self.horizontalLayout.addWidget(self.ResultBtn)
        self.ResCmpBtn = QtWidgets.QPushButton(self.horizontalLayoutWidget_7)
        self.ResCmpBtn.setMinimumSize(QtCore.QSize(150, 40))
        self.ResCmpBtn.setMaximumSize(QtCore.QSize(150, 40))
        self.ResCmpBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ResCmpBtn.setStyleSheet("QPushButton {\n"
"font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"border-color: #FFF;\n"
"color: rgb(85, 170, 255)\n"
"}")
        self.ResCmpBtn.setObjectName("ResCmpBtn")
        self.horizontalLayout.addWidget(self.ResCmpBtn)
        self.PatientInfoTable = QtWidgets.QTableWidget(self.CannelFrame)
        self.PatientInfoTable.setGeometry(QtCore.QRect(50, 551, 531, 248))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PatientInfoTable.sizePolicy().hasHeightForWidth())
        self.PatientInfoTable.setSizePolicy(sizePolicy)
        self.PatientInfoTable.setMinimumSize(QtCore.QSize(0, 0))
        self.PatientInfoTable.setSizeIncrement(QtCore.QSize(0, 0))
        self.PatientInfoTable.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Medium")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.PatientInfoTable.setFont(font)
        self.PatientInfoTable.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.PatientInfoTable.setStyleSheet("QWidget {\n"
                                            "color: #fff;\n"
                                            "}\n"
                                            "QHeaderView::section {\n"
                                            "    background-color: rgb(49, 49, 49);\n"
                                            "    padding: 4px;\n"
                                            "    border: 1px solid #fffff8;\n"
                                            "    font: 11pt \"KoPub돋움체 Medium\";\n"
                                            "}\n"
                                            "QTableWidget {\n"
                                            "    gridline-color: #fffff8;\n"
                                            "    font: 11pt \"KoPub돋움체 Medium\";\n"
                                            "}\n"
                                            "QTableWidget QTableCornerButton::section {\n"
                                            "    background-color: rgb(49, 49, 49);\n"
                                            "    border: 1px solid #fffff8;\n"
                                            "}font: 12pt \"KoPub돋움체 Medium\";")
        self.PatientInfoTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.PatientInfoTable.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.PatientInfoTable.setLineWidth(0)
        self.PatientInfoTable.setMidLineWidth(0)
        self.PatientInfoTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.PatientInfoTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.PatientInfoTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.PatientInfoTable.setAutoScrollMargin(16)
        self.PatientInfoTable.setTabKeyNavigation(True)
        self.PatientInfoTable.setDragEnabled(False)
        self.PatientInfoTable.setDragDropOverwriteMode(True)
        self.PatientInfoTable.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.PatientInfoTable.setAlternatingRowColors(False)
        self.PatientInfoTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.PatientInfoTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.PatientInfoTable.setTextElideMode(QtCore.Qt.ElideRight)
        self.PatientInfoTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.PatientInfoTable.setShowGrid(True)
        self.PatientInfoTable.setGridStyle(QtCore.Qt.CustomDashLine)
        self.PatientInfoTable.setWordWrap(True)
        self.PatientInfoTable.setCornerButtonEnabled(True)
        self.PatientInfoTable.setColumnCount(1)
        self.PatientInfoTable.setObjectName("PatientInfoTable")
        self.PatientInfoTable.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.PatientInfoTable.setItem(6, 0, item)
        self.PatientInfoTable.horizontalHeader().setVisible(True)
        self.PatientInfoTable.horizontalHeader().setCascadingSectionResizes(True)
        self.PatientInfoTable.horizontalHeader().setDefaultSectionSize(150)
        self.PatientInfoTable.horizontalHeader().setHighlightSections(True)
        self.PatientInfoTable.horizontalHeader().setMinimumSectionSize(51)
        self.PatientInfoTable.horizontalHeader().setSortIndicatorShown(False)
        self.PatientInfoTable.horizontalHeader().setStretchLastSection(True)
        self.PatientInfoTable.verticalHeader().setVisible(True)
        self.PatientInfoTable.verticalHeader().setCascadingSectionResizes(False)
        self.PatientInfoTable.verticalHeader().setDefaultSectionSize(50)
        self.PatientInfoTable.verticalHeader().setHighlightSections(True)
        self.PatientInfoTable.verticalHeader().setMinimumSectionSize(50)
        self.T2_Img = QtWidgets.QLabel(self.CannelFrame)
        self.T2_Img.setGeometry(QtCore.QRect(330, 10, 285, 301))
        self.T2_Img.setStyleSheet("background-image: url(:/Image/ax t2.png)")
        self.T2_Img.setText("")
        self.T2_Img.setObjectName("T2_Img")
        self.T1_Img = QtWidgets.QLabel(self.CannelFrame)
        self.T1_Img.setGeometry(QtCore.QRect(30, 10, 291, 301))
        self.T1_Img.setStyleSheet("background-image: url(:/Image/ax t1.png)")
        self.T1_Img.setText("")
        self.T1_Img.setObjectName("T1_Img")
        self.T1_Label = QtWidgets.QLabel(self.CannelFrame)
        self.T1_Label.setGeometry(QtCore.QRect(140, 330, 77, 18))
        self.T1_Label.setStyleSheet("font: 10pt \"KoPub돋움체 Medium\";\n"
                                    "color: rgb(255, 255, 255)")
        self.T1_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.T1_Label.setObjectName("T1_Label")
        self.T2_Label = QtWidgets.QLabel(self.CannelFrame)
        self.T2_Label.setGeometry(QtCore.QRect(430, 330, 77, 18))
        self.T2_Label.setStyleSheet("font: 10pt \"KoPub돋움체 Medium\";\n"
                                    "color: rgb(255, 255, 255)")
        self.T2_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.T2_Label.setObjectName("T2_Label")
        self.ResShowErr = QtWidgets.QLabel(self.CannelFrame)
        self.ResShowErr.setGeometry(QtCore.QRect(370, 500, 211, 31))
        self.ResShowErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 0, 0)")
        self.ResShowErr.setObjectName("ResShowErr")
        self.ResShowErr.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.line_2 = QtWidgets.QFrame(self.PatDiagWidget_2)
        self.line_2.setGeometry(QtCore.QRect(650, 10, 20, 921))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.PatDiagWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.PatDiagWidget_3.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        self.PatDiagWidget_3.setObjectName("PatDiagWidget_3")
        self.ResChanLabel = QtWidgets.QLabel(self.PatDiagWidget_3)
        self.ResChanLabel.setGeometry(QtCore.QRect(140, 100, 190, 29))
        self.ResChanLabel.setStyleSheet("font: 13pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);")
        self.ResChanLabel.setObjectName("ResChanLabel")
        self.fig3 = plt.Figure()
        #self.ResChanGraph = FigureCanvas(self.fig3)
        #self.ResChanGraph = self.PatDiagWidget_3
        #self.ResChanGraph.setGeometry(QtCore.QRect(130, 210, 1300, 500))
        #self.ResChanGraph.setStyleSheet("background-color: #fff;")
        #self.ResChanGraph.setObjectName("ResChanGraph")
        self.ResChanGraphLabel = QtWidgets.QLabel(self.PatDiagWidget_3)
        self.ResChanGraphLabel.setGeometry(QtCore.QRect(130, 210, 1300, 500))
        self.ResChanGraphLabel.setStyleSheet("background-color: #fff;")
        self.ResChanGraphLabel.setObjectName("ResChanGraphLabel")
        self.fig3 = plt.Figure()
        self.ResChanGraph = FigureCanvas(self.fig3)
        self.ResChanGraphLayout = QtWidgets.QHBoxLayout(self.ResChanGraphLabel)
        self.ResChanGraphLayout.addWidget(self.ResChanGraph)
        self.BackBtn = QtWidgets.QPushButton(self.PatDiagWidget_3)
        self.BackBtn.setGeometry(QtCore.QRect(1300, 100, 120, 40))
        self.BackBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.BackBtn.setStyleSheet("QPushButton {\n"
"font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"border-color: #FFF;\n"
"color: rgb(100, 100, 100)\n"
"}")
        self.BackBtn.setObjectName("BackBtn")
        self.PatDiagWidget_1 = QtWidgets.QWidget(self.centralwidget)
        self.PatDiagWidget_1.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        self.PatDiagWidget_1.setObjectName("PatDiagWidget_1")
        self.PatSearBtn = QtWidgets.QPushButton(self.PatDiagWidget_1)
        self.PatSearBtn.setGeometry(QtCore.QRect(920, 420, 80, 40))
        self.PatSearBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PatSearBtn.setStyleSheet("QPushButton {\n"
"font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.PatSearBtn.setObjectName("PatSearBtn")
        self.PatDiagLabel = QtWidgets.QLabel(self.PatDiagWidget_1)
        self.PatDiagLabel.setGeometry(QtCore.QRect(660, 0, 101, 31))
        self.PatDiagLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);")
        self.PatDiagLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.PatDiagLabel.setObjectName("PatDiagLabel")
        self.PatDiagLine = QtWidgets.QFrame(self.PatDiagWidget_1)
        self.PatDiagLine.setGeometry(QtCore.QRect(10, 40, 1641, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PatDiagLine.sizePolicy().hasHeightForWidth())
        self.PatDiagLine.setSizePolicy(sizePolicy)
        self.PatDiagLine.setStyleSheet("")
        self.PatDiagLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.PatDiagLine.setLineWidth(0)
        self.PatDiagLine.setMidLineWidth(2)
        self.PatDiagLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.PatDiagLine.setObjectName("PatDiagLine")
        self.PatImg = QtWidgets.QLabel(self.PatDiagWidget_1)
        self.PatImg.setGeometry(QtCore.QRect(415, 416, 37, 46))
        self.PatImg.setStyleSheet("background-image: url(:/Image/PatImg.png);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.PatImg.setText("")
        self.PatImg.setObjectName("PatImg")
        self.PatSearLabel = QtWidgets.QLabel(self.PatDiagWidget_1)
        self.PatSearLabel.setGeometry(QtCore.QRect(375, 380, 660, 120))
        self.PatSearLabel.setStyleSheet("font: 13pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"border-color: rgb(116, 116, 116);\n"
"min-width: 10em;\n"
"padding: 5px;")
        self.PatSearLabel.setObjectName("PatSearLabel")
        self.PatNum = QtWidgets.QLineEdit(self.PatDiagWidget_1)
        self.PatNum.setGeometry(QtCore.QRect(640, 420, 250, 40))
        self.PatNum.setStyleSheet("font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-color: #FFF;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;")
        self.PatNum.setObjectName("PatNum")
        self.PatDiagErr = QtWidgets.QLabel(self.PatDiagWidget_1)
        self.PatDiagErr.setGeometry(QtCore.QRect(820, 520, 200, 18))
        self.PatDiagErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 0, 0)")
        self.PatDiagErr.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.PatDiagErr.setObjectName("PatDiagErr")
        self.PatSearLabel.raise_()
        self.PatSearBtn.raise_()
        self.PatDiagLabel.raise_()
        self.PatDiagLine.raise_()
        self.PatImg.raise_()
        self.PatNum.raise_()
        self.PatDiagErr.raise_()
        self.AccManWidget_1 = QtWidgets.QWidget(self.centralwidget)
        self.AccManWidget_1.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        self.AccManWidget_1.setObjectName("AccManWidget_1")
        self.AccManLabel_1 = QtWidgets.QLabel(self.AccManWidget_1)
        self.AccManLabel_1.setGeometry(QtCore.QRect(660, 0, 101, 31))
        self.AccManLabel_1.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);")
        self.AccManLabel_1.setAlignment(QtCore.Qt.AlignCenter)
        self.AccManLabel_1.setObjectName("AccManLabel_1")
        self.AccManLine_1 = QtWidgets.QFrame(self.AccManWidget_1)
        self.AccManLine_1.setGeometry(QtCore.QRect(10, 40, 1641, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AccManLine_1.sizePolicy().hasHeightForWidth())
        self.AccManLine_1.setSizePolicy(sizePolicy)
        self.AccManLine_1.setStyleSheet("")
        self.AccManLine_1.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.AccManLine_1.setLineWidth(0)
        self.AccManLine_1.setMidLineWidth(2)
        self.AccManLine_1.setFrameShape(QtWidgets.QFrame.HLine)
        self.AccManLine_1.setObjectName("AccManLine_1")
        self.PWEntBtn = QtWidgets.QPushButton(self.AccManWidget_1)
        self.PWEntBtn.setGeometry(QtCore.QRect(920, 420, 80, 40))
        self.PWEntBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.PWEntBtn.setStyleSheet("QPushButton {\n"
"font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;\n"
"}\n"
"QPushButton:hover {\n"
"background: qradialgradient(\n"
"cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
");\n"
"}\n"
"QPushButton:pressed {\n"
"border-style: inset;\n"
"background: qradialgradient(\n"
"cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
");\n"
"}")
        self.PWEntBtn.setObjectName("PWEntBtn")
        self.PWEntLabel = QtWidgets.QLabel(self.AccManWidget_1)
        self.PWEntLabel.setGeometry(QtCore.QRect(375, 380, 660, 120))
        self.PWEntLabel.setStyleSheet("font: 13pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 10px;\n"
"border-color: rgb(116, 116, 116);\n"
"min-width: 10em;\n"
"padding: 5px;")
        self.PWEntLabel.setObjectName("PWEntLabel")
        self.UserPWImg = QtWidgets.QLabel(self.AccManWidget_1)
        self.UserPWImg.setGeometry(QtCore.QRect(415, 416, 37, 46))
        self.UserPWImg.setStyleSheet("background-image: url(:/Image/UserPWImg.png);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.UserPWImg.setText("")
        self.UserPWImg.setObjectName("UserPWImg")
        self.PWEnt = QtWidgets.QLineEdit(self.AccManWidget_1)
        self.PWEnt.setGeometry(QtCore.QRect(640, 420, 250, 40))
        self.PWEnt.setStyleSheet("font: 10pt \"KoPub돋움체 Medium\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-color: #FFF;\n"
"border-style: outset;\n"
"border-width: 1px;\n"
"border-radius: 3px;\n"
"padding: 5px;")
        self.PWEnt.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PWEnt.setObjectName("PWEnt")
        self.AcctManErrMsg = QtWidgets.QLabel(self.AccManWidget_1)
        self.AcctManErrMsg.setGeometry(QtCore.QRect(820, 520, 200, 20))
        self.AcctManErrMsg.setStyleSheet("font: 10pt \"KoPub돋움체 Medium\";\n"
                                         "color: rgb(255, 32, 32);")
        self.AcctManErrMsg.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.AcctManErrMsg.setObjectName("AcctManErrMsg")
        self.AccManLabel_1.raise_()
        self.AccManLine_1.raise_()
        self.PWEntLabel.raise_()
        self.UserPWImg.raise_()
        self.PWEnt.raise_()
        self.PWEntBtn.raise_()
        self.AcctManErrMsg.raise_()
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(140, 290, 24, 24))
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.label_2.setStyleSheet("background-image: url(:/Image/SettingImg.png);\n"
"background-color: rgba(255, 255, 255, 0);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.NameLabel = QtWidgets.QLabel(self.centralwidget)
        self.NameLabel.setEnabled(True)
        self.NameLabel.setGeometry(QtCore.QRect(40, 340, 131, 34))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Bold")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.NameLabel.setFont(font)
        self.NameLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(85, 170, 255)\n"
"")
        self.NameLabel.setInputMethodHints(QtCore.Qt.ImhUrlCharactersOnly)
        self.NameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.NameLabel.setObjectName("NameLabel")
        self.PatRegWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.PatRegWidget_3.setEnabled(True)
        self.PatRegWidget_3.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.PatRegWidget_3.setFont(font)
        self.PatRegWidget_3.setStyleSheet("")
        self.PatRegWidget_3.setObjectName("PatRegWidget_3")
        self.PatLabel_2 = QtWidgets.QLabel(self.PatRegWidget_3)
        self.PatLabel_2.setGeometry(QtCore.QRect(645, 0, 131, 31))
        self.PatLabel_2.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
                                      "color: rgb(255, 255, 255);")
        self.PatLabel_2.setAlignment(QtCore.Qt.AlignCenter)
        self.PatLabel_2.setObjectName("PatLabel_2")
        self.PatLine_2 = QtWidgets.QFrame(self.PatRegWidget_3)
        self.PatLine_2.setGeometry(QtCore.QRect(10, 40, 1641, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PatLine_2.sizePolicy().hasHeightForWidth())
        self.PatLine_2.setSizePolicy(sizePolicy)
        self.PatLine_2.setStyleSheet("")
        self.PatLine_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.PatLine_2.setLineWidth(0)
        self.PatLine_2.setMidLineWidth(2)
        self.PatLine_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.PatLine_2.setObjectName("PatLine_2")
        self.BackBtn_2 = QtWidgets.QPushButton(self.PatRegWidget_3)
        self.BackBtn_2.setGeometry(QtCore.QRect(630, 750, 170, 50))
        self.BackBtn_2.setStyleSheet("QPushButton {\n"
                                     "font: 12pt \"KoPub돋움체 Medium\";\n"
                                     "color: rgb(255, 255, 255);\n"
                                     "background: rgb(49, 49, 49);\n"
                                     "border-style: outset;\n"
                                     "border-width: 1px;\n"
                                     "border-radius: 3px;\n"
                                     "padding: 5px;\n"
                                     "}\n"
                                     "QPushButton:hover {\n"
                                     "background: qradialgradient(\n"
                                     "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                     "radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
                                     ");\n"
                                     "}\n"
                                     "QPushButton:pressed {\n"
                                     "border-style: inset;\n"
                                     "background: qradialgradient(\n"
                                     "cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                     "radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
                                     ");\n"
                                     "}")
        self.BackBtn_2.setObjectName("BackBtn_2")
        self.SearPatInfTable = QtWidgets.QTableWidget(self.PatRegWidget_3)
        self.SearPatInfTable.setGeometry(QtCore.QRect(80, 150, 1490, 541))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SearPatInfTable.sizePolicy().hasHeightForWidth())
        self.SearPatInfTable.setSizePolicy(sizePolicy)
        self.SearPatInfTable.setMinimumSize(QtCore.QSize(0, 0))
        self.SearPatInfTable.setSizeIncrement(QtCore.QSize(0, 0))
        self.SearPatInfTable.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Medium")
        font.setPointSize(11)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.SearPatInfTable.setFont(font)
        self.SearPatInfTable.setFocusPolicy(QtCore.Qt.WheelFocus)
        self.SearPatInfTable.setStyleSheet("QWidget {\n"
                                           "color: #fff;\n"
                                           "}\n"
                                           "QHeaderView::section {\n"
                                           "    background-color: rgb(49, 49, 49);\n"
                                           "    padding: 4px;\n"
                                           "    border: 1px solid #fffff8;\n"
                                           "    font: 11pt \"KoPub돋움체 Medium\";\n"
                                           "}\n"
                                           "QTableWidget {\n"
                                           "    gridline-color: #fffff8;\n"
                                           "    font: 11pt \"KoPub돋움체 Medium\";\n"
                                           "}\n"
                                           "QTableWidget QTableCornerButton::section {\n"
                                           "    background-color: rgb(49, 49, 49);\n"
                                           "    border: 1px solid #fffff8;\n"
                                           "}font: 12pt \"KoPub돋움체 Medium\";")
        self.SearPatInfTable.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SearPatInfTable.setFrameShadow(QtWidgets.QFrame.Plain)
        self.SearPatInfTable.setLineWidth(0)
        self.SearPatInfTable.setMidLineWidth(0)
        self.SearPatInfTable.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.SearPatInfTable.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.SearPatInfTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.SearPatInfTable.setAutoScrollMargin(16)
        self.SearPatInfTable.setTabKeyNavigation(True)
        self.SearPatInfTable.setDragEnabled(False)
        self.SearPatInfTable.setDragDropOverwriteMode(True)
        self.SearPatInfTable.setDragDropMode(QtWidgets.QAbstractItemView.NoDragDrop)
        self.SearPatInfTable.setAlternatingRowColors(False)
        self.SearPatInfTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.SearPatInfTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.SearPatInfTable.setTextElideMode(QtCore.Qt.ElideRight)
        self.SearPatInfTable.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.SearPatInfTable.setShowGrid(True)
        self.SearPatInfTable.setGridStyle(QtCore.Qt.CustomDashLine)
        self.SearPatInfTable.setWordWrap(True)
        self.SearPatInfTable.setCornerButtonEnabled(True)
        self.SearPatInfTable.setRowCount(100)
        self.SearPatInfTable.setColumnCount(7)
        self.SearPatInfTable.setObjectName("SearPatInfTable")
        item = QtWidgets.QTableWidgetItem()
        self.SearPatInfTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.SearPatInfTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.SearPatInfTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.SearPatInfTable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.SearPatInfTable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.SearPatInfTable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.SearPatInfTable.setHorizontalHeaderItem(6, item)
        self.SearPatInfTable.horizontalHeader().setVisible(True)
        self.SearPatInfTable.horizontalHeader().setCascadingSectionResizes(True)
        self.SearPatInfTable.horizontalHeader().setDefaultSectionSize(200)
        self.SearPatInfTable.horizontalHeader().setHighlightSections(True)
        self.SearPatInfTable.horizontalHeader().setMinimumSectionSize(70)
        self.SearPatInfTable.horizontalHeader().setSortIndicatorShown(False)
        self.SearPatInfTable.horizontalHeader().setStretchLastSection(True)
        self.SearPatInfTable.verticalHeader().setVisible(True)
        self.SearPatInfTable.verticalHeader().setCascadingSectionResizes(False)
        self.SearPatInfTable.verticalHeader().setDefaultSectionSize(50)
        self.SearPatInfTable.verticalHeader().setHighlightSections(True)
        self.SearPatInfTable.verticalHeader().setMinimumSectionSize(50)
        self.PatDiagWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.PatDiagWidget_4.setEnabled(True)
        self.PatDiagWidget_4.setGeometry(QtCore.QRect(230, 110, 1661, 941))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Medium")
        font.setPointSize(8)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.PatDiagWidget_4.setFont(font)
        self.PatDiagWidget_4.setStyleSheet("")
        self.PatDiagWidget_4.setObjectName("PatDiagWidget_4")
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(self.PatDiagWidget_4)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(380, 130, 141, 321))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.NewPatInf_2 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.NewPatInf_2.setContentsMargins(0, 0, 0, 0)
        self.NewPatInf_2.setObjectName("NewPatInf_2")
        self.DateLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.DateLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 255, 255);")
        self.DateLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.DateLabel.setObjectName("DateLabel")
        self.NewPatInf_2.addWidget(self.DateLabel)
        self.FNCLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.FNCLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                    "color: rgb(255, 255, 255);")
        self.FNCLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.FNCLabel.setObjectName("FNCLabel")
        self.NewPatInf_2.addWidget(self.FNCLabel)
        self.SBMLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.SBMLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                    "color: rgb(255, 255, 255);")
        self.SBMLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.SBMLabel.setObjectName("SBMLabel")
        self.NewPatInf_2.addWidget(self.SBMLabel)
        self.EEGLabel = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.EEGLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                    "color: rgb(255, 255, 255);")
        self.EEGLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.EEGLabel.setObjectName("EEGLabel")
        self.NewPatInf_2.addWidget(self.EEGLabel)
        self.DataLabel = QtWidgets.QLabel(self.PatDiagWidget_4)
        self.DataLabel.setGeometry(QtCore.QRect(625, 0, 171, 31))
        self.DataLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
                                     "color: rgb(255, 255, 255);")
        self.DataLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.DataLabel.setObjectName("DataLabel")
        self.DataLine = QtWidgets.QFrame(self.PatDiagWidget_4)
        self.DataLine.setGeometry(QtCore.QRect(10, 40, 1641, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DataLine.sizePolicy().hasHeightForWidth())
        self.DataLine.setSizePolicy(sizePolicy)
        self.DataLine.setStyleSheet("")
        self.DataLine.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.DataLine.setLineWidth(0)
        self.DataLine.setMidLineWidth(2)
        self.DataLine.setFrameShape(QtWidgets.QFrame.HLine)
        self.DataLine.setObjectName("DataLine")
        self.EEGData = QtWidgets.QLineEdit(self.PatDiagWidget_4)
        self.EEGData.setGeometry(QtCore.QRect(540, 390, 350, 50))
        self.EEGData.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(49, 49, 49);\n"
                                   "border: 1px solid rgb(198, 198, 198);\n"
                                   "border-radius: 3px;\n"
                                   "padding: 4px;\n"
                                   "")
        self.EEGData.setText("")
        self.EEGData.setObjectName("EEGData")
        self.FNCData = QtWidgets.QLineEdit(self.PatDiagWidget_4)
        self.FNCData.setGeometry(QtCore.QRect(540, 224, 350, 50))
        self.FNCData.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(49, 49, 49);\n"
                                   "border: 1px solid rgb(198, 198, 198);\n"
                                   "border-radius: 3px;\n"
                                   "padding: 4px;\n"
                                   "")
        self.FNCData.setText("")
        self.FNCData.setObjectName("FNCData")
        self.SBMData = QtWidgets.QLineEdit(self.PatDiagWidget_4)
        self.SBMData.setGeometry(QtCore.QRect(540, 307, 350, 50))
        self.SBMData.setStyleSheet("font: 12pt \"KoPub돋움체 Bold\";\n"
                                   "color: rgb(255, 255, 255);\n"
                                   "background-color: rgb(49, 49, 49);\n"
                                   "border: 1px solid rgb(198, 198, 198);\n"
                                   "border-radius: 3px;\n"
                                   "padding: 4px;")
        self.SBMData.setText("")
        self.SBMData.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.SBMData.setObjectName("SBMData")
        self.DataOkBtn = QtWidgets.QPushButton(self.PatDiagWidget_4)
        self.DataOkBtn.setGeometry(QtCore.QRect(540, 510, 170, 50))
        self.DataOkBtn.setStyleSheet("QPushButton {\n"
                                     "font: 12pt \"KoPub돋움체 Bold\";\n"
                                     "color: #333;\n"
                                     "border-radius: 3px;\n"
                                     "padding: 5px;\n"
                                     "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
                                     "fx: 0.3, fy: -0.4,\n"
                                     "radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
                                     "min-width: 80px;\n"
                                     "}\n"
                                     "QPushButton:hover {\n"
                                     "background: qradialgradient(\n"
                                     "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                     "radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
                                     ");\n"
                                     "color: #FFF;\n"
                                     "}\n"
                                     "QPushButton:pressed {\n"
                                     "border-style: inset;\n"
                                     "background: qradialgradient(\n"
                                     "cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                     "radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
                                     ");\n"
                                     "}")
        self.DataOkBtn.setObjectName("DataOkBtn")
        self.DataOkBtn.clicked.connect(self.InsData)
        self.DataCanBtn = QtWidgets.QPushButton(self.PatDiagWidget_4)
        self.DataCanBtn.setGeometry(QtCore.QRect(720, 510, 170, 50))
        self.DataCanBtn.setStyleSheet("QPushButton {\n"
                                      "font: 12pt \"KoPub돋움체 Bold\";\n"
                                      "color: #333;\n"
                                      "border-radius: 3px;\n"
                                      "padding: 5px;\n"
                                      "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
                                      "fx: 0.3, fy: -0.4,\n"
                                      "radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
                                      "min-width: 80px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "background: qradialgradient(\n"
                                      "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                      "radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
                                      ");\n"
                                      "color: #FFF;\n"
                                      "}\n"
                                      "QPushButton:pressed {\n"
                                      "border-style: inset;\n"
                                      "background: qradialgradient(\n"
                                      "cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                      "radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
                                      ");\n"
                                      "}")
        self.DataCanBtn.setObjectName("DataCanBtn")
        self.DataCanBtn.clicked.connect(self.PatDiagWidget_2.show)
        self.FNCDataErr = QtWidgets.QLabel(self.PatDiagWidget_4)
        self.FNCDataErr.setGeometry(QtCore.QRect(1047, 240, 200, 18))
        self.FNCDataErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 0, 0)")
        self.FNCDataErr.setObjectName("FNCDataErr")
        self.SBMDataErr = QtWidgets.QLabel(self.PatDiagWidget_4)
        self.SBMDataErr.setGeometry(QtCore.QRect(1047, 323, 200, 18))
        self.SBMDataErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 0, 0)")
        self.SBMDataErr.setObjectName("SBMDataErr")
        self.EEGDataErr = QtWidgets.QLabel(self.PatDiagWidget_4)
        self.EEGDataErr.setGeometry(QtCore.QRect(1047, 405, 200, 18))
        self.EEGDataErr.setStyleSheet("font: 9pt \"KoPub돋움체 Medium\";\n"
                                      "color: rgb(255, 0, 0)")
        self.EEGDataErr.setObjectName("EEGDataErr")
        self.FNCFileBtn = QtWidgets.QPushButton(self.PatDiagWidget_4)
        self.FNCFileBtn.setGeometry(QtCore.QRect(910, 230, 120, 40))
        self.FNCFileBtn.setStyleSheet("QPushButton {\n"
                                      "font: 10pt \"KoPub돋움체 Medium\";\n"
                                      "color: #333;\n"
                                      "border-radius: 3px;\n"
                                      "padding: 5px;\n"
                                      "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
                                      "fx: 0.3, fy: -0.4,\n"
                                      "radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
                                      "min-width: 80px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "background: qradialgradient(\n"
                                      "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                      "radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
                                      ");\n"
                                      "color: #FFF;\n"
                                      "}\n"
                                      "QPushButton:pressed {\n"
                                      "border-style: inset;\n"
                                      "background: qradialgradient(\n"
                                      "cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                      "radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
                                      ");\n"
                                      "}")
        self.FNCFileBtn.setObjectName("FNCFileBtn")
        self.FNCFileBtn.clicked.connect(self.OpenFNCFile)
        self.EEGFileBtn = QtWidgets.QPushButton(self.PatDiagWidget_4)
        self.EEGFileBtn.setGeometry(QtCore.QRect(910, 395, 120, 40))
        self.EEGFileBtn.setStyleSheet("QPushButton {\n"
                                      "font: 10pt \"KoPub돋움체 Medium\";\n"
                                      "color: #333;\n"
                                      "border-radius: 3px;\n"
                                      "padding: 5px;\n"
                                      "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
                                      "fx: 0.3, fy: -0.4,\n"
                                      "radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
                                      "min-width: 80px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "background: qradialgradient(\n"
                                      "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                      "radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
                                      ");\n"
                                      "color: #FFF;\n"
                                      "}\n"
                                      "QPushButton:pressed {\n"
                                      "border-style: inset;\n"
                                      "background: qradialgradient(\n"
                                      "cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                      "radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
                                      ");\n"
                                      "}")
        self.EEGFileBtn.setObjectName("EEGFileBtn")
        self.EEGFileBtn.clicked.connect(self.OpenEEGFile)
        self.SBMFileBtn = QtWidgets.QPushButton(self.PatDiagWidget_4)
        self.SBMFileBtn.setGeometry(QtCore.QRect(910, 312, 120, 40))
        self.SBMFileBtn.setStyleSheet("QPushButton {\n"
                                      "font: 10pt \"KoPub돋움체 Medium\";\n"
                                      "color: #333;\n"
                                      "border-radius: 3px;\n"
                                      "padding: 5px;\n"
                                      "background: qradialgradient(cx: 0.3, cy: -0.4,\n"
                                      "fx: 0.3, fy: -0.4,\n"
                                      "radius: 3, stop: 0 #fff, stop: 1 rgb(191, 191, 191));\n"
                                      "min-width: 80px;\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "background: qradialgradient(\n"
                                      "cx: 0.3, cy: -0.4, fx: 0.3, fy: -0.4,\n"
                                      "radius: 1.35, stop: 0 #fff, stop: 1 #888\n"
                                      ");\n"
                                      "color: #FFF;\n"
                                      "}\n"
                                      "QPushButton:pressed {\n"
                                      "border-style: inset;\n"
                                      "background: qradialgradient(\n"
                                      "cx: 0.4, cy: -0.1, fx: 0.4, fy: -0.1,\n"
                                      "radius: 1.35, stop: 0 #fff, stop: 1 #aaa\n"
                                      ");\n"
                                      "}")
        self.SBMFileBtn.setObjectName("SBMFileBtn")
        self.SBMFileBtn.clicked.connect(self.OpenSBMFile)
        self.ComeDate = QtWidgets.QDateEdit(self.PatDiagWidget_4)
        self.ComeDate.setGeometry(QtCore.QRect(540, 140, 350, 50))
        font = QtGui.QFont()
        font.setFamily("KoPub돋움체 Medium")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.ComeDate.setFont(font)
        self.ComeDate.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                    "color: rgb(255, 255, 255);\n"
                                    "border: 1px solid rgb(198, 198, 198);;\n"
                                    "border-radius: 3px;")
        self.ComeDate.setFrame(False)
        self.ComeDate.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.ComeDate.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToPreviousValue)
        self.ComeDate.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 1, 1), QtCore.QTime(0, 0, 0)))
        self.ComeDate.setMaximumDateTime(QtCore.QDateTime(QtCore.QDate(7999, 12, 31), QtCore.QTime(23, 59, 59)))
        self.ComeDate.setCalendarPopup(True)
        self.ComeDate.setObjectName("ComeDate")
        self.HomeBtn = QtWidgets.QPushButton(self.centralwidget)
        self.HomeBtn.setGeometry(QtCore.QRect(215, 41, 126, 26))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.HomeBtn.sizePolicy().hasHeightForWidth())
        self.HomeBtn.setSizePolicy(sizePolicy)
        self.HomeBtn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.HomeBtn.setStyleSheet("QPushButton {\n"
"font: 12pt \"KoPub돋움체 Bold\";\n"
"color: rgb(255, 255, 255);\n"
"background: rgb(49, 49, 49);\n"
"border-style: outset;\n"
"}\n"
"QPushButton:hover {\n"
"color: rgb(85, 170, 255);\n"
"}")
        self.HomeBtn.setObjectName("HomeBtn")
        self.UserImage.raise_()
        self.HorizontalLine.raise_()
        self.Logo.raise_()
        self.horizontalLayoutWidget.raise_()
        self.VerticalLine.raise_()
        self.label_2.raise_()
        self.NameLabel.raise_()
        self.HomeBtn.raise_()
        self.AccManWidget_2.raise_()
        self.AccManWidget_1.raise_()
        self.PatDiagWidget_4.raise_()
        self.PatDiagWidget_3.raise_()
        self.PatDiagWidget_2.raise_()
        self.PatDiagWidget_1.raise_()
        self.PatRegWidget_3.raise_()
        self.PatRegWidget_2.raise_()
        self.PatRegWidget_1.raise_()
        self.HomeWidget.raise_()
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.HomeBtn.clicked.connect(self.HomeWidget.show)
        self.AccManBtn.clicked.connect(self.AccManWidget_1.show)
        self.PatRegBtn.clicked.connect(self.HomeWidget.hide)
        self.PatDiagBtn.clicked.connect(self.HomeWidget.hide)
        self.AccManBtn.clicked.connect(self.HomeWidget.hide)
        self.PatRegBtn.clicked.connect(self.PatRegWidget_1.show)
        self.PatRegBtn.clicked.connect(self.PatSearInitialize)
        self.AccManBtn.clicked.connect(self.PatRegWidget_1.hide)
        self.PatDiagBtn.clicked.connect(self.PatRegWidget_1.hide)
        self.NewPatBtn.clicked.connect(self.PatRegWidget_2.show)
        self.NewPatBtn.clicked.connect(self.HomeWidget.hide)
        self.NewPatBtn.clicked.connect(self.PatRegWidget_1.hide)
        self.NewPatBtn.clicked.connect(self.PatRegInitialize)
        self.AccManBtn.clicked.connect(self.PatRegWidget_2.hide)
        self.PatDiagBtn.clicked.connect(self.PatRegWidget_2.hide)
        self.PatDiagBtn.clicked.connect(self.PatDiagWidget_1.show)
        self.PatDiagBtn.clicked.connect(self.PatDiagInitialize)
        self.AccManBtn.clicked.connect(self.PatDiagWidget_1.hide)
        self.AccManBtn.clicked.connect(self.PatDiagWidget_2.hide)
        self.ResCmpBtn.clicked.connect(self.PatDiagWidget_3.show)
        self.ResCmpBtn.clicked.connect(self.HomeWidget.hide)
        self.ResCmpBtn.clicked.connect(self.PatRegWidget_1.hide)
        self.ResCmpBtn.clicked.connect(self.PatRegWidget_2.hide)
        self.ResCmpBtn.clicked.connect(self.PatDiagWidget_2.hide)
        self.ResCmpBtn.clicked.connect(self.ResCmpGraph)
        self.AccManBtn.clicked.connect(self.PatDiagWidget_3.hide)
        self.AccManBtn.clicked.connect(self.AccManInitialize)
        self.BackBtn.clicked.connect(self.PatDiagWidget_2.show)
        self.PatDiagBtn.clicked.connect(self.PatRegWidget_3.hide)
        self.AccManBtn.clicked.connect(self.PatRegWidget_3.hide)
        self.BackBtn_2.clicked.connect(self.PatRegWidget_1.show)
        self.BackBtn_2.clicked.connect(self.PatSearInitialize)
        self.BackBtn_2.clicked.connect(self.PatTableInitialize)
        self.DataRegBtn.clicked.connect(self.PatDiagWidget_4.show)
        self.DataRegBtn.clicked.connect(self.PatDiagWidget_3.hide)
        self.DataRegBtn.clicked.connect(self.PatDiagWidget_2.hide)
        self.DataRegBtn.clicked.connect(self.PatDiagWidget_1.hide)
        self.DataRegBtn.clicked.connect(self.PatRegWidget_3.hide)
        self.DataRegBtn.clicked.connect(self.PatRegWidget_2.hide)
        self.DataRegBtn.clicked.connect(self.PatRegWidget_1.hide)
        self.DataRegBtn.clicked.connect(self.HomeWidget.hide)
        self.DataRegBtn.clicked.connect(self.DataInitialize)
        self.AccManBtn.clicked.connect(self.PatDiagWidget_4.hide)
        self.PWEntBtn.clicked.connect(self.PatDiagWidget_4.hide)

        # 채널 버튼 이벤트 처리
        self.AF3_Btn.clicked.connect(self.AF3_Btn_clicked)
        self.AF4_Btn.clicked.connect(self.AF4_Btn_clicked)
        self.AF7_Btn.clicked.connect(self.AF7_Btn_clicked)
        self.AF8_Btn.clicked.connect(self.AF8_Btn_clicked)
        self.AFz_Btn.clicked.connect(self.AFz_Btn_clicked)
        self.C1_Btn.clicked.connect(self.C1_Btn_clicked)
        self.C2_Btn.clicked.connect(self.C2_Btn_clicked)
        self.C3_Btn.clicked.connect(self.C3_Btn_clicked)
        self.C4_Btn.clicked.connect(self.C4_Btn_clicked)
        self.C5_Btn.clicked.connect(self.C5_Btn_clicked)
        self.C6_Btn.clicked.connect(self.C6_Btn_clicked)
        self.CP1_Btn.clicked.connect(self.CP1_Btn_clicked)
        self.CP2_Btn.clicked.connect(self.CP2_Btn_clicked)
        self.CP3_Btn.clicked.connect(self.CP3_Btn_clicked)
        self.CP4_Btn.clicked.connect(self.CP4_Btn_clicked)
        self.CP5_Btn.clicked.connect(self.CP5_Btn_clicked)
        self.CP6_Btn.clicked.connect(self.CP6_Btn_clicked)
        self.CPz_Btn.clicked.connect(self.CPz_Btn_clicked)
        self.Cz_Btn.clicked.connect(self.Cz_Btn_clicked)
        self.F1_Btn.clicked.connect(self.F1_Btn_clicked)
        self.F2_Btn.clicked.connect(self.F2_Btn_clicked)
        self.F3_Btn.clicked.connect(self.F3_Btn_clicked)
        self.F4_Btn.clicked.connect(self.F4_Btn_clicked)
        self.F5_Btn.clicked.connect(self.F5_Btn_clicked)
        self.F6_Btn.clicked.connect(self.F6_Btn_clicked)
        self.F7_Btn.clicked.connect(self.F7_Btn_clicked)
        self.F8_Btn.clicked.connect(self.F8_Btn_clicked)
        self.FC1_Btn.clicked.connect(self.FC1_Btn_clicked)
        self.FC2_Btn.clicked.connect(self.FC2_Btn_clicked)
        self.FC3_Btn.clicked.connect(self.FC3_Btn_clicked)
        self.FC4_Btn.clicked.connect(self.FC4_Btn_clicked)
        self.FC5_Btn.clicked.connect(self.FC5_Btn_clicked)
        self.FC6_Btn.clicked.connect(self.FC6_Btn_clicked)
        self.FCz_Btn.clicked.connect(self.FCz_Btn_clicked)
        self.FT7_Btn.clicked.connect(self.FT7_Btn_clicked)
        self.FT8_Btn.clicked.connect(self.FT8_Btn_clicked)
        self.Fp1_Btn.clicked.connect(self.Fp1_Btn_clicked)
        self.Fp2_Btn.clicked.connect(self.Fp2_Btn_clicked)
        self.Fpz_Btn.clicked.connect(self.Fpz_Btn_clicked)
        self.Fz_Btn.clicked.connect(self.Fz_Btn_clicked)
        self.O1_Btn.clicked.connect(self.O1_Btn_clicked)
        self.O2_Btn.clicked.connect(self.O2_Btn_clicked)
        self.Oz_Btn.clicked.connect(self.Oz_Btn_clicked)
        self.P1_Btn.clicked.connect(self.P1_Btn_clicked)
        self.P2_Btn.clicked.connect(self.P2_Btn_clicked)
        self.P3_Btn.clicked.connect(self.P3_Btn_clicked)
        self.P4_Btn.clicked.connect(self.P4_Btn_clicked)
        self.P5_Btn.clicked.connect(self.P5_Btn_clicked)
        self.P6_Btn.clicked.connect(self.P6_Btn_clicked)
        self.P7_Btn.clicked.connect(self.P7_Btn_clicked)
        self.P8_Btn.clicked.connect(self.P8_Btn_clicked)
        self.PO3_Btn.clicked.connect(self.PO3_Btn_clicked)
        self.PO4_Btn.clicked.connect(self.PO4_Btn_clicked)
        self.PO7_Btn.clicked.connect(self.PO7_Btn_clicked)
        self.PO8_Btn.clicked.connect(self.PO8_Btn_clicked)
        self.POz_Btn.clicked.connect(self.POz_Btn_clicked)
        self.Pz_Btn.clicked.connect(self.Pz_Btn_clicked)
        self.T7_Btn.clicked.connect(self.T7_Btn_clicked)
        self.T8_Btn.clicked.connect(self.T8_Btn_clicked)
        self.TP7_Btn.clicked.connect(self.TP7_Btn_clicked)
        self.TP8_Btn.clicked.connect(self.TP8_Btn_clicked)

        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.HomeBtn, self.PatRegBtn)
        MainWindow.setTabOrder(self.PatRegBtn, self.PatDiagBtn)
        MainWindow.setTabOrder(self.PatDiagBtn, self.AccManBtn)
        MainWindow.setTabOrder(self.AccManBtn, self.NewPatBtn)
        MainWindow.setTabOrder(self.NewPatBtn, self.ExiPatNum)
        MainWindow.setTabOrder(self.ExiPatNum, self.ExiPatBtn)
        MainWindow.setTabOrder(self.ExiPatBtn, self.PatRegNum)
        MainWindow.setTabOrder(self.PatRegNum, self.PatName)
        MainWindow.setTabOrder(self.PatName, self.PatBirth)
        MainWindow.setTabOrder(self.PatBirth, self.PatMBtn)
        MainWindow.setTabOrder(self.PatMBtn, self.PatFBtn)
        MainWindow.setTabOrder(self.PatFBtn, self.PatHCBtn)
        MainWindow.setTabOrder(self.PatHCBtn, self.PatSZBtn)
        MainWindow.setTabOrder(self.PatSZBtn, self.PatPenBtn)
        MainWindow.setTabOrder(self.PatPenBtn, self.PatPhone)
        MainWindow.setTabOrder(self.PatPhone, self.PatDocID)
        MainWindow.setTabOrder(self.PatDocID, self.PatOkBtn)
        MainWindow.setTabOrder(self.PatOkBtn, self.PatCanBtn)
        MainWindow.setTabOrder(self.PatCanBtn, self.PatNum)
        MainWindow.setTabOrder(self.PatNum, self.PatSearBtn)
        MainWindow.setTabOrder(self.PatSearBtn, self.DataRegBtn)
        MainWindow.setTabOrder(self.DataRegBtn, self.ResultBtn)
        MainWindow.setTabOrder(self.ResultBtn, self.ResCmpBtn)
        MainWindow.setTabOrder(self.ResCmpBtn, self.PatientInfoTable)
        MainWindow.setTabOrder(self.PatientInfoTable, self.PO8_Btn)
        MainWindow.setTabOrder(self.PO8_Btn, self.PO4_Btn)
        MainWindow.setTabOrder(self.PO4_Btn, self.O2_Btn)
        MainWindow.setTabOrder(self.O2_Btn, self.P8_Btn)
        MainWindow.setTabOrder(self.P8_Btn, self.P6_Btn)
        MainWindow.setTabOrder(self.P6_Btn, self.P4_Btn)
        MainWindow.setTabOrder(self.P4_Btn, self.Oz_Btn)
        MainWindow.setTabOrder(self.Oz_Btn, self.POz_Btn)
        MainWindow.setTabOrder(self.POz_Btn, self.P2_Btn)
        MainWindow.setTabOrder(self.P2_Btn, self.Pz_Btn)
        MainWindow.setTabOrder(self.Pz_Btn, self.O1_Btn)
        MainWindow.setTabOrder(self.O1_Btn, self.PO3_Btn)
        MainWindow.setTabOrder(self.PO3_Btn, self.P1_Btn)
        MainWindow.setTabOrder(self.P1_Btn, self.PO7_Btn)
        MainWindow.setTabOrder(self.PO7_Btn, self.P3_Btn)
        MainWindow.setTabOrder(self.P3_Btn, self.P5_Btn)
        MainWindow.setTabOrder(self.P5_Btn, self.P7_Btn)
        MainWindow.setTabOrder(self.P7_Btn, self.C6_Btn)
        MainWindow.setTabOrder(self.C6_Btn, self.CP6_Btn)
        MainWindow.setTabOrder(self.CP6_Btn, self.CP4_Btn)
        MainWindow.setTabOrder(self.CP4_Btn, self.C4_Btn)
        MainWindow.setTabOrder(self.C4_Btn, self.CP2_Btn)
        MainWindow.setTabOrder(self.CP2_Btn, self.C2_Btn)
        MainWindow.setTabOrder(self.C2_Btn, self.CPz_Btn)
        MainWindow.setTabOrder(self.CPz_Btn, self.Cz_Btn)
        MainWindow.setTabOrder(self.Cz_Btn, self.CP1_Btn)
        MainWindow.setTabOrder(self.CP1_Btn, self.C1_Btn)
        MainWindow.setTabOrder(self.C1_Btn, self.C3_Btn)
        MainWindow.setTabOrder(self.C3_Btn, self.CP3_Btn)
        MainWindow.setTabOrder(self.CP3_Btn, self.FT8_Btn)
        MainWindow.setTabOrder(self.FT8_Btn, self.FC6_Btn)
        MainWindow.setTabOrder(self.FC6_Btn, self.FC4_Btn)
        MainWindow.setTabOrder(self.FC4_Btn, self.FC2_Btn)
        MainWindow.setTabOrder(self.FC2_Btn, self.CP5_Btn)
        MainWindow.setTabOrder(self.CP5_Btn, self.TP7_Btn)
        MainWindow.setTabOrder(self.TP7_Btn, self.C5_Btn)
        MainWindow.setTabOrder(self.C5_Btn, self.T7_Btn)
        MainWindow.setTabOrder(self.T7_Btn, self.FCz_Btn)
        MainWindow.setTabOrder(self.FCz_Btn, self.FC1_Btn)
        MainWindow.setTabOrder(self.FC1_Btn, self.FC3_Btn)
        MainWindow.setTabOrder(self.FC3_Btn, self.FC5_Btn)
        MainWindow.setTabOrder(self.FC5_Btn, self.FT7_Btn)
        MainWindow.setTabOrder(self.FT7_Btn, self.Fz_Btn)
        MainWindow.setTabOrder(self.Fz_Btn, self.AFz_Btn)
        MainWindow.setTabOrder(self.AFz_Btn, self.F2_Btn)
        MainWindow.setTabOrder(self.F2_Btn, self.F4_Btn)
        MainWindow.setTabOrder(self.F4_Btn, self.F6_Btn)
        MainWindow.setTabOrder(self.F6_Btn, self.F8_Btn)
        MainWindow.setTabOrder(self.F8_Btn, self.AF8_Btn)
        MainWindow.setTabOrder(self.AF8_Btn, self.AF4_Btn)
        MainWindow.setTabOrder(self.AF4_Btn, self.Fp2_Btn)
        MainWindow.setTabOrder(self.Fp2_Btn, self.Fpz_Btn)
        MainWindow.setTabOrder(self.Fpz_Btn, self.F1_Btn)
        MainWindow.setTabOrder(self.F1_Btn, self.F3_Btn)
        MainWindow.setTabOrder(self.F3_Btn, self.AF3_Btn)
        MainWindow.setTabOrder(self.AF3_Btn, self.Fp1_Btn)
        MainWindow.setTabOrder(self.Fp1_Btn, self.AF7_Btn)
        MainWindow.setTabOrder(self.AF7_Btn, self.F5_Btn)
        MainWindow.setTabOrder(self.F5_Btn, self.F7_Btn)
        MainWindow.setTabOrder(self.F7_Btn, self.TP8_Btn)
        MainWindow.setTabOrder(self.TP8_Btn, self.T8_Btn)
        MainWindow.setTabOrder(self.T8_Btn, self.BackBtn)
        MainWindow.setTabOrder(self.BackBtn, self.PWEnt)
        MainWindow.setTabOrder(self.PWEnt, self.PWEntBtn)
        MainWindow.setTabOrder(self.PWEntBtn, self.UserID)
        MainWindow.setTabOrder(self.UserID, self.UserPW)
        MainWindow.setTabOrder(self.UserPW, self.UserPWCheck)
        MainWindow.setTabOrder(self.UserPWCheck, self.UserName)
        MainWindow.setTabOrder(self.UserName, self.UserBirth)
        MainWindow.setTabOrder(self.UserBirth, self.UserMBtn)
        MainWindow.setTabOrder(self.UserMBtn, self.UserFBtn)
        MainWindow.setTabOrder(self.UserFBtn, self.UserPhone)
        MainWindow.setTabOrder(self.UserPhone, self.UserHos)
        MainWindow.setTabOrder(self.UserHos, self.UserDep)
        MainWindow.setTabOrder(self.UserDep, self.UserSubBtn_Ok)
        MainWindow.setTabOrder(self.UserSubBtn_Ok, self.UserSubBtn_Cancel)
        MainWindow.setTabOrder(self.UserSubBtn_Cancel, self.UserWDBtn)
        MainWindow.setTabOrder(self.ComeDate, self.FNCData)
        MainWindow.setTabOrder(self.FNCData, self.SBMData)
        MainWindow.setTabOrder(self.SBMData, self.EEGData)

        self.ExiPatBtn.clicked.connect(self.ExiPatBtn_clicked)  # 환자 조회 버튼 이벤트 처리
        self.ResultBtn.clicked.connect(self.ResultBtn_clicked)  # 환자 진단 결과 보기 버튼 이벤트 처리
        self.PatSearBtn.clicked.connect(self.pat_diag_clicked)  # 환자 등록번호 입력 이벤트 처리
        self.PatSearBtn.clicked.connect(self.Fz_Btn_clicked)  # 환자 Fz 그래프
        self.PWEntBtn.clicked.connect(self.acct_man_clicked)  # 의사 계정관리 비밀번호 입력 이벤트 처리

    # 환자 조회 버튼 이벤트 처리
    def ExiPatBtn_clicked(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        # 빈 정보를 입력했을 때
        if not self.ExiPatNum.text():
            self.PatSearErr.setText(_translate("MainWindow", "이름을 입력해주세요."))
        # 입력 값과 DB의 계정 정보 비교
        else:
            with conn.cursor() as curs:
                global name
                name = self.ExiPatNum.text()
                sql = "SELECT EXISTS(SELECT * FROM mydb.subject_info WHERE name = '%s')" % name
                curs.execute(sql)
                rs = curs.fetchall()
                for row in rs:
                    # 등록된 환자가 없는 경우
                    if row[0] == 0:
                        self.PatSearErr.setText(_translate("MainWindow", "등록된 환자가 없습니다."))
                    # 등록된 환자가 있는 경우
                    else:
                        self.PatRegWidget_3.show()
                        self.HomeWidget.hide()
                        self.PatRegWidget_1.hide()
                        self.PatRegWidget_2.hide()
                        self.showRegPatInf()  # 등록된 환자 정보 출력 이벤트

    # 등록된 환자 정보 출력 이벤트
    def showRegPatInf(self):
        _translate = QtCore.QCoreApplication.translate

        with conn.cursor() as curs:
            sql = "SELECT * FROM mydb.subject_info WHERE name = '%s'" % name
            curs.execute(sql)
            rs = curs.fetchall()
            col = 0
            for res1 in rs:
                row = 0
                for res2 in res1:
                    item = QtWidgets.QTableWidgetItem()
                    self.SearPatInfTable.setItem(col, row, item)
                    item = self.SearPatInfTable.item(col, row)
                    if row == 4:
                        if res2 == '0':
                            item.setText(_translate("MainWindow", "HC"))
                        elif res2 == '1':
                            item.setText(_translate("MainWindow", "SZ"))
                        else:
                            item.setText(_translate("MainWindow", "Pending"))
                    else:
                        item.setText(_translate("MainWindow", res2))

                    row += 1
                col += 1

    # 환자 조회 테이블 초기화
    def PatTableInitialize(self):
        with conn.cursor() as curs:
            sql = "SELECT * FROM mydb.subject_info WHERE name = '%s'" % name
            curs.execute(sql)
            rs = curs.fetchall()
            col = 0
            for res1 in rs:
                row = 0
                for res2 in res1:
                    item = QtWidgets.QTableWidgetItem()
                    self.SearPatInfTable.setItem(col, row, item)
                    item = self.SearPatInfTable.item(col, row)
                    item.setText("")

                    row += 1
                col += 1

    # 환자 진단 결과 보기 버튼 이벤트 처리
    def ResultBtn_clicked(self):
        _translate = QtCore.QCoreApplication.translate

        global fnc_data
        global sbm_data
        global come_date

        if fnc_data == "":
            self.ResShowErr.setText(_translate("MainWindow", "데이터를 먼저 등록해주세요."))
        elif sbm_data == "":
            self.ResShowErr.setText(_translate("MainWindow", "데이터를 먼저 등록해주세요."))
        else:
            with conn.cursor() as cur:
                sql1 = "SELECT EXISTS(SELECT * FROM mydb.diagnose_record WHERE subject_id = '%s' and come_date = '%s')" % (patId, come_date)
                cur.execute(sql1)
                rs = cur.fetchall()
                for row in rs:
                    # 이미 등록된 번호일 경우
                    if row[0] == 1:
                        self.ResShowErr.setText(_translate("MainWindow", "진단 내역이 존재합니다."))
                    else:
                        self.ResShowErr.setText(_translate("MainWindow", ""))
                        ids, data, labels = load_data()
                        clf = svm.SVC().fit(data, labels)
                        a = write_predictions(clf)
                        c = write_results(clf)

                        b = round(a[-1]*100, 2)
                        self.PerLabel_1.setText(str(b))

                        with conn.cursor() as cur:
                            data = cur.execute("INSERT INTO mydb.diagnose_record(subject_id, come_date, result) VALUES('%s', '%s', '%s')" % (patId, come_date, b))
                            conn.commit()

                        # DB 바꿔주는 코드 삽입 필요

                            subId = patId + come_date.split('-')[0] + come_date.split('-')[1] + come_date.split('-')[2]

                        with conn.cursor() as cur:
                            data = cur.execute("INSERT INTO mydb.train_labels(subject_id, class) VALUES('%s', '%s')" % (subId, c[0]))
                            conn.commit()

                            f = open(fnc_data, 'r')
                            csvReader = csv.reader(f)

                            for row in csvReader:
                                data = []
                                num = 1
                                for col in row:
                                    if num < 379:
                                        data.append(row[num])
                                        num = num + 1

                            data1 = cur.execute(
                                "INSERT INTO mydb.train_fnc(subject_id, FNC1, FNC2, FNC3, FNC4, FNC5, FNC6, FNC7, FNC8, FNC9, FNC10," \
                                "FNC11, FNC12, FNC13, FNC14, FNC15, FNC16, FNC17, FNC18, FNC19, FNC20, FNC21, FNC22, FNC23, FNC24, FNC25," \
                                "FNC26, FNC27, FNC28, FNC29, FNC30, FNC31, FNC32, FNC33, FNC34, FNC35, FNC36, FNC37, FNC38, FNC39, FNC40," \
                                "FNC41, FNC42, FNC43, FNC44, FNC45, FNC46, FNC47, FNC48, FNC49, FNC50, FNC51, FNC52, FNC53, FNC54, FNC55," \
                                "FNC56, FNC57, FNC58, FNC59, FNC60, FNC61, FNC62, FNC63, FNC64, FNC65, FNC66, FNC67, FNC68, FNC69, FNC70," \
                                "FNC71, FNC72, FNC73, FNC74, FNC75, FNC76, FNC77, FNC78, FNC79, FNC80, FNC81, FNC82, FNC83, FNC84, FNC85," \
                                "FNC86, FNC87, FNC88, FNC89, FNC90, FNC91, FNC92, FNC93, FNC94, FNC95, FNC96, FNC97, FNC98, FNC99, FNC100," \
                                "FNC101, FNC102, FNC103, FNC104, FNC105, FNC106, FNC107, FNC108, FNC109, FNC110, FNC111, FNC112, FNC113, FNC114, FNC115," \
                                "FNC116, FNC117, FNC118, FNC119, FNC120, FNC121, FNC122, FNC123, FNC124, FNC125, FNC126, FNC127, FNC128, FNC129, FNC130," \
                                "FNC131, FNC132, FNC133, FNC134, FNC135, FNC136, FNC137, FNC138, FNC139, FNC140, FNC141, FNC142, FNC143, FNC144, FNC145," \
                                "FNC146, FNC147, FNC148, FNC149, FNC150, FNC151, FNC152, FNC153, FNC154, FNC155, FNC156, FNC157, FNC158, FNC159, FNC160," \
                                "FNC161, FNC162, FNC163, FNC164, FNC165, FNC166, FNC167, FNC168, FNC169, FNC170, FNC171, FNC172, FNC173, FNC174, FNC175," \
                                "FNC176, FNC177, FNC178, FNC179, FNC180, FNC181, FNC182, FNC183, FNC184, FNC185, FNC186, FNC187, FNC188, FNC189, FNC190," \
                                "FNC191, FNC192, FNC193, FNC194, FNC195, FNC196, FNC197, FNC198, FNC199, FNC200, FNC201, FNC202, FNC203, FNC204, FNC205," \
                                "FNC206, FNC207, FNC208, FNC209, FNC210, FNC211, FNC212, FNC213, FNC214, FNC215, FNC216, FNC217, FNC218, FNC219, FNC220," \
                                "FNC221, FNC222, FNC223, FNC224, FNC225, FNC226, FNC227, FNC228, FNC229, FNC230, FNC231, FNC232, FNC233, FNC234, FNC235," \
                                "FNC236, FNC237, FNC238, FNC239, FNC240, FNC241, FNC242, FNC243, FNC244, FNC245, FNC246, FNC247, FNC248, FNC249, FNC250," \
                                "FNC251, FNC252, FNC253, FNC254, FNC255, FNC256, FNC257, FNC258, FNC259, FNC260, FNC261, FNC262, FNC263, FNC264, FNC265," \
                                "FNC266, FNC267, FNC268, FNC269, FNC270, FNC271, FNC272, FNC273, FNC274, FNC275, FNC276, FNC277, FNC278, FNC279, FNC280," \
                                "FNC281, FNC282, FNC283, FNC284, FNC285, FNC286, FNC287, FNC288, FNC289, FNC290, FNC291, FNC292, FNC293, FNC294, FNC295," \
                                "FNC296, FNC297, FNC298, FNC299, FNC300, FNC301, FNC302, FNC303, FNC304, FNC305, FNC306, FNC307, FNC308, FNC309, FNC310," \
                                "FNC311, FNC312, FNC313, FNC314, FNC315, FNC316, FNC317, FNC318, FNC319, FNC320, FNC321, FNC322, FNC323, FNC324, FNC325," \
                                "FNC326, FNC327, FNC328, FNC329, FNC330, FNC331, FNC332, FNC333, FNC334, FNC335, FNC336, FNC337, FNC338, FNC339, FNC340," \
                                "FNC341, FNC342, FNC343, FNC344, FNC345, FNC346, FNC347, FNC348, FNC349, FNC350, FNC351, FNC352, FNC353, FNC354, FNC355," \
                                "FNC356, FNC357, FNC358, FNC359, FNC360, FNC361, FNC362, FNC363, FNC364, FNC365, FNC366, FNC367, FNC368, FNC369, FNC370," \
                                "FNC371, FNC372, FNC373, FNC374, FNC375, FNC376, FNC377, FNC378)"
                                "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                                % (subId, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                                   data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20],
                                   data[21], data[22], data[23], data[24], data[25], data[26], data[27], data[28], data[29], data[30],
                                   data[31], data[32], data[33], data[34], data[35], data[36], data[37], data[38], data[39], data[40],
                                   data[41], data[42], data[43], data[44], data[45], data[46], data[47], data[48], data[49], data[50],
                                   data[51], data[52], data[53], data[54], data[55], data[56], data[57], data[58], data[59], data[60],
                                   data[61], data[62], data[63], data[64], data[65], data[66], data[67], data[68], data[69], data[70],
                                   data[71], data[72], data[73], data[74], data[75], data[76], data[77], data[78], data[79], data[80],
                                   data[81], data[82], data[83], data[84], data[85], data[86], data[87], data[88], data[89], data[90],
                                   data[91], data[92], data[93], data[94], data[95], data[96], data[97], data[98], data[99], data[100],
                                   data[101], data[102], data[103], data[104], data[105], data[106], data[107], data[108], data[109], data[110],
                                   data[111], data[112], data[113], data[114], data[115], data[116], data[117], data[118], data[119], data[120],
                                   data[121], data[122], data[123], data[124], data[125], data[126], data[127], data[128], data[129], data[130],
                                   data[131], data[132], data[133], data[134], data[135], data[136], data[137], data[138], data[139], data[140],
                                   data[141], data[142], data[143], data[144], data[145], data[146], data[147], data[148], data[149], data[150],
                                   data[151], data[152], data[153], data[154], data[155], data[156], data[157], data[158], data[159], data[160],
                                   data[161], data[162], data[163], data[164], data[165], data[166], data[167], data[168], data[169], data[170],
                                   data[171], data[172], data[173], data[174], data[175], data[176], data[177], data[178], data[179], data[180],
                                   data[181], data[182], data[183], data[184], data[185], data[186], data[187], data[188], data[189], data[190],
                                   data[191], data[192], data[193], data[194], data[195], data[196], data[197], data[198], data[199], data[200],
                                   data[201], data[202], data[203], data[204], data[205], data[206], data[207], data[208], data[209], data[210],
                                   data[211], data[212], data[213], data[214], data[215], data[216], data[217], data[218], data[219], data[220],
                                   data[221], data[222], data[223], data[224], data[225], data[226], data[227], data[228], data[229], data[230],
                                   data[231], data[232], data[233], data[234], data[235], data[236], data[237], data[238], data[239], data[240],
                                   data[241], data[242], data[243], data[244], data[245], data[246], data[247], data[248], data[249], data[250],
                                   data[251], data[252], data[253], data[254], data[255], data[256], data[257], data[258], data[259], data[260],
                                   data[261], data[262], data[263], data[264], data[265], data[266], data[267], data[268], data[269], data[270],
                                   data[271], data[272], data[273], data[274], data[275], data[276], data[277], data[278], data[279], data[280],
                                   data[281], data[282], data[283], data[284], data[285], data[286], data[287], data[288], data[289], data[290],
                                   data[291], data[292], data[293], data[294], data[295], data[296], data[297], data[298], data[299], data[300],
                                   data[301], data[302], data[303], data[304], data[305], data[306], data[307], data[308], data[309], data[310],
                                   data[311], data[312], data[313], data[314], data[315], data[316], data[317], data[318], data[319], data[320],
                                   data[321], data[322], data[323], data[324], data[325], data[326], data[327], data[328], data[329], data[330],
                                   data[331], data[332], data[333], data[334], data[335], data[336], data[337], data[338], data[339], data[340],
                                   data[341], data[342], data[343], data[344], data[345], data[346], data[347], data[348], data[349], data[350],
                                   data[351], data[352], data[353], data[354], data[355], data[356], data[357], data[358], data[359], data[360],
                                   data[361], data[362], data[363], data[364], data[365], data[366], data[367], data[368], data[369], data[370],
                                   data[371], data[372], data[373], data[374], data[375], data[376], data[377]))
                            conn.commit()

                            f = open(sbm_data, 'r')
                            csvReader = csv.reader(f)

                            for row in csvReader:
                                data = []
                                num = 1
                                for col in row:
                                    if num < 33:
                                        data.append(row[num])
                                        num = num + 1

                            data2 = cur.execute(
                                "INSERT INTO mydb.train_sbm(subject_id, SBM_map1, SBM_map2, SBM_map3, SBM_map4, SBM_map5, SBM_map6, SBM_map7, SBM_map8," \
                                "SBM_map10, SBM_map13, SBM_map17, SBM_map22, SBM_map26, SBM_map28, SBM_map32, SBM_map36, SBM_map40, SBM_map43, SBM_map45, SBM_map48," \
                                "SBM_map51, SBM_map52, SBM_map55, SBM_map61, SBM_map64, SBM_map67, SBM_map69, SBM_map71, SBM_map72, SBM_map73, SBM_map74, SBM_map75)"
                                "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                                "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                                % (subId, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12],
                                   data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21], data[22], data[23], data[24], data[25],
                                   data[26], data[27], data[28], data[29], data[30], data[31]))
                            conn.commit()

    # Brain 그래프 이벤트
    def brainGraphShow(self):
        subject = int(patId)
        if eeg_data == "":
            self.brainGraphLabel.setStyleSheet("font: 12pt \"KoPub돋움체 Medium\";\n"
                                               "background-color: rgb(255, 255, 255); color: rgb(0, 0, 255);")
            self.brainGraphLabel.setText("                                                등록된 EEG 데이터가 없습니다.")
        else:
            self.brainGraphLabel.setText("")
            # col_names = pd.read_csv('eeg/columnLabels.csv')
            # ch_names = list(col_names.columns[4:])
            # ch_type = ['eeg'] * 64
            #
            # sfreq = 1024
            # montage = read_montage('standard_1005', ch_names)
            # info = create_info(ch_names, sfreq, ch_type, montage)
            #
            # def creat_mne_epoch_object(fname, info):
            #     info['description'] = 'dataset from ' + fname
            #     tmin = -1.5
            #
            #     data = pd.read_csv(fname, header=None)
            #     npdata = np.array(data)
            #
            #     onsets = np.array(np.where(npdata[:, 3] == 1537))
            #     conditions = npdata[npdata[:, 3] == 1537, 2]
            #     events = np.squeeze(np.dstack((onsets.flatten(), np.zeros(conditions.shape), conditions)))
            #
            #     EEGdata = npdata.reshape(len(conditions), 3072, 68)
            #     EEGdata = EEGdata[:, :, 4:]
            #     EEGdata = np.swapaxes(EEGdata, 1, 2)
            #
            #     event_id = dict(button_tone=1, playback_tone=2, button_alone=3)
            #     custom_epochs = EpochsArray(EEGdata, info=info, events=events.astype('int'), tmin=tmin,
            #                                 event_id=event_id)
            #     return custom_epochs
            #
            # col_names = pd.read_csv('eeg/columnLabels.csv')
            # ch_names = list(col_names.columns[4:])
            # ch_type = ['eeg'] * 64
            #
            # sfreq = 1024
            #
            # montage = read_montage('standard_1005', ch_names)
            #
            # info = create_info(ch_names, sfreq, ch_type, montage)
            #
            # def creat_mne_epoch_object(fname, info):
            #     info['description'] = 'dataset from ' + fname
            #     tmin = -1.5
            #
            #     data = pd.read_csv(fname, header=None)
            #     npdata = np.array(data)
            #
            #     onsets = np.array(np.where(npdata[:, 3] == 1537))
            #     conditions = npdata[npdata[:, 3] == 1537, 2]
            #     events = np.squeeze(np.dstack((onsets.flatten(), np.zeros(conditions.shape), conditions)))
            #
            #     EEGdata = npdata.reshape(len(conditions), 3072, 68)
            #     EEGdata = EEGdata[:, :, 4:]
            #     EEGdata = np.swapaxes(EEGdata, 1, 2)
            #
            #     event_id = dict(button_tone=1, playback_tone=2, button_alone=3)
            #
            #     custom_epochs = EpochsArray(EEGdata, info=info, events=events.astype('int'), tmin=tmin, event_id=event_id)
            #     return custom_epochs
            #
            # auc = []
            # epochs_tot = []
            #
            # fnames = glob("%s" % eeg_data)
            # print(fnames)
            # fname = fnames[0]
            # session = []
            # y = []
            #
            # custom_epochs = creat_mne_epoch_object(fname, info)
            # picks = pick_types(custom_epochs.info, eeg=True)
            # custom_epochs.filter(7, 35, picks=picks, method='iir', n_jobs=-1, verbose=False)
            #
            # epochs = custom_epochs['button_tone']
            # epochs_tot.append(epochs)
            # session.extend([1] * len(epochs))
            # y.extend([1] * len(epochs))
            #
            # epochs = custom_epochs['playback_tone']
            # epochs_tot.append(epochs)
            # session.extend([1] * len(epochs))
            # y.extend([-1] * len(epochs))
            #
            # epochs = concatenate_epochs(epochs_tot)
            #
            # X = epochs.crop(tmin=-0.7, tmax=0.299).get_data()
            # X = X[:, [ch == 'eeg' for ch in ch_type], :]
            # y = np.array(y)
            #
            # csp = CSP(reg='ledoit_wolf')
            # csp.fit(X, y)
            #
            # po = []
            # for x in X:
            #     f, p = welch(np.dot(csp.filters_[0, :].T, x), sfreq, nperseg=X.shape[2])
            #     po.append(p)
            # po = np.array(po)
            #
            # _, epos, _, _, _ = _prepare_topo_plot(epochs, 'eeg', None)
            #
            # pattern = csp.patterns_[0, :]
            # pattern -= pattern.mean()
            # ix = np.argmax(abs(pattern))
            #
            # if pattern[ix] > 0:
            #     sign = 1.0
            # else:
            #     sign = -1.0
            #
            # fig, ax_topo = plt.subplots(1, 1, figsize=(12, 4))
            # img, _ = plot_topomap(sign * pattern, epos, axes=ax_topo, show=False)
            # divider = make_axes_locatable(ax_topo)
            # ax_colorbar = divider.append_axes('right', size='5%', pad=0.05)
            # plt.colorbar(img, cax=ax_colorbar)
            #
            # fix = (f > 7) & (f < 35)
            # ax_spectrum = divider.append_axes('right', size='300%', pad=1.2)
            # ax_spectrum.plot(f[fix], np.log(po[y == 1][:, fix].mean(axis=0).T), '-r', lw=2)
            # ax_spectrum.plot(f[fix], np.log(po[y == -1][:, fix].mean(axis=0).T), '-b', lw=2)
            # ax_spectrum.set_xlabel('Frequency (Hz)')
            # ax_spectrum.set_ylabel('Power (dB)')
            # plt.grid()
            # plt.legend(['button tone', 'playback'])
            # plt.title('Subject %d' % subject)
            # plt.savefig('spatial_pattern.png', bbox_inches='tight')

            pixmap = QPixmap('spatial_pattern.png')
            self.brainGraphLabel.setPixmap(QPixmap(pixmap))

    # 채널 버튼 이벤트
    def AF3_Btn_clicked(self, MainWindow):
        self.label.setText("AF3")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, AF3 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, AF3 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def AF4_Btn_clicked(self, MainWindow):
        self.label.setText("AF4")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, AF4 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, AF4 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def AF7_Btn_clicked(self, MainWindow):
        self.label.setText("AF7")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, AF7 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, AF7 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def AF8_Btn_clicked(self, MainWindow):
        self.label.setText("AF8")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, AF8 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, AF8 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def AFz_Btn_clicked(self, MainWindow):
        self.label.setText("AFz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, AFz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, AFz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def C1_Btn_clicked(self, MainWindow):
        self.label.setText("C1")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, C1 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, C1 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def C2_Btn_clicked(self, MainWindow):
        self.label.setText("C2")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, C2 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, C2 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def C3_Btn_clicked(self, MainWindow):
        self.label.setText("C3")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, C3 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, C3 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def C4_Btn_clicked(self, MainWindow):
        self.label.setText("C4")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, C4 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, C4 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def C5_Btn_clicked(self, MainWindow):
        self.label.setText("C5")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, C5 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, C5 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def C6_Btn_clicked(self, MainWindow):
        self.label.setText("C6")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, C6 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, C6 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def CP1_Btn_clicked(self, MainWindow):
        self.label.setText("CP1")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, CP1 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, CP1 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def CP2_Btn_clicked(self, MainWindow):
        self.label.setText("CP2")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, CP2 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, CP2 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def CP3_Btn_clicked(self, MainWindow):
        self.label.setText("CP3")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, CP3 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, CP3 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def CP4_Btn_clicked(self, MainWindow):
        self.label.setText("CP4")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, CP4 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, CP4 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def CP5_Btn_clicked(self, MainWindow):
        self.label.setText("CP5")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, CP5 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, CP5 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def CP6_Btn_clicked(self, MainWindow):
        self.label.setText("CP6")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, CP6 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, CP6 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def CPz_Btn_clicked(self, MainWindow):
        self.label.setText("CPz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, CPz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, CPz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def Cz_Btn_clicked(self, MainWindow):
        self.label.setText("Cz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, Cz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, Cz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def F1_Btn_clicked(self, MainWindow):
        self.label.setText("F1")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, F1 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, F1 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def F2_Btn_clicked(self, MainWindow):
        self.label.setText("F2")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, F2 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, F2 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def F3_Btn_clicked(self, MainWindow):
        self.label.setText("F3")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, F3 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, F3 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def F4_Btn_clicked(self, MainWindow):
        self.label.setText("F4")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, F4 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, F4 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def F5_Btn_clicked(self, MainWindow):
        self.label.setText("F5")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, F5 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, F5 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def F6_Btn_clicked(self, MainWindow):
        self.label.setText("F6")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, F6 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, F6 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def F7_Btn_clicked(self, MainWindow):
        self.label.setText("F7")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, F7 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, F7 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def F8_Btn_clicked(self, MainWindow):
        self.label.setText("F8")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, F8 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, F8 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FC1_Btn_clicked(self, MainWindow):
        self.label.setText("FC1")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FC1 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FC1 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FC2_Btn_clicked(self, MainWindow):
        self.label.setText("FC2")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FC2 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FC2 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FC3_Btn_clicked(self, MainWindow):
        self.label.setText("FC3")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FC3 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FC3 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FC4_Btn_clicked(self, MainWindow):
        self.label.setText("FC4")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FC4 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FC4 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FC5_Btn_clicked(self, MainWindow):
        self.label.setText("FC5")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FC5 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FC5 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FC6_Btn_clicked(self, MainWindow):
        self.label.setText("FC6")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FC6 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FC6 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FCz_Btn_clicked(self, MainWindow):
        self.label.setText("FCz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FCz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FCz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FT7_Btn_clicked(self, MainWindow):
        self.label.setText("FT7")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FT7 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FT7 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def FT8_Btn_clicked(self, MainWindow):
        self.label.setText("FT8")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, FT8 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, FT8 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def Fp1_Btn_clicked(self, MainWindow):
        self.label.setText("Fp1")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, Fp1 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, Fp1 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def Fp2_Btn_clicked(self, MainWindow):
        self.label.setText("Fp2")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, Fp2 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, Fp2 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def Fpz_Btn_clicked(self, MainWindow):
        self.label.setText("Fpz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, Fpz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, Fpz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def Fz_Btn_clicked(self, MainWindow):
        self.label.setText("Fz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, Fz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, Fz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def O1_Btn_clicked(self, MainWindow):
        self.label.setText("O1")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, O1 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, O1 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def O2_Btn_clicked(self, MainWindow):
        self.label.setText("O2")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, O2 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, O2 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def Oz_Btn_clicked(self, MainWindow):
        self.label.setText("Oz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, Oz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, Oz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def P1_Btn_clicked(self, MainWindow):
        self.label.setText("P1")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, P1 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, P1 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def P2_Btn_clicked(self, MainWindow):
        self.label.setText("P2")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, P2 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, P2 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def P3_Btn_clicked(self, MainWindow):
        self.label.setText("P3")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, P3 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, P3 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def P4_Btn_clicked(self, MainWindow):
        self.label.setText("P4")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, P4 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, P4 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def P5_Btn_clicked(self, MainWindow):
        self.label.setText("P5")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, P5 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, P5 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def P6_Btn_clicked(self, MainWindow):
        self.label.setText("P6")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, P6 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, P6 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def P7_Btn_clicked(self, MainWindow):
        self.label.setText("P7")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, P7 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, P7 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def P8_Btn_clicked(self, MainWindow):
        self.label.setText("P8")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, P8 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, P8 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def PO3_Btn_clicked(self, MainWindow):
        self.label.setText("PO3")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, PO3 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, PO3 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def PO4_Btn_clicked(self, MainWindow):
        self.label.setText("PO4")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, PO4 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, PO4 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def PO7_Btn_clicked(self, MainWindow):
        self.label.setText("PO7")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, PO7 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, PO7 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def PO8_Btn_clicked(self, MainWindow):
        self.label.setText("PO8")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, PO8 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, PO8 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def POz_Btn_clicked(self, MainWindow):
        self.label.setText("POz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, POz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, POz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def Pz_Btn_clicked(self, MainWindow):
        self.label.setText("Pz")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, Pz FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, Pz FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def T7_Btn_clicked(self, MainWindow):
        self.label.setText("T7")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, T7 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, T7 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def T8_Btn_clicked(self, MainWindow):
        self.label.setText("T8")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, T8 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, T8 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def TP7_Btn_clicked(self, MainWindow):
        self.label.setText("TP7")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, TP7 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, TP7 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()
    def TP8_Btn_clicked(self, MainWindow):
        self.label.setText("TP8")
        with conn.cursor() as curs:
            sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
            curs.execute(sql)
            rs = curs.fetchall()
            x1 = []
            y1 = []
            for row in rs:
                # 등록된 데이터가 있는 경우
                if row[0] == 1:
                    sql = "SELECT sample, TP8 FROM mydb.subject%s_eeg WHERE subject%s_eeg.condition = 1" % (patId, patId)
                    curs.execute(sql)
                    rs = curs.fetchall()
                    for row in rs:
                        x1.append(row[0])
                        y1.append(row[1])
            sql = "SELECT sample, TP8 FROM mydb.control_eeg"
            curs.execute(sql)
            rs = curs.fetchall()
            x2 = []
            y2 = []
            for row in rs:
                x2.append(row[0])
                y2.append(row[1])
            ax1 = self.fig1.add_subplot(1, 1, 1)
            ax1.clear()
            ax1.grid()
            ax1.plot(x1, y1, label="Patient", color="red")
            ax1.plot(x2, y2, label="Control", color="blue")
            ax1.set_xlabel('Time', fontsize=10, color="blue")
            ax1.set_ylabel('EEG', fontsize=10, color="blue")
            ax1.set_xlim(1540, 1750)
            ax1.legend(loc='best')
            self.eegGraph.draw()

    # 팝업 알림창 이벤트
    def messagebox(self, title, message):
        mess = QtWidgets.QMessageBox()
        mess.setWindowTitle(title)
        mess.setText(message)
        mess.setStandardButtons(QtWidgets.QMessageBox.Ok)
        mess.exec_()

    # 환자 등록 위젯1 초기화
    def PatSearInitialize(self):
        self.ExiPatNum.setText("")
        self.PatSearErr.setText("")

    # 환자 진단 위젯1 초기화
    def PatDiagInitialize(self):
        self.PatNum.setText("")
        self.PatDiagErr.setText("")

    # 환자 진단 위젯4 초기화
    def DataInitialize(self):
        self.FNCData.setText("")
        self.SBMData.setText("")
        self.EEGData.setText("")
        self.FNCDataErr.setText("")
        self.SBMDataErr.setText("")
        self.EEGDataErr.setText("")

    # 계정 관리 위젯1 초기화
    def AccManInitialize(self, MainWindow):
        self.PWEnt.setText("")
        self.AcctManErrMsg.setText("")

    # 환자 등록 초기화
    def PatRegInitialize(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        self.PatRegNum.setText("")
        self.PatName.setText("")
        self.PatBirth.setDateTime(QtCore.QDateTime(QtCore.QDate(2020, 1, 1), QtCore.QTime(0, 0, 0)))
        self.PatMBtn.setChecked(True)
        self.PatHCBtn.setChecked(True)
        self.PatPhone.setText("")
        self.PatDocID.setText(drId)

        self.PatNumErr.setText(_translate("MainWindow", ""))
        self.PatNameErr.setText(_translate("MainWindow", ""))
        self.PatPhoneErr.setText(_translate("MainWindow", ""))
        self.PatDocIDErr.setText(_translate("MainWindow", ""))

    # 환자 등록 이벤트 처리
    def InsPatInfo(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        num = 0

        self.PatNumErr.setText(_translate("MainWindow", ""))
        self.PatNameErr.setText(_translate("MainWindow", ""))
        self.PatPhoneErr.setText(_translate("MainWindow", ""))
        self.PatDocIDErr.setText(_translate("MainWindow", ""))

        # 빈 정보를 입력했을 때
        if not self.PatRegNum.text():
            self.PatNumErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            with conn.cursor() as cur:
                sql1 = "SELECT EXISTS(SELECT * FROM mydb.subject_info WHERE subject_id = '%s')" % self.PatRegNum.text()
                cur.execute(sql1)
                rs = cur.fetchall()
                for row in rs:
                    # 이미 등록된 번호일 경우
                    if row[0] == 1:
                        self.PatNumErr.setText(_translate("MainWindow", "이미 등록된 번호입니다."))
                    else:
                        num += 1
        if not self.PatName.text():
            self.PatNameErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            num += 1
        if not self.PatPhone.text():
            self.PatPhoneErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            num += 1
        if not self.PatDocID.text():
            self.PatDocIDErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            num += 1

        if num == 4:
            # 등록 가능한 번호일 경우
            if self.PatMBtn.isChecked():
                PatGen = 'M'
            else:
                PatGen = 'F'

            if self.PatHCBtn.isChecked():
                PatGroup = '0'
            elif self.PatSZBtn.isChecked():
                PatGroup = '1'
            else:
                PatGroup = '2'

            with conn.cursor() as cur:
                subject_id = self.PatRegNum.text()

                sql1 = "CREATE TABLE mydb.subject%s_fnc (`subject_id` VARCHAR(20) NOT NULL, `come_date` VARCHAR(10) NOT NULL," \
                       "`FNC1` DOUBLE NULL, `FNC2` DOUBLE NULL, `FNC3` DOUBLE NULL, `FNC4` DOUBLE NULL, `FNC5` DOUBLE NULL," \
                       "`FNC6` DOUBLE NULL, `FNC7` DOUBLE NULL, `FNC8` DOUBLE NULL, `FNC9` DOUBLE NULL, `FNC10` DOUBLE NULL," \
                       "`FNC11` DOUBLE NULL, `FNC12` DOUBLE NULL, `FNC13` DOUBLE NULL, `FNC14` DOUBLE NULL, `FNC15` DOUBLE NULL," \
                       "`FNC16` DOUBLE NULL, `FNC17` DOUBLE NULL, `FNC18` DOUBLE NULL, `FNC19` DOUBLE NULL, `FNC20` DOUBLE NULL," \
                       "`FNC21` DOUBLE NULL, `FNC22` DOUBLE NULL, `FNC23` DOUBLE NULL, `FNC24` DOUBLE NULL, `FNC25` DOUBLE NULL," \
                       "`FNC26` DOUBLE NULL, `FNC27` DOUBLE NULL, `FNC28` DOUBLE NULL, `FNC29` DOUBLE NULL, `FNC30` DOUBLE NULL," \
                       "`FNC31` DOUBLE NULL, `FNC32` DOUBLE NULL, `FNC33` DOUBLE NULL, `FNC34` DOUBLE NULL, `FNC35` DOUBLE NULL," \
                       "`FNC36` DOUBLE NULL, `FNC37` DOUBLE NULL, `FNC38` DOUBLE NULL, `FNC39` DOUBLE NULL, `FNC40` DOUBLE NULL," \
                       "`FNC41` DOUBLE NULL, `FNC42` DOUBLE NULL, `FNC43` DOUBLE NULL, `FNC44` DOUBLE NULL, `FNC45` DOUBLE NULL," \
                       "`FNC46` DOUBLE NULL, `FNC47` DOUBLE NULL, `FNC48` DOUBLE NULL, `FNC49` DOUBLE NULL, `FNC50` DOUBLE NULL," \
                       "`FNC51` DOUBLE NULL, `FNC52` DOUBLE NULL, `FNC53` DOUBLE NULL, `FNC54` DOUBLE NULL, `FNC55` DOUBLE NULL," \
                       "`FNC56` DOUBLE NULL, `FNC57` DOUBLE NULL, `FNC58` DOUBLE NULL, `FNC59` DOUBLE NULL, `FNC60` DOUBLE NULL," \
                       "`FNC61` DOUBLE NULL, `FNC62` DOUBLE NULL, `FNC63` DOUBLE NULL, `FNC64` DOUBLE NULL, `FNC65` DOUBLE NULL," \
                       "`FNC66` DOUBLE NULL, `FNC67` DOUBLE NULL, `FNC68` DOUBLE NULL, `FNC69` DOUBLE NULL, `FNC70` DOUBLE NULL," \
                       "`FNC71` DOUBLE NULL, `FNC72` DOUBLE NULL, `FNC73` DOUBLE NULL, `FNC74` DOUBLE NULL, `FNC75` DOUBLE NULL," \
                       "`FNC76` DOUBLE NULL, `FNC77` DOUBLE NULL, `FNC78` DOUBLE NULL, `FNC79` DOUBLE NULL, `FNC80` DOUBLE NULL," \
                       "`FNC81` DOUBLE NULL, `FNC82` DOUBLE NULL, `FNC83` DOUBLE NULL, `FNC84` DOUBLE NULL, `FNC85` DOUBLE NULL," \
                       "`FNC86` DOUBLE NULL, `FNC87` DOUBLE NULL, `FNC88` DOUBLE NULL, `FNC89` DOUBLE NULL, `FNC90` DOUBLE NULL," \
                       "`FNC91` DOUBLE NULL, `FNC92` DOUBLE NULL, `FNC93` DOUBLE NULL, `FNC94` DOUBLE NULL, `FNC95` DOUBLE NULL," \
                       "`FNC96` DOUBLE NULL, `FNC97` DOUBLE NULL, `FNC98` DOUBLE NULL, `FNC99` DOUBLE NULL, `FNC100` DOUBLE NULL," \
                       "`FNC101` DOUBLE NULL, `FNC102` DOUBLE NULL, `FNC103` DOUBLE NULL, `FNC104` DOUBLE NULL, `FNC105` DOUBLE NULL," \
                       "`FNC106` DOUBLE NULL, `FNC107` DOUBLE NULL, `FNC108` DOUBLE NULL, `FNC109` DOUBLE NULL, `FNC110` DOUBLE NULL," \
                       "`FNC111` DOUBLE NULL, `FNC112` DOUBLE NULL, `FNC113` DOUBLE NULL, `FNC114` DOUBLE NULL, `FNC115` DOUBLE NULL," \
                       "`FNC116` DOUBLE NULL, `FNC117` DOUBLE NULL, `FNC118` DOUBLE NULL, `FNC119` DOUBLE NULL, `FNC120` DOUBLE NULL," \
                       "`FNC121` DOUBLE NULL, `FNC122` DOUBLE NULL, `FNC123` DOUBLE NULL, `FNC124` DOUBLE NULL, `FNC125` DOUBLE NULL," \
                       "`FNC126` DOUBLE NULL, `FNC127` DOUBLE NULL, `FNC128` DOUBLE NULL, `FNC129` DOUBLE NULL, `FNC130` DOUBLE NULL," \
                       "`FNC131` DOUBLE NULL, `FNC132` DOUBLE NULL, `FNC133` DOUBLE NULL, `FNC134` DOUBLE NULL, `FNC135` DOUBLE NULL," \
                       "`FNC136` DOUBLE NULL, `FNC137` DOUBLE NULL, `FNC138` DOUBLE NULL, `FNC139` DOUBLE NULL, `FNC140` DOUBLE NULL," \
                       "`FNC141` DOUBLE NULL, `FNC142` DOUBLE NULL, `FNC143` DOUBLE NULL, `FNC144` DOUBLE NULL, `FNC145` DOUBLE NULL," \
                       "`FNC146` DOUBLE NULL, `FNC147` DOUBLE NULL, `FNC148` DOUBLE NULL, `FNC149` DOUBLE NULL, `FNC150` DOUBLE NULL," \
                       "`FNC151` DOUBLE NULL, `FNC152` DOUBLE NULL, `FNC153` DOUBLE NULL, `FNC154` DOUBLE NULL, `FNC155` DOUBLE NULL," \
                       "`FNC156` DOUBLE NULL, `FNC157` DOUBLE NULL, `FNC158` DOUBLE NULL, `FNC159` DOUBLE NULL, `FNC160` DOUBLE NULL," \
                       "`FNC161` DOUBLE NULL, `FNC162` DOUBLE NULL, `FNC163` DOUBLE NULL, `FNC164` DOUBLE NULL, `FNC165` DOUBLE NULL," \
                       "`FNC166` DOUBLE NULL, `FNC167` DOUBLE NULL, `FNC168` DOUBLE NULL, `FNC169` DOUBLE NULL, `FNC170` DOUBLE NULL," \
                       "`FNC171` DOUBLE NULL, `FNC172` DOUBLE NULL, `FNC173` DOUBLE NULL, `FNC174` DOUBLE NULL, `FNC175` DOUBLE NULL," \
                       "`FNC176` DOUBLE NULL, `FNC177` DOUBLE NULL, `FNC178` DOUBLE NULL, `FNC179` DOUBLE NULL, `FNC180` DOUBLE NULL," \
                       "`FNC181` DOUBLE NULL, `FNC182` DOUBLE NULL, `FNC183` DOUBLE NULL, `FNC184` DOUBLE NULL, `FNC185` DOUBLE NULL," \
                       "`FNC186` DOUBLE NULL, `FNC187` DOUBLE NULL, `FNC188` DOUBLE NULL, `FNC189` DOUBLE NULL, `FNC190` DOUBLE NULL," \
                       "`FNC191` DOUBLE NULL, `FNC192` DOUBLE NULL, `FNC193` DOUBLE NULL, `FNC194` DOUBLE NULL, `FNC195` DOUBLE NULL," \
                       "`FNC196` DOUBLE NULL, `FNC197` DOUBLE NULL, `FNC198` DOUBLE NULL, `FNC199` DOUBLE NULL, `FNC200` DOUBLE NULL," \
                       "`FNC201` DOUBLE NULL, `FNC202` DOUBLE NULL, `FNC203` DOUBLE NULL, `FNC204` DOUBLE NULL, `FNC205` DOUBLE NULL," \
                       "`FNC206` DOUBLE NULL, `FNC207` DOUBLE NULL, `FNC208` DOUBLE NULL, `FNC209` DOUBLE NULL, `FNC210` DOUBLE NULL," \
                       "`FNC211` DOUBLE NULL, `FNC212` DOUBLE NULL, `FNC213` DOUBLE NULL, `FNC214` DOUBLE NULL, `FNC215` DOUBLE NULL," \
                       "`FNC216` DOUBLE NULL, `FNC217` DOUBLE NULL, `FNC218` DOUBLE NULL, `FNC219` DOUBLE NULL, `FNC220` DOUBLE NULL," \
                       "`FNC221` DOUBLE NULL, `FNC222` DOUBLE NULL, `FNC223` DOUBLE NULL, `FNC224` DOUBLE NULL, `FNC225` DOUBLE NULL," \
                       "`FNC226` DOUBLE NULL, `FNC227` DOUBLE NULL, `FNC228` DOUBLE NULL, `FNC229` DOUBLE NULL, `FNC230` DOUBLE NULL," \
                       "`FNC231` DOUBLE NULL, `FNC232` DOUBLE NULL, `FNC233` DOUBLE NULL, `FNC234` DOUBLE NULL, `FNC235` DOUBLE NULL," \
                       "`FNC236` DOUBLE NULL, `FNC237` DOUBLE NULL, `FNC238` DOUBLE NULL, `FNC239` DOUBLE NULL, `FNC240` DOUBLE NULL," \
                       "`FNC241` DOUBLE NULL, `FNC242` DOUBLE NULL, `FNC243` DOUBLE NULL, `FNC244` DOUBLE NULL, `FNC245` DOUBLE NULL," \
                       "`FNC246` DOUBLE NULL, `FNC247` DOUBLE NULL, `FNC248` DOUBLE NULL, `FNC249` DOUBLE NULL, `FNC250` DOUBLE NULL," \
                       "`FNC251` DOUBLE NULL, `FNC252` DOUBLE NULL, `FNC253` DOUBLE NULL, `FNC254` DOUBLE NULL, `FNC255` DOUBLE NULL," \
                       "`FNC256` DOUBLE NULL, `FNC257` DOUBLE NULL, `FNC258` DOUBLE NULL, `FNC259` DOUBLE NULL, `FNC260` DOUBLE NULL," \
                       "`FNC261` DOUBLE NULL, `FNC262` DOUBLE NULL, `FNC263` DOUBLE NULL, `FNC264` DOUBLE NULL, `FNC265` DOUBLE NULL," \
                       "`FNC266` DOUBLE NULL, `FNC267` DOUBLE NULL, `FNC268` DOUBLE NULL, `FNC269` DOUBLE NULL, `FNC270` DOUBLE NULL," \
                       "`FNC271` DOUBLE NULL, `FNC272` DOUBLE NULL, `FNC273` DOUBLE NULL, `FNC274` DOUBLE NULL, `FNC275` DOUBLE NULL," \
                       "`FNC276` DOUBLE NULL, `FNC277` DOUBLE NULL, `FNC278` DOUBLE NULL, `FNC279` DOUBLE NULL, `FNC280` DOUBLE NULL," \
                       "`FNC281` DOUBLE NULL, `FNC282` DOUBLE NULL, `FNC283` DOUBLE NULL, `FNC284` DOUBLE NULL, `FNC285` DOUBLE NULL," \
                       "`FNC286` DOUBLE NULL, `FNC287` DOUBLE NULL, `FNC288` DOUBLE NULL, `FNC289` DOUBLE NULL, `FNC290` DOUBLE NULL," \
                       "`FNC291` DOUBLE NULL, `FNC292` DOUBLE NULL, `FNC293` DOUBLE NULL, `FNC294` DOUBLE NULL, `FNC295` DOUBLE NULL," \
                       "`FNC296` DOUBLE NULL, `FNC297` DOUBLE NULL, `FNC298` DOUBLE NULL, `FNC299` DOUBLE NULL, `FNC300` DOUBLE NULL," \
                       "`FNC301` DOUBLE NULL, `FNC302` DOUBLE NULL, `FNC303` DOUBLE NULL, `FNC304` DOUBLE NULL, `FNC305` DOUBLE NULL," \
                       "`FNC306` DOUBLE NULL, `FNC307` DOUBLE NULL, `FNC308` DOUBLE NULL, `FNC309` DOUBLE NULL, `FNC310` DOUBLE NULL," \
                       "`FNC311` DOUBLE NULL, `FNC312` DOUBLE NULL, `FNC313` DOUBLE NULL, `FNC314` DOUBLE NULL, `FNC315` DOUBLE NULL," \
                       "`FNC316` DOUBLE NULL, `FNC317` DOUBLE NULL, `FNC318` DOUBLE NULL, `FNC319` DOUBLE NULL, `FNC320` DOUBLE NULL," \
                       "`FNC321` DOUBLE NULL, `FNC322` DOUBLE NULL, `FNC323` DOUBLE NULL, `FNC324` DOUBLE NULL, `FNC325` DOUBLE NULL," \
                       "`FNC326` DOUBLE NULL, `FNC327` DOUBLE NULL, `FNC328` DOUBLE NULL, `FNC329` DOUBLE NULL, `FNC330` DOUBLE NULL," \
                       "`FNC331` DOUBLE NULL, `FNC332` DOUBLE NULL, `FNC333` DOUBLE NULL, `FNC334` DOUBLE NULL, `FNC335` DOUBLE NULL," \
                       "`FNC336` DOUBLE NULL, `FNC337` DOUBLE NULL, `FNC338` DOUBLE NULL, `FNC339` DOUBLE NULL, `FNC340` DOUBLE NULL," \
                       "`FNC341` DOUBLE NULL, `FNC342` DOUBLE NULL, `FNC343` DOUBLE NULL, `FNC344` DOUBLE NULL, `FNC345` DOUBLE NULL," \
                       "`FNC346` DOUBLE NULL, `FNC347` DOUBLE NULL, `FNC348` DOUBLE NULL, `FNC349` DOUBLE NULL, `FNC350` DOUBLE NULL," \
                       "`FNC351` DOUBLE NULL, `FNC352` DOUBLE NULL, `FNC353` DOUBLE NULL, `FNC354` DOUBLE NULL, `FNC355` DOUBLE NULL," \
                       "`FNC356` DOUBLE NULL, `FNC357` DOUBLE NULL, `FNC358` DOUBLE NULL, `FNC359` DOUBLE NULL, `FNC360` DOUBLE NULL," \
                       "`FNC361` DOUBLE NULL, `FNC362` DOUBLE NULL, `FNC363` DOUBLE NULL, `FNC364` DOUBLE NULL, `FNC365` DOUBLE NULL," \
                       "`FNC366` DOUBLE NULL, `FNC367` DOUBLE NULL, `FNC368` DOUBLE NULL, `FNC369` DOUBLE NULL, `FNC370` DOUBLE NULL," \
                       "`FNC371` DOUBLE NULL, `FNC372` DOUBLE NULL, `FNC373` DOUBLE NULL, `FNC374` DOUBLE NULL, `FNC375` DOUBLE NULL," \
                       "`FNC376` DOUBLE NULL, `FNC377` DOUBLE NULL, `FNC378` DOUBLE NULL, PRIMARY KEY (`subject_id`, `come_date`))" % (
                       subject_id)
                cur.execute(sql1)

                sql2 = "CREATE TABLE mydb.subject%s_sbm (`subject_id` VARCHAR(20) NOT NULL, `come_date` VARCHAR(10) NOT NULL," \
                       "`SBM_map1` DOUBLE NULL, `SBM_map2` DOUBLE NULL, `SBM_map3` DOUBLE NULL, `SBM_map4` DOUBLE NULL, `SBM_map5` DOUBLE NULL," \
                       "`SBM_map6` DOUBLE NULL, `SBM_map7` DOUBLE NULL, `SBM_map8` DOUBLE NULL, `SBM_map10` DOUBLE NULL, `SBM_map13` DOUBLE NULL," \
                       "`SBM_map17` DOUBLE NULL, `SBM_map22` DOUBLE NULL, `SBM_map26` DOUBLE NULL, `SBM_map28` DOUBLE NULL, `SBM_map32` DOUBLE NULL," \
                       "`SBM_map36` DOUBLE NULL, `SBM_map40` DOUBLE NULL, `SBM_map43` DOUBLE NULL, `SBM_map45` DOUBLE NULL, `SBM_map48` DOUBLE NULL," \
                       "`SBM_map51` DOUBLE NULL, `SBM_map52` DOUBLE NULL, `SBM_map55` DOUBLE NULL, `SBM_map61` DOUBLE NULL, `SBM_map64` DOUBLE NULL," \
                       "`SBM_map67` DOUBLE NULL, `SBM_map69` DOUBLE NULL, `SBM_map71` DOUBLE NULL, `SBM_map72` DOUBLE NULL, `SBM_map73` DOUBLE NULL," \
                       "`SBM_map74` DOUBLE NULL, `SBM_map75` DOUBLE NULL, PRIMARY KEY (`subject_id`, `come_date`))" % (
                       subject_id)
                cur.execute(sql2)

                sql3 = "CREATE TABLE mydb.subject%s_eeg (`subject_id` VARCHAR(20) NOT NULL, `trial` VARCHAR(5) NOT NULL, `condition` VARCHAR(5) NOT NULL, `sample` INT NOT NULL," \
                       "`Fp1` DOUBLE NULL, `AF7` DOUBLE NULL, `AF3` DOUBLE NULL, `F1` DOUBLE NULL, `F3` DOUBLE NULL, `F5` DOUBLE NULL," \
                       "`F7` DOUBLE NULL, `FT7` DOUBLE NULL, `FC5` DOUBLE NULL, `FC3` DOUBLE NULL, `FC1` DOUBLE NULL, `C1` DOUBLE NULL," \
                       "`C3` DOUBLE NULL, `C5` DOUBLE NULL, `T7` DOUBLE NULL, `TP7` DOUBLE NULL, `CP5` DOUBLE NULL, `CP3` DOUBLE NULL," \
                       "`CP1` DOUBLE NULL, `P1` DOUBLE NULL, `P3` DOUBLE NULL, `P5` DOUBLE NULL, `P7` DOUBLE NULL, `P9` DOUBLE NULL," \
                       "`PO7` DOUBLE NULL, `PO3` DOUBLE NULL, `O1` DOUBLE NULL, `lz` DOUBLE NULL, `Oz` DOUBLE NULL, `POz` DOUBLE NULL," \
                       "`Pz` DOUBLE NULL, `CPz` DOUBLE NULL, `Fpz` DOUBLE NULL, `Fp2` DOUBLE NULL, `AF8` DOUBLE NULL, `AF4` DOUBLE NULL," \
                       "`AFz` DOUBLE NULL, `Fz` DOUBLE NULL, `F2` DOUBLE NULL, `F4` DOUBLE NULL, `F6` DOUBLE NULL, `F8` DOUBLE NULL," \
                       "`FT8` DOUBLE NULL, `FC6` DOUBLE NULL, `FC4` DOUBLE NULL, `FC2` DOUBLE NULL, `FCz` DOUBLE NULL, `Cz` DOUBLE NULL," \
                       "`C2` DOUBLE NULL, `C4` DOUBLE NULL, `C6` DOUBLE NULL, `T8` DOUBLE NULL, `TP8` DOUBLE NULL, `CP6` DOUBLE NULL," \
                       "`CP4` DOUBLE NULL, `CP2` DOUBLE NULL, `P2` DOUBLE NULL, `P4` DOUBLE NULL, `P6` DOUBLE NULL, `P8` DOUBLE NULL," \
                       "`P10` DOUBLE NULL, `PO8` DOUBLE NULL, `PO4` DOUBLE NULL, `O2` DOUBLE NULL, PRIMARY KEY (`subject_id`, `trial`, `condition`, `sample`)," \
                       "CONSTRAINT `sub%s_eeg_sample` FOREIGN KEY (`sample`) REFERENCES `mydb`.`time` (`sample`) ON DELETE NO ACTION ON UPDATE NO ACTION)" % (
                       subject_id, subject_id)
                cur.execute(sql3)

                data = cur.execute("INSERT INTO mydb.subject_info(subject_id, name, birth, gender, class, phone, dr_id)"
                                   "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (subject_id,
                                                                                         ''.join(self.PatName.text()),
                                                                                         ''.join(self.PatBirth.text()),
                                                                                         PatGen,
                                                                                         PatGroup,
                                                                                         ''.join(self.PatPhone.text()),
                                                                                         ''.join(self.PatDocID.text())))

                conn.commit()

                if(data):
                    self.messagebox("알림", "환자정보가 등록되었습니다.")

                self.PatRegWidget_1.show()
                self.PatSearInitialize()

    # FNC 파일 선택 이벤트
    def OpenFNCFile(self):
        fname = QFileDialog.getOpenFileName()
        if fname[0]:
            self.FNCData.setText(fname[0])
        else:
            self.messagebox("경고", "파일을 선택하지 않았습니다.")

    # SBM 파일 선택 이벤트
    def OpenSBMFile(self):
        fname = QFileDialog.getOpenFileName()
        if fname[0]:
            self.SBMData.setText(fname[0])
        else:
            self.messagebox("경고", "파일을 선택하지 않았습니다.")

    # EEG 파일 선택 이벤트
    def OpenEEGFile(self):
        fname = QFileDialog.getOpenFileName()
        if fname[0]:
            self.EEGData.setText(fname[0])
        else:
            self.messagebox("경고", "파일을 선택하지 않았습니다.")

    # 데이터 등록 이벤트 처리
    def InsData(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        num = 0

        self.FNCDataErr.setText(_translate("MainWindow", ""))
        self.SBMDataErr.setText(_translate("MainWindow", ""))
        self.EEGDataErr.setText(_translate("MainWindow", ""))

        if not self.FNCData.text():
            self.FNCDataErr.setText(_translate("MainWindow", "필수 정보입니다."))
        elif not os.path.exists(self.FNCData.text()):
            self.FNCDataErr.setText(_translate("MainWindow", "파일이 존재하지 않습니다."))
        else:
            num += 1
        if not self.SBMData.text():
            self.SBMDataErr.setText(_translate("MainWindow", "필수 정보입니다."))
        elif not os.path.exists(self.SBMData.text()):
            self.SBMDataErr.setText(_translate("MainWindow", "파일이 존재하지 않습니다."))
        else:
            num += 1
        if not self.EEGData.text():
            self.EEGDataErr.setText(_translate("MainWindow", "필수 정보입니다."))
        elif not os.path.exists(self.EEGData.text()):
            self.EEGDataErr.setText(_translate("MainWindow", "파일이 존재하지 않습니다."))
        else:
            num += 1

        if num == 3:
            global fnc_data
            fnc_data = self.FNCData.text()
            global sbm_data
            sbm_data = self.SBMData.text()
            global eeg_data
            eeg_data = self.EEGData.text()
            global come_date
            come_date = self.ComeDate.text()

            with conn.cursor() as cur:
                f = open(fnc_data, 'r')
                csvReader = csv.reader(f)

                for row in csvReader:
                    data = []
                    data.append(come_date)
                    num = 0
                    for col in row:
                        if num < 379:
                            data.append(row[num])
                            num = num + 1
                data1 = cur.execute(
                    "INSERT INTO mydb.subject%s_fnc(subject_id, come_date, FNC1, FNC2, FNC3, FNC4, FNC5, FNC6, FNC7, FNC8, FNC9, FNC10," \
                    "FNC11, FNC12, FNC13, FNC14, FNC15, FNC16, FNC17, FNC18, FNC19, FNC20, FNC21, FNC22, FNC23, FNC24, FNC25," \
                    "FNC26, FNC27, FNC28, FNC29, FNC30, FNC31, FNC32, FNC33, FNC34, FNC35, FNC36, FNC37, FNC38, FNC39, FNC40," \
                    "FNC41, FNC42, FNC43, FNC44, FNC45, FNC46, FNC47, FNC48, FNC49, FNC50, FNC51, FNC52, FNC53, FNC54, FNC55," \
                    "FNC56, FNC57, FNC58, FNC59, FNC60, FNC61, FNC62, FNC63, FNC64, FNC65, FNC66, FNC67, FNC68, FNC69, FNC70," \
                    "FNC71, FNC72, FNC73, FNC74, FNC75, FNC76, FNC77, FNC78, FNC79, FNC80, FNC81, FNC82, FNC83, FNC84, FNC85," \
                    "FNC86, FNC87, FNC88, FNC89, FNC90, FNC91, FNC92, FNC93, FNC94, FNC95, FNC96, FNC97, FNC98, FNC99, FNC100," \
                    "FNC101, FNC102, FNC103, FNC104, FNC105, FNC106, FNC107, FNC108, FNC109, FNC110, FNC111, FNC112, FNC113, FNC114, FNC115," \
                    "FNC116, FNC117, FNC118, FNC119, FNC120, FNC121, FNC122, FNC123, FNC124, FNC125, FNC126, FNC127, FNC128, FNC129, FNC130," \
                    "FNC131, FNC132, FNC133, FNC134, FNC135, FNC136, FNC137, FNC138, FNC139, FNC140, FNC141, FNC142, FNC143, FNC144, FNC145," \
                    "FNC146, FNC147, FNC148, FNC149, FNC150, FNC151, FNC152, FNC153, FNC154, FNC155, FNC156, FNC157, FNC158, FNC159, FNC160," \
                    "FNC161, FNC162, FNC163, FNC164, FNC165, FNC166, FNC167, FNC168, FNC169, FNC170, FNC171, FNC172, FNC173, FNC174, FNC175," \
                    "FNC176, FNC177, FNC178, FNC179, FNC180, FNC181, FNC182, FNC183, FNC184, FNC185, FNC186, FNC187, FNC188, FNC189, FNC190," \
                    "FNC191, FNC192, FNC193, FNC194, FNC195, FNC196, FNC197, FNC198, FNC199, FNC200, FNC201, FNC202, FNC203, FNC204, FNC205," \
                    "FNC206, FNC207, FNC208, FNC209, FNC210, FNC211, FNC212, FNC213, FNC214, FNC215, FNC216, FNC217, FNC218, FNC219, FNC220," \
                    "FNC221, FNC222, FNC223, FNC224, FNC225, FNC226, FNC227, FNC228, FNC229, FNC230, FNC231, FNC232, FNC233, FNC234, FNC235," \
                    "FNC236, FNC237, FNC238, FNC239, FNC240, FNC241, FNC242, FNC243, FNC244, FNC245, FNC246, FNC247, FNC248, FNC249, FNC250," \
                    "FNC251, FNC252, FNC253, FNC254, FNC255, FNC256, FNC257, FNC258, FNC259, FNC260, FNC261, FNC262, FNC263, FNC264, FNC265," \
                    "FNC266, FNC267, FNC268, FNC269, FNC270, FNC271, FNC272, FNC273, FNC274, FNC275, FNC276, FNC277, FNC278, FNC279, FNC280," \
                    "FNC281, FNC282, FNC283, FNC284, FNC285, FNC286, FNC287, FNC288, FNC289, FNC290, FNC291, FNC292, FNC293, FNC294, FNC295," \
                    "FNC296, FNC297, FNC298, FNC299, FNC300, FNC301, FNC302, FNC303, FNC304, FNC305, FNC306, FNC307, FNC308, FNC309, FNC310," \
                    "FNC311, FNC312, FNC313, FNC314, FNC315, FNC316, FNC317, FNC318, FNC319, FNC320, FNC321, FNC322, FNC323, FNC324, FNC325," \
                    "FNC326, FNC327, FNC328, FNC329, FNC330, FNC331, FNC332, FNC333, FNC334, FNC335, FNC336, FNC337, FNC338, FNC339, FNC340," \
                    "FNC341, FNC342, FNC343, FNC344, FNC345, FNC346, FNC347, FNC348, FNC349, FNC350, FNC351, FNC352, FNC353, FNC354, FNC355," \
                    "FNC356, FNC357, FNC358, FNC359, FNC360, FNC361, FNC362, FNC363, FNC364, FNC365, FNC366, FNC367, FNC368, FNC369, FNC370," \
                    "FNC371, FNC372, FNC373, FNC374, FNC375, FNC376, FNC377, FNC378)"
                    "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                    % (patId, data[1], data[0], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10],
                       data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20],
                       data[21], data[22], data[23], data[24], data[25], data[26], data[27], data[28], data[29], data[30],
                       data[31], data[32], data[33], data[34], data[35], data[36], data[37], data[38], data[39], data[40],
                       data[41], data[42], data[43], data[44], data[45], data[46], data[47], data[48], data[49], data[50],
                       data[51], data[52], data[53], data[54], data[55], data[56], data[57], data[58], data[59], data[60],
                       data[61], data[62], data[63], data[64], data[65], data[66], data[67], data[68], data[69], data[70],
                       data[71], data[72], data[73], data[74], data[75], data[76], data[77], data[78], data[79], data[80],
                       data[81], data[82], data[83], data[84], data[85], data[86], data[87], data[88], data[89], data[90],
                       data[91], data[92], data[93], data[94], data[95], data[96], data[97], data[98], data[99], data[100],
                       data[101], data[102], data[103], data[104], data[105], data[106], data[107], data[108], data[109], data[110],
                       data[111], data[112], data[113], data[114], data[115], data[116], data[117], data[118], data[119], data[120],
                       data[121], data[122], data[123], data[124], data[125], data[126], data[127], data[128], data[129], data[130],
                       data[131], data[132], data[133], data[134], data[135], data[136], data[137], data[138], data[139], data[140],
                       data[141], data[142], data[143], data[144], data[145], data[146], data[147], data[148], data[149], data[150],
                       data[151], data[152], data[153], data[154], data[155], data[156], data[157], data[158], data[159], data[160],
                       data[161], data[162], data[163], data[164], data[165], data[166], data[167], data[168], data[169], data[170],
                       data[171], data[172], data[173], data[174], data[175], data[176], data[177], data[178], data[179], data[180],
                       data[181], data[182], data[183], data[184], data[185], data[186], data[187], data[188], data[189], data[190],
                       data[191], data[192], data[193], data[194], data[195], data[196], data[197], data[198], data[199], data[200],
                       data[201], data[202], data[203], data[204], data[205], data[206], data[207], data[208], data[209], data[210],
                       data[211], data[212], data[213], data[214], data[215], data[216], data[217], data[218], data[219], data[220],
                       data[221], data[222], data[223], data[224], data[225], data[226], data[227], data[228], data[229], data[230],
                       data[231], data[232], data[233], data[234], data[235], data[236], data[237], data[238], data[239], data[240],
                       data[241], data[242], data[243], data[244], data[245], data[246], data[247], data[248], data[249], data[250],
                       data[251], data[252], data[253], data[254], data[255], data[256], data[257], data[258], data[259], data[260],
                       data[261], data[262], data[263], data[264], data[265], data[266], data[267], data[268], data[269], data[270],
                       data[271], data[272], data[273], data[274], data[275], data[276], data[277], data[278], data[279], data[280],
                       data[281], data[282], data[283], data[284], data[285], data[286], data[287], data[288], data[289], data[290],
                       data[291], data[292], data[293], data[294], data[295], data[296], data[297], data[298], data[299], data[300],
                       data[301], data[302], data[303], data[304], data[305], data[306], data[307], data[308], data[309], data[310],
                       data[311], data[312], data[313], data[314], data[315], data[316], data[317], data[318], data[319], data[320],
                       data[321], data[322], data[323], data[324], data[325], data[326], data[327], data[328], data[329], data[330],
                       data[331], data[332], data[333], data[334], data[335], data[336], data[337], data[338], data[339], data[340],
                       data[341], data[342], data[343], data[344], data[345], data[346], data[347], data[348], data[349], data[350],
                       data[351], data[352], data[353], data[354], data[355], data[356], data[357], data[358], data[359], data[360],
                       data[361], data[362], data[363], data[364], data[365], data[366], data[367], data[368], data[369], data[370],
                       data[371], data[372], data[373], data[374], data[375], data[376], data[377], data[378], data[379]))
                conn.commit()

                f = open(sbm_data, 'r')
                csvReader = csv.reader(f)

                for row in csvReader:
                    data = []
                    data.append(come_date)
                    num = 0
                    for col in row:
                        if num < 33:
                            data.append(row[num])
                            num = num + 1

                data2 = cur.execute(
                    "INSERT INTO mydb.subject%s_sbm(subject_id, come_date, SBM_map1, SBM_map2, SBM_map3, SBM_map4, SBM_map5, SBM_map6, SBM_map7, SBM_map8," \
                    "SBM_map10, SBM_map13, SBM_map17, SBM_map22, SBM_map26, SBM_map28, SBM_map32, SBM_map36, SBM_map40, SBM_map43, SBM_map45, SBM_map48," \
                    "SBM_map51, SBM_map52, SBM_map55, SBM_map61, SBM_map64, SBM_map67, SBM_map69, SBM_map71, SBM_map72, SBM_map73, SBM_map74, SBM_map75)"
                    "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                    "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"
                    % (patId, data[1], data[0], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12],
                       data[13], data[14], data[15], data[16], data[17], data[18], data[19], data[20], data[21], data[22], data[23], data[24], data[25],
                       data[26], data[27], data[28], data[29], data[30], data[31], data[32], data[33]))
                conn.commit()

                f = open(eeg_data, 'r')
                csvReader = csv.reader(f)

                sql = "SELECT EXISTS(SELECT * FROM mydb.subject%s_eeg WHERE subject_id = '%s')" % (patId, patId)
                cur.execute(sql)
                rs = cur.fetchall()
                for row in rs:
                    # 등록된 데이터가 있는 경우
                    if row[0] == 1:
                        sql = "TRUNCATE TABLE mydb.subject%s_eeg" % (patId)
                        cur.execute(sql)
                        conn.commit()

                # # data3 = cur.execute("LOAD DATA INFILE ''%s'' INTO TABLE mydb.subject%s_eeg FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'") % (eeg_data, patId)
                # # conn.commit()

                for row in csvReader:
                    data = []
                    num = 1
                    for col in row:
                        if num < 68:
                            data.append(row[num])
                            num = num + 1
                    data[0] = float(data[0])
                    data[0] = int(data[0])
                    data[1] = float(data[1])
                    data[1] = int(data[1])
                    data[2] = float(data[2])
                    data[2] = int(data[2])
                    data3 = cur.execute(
                        "INSERT INTO `mydb`.`subject%s_eeg` (`subject_id`, `trial`, `condition`, `sample`, `Fp1`, `AF7`, `AF3`, `F1`, `F3`, `F5`, `F7`, `FT7`, `FC5`, `FC3`, `FC1`, `C1`, `C3`," \
                        "`C5`, `T7`, `TP7`, `CP5`, `CP3`, `CP1`, `P1`, `P3`, `P5`, `P7`, `P9`, `PO7`, `PO3`, `O1`, `lz`, `Oz`, `POz`, `Pz`, `CPz`, `Fpz`, `Fp2`, `AF8`, `AF4`, `AFz`, `Fz`," \
                        "`F2`, `F4`, `F6`, `F8`, `FT8`, `FC6`, `FC4`, `FC2`, `FCz`, `Cz`, `C2`, `C4`, `C6`, `T8`, `TP8`, `CP6`, `CP4`, `CP2`, `P2`, `P4`, `P6`, `P8`, `P10`, `PO8`, `PO4`, `O2`)"
                        "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                        "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                        "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'," \
                        "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (
                        patId, patId, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9],
                        data[10], data[11], data[12], data[13], data[14], data[15], data[16], data[17], data[18], data[19],
                        data[20], data[21], data[22], data[23], data[24], data[25], data[26], data[27], data[28], data[29],
                        data[30], data[31], data[32], data[33], data[34], data[35], data[36], data[37], data[38], data[39],
                        data[40], data[41], data[42], data[43], data[44], data[45], data[46], data[47], data[48], data[49],
                        data[50], data[51], data[52], data[53], data[54], data[55], data[56], data[57], data[58], data[59],
                        data[60], data[61], data[62], data[63], data[64], data[65], data[66]))
                    conn.commit()

                if (data1 + data2 + data3 == 3):
                    self.messagebox("알림", "데이터가 등록되었습니다.")

            self.PatDiagWidget_2.show()
            self.ResShowErr.setText(_translate("MainWindow", ""))
            self.brainGraphShow()

    # 환자 등록번호 입력 이벤트 처리
    def pat_diag_clicked(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        msg = self.PatDiagErr

        # 빈 정보를 입력했을 때
        if not self.PatNum.text():
            msg.setText(_translate("MainWindow", "등록번호를 입력해주세요."))
        # 입력 값과 DB의 계정 정보 비교
        else:
            with conn.cursor() as curs:
                global patId
                patId = self.PatNum.text()
                sql = "SELECT EXISTS(SELECT * FROM mydb.subject_info WHERE subject_id = '%s')" % patId
                curs.execute(sql)
                rs = curs.fetchall()
                for row in rs:
                    # 등록되지 않은 번호일 경우
                    if row[0] == 0:
                        msg.setText(_translate("MainWindow", "등록되지 않은 번호입니다."))
                    # 등록된 번호일 경우
                    else:
                        self.PerLabel_1.setText("")
                        self.label.setText("Fz")
                        self.ResShowErr.setText("")
                        self.PatDiagWidget_2.show()
                        self.PatDiagWidget_1.hide()
                        self.PatRegWidget_1.hide()
                        self.PatRegWidget_2.hide()
                        self.HomeWidget.hide()
                        self.showPatInf()
                        self.brainGraphShow()

    # 환자 정보 테이블 이벤트
    def showPatInf(self):
        _translate = QtCore.QCoreApplication.translate

        with conn.cursor() as curs:
            sql = "SELECT * FROM mydb.subject_info WHERE subject_id = '%s'" % patId
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                item = self.PatientInfoTable.item(0, 0)
                item.setText(_translate("MainWindow", row[0]))
                item = self.PatientInfoTable.item(1, 0)
                item.setText(_translate("MainWindow", row[1]))
                item = self.PatientInfoTable.item(2, 0)
                item.setText(_translate("MainWindow", row[2]))
                item = self.PatientInfoTable.item(3, 0)
                item.setText(_translate("MainWindow", row[3]))
                item = self.PatientInfoTable.item(4, 0)
                if row[4] == '0':
                    item.setText(_translate("MainWindow", "HC"))
                elif row[4] == '1':
                    item.setText(_translate("MainWindow", "SZ"))
                else:
                    item.setText(_translate("MainWindow", "Pending"))
                item = self.PatientInfoTable.item(5, 0)
                item.setText(_translate("MainWindow", row[5]))
                item = self.PatientInfoTable.item(6, 0)
                item.setText(_translate("MainWindow", row[6]))

    # 결과 변화 그래프 그리기
    def ResCmpGraph(self, MainWindow):
        with conn.cursor() as curs:
            sql = "SELECT come_date, result FROM mydb.diagnose_record WHERE subject_id = '%s'" % patId
            curs.execute(sql)
            rs = curs.fetchall()

            x = []
            y = []
            for row in rs:
                x.append(row[0])
                y.append(row[1])

            while True:
                if len(x) > 10:
                    x.pop(0)
                    y.pop(0)
                else:
                    break

            ax3 = self.fig3.add_subplot(1, 1, 1)
            ax3.clear()
            ax3.grid()
            ax3.plot(x, y, 'ro-', label= "MRI Predict")
            ax3.set_xlabel('Date', fontsize=12, color="blue")
            ax3.set_ylabel('Percentage (%)', fontsize=12, color="blue")
            #ax3.set_ylim(0, 100)
            ax3.legend(loc='best')
            self.ResChanGraph.draw()

    # 의사 계정관리 비밀번호 입력 이벤트 처리
    def acct_man_clicked(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        msg = self.AcctManErrMsg

        # 빈 정보를 입력했을 때
        if not self.PWEnt.text():
            msg.setText(_translate("LoginWindow", "비밀번호를 입력해주세요."))
        # 입력 값과 DB의 계정 정보 비교
        else:
            with conn.cursor() as curs:
                sql = "SELECT password FROM mydb.doctor_info WHERE dr_id = '%s'" % drId
                curs.execute(sql)
                rs = curs.fetchall()
                for row in rs:
                    # PW 틀렸을 시
                    if self.PWEnt.text() != row[0]:
                        msg.setText(_translate("MainWindow", "비밀번호가 틀립니다."))
                    # PW 입력 성공
                    else:
                        self.AccManWidget_2.show()
                        self.AccManWidget_1.hide()
                        self.PatDiagWidget_1.hide()
                        self.PatDiagWidget_2.hide()
                        self.PatDiagWidget_3.hide()
                        self.PatRegWidget_1.hide()
                        self.PatRegWidget_2.hide()
                        self.PatRegWidget_3.hide()
                        self.HomeWidget.hide()
                        self.acct_man_window()  # 의사 계정정보 수정 이벤트 처리

    # 의사 계정정보 수정 이벤트 처리
    def acct_man_window(self):
        _translate = QtCore.QCoreApplication.translate

        self.UserPW.setText("")
        self.UserPWCheck.setText("")
        self.AcctManErrMsg_2.setText(_translate("MainWindow", ""))
        self.UserNameErr.setText(_translate("MainWindow", ""))
        self.UserBirthErr.setText(_translate("MainWindow", ""))
        self.UserPhoneErr.setText(_translate("MainWindow", ""))
        self.UserHosErr.setText(_translate("MainWindow", ""))
        self.UserDepErr.setText(_translate("MainWindow", ""))

        with conn.cursor() as curs:
            sql = "SELECT * FROM mydb.doctor_info WHERE dr_id = '%s'" % drId
            curs.execute(sql)
            rs = curs.fetchall()
            for row in rs:
                # 계정 정보 출력
                self.UserID.setText(_translate("MainWindow", row[0]))
                self.UserName.setText(_translate("MainWindow", row[2]))
                self.UserBirth.setText(_translate("MainWindow", row[3]))
                self.UserHos.setText(_translate("MainWindow", row[5]))
                self.UserDep.setText(_translate("MainWindow", row[6]))
                self.UserPhone.setText(_translate("MainWindow", row[7]))
                if row[4] == "F":
                    self.UserFBtn.setChecked(True)
                else:
                    self.UserMBtn.setChecked(True)

        self.UserSubBtn_Ok.clicked.connect(self.acct_man_modify)
        self.UserSubBtn_Ok.clicked.connect(self.AccManInitialize)
        self.UserSubBtn_Cancel.clicked.connect(self.AccManWidget_1.show)
        self.UserSubBtn_Cancel.clicked.connect(self.AccManInitialize)


    # 계정정보 수정 - DB에 commit
    def acct_man_modify(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate

        num = 0

        self.AcctManErrMsg_2.setText(_translate("MainWindow", ""))
        self.UserNameErr.setText(_translate("MainWindow", ""))
        self.UserBirthErr.setText(_translate("MainWindow", ""))
        self.UserPhoneErr.setText(_translate("MainWindow", ""))
        self.UserHosErr.setText(_translate("MainWindow", ""))
        self.UserDepErr.setText(_translate("MainWindow", ""))

        # 빈 정보를 입력했을 때
        if not self.UserPW.text():
            self.AcctManErrMsg_2.setText(_translate("MainWindow", "비밀번호를 입력해주세요."))  # 비밀번호 미입력
        elif self.UserPW.text() != self.UserPWCheck.text():
            self.AcctManErrMsg_2.setText(_translate("MainWindow", "비밀번호가 일치하지 않습니다."))  # 비밀번호 확인 불일치
        else:
            num += 1
        if not self.UserName.text():
            self.UserNameErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            num += 1
        if not self.UserBirth.text():
            self.UserBirthErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            num += 1
        if not self.UserPhone.text():
            self.UserPhoneErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            num += 1
        if not self.UserHos.text():
            self.UserHosErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            num += 1
        if not self.UserDep.text():
            self.UserDepErr.setText(_translate("MainWindow", "필수 정보입니다."))
        else:
            num += 1

        if num == 6:
            # 모든 정보가 입력된 경우
            if self.UserMBtn.isChecked():
                gender = 'M'
            else:
                gender = 'F'

            with conn.cursor() as curs:
                sql2 = "UPDATE mydb.doctor_info SET password=%s, name=%s, birth=%s, gender=%s, hospital=%s, department=%s, phone=%s WHERE dr_id=%s"

                val = (self.UserPW.text(), self.UserName.text(), self.UserBirth.text(), gender, self.UserHos.text(), self.UserDep.text(), self.UserPhone.text(), drId)

                data = curs.execute(sql2, val)
                conn.commit()

                if (data):
                    self.messagebox("알림", "정보가 수정되었습니다.")

                self.AccManWidget_1.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Main"))
        self.PatRegBtn.setText(_translate("MainWindow", "환자 등록"))
        self.PatDiagBtn.setText(_translate("MainWindow", "환자 진단"))
        self.AccManBtn.setText(_translate("MainWindow", "계정 관리"))
        self.HomeLabel.setText(_translate("MainWindow", "HOME"))
        self.ExpLabel_1.setText(_translate("MainWindow", "Welcome to EASY EEG!"))
        self.ExpLabel_2.setText(_translate("MainWindow", "EASY EEG에서 손쉽게 조현병을 진단할 수 있습니다.\n"
"\n"
"\n"
"[환자 등록]\n"
"\n"
"- 새 환자 등록 : 새로운 환자를 등록합니다. 모든 정보를 입력 후 등록을 진행합니다.\n"
"\n"
"- 환자 조회 : 환자의 등록 여부 및 정보를 조회합니다.\n"
"\n"
"* 뇌파 데이터는 .csv 형식만 지원됩니다.\n"
"\n"
"\n"
"[환자 진단]\n"
"\n"
"- 등록된 환자의 뇌파를 건강인/환자의 평균 뇌파와 비교할 수 있습니다.\n"
"\n"
"- 결과 보기 : MRI를 이용하여 조현병 예상 확률을 진단합니다.\n"
"\n"
"- 지난 결과 비교 : 등록된 지난 예상 확률 진단 기록을 그래프로 비교할 수 있습니다.\n"
"\n"
"\n"
"[계정 관리]\n"
"\n"
"- 사용자의 계정 정보 수정 및 관리가 가능합니다."))
        self.AccManLabel_2.setText(_translate("MainWindow", "계정 관리"))
        self.UserIDLabel.setText(_translate("MainWindow", "계정 ID"))
        self.UserPWLabel.setText(_translate("MainWindow", "비밀번호"))
        self.UserNameLabel.setText(_translate("MainWindow", "이름"))
        self.UserAgeLabel.setText(_translate("MainWindow", "생년월일"))
        self.UserGenLabel.setText(_translate("MainWindow", "성별"))
        self.UserPhoneLabel.setText(_translate("MainWindow", "연락처"))
        self.UserHosLabel.setText(_translate("MainWindow", "소속 병원"))
        self.UserDepLabel.setText(_translate("MainWindow", "소속 과"))
        self.UserWDBtn.setText(_translate("MainWindow", "회원탈퇴"))
        self.PWCheckLabel.setText(_translate("MainWindow", "확인"))
        self.UserMBtn.setText(_translate("MainWindow", "MALE"))
        self.UserFBtn.setText(_translate("MainWindow", "FEMALE"))
        self.AcctManErrMsg_2.setText(_translate("MainWindow", ""))
        self.UserSubBtn_Ok.setText(_translate("MainWindow", "정보수정"))
        self.UserSubBtn_Cancel.setText(_translate("MainWindow", "취소"))
        self.UserBirthErr.setText(_translate("MainWindow", ""))
        self.UserNameErr.setText(_translate("MainWindow", ""))
        self.UserPhoneErr.setText(_translate("MainWindow", ""))
        self.UserHosErr.setText(_translate("MainWindow", ""))
        self.UserDepErr.setText(_translate("MainWindow", ""))
        self.PatRegLabel.setText(_translate("MainWindow", "환자 등록"))
        self.NewPatBtn.setText(_translate("MainWindow", "         새 환자 등록                                            >"))
        self.ExiPatLabel.setText(_translate("MainWindow", "             환자 조회"))
        self.ExiPatBtn.setText(_translate("MainWindow", "검색"))
        self.PatSearErr.setText(_translate("MainWindow", ""))
        self.PatIDLabel.setText(_translate("MainWindow", "환자 등록번호"))
        self.PatNameLabel.setText(_translate("MainWindow", "이름"))
        self.PatDateLabel.setText(_translate("MainWindow", "생년월일"))
        self.PatGenLabel.setText(_translate("MainWindow", "성별"))
        self.PatGroupLabel.setText(_translate("MainWindow", "조현병 여부"))
        self.PatPhoneLabel.setText(_translate("MainWindow", "연락처"))
        self.PatDocIDLabel.setText(_translate("MainWindow", "등록 의사 ID"))
        self.PatLabel.setText(_translate("MainWindow", "새 환자 등록"))
        self.PatOkBtn.setText(_translate("MainWindow", "등록"))
        self.PatCanBtn.setText(_translate("MainWindow", "취소"))
        self.PatNumErr.setText(_translate("MainWindow", ""))
        self.PatNameErr.setText(_translate("MainWindow", ""))
        self.PatPhoneErr.setText(_translate("MainWindow", ""))
        self.PatDocIDErr.setText(_translate("MainWindow", ""))
        self.PatMBtn.setText(_translate("MainWindow", "MALE"))
        self.PatFBtn.setText(_translate("MainWindow", "FEMALE"))
        self.PatHCBtn.setText(_translate("MainWindow", "HC"))
        self.PatSZBtn.setText(_translate("MainWindow", "SZ"))
        self.PatPenBtn.setText(_translate("MainWindow", "Pending"))
        self.label.setText(_translate("MainWindow", ""))
        self.ChannelName.setText(_translate("MainWindow", "채널 그래프 - "))
        self.PerLabel_2.setText(_translate("MainWindow", "%"))
        self.MsgLabel.setText(_translate("MainWindow", "확률로 조현병이 예상됩니다."))
        self.DataRegBtn.setText(_translate("MainWindow", "데이터 등록"))
        self.ResultBtn.setText(_translate("MainWindow", "결과 보기"))
        self.ResCmpBtn.setText(_translate("MainWindow", "지난 결과 비교"))
        self.PatientInfoTable.setSortingEnabled(False)
        item = self.PatientInfoTable.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", " 환자 등록번호     "))
        item = self.PatientInfoTable.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", " 이름"))
        item = self.PatientInfoTable.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", " 생년월일"))
        item = self.PatientInfoTable.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", " 성별"))
        item = self.PatientInfoTable.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", " 조현병 유무"))
        item = self.PatientInfoTable.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", " 연락처"))
        item = self.PatientInfoTable.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", " 등록 의사 ID"))
        item = self.PatientInfoTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "환자 정보"))
        self.ResChanLabel.setText(_translate("MainWindow", "결과 변화 그래프"))
        self.T1_Label.setText(_translate("MainWindow", "AX T1"))
        self.T2_Label.setText(_translate("MainWindow", "AX T2"))
        self.ResShowErr.setText(_translate("MainWindow", ""))
        self.BackBtn.setText(_translate("MainWindow", "이전 화면"))
        self.PatSearBtn.setText(_translate("MainWindow", "검색"))
        self.PatDiagLabel.setText(_translate("MainWindow", "환자 진단"))
        self.PatSearLabel.setText(_translate("MainWindow", "           환자 등록번호"))
        self.PatDiagErr.setText(_translate("MainWindow", ""))
        self.AccManLabel_1.setText(_translate("MainWindow", "계정 관리"))
        self.PWEntBtn.setText(_translate("MainWindow", "확인"))
        self.PWEntLabel.setText(_translate("MainWindow", "           비밀번호 입력"))
        self.AcctManErrMsg.setText(_translate("MainWindow", ""))
        self.NameLabel.setText(_translate("MainWindow", drId))
        self.PatLabel_2.setText(_translate("MainWindow", "환자 조회"))
        self.BackBtn_2.setText(_translate("MainWindow", "이전 화면"))
        self.SearPatInfTable.setSortingEnabled(False)
        item = self.SearPatInfTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "환자 등록번호"))
        item = self.SearPatInfTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "이름"))
        item = self.SearPatInfTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "생년월일"))
        item = self.SearPatInfTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "성별"))
        item = self.SearPatInfTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "조현병 여부"))
        item = self.SearPatInfTable.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "연락처"))
        item = self.SearPatInfTable.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "등록 의사 ID"))
        __sortingEnabled = self.SearPatInfTable.isSortingEnabled()
        self.HomeBtn.setText(_translate("MainWindow", "HOME"))
        self.DateLabel.setText(_translate("MainWindow", "등록 날짜"))
        self.FNCLabel.setText(_translate("MainWindow", "FNC Data"))
        self.SBMLabel.setText(_translate("MainWindow", "SBM Data"))
        self.EEGLabel.setText(_translate("MainWindow", "EEG Data"))
        self.DataLabel.setText(_translate("MainWindow", "진단 데이터 등록"))
        self.DataOkBtn.setText(_translate("MainWindow", "OK"))
        self.DataCanBtn.setText(_translate("MainWindow", "Cancel"))
        self.FNCDataErr.setText(_translate("MainWindow", ""))
        self.SBMDataErr.setText(_translate("MainWindow", ""))
        self.EEGDataErr.setText(_translate("MainWindow", ""))
        self.FNCFileBtn.setText(_translate("MainWindow", "파일 찾기"))
        self.EEGFileBtn.setText(_translate("MainWindow", "파일 찾기"))
        self.SBMFileBtn.setText(_translate("MainWindow", "파일 찾기"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    app.exec_()
