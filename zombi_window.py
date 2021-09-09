#!/usr/bin/python3
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import *
import sys
import re
import os

class Zombi(QLabel):
    __counter = 0
    
    def __init__(self, parent=None, pos=(0,0), map_size=0):
        super(Zombi, self).__init__(parent)
        Zombi.__counter += 1
        self.ids = Zombi.__counter
        self.x, self.y = pos
        self.map_size = map_size
        
        self.img_folder_name = 'img'
        self.img_path_folder = os.path.join(os.getcwd(), self.img_folder_name)
        self.image_path = os.path.join(self.img_path_folder, '010.png')
        self.setFixedSize(50,50)
        self.setPixmap(QPixmap(self.image_path))
        
        self.log = LogFile()
        self.name = 'Зомби'
        self.log.write_log(f'{self.name}_{self.ids} появился на ({self.x}, {self.y})')
    
    def __position_control(self):
        if self.x < 0: self.x = self.map_size + self.x
        if self.x > self.map_size - 1: self.x = self.map_size - self.x
        if self.y < 0: self.y = self.map_size + self.y
        if self.y > self.map_size - 1: self.y = self.map_size - self.y
        self.log.write_log(f'{self.name}_{self.ids} переместился на ({self.x}, {self.y})')
    
    def move(self, comand):
        self.comand = comand
        if comand == 'R': self.x += 1
        if comand == 'L': self.x -= 1
        if comand == 'D': self.y += 1
        if comand == 'U': self.y -= 1
        self.__position_control()
                    
class Creatur(QLabel):
    __counter = 0
    
    def __init__(self, parent=None, pos=(0,0), map_size=0):
        super(Creatur, self).__init__(parent)
        Creatur.__counter += 1
        self.ids = Creatur.__counter
        self.x, self.y = pos
        self.map_size = map_size
        self.img_folder_name = 'img'
        self.img_path_folder = os.path.join(os.getcwd(), self.img_folder_name)
        self.image_path = os.path.join(self.img_path_folder, '001.png')
        self.setFixedSize(50,50)
        self.setPixmap(QPixmap(self.image_path))
        
        self.log = LogFile()
        self.name = 'Существо'
        self.log.write_log(f'{self.name}_{self.ids} появилось на ({self.x}, {self.y})')
    
    def infection(self, zombi):
        self.log.write_log(f'{self.name}_{self.ids} заражено {zombi.name}_{zombi.ids} на ({self.x}, {self.y})')
        
        # Не самое лучшее решение, но в рамках поставленной задачи отражает суть зомби
        self.__class__ = Zombi
        self.ids += 1
        self.name = zombi.name
        self.setPixmap(QPixmap(zombi.image_path))
        self.move(zombi.comand)
        
class NullPole(QLabel):
    def __init__(self, parent=None):
        super(NullPole, self).__init__(parent)
        self.img_folder_name = 'img'
        self.img_path_folder = os.path.join(os.getcwd(), self.img_folder_name)
        self.image_path = os.path.join(self.img_path_folder, '000.png')
        self.setFixedSize(50,50)
        self.setPixmap(QPixmap(self.image_path))
        
class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle('Зомби-заражения')
        
        # Список флагов проверки валидности введенных пользователем данных
        self.closed_flags = []
        
        # Меню создания симуляции
        self.grid_layout = QGridLayout(self)
        self.label_1 = QLabel('Размер мира:')
        self.label_2 = QLabel('Исходное положение зомби:')
        self.label_3 = QLabel('Исходные позиции существ:')
        self.label_4 = QLabel('Команда движения зомби:')
        self.line_edit_1 = QLineEdit()
        self.line_edit_1.setPlaceholderText('Целое от 2 до 20')
        self.line_edit_2 = QLineEdit()
        self.line_edit_2.setPlaceholderText('(n,n)')
        self.line_edit_3 = QLineEdit()
        self.line_edit_3.setPlaceholderText('(n,n) (m,m) ..')
        self.line_edit_4 = QLineEdit()
        self.line_edit_4.setPlaceholderText('RLDU')
        self.build_simul_button = QPushButton('Создать симуляцию')

        self.grid_layout.addWidget(self.label_1, 0,0)
        self.grid_layout.addWidget(self.line_edit_1, 0,1)
        self.grid_layout.addWidget(self.label_2, 1,0)
        self.grid_layout.addWidget(self.line_edit_2, 1,1)
        self.grid_layout.addWidget(self.label_3, 2,0)
        self.grid_layout.addWidget(self.line_edit_3, 2,1)
        self.grid_layout.addWidget(self.label_4, 3,0)
        self.grid_layout.addWidget(self.line_edit_4, 3,1)
        self.grid_layout.addWidget(self.build_simul_button, 4,0,1,2)
        
        # Обработка кнопки
        self.build_simul_button.pressed.connect(self.collect_options)
    
    def collect_options(self):
        # Проверка валидности размера мира
        self.map_size = self.line_edit_1.text()
        if bool(re.search( r'\D', self.map_size)) or (self.map_size == ''): 
            self.closed_flags.append(False)
            self.line_edit_1.setText('')
        else:
            self.map_size = int(self.map_size)
            if (self.map_size < 2) or (self.map_size > 20):
                self.closed_flags.append(False)
                self.line_edit_1.setText('')
            else:
                self.closed_flags.append(True)
                
                # Проверка валидности позиции зомби
                self.zombi_pos = self.line_edit_2.text()
                self.zombi_pos = re.findall(r'\(\d+\,\d+\)', self.zombi_pos)
                if len(self.zombi_pos) != 1:
                    self.closed_flags.append(False)
                    self.line_edit_2.setText('')
                else:
                    self.zombi_pos = eval(self.zombi_pos[0])
                    if all(i >= self.map_size for i in self.zombi_pos):
                        self.closed_flags.append(False)
                        self.line_edit_2.setText('')
                    else:
                        self.closed_flags.append(True)
                     
                # Проверка валидности позиции существ
                self.creaturs_pos = self.line_edit_3.text()
                self.creaturs_pos = re.findall(r'\(\d+\,\d+\)', self.creaturs_pos)
                if len(self.creaturs_pos) < 1:
                    self.closed_flags.append(False)
                    self.line_edit_3.setText('')
                else:
                    self.creaturs_pos = [eval(i) for i in self.creaturs_pos]
                    if all(all(j >= self.map_size for j in i) for i in self.creaturs_pos):
                        self.closed_flags.append(False)
                        self.line_edit_3.setText('')
                    else:
                        self.closed_flags.append(True)
                
                # Проверка валидности команды на движение зомби
                self.zombi_move_comands = self.line_edit_4.text()
                if bool(re.search(r'[^RLDU]', self.zombi_move_comands )):
                    self.closed_flags.append(False)
                    self.line_edit_4.setText('')
                else:
                    self.closed_flags.append(True)
                    
        # Если все верно, то отображаем окно симуляции
        if all(self.closed_flags):
            self.simul_options = (self.map_size, self.zombi_pos, self.creaturs_pos, self.zombi_move_comands)
            self.simul_window = SubWindowSimulate(None, self.simul_options)
            self.simul_window.show()
            
            
class SubWindowSimulate(QScrollArea):
    def __init__(self, parent=None, simul_options=()):
        super(SubWindowSimulate, self).__init__(parent)
        self.log = LogFile()
        self.setWindowTitle('Cимуляция')
        self.widget = QWidget()
        self.nex_button = QPushButton('Следующий ход')
        self.simul_options = simul_options
        self.simul_grid_layout = QGridLayout(self.widget)
        self.simul_grid_layout.setVerticalSpacing(0)
        self.simul_grid_layout.setHorizontalSpacing(0)
        if len(self.simul_options) != 0:
            # Создаем мир
            self.map_size = self.simul_options[0]
            for i in range(self.map_size):
                for j in range(self.map_size):
                    self.simul_grid_layout.addWidget(NullPole(self.widget), i,j)
                    
            # Создаем зомби
            self.zombi = Zombi(self.widget, self.simul_options[1], self.map_size)
            self.simul_grid_layout.addWidget(self.zombi, self.zombi.y, self.zombi.x)
            
            # Создаем существ
            self.creaturs = []
            for i in self.simul_options[2]:
                creatur = Creatur(self.widget, i, self.map_size)
                self.creaturs.append(creatur)
                self.simul_grid_layout.addWidget(creatur, creatur.y, creatur.x)
                
            # Создаем генератор команд
            self.comands_gen = (i for i in self.simul_options[3])
            
            self.simul_grid_layout.addWidget(self.nex_button, self.map_size, 0, 1, self.map_size)
        
        self.setWidget(self.widget)
        
        self.nex_button.pressed.connect(self.paint_move)
            
    def paint_move(self):
        try:
            comand = next(self.comands_gen)
            self.simul_grid_layout.addWidget(NullPole(self.widget), self.zombi.y, self.zombi.x)
            self.zombi.move(comand)
            self.simul_grid_layout.addWidget(self.zombi, self.zombi.y, self.zombi.x)
            for i in range(len(self.simul_options[2])):
                if (self.zombi.x, self.zombi.y) == self.simul_options[2][i]:
                    self.creaturs[i].infection(self.zombi)
                    for cr in self.creaturs:
                        self.simul_grid_layout.addWidget(cr, cr.y, cr.x)
        except:
            self.nex_button.setEnabled(False)
            self.log.write_log('Симуляция завершена') 
            zombi_coords = []
            creat_coords = []
            for i in self.creaturs + [self.zombi]:
                if i.name == 'Зомби':
                    zombi_coords.append((i.x, i.y))
                else:
                    creat_coords.append((i.x, i.y))
            self.log.write_log(f'Позиции зомби:{zombi_coords}')
            self.log.write_log(f'Позиции существ:{creat_coords}')  
            
            
class LogFile(object):
    def __init__(self):
        self.file_name = 'log.txt'
        self.file_path = os.path.join(os.getcwd(), self.file_name)
        self.encoding = 'utf-8'
        if not os.path.isfile(self.file_path):
            with open(self.file_path, 'w', encoding=self.encoding) as f:
                pass
    
    def write_log(self, log_message):
        log_lines = f'[{str(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))}] {log_message}\n'
        print(log_lines, end='')
        with open(self.file_path, 'a+', encoding=self.encoding) as f:
            f.write(log_lines)

                        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    ex.setFixedSize(ex.size())
    sys.exit(app.exec_())