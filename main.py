import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)

        self.db_conn = sqlite3.connect('coffee.sqlite')
        self.db_cursor = self.db_conn.cursor()

        if False:
            self.tableWidget = QTableWidget()
        self.load_data()

    def load_data(self):
        titles = ['ID', 'название сорта', 'степень обжарки', 'молотый/в зернах', 'описание вкуса', 'цена',
                  'объем упаковки']
        command = "SELECT * FROM coffe"
        data = self.db_cursor.execute(command).fetchall()
        self.tableWidget.setColumnCount(len(titles))
        self.tableWidget.setHorizontalHeaderLabels(titles)
        self.tableWidget.resizeColumnsToContents()
        self.tableWidget.setRowCount(0)
        self.tableWidget.resizeColumnsToContents()
        for row, i in enumerate(data):
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for col, j in enumerate(i):
                item = QTableWidgetItem(str(j))
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                self.tableWidget.setItem(row, col, item)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
