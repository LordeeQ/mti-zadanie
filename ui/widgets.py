# тут все мои виджеты, унаследованные от виджетов qt

from datetime import datetime

from PyQt6.QtCore import QLocale, Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (
    QAbstractItemView, QCheckBox, QComboBox, QGroupBox, QHeaderView, QLabel,
    QLineEdit, QListWidget, QMenuBar, QMessageBox, QPushButton,
    QSpinBox, QStatusBar, QTableWidget, QTableWidgetItem, QTabWidget,
)

from services.formatter import Formatter


class StyledButton(QPushButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        # +32 потому что стиль добавляет отступы и текст обрезался
        self.setMinimumWidth(self.sizeHint().width() + 32)


# красная кнопка
class DangerButton(StyledButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("role", "danger")


# зеленая кнопка
class SuccessButton(StyledButton):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setProperty("role", "success")


class SearchLineEdit(QLineEdit):

    def __init__(self, placeholder="Поиск...", parent=None):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setClearButtonEnabled(True)

    # по Esc очищаем поиск
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            self.clear()
        else:
            super().keyPressEvent(event)


class PriceSpinBox(QSpinBox):

    def __init__(self, value=0, parent=None):
        super().__init__(parent)
        self.setRange(0, 100000000)
        self.setSingleStep(50000)
        # русская локаль чтобы тысячи разделялись пробелом а не запятой
        self.setLocale(QLocale(QLocale.Language.Russian, QLocale.Country.Russia))
        self.setGroupSeparatorShown(True)
        self.setSuffix(" руб.")
        self.setValue(value)


class YearSpinBox(QSpinBox):

    def __init__(self, parent=None):
        super().__init__(parent)
        year = datetime.now().year
        self.setRange(1950, year + 1)
        self.setValue(year)


class TypeComboBox(QComboBox):
    ALL = "Все типы"

    def __init__(self, type_names, with_all=True, parent=None):
        super().__init__(parent)
        if with_all:
            self.addItem(self.ALL)
        self.addItems(type_names)

    def selected_type(self):
        if self.currentText() == self.ALL:
            return None
        return self.currentText()


class SortComboBox(QComboBox):

    def __init__(self, options, parent=None):
        super().__init__(parent)
        self.addItems(options)


class InStockCheckBox(QCheckBox):

    def __init__(self, parent=None):
        super().__init__("Только в наличии", parent)
        self.setChecked(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class TitleLabel(QLabel):

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        font = self.font()
        font.setPointSize(16)
        font.setBold(True)
        self.setFont(font)


class TotalLabel(QLabel):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.setStyleSheet("font-size: 14pt; font-weight: 700; color: #16a34a;")
        self.set_total(0)

    def set_total(self, value):
        self.setText("Итого: " + Formatter.price(value))


class SectionGroupBox(QGroupBox):

    def __init__(self, title, parent=None):
        super().__init__(title, parent)


# таблица которую нельзя редактировать, выделяется вся строка
class ReadOnlyTable(QTableWidget):

    def __init__(self, headers, parent=None):
        super().__init__(0, len(headers), parent)
        self.setHorizontalHeaderLabels(headers)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.setAlternatingRowColors(True)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

    # эти колонки растягиваются, остальные по ширине текста
    def stretch_columns(self, *columns):
        for col in columns:
            self.horizontalHeader().setSectionResizeMode(col, QHeaderView.ResizeMode.Stretch)

    @staticmethod
    def make_item(text, right=False):
        item = QTableWidgetItem(text)
        if right:
            item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        return item


class VehicleTable(ReadOnlyTable):
    HEADERS = ["Тип", "Марка", "Модель", "Год", "Цвет", "Параметр", "Цена", "Статус"]
    vehicle_activated = pyqtSignal(object)  # двойной клик по машине

    def __init__(self, parent=None):
        super().__init__(self.HEADERS, parent)
        self.stretch_columns(1, 2)
        self._vehicles = []

    def set_vehicles(self, vehicles):
        self._vehicles = list(vehicles)
        self.setRowCount(len(self._vehicles))
        for row, v in enumerate(self._vehicles):
            cells = [
                self.make_item(v.type_name()),
                self.make_item(v.brand),
                self.make_item(v.model),
                self.make_item(str(v.year), right=True),
                self.make_item(v.color),
                self.make_item(v.extra_text(), right=True),
                self.make_item(Formatter.price(v.price), right=True),
                self.make_item(Formatter.stock(v.in_stock)),
            ]
            # проданные серым
            if not v:
                for cell in cells:
                    cell.setForeground(QColor("#94a3b8"))
            for col, cell in enumerate(cells):
                self.setItem(row, col, cell)

    def selected_vehicle(self):
        row = self.currentRow()
        if row < 0 or row >= len(self._vehicles):
            return None
        if not self.selectionModel().hasSelection():
            return None
        return self._vehicles[row]

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        v = self.selected_vehicle()
        if v is not None:
            self.vehicle_activated.emit(v)


class SalesTable(ReadOnlyTable):
    HEADERS = ["N", "Дата", "Клиент", "Телефон", "Машины", "Менеджер", "Сумма"]

    def __init__(self, parent=None):
        super().__init__(self.HEADERS, parent)
        self.stretch_columns(2, 4)

    def set_orders(self, orders):
        self.setRowCount(len(orders))
        for row, order in enumerate(orders):
            cars = ", ".join(v.title for v in order)
            cells = [
                self.make_item(str(order.number), right=True),
                self.make_item(order.created_at.strftime("%d.%m.%Y %H:%M")),
                self.make_item(order.client.name),
                self.make_item(order.client.phone),
                self.make_item(cars),
                self.make_item(order.manager_login),
                self.make_item(Formatter.price(order.total), right=True),
            ]
            for col, cell in enumerate(cells):
                self.setItem(row, col, cell)


class CartListWidget(QListWidget):
    remove_requested = pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._vehicles = []

    def set_vehicles(self, vehicles):
        self.clear()
        self._vehicles = list(vehicles)
        for v in self._vehicles:
            self.addItem(f"{v.title} - {Formatter.price(v.price)}")

    def selected_vehicle(self):
        row = self.currentRow()
        if 0 <= row < len(self._vehicles):
            return self._vehicles[row]
        return None

    # Delete убирает машину из корзины
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete and self.selected_vehicle() is not None:
            self.remove_requested.emit(self.selected_vehicle())
        else:
            super().keyPressEvent(event)


class AppTabWidget(QTabWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTabPosition(QTabWidget.TabPosition.North)


# снизу показывает кто зашел и часы
class ClockStatusBar(QStatusBar):

    def __init__(self, login, parent=None):
        super().__init__(parent)
        self._user_label = QLabel("Пользователь: " + login)
        self._clock_label = QLabel()
        self.addWidget(self._user_label)
        self.addPermanentWidget(self._clock_label)
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update_clock)
        self._timer.start(1000)
        self.update_clock()

    def update_clock(self):
        self._clock_label.setText(datetime.now().strftime("%d.%m.%Y %H:%M:%S"))


class AppMenuBar(QMenuBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.file_menu = self.addMenu("Файл")
        self.add_action = self.file_menu.addAction("Добавить машину")
        self.file_menu.addSeparator()
        self.exit_action = self.file_menu.addAction("Выход")
        self.help_menu = self.addMenu("Справка")
        self.stats_action = self.help_menu.addAction("Статистика по маркам")
        self.about_action = self.help_menu.addAction("О программе")


# окно да/нет, у стандартного кнопки на английском
class ConfirmBox(QMessageBox):

    def __init__(self, title, text, parent=None):
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Question)
        self.setWindowTitle(title)
        self.setText(text)
        self._yes = self.addButton("Да", QMessageBox.ButtonRole.YesRole)
        self.addButton("Нет", QMessageBox.ButtonRole.NoRole)

    @staticmethod
    def ask(parent, title, text):
        box = ConfirmBox(title, text, parent)
        box.exec()
        return box.clickedButton() == box._yes
