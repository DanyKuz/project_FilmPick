
import os
import re
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt
from BD import FilmDB


class NewFilm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Добавить новый фильм")
        self.setGeometry(200, 200, 400, 450)
        self.db = FilmDB()
        self.selected_cover = None

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel("Название фильма: *"))
        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Жанр:"))
        self.genre_combo = QComboBox()
        self.genre_combo.addItems([
            "", "Боевик", "Драма", "Комедия", "Фантастика",
            "Ужасы", "Мультфильм", "Детектив", "Фэнтези", "Триллер", "История"
        ])
        layout.addWidget(self.genre_combo)

        layout.addWidget(QLabel("Возрастное ограничение:"))
        self.age_combo = QComboBox()
        self.age_combo.addItems(["", "0+", "6+", "12+", "14+", "16+", "18+"])
        layout.addWidget(self.age_combo)

        layout.addWidget(QLabel("Рейтинг (0–10):"))
        self.rating_input = QLineEdit()
        self.rating_input.setPlaceholderText("Например: 8")
        layout.addWidget(self.rating_input)

        layout.addWidget(QLabel("Обложка:"))
        cover_layout = QHBoxLayout()
        self.cover_path_label = QLabel("Не выбрана")
        self.cover_path_label.setWordWrap(True)
        self.choose_cover_button = QPushButton("Выбрать файл...")
        self.choose_cover_button.clicked.connect(self.select_cover)
        cover_layout.addWidget(self.choose_cover_button)
        cover_layout.addWidget(self.cover_path_label)
        layout.addLayout(cover_layout)

        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.close_button = QPushButton("Отмена")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.close_button)
        layout.addLayout(button_layout)

        self.save_button.clicked.connect(self.save_film)
        self.close_button.clicked.connect(self.close)

    def select_cover(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите обложку фильма",
            "",
            "Изображения (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            filename = os.path.basename(file_path)
            self.selected_cover = filename
            self.cover_path_label.setText(filename)

            os.makedirs("data/save_covers", exist_ok=True)

            dest_path = os.path.join("data/save_covers", filename)
            try:
                with open(file_path, "rb") as src, open(dest_path, "wb") as dst:
                    dst.write(src.read())
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить обложку:\n{e}")
                self.selected_cover = None
                self.cover_path_label.setText("Ошибка загрузки")

    def save_film(self):
        title = self.title_input.text().strip()
        if not title:
            QMessageBox.warning(self, "Ошибка", "Название фильма обязательно!")
            return

        category = self.genre_combo.currentText() or None
        age_restriction = self.age_combo.currentText() or None
        rating_text = self.rating_input.text().strip()

        rating = None
        if rating_text:
            if not rating_text.isdigit():
                QMessageBox.warning(self, "Ошибка", "Рейтинг должен быть целым числом от 0 до 10.")
                return
            rating = int(rating_text)
            if not (0 <= rating <= 10):
                QMessageBox.warning(self, "Ошибка", "Рейтинг должен быть от 0 до 10.")
                return

        try:
            film_id = self.db.add_film(
                title=title,
                category=category,
                age_restriction=age_restriction,
                rating=rating,
                cover=self.selected_cover
            )
            QMessageBox.information(self, "Успешно", f"Фильм «{title}» добавлен (ID: {film_id})")
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось сохранить фильм:\n{e}")