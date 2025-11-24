import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox
)
class NewFilm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить новый фильм")
        self.setGeometry(200, 200, 400, 300)


        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)


        layout.addWidget(QLabel("Название фильма:"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)


        layout.addWidget(QLabel("Режиссёр:"))
        self.director_input = QLineEdit()
        layout.addWidget(self.director_input)


        layout.addWidget(QLabel("Год создания:"))
        self.year_input = QLineEdit()
        layout.addWidget(self.year_input)


        layout.addWidget(QLabel("Жанр:"))
        self.genre_combo = QComboBox()
        self.genre_combo.addItems([
            "Боевик", "Драма", "Комедия", "Фантастика",
            "Ужасы", "Мультфильм", "Детектив", "Фэнтези"
        ])
        layout.addWidget(self.genre_combo)

        layout.addWidget(QLabel("Возрастное ограничение:"))
        self.age = QComboBox()
        self.age.addItems([
            "0+", "6+", "12+", "14+",
            "16+", "18+", "Нет"
        ])
        layout.addWidget(self.age)


        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.close_button = QPushButton("Закрыть")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)


        self.save_button.clicked.connect(self.save_film)
        self.close_button.clicked.connect(self.close)


    def save_film(self):
        title = self.title_input.text().strip()
        director = self.director_input.text().strip()
        year = self.year_input.text().strip()
        genre = self.genre_combo.currentText()
        age = self.age.currentText()

        if not title:
            print("Название фильма обязательно!")
            return


        if year and not year.isdigit():
            print("Год должен быть числом!")
            return

        print(f"\nФильм добавлен:")
        print(f"  -Название: {title}")
        print(f"  -Режиссёр: {director}")
        print(f"  -Год: {year if year else 'не указан'}")
        print(f"  -Жанр: {genre}")
        print(f"  -Возрастное ограничение: {age}")

        self.close()
