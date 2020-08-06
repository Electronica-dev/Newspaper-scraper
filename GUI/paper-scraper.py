# A multi threaded web scraping GUI

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from pathlib import Path
from prajavaniLogic import prajavani_download
from karavaliLogic import karavali_download
from os import path
import traceback


# Main class
class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.setMinimumSize(QtCore.QSize(660, 220))
        MainWindow.setMaximumSize(QtCore.QSize(660, 220))
        MainWindow.setWindowIcon((QtGui.QIcon('paper.png')))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setObjectName("gridLayout")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 2)

        self.yes_cb = QtWidgets.QRadioButton(self.centralwidget)
        self.yes_cb.setObjectName("yes_cb")
        self.gridLayout.addWidget(self.yes_cb, 1, 2, 1, 1)
        self.yes_cb.clicked.connect(self.yes_cb_clicked)

        self.no_cb = QtWidgets.QRadioButton(self.centralwidget)
        self.no_cb.setObjectName("no_cb")
        self.gridLayout.addWidget(self.no_cb, 1, 3, 1, 1)
        self.no_cb.setChecked(True)
        self.no_cb.clicked.connect(self.no_cb_clicked)

        self.directory_label = QtWidgets.QLabel(self.centralwidget)
        self.directory_label.setTextFormat(QtCore.Qt.AutoText)
        self.directory_label.setObjectName("directory_label")
        self.gridLayout.addWidget(self.directory_label, 3, 0, 1, 1)

        self.karavali_cb = QtWidgets.QCheckBox(self.centralwidget)
        self.karavali_cb.setObjectName("karavali_cb")
        self.gridLayout.addWidget(self.karavali_cb, 0, 3, 1, 1)

        self.prajavani_cb = QtWidgets.QCheckBox(self.centralwidget)
        self.prajavani_cb.setObjectName("prajavani_cb")
        self.gridLayout.addWidget(self.prajavani_cb, 0, 2, 1, 1)

        self.recipient_address_label = QtWidgets.QLabel(self.centralwidget)
        self.recipient_address_label.setObjectName("recipient_address_label")
        self.gridLayout.addWidget(self.recipient_address_label, 2, 0, 1, 1, alignment=QtCore.Qt.AlignTop)

        self.add_email_te = QtWidgets.QTextEdit(self.centralwidget)
        self.add_email_te.setStyleSheet('font-size: 12pt')
        self.add_email_te.setObjectName("add_email_te")
        self.gridLayout.addWidget(self.add_email_te, 2, 1, 1, 4)
        self.add_email_te.setDisabled(True)

        self.open_btn = QtWidgets.QPushButton(self.centralwidget)
        self.open_btn.setObjectName("open_btn")
        self.open_btn.setIcon(QtGui.QIcon('open.png'))
        self.open_btn.setIconSize(QtCore.QSize(21, 21))
        self.open_btn.setSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        self.gridLayout.addWidget(self.open_btn, 3, 4)
        self.open_btn.clicked.connect(self.open_file_dialog)

        self.directory_le = QtWidgets.QLineEdit(self.centralwidget)
        self.directory_le.setStyleSheet('font-size: 12pt')
        self.directory_le.setMaxLength(64)
        self.directory_le.setObjectName("directory_le")
        self.gridLayout.addWidget(self.directory_le, 3, 1, 1, 3)

        self.start_btn = QtWidgets.QPushButton(self.centralwidget)
        self.start_btn.setObjectName("start_btn")
        self.start_btn.setMinimumWidth(120)
        self.gridLayout.addWidget(self.start_btn, 5, 1, 1, 2)
        self.gridLayout.setAlignment(self.start_btn, QtCore.Qt.AlignHCenter)
        self.start_btn.clicked.connect(self.start_scraping)

        self.progress_label = QtWidgets.QLabel(self.centralwidget)
        self.progress_label.setObjectName('progress_label')
        self.gridLayout.addWidget(self.progress_label, 6, 0)
        self.progress_label.hide()

        self.progress_bar = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar.setObjectName('progress_bar')
        self.gridLayout.addWidget(self.progress_bar, 6, 3, 1, 2)
        self.progress_bar.hide()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Newspaper Scraper"))
        self.start_btn.setText(_translate("MainWindow", "Start scraping"))
        self.start_btn.setStyleSheet('font-size: 12pt')

        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\"font-size:12pt;\">Select the "
                                                    "newspaper you want to scrape:</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\"font-size:12pt;\">Do you "
                                                      "want an email to be sent?</span></p></body></html>"))
        self.progress_label.setStyleSheet('font-size: 12pt')

        self.yes_cb.setText(_translate("MainWindow", "Yes"))
        self.yes_cb.setStyleSheet('font-size: 12pt')
        self.no_cb.setText(_translate("MainWindow", "No"))
        self.no_cb.setStyleSheet('font-size: 12pt')

        self.directory_label.setText(_translate("MainWindow", "<html><head/><body><p><span "
                                                              "style=\"font-size:12pt;\">Directory to save files: "
                                                              "</span></p></body></html>"))
        self.recipient_address_label.setText(_translate("MainWindow", "<html><head/><body><p><span "
                                                              "style=\"font-size:12pt;\">Recipient address: "
                                                              "</span></p></body></html>"))

        self.karavali_cb.setText(_translate("MainWindow", "Karavali Munjavu"))
        self.karavali_cb.setStyleSheet('font-size: 12pt')
        self.prajavani_cb.setText(_translate("MainWindow", "Prajavani"))
        self.prajavani_cb.setStyleSheet('font-size: 12pt')

    def yes_cb_clicked(self):
            self.add_email_te.setEnabled(True)
            self.add_email_te.setToolTip('Separate multiple emails with a comma')

    def no_cb_clicked(self):
            self.add_email_te.clear()
            self.add_email_te.setDisabled(True)

    def open_file_dialog(self):
        home_dir = str(Path.home())
        f_name = QtWidgets.QFileDialog.getExistingDirectory(self.centralwidget, 'Open file', home_dir)
        self.directory_le.setText(str(f_name))

    def start_scraping(self):
        if self.directory_le.text() == '':
            self.directory_le.setPlaceholderText('Please specify a directory')
        elif not path.isdir(self.directory_le.text()):
            QtWidgets.QMessageBox.critical(self.centralwidget, 'Error', "<html><span "
                                                                        "style=\"font-size:12pt;\">Directory does not "
                                                                        "exist</span></html>",
                                           QtWidgets.QMessageBox.Ok)
        elif path.isdir(self.directory_le.text()):
            if self.prajavani_cb.isChecked() and self.karavali_cb.isChecked():
                QtWidgets.QMessageBox.warning(self.centralwidget, 'Warning', "<html><span "
                                                                             "style=\"font-size:12pt;\">This will open "
                                                                             "a browser window (only for Prajavani). It is "
                                                                             "recommended that "
                                                                             "you don't interrupt the scraping process "
                                                                             "as it can lead to errors. "
                                                                             "</span></html>",
                                              QtWidgets.QMessageBox.Ok)
                self.pr_thread = PrajavaniThread(self.directory_le.text(), self.add_email_te.text())
                self.pr_thread.start()
                self.kr_thread = KaravaliThread(self.directory_le.text(), self.add_email_te.text())
                self.kr_thread.start()
            if self.prajavani_cb.isChecked():
                QtWidgets.QMessageBox.warning(self.centralwidget, 'Warning', "<html><span "
                                                                            "style=\"font-size:12pt;\">This will open "
                                                                            "a browser window (only for Prajavani). It is "
                                                                             "recommended that "
                                                                            "you don't interrupt the scraping process "
                                                                            "as it can lead to errors. "
                                                                            "</span></html>",
                                              QtWidgets.QMessageBox.Ok)
                self.pr_thread = PrajavaniThread(self.directory_le.text(), self.add_email_te.toPlainText())
                self.pr_thread.start()
            if self.karavali_cb.isChecked():
                self.kr_thread = KaravaliThread(self.directory_le.text(), self.add_email_te.toPlainText())
                self.kr_thread.start()


class PrajavaniThread(QtCore.QThread):
    """Thread to scrape prajavani."""
    def __init__(self, directory, emails):
        super().__init__()
        self.directory = directory
        email_list = emails.split(',')
        self.email_list = [ele.strip() for ele in email_list]

    def __del__(self):
        self.wait()

    def run(self):
        try:
            prajavani_download(self.directory, self.email_list)
        except:
            self.exception_thread = ExceptionThread(traceback.format_exc())
            self.exception_thread.start()


class KaravaliThread(QtCore.QThread):
    """Thread to scrape karavali munjavu."""
    def __init__(self, directory, emails):
        super().__init__()
        self.directory = directory
        email_list = emails.split(',')
        self.email_list = [ele.strip() for ele in email_list]

    def run(self):
        try:
            karavali_download(self.directory, self.email_list)
        except:
            self.exception_thread = ExceptionThread(traceback.format_exc())
            self.exception_thread.start()


class ExceptionThread(QtCore.QThread):
    """Thread to write exceptions to a file"""
    def __init__(self, exception):
        super().__init__()
        self.exception = exception

    def run(self):
        error_file = open('error_info.txt', 'w')
        error_file.write(self.exception)
        error_file.close()


def main():
    app = QtWidgets.QApplication([])
    mw = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    mw.setupUi(w)
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
