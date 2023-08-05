"""This submodule defines the main window of our application."""
from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QThreadPool
from PySide6.QtGui import QCloseEvent, QKeyEvent

from melon.melon import Melon
from melon.todo import Todo

from .calendarlist import CalendarListView
from .tasklist import TaskListView, UserRole


class GuiMelon(Melon):
    """Subclasses the `Melon` main object, adding a handler for changes within the data."""

    def __init__(self) -> None:
        """Initialises the Melon."""
        super().__init__()
        self.tasklistView: TaskListView | None = None

    def addOrUpdateTask(self, todo: Todo):
        """
        Args:
            todo (Todo): Argument
        """
        assert self.tasklistView is not None
        uid = todo.uid
        assert uid is not None
        for row in range(self.tasklistView.count()):
            data = self.tasklistView.item(row).data(UserRole)
            if getattr(data, "uid", None) == uid:
                if todo.isComplete():
                    self.tasklistView.takeItem(row)
                else:
                    self.tasklistView.blockSignals(True)
                    self.tasklistView.item(row).setText(todo.summary)
                    self.tasklistView.item(row).setData(UserRole, todo)
                    self.tasklistView.blockSignals(False)
                return
        if todo.isIncomplete():
            self.tasklistView.addTask(todo)


class MainWindow(QtWidgets.QWidget):
    """Main Window class that defines most of the UI."""

    def __init__(self) -> None:
        """Initialises the main window."""
        super().__init__()
        self.melon = GuiMelon()
        self.threadPool = QThreadPool()
        self.setWindowTitle("Melon UI")

    def buildUI(self):
        """
        Args:
        """
        self.tasklistView = TaskListView(self.melon)
        self.melon.tasklistView = self.tasklistView
        self.calendarlistView = CalendarListView()
        self.calendarlistView.currentItemChanged.connect(self.calendarListClicked)
        self.searchWidget = QtWidgets.QLineEdit()
        self.searchWidget.setPlaceholderText("Search tasks...")
        self.messageLabel = QtWidgets.QLabel(self)
        self.messageLabel.setHidden(True)
        self.messageLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.messageLabel, 0, 1, 1, 2)
        # layout.addWidget(self.searchWidget, 0, 1, 1, 2)
        layout.addWidget(self.calendarlistView, 1, 1)
        layout.addWidget(self.tasklistView, 1, 2)
        self.setLayout(layout)

    def start(self):
        """
        Args:
        """
        self.melon.autoInit()
        self.tasklistView.sortItems()
        self.calendarlistView.populate(self.melon.calendars.values())
        # QTimer.singleShot(200, self.sync)

    def sync(self):
        """
        Args:
        """
        self.showInfoMessage("Syncing...")
        QtWidgets.QApplication.processEvents()
        self.melon.syncAll()
        self.tasklistView.sortItems()
        self.hideMessage()

    def closeEvent(self, event: QCloseEvent) -> None:
        """
        Args:
            event (QCloseEvent): Argument

        """
        self.melon.store()
        return super().closeEvent(event)

    def calendarListClicked(self, item: QtWidgets.QListWidgetItem):
        """
        Args:
            item (QListWidgetItem): Argument
        """
        userData = item.data(Qt.ItemDataRole.UserRole)
        if userData and userData["is-special"] and userData["specialty"] == "all":
            self.tasklistView.clearCalendarFilter()
        else:
            self.tasklistView.setCalendarFilter(item.text())

    def keyPressEvent(self, event: QKeyEvent):
        """
        Args:
            event (QKeyEvent): Argument
        """
        # print("Key Event", event)
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_W:
                self.close()
            elif event.key() == Qt.Key.Key_S:
                self.sync()
            elif event.key() == Qt.Key.Key_H:
                self.calendarlistView.setCurrentRow(0)
            elif event.key() == Qt.Key.Key_Plus:
                self.tasklistView.addEmptyTask()
            elif event.key() == Qt.Key.Key_Return:
                self.threadPool.start(self.melon.scheduleAllAndExport)
        # if Qt.Key.Key_A <= event.key() <= Qt.Key.Key_Z:
        #     self.searchWidget.setFocus()
        return super().keyPressEvent(event)

    def showInfoMessage(self, msg: str):
        """
        Args:
            msg (str): Argument
        """
        self.messageLabel.setText(msg)
        self.messageLabel.setHidden(False)

    def hideMessage(self):
        """
        Args:
        """
        self.messageLabel.setHidden(True)
