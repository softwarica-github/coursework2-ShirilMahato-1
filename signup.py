import bcrypt
import sqlite3
from imports import*

class SignupWindow(QWidget):
    def __init__(self, login_window):
        super().__init__()
        self.login_window = login_window

        self.setWindowTitle("WhatsApp Lite - Signup")
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

        # Create signup form
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

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("""
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

        self.signup_button = QPushButton("Sign up")
        self.signup_button.setStyleSheet("""
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

        # Add signup form widgets to layout
        layout.addWidget(self.username_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.signup_button)

        layout.addSpacing(80)

        # Add line separator
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)

        # Add spacing below the line
        layout.addSpacing(20)

        # "Already a member? Signin Here" text
        signin_text = QLabel("Already have an Account? ")
        signin_text.setAlignment(Qt.AlignRight)
        signin_text.setStyleSheet("color: white;")

        signin_link = QLabel("<a href='#'>Signin Here</a>")
        signin_link.setAlignment(Qt.AlignLeft)
        signin_link.setStyleSheet("color: white; font-weight: bold;")
        signin_link.setOpenExternalLinks(False)
        signin_link.linkActivated.connect(self.open_signin)

        signin_layout = QHBoxLayout()
        signin_layout.addWidget(signin_text)
        signin_layout.addWidget(signin_link)

        # Add the signin text layout to the bottom
        layout.addLayout(signin_layout)

        # Set layout alignment
        layout.setContentsMargins(120, 0, 120, 0)
        layout.setAlignment(Qt.AlignCenter)

        self.setLayout(layout)

        # Set palette for text colors
        palette = QPalette()
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        # Connect button signals to methods
        self.signup_button.clicked.connect(self.signup)

    def paintEvent(self, event):
        # Custom paint event to draw the gradient background
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#4CAF50"))
        gradient.setColorAt(1, QColor("#202020"))
        painter.fillRect(self.rect(), gradient)

    def open_signin(self):
        self.close()
        self.login_window.show()

    def signup(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()

        if not username or not email or not password:
            QMessageBox.warning(self, "Signup Error", "Please fill in all the fields.")
            return

        # Check if username already exists
        if self.username_exists(username):
            QMessageBox.warning(self, "Signup Error", "Username already exists. Please choose a different username.")
            return

        # Encrypt the password
        hashed_password = self.hash_password(password)

        # Save the user to the database
        self.save_user(username, email, hashed_password)

        QMessageBox.information(self, "Signup Successful", "Your account has been created successfully!")

    def username_exists(self, username):
        # Connect to the database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Create the users table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT, password TEXT)")

        # Check if the username already exists in the database
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        # Close the database connection
        conn.close()

        return result is not None


    def hash_password(self, password):
        # Generate a salt for bcrypt
        salt = bcrypt.gensalt()

        # Hash the password with the salt
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        # Convert the hashed password to a string for storage
        return hashed_password.decode("utf-8")

    def save_user(self, username, email, password):
        # Connect to the database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Create the users table if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, email TEXT, password TEXT)")

        # Insert the user into the table
        cursor.execute("INSERT INTO users VALUES (?, ?, ?)", (username, email, password))

        # Commit the changes and close the database connection
        conn.commit()
        conn.close()
