from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFormLayout, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QVBoxLayout, QWidget,
)

from containers.showroom import Cart, OrderBook, Showroom
from models.order import Order
from services.formatter import Formatter
from services.report import ReportWriter
from ui.dialogs import AddVehicleDialog, CheckoutDialog
from ui.widgets import (
    AppMenuBar, AppTabWidget, CartListWidget, ClockStatusBar, ConfirmBox, DangerButton,
    InStockCheckBox, PriceSpinBox, SalesTable, SearchLineEdit, SectionGroupBox,
    SortComboBox, StyledButton, SuccessButton, TitleLabel, TotalLabel, TypeComboBox,
    VehicleTable,
)


class MainWindow(QMainWindow):

    def __init__(self, user, session, showroom, vehicle_types):
        super().__init__()
        self._user = user
        self._session = session
        self._showroom = showroom
        self._vehicle_types = vehicle_types
        self._cart = Cart()
        self._orders = OrderBook()

        self.setWindowTitle("Автосалон - " + user.full_name)
        self.resize(1400, 760)

        self.make_menu()
        self.setStatusBar(ClockStatusBar(user.login))

        self._tabs = AppTabWidget()
        self._tabs.addTab(self.make_catalog_tab(), "Каталог")
        self._tabs.addTab(self.make_sales_tab(), "Продажи")
        self.setCentralWidget(self._tabs)

        self.refresh_catalog()
        self.refresh_cart()
        self.refresh_sales()

    def make_menu(self):
        menu = AppMenuBar()
        menu.add_action.triggered.connect(self.add_vehicle)
        menu.exit_action.triggered.connect(self.close)
        menu.stats_action.triggered.connect(self.show_stats)
        menu.about_action.triggered.connect(self.show_about)
        self.setMenuBar(menu)

    def make_catalog_tab(self):
        # фильтры слева
        self._search_edit = SearchLineEdit("Марка, модель или цвет")
        self._type_box = TypeComboBox(self._vehicle_types.keys())
        self._min_price = PriceSpinBox(0)
        self._max_price = PriceSpinBox(self._showroom.max_price)
        self._sort_box = SortComboBox(Showroom.SORT_OPTIONS.keys())
        self._stock_check = InStockCheckBox()
        reset_btn = StyledButton("Сбросить")
        reset_btn.clicked.connect(self.reset_filters)

        filters_form = QFormLayout()
        filters_form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        filters_form.addRow("Поиск:", self._search_edit)
        filters_form.addRow("Тип:", self._type_box)
        filters_form.addRow("Цена от:", self._min_price)
        filters_form.addRow("Цена до:", self._max_price)
        filters_form.addRow("Сортировка:", self._sort_box)
        filters_form.addRow("", self._stock_check)
        filters_form.addRow("", reset_btn)
        filters_box = SectionGroupBox("Фильтры")
        filters_box.setLayout(filters_form)
        filters_box.setFixedWidth(300)

        # при любом изменении фильтра обновляем таблицу
        self._search_edit.textChanged.connect(self.refresh_catalog)
        self._type_box.currentIndexChanged.connect(self.refresh_catalog)
        self._min_price.valueChanged.connect(self.refresh_catalog)
        self._max_price.valueChanged.connect(self.refresh_catalog)
        self._sort_box.currentIndexChanged.connect(self.refresh_catalog)
        self._stock_check.toggled.connect(self.refresh_catalog)

        # таблица машин по центру
        self._table = VehicleTable()
        self._table.vehicle_activated.connect(self.add_to_cart)
        self._found_label = QLabel()
        add_btn = StyledButton("Добавить авто")
        add_btn.clicked.connect(self.add_vehicle)
        to_cart_btn = SuccessButton("В корзину")
        to_cart_btn.clicked.connect(self.add_selected_to_cart)
        delete_btn = DangerButton("Удалить")
        delete_btn.clicked.connect(self.delete_selected)

        catalog_buttons = QHBoxLayout()
        catalog_buttons.addStretch()
        catalog_buttons.addWidget(add_btn)
        catalog_buttons.addWidget(delete_btn)
        catalog_buttons.addWidget(to_cart_btn)

        catalog_layout = QVBoxLayout()
        catalog_layout.addWidget(self._found_label)
        catalog_layout.addWidget(self._table)
        catalog_layout.addLayout(catalog_buttons)
        catalog_box = SectionGroupBox("Автомобили")
        catalog_box.setLayout(catalog_layout)

        # корзина справа
        self._cart_list = CartListWidget()
        self._cart_list.remove_requested.connect(self.remove_from_cart)
        self._total_label = TotalLabel()
        remove_btn = DangerButton("Убрать")
        remove_btn.clicked.connect(self.remove_selected_from_cart)
        self._checkout_btn = SuccessButton("Оформить покупку")
        self._checkout_btn.clicked.connect(self.checkout)

        cart_buttons = QHBoxLayout()
        cart_buttons.addWidget(remove_btn)
        cart_buttons.addWidget(self._checkout_btn)
        cart_layout = QVBoxLayout()
        cart_layout.addWidget(self._cart_list)
        cart_layout.addWidget(self._total_label)
        cart_layout.addLayout(cart_buttons)
        cart_box = SectionGroupBox("Корзина")
        cart_box.setLayout(cart_layout)
        cart_box.setMinimumWidth(340)

        body = QHBoxLayout()
        body.addWidget(filters_box)
        body.addWidget(catalog_box, stretch=1)
        body.addWidget(cart_box)

        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Каталог автосалона"))
        layout.addLayout(body)
        page = QWidget()
        page.setLayout(layout)
        return page

    def make_sales_tab(self):
        self._sales_table = SalesTable()
        self._revenue_label = TotalLabel()
        layout = QVBoxLayout()
        layout.addWidget(TitleLabel("Журнал продаж"))
        layout.addWidget(self._sales_table)
        layout.addWidget(self._revenue_label)
        page = QWidget()
        page.setLayout(layout)
        return page

    def refresh_catalog(self):
        max_price = self._max_price.value()
        if max_price == 0:
            max_price = None
        vehicles = self._showroom.filter(
            text=self._search_edit.text(),
            type_name=self._type_box.selected_type(),
            min_price=self._min_price.value(),
            max_price=max_price,
            only_in_stock=self._stock_check.isChecked(),
            sort_by=self._sort_box.currentText(),
        )
        self._table.set_vehicles(vehicles)
        self._found_label.setText(f"Найдено: {len(vehicles)} из {len(self._showroom)}, "
                                  f"в наличии: {self._showroom.in_stock_count}")

    def refresh_cart(self):
        self._cart_list.set_vehicles(self._cart)
        self._total_label.set_total(self._cart.total)
        self._checkout_btn.setEnabled(len(self._cart) > 0)

    def refresh_sales(self):
        self._sales_table.set_orders(list(self._orders))
        self._revenue_label.setText(f"Продано заказов: {len(self._orders)}, "
                                    f"выручка: {Formatter.price(self._orders.revenue)}")

    def reset_filters(self):
        self._search_edit.clear()
        self._type_box.setCurrentIndex(0)
        self._min_price.setValue(0)
        self._max_price.setValue(self._showroom.max_price)
        self._sort_box.setCurrentIndex(0)
        self._stock_check.setChecked(True)

    def add_vehicle(self):
        dialog = AddVehicleDialog(self._vehicle_types, self)
        if not dialog.exec():
            return
        try:
            self._showroom.add(dialog.vehicle)
        except ValueError as e:
            QMessageBox.warning(self, "Ошибка", str(e))
            return
        # если новая машина дороже фильтра, то ее не будет видно, поднимаем фильтр
        if dialog.vehicle.price > self._max_price.value():
            self._max_price.setValue(self._showroom.max_price)
        self.refresh_catalog()
        self.statusBar().showMessage("Добавлено: " + str(dialog.vehicle), 4000)

    def delete_selected(self):
        vehicle = self._table.selected_vehicle()
        if vehicle is None:
            QMessageBox.information(self, "Удаление", "Сначала выберите машину в таблице")
            return
        if not ConfirmBox.ask(self, "Удаление", f"Удалить {vehicle.title} из каталога?"):
            return
        self._showroom.remove(vehicle)
        if vehicle in self._cart:
            self._cart.remove(vehicle)
        self.refresh_catalog()
        self.refresh_cart()

    def add_selected_to_cart(self):
        vehicle = self._table.selected_vehicle()
        if vehicle is None:
            QMessageBox.information(self, "Корзина", "Сначала выберите машину в таблице")
            return
        self.add_to_cart(vehicle)

    def add_to_cart(self, vehicle):
        try:
            self._cart += vehicle
        except ValueError as e:
            QMessageBox.information(self, "Корзина", str(e))
            return
        self.refresh_cart()
        self.statusBar().showMessage("В корзину: " + vehicle.title, 3000)

    def remove_selected_from_cart(self):
        vehicle = self._cart_list.selected_vehicle()
        if vehicle is not None:
            self.remove_from_cart(vehicle)

    def remove_from_cart(self, vehicle):
        self._cart.remove(vehicle)
        self.refresh_cart()

    def checkout(self):
        if len(self._cart) == 0:
            return
        dialog = CheckoutDialog(self._cart.total, len(self._cart), self)
        if not dialog.exec():
            return
        order = Order(dialog.client, self._user.login)
        for vehicle in self._cart:
            order += vehicle
            vehicle.in_stock = False
        self._orders.add(order)
        self._cart.clear()
        self.refresh_cart()
        self.refresh_catalog()
        self.refresh_sales()
        QMessageBox.information(self, "Покупка оформлена",
                                f"{order}\nСумма: {Formatter.price(order.total)}")

    def show_stats(self):
        stats = self._showroom.brand_stats()
        lines = []
        for brand in sorted(stats):
            lines.append(f"{brand}: {stats[brand]} шт.")
        if not lines:
            lines.append("Каталог пуст")
        QMessageBox.information(self, "В наличии по маркам", "\n".join(lines))

    def show_about(self):
        QMessageBox.about(self, "О программе",
                          "Автосалон. Задание по ООП, Python + PyQt6.\n"
                          "Двойной клик по машине кладет ее в корзину, "
                          "Delete в корзине убирает.")

    # Ctrl+F поиск, Ctrl+N новая машина
    def keyPressEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_F:
                self._tabs.setCurrentIndex(0)
                self._search_edit.setFocus()
                return
            if event.key() == Qt.Key.Key_N:
                self.add_vehicle()
                return
        super().keyPressEvent(event)

    # при закрытии пишем отчет
    # print тут нельзя, в exe без консоли он падает
    def closeEvent(self, event):
        ReportWriter.save(self._session)
        event.accept()
