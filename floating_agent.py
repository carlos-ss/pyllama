import sys 
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget,
    QTextEdit,
    QPushButton,
)

from ask_box import AskBox
from PyQt6.QtCore import Qt, QPoint, QTimer 
from PyQt6.QtGui import QPixmap, QMovie, QIcon


class FloatingAgent(QMainWindow):
    def __init__(self):
        super().__init__()
        # self.setWindowFlags(
        #     Qt.WindowType.FramelessWindowHint | 
        #     Qt.WindowType.WindowStaysOnTopHint | 
        #     Qt.WindowType.Tool
        # )
        
        # self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.setFixedSize(300, 150)

        # self.character = QLabel(self)
        # self.movie = QMovie('assets/test.png')
        # self.character.setMovie(self.movie)
        # self.movie.start()

        self.character = QLabel(self)
        self.character.setGeometry(0, 0, 130, 150)
        pixmap = QPixmap('assets/test.png')
        self.character.setPixmap(pixmap)

        if pixmap.isNull():
            print("Failed to load image")

        self.response_box = QTextEdit(self)
        self.response_box.setFixedSize(150, 30)
        self.response_box.setReadOnly(True)
        self.response_box.move(135, 0)
        # self.response_box.hide()
        self.response_box.setPlainText("Hi, ask me a question!")

        self.ask_box = AskBox(self)
        self.ask_box.setPlaceholderText("Type and press enter..")
        


        self.drag_pos = QPoint()

        self.timer = QTimer(self)
        # self.timer.timeout.connect(self.check_for_question)


    def mousePressEvent(self, event):
        if(event.button() == Qt.MouseButton.LeftButton):
            self.drag_pos = event.globalPosition().toPoint() - self.pos()
        
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
    
    def mouseDoubleClickEvent(self, event):
        if self.response_box.isHidden():
            self.response_box.show()
            
        else:
            self.response_box.hide()


    
            



    #  probably wont need, all questions should typed
    # def check_for_question(self):
    #     clipboard = QApplication.clipboard().text()
    #     if "?" in clipboard:
    #         self.ask_ai(clipboard)
            
    
if __name__ == "__main__":  
    app = QApplication(sys.argv)
    window = FloatingAgent()
    window.show()
    sys.exit(app.exec())
