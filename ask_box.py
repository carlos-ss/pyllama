
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtCore import Qt

from cache import CacheManager



class AskBox(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setPlaceholderText("Enter your text here...")
        self.setFixedHeight(30)
        self.setFixedWidth(150)
        self.move(150, 95)

        self.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 5px;
            }""")

        self.cache = CacheManager()


    def keyPressEvent(self, event): 
        isEnterKey = event.key() == Qt.Key.Key_Return or event.key() == Qt.Key.Key_Enter
        isNotShiftKey = not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        
        if isEnterKey and isNotShiftKey:
            
            response = self.cache.get_response(self.toPlainText())
            self.parent.response_box.setPlainText(response)
            self.clear()
            
            
        else:
            super().keyPressEvent(event)