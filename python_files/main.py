import sys
from gui import QT_app, MainWindow

def main() -> int:

    UI = QT_app(sys.argv)
    window = MainWindow(filename="settings.ini", app = UI)
    window.show()
    UI.exec()

    return 0


if __name__ == '__main__':
    main()
    sys.exit()
