from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QPushButton, QApplication
from PyQt5.QtGui import QPalette, QColor
from ui_forms import AddProductForm, AddReceiptForm, AddIssueForm, ReportForm, ViewProductsForm, SearchProductForm, SettingsForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Система управления запасами - ООО ТПК"Атлант-Медиа"')
        
        self.stackedWidget = QStackedWidget()
        self.setCentralWidget(self.stackedWidget)

        self.mainMenu = QWidget()
        self.addProductWidget = AddProductForm()
        self.addReceiptWidget = AddReceiptForm()
        self.addIssueWidget = AddIssueForm()
        self.reportWidget = ReportForm()
        self.viewProductsWidget = ViewProductsForm()
        self.searchProductWidget = SearchProductForm()
        self.settingsWidget = SettingsForm()

        self.stackedWidget.addWidget(self.mainMenu)
        self.stackedWidget.addWidget(self.addProductWidget)
        self.stackedWidget.addWidget(self.addReceiptWidget)
        self.stackedWidget.addWidget(self.addIssueWidget)
        self.stackedWidget.addWidget(self.reportWidget)
        self.stackedWidget.addWidget(self.viewProductsWidget)
        self.stackedWidget.addWidget(self.searchProductWidget)
        self.stackedWidget.addWidget(self.settingsWidget)

        self.initMainMenu()

        self.addProductWidget.go_back.connect(self.showMainMenu)
        self.addReceiptWidget.go_back.connect(self.showMainMenu)
        self.addIssueWidget.go_back.connect(self.showMainMenu)
        self.reportWidget.go_back.connect(self.showMainMenu)
        self.viewProductsWidget.go_back.connect(self.showMainMenu)
        self.searchProductWidget.go_back.connect(self.showMainMenu)
        self.settingsWidget.go_back.connect(self.showMainMenu)

        self.addProductWidget.data_updated.connect(self.refreshData)
        self.addReceiptWidget.data_updated.connect(self.refreshData)
        self.addIssueWidget.data_updated.connect(self.refreshData)

        self.settingsWidget.theme_changed.connect(self.changeTheme)

    def initMainMenu(self):
        layout = QVBoxLayout()
        self.mainMenu.setLayout(layout)

        addProductButton = QPushButton('Добавить продукт')
        addReceiptButton = QPushButton('Добавить поступление')
        addIssueButton = QPushButton('Добавить выдачу')
        reportButton = QPushButton('Сформировать отчет')
        viewProductsButton = QPushButton('Просмотр и редактирование продуктов')
        searchProductButton = QPushButton('Поиск продукта')
        settingsButton = QPushButton('Настройки')

        addProductButton.clicked.connect(self.showAddProductWidget)
        addReceiptButton.clicked.connect(self.showAddReceiptWidget)
        addIssueButton.clicked.connect(self.showAddIssueWidget)
        reportButton.clicked.connect(self.showReportWidget)
        viewProductsButton.clicked.connect(self.showViewProductsWidget)
        searchProductButton.clicked.connect(self.showSearchProductWidget)
        settingsButton.clicked.connect(self.showSettingsWidget)

        layout.addWidget(addProductButton)
        layout.addWidget(addReceiptButton)
        layout.addWidget(addIssueButton)
        layout.addWidget(reportButton)
        layout.addWidget(viewProductsButton)
        layout.addWidget(searchProductButton)
        layout.addWidget(settingsButton)

    def showMainMenu(self):
        self.stackedWidget.setCurrentWidget(self.mainMenu)

    def showAddProductWidget(self):
        self.stackedWidget.setCurrentWidget(self.addProductWidget)

    def showAddReceiptWidget(self):
        self.stackedWidget.setCurrentWidget(self.addReceiptWidget)

    def showAddIssueWidget(self):
        self.stackedWidget.setCurrentWidget(self.addIssueWidget)

    def showReportWidget(self):
        self.stackedWidget.setCurrentWidget(self.reportWidget)

    def showViewProductsWidget(self):
        self.stackedWidget.setCurrentWidget(self.viewProductsWidget)
        self.viewProductsWidget.refresh()

    def showSearchProductWidget(self):
        self.stackedWidget.setCurrentWidget(self.searchProductWidget)

    def showSettingsWidget(self):
        self.stackedWidget.setCurrentWidget(self.settingsWidget)

    def refreshData(self):
        if self.stackedWidget.currentWidget() == self.reportWidget:
            self.reportWidget.generateReport()
        elif self.stackedWidget.currentWidget() == self.viewProductsWidget:
            self.viewProductsWidget.refresh()

    def changeTheme(self, theme):
        if theme == 'Светлая тема':
            self.setLightTheme()
        elif theme == 'Темная тема':
            self.setDarkTheme()

    def setLightTheme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(255, 255, 255))
        palette.setColor(QPalette.WindowText, QColor(0, 0, 0))
        palette.setColor(QPalette.Base, QColor(255, 255, 255))
        palette.setColor(QPalette.AlternateBase, QColor(240, 240, 240))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(0, 0, 0))
        palette.setColor(QPalette.Button, QColor(240, 240, 240))
        palette.setColor(QPalette.ButtonText, QColor(0, 0, 0))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(0, 0, 255))
        palette.setColor(QPalette.Highlight, QColor(0, 120, 215))
        palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
        QApplication.instance().setPalette(palette)

    def setDarkTheme(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        palette.setColor(QPalette.Base, QColor(35, 35, 35))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, QColor(255, 255, 255))
        palette.setColor(QPalette.ToolTipText, QColor(0, 0, 0))
        palette.setColor(QPalette.Text, QColor(255, 255, 255))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        palette.setColor(QPalette.Link, QColor(42, 130, 218))
        palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        palette.setColor(QPalette.HighlightedText, QColor(0, 0, 0))


        QApplication.instance().setPalette(palette)

