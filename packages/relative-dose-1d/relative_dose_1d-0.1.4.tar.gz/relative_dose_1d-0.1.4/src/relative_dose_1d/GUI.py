# -*- coding: utf-8 -*-
"""
Created Apr-2023

@author: Luis Alfonso Olivares Jimenez

GUI to load text data corresponding to dose profiles and PDD. 

The data should be in M ​​rows by 2 columns, corresponding to positions and
dose values, respectively.

The script has been tested with the following examples:

    * File in w2CAD format (format used by the TPS Eclipse 16.1, from the Varian(R) company).
      In the algorithm, the start of the data is identified by the words: '$STOM' or '$STOD'
      Physical unit assumed to be in mm.

    * File in mcc format (format used by Verisoft 7.1.0.199 software, from PTW(R) company).
      In the algorithm, the beginning of the data is identified by the word: 'BEGIN_DATA'
      Physical unit assumed to be in mm.

    * File in text format
      The data must be distributed in M ​​rows by 2 columns and separated
      for a blank space.
      The script ask for a word to identify the beginning of the data in the text file, 
      a number to add to the positions, and a factor for distance dimension conversion.

After two successful loaded data, gamma index and dose difference are automatically calculated.

"""

import sys
import os
import numpy as np
from PyQt6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QHBoxLayout,
                             QPushButton, QMessageBox, QFileDialog, QVBoxLayout,
                             QFormLayout, QInputDialog, QMainWindow)
from PyQt6.QtCore import Qt

from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvas

from relative_dose_1d.tools import identify_format, get_data, gamma_1D
# For testing
#from tools import identify_format, get_data, gamma_1D

class Main_Window(QWidget):

    def __init__(self):
        """Constructor for Empty Window Class"""
        super().__init__()
        self.loaded_data = []
        self.initializeUI()

    def initializeUI(self):
        """Set up the apllication"""
        "x, y, width, height"
        self.setGeometry(200,100,1000,400)
        self.setWindowTitle("Relative dose 1D")

        self.set_up()
        self.show()

    def set_up(self):
        "Layouts definition"
        self.main_box_layout = QVBoxLayout()

        self.open_and_clear_layout = QVBoxLayout()
        self.main_box_layout.addLayout(self.open_and_clear_layout)

        self.h_box_layout = QHBoxLayout()
        self.settings_layout_v = QVBoxLayout()
        self.h_box_layout.addLayout(self.settings_layout_v)
        self.main_box_layout.addLayout(self.h_box_layout)

        self.setLayout(self.main_box_layout)

        self.open_file_button = QPushButton("Load a text file", self)
        self.open_file_button.clicked.connect(self.open_file_button_clicked)

        self.clear_button = QPushButton("Clear", self)
        self.clear_button.clicked.connect(self.clear_data_and_plots)
        
        self.button_factor = QPushButton("Scale factor", self)
        self.button_factor.clicked.connect(self.factor_button_clicked)
        self.button_factor.setFixedSize(75, 40)
        self.button_factor.setEnabled(False)

        self.button_origin = QPushButton("Move origin", self)
        self.button_origin.clicked.connect(self.move_button_clicked)
        self.button_origin.setFixedSize(75, 40)
        self.button_origin.setEnabled(False)
        self.settings_layout_v.addWidget(self.button_factor)
        self.settings_layout_v.addWidget(self.button_origin)
        self.settings_layout_v.addStretch()
        self.Q_grafica = Q_Graphic_Block() 
        self.h_box_layout.addWidget(self.Q_grafica.Qt_fig)
         
        self.open_and_clear_layout.addWidget(self.open_file_button)
        self.open_and_clear_layout.addWidget(self.clear_button)
        

    # Button's functions

    def open_file_button_clicked(self):
        self.last_file_name, _ = QFileDialog.getOpenFileName()
        _ , extension = os.path.splitext(self.last_file_name)

        if self.last_file_name:
            with open(self.last_file_name, encoding='UTF-8', mode = 'r') as file:
                all_list = [line.strip() for line in file]

            format = identify_format(all_list)

            if format == 'text_file':
                self.show_new_window()  #New window for input user parameters.

            else:
                data = get_data(self.last_file_name)
                self.load_data(data)


    def clear_data_and_plots(self):
        self.Q_grafica.ax_perfil.clear()
        self.Q_grafica.ax_perfil_resta.clear()
        self.Q_grafica.ax_gamma.clear()
        self.Q_grafica.fig.canvas.draw()
        self.open_file_button.setEnabled(True)
        self.loaded_data = []

    def factor_button_clicked(self):
        scale_factor, ok = QInputDialog.getText(self, 'Scale factor', 'Scale factor:')
        try:
            scale_factor = float(scale_factor)
            if ok:
                self.loaded_data[-1][:,0] = self.loaded_data[-1][:,0] * scale_factor
                cache_data = self.loaded_data
                self.clear_data_and_plots()

                for data in cache_data:
                    self.load_data(data)

        except ValueError:
            QMessageBox().critical(self, "Error", "Enter a number.")
            print('Error, give a number.')

    def move_button_clicked(self):
        delta, ok = QInputDialog.getText(self, 'Scale factor', 'Origin displacement:')
        try:
            delta = float(delta)
            if ok:
                self.loaded_data[-1][:,0] = self.loaded_data[-1][:,0] + delta
                cache_data = self.loaded_data
                self.clear_data_and_plots()

                for data in cache_data:
                    self.load_data(data)

        except ValueError:
            QMessageBox().critical(self, "Error", "Enter a number.")
            print('Error, give a number.')        

    def show_new_window(self):
        start_word, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Start word:')
        if ok:
            data = get_data(self.last_file_name, start_word)
        else:
            data = get_data(self.last_file_name)
                
        self.load_data(data)
    
    #   Additional functions

    def load_data(self, data):
        
        self.loaded_data.append(data)       
        self.Q_grafica.plot_data(data)
        self.button_factor.setEnabled(True)
        self.button_origin.setEnabled(True)
        if len(self.loaded_data) == 2:
            self.calc_difference_and_gamma()

    def calc_difference_and_gamma(self):

        data_A = self.loaded_data[0]
        data_B = self.loaded_data[1]

        # Using interpolation, new values ​​of B are computed at positions given by A.
        data_B_from_A_positions = np.interp(data_A[:,0], data_B[:,0], data_B[:,1], left = np.nan)
    
        difference = data_A[:,1] - data_B_from_A_positions

        added_positions = np.array((data_A[:,0], difference))
        values = np.transpose(added_positions)
       
        g, g_percent = gamma_1D(data_A, data_B)

        self.Q_grafica.plot_resta(values)
        self.Q_grafica.plot_gamma(g)
        print(g_percent)

    
class Q_Graphic_Block:
        
    def __init__(self):
        self.fig = Figure(figsize=(4,3), tight_layout = True, facecolor = 'whitesmoke')
        self.Qt_fig = FigureCanvas(self.fig)

        #   Axes para la imagen
        self.ax_perfil = self.fig.add_subplot(1, 2, 1)
        #self.ax_perfil.set_title('Pro')
        self.ax_perfil.set_ylabel('Percentage [%]')
        self.ax_perfil.set_xlabel('Distance')
        self.ax_perfil.grid(alpha = 0.3)

        self.ax_perfil_resta =  self.fig.add_subplot(1, 2, 2)
        #self.ax_perfil_resta.set_title('Resta')
        self.ax_perfil_resta.set_ylabel('Percentage [%]')
        self.ax_perfil_resta.set_xlabel('Distance')
        self.ax_perfil_resta.grid(alpha = 0.3)

        self.ax_gamma = self.ax_perfil_resta.twinx()
        self.ax_gamma.set_ylabel('gamma')
        #self.ax_gamma.set_ylim((0, 2))
        
    def plot_data(self, data):
        x = data[:,0]
        y = data[:,1]
        self.ax_perfil.plot(x, y)
        self.ax_perfil.set_ylabel('Percentage [%]')
        self.ax_perfil.set_xlabel('Distance')
        self.ax_perfil.grid(alpha = 0.3)
        self.fig.canvas.draw()
        
    def plot_resta(self, data):
        x = data[:,0]
        y = data[:,1]
        self.ax_perfil_resta.plot(x, y, color='r', label = 'Diferencia', alpha = 0.6)
        self.ax_perfil_resta.set_ylabel('Diferencia')
        self.ax_perfil_resta.set_xlabel('Distancia [mm]')
        self.ax_perfil_resta.grid(alpha = 0.3)
        self.ax_perfil_resta.legend(loc = 'upper left')

        self.fig.canvas.draw()

    def plot_gamma(self, data):
        x = data[:,0]
        y = data[:,1]

        self.ax_gamma.plot(x, y, color='g', label = 'gamma', marker = '.')
        self.ax_gamma.set_ylabel('gamma')
        self.ax_gamma.legend(loc = 'upper right')

        self.fig.canvas.draw()        

        
app = QApplication(sys.argv)
window = Main_Window()
sys.exit(app.exec())

