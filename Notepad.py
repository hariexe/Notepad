import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class NotepadApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.text_edit = QTextEdit(self)
        layout.addWidget(self.text_edit)

        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        new_action = QAction(QIcon('icons/new.png'), 'New', self)
        new_action.setShortcut('Ctrl+N')
        new_action.triggered.connect(self.new_file)
        toolbar.addAction(new_action)

        open_action = QAction(QIcon('icons/open.png'), 'Open', self)
        open_action.setShortcut('Ctrl+O')
        open_action.triggered.connect(self.open_file)
        toolbar.addAction(open_action)

        save_action = QAction(QIcon('icons/save.png'), 'Save', self)
        save_action.setShortcut('Ctrl+S')
        save_action.triggered.connect(self.save_file)
        toolbar.addAction(save_action)

        toolbar.addSeparator()
        
        cut_action = QAction(QIcon('icons/cut.png'), 'Cut', self)
        cut_action.setShortcut('Ctrl+X')
        cut_action.triggered.connect(self.cut_text)
        toolbar.addAction(cut_action)

        copy_action = QAction(QIcon('icons/copy.png'), 'Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy_text)
        toolbar.addAction(copy_action)

        paste_action = QAction(QIcon('icons/paste.png'), 'Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.paste_text)
        toolbar.addAction(paste_action)

        toolbar.addSeparator()

        undo_action = QAction(QIcon('icons/undo.png'), 'Undo', self)
        undo_action.setShortcut('Ctrl+Z')
        undo_action.triggered.connect(self.text_edit.undo)
        toolbar.addAction(undo_action)

        redo_action = QAction(QIcon('icons/redo.png'), 'Redo', self)
        redo_action.setShortcut('Ctrl+Y')
        redo_action.triggered.connect(self.text_edit.redo)
        toolbar.addAction(redo_action)

        toolbar.addSeparator()

        color_action = QAction(QIcon('icons/color.png'), 'Change Color', self)
        color_action.triggered.connect(self.change_text_color)
        toolbar.addAction(color_action)
        
        toolbar.addSeparator()

        font_size_combo = QComboBox(self)
        font_size_combo.setPlaceholderText('Font Size')
        font_size_combo.addItem('8')
        font_size_combo.addItem('10')
        font_size_combo.addItem('12')
        font_size_combo.addItem('14')
        font_size_combo.addItem('16')
        font_size_combo.addItem('18')
        font_size_combo.addItem('20')
        font_size_combo.addItem('24')
        font_size_combo.addItem('28')
        font_size_combo.addItem('32')
        font_size_combo.currentIndexChanged.connect(self.change_font_size)
        toolbar.addWidget(font_size_combo)

        self.setStyleSheet('QMainWindow {background-color: #2b2b2b; color: #ffffff;}'
                           'QTextEdit {background-color: black; color: white;}'
                           'QToolBar {background-color: #2b2b2b;}'
                           'QToolButton {background-color: white; color: #ffffff;}')

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Notepad')
        self.show()
    
    def change_font_size(self, index):
        font_size = int(self.sender().currentText())

        cursor = self.text_edit.textCursor()
        fmt = QTextCharFormat()
        fmt.setFontPointSize(font_size)
        cursor.mergeCharFormat(fmt)
        self.text_edit.setTextCursor(cursor)


    def keyPressEvent(self, event):
        # Mengatur ukuran font sesuai dengan ukuran terakhir yang diatur
        cursor = self.text_edit.textCursor()
        fmt = cursor.charFormat()
        font_size = fmt.fontPointSize()

        # Jika tidak ada teks tersisa, kita atur ukuran font sesuai dengan yang terakhir kali diatur
        if not self.text_edit.toPlainText():
            if font_size > 0:
                font = QFont()
                font.setPointSize(int(font_size))  # Ubah ke tipe data integer
                fmt.setFont(font)  # Gunakan setFont pada QTextCharFormat
                cursor.setCharFormat(fmt)
                cursor.insertText(event.text())
            else:
                # Jika ukuran font tidak diatur, gunakan ukuran default
                super().keyPressEvent(event)
        else:
            # Jika masih ada teks, kita lanjutkan seperti sebelumnya
            if font_size > 0:
                font = QFont()
                font.setPointSize(int(font_size))  # Ubah ke tipe data integer
                fmt.setFont(font)  # Gunakan setFont pada QTextCharFormat
                cursor.setCharFormat(fmt)
                cursor.insertText(event.text())
            else:
                super().keyPressEvent(event)

    def new_file(self):
        self.text_edit.clear()

    def open_file(self):
        dialog = QFileDialog()
        dialog.setNameFilter('Text Files (*.txt);;All Files (*)')
        file_paths, _ = dialog.getOpenFileNames(self, 'Open File', '', 'Text Files (*.txt);;All Files (*)',)
            
        if file_paths:
            file_path = file_paths[0]
            try:
                with open(file_path, 'r') as file:
                    self.text_edit.setPlainText(file.read())
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error opening file:\n{str(e)}')

    def save_file(self):
        options = QFileDialog()
        options.setNameFilter('Text Files (*.txt);;All Files (*)')
        file_name, _ = options.getSaveFileName(self, 'Save File', '', 'Text Files (*.txt);;All Files (*)',)

        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, 'Success', 'File saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Error saving file:\n{str(e)}')

    def cut_text(self):
        cursor = self.text_edit.textCursor()
        cursor.removeSelectedText()

    def copy_text(self):
        cursor = self.text_edit.textCursor()
        cursor.copy()

    def paste_text(self):
        cursor = self.text_edit.textCursor()
        cursor.insertText(QApplication.clipboard().text())

    def change_text_color(self):
        color = QColorDialog.getColor(initial=Qt.GlobalColor.white, parent=self)

        if color.isValid():
            self.text_edit.setTextColor(color)



def main():
    app = QApplication(sys.argv)
    notepad_app = NotepadApp()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()