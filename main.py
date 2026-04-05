"""
Airline Reservation System — Application Entry Point
"""

import sys
import os

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFont
from ui.main_window import MainWindow


# ======================================================================
#  MODERN DARK STYLESHEET
# ======================================================================
STYLESHEET = """
/* ---- Global ---- */
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", "Roboto", "Arial", sans-serif;
    font-size: 14px;
}

/* ---- Auth Card ---- */
#authCard {
    background-color: #313244;
    border-radius: 16px;
    border: 1px solid #45475a;
}
#authTitle {
    font-size: 22px;
    font-weight: bold;
    color: #89b4fa;
    padding: 10px 0;
}

/* ---- Tabs ---- */
QTabWidget::pane {
    border: 1px solid #45475a;
    border-radius: 8px;
    background: #313244;
}
QTabBar::tab {
    background: #45475a;
    color: #cdd6f4;
    padding: 8px 20px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #89b4fa;
    color: #1e1e2e;
    font-weight: bold;
}

/* ---- Inputs ---- */
QLineEdit, QSpinBox, QComboBox, QDateTimeEdit {
    background-color: #45475a;
    border: 1px solid #585b70;
    border-radius: 6px;
    padding: 8px 12px;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
}
QLineEdit:focus, QSpinBox:focus, QComboBox:focus, QDateTimeEdit:focus {
    border: 1px solid #89b4fa;
}
QComboBox::drop-down {
    border: none;
    padding-right: 8px;
}
QComboBox QAbstractItemView {
    background-color: #45475a;
    color: #cdd6f4;
    selection-background-color: #89b4fa;
    selection-color: #1e1e2e;
}

/* ---- Buttons ---- */
QPushButton {
    background-color: #45475a;
    color: #cdd6f4;
    padding: 8px 18px;
    border-radius: 6px;
    border: none;
    font-weight: 500;
}
QPushButton:hover {
    background-color: #585b70;
}
QPushButton:pressed {
    background-color: #6c7086;
}
#primaryBtn {
    background-color: #89b4fa;
    color: #1e1e2e;
    font-weight: bold;
}
#primaryBtn:hover {
    background-color: #74c7ec;
}
#dangerBtn {
    background-color: #f38ba8;
    color: #1e1e2e;
    font-weight: bold;
}
#dangerBtn:hover {
    background-color: #eba0ac;
}
#logoutBtn {
    background-color: transparent;
    color: #f38ba8;
    border: 1px solid #f38ba8;
}
#logoutBtn:hover {
    background-color: #f38ba8;
    color: #1e1e2e;
}

/* ---- Tables ---- */
QTableWidget {
    background-color: #313244;
    gridline-color: #45475a;
    border: 1px solid #45475a;
    border-radius: 8px;
    selection-background-color: #585b70;
}
QHeaderView::section {
    background-color: #45475a;
    color: #89b4fa;
    font-weight: bold;
    padding: 6px;
    border: none;
    border-bottom: 2px solid #89b4fa;
}

/* ---- Panel Title ---- */
#panelTitle {
    font-size: 20px;
    font-weight: bold;
    color: #89b4fa;
    padding: 8px 0;
}

/* ---- Scrollbar ---- */
QScrollBar:vertical {
    background: #313244;
    width: 10px;
    border-radius: 5px;
}
QScrollBar::handle:vertical {
    background: #585b70;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

/* ---- Group Box ---- */
QGroupBox {
    border: 1px solid #45475a;
    border-radius: 8px;
    margin-top: 10px;
    padding-top: 14px;
    font-weight: bold;
    color: #89b4fa;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}

/* ---- Message Box ---- */
QMessageBox {
    background-color: #313244;
}
QMessageBox QLabel {
    color: #cdd6f4;
}
QMessageBox QPushButton {
    min-width: 80px;
}

/* ---- Dialog ---- */
QDialog {
    background-color: #313244;
    border-radius: 12px;
}

/* ---- Labels ---- */
QLabel {
    background: transparent;
}
"""


def main():
    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setStyleSheet(STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
