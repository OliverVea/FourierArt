from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtWidgets import QFileDialog

import numpy as np
import time

# No operation function
def Nop(*args, **kwargs):
    pass

# Lambda no operation function
Lop = lambda *args, **kwargs: None 

def db_to_lin(db):
    return pow(10, (db / 20))

def lin_to_db(lin):
    return 20 * np.log10(lin)

def to_float(f: float):
    try:
        return float(f)
    except:
        return None
    
def get_file_name():
    return QFileDialog.getOpenFileName(None, 'Single File', QDir.rootPath() , '*.wav')[0]

def slice_array(arr, start, end):
    n = len(arr)
    start, end = int(start*n), int(end*n)

    return arr[start:end]

def time_func(func, *args, print_format_func = None, **kwargs):
    a = time.time()

    ret = func(*args, **kwargs)

    t = time.time() - a

    if not print_format_func:
        print_format_func = lambda t: f'{func.__name__} -> {t}s'
    
    print(print_format_func(t))

    return ret