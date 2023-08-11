import sqlite3
from dashboard import ChatHeaderWidget
from imports import *
import time
# from cryptography.fernet import Fernet
from cryptography.fernet import Fernet, InvalidToken
import base64
# import cipher_suite
from encryption import EncryptionManager
from contact_functions import ContactFunctions

from database import add_contact, get_contacts, update_chat_history

from PyQt5.QtCore import pyqtSignal
from socketio import Client
from flask_socketio import Namespace
from chat_functions import ChatFunctions


class MainWindow(QMainWindow, ChatFunctions, ContactFunctions):
    update_gui_signal = pyqtSignal(str)
    def __init__(self, username):
        super().__init__()

        self.update_gui_signal.connect(self.update_gui)
        # Set the window title
        self.setWindowTitle("WhatsApp Lite")

        # Set the fixed window size
        self.setFixedSize(800, 600)
        
        # Custom background gradient
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#4CAF50"))
        gradient.setColorAt(1, QColor("#202020"))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # Set the central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create the main layout
        self.main_layout = QHBoxLayout(self.central_widget)

        # Create the left panel layout
        self.left_panel_layout = QVBoxLayout()
        self.left_panel_layout.setAlignment(Qt.AlignTop)
        self.main_layout.addLayout(self.left_panel_layout)

        # Add the WhatsApp logo and title to the left panel
        logo_title_layout = QHBoxLayout()
        whatsapp_logo_label = QLabel()
        whatsapp_logo_pixmap = QPixmap("D:\Shiril\cw\cw_2\WhatsApp.png")
        whatsapp_logo_label.setPixmap(
            whatsapp_logo_pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio)
        )
        logo_title_layout.addWidget(whatsapp_logo_label)

        whatsapp_title_label = QLabel("WhatsApp Lite")
        whatsapp_title_label.setStyleSheet("font-size: 25px; color: white;")
        logo_title_layout.addWidget(whatsapp_title_label, alignment=Qt.AlignRight)

        self.left_panel_layout.addLayout(logo_title_layout)

        # Add a line separator
        line_separator = QFrame()
        line_separator.setFrameShape(QFrame.HLine)
        line_separator.setFrameShadow(QFrame.Sunken)
        self.left_panel_layout.addWidget(line_separator)

        # Create the contact list widget
        self.contact_list_widget = QListWidget()
        self.contact_list_widget.setStyleSheet("""
            QListWidget {
                background-color: #2C4029;
                border: none;
                color: white;
                font-size: 20px;
            }

            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }
        """)

        self.left_panel_layout.addWidget(self.contact_list_widget)

        # Create the "Add Contact" button widget
        add_contact_button = QPushButton("Add Contact")
        add_contact_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)
        add_contact_button.clicked.connect(self.add_contact)
        self.left_panel_layout.addWidget(add_contact_button, alignment=Qt.AlignBottom)

        # Create the "Delete Contact" button widget
        delete_contact_button = QPushButton("Delete Contact")
        delete_contact_button.setStyleSheet("""
            QPushButton {
                background-color: #FF0000;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #e20000;
            }
        """)
        delete_contact_button.clicked.connect(self.delete_contact)
        self.left_panel_layout.addWidget(delete_contact_button, alignment=Qt.AlignBottom)

        # Create the right panel layout
        self.right_panel_layout = QVBoxLayout()
        self.right_panel_layout.setAlignment(Qt.AlignTop)
        self.main_layout.addLayout(self.right_panel_layout)

        # Create the stacked widget to switch between conversation list and chat
        self.stacked_widget = QStackedWidget()
        self.right_panel_layout.addWidget(self.stacked_widget)

        # Create the conversation list widget
        self.conversation_list_widget = QWidget()
        conversation_list_layout = QVBoxLayout(self.conversation_list_widget)
        conversation_list_layout.setContentsMargins(10, 10, 10, 10)

        # Add the conversation list widget to the stacked widget
        self.stacked_widget.addWidget(self.conversation_list_widget)

        # Create the chat widget
        self.chat_widget = QWidget()
        chat_layout = QVBoxLayout(self.chat_widget)
        chat_layout.setContentsMargins(10, 10, 10, 10)

        # Add the chat widget to the stacked widget
        self.stacked_widget.addWidget(self.chat_widget)

        # Create the chat header widget
        self.chat_header_widget = ChatHeaderWidget("", "")
        chat_layout.addWidget(self.chat_header_widget)

        # Create the chat history widget
        self.chat_history_widget = QTextBrowser()
        self.chat_history_widget.setReadOnly(True)
        self.chat_history_widget.setStyleSheet("""
            QTextBrowser {
                background-color: #E0E0E0;
                border: none;
                padding: 10px;
                font-size: 14px;
                color: black;
            }
        """)
        chat_layout.addWidget(self.chat_history_widget)

        # Create the chat input widget
        self.chat_input_widget = QLineEdit()
        self.chat_input_widget.setPlaceholderText("Type your message here...")
        self.chat_input_widget.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                color: black;
            }
        """)
        chat_layout.addWidget(self.chat_input_widget)

        # Create the send button
        self.send_button = QPushButton("Send")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }

            QPushButton:hover {
                background-color: #3e8e41;
            }
        """)
        self.send_button.clicked.connect(self.send_message)
        chat_layout.addWidget(self.send_button)

        # Connect the contact list item selection to show the conversation
        self.contact_list_widget.itemSelectionChanged.connect(self.show_conversation)

        # Store chat history for each contact
        self.chat_history = {}

        # Initialize the file_sent_flag
        self.file_sent_flag = False
        self.contact_list_widget.itemSelectionChanged.connect(self.show_conversation)
        self.username = username
        # self.is_registered = False
        
         # Connect to the server
        self.socketio = Client()  # Initialize the 'socketio' attribute
        self.socketio.on('connect', self.on_connect)
        self.socketio.on('message', self.receive_message, namespace='/chat')
        self.socketio.connect('http://192.168.254.17:5000', namespaces=['/chat'])       
        
        # Load contacts from the database
        contacts = get_contacts(username)
        for contact, chat_history in contacts:
            item = QListWidgetItem(contact)
            item.setSizeHint(item.sizeHint())
            self.contact_list_widget.addItem(item)
            self.chat_history[contact] = chat_history.split("\n")
            
        # self.update_gui_signal.connect(self.update_gui) #check for the gui update

        # Add animation to the send button
        self.animation = QPropertyAnimation(self.send_button, b"geometry")
        self.animation.setDuration(1000)
        self.animation.setStartValue(QRect(0, 0, 100, 50))
        self.animation.setEndValue(QRect(0, 0, 200, 100))
        self.animation.start()
        
        self.socketio.on('message', self.receive_message)  # Add this line to handle incoming messages
        

        # Load or generate a symmetric encryption key
        key_file_path = "encryption_key.key"
        if os.path.exists(key_file_path):
            with open(key_file_path, "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_file_path, "wb") as key_file:
                key_file.write(key)

        self.cipher_suite = Fernet(key)
        self.encryption_manager = EncryptionManager(key)

    def encrypt_message(self, message):
        return self.encryption_manager.encrypt_message(message)

    def decrypt_message(self, encrypted_message):
        return self.encryption_manager.decrypt_message(encrypted_message)

    def on_connect(self):
        self.socketio.emit('register', {'username': self.username}, namespace='/chat')  # Send the username when connecting
        # self.is_registered = True


    def update_gui(self, sender):
        # If the sender is the currently selected contact, display the updated chat history
        selected_contact_name = self.contact_list_widget.currentItem().text()
        if sender == selected_contact_name:
            self.display_chat_history(selected_contact_name)


    def closeEvent(self, event):
        # Show a confirmation dialog box before closing the window
        reply = QMessageBox.question(self, "Quit", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def getUsername(self):
        return self.username

    def setUsername(self, username):
        self.username = username