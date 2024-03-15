import sys
from turtle import color
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton,QLineEdit,QLabel, QComboBox,QTableWidget,QTableWidgetItem,QGridLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import pandas as pd
from PyQt5.QtWidgets import QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore
from PyQt5.QtChart import QChart,QPieSeries,QChartView
from PyQt5 import QtChart
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("money management program")
        self.setGeometry(50, 50, 1400, 800)
        self.initUI()
        self.trans_list = []
        self.whole_btn_clicked = True
        self.incomeCatList = ['interest', 'dividend', 'salary', 'etc.']
        self.outcomeCatList = ['food', 'fashion' ,'snack', 'leisure' ,'life' 'insurance', 'self development', 'etc.']

        try:
            self.dataset = pd.read_csv('data.csv', encoding='utf-8')
            self.df = pd.DataFrame(data = self.dataset.values,columns = ['date', 'sector', 'amount', 'details', 'note'])
            self.table.setRowCount(len(self.dataset) + 1)
            for i in range(len(self.dataset)):
                self.table.setItem(i,0, QTableWidgetItem(str(self.df.iloc[i,0])))
                self.table.setItem(i,1, QTableWidgetItem(self.df.iloc[i,1]))
                self.table.setItem(i,2, QTableWidgetItem(str(self.df.iloc[i,2])))
                self.table.setItem(i,3, QTableWidgetItem(self.df.iloc[i,3]))
                self.table.setItem(i,4, QTableWidgetItem(str(self.df.iloc[i,4])))

        except pd.errors.EmptyDataError:
            self.df = pd.DataFrame(columns = ['date', 'sector', 'amount', 'details', 'note'])
            print('Empty csv file !')

    #UI 보여줌
    def initUI(self):
        
        self.table_clicked_j = False
        self.trans_date_label = QLabel('date', self)
        self.trans_date_label.setGeometry(20,25,70,40)

        self.datetime = QDate.currentDate() 
        self.date_textbox = QLineEdit(self)
        self.date_textbox.setGeometry(100,30,120,30)
        self.date_textbox.setAlignment(QtCore.Qt.AlignRight)
        self.date_textbox.setText(self.datetime.toString(Qt.ISODate))

        self.trans_amount_label = QLabel('amount', self)
        self.trans_amount_label.setGeometry(20,85,70,40)
        self.amount_textbox = QLineEdit(self)
        self.amount_textbox.setGeometry(100,90, 120,30)
        self.amount_textbox.setValidator(QIntValidator())
        self.amount_textbox.setMaxLength(10)
        self.amount_textbox.setAlignment(QtCore.Qt.AlignRight)

        self.trans_selec_label = QLabel('sector',self)
        self.trans_selec_label.setGeometry(250,25,70,40)
    
        self.btn_1 = QComboBox(self)
        self.btn_1.addItem('income')
        self.btn_1.addItem('outcome')
        
        self.btn_1.activated[str].connect(self.setCategory)
        self.btn_1.setGeometry(330, 30,170,30)
        
        self.trans_label = QLabel('details', self)
        self.trans_label.setGeometry(250,85,70,40)
        self.btn_2 = QComboBox(self)
        self.btn_2.setGeometry(330,90,170,30)
        self.btn_2.addItem('interest')
        self.btn_2.addItem('dividend')
        self.btn_2.addItem('salary')
        self.btn_2.addItem('etc.')
        
        self.note_label = QLabel('note', self)
        self.note_label.setGeometry(20,130,70,40)
        

        self.note_textbox = QLineEdit(self)
        self.note_textbox.setGeometry(100,135,400,90)
        self.note_textbox.setAlignment(QtCore.Qt.AlignTop)
        self.note_textbox.setMaxLength(25)

        self.regis_btn = QPushButton('register',self)
        self.regis_btn.setGeometry(20,245,105,30)
        self.regis_btn.clicked.connect(self.register)
    
        self.modify_btn = QPushButton('modify',self)
        self.modify_btn.setGeometry(145,245,105,30)
        self.modify_btn.clicked.connect(self.modify)

        self.delete_btn = QPushButton('delete',self)
        self.delete_btn.setGeometry(270,245,105,30)
        self.delete_btn.clicked.connect(self.delete)

        self.clear_btn = QPushButton('reset',self)
        self.clear_btn.setGeometry(395,245,105,30)
        self.clear_btn.clicked.connect(self.reset)

        self.income_check_btn = QPushButton('show income', self)
        self.income_check_btn.setGeometry(20,290,230,30)
        self.income_check_btn.clicked.connect(self.showIncomeList)

        self.expense_check_btn = QPushButton('show outcome', self)
        self.expense_check_btn.setGeometry(270,290,230,30)
        self.expense_check_btn.clicked.connect(self.showOutcomeList)

        self.whole_check_btn = QPushButton('show all', self)
        self.whole_check_btn.setGeometry(20,335,480,30)
        self.whole_check_btn.clicked.connect(self.showWhole)

        #데이터 조회

        self.check_label = QLabel('show data',self)
        self.check_label.setGeometry(540,25,100,40)
        self.check_label.setFont(QFont('Bold',10))

        self.table = QTableWidget(self)
        self.table.setRowCount(self.table.rowCount() + 1)
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['date', 'sector', 'amount', 'details', 'note'])
        self.table.setColumnWidth(0,150)
        self.table.setColumnWidth(1,120)
        self.table.setColumnWidth(2,120)
        self.table.setColumnWidth(3,180)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setGeometry(540,85,820,280)

        self.table.cellClicked.connect(self.setRowValue)

        f = Figure(figsize=(5,4))
        self.canvas = FigureCanvas(f)
        
        self.canvas.setGeometry(50,470,1400,500)

        self.widget = QWidget(self.canvas)
        self.income_chart = QPushButton("income chart", self.canvas)
        self.outcome_chart = QPushButton('outcome chart', self.canvas)
        self.compare_chart = QPushButton("comparing chart", self.canvas)
        self.income_chart.setGeometry(20,20,130,40)
        self.outcome_chart.setGeometry(20,90,130,40)
        self.compare_chart.setGeometry(20,160,130,40)
        self.income_chart.clicked.connect(self.calcIncome)
        self.outcome_chart.clicked.connect(self.calcOutcome)
        self.compare_chart.clicked.connect(self.compareInOut)

        self.in_1_txt = QLabel(self.canvas)
        self.in_1_txt.setGeometry(1050,20,200,40)

        self.in_2_txt = QLabel(self.canvas)
        self.in_2_txt.setGeometry(1050,80,200,40)

        self.in_3_txt = QLabel(self.canvas)
        self.in_3_txt.setGeometry(1050,140,200,40)

        self.in_4_txt = QLabel(self.canvas)
        self.in_4_txt.setGeometry(1050,200,200,40)

        self.in_5_txt = QLabel(self.canvas)
        self.in_5_txt.setGeometry(1050,260,200,40)

        self.in_6_txt = QLabel(self.canvas)
        self.in_6_txt.setGeometry(1050,320,200,40)

        self.in_7_txt = QLabel(self.canvas)
        self.in_7_txt.setGeometry(1050,380,200,40)

        self.in_8_txt = QLabel(self.canvas)
        self.in_8_txt.setGeometry(1050,440,200,40)

        self.layout = QGridLayout()
 
        self.widget.setLayout(self.layout)

        self.widget.setGeometry(200,0,800,500)
        self.show()   
        self.canvas.setWindowTitle("chart")
        self.canvas.show()

    # 데이터 register
    def register(self):    
        self.trans_list = []
        self.table_clicked_j = False

        if not self.whole_btn_clicked:
            QMessageBox.about(self, "Title", "press show all")

        if self.amount_textbox.text() != "" and self.date_textbox.text() != "" and self.whole_btn_clicked:
            if self.note_textbox.text() != "":
                self.trans_list = []
                self.trans_list.append(self.date_textbox.text())
                self.trans_list.append(self.btn_1.currentText())
                self.trans_list.append(self.amount_textbox.text())
                self.trans_list.append(self.btn_2.currentText())
                self.trans_list.append(self.note_textbox.text())
                self.table.setItem(self.table.rowCount() - 1,0, QTableWidgetItem(self.date_textbox.text()))
                self.table.setItem(self.table.rowCount() - 1,1, QTableWidgetItem(self.btn_1.currentText()))
                self.table.setItem(self.table.rowCount() - 1,2, QTableWidgetItem(self.amount_textbox.text()))
                self.table.setItem(self.table.rowCount() - 1,3, QTableWidgetItem(self.btn_2.currentText()))
                self.table.setItem(self.table.rowCount() - 1,4, QTableWidgetItem(self.note_textbox.text()))
            else:
                self.trans_list = []
                self.trans_list.append(self.date_textbox.text())
                self.trans_list.append(self.btn_1.currentText())
                self.trans_list.append(self.amount_textbox.text())
                self.trans_list.append(self.btn_2.currentText())
                self.trans_list.append("none")
                self.table.setItem(self.table.rowCount() - 1,0, QTableWidgetItem(self.date_textbox.text()))
                self.table.setItem(self.table.rowCount() - 1,1, QTableWidgetItem(self.btn_1.currentText()))
                self.table.setItem(self.table.rowCount() - 1,2, QTableWidgetItem(self.amount_textbox.text()))
                self.table.setItem(self.table.rowCount() - 1,3, QTableWidgetItem(self.btn_2.currentText()))
                self.table.setItem(self.table.rowCount() - 1,4, QTableWidgetItem(self.note_textbox.text()))
        if len(self.trans_list) == 5:   #모든 데이터 필드가 채워졌는지 확인 
           
            try:
                self.dataset = pd.read_csv('data.csv')
                self.dataset.loc[self.table.rowCount() - 1] = self.trans_list
                self.dataset.to_csv('data.csv', index=False,header = ['date', 'sector', 'amount', 'details', 'note'],encoding='utf_8_sig')
            except pd.errors.EmptyDataError:
                self.df.loc[self.table.rowCount() - 1] = self.trans_list
                self.df.to_csv('data.csv', index=False,header = ['date', 'sector', 'amount', 'details', 'note'],encoding='utf_8_sig')
                print('Empty csv file!')

            self.trans_list = []
            self.date_textbox.setText(self.datetime.toString(Qt.ISODate))
            self.btn_1.setCurrentText("income")
            self.btn_2.clear()
            self.btn_2.addItem(self.incomeCatList[0])
            self.btn_2.addItem(self.incomeCatList[1])
            self.btn_2.addItem(self.incomeCatList[2])
            self.btn_2.addItem(self.incomeCatList[3])
            self.amount_textbox.setText("")
            self.note_textbox.setText("")
            self.table.setRowCount(self.table.rowCount() + 1)

    # 거래 항목에 따른 상세내역 변경
    def setCategory(self,text):
        self.trans_amount_label.setText(text + ' amount')
        if text == 'income':
            self.btn_2.clear()
            for cat in self.incomeCatList:
                self.btn_2.addItem(cat)

        elif text == 'outcome':
            self.btn_2.clear()
            for cat in self.outcomeCatList:
                self.btn_2.addItem(cat)
        else: 
            self.btn_2.clear()
            self.btn_2.addItem('transactions')
    
    # 테이블에서 클릭된 줄에 따른 fields' value setting
    def setRowValue(self):
        if not self.whole_btn_clicked:
            QMessageBox.about(self, "Title", "press show all")
        
        if self.table.currentRow() < self.table.rowCount() - 1 and self.whole_btn_clicked:
            self.table_clicked_j = True
            self.date_textbox.setText(self.table.item(self.table.currentRow(), 0).text())      #############################
            self.btn_1.setCurrentText(self.table.item(self.table.currentRow(), 1).text())
            self.amount_textbox.setText(self.table.item(self.table.currentRow(), 2).text())
            self.btn_2.clear()
            if self.table.item(self.table.currentRow(), 1).text() == 'income':
                self.btn_2.addItem(self.table.item(self.table.currentRow(), 3).text())
                for cat in self.incomeCatList:
                    if cat != self.table.item(self.table.currentRow(), 3).text():
                        self.btn_2.addItem(cat)

            else:
                self.btn_2.addItem(self.table.item(self.table.currentRow(), 3).text())
                for cat in self.outcomeCatList:
                    if cat != self.table.item(self.table.currentRow(), 3).text():
                        self.btn_2.addItem(cat)
               
            self.note_textbox.setText(self.table.item(self.table.currentRow(), 4).text())

    # 데이터 modify
    def modify(self):   
        
        if not self.whole_btn_clicked:
            QMessageBox.about(self, "Title", "press show all")

        if self.table_clicked_j and self.whole_btn_clicked:
           
            self.table.setItem(self.table.currentRow(),0, QTableWidgetItem(self.date_textbox.text()))    ###################
            self.table.setItem(self.table.currentRow(),1, QTableWidgetItem(self.btn_1.currentText()))
            self.table.setItem(self.table.currentRow(),2, QTableWidgetItem(self.amount_textbox.text()))
            self.table.setItem(self.table.currentRow(),3, QTableWidgetItem(self.btn_2.currentText()))
            self.table.setItem(self.table.currentRow(),4, QTableWidgetItem(self.note_textbox.text())) 
            
            try:
                self.dataset = pd.read_csv('data.csv')
                self.dataset.loc[self.table.currentRow(), :] = [self.date_textbox.text(),self.btn_1.currentText(),self.amount_textbox.text(),self.btn_2.currentText(),self.note_textbox.text()]
                self.dataset.to_csv('data.csv', index=False,header = ['date', 'sector', 'amount', 'details', 'note'],encoding='utf_8_sig')
            except pd.errors.EmptyDataError:
                self.df.loc[self.table.currentRow(), :] = [self.date_textbox.text(),self.btn_1.currentText(),self.amount_textbox.text(),self.btn_2.currentText(),self.note_textbox.text()]
                self.df.to_csv('data.csv', index=False,header = ['date', 'sector', 'amount', 'details', 'note'],encoding='utf_8_sig')
                print('Empty csv file!')

            self.date_textbox.setText(self.datetime.toString(Qt.ISODate)) ##############################
            self.btn_1.setCurrentText("income")
            self.btn_2.clear()
            self.btn_2.addItem('interest')
            self.btn_2.addItem('dividend')
            self.btn_2.addItem('salary')
            self.btn_2.addItem('etc.')
            self.amount_textbox.setText("")
            self.note_textbox.setText("")
            
    # 데이터 delete
    def delete(self):   
        if not self.whole_btn_clicked:
            QMessageBox.about(self, "Title", "press show all")
        
        if self.table_clicked_j and self.whole_btn_clicked:

            try:
                self.dataset = pd.read_csv('data.csv')
                self.dataset.loc[self.table.currentRow(), :] = ["0", "0", "0", "0", "0"]
                self.dataset.to_csv('data.csv', index=False,header = ['date', 'sector', 'amount', 'details', 'note'],encoding='utf_8_sig')
            except pd.errors.EmptyDataError:
                self.df.loc[self.table.currentRow(), :] = [self.date_textbox.text(),self.btn_1.currentText(),self.amount_textbox.text(),self.btn_2.currentText(),self.note_textbox.text()]
                self.df.to_csv('data.csv', index=False,header = ["0", "0", "0", "0", "0"],encoding='utf_8_sig')
                print('Empty csv file!')
           
            self.table.setItem(self.table.currentRow(),0, QTableWidgetItem(""))  ################################
            self.table.setItem(self.table.currentRow(),1, QTableWidgetItem(""))
            self.table.setItem(self.table.currentRow(),2, QTableWidgetItem(""))
            self.table.setItem(self.table.currentRow(),3, QTableWidgetItem(""))
            self.table.setItem(self.table.currentRow(),4, QTableWidgetItem("")) 

            self.date_textbox.setText(self.datetime.toString(Qt.ISODate)) ###################################
            self.btn_1.setCurrentText("income")
            self.btn_2.clear()
            self.btn_2.addItem('interest')
            self.btn_2.addItem('dividend')
            self.btn_2.addItem('salary')
            self.btn_2.addItem('etc.')
            self.amount_textbox.setText("")
            self.note_textbox.setText("")

    # reset 버튼에 관한 코드
    def reset(self):    
        self.reset = False
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Are you sure to reset? ")
        msg.setWindowTitle("reset")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        returnValue = msg.exec()
        if returnValue == QMessageBox.Ok:
            self.reset = True
        if self.reset:
            try:
                self.dataset = pd.read_csv('data.csv')
                self.dataset.drop(self.dataset.columns[:],axis=1, inplace=True)
                self.dataset.to_csv('data.csv', index=False,header = False)
                self.table.setRowCount(1)
                self.table.setItem(0,0, QTableWidgetItem(""))
                self.table.setItem(0,1, QTableWidgetItem(""))
                self.table.setItem(0,2, QTableWidgetItem(""))
                self.table.setItem(0,3, QTableWidgetItem(""))
                self.table.setItem(0,4, QTableWidgetItem("")) 
                sys.exit(app.exec_()) 

            except pd.errors.EmptyDataError:
                print('Empty csv file!') 

    # income 내역만 조회
    def showIncomeList(self): 
        try:
            self.whole_btn_clicked = False
            self.dataset = pd.read_csv('data.csv')
            self.income = []
            for i in range(len(self.dataset)):
                if self.dataset.iloc[i,1] == "income":
                    self.income.append(self.dataset.iloc[i,:].values)
            self.table.setRowCount(len(self.income))

            for l in range(len(self.income)):
                self.table.setItem(l,0, QTableWidgetItem(str(self.income[l][0])))
                self.table.setItem(l,1, QTableWidgetItem(self.income[l][1]))
                self.table.setItem(l,2, QTableWidgetItem(str(self.income[l][2])))
                self.table.setItem(l,3, QTableWidgetItem(self.income[l][3]))
                self.table.setItem(l,4, QTableWidgetItem(str(self.income[l][4])))
            self.table.setRowCount(len(self.income) + 1)

            
        except pd.errors.EmptyDataError:
            print('Empty csv file!')
    
    # outcome 내역만 조회
    def showOutcomeList(self):
        try:
            self.whole_btn_clicked = False
            self.dataset = pd.read_csv('data.csv')
            self.out = []
            for i in range(len(self.dataset)):
                if self.dataset.iloc[i,1] == "outcome":
                    self.out.append(self.dataset.iloc[i,:].values)
            self.table.setRowCount(len(self.out))

            for l in range(len(self.out)):
                self.table.setItem(l,0, QTableWidgetItem(str(self.out[l][0])))
                self.table.setItem(l,1, QTableWidgetItem(self.out[l][1]))
                self.table.setItem(l,2, QTableWidgetItem(str(self.out[l][2])))
                self.table.setItem(l,3, QTableWidgetItem(self.out[l][3]))
                self.table.setItem(l,4, QTableWidgetItem(str(self.out[l][4])))
            self.table.setRowCount(len(self.out) + 1)
            
        except pd.errors.EmptyDataError:
            print('Empty csv file!')

    # 전체 조회       
    def showWhole(self):
        self.whole_btn_clicked = True 
        try:
            self.dataset = pd.read_csv('data.csv')
            self.whole = []
            for i in range(len(self.dataset)):
                self.whole.append(self.dataset.iloc[i,:].values)
            self.table.setRowCount(len(self.whole))

            for l in range(len(self.whole)):
                self.table.setItem(l,0, QTableWidgetItem(str(self.whole[l][0])))
                self.table.setItem(l,1, QTableWidgetItem(self.whole[l][1]))
                self.table.setItem(l,2, QTableWidgetItem(str(self.whole[l][2])))
                self.table.setItem(l,3, QTableWidgetItem(self.whole[l][3]))
                self.table.setItem(l,4, QTableWidgetItem(str(self.whole[l][4])))
            self.table.setRowCount(len(self.whole) + 1)
        except pd.errors.EmptyDataError:
            print('Empty csv file!')

    # income 계산 및 chart에 표시
    def calcIncome(self):
        try:
            self.income_list = [0,0,0,0]
            self.dataset = pd.read_csv('data.csv')
            whole = self.dataset.iloc[:,:].values
            for i in range(len(whole)):
                if whole[i][1] == 'income':
                    print(whole[i][3])
                    if whole[i][3] in self.incomeCatList:
                        k = self.incomeCatList.index(whole[i][3])
                        self.income_list[k] += int(whole[i][2])

            
            series = QPieSeries()
            for i in range(len(self.incomeCatList)):
                series.append(self.incomeCatList[i], self.income_list[i])

            series.setLabelsVisible(True)

            chart = QChart()
            chart.addSeries(series)  
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chartview = QChartView(chart)
            self.layout.addWidget(chartview, 0,0,0,0)
            self.widget.setGeometry(200,0,800,500)

            series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)
            for slice in series.slices():
                slice.setLabel("{:.2f}%".format(100 * slice.percentage()))

            for i in range(len(self.incomeCatList)):
                chart.legend().markers(series)[i].setLabel(self.incomeCatList[i])       

            self.in_1_txt.setText('whole income : ' + str(sum(self.income_list)) + 'won')
            self.in_2_txt.setText('interest : ' + str(self.income_list[0]) + 'won')
            self.in_3_txt.setText('dividend : ' + str(self.income_list[1]) + 'won')
            self.in_4_txt.setText('salary : ' + str(self.income_list[2]) + 'won')
            self.in_5_txt.setText('etc. : ' + str(self.income_list[3]) +'won')
            self.in_6_txt.setText("")
            self.in_7_txt.setText("")
            self.in_8_txt.setText("")

        except pd.errors.EmptyDataError:
            print('Empty csv file!')

    # outcome 계산 및 chart에 표시
    def calcOutcome(self):
        print("outcome")

        try:
            self.outcome_list = [0,0,0,0,0,0,0]
            self.dataset = pd.read_csv('data.csv')
            whole = self.dataset.iloc[:,:].values
            for i in range(len(whole)):
                if whole[i][1] == 'outcome':
                    if whole[i][3] in self.outcomeCatList:
                        k = self.outcomeCatList.index(whole[i][3])
                        self.outcome_list[k] += int(whole[i][2])
                        
            series = QPieSeries()
            for i in range(len(self.outcomeCatList)):
                series.append(self.outcomeCatList[i], self.outcome_list[i])
            series.setLabelsVisible(True)

            chart = QChart()
            chart.addSeries(series)  
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chartview = QChartView(chart)
            self.layout.addWidget(chartview, 0,0,0,0)
            self.widget.setGeometry(200,0,800,500)

            series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)
            for slice in series.slices():
                slice.setLabel("{:.2f}%".format(100 * slice.percentage()))

            for i in range(len(self.outcomeCatList)):
                chart.legend().markers(series)[i].setLabel(self.outcomeCatList[i]) 


            self.in_1_txt.setText('whole outcome : ' + str(sum(self.outcome_list)) + 'won')
            self.in_2_txt.setText('food : ' + str(self.outcome_list[0]) + 'won')
            self.in_3_txt.setText('fashion : ' + str(self.outcome_list[1]) + 'won')
            self.in_4_txt.setText('snack : ' + str(self.outcome_list[2]) + 'won')
            self.in_5_txt.setText('leisure life : ' + str(self.outcome_list[3]) +'won')
            self.in_6_txt.setText('insurance : ' + str(self.outcome_list[4]) + 'won')
            self.in_7_txt.setText('self development : ' + str(self.outcome_list[5]) + 'won')
            self.in_8_txt.setText('etc. : ' + str(self.outcome_list[6]) + 'won')
        
        except pd.errors.EmptyDataError:
            print('Empty csv file!')

    # income outcome 비교
    def compareInOut(self):
        print("compare")

        try:
            out_sector_list = ['food','fashion','snack','leisure life','insurance','self development','etc.']
            self.outcome_list = [0,0,0,0,0,0,0]
            self.dataset = pd.read_csv('data.csv')
            whole = self.dataset.iloc[:,:].values
            for i in range(len(whole)):
                if whole[i][1] == 'outcome':
                    if whole[i][3] in out_sector_list:
                        k = out_sector_list.index(whole[i][3])
                        self.outcome_list[k] += int(whole[i][2])
            
            in_sector_list = ['interest','dividend','salary','etc.']
            self.income_list = [0,0,0,0]
            self.dataset = pd.read_csv('data.csv')
            whole = self.dataset.iloc[:,:].values
            for i in range(len(whole)):
                if whole[i][1] == 'income':
                    print(whole[i][3])
                    if whole[i][3] in in_sector_list:
                        k = in_sector_list.index(whole[i][3])
                        #income_list[k] += income_list[i]
                        self.income_list[k] += int(whole[i][2])
            series = QPieSeries()
            series.append("whole income", sum(self.income_list))
            series.append("whole outcome", sum(self.outcome_list))
            series.setLabelsVisible(True)

            chart = QChart()
            chart.addSeries(series)  
            chart.setAnimationOptions(QChart.SeriesAnimations)
            chartview = QChartView(chart)
            self.layout.addWidget(chartview, 0,0,0,0)
            self.widget.setGeometry(200,0,800,500)

            series.setLabelsPosition(QtChart.QPieSlice.LabelInsideHorizontal)
            for slice in series.slices():
                slice.setLabel("{:.2f}%".format(100 * slice.percentage()))

            chart.legend().markers(series)[0].setLabel("whole income") 
            chart.legend().markers(series)[1].setLabel("whole outcome")
        
        except pd.errors.EmptyDataError:
            print('Empty csv file!')


        self.in_1_txt.setText('whole income : ' + str(sum(self.income_list)) + 'won')
        self.in_2_txt.setText('whole outcome : ' + str(sum(self.outcome_list)) + 'won')
        self.in_3_txt.setText("")
        self.in_4_txt.setText("")
        self.in_5_txt.setText("")
        self.in_6_txt.setText("")
        self.in_7_txt.setText("")
        self.in_8_txt.setText("")


app = QApplication(sys.argv)
main = Main()
sys.exit(app.exec_())