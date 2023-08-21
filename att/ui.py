from PySide6.QtWidgets import (
    QMainWindow, QWidget, QTabWidget, QGridLayout
    )
# from tab_layouts import StudentLayout
# from tab_layouts import BookLayout
# from tab_layouts import loanAndDevolutionLayout

from PySide6.QtWidgets import (
    QVBoxLayout, QTableWidget, QTableWidgetItem, QHeaderView
)
from function_windows import StudentRegisterWindow
from function_windows import BookRegisterWindow
from mybuttons import MyButtons
from database import DataBase


db = DataBase()
STUDENTS_INFO = db._getTableInfo("students")
BOOKS_INFO = db._getTableInfo("books")
LOAN_INFO = db._getTableInfo("loan")
db._closeConnectionAndCursor()


def createTable(headerLabels: list[str], infos) -> QTableWidget:
    table = QTableWidget()
    table.setColumnCount(len(headerLabels))
    table.setHorizontalHeaderLabels(headerLabels)
    table.horizontalHeader().setStretchLastSection(True)
    table.setEditTriggers(QTableWidget.NoEditTriggers)
    table.setFixedHeight(500)
    table.horizontalHeader().setSectionResizeMode(
        QHeaderView.Stretch
    )
    for i in range(0, len(infos)):
        table.insertRow(i)
        for j in range(0, len(infos[i])):
            table.setItem(
                i,
                j,
                QTableWidgetItem(str(infos[i][j]))
            )
    return table


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Biblioteca")
        self.resize(900, 800)
        self.setCentralWidget(self.createTabWidget())

    def createTabWidget(self) -> QTabWidget:
        _tabWidget = QTabWidget()
        initialTab = QWidget()
        initialTabLayout = QGridLayout()
        initialTab.setLayout(initialTabLayout)

        studentTab = QWidget()
        studentTabLayout = StudentLayout()
        studentTab.setLayout(studentTabLayout)

        bookTab = QWidget()
        bookTabLayout = BookLayout()
        bookTab.setLayout(bookTabLayout)

        loanAndDevolutionTab = QWidget()
        loanAndDevolutionTabLayout = loanAndDevolutionLayout()
        loanAndDevolutionTab.setLayout(loanAndDevolutionTabLayout)

        _tabWidget.addTab(initialTab, "Início")
        _tabWidget.addTab(studentTab, "Alunos")
        _tabWidget.addTab(bookTab, "Livros")
        _tabWidget.addTab(loanAndDevolutionTab, "Empréstimos e Devoluções")
        return _tabWidget


class StudentLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.registerWindow = StudentRegisterWindow()
        self.changeRegisterWindow = StudentRegisterWindow(changeRegister=True)

        register = MyButtons("Cadastro")
        changeRegister = MyButtons("Alterar Cadastro")
        deleteRegister = MyButtons("Apagar Cadastro")

        self.studentTable = createTable(
            [
                "ID",
                "NOME",
                "IDADE",
                "CONTATO",
                "ENDEREÇO",
                "TURNO",
                "SÉRIE"
            ],
            STUDENTS_INFO
        )

        self.addWidget(self.studentTable)
        self.addWidget(register)
        self.addWidget(changeRegister)
        self.addWidget(deleteRegister)

        register.clicked.connect(self.registerWindow.show)
        changeRegister.clicked.connect(self.changeRegisterWindow.show)


class BookLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.registerWindow = BookRegisterWindow()
        self.changeRegisterWindow = BookRegisterWindow(changeRegister=True)
        self.bookTable = createTable(
            [
                "ID",
                "TÍTULO",
                "AUTOR",
                "EDITORA",
                "GÊNERO",
                "QUANTIDADE"
            ],
            BOOKS_INFO
        )

        self.addWidget(self.bookTable)
        register = MyButtons("Cadastro")
        changeRegister = MyButtons("Alterar Cadastro")
        deleteRegister = MyButtons("Apagar Cadastro")

        self.addWidget(register)
        self.addWidget(changeRegister)
        self.addWidget(deleteRegister)

        register.clicked.connect(self.registerWindow.show)
        changeRegister.clicked.connect(self.changeRegisterWindow.show)


class loanAndDevolutionLayout(QVBoxLayout):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.loanTable = createTable(
            [
                "ID EMPŔESTIMO",
                "ID ALUNO",
                "ID LIVRO",
                "DATA EMPRÉSTIMO",
                "DATA DEVOLUÇÃO"
            ],
            LOAN_INFO
        )

        self.addWidget(self.loanTable)
        loan = MyButtons("Realizar Empréstimo")
        devolution = MyButtons("Realizar Devolução")

        self.addWidget(loan)
        self.addWidget(devolution)
