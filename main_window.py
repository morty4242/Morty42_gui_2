import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pickle
from PyQt5 import QtCore, QtWidgets, QtGui
from ui_main import Ui_MainWindow
from datamodels.PandasDataModel import PandasDataModel, NewPandasDataModel
from datamodels.UniversalDataModel import UniversalDataModel


class MainApp(Ui_MainWindow):
    def __init__(self, parent):
        self.setupUi(parent)
        parent.setWindowTitle('MRMC Model Manager')
        self.tableView_1.horizontalHeader().setStyleSheet("::section {""background-color: rgb(0, 143, 150);}")

        # initialize variables
        self.df = pd.read_excel('model_data_file/model_inventory.xlsx', engine='openpyxl')

        # load data
        self.load_data()

        self.tableView_1.setModel(self.data_model)
        #
        # self.data_model.layoutChanged.connect(self.tableView.resizeColumnsToContents)
        self.filter_button.clicked.connect(self.filter_on_model_type)
        self.filter_button.clicked.connect(self.update_model_box)

        self.reset_button.clicked.connect(self.reset)

        self.pushButton_14.clicked.connect(self.override)
        self.pushButton_15.clicked.connect(self.clear)

    def load_data(self):
        self.data_model = PandasDataModel(self.df)

    def filter_on_model_type(self):
        cur_model_type = self.comboBox_3.currentText()
        print(cur_model_type)

        self.new_df = self.df[self.df['Model Type'] == cur_model_type]
        print(self.new_df)

        self.override_df = self.new_df.copy()
        new_data_model = PandasDataModel(self.new_df)
        self.tableView_1.setModel(new_data_model)

    def reset(self):
        self.new_df = self.df

        self.override_df = self.new_df.copy()
        self.tableView_1.setModel(PandasDataModel(self.new_df))
        self.model_combobox.clear()

    def update_model_box(self):
        print('See new Models')
        model_list = self.new_df['Model Name'].tolist()
        print(self.new_df['Model Name'].tolist())

        self.model_combobox.clear()
        self.model_combobox.addItems(model_list)

    def override(self):
        cur_model = self.model_combobox.currentText()
        cur_group = self.rating_type_combobox.currentText()
        set_rating = self.set_rating_combobox.currentText()
        print(cur_model, cur_group, set_rating)

        index = self.override_df[self.override_df['Model Name'] == cur_model].index.tolist()
        print(index[0])
        print(self.override_df.loc[index[0], cur_group + ' Rating'])
        # print(self.override_df.ix[index, cur_group + ' Rating'])
        self.override_df.at[index[0], cur_group + ' Rating'] = set_rating
        self.tableView_1.setModel(PandasDataModel(self.override_df))

    def clear(self):
        self.override_df = self.new_df.copy()
        self.tableView_1.setModel(PandasDataModel(self.override_df))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainApp(MainWindow)
    MainWindow.show()

    sys.exit(app.exec_())
