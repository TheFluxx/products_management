from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QComboBox, QFontComboBox, QSpinBox
from PyQt5.QtCore import QDate, pyqtSignal
from database import Database
from ui_helpers import show_message, show_warning, fill_table_with_products, fill_table_with_report, get_product_id_and_quantity
from PyQt5.QtWidgets import QApplication

class AddProductForm(QWidget):
    go_back = pyqtSignal()
    data_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database('inventory.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить продукт - ООО ТПК"Атлант-Медиа"')
        layout = QVBoxLayout()
        formLayout = QFormLayout()
        self.setLayout(layout)

        self.productNameInput = QLineEdit()
        formLayout.addRow('Название продукта:', self.productNameInput)

        self.addButton = QPushButton('Добавить продукт')
        self.addButton.clicked.connect(self.addProduct)

        layout.addLayout(formLayout)
        layout.addWidget(self.addButton)
        backButton = QPushButton('Назад')
        backButton.clicked.connect(self.go_back.emit)
        layout.addWidget(backButton)

    def addProduct(self):
        name = self.productNameInput.text()

        if not name:
            show_warning(self, 'Ошибка', 'Название продукта не может быть пустым')
            return

        existing_product = self.db.get_product_by_name(name)
        if existing_product:
            show_warning(self, 'Ошибка', 'Продукт с таким названием уже существует')
            return

        self.db.add_product(name)
        show_message(self, 'Успех', 'Продукт успешно добавлен')
        self.data_updated.emit()



class AddReceiptForm(QWidget):
    go_back = pyqtSignal()
    data_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database('inventory.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить поступление - ООО ТПК"Атлант-Медиа"')
        layout = QVBoxLayout()
        formLayout = QFormLayout()
        self.setLayout(layout)

        self.receiptProductNameInput = QLineEdit()
        self.receiptQuantityInput = QLineEdit()

        formLayout.addRow('Название продукта:', self.receiptProductNameInput)
        formLayout.addRow('Количество поступления:', self.receiptQuantityInput)

        self.receiptButton = QPushButton('Добавить поступление')
        self.receiptButton.clicked.connect(self.addReceipt)

        layout.addLayout(formLayout)
        layout.addWidget(self.receiptButton)
        backButton = QPushButton('Назад')
        backButton.clicked.connect(self.go_back.emit)
        layout.addWidget(backButton)

    def addReceipt(self):
        name = self.receiptProductNameInput.text()
        quantity_text = self.receiptQuantityInput.text()

        product_id, current_quantity, error = get_product_id_and_quantity(self.db, name, quantity_text)
        if error:
            show_warning(self, 'Ошибка', error)
            return

        new_quantity = current_quantity + float(quantity_text)
        self.db.update_product_quantity(product_id, new_quantity)
        self.db.add_receipt(product_id, QDate.currentDate().toString('yyyy-MM-dd'), float(quantity_text))
        show_message(self, 'Успех', 'Поступление успешно добавлено')
        self.data_updated.emit()

class AddIssueForm(QWidget):
    go_back = pyqtSignal()
    data_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database('inventory.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Добавить выдачу - ООО ТПК"Атлант-Медиа"')
        layout = QVBoxLayout()
        formLayout = QFormLayout()
        self.setLayout(layout)

        self.issueProductNameInput = QLineEdit()
        self.issueQuantityInput = QLineEdit()

        formLayout.addRow('Название продукта:', self.issueProductNameInput)
        formLayout.addRow('Количество выдачи:', self.issueQuantityInput)

        self.issueButton = QPushButton('Добавить выдачу')
        self.issueButton.clicked.connect(self.addIssue)

        layout.addLayout(formLayout)
        layout.addWidget(self.issueButton)
        backButton = QPushButton('Назад')
        backButton.clicked.connect(self.go_back.emit)
        layout.addWidget(backButton)

    def addIssue(self):
        name = self.issueProductNameInput.text()
        quantity_text = self.issueQuantityInput.text()

        product_id, current_quantity, error = get_product_id_and_quantity(self.db, name, quantity_text)
        if error:
            show_warning(self, 'Ошибка', error)
            return

        if current_quantity < float(quantity_text):
            show_warning(self, 'Ошибка', 'Недостаточное количество продукта')
            return

        new_quantity = current_quantity - float(quantity_text)
        self.db.update_product_quantity(product_id, new_quantity)
        self.db.add_issue(product_id, QDate.currentDate().toString('yyyy-MM-dd'), float(quantity_text))
        show_message(self, 'Успех', 'Выдача успешно добавлена')
        self.data_updated.emit()

class ReportForm(QWidget):
    go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database('inventory.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Отчет - ООО ТПК"Атлант-Медиа"')
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.reportTable = QTableWidget()
        layout.addWidget(self.reportTable)
        backButton = QPushButton('Назад')
        backButton.clicked.connect(self.go_back.emit)
        layout.addWidget(backButton)

        self.reportButton = QPushButton('Сформировать отчет')
        self.reportButton.clicked.connect(self.generateReport)
        layout.addWidget(self.reportButton)

    def generateReport(self):
        products = self.db.get_all_products()
        fill_table_with_report(self.reportTable, products)

class ViewProductsForm(QWidget):
    go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database('inventory.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Просмотр и редактирование продуктов - ООО ТПК"Атлант-Медиа"')
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.productsTable = QTableWidget()
        layout.addWidget(self.productsTable)

        self.refreshButton = QPushButton('Обновить')
        self.refreshButton.clicked.connect(self.refresh)
        layout.addWidget(self.refreshButton)

        editLayout = QHBoxLayout()
        self.editIdInput = QLineEdit()
        self.editNameInput = QLineEdit()
        self.editQuantityInput = QLineEdit()
        editLayout.addWidget(QLabel('ID:'))
        editLayout.addWidget(self.editIdInput)
        editLayout.addWidget(QLabel('Название:'))
        editLayout.addWidget(self.editNameInput)
        editLayout.addWidget(QLabel('Количество:'))
        editLayout.addWidget(self.editQuantityInput)
        self.editButton = QPushButton('Редактировать')
        self.editButton.clicked.connect(self.editProduct)
        editLayout.addWidget(self.editButton)
        layout.addLayout(editLayout)

        backButton = QPushButton('Назад')
        backButton.clicked.connect(self.go_back.emit)
        layout.addWidget(backButton)

    def refresh(self):
        products = self.db.get_all_products()
        fill_table_with_products(self.productsTable, products)

    def editProduct(self):
        product_id = self.editIdInput.text()
        new_name = self.editNameInput.text()
        new_quantity_text = self.editQuantityInput.text()

        if not product_id:
            show_warning(self, 'Ошибка', 'ID продукта не может быть пустым')
            return

        if not new_quantity_text:
            show_warning(self, 'Ошибка', 'Количество не может быть пустым')
            return

        try:
            new_quantity = float(new_quantity_text)
        except ValueError:
            show_warning(self, 'Ошибка', 'Количество должно быть числом')
            return

        self.db.update_product(product_id, new_name, new_quantity)
        show_message(self, 'Успех', 'Продукт успешно обновлен')
        self.refresh()

class SearchProductForm(QWidget):
    go_back = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.db = Database('inventory.db')
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Поиск продукта - ООО ТПК"Атлант-Медиа"')
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.searchProductInput = QLineEdit()
        self.searchProductButton = QPushButton('Поиск')

        layout.addWidget(QLabel('Введите название продукта:'))
        layout.addWidget(self.searchProductInput)
        layout.addWidget(self.searchProductButton)

        self.searchProductButton.clicked.connect(self.searchProduct)

        self.searchResultsTable = QTableWidget()
        layout.addWidget(self.searchResultsTable)

        backButton = QPushButton('Назад')
        backButton.clicked.connect(self.go_back.emit)
        layout.addWidget(backButton)

    def searchProduct(self):
        search_text = self.searchProductInput.text()
        products = self.db.search_products_by_name(search_text)
        fill_table_with_products(self.searchResultsTable, products)


class SettingsForm(QWidget):
    go_back = pyqtSignal()
    theme_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Настройки - ООО ТПК"Атлант-Медиа"')
        layout = QVBoxLayout()
        self.setLayout(layout)

        themeLayout = QHBoxLayout()
        themeLabel = QLabel('Выберите тему:')
        themeLabel.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: black;
                padding: 10px;
            }
        """)
        self.themeComboBox = QComboBox()
        self.themeComboBox.addItems(['Светлая тема', 'Темная тема'])
        self.themeComboBox.currentTextChanged.connect(self.changeTheme)
        

        self.themeComboBox.setStyleSheet("""
            QComboBox {
                color: black;
            }
            QComboBox QAbstractItemView {
                color: black;
            }
        """)

        themeLayout.addWidget(themeLabel)
        themeLayout.addWidget(self.themeComboBox)

        fontLayout = QHBoxLayout()
        fontLabel = QLabel('Выберите шрифт:')
        fontLabel.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: black;
                padding: 10px;
            }
        """)
        self.fontComboBox = QFontComboBox()
        self.fontComboBox.currentFontChanged.connect(self.changeFont)

        fontLayout.addWidget(fontLabel)
        fontLayout.addWidget(self.fontComboBox)

        fontSizeLayout = QHBoxLayout()
        fontSizeLabel = QLabel('Размер шрифта:')
        fontSizeLabel.setStyleSheet("""
            QLabel {
                font-size: 18px;
                font-weight: bold;
                color: black;
                padding: 10px;
            }
        """)
        self.fontSizeSpinBox = QSpinBox()
        self.fontSizeSpinBox.setRange(8, 22)
        self.fontSizeSpinBox.setValue(12)
        self.fontSizeSpinBox.valueChanged.connect(self.changeFontSize)
        self.fontSizeSpinBox.editingFinished.connect(self.validateFontSize)

        fontSizeLayout.addWidget(fontSizeLabel)
        fontSizeLayout.addWidget(self.fontSizeSpinBox)

        layout.addLayout(themeLayout)
        layout.addLayout(fontLayout)
        layout.addLayout(fontSizeLayout)

        backButton = QPushButton('Назад')
        backButton.clicked.connect(self.go_back.emit)
        layout.addWidget(backButton)

    def validateFontSize(self):
        if self.fontSizeSpinBox.value() > self.fontSizeSpinBox.maximum():
            self.fontSizeSpinBox.setValue(self.fontSizeSpinBox.maximum())

    def changeTheme(self, theme):
        self.theme_changed.emit(theme)

    def changeFont(self, font):
        QApplication.instance().setFont(font)

    def changeFontSize(self, size):
        font = QApplication.instance().font()
        font.setPointSize(size)
        QApplication.instance().setFont(font)