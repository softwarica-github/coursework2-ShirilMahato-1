from imports import*
import sqlite3
import bcrypt
from mainwindow import MainWindow


class LoginWindow(QWidget):
    def __init__(self, signup_window):
        super().__init__()
        self.signup_window = signup_window

        self.setWindowTitle("WhatsApp Lite - Login")
        self.setFixedSize(650, 700)  # Set fixed window size

        layout = QVBoxLayout()

        # Custom background gradient
        self.setAutoFillBackground(True)
        palette = self.palette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#4CAF50"))
        gradient.setColorAt(1, QColor("#202020"))
        palette.setBrush(QPalette.Window, gradient)
        self.setPalette(palette)

        # WhatsApp logo and title
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)
        logo_pixmap = QPixmap("D:\Shiril\programming\python\cw_2\WhatsApp.png")  # Replace with the actual path to your logo image
        logo_label.setPixmap(logo_pixmap.scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio))

        title_label = QLabel("WhatsApp Lite")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 36px; font-weight: bold; color: white;")

        # Add logo and title to layout
        logo_layout = QVBoxLayout()
        logo_layout.addWidget(logo_label)
        logo_layout.addSpacing(10)  # Add spacing between the logo and title
        logo_layout.addWidget(title_label)
        layout.addLayout(logo_layout)

        layout.addSpacing(60)

        # Create login form
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
        """)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                background-color: #333333;
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
        """)

        self.login_button = QPushButton("Sign in")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Add login form widgets to layout
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        # Add spacing between the login form and line
        layout.addSpacing(100)

        # Add line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Add spacing below the line
        layout.addSpacing(20)

        # "Not a member? Signup Here" text
        signup_text = QLabel("Not have an Account? ")
        signup_text.setAlignment(Qt.AlignRight)
        signup_text.setStyleSheet("color: white;")

        signup_link = QLabel("<a href='#'>Signup Here</a>")
        signup_link.setAlignment(Qt.AlignLeft)
        signup_link.setStyleSheet("color: white; font-weight: bold;")
        signup_link.setOpenExternalLinks(False)
        signup_link.linkActivated.connect(self.open_signup)

        signup_layout = QHBoxLayout()
        signup_layout.addWidget(signup_text)
        signup_layout.addWidget(signup_link)

        # Add the signup text layout to the bottom
        layout.addLayout(signup_layout)

        # Set layout alignment
        layout.setContentsMargins(120, 0, 120, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

        # Set palette for text colors
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # Connect button signals to methods
        self.login_button.clicked.connect(self.login)

    def paintEvent(self, event):
        # Custom paint event to draw the gradient background
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#4CAF50"))
        gradient.setColorAt(1, QColor("#202020"))
        painter.fillRect(self.rect(), gradient)

    def open_signup(self):
        self.close()
        self.signup_window.show()


    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Login Error", "Please enter username and password.")
            return

        # Authenticate the user
        if self.authenticate_user(username, password):
            self.open_dashboard(username)
        else:
            QMessageBox.warning(self, "Login Error", "Invalid username or password.")

    def authenticate_user(self, username, password):
        # Connect to the database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Retrieve the user's hashed password from the database
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        # Close the database connection
        conn.close()

        if result is not None:
            hashed_password = result[0].encode("utf-8")
            # Check if the entered password matches the hashed password
            if bcrypt.checkpw(password.encode("utf-8"), hashed_password):
                return True

        return False

    def open_dashboard(self, username):
        # You can create a new window or update the existing window to show the dashboard
        from mainwindow import MainWindow  # Lazy import
        self.main_window = MainWindow(username)  # Create a new instance of MainWindow
        self.main_window.show()  # Show the MainWindow
        self.close()

        # if username and password:
        #     main_window = MainWindow(username)  # Pass the username to the main window
        #     main_window.show()
        #     self.close()