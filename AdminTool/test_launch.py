import sys
from PyQt5.QtWidgets import QApplication
try:
    from admin_gui import AdminWindow
    print("Successfully imported AdminWindow")
except Exception as e:
    print(f"Failed to import AdminWindow: {e}")
    sys.exit(1)

def main():
    app = QApplication(sys.argv)
    try:
        window = AdminWindow()
        print("Successfully instantiated AdminWindow")
        # Don't show or exec, just check if it crashes on init
        # window.show() 
    except Exception as e:
        print(f"Failed to instantiate AdminWindow: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
