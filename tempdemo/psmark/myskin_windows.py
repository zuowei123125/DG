from os.path import join, dirname, abspath
from qtpy.QtCore import Qt, QMetaObject, Signal, Slot, QEvent
from qtpy.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QToolButton, QLabel, QSizePolicy
from PyQt5.QtGui import QIcon, QPixmap
import qtpy, platform

QT_VERSION = tuple((int(v) for v in qtpy.QT_VERSION.split('.')))
PLATFORM = platform.system()
_FL_STYLESHEET = 'frameless.qss'

class WindowDragger(QWidget):
    '''Window dragger.
    Args:
    window (QWidget): Associated window.
    parent (QWidget, optional): Parent widget.
    '''
    doubleClicked = Signal()

    def __init__(self, window, parent=None):
        QWidget.__init__(self, parent)
        self._window = window
        self._mousePressed = False

    def mousePressEvent(self, event):
        self._mousePressed = True
        self._mousePos = event.globalPos()
        self._windowPos = self._window.pos()

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self._window.move(self._windowPos + (event.globalPos() - self._mousePos))

    def mouseReleaseEvent(self, event):
        self._mousePressed = False

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()


class ModernWindow(QWidget):
    '''
    Modern window.
    Args:
    w (QWidget): Main widget.
    parent (QWidget, optional): Parent widget.
    '''

    def __init__(self, w, parent=None):
        QWidget.__init__(self, parent)
        self._w = w
        self.setupUi()
        contentLayout = QHBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.addWidget(w)
        self.windowContent.setLayout(contentLayout)
        self.setWindowTitle(w.windowTitle())
        self.setGeometry(w.geometry())
        self._w.setAttribute(Qt.WA_DeleteOnClose, True)
        self._w.destroyed.connect(self._ModernWindow__child_was_closed)

    def setupUi(self):
        self.vboxWindow = QVBoxLayout(self)
        self.vboxWindow.setContentsMargins(0, 0, 0, 0)
        self.windowFrame = QWidget(self)
        self.windowFrame.setObjectName('windowFrame')
        self.vboxFrame = QVBoxLayout(self.windowFrame)
        self.vboxFrame.setContentsMargins(0, 0, 0, 0)
        self.titleBar = WindowDragger(self, self.windowFrame)
        self.titleBar.setObjectName('titleBar')
        self.titleBar.setSizePolicy(QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed))
        self.hboxTitle = QHBoxLayout(self.titleBar)
        self.hboxTitle.setContentsMargins(0, 0, 0, 0)
        self.hboxTitle.setSpacing(0)
        titleIcon = QPixmap('./ui/icon.png')
        Icon = QLabel()
        Icon.setPixmap(titleIcon.scaled(30, 30))
        self.icon = Icon
        self.icon.setAlignment(Qt.AlignLeft)
        self.lblTitle = QLabel('Title')
        self.lblTitle.setObjectName('lblTitle')
        self.lblTitle.setAlignment(Qt.AlignVCenter)
        spButtons = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnMinimize = QToolButton(self.titleBar)
        self.btnMinimize.setObjectName('btnMinimize')
        self.btnMinimize.setSizePolicy(spButtons)
        self.btnRestore = QToolButton(self.titleBar)
        self.btnRestore.setObjectName('btnRestore')
        self.btnRestore.setSizePolicy(spButtons)
        self.btnRestore.setVisible(False)
        self.btnMaximize = QToolButton(self.titleBar)
        self.btnMaximize.setObjectName('btnMaximize')
        self.btnMaximize.setSizePolicy(spButtons)
        self.btnClose = QToolButton(self.titleBar)
        self.btnClose.setObjectName('btnClose')
        self.btnClose.setSizePolicy(spButtons)
        self.vboxFrame.addWidget(self.titleBar)
        self.windowContent = QWidget(self.windowFrame)
        self.vboxFrame.addWidget(self.windowContent)
        self.vboxWindow.addWidget(self.windowFrame)
        PLATFORM = '1Darwin'
        if PLATFORM == 'Darwin':
            self.hboxTitle.addWidget(self.btnClose)
            self.hboxTitle.addWidget(self.btnMinimize)
            self.hboxTitle.addWidget(self.btnRestore)
            self.hboxTitle.addWidget(self.btnMaximize)
            self.hboxTitle.addWidget(self.lblTitle)
        else:
            self.hboxTitle.addWidget(self.icon)
            self.hboxTitle.addWidget(self.lblTitle)
            self.hboxTitle.addWidget(self.btnMinimize)
            self.hboxTitle.addWidget(self.btnRestore)
            self.hboxTitle.addWidget(self.btnMaximize)
            self.hboxTitle.addWidget(self.btnClose)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        with open(_FL_STYLESHEET) as (stylesheet):
            self.setStyleSheet(stylesheet.read())
        QMetaObject.connectSlotsByName(self)

    def __child_was_closed(self):
        self._w = None
        self.close()

    def closeEvent(self, event):
        if not self._w:
            event.accept()
        else:
            self._w.close()
            event.setAccepted(self._w.isHidden())

    def setWindowTitle(self, title):
        super(ModernWindow, self).setWindowTitle(title)
        self.lblTitle.setText(title)

    @Slot()
    def on_btnMinimize_clicked(self):
        self.setWindowState(Qt.WindowMinimized)

    @Slot()
    def on_btnRestore_clicked(self):
        self.btnRestore.setVisible(False)
        self.btnMaximize.setVisible(True)
        self.setWindowState(Qt.WindowNoState)

    @Slot()
    def on_btnMaximize_clicked(self):
        self.btnRestore.setVisible(True)
        self.btnMaximize.setVisible(False)
        self.setWindowState(Qt.WindowMaximized)

    @Slot()
    def on_btnClose_clicked(self):
        self.close()

    @Slot()
    def on_titleBar_doubleClicked(self):
        if self.btnMaximize.isVisible():
            self.on_btnMaximize_clicked()
        else:
            self.on_btnRestore_clicked()
