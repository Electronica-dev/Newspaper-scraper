
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QApplication, QTextEdit, QPushButton, QSizePolicy, \
    QGridLayout, QHBoxLayout
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt
import sys
import re


class TextEditNew(QTextEdit):

    def __init__(self):

        super().__init__()

        self.setFont(QFont('Calibri', 13))
        self.setFixedSize(200, 300)


class Tablet(QMainWindow):

    def __init__(self):

        super().__init__()
        self.init_ui()

        self.pattern = re.compile(r', +| +,|,| +and +')

    def init_ui(self):

        self.setFont(QFont('Lucida Bright', 12))
        self.setFixedSize(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.widget = QWidget()

        self.setCentralWidget(self.widget)

        self.add_item_button = QPushButton()
        self.add_item_button.setIcon(QIcon(r'add.png'))
        self.add_item_button.setIconSize(QSize(32, 32))
        self.add_item_button.clicked.connect(self.add_item)

        self.find_elements = QPushButton()
        self.find_elements.setText('Find common\nelements')
        self.find_elements.setStyleSheet('padding: 4px; font-family: Lucida Bright; font: 14px')
        self.find_elements.clicked.connect(self.get_common_elements)

        self.delete_button = QPushButton()
        self.delete_button.setIcon(QIcon(r'delete.png'))
        self.delete_button.setIconSize(QSize(32, 32))
        self.delete_button.hide()
        self.delete_button.clicked.connect(self.close_item)

        label1 = QLabel('Elements of dataset 1: ')
        label2 = QLabel('Elements of dataset 2: ')
        self.common_elements_label = QLabel('Common elements: ')
        self.common_elements_label.hide()
        self.common_elements = QLabel()
        self.common_elements.hide()
        self.remove_comma_list = []

        self.te = TextEditNew()
        self.te1 = TextEditNew()

        self.grid_layout = QGridLayout()

        self.h_layout = QHBoxLayout()
        self.btn_close_layout = QHBoxLayout()

        self.h_layout.addWidget(self.add_item_button)
        self.h_layout.addWidget(self.find_elements)
        self.h_layout.addStretch()
        self.btn_close_layout.addWidget(self.delete_button)

        layout_elements = ['', '',
                           label1, label2,
                           self.te, self.te1,
                           self.common_elements_label, self.common_elements]

        positions = [(i, j) for i in range(4) for j in range(2)]

        for layout_element, position in zip(layout_elements, positions):
            if layout_element == '':
                continue
            self.grid_layout.addWidget(layout_element, *position)

        self.grid_layout.addLayout(self.h_layout, 0, 0)
        self.grid_layout.addLayout(self.btn_close_layout, 0, 1, alignment=Qt.AlignCenter)

        self.centralWidget().setLayout(self.grid_layout)

        self.index = self.grid_layout.count()
        self.const_index = self.grid_layout.count()

        self.move(200, 100)
        self.setWindowTitle('Common elements')
        self.show()

    def add_item(self):

        self.delete_button.show()

        column_no = len(self.widget.findChildren(QLabel)) - 1

        self.label_x = QLabel(f'Elements of dataset {column_no}: ')
        self.TE = TextEditNew()

        self.grid_layout.addWidget(self.label_x, 1, column_no)
        self.grid_layout.addWidget(self.TE, 2, column_no)

        if column_no == 5:
            self.add_item_button.setEnabled(False)

    def get_common_elements(self):

        self.common_elements_label.show()
        self.common_elements.show()
        arr = []
        text_edit_list = self.widget.findChildren(QTextEdit)

        for i in range(len(text_edit_list)):
            text = text_edit_list[i].toPlainText()
            element = self.pattern.split(text)
            arr.append(element)

        result = set(arr[0])

        for current_set in arr[1:]:
            result.intersection_update(current_set)

        if result == {''}:
            self.common_elements.setText('No common elements')
        else:
            result_sorted = sorted(result)
            self.common_elements.setText(str(', '.join(result_sorted)))

        result.clear()
        arr.clear()

    def close_item(self):

        self.add_item_button.setEnabled(True)

        latest_te_widget = self.widget.findChildren(QTextEdit)
        latest_label_widget = self.widget.findChildren(QLabel)

        self.grid_layout.removeWidget(latest_te_widget[-1])
        latest_te_widget[-1].deleteLater()
        self.grid_layout.removeWidget(latest_label_widget[-1])
        latest_label_widget[-1].deleteLater()

        self.widget.adjustSize()
        self.adjustSize()

        if len(latest_te_widget) == 3:
            self.delete_button.hide()


def main():
    app = QApplication([])
    t = Tablet()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
