import sys
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QColor, QPalette, QPixmap, QLinearGradient, QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QFrame
from login import LoginWindow
from signup import SignupWindow
from mainwindow import MainWindow
import bcrypt
import sqlite3
