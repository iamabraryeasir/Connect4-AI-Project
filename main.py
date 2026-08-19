import sys

from PyQt6.QtWidgets import QApplication

from src.ui.app_controller import AppController


def main():
    app = QApplication(sys.argv)
    window = AppController()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
