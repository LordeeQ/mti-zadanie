from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QSpinBox, QVBoxLayout,
)

from models.people import Client
from services.formatter import Formatter
from ui.widgets import (
    DangerButton, PriceSpinBox, StyledButton, SuccessButton, TitleLabel,
    TypeComboBox, YearSpinBox,
)


class LoginWindow(QDialog):

    def __init__(self, registry, parent=None):
        super().__init__(parent)
        self._registry = registry
        self._user = None
        self.setWindowTitle("Автосалон - вход")
        self.setFixedWidth(360)

        self._login_edit = QLineEdit()
        self._login_edit.setPlaceholderText("Логин")
        self._password_edit = QLineEdit()
        self._password_edit.setPlaceholderText("Пароль")
        self._password_edit.setEchoMode(QLineEdit.EchoMode.Password)
        hint = QLabel("Тестовый вход: admin / admin или manager / 1234")
        hint.setStyleSheet("color: #64748b;")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)

        form = QFormLayout()
        form.addRow("Логин:", self._login_edit)
        form.addRow("Пароль:", self._password_edit)

        login_btn = StyledButton("Войти")
        login_btn.setDefault(True)
        login_btn.clicked.connect(self.try_login)
        cancel_btn = DangerButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addWidget(cancel_btn)
        buttons.addWidget(login_btn)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.addWidget(TitleLabel("Автосалон"), alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addLayout(form)
        layout.addWidget(hint)
        layout.addLayout(buttons)

    @property
    def user(self):
        return self._user

    def try_login(self):
        try:
            self._user = self._registry.authenticate(
                self._login_edit.text(), self._password_edit.text())
        except PermissionError as e:
            QMessageBox.warning(self, "Ошибка входа", str(e))
            self._password_edit.clear()
            self._password_edit.setFocus()
            return
        self.accept()


# форма добавления машины
class AddVehicleDialog(QDialog):

    def __init__(self, vehicle_types, parent=None):
        super().__init__(parent)
        self._vehicle_types = vehicle_types
        self._vehicle = None
        self.setWindowTitle("Новая машина")
        self.setMinimumWidth(420)

        self._type_box = TypeComboBox(vehicle_types.keys(), with_all=False)
        self._vin_edit = QLineEdit()
        self._vin_edit.setMaxLength(17)
        self._vin_edit.setPlaceholderText("17 символов, например XTA21700080000001")
        self._brand_edit = QLineEdit()
        self._model_edit = QLineEdit()
        self._year_spin = YearSpinBox()
        self._color_edit = QLineEdit()
        self._price_spin = PriceSpinBox(1000000)
        self._extra_label = QLabel()
        self._extra_spin = QSpinBox()
        self._extra_spin.setRange(1, 100000)

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form.addRow("Тип:", self._type_box)
        form.addRow("VIN:", self._vin_edit)
        form.addRow("Марка:", self._brand_edit)
        form.addRow("Модель:", self._model_edit)
        form.addRow("Год выпуска:", self._year_spin)
        form.addRow("Цвет:", self._color_edit)
        form.addRow("Цена:", self._price_spin)
        form.addRow(self._extra_label, self._extra_spin)

        save_btn = SuccessButton("Сохранить")
        save_btn.clicked.connect(self.try_save)
        cancel_btn = DangerButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(cancel_btn)
        buttons.addWidget(save_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)

        self._type_box.currentTextChanged.connect(self.update_extra_field)
        self.update_extra_field(self._type_box.currentText())

    @property
    def vehicle(self):
        return self._vehicle

    # у каждого типа свой доп. параметр, меняем подпись
    def update_extra_field(self, type_name):
        cls = self._vehicle_types[type_name]
        self._extra_label.setText(cls.extra_label() + ":")

    def try_save(self):
        cls = self._vehicle_types[self._type_box.currentText()]
        try:
            self._vehicle = cls(
                self._vin_edit.text(), self._brand_edit.text(), self._model_edit.text(),
                self._year_spin.value(), self._price_spin.value(), self._color_edit.text(),
                self._extra_spin.value(),
            )
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
            return
        self.accept()


class CheckoutDialog(QDialog):

    def __init__(self, total, items_count, parent=None):
        super().__init__(parent)
        self._client = None
        self.setWindowTitle("Оформление покупки")
        self.setMinimumWidth(380)

        self._name_edit = QLineEdit()
        self._name_edit.setPlaceholderText("Иванов Петр")
        self._phone_edit = QLineEdit()
        self._phone_edit.setPlaceholderText("+7 900 123-45-67")

        form = QFormLayout()
        form.addRow("Позиций:", QLabel(str(items_count)))
        form.addRow("Сумма:", QLabel(Formatter.price(total)))
        form.addRow("Клиент:", self._name_edit)
        form.addRow("Телефон:", self._phone_edit)

        ok_btn = SuccessButton("Оформить")
        ok_btn.clicked.connect(self.try_accept)
        cancel_btn = DangerButton("Отмена")
        cancel_btn.clicked.connect(self.reject)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(cancel_btn)
        buttons.addWidget(ok_btn)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addLayout(buttons)

    @property
    def client(self):
        return self._client

    def try_accept(self):
        try:
            self._client = Client(self._name_edit.text(), self._phone_edit.text())
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
            return
        self.accept()
