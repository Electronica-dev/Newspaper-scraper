""" A multi threaded web scraping GUI """

import sys
from pathlib import Path
from os import path
from PyQt5 import QtCore, QtGui, QtWidgets
from prajavani_logic import DownloadPrajavani
from karavali_logic import DownloadKaravali


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.setFixedSize(QtCore.QSize(760, 240))
        MainWindow.setWindowIcon((QtGui.QIcon('paper.png')))

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)

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
        self.open_btn.setIcon(QtGui.QIcon('../paper-scraper/open.png'))
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
        self.gridLayout.addWidget(self.start_btn, 5, 0, 1, 5)
        self.gridLayout.setAlignment(self.start_btn, QtCore.Qt.AlignHCenter)
        self.start_btn.clicked.connect(self.start_scraping)

        self.progress_label_kr = QtWidgets.QLabel(self.centralwidget)
        self.progress_label_kr.setObjectName('progress_label_kr')
        self.gridLayout.addWidget(self.progress_label_kr, 6, 0)
        self.progress_label_kr.hide()

        self.progress_bar_kr = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar_kr.setObjectName('progress_bar_kr')
        self.progress_bar_kr.setMinimum(0)
        self.progress_bar_kr.setMaximum(100)
        self.gridLayout.addWidget(self.progress_bar_kr, 6, 1, 1, 4)
        self.progress_bar_kr.hide()

        self.error_label_kr = QtWidgets.QLabel(self.centralwidget)
        self.error_label_kr.setObjectName('error_label_kr')
        self.gridLayout.addWidget(self.error_label_kr, 7, 0, 1, 4)
        self.error_label_kr.hide()

        self.progress_label_pr = QtWidgets.QLabel(self.centralwidget)
        self.progress_label_pr.setObjectName('progress_label_pr')
        self.gridLayout.addWidget(self.progress_label_pr, 8, 0)
        self.progress_label_pr.hide()

        self.progress_bar_pr = QtWidgets.QProgressBar(self.centralwidget)
        self.progress_bar_pr.setObjectName('progress_bar_pr')
        self.progress_bar_pr.setMinimum(0)
        self.progress_bar_pr.setMaximum(100)
        self.gridLayout.addWidget(self.progress_bar_pr, 8, 1, 1, 4)
        self.progress_bar_pr.hide()

        self.error_label_kr = QtWidgets.QLabel(self.centralwidget)
        self.error_label_kr.setObjectName('error_label_kr')
        self.gridLayout.addWidget(self.error_label_kr, 9, 0, 1, 4)
        self.error_label_kr.hide()

        self.error_label_pr = QtWidgets.QLabel(self.centralwidget)
        self.error_label_pr.setObjectName('error_label_pr')
        self.gridLayout.addWidget(self.error_label_pr, 10, 0, 1, 4)
        self.error_label_pr.hide()

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.main_height = MainWindow.height()
        self.main_width = MainWindow.width()
        self.mainwindow = MainWindow

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Newspaper Scraper"))
        self.start_btn.setText(_translate("MainWindow", "Start scraping"))
        self.start_btn.setStyleSheet('font-size: 12pt')

        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\"font-size:12pt;\">Select the "
                                                    "newspaper you want to scrape:</span></p></body></html>"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\"font-size:12pt;\">Do you "
                                                      "want an email to be sent?</span></p></body></html>"))
        self.progress_label_kr.setStyleSheet('font-size: 12pt')
        self.progress_label_pr.setStyleSheet('font-size: 12pt')

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

    def start_kr_thread(self):

        self.kr_thread = DownloadKaravali(self.directory_le.text(), self.add_email_te.toPlainText())
        self.kr_thread.start_signal_kr.connect(self.show_bar_label_kr)
        self.kr_thread.percentage_signal_kr.connect(self.update_progress_bar_kr)
        self.kr_thread.page_no_signal_kr.connect(self.update_progress_label_kr)
        self.kr_thread.pdf_progress_signal_kr.connect(self.update_progress_label_kr)
        self.kr_thread.done_signal_kr.connect(self.hide_bar_label_kr)
        self.kr_thread.error_signal_kr.connect(self.update_error_label_kr)
        self.kr_thread.start()

    def update_error_label_kr(self, error):
        
        height = self.mainwindow.height()
        height += self.error_label_kr.height()
        self.centralwidget.setFixedSize(self.centralwidget.width(), height)
        self.mainwindow.setFixedSize(self.mainwindow.width(), height)
        self.error_label_kr.show()
        self.error_label_kr.setText(error)

    def start_pr_thread(self):

        self.pr_thread = DownloadPrajavani(self.directory_le.text(), self.add_email_te.toPlainText())
        self.pr_thread.start_signal_pr.connect(self.show_bar_label_pr)
        self.pr_thread.percentage_signal_pr.connect(self.update_progress_bar_pr)
        self.pr_thread.page_no_signal_pr.connect(self.update_progress_label_pr)
        self.pr_thread.pdf_progress_signal_pr.connect(self.update_progress_label_pr)
        self.pr_thread.done_signal_pr.connect(self.hide_bar_label_pr)
        self.pr_thread.start()

    def update_error_label_pr(self, error):
        
        height = self.mainwindow.height()
        height += self.error_label_pr.height()
        self.centralwidget.setFixedSize(self.centralwidget.width(), height)
        self.mainwindow.setFixedSize(self.mainwindow.width(), height)
        self.error_label_pr.show()
        self.error_label_pr.setText(error) 

    def start_scraping(self):

        if self.directory_le.text() == '':

            self.directory_le.setPlaceholderText('Please specify a directory')

        elif not path.isdir(self.directory_le.text()):

            QtWidgets.QMessageBox.critical(self.centralwidget, 'Error', "<html><span "
                                                                        "style=\"font-size:12pt;\">Directory does not "
                                                                        "exist</span></html>",
                                           QtWidgets.QMessageBox.Ok)
        else:

            if self.prajavani_cb.isChecked() and self.karavali_cb.isChecked():

                QtWidgets.QMessageBox.warning(self.centralwidget, 'Warning', "<html><span "
                                                                             "style=\"font-size:12pt;\">This will open "
                                                                             "a browser window (only for Prajavani). "
                                                                             "It is recommended that you don't "
                                                                             "interrupt the scraping process as it "
                                                                             "can lead to errors.</span></html>",
                                              QtWidgets.QMessageBox.Ok)
                self.start_pr_thread()
                self.start_kr_thread()

            elif self.prajavani_cb.isChecked():

                QtWidgets.QMessageBox.warning(self.centralwidget, 'Warning', "<html><span style=\"font-size:12pt"
                                                                             ";\">This will open a browser window ("
                                                                             "only for Prajavani). It is recommended "
                                                                             "that you don't interrupt the scraping "
                                                                             "process as it can lead to "
                                                                             "errors.</span></html>",
                                              QtWidgets.QMessageBox.Ok)
                self.start_pr_thread()

            elif self.karavali_cb.isChecked():

                self.start_kr_thread()

    def update_progress_bar_kr(self, val):

        self.progress_bar_kr.setValue(val)

    def update_progress_label_kr(self, page_no):

        self.progress_label_kr.setText('Downloading page ' + page_no)

    def show_bar_label_kr(self, val):

        height = self.mainwindow.height()
        if val:
            height += self.progress_bar_kr.height()
            self.centralwidget.setFixedSize(self.main_width, height)
            self.mainwindow.setFixedSize(self.mainwindow.width(), height)
            self.progress_bar_kr.show()
            self.progress_label_kr.show()

    def hide_bar_label_kr(self, val):

        if val:
            self.progress_bar_kr.hide()
            self.progress_label_kr.hide()

    def update_progress_bar_pr(self, val):

        self.progress_bar_pr.setValue(val)

    def update_progress_label_pr(self, page_no):

        self.progress_label_pr.setText('Downloading page ' + page_no + '.pdf')

    def show_bar_label_pr(self, val):

        height = self.mainwindow.height()
        if val:
            height += self.progress_bar_pr.height()
            self.centralwidget.setFixedSize(self.main_width, height)
            self.mainwindow.setFixedSize(self.mainwindow.width(), height)
            self.progress_bar_pr.show()
            self.progress_label_pr.show()

    def hide_bar_label_pr(self, val):

        if val:
            self.progress_bar_pr.hide()
            self.progress_label_pr.hide()


def main():
    app = QtWidgets.QApplication([])
    mainwindow = Ui_MainWindow()
    widget = QtWidgets.QMainWindow()
    mainwindow.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
