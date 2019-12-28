import sqlite3
import sys

from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QMessageBox

main_uic = 'main.ui'
path_uic_add = "addEditCoffeeForm.ui"


class MyApp(QMainWindow):
    global main_uic

    def __init__(self):
        super().__init__()
        uic.loadUi(main_uic, self)

        self.db_conn = sqlite3.connect('coffee.sqlite')
        self.db_cursor = self.db_conn.cursor()

        if False:
            self.tableWidget = QTableWidget()
        self.btn_edit.clicked.connect(self.editData)
        self.load_data()

    def editData(self):
        self.now = AddChangeForm()
        self.now.show()
        self.close()

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


class AddChangeForm(QMainWindow):
    global path_uic_add

    def __init__(self):
        super().__init__()
        self.db_conn = sqlite3.connect('coffee.sqlite')
        self.db_cursor = self.db_conn.cursor()
        uic.loadUi(path_uic_add, self)
        self.btn_exit.clicked.connect(self.BtnExitReaction)
        self.btn_change.clicked.connect(self.change_data)
        self.btn_add.clicked.connect(self.add_data)

    def get_data(self):
        edits_list = [self.lineEdit_id, self.lineEdit_name, self.lineEdit_fry, self.lineEdit_type, self.lineEdit_desc,
                      self.lineEdit_price, self.lineEdit_volume]
        result = list()
        for edit in edits_list:
            text = edit.text()
            if len(text.replace(' ', '')):
                result.append(text)
            else:
                result.append(None)
        id = int(result[0]) if result[0] is not None and result[0].isnumeric() else None
        price = int(result[5]) if result[5] is not None and result[5].isnumeric() else None
        volume = int(result[6]) if result[6] is not None and result[6].isnumeric() else None
        return [id, *result[1:5], price, volume]

    def check_id(self, id):
        return bool(len(self.db_cursor.execute("SELECT * FROM coffe WHERE ID=?", (id,)).fetchall()))

    def add_data(self):
        data = self.get_data()[1:]
        if all(data) is False:
            msg = QMessageBox(self)
            msg.setText('Одно из полей не заполнено или заполнено не правильно')
            msg.show()
            return
        command = """INSERT INTO coffe ([Name Sort],[Frying Degree], Type, Description, Price, Volume) VALUES(?, ?, ?, ?, ?, ?)"""
        self.db_cursor.execute(command, data)
        self.db_conn.commit()

    def change_data(self):
        data = self.get_data()
        id = data.pop(0)
        if id is None:
            msg = QMessageBox(self)
            msg.setText("Не заполено поля с id или там не число")
            msg.show()
            return
        if self.check_id(id) is False:
            msg = QMessageBox(self)
            msg.setText("Такого ID нету")
            return

        asks = ['Name Sort=', 'Frying Degree=', 'Type=', 'Description=', 'Price=', 'Volume=']
        take = [i for i in range(len(data)) if data[i] is not None]
        update_ask = ' , '.join([asks[i] + '?' for i in take])
        if update_ask.__len__() == 0:
            return
        self.db_cursor.execute(f"UPDATE coffe SET {update_ask} WHERE ID=?", (*[data[i] for i in take], id))
        self.db_conn.commit()

    def BtnExitReaction(self):
        self.now = MyApp()
        self.now.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())

# db_conn = sqlite3.connect('coffee.sqlite')
# db_cursor = db_conn.cursor()
# result = db_cursor.execute("SELECT * FROM coffe WHERE ID=?", ("ID",)).fetchall()
# print(result)
