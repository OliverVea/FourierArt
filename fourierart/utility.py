from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QFileDialog

import numpy as np

def db_to_lin(db):
    return pow(10, (db / 20))

def get_dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)
    return palette
    
def get_file_name(caller):
    return QFileDialog.getOpenFileName(caller, 'Single File', QDir.rootPath() , '*.wav')[0]

def slice_array(arr, start, end, downsample = 1.0):
    n = len(arr)
    start, end = int(start*n), int(end*n)

    return arr[start:end]