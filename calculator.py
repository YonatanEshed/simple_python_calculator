import sys
import math
import threading

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtGui import QFont
from PyQt5.QtGui import QResizeEvent


class CalculatorWin(QWidget):
	def __init__(self):
		super().__init__()
		loadUi("calculator.ui", self)
		
		self.calc_str = ''
		
		# line edit resize event
		self.calc_line.resizeEvent = self.resizeEvent
		
		# numbers and dot buttons
		self.zero_button.clicked.connect(lambda: self.add_to_calc('0'))
		self.one_button.clicked.connect(lambda: self.add_to_calc('1'))
		self.two_button.clicked.connect(lambda: self.add_to_calc('2'))
		self.three_button.clicked.connect(lambda: self.add_to_calc('3'))
		self.four_button.clicked.connect(lambda: self.add_to_calc('4'))
		self.five_button.clicked.connect(lambda: self.add_to_calc('5'))
		self.six_button.clicked.connect(lambda: self.add_to_calc('6'))
		self.seven_button.clicked.connect(lambda: self.add_to_calc('7'))
		self.eight_button.clicked.connect(lambda: self.add_to_calc('8'))
		self.nine_button.clicked.connect(lambda: self.add_to_calc('9'))
		self.dot_button.clicked.connect(lambda: self.add_to_calc('.'))
		
		# operation button
		self.div_button.clicked.connect(lambda: self.add_to_calc('/'))
		self.mult_button.clicked.connect(lambda: self.add_to_calc('*'))
		self.subt_button.clicked.connect(lambda: self.add_to_calc('-'))
		self.add_button.clicked.connect(lambda: self.add_to_calc('+'))
		
		# delete, clear and equal buttons
		self.delete_button.clicked.connect(self.remove)
		self.clear_button.clicked.connect(self.clear)
		self.equal_button.clicked.connect(self.set_answer)
		
		# square root and square buttons
		self.sqrt_button.clicked.connect(self.square_root)
		self.sqr_button.clicked.connect(lambda: self.add_to_calc('**2'))
	
	def set_calc_line(self) -> None:
		self.calc_line.setText(self.calc_str.replace(' ', '')
								.replace('**2', '²')
								.replace('/', '÷')
								.replace('*', '×')
								.replace('-', '−')
								.replace('math.sqrt(', '√('))
	
	def add_to_calc(self, inpt: str) -> None:
		if not len(self.calc_str.replace(' ', '')
								.replace('**2', '²')
								.replace('/', '÷')
								.replace('*', '×')
								.replace('-', '−')
								.replace('math.sqrt(', '√(')) >= 11:
			
			self.calc_str += ' ' + inpt + ' '
			self.set_calc_line()
	
	def square_root(self):
		calc_str_split = self.calc_str.split(' ')
		last_digit_of_num = ''
		
		# check if last number is a digit
		if not calc_str_split[-1].isdigit():
			pass
		
		calc_str_split = [value for value in calc_str_split if value != '']
		
		for num in calc_str_split[::-1]:
			if not (num.isdigit() or num == '.'):
				last_digit_of_num = calc_str_split[::-1].index(num)
		
		if not last_digit_of_num:
			last_digit_of_num = len(calc_str_split)
		
		calc_str_split.insert(len(calc_str_split) - last_digit_of_num, 'math.sqrt(')
		calc_str_split.insert(len(calc_str_split), ')')
		self.calc_str = ' '.join(calc_str_split)
		self.set_calc_line()
	
	def set_answer(self) -> None:
		if self.calc_str:
			calculate = threading.Thread(target=self.calculate)
			calculate.start()
	
	def remove(self) -> None:
		if self.calc_str:
			if self.calc_str[-1] == ')':
				self.calc_str = self.calc_str[:-16]
			else:
				self.calc_str = self.calc_str[:-3]
		self.set_calc_line()
	
	def clear(self) -> None:
		self.calc_str = ''
		self.set_calc_line()
	
	def calculate(self):
		try:
			self.calc_str = str(eval(self.calc_str.replace(' ', '')))
			if len(self.calc_str) > 11:
				self.calc_str = self.calc_str[:11]
			self.calc_str = '  '.join(self.calc_str)
			self.set_calc_line()
		except:
			self.calc_line.setText("ERROR")
	
	def resizeEvent(self, a0: QResizeEvent) -> None:
		self.calc_line.setFont(QFont('Segoe UI Semibold', self.rect().width() // 9))


if __name__ == '__main__':
	app = QApplication(sys.argv)
	win = CalculatorWin()
	win.show()
	
	sys.exit(app.exec_())
