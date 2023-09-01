import sys
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSize, QPoint
from PyQt5.QtGui import QIcon, QPalette, QColor, QFont, QCursor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QHBoxLayout, QDialog, QToolTip, QTextEdit
)
# Import the generated resources module
import resources_rc

# ... Rest of your code ...


# Initialize variables
current_webhook_url = 'YOUR_DEFAULT_WEBHOOK_URL'  # Replace with your default webhook URL
auto_message_content = "Hello, World!"

class HintsWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Hints")
        self.setGeometry(100, 100, 400, 300)  # Size of the hints dialog
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # Enable transparency
        self.setWindowOpacity(0.85)  # Adjust the transparency level here

        layout = QVBoxLayout()

        hints_label = QLabel()
        hints_text = """
            <html>
                <head/>
                <body>
                    <p>
                        <span style='color:red;font-weight:bold;'>Helpful Hints</span>
                    </p>
                    <ul>
                        <li><font color='red'>Strikethrough:</font> <span style='color:red;'>~~Your Text~~</span></li>
                        <li><font color='red'>Bold:</font> <span style='color:red;'>**Your Text**</span></li>
                        <li><font color='red'>Italics:</font> <span style='color:red;'>*Your Text* or _Your Text_</span></li>
                        <li><font color='red'>Bold Italics:</font> <span style='color:red;'>***Your Text***</span></li>
                        <li><font color='red'>Underlined:</font> <span style='color:red;'>__Your Text__</span></li>
                        <li><font color='red'>Underline bold:</font> <span style='color:red;'>__**Your Text**__</span></li>
                        <li><font color='red'>Underline italics:</font> <span style='color:red;'>__*Your Text*__</span></li>
                        <li><font color='red'>Underline bold italics:</font> <span style='color:red;'>__***Your Text***</span></li>
                        <li><font color='red'>Spoiler Tag:</font> <span style='color:red;'>||Your Text||</span></li>
                        <li><font color='red'>Empty Lines:</font> <span style='color:red;'>Shift+Enter</span></li>
                        <li><font color='red'>Single Line Code Block:</font> <span style='color:red;'>`Your Text`</span></li>
                        <li><font color='red'>Multiple Line Code Blocks:</font> <span style='color:red;'>```Your Text```</span></li>
                        <li><font color='red'>Single Line Quote:</font> <span style='color:red;'> > Your Text</span></li>
                        <li><font color='red'>Multiple lines Line Quote:</font> <span style='color:red;'> >>> Your Text</span></li>
                    </ul>
                </body>
            </html>
        """
        hints_label.setText(hints_text)

        layout.addWidget(hints_label)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class TransparentWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Linux Phantom ©")
        self.setGeometry(100, 100, 400, 180)  # Smaller window size
        self.setWindowOpacity(0.85)  # Adjust the transparency level here
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowIcon(QIcon(sys._MEIPASS + '/LP.ico'))  # Use sys._MEIPASS for the icon

        # Initialize drag_position
        self.drag_position = None

        # Create a central widget with a vertical layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Load and display the background image with transparency
        bg_image = QLabel()
        # Use sys._MEIPASS to load the image
        pixmap = QPixmap(sys._MEIPASS + "/LP.png")
        bg_image.setPixmap(pixmap)

        layout.addWidget(bg_image)

        # Create labels and entry fields for webhook URL and message content
        webhook_label = QLabel("Webhook URL:")
        self.webhook_entry = QLineEdit(current_webhook_url)

        message_label = QLabel("Message Content:")
        self.message_entry = QTextEdit(auto_message_content)  # Use QTextEdit for multiline input

        # Set red lettering for labels
        webhook_label.setStyleSheet("color: red;")
        message_label.setStyleSheet("color: red;")

        layout.addWidget(webhook_label)
        layout.addWidget(self.webhook_entry)
        layout.addWidget(message_label)
        layout.addWidget(self.message_entry)

        # Create a button to send the message with a red border
        send_message_button = QPushButton("Send Message")
        send_message_button.setStyleSheet("QPushButton { color: red; background-color: #333; border: 2px solid red; }")
        send_message_button.clicked.connect(self.send_single_message)

        layout.addWidget(send_message_button)

        # Create a status label
        self.status_label = QLabel()
        layout.addWidget(self.status_label)

        # Create an "eXit" button
        exit_button = QPushButton("eXit")
        exit_button.setStyleSheet("QPushButton { background-color: red; color: white; border: none; font-size: 18px; }")
        exit_button.clicked.connect(self.close)

        # Create a horizontal layout for buttons and center the "eXit" button
        button_layout = QHBoxLayout()
        button_layout.addWidget(send_message_button)
        button_layout.addStretch()
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

        # Create a question mark label
        question_mark_label = QLabel()
        # Use sys._MEIPASS to load the image
        question_mark_icon = QPixmap(sys._MEIPASS + "/question_mark.png")
        question_mark_icon = question_mark_icon.scaled(QSize(20, 20))
        question_mark_label.setPixmap(question_mark_icon)
        question_mark_label.setCursor(Qt.PointingHandCursor)
        QToolTip.setFont(QFont("Arial", 12))
        question_mark_label.setToolTip("Click for Hints")
        question_mark_label.mousePressEvent = self.show_hints

        layout.addWidget(question_mark_label)

        self.hints_window = HintsWindow()  # Create an instance of the HintsWindow

    def show_hints(self, event):
        self.hints_window.show()  # Show the HintsWindow non-modally

    def send_single_message(self):
        global current_webhook_url, auto_message_content
        current_webhook_url = self.webhook_entry.text()
        auto_message_content = self.message_entry.toPlainText()

        # Create a dictionary with the message content
        message_data = {
            "content": auto_message_content
        }

        try:
            # Send a POST request to the Discord webhook URL
            response = requests.post(current_webhook_url, json=message_data)

            # Check if the request was successful (HTTP status code 200)
            if response.status_code == 200:
                self.status_label.setText('Message sent.')
            else:
                self.status_label.setText('Message sent.')
        except Exception as e:
            self.status_label.setText('Error: ' + str(e))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and self.drag_position is not None:
            self.move(event.globalPos() - self.drag_position)
            event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TransparentWindow()

    # Set a darker background color
    window.setAutoFillBackground(True)
    p = window.palette()
    p.setColor(QPalette.Window, QColor(51, 51, 51))  # Dark gray background
    window.setPalette(p)

    window.show()
    sys.exit(app.exec_())