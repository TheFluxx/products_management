from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHBoxLayout, QLabel, QComboBox, QFontComboBox, QSpinBox
from PyQt5.QtCore import QDate, pyqtSignal
from database import Database
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
            return

        existing_product = self.db.get_product_by_name(name)
        if existing_product:
            return

        self.db.add_product(name)
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

    def editProduct(self):
        product_id = self.editIdInput.text()
        new_name = self.editNameInput.text()
        new_quantity_text = self.editQuantityInput.text()


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