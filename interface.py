import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QLabel, 
                             QVBoxLayout, QHBoxLayout, QWidget, QStackedWidget, QFrame)
from PyQt5.QtGui import QMovie, QFont, QColor, QPalette, QBrush, QPixmap
from PyQt5.QtCore import QProcess, Qt, QSize, QTimer

class HighTechFrame(QFrame):
    """A custom frame with a glowing futuristic border"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: rgba(0, 20, 40, 150);
                border: 2px solid cyan;
                border-radius: 15px;
            }
        """)

class AegisUltimateGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.setWindowTitle("AEGIS OPTIMUS - BIOMETRIC UNIT")
        self.setGeometry(100, 100, 900, 700)
        
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(0, 0, 10))
        self.setPalette(palette)

        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        
        self.header_label = QLabel(">> SYSTEM INITIALIZING...", self)
        self.header_label.setAlignment(Qt.AlignCenter)
        self.header_label.setStyleSheet("""
            color: cyan; font-family: 'Courier New'; font-size: 18px; font-weight: bold;
            border-bottom: 2px solid cyan; padding-bottom: 10px;
        """)
        main_layout.addWidget(self.header_label)

        
        self.stack = QStackedWidget()
        self.stack.setStyleSheet("background-color: transparent;")
        
        
        self.page_idle = QLabel()
        self.page_idle.setAlignment(Qt.AlignCenter)
        self.movie_idle = QMovie("idle_core.gif") 
        self.page_idle.setMovie(self.movie_idle)
        self.movie_idle.start()
        self.stack.addWidget(self.page_idle)

        
        self.page_scan.setAlignment(Qt.AlignCenter)
        self.movie_scan = QMovie("face_scan.gif") 
        self.page_scan.setMovie(self.movie_scan)
        
        self.stack.addWidget(self.page_scan)

        
        self.page_listen = QLabel()
        self.page_listen.setAlignment(Qt.AlignCenter)
        self.movie_listen = QMovie("listening.gif") 
        self.page_listen.setMovie(self.movie_listen)
        self.stack.addWidget(self.page_listen)

        
        core_frame = HighTechFrame()
        core_layout = QVBoxLayout()
        core_layout.addWidget(self.stack)
        core_frame.setLayout(core_layout)
        main_layout.addWidget(core_frame, stretch=2) 

        
        log_frame = HighTechFrame()
        log_layout = QVBoxLayout()
        
        log_label = QLabel(">> MISSION LOG")
        log_label.setStyleSheet("color: cyan; font-family: Impact; border: none;")
        log_layout.addWidget(log_label)

        self.terminal = QTextEdit(self)
        self.terminal.setReadOnly(True)
        self.terminal.setStyleSheet("""
            background-color: transparent; 
            color: #00FF00; 
            font-family: Consolas; 
            font-size: 14px; 
            border: none;
        """)
        self.terminal.setFixedHeight(150)
        log_layout.addWidget(self.terminal)
        log_frame.setLayout(log_layout)
        main_layout.addWidget(log_frame)

        
        self.process = QProcess(self)
        self.process.readyReadStandardOutput.connect(self.handle_output)
        self.process.readyReadStandardError.connect(self.handle_error)
        
        self.process.start("python", ["-u", "main.py"])

    def set_status(self, text, color="cyan"):
        """Updates the top header text"""
        self.header_label.setText(f">> {text.upper()}")
        self.header_label.setStyleSheet(f"""
            color: {color}; font-family: 'Courier New'; font-size: 18px; font-weight: bold;
            border-bottom: 2px solid {color}; padding-bottom: 10px;
        """)

    def handle_output(self):
        """The Brain: Reads main.py output and updates UI dynamically"""
        data = self.process.readAllStandardOutput()
        text = bytes(data).decode("utf8").strip()
        
        if not text: return

        lower_text = text.lower()

        
        if "scanning face" in lower_text or "biometric" in lower_text:
            self.set_status("BIOMETRIC SCAN IN PROGRESS...", "red")
            self.stack.setCurrentIndex(1) 
            self.movie_scan.start()

        
        elif "access granted" in lower_text or "welcome" in lower_text:
            self.movie_scan.stop()
            self.set_status("IDENTITY VERIFIED. SYSTEMS ONLINE.", "#00FF00")
            self.stack.setCurrentIndex(0) # Back to Idle Core
            self.terminal.append(f"\n[SUCCESS] {text}")

        
        elif "listening..." in lower_text:
            self.set_status("LISTENING FOR COMMAND...", "yellow")
            self.stack.setCurrentIndex(2) 
            self.movie_listen.start()

        
        elif "processing..." in lower_text:
             self.set_status("PROCESSING DATA...", "orange")
             
        
        elif "aegis:" in lower_text:
            self.set_status("AEGIS SPEAKING", "cyan")
            self.stack.setCurrentIndex(0) 
            
            clean_text = text.replace("AEGIS:", "").strip()
            self.terminal.append(f"[AEGIS] >> {clean_text}")
        
        
        elif "user:" in lower_text:
            clean_text = text.replace("User:", "").strip()
            self.terminal.append(f"[USER] >> {clean_text}")
            
        
        elif "error" in lower_text or "denied" in lower_text:
            self.set_status("SYSTEM WARNING / ACCESS DENIED", "red")
            self.movie_scan.stop()
            self.stack.setCurrentIndex(0)

        
        cursor = self.terminal.textCursor()
        cursor.movePosition(cursor.End)
        self.terminal.setTextCursor(cursor)

    def handle_error(self):
        data = self.process.readAllStandardError()
        error = bytes(data).decode("utf8")
        if error.strip():
            self.terminal.append(f"[SYSTEM ERROR] >> {error}")

    def closeEvent(self, event):
        self.process.terminate()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AegisUltimateGUI()
    window.show()
    sys.exit(app.exec_())