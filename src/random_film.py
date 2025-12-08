import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QPushButton, QMessageBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from BD import FilmDB


class RandomFilmWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Случайный фильм")
        self.setGeometry(250, 250, 600, 500)
        self.db = FilmDB()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        layout.addWidget(QLabel("Выберите жанр (или оставьте 'Любой'):"))
        self.genre_combo = QComboBox()
        self.genre_combo.addItem("Любой")
        self.genre_combo.addItems([
            "Боевик", "Драма", "Комедия", "Фантастика",
            "Ужасы", "Мультфильм", "Детектив", "Фэнтези", "Триллер", "История"
        ])
        layout.addWidget(self.genre_combo)

        self.pick_button = QPushButton("Выбрать случайный фильм")
        self.pick_button.clicked.connect(self.pick_random_film)
        layout.addWidget(self.pick_button)

        self.info_layout = QVBoxLayout()
        self.title_label = QLabel("<i>Фильм ещё не выбран</i>")
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.title_label.setWordWrap(True)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.details_label = QLabel()
        self.details_label.setWordWrap(True)
        self.details_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.cover_label = QLabel()
        self.cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.cover_label.setFixedSize(200, 300)
        self.cover_label.setStyleSheet("border: 1px solid #ccc;")

        self.info_layout.addWidget(self.title_label)
        self.info_layout.addWidget(self.details_label)
        self.info_layout.addWidget(self.cover_label, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addLayout(self.info_layout)

        self.retry_button = QPushButton("Выбрать другой")
        self.retry_button.clicked.connect(self.pick_random_film)
        self.retry_button.setEnabled(False)
        layout.addWidget(self.retry_button)
        self.retry_button.hide()

        self.film_displayed = False

    def pick_random_film(self):
        selected_genre = self.genre_combo.currentText()
        category = None if selected_genre == "Любой" else selected_genre

        film = self.db.get_random_film_by_category(category)

        if not film:
            QMessageBox.information(
                self,
                "Нет фильмов",
                f"В базе нет фильмов {'вообще' if category is None else f'в жанре «{category}»'}."
            )
            self.clear_display()
            self.retry_button.setEnabled(False)
            return

        film_id, title, cat, age, status, date_added, rating, cover = film

        details = f"<b>Жанр:</b> {cat or '—'}<br>"
        details += f"<b>Возраст:</b> {age or '—'}<br>"
        details += f"<b>Статус:</b> {status or 'не смотрел'}<br>"
        details += f"<b>Дата добавления:</b> {date_added}<br>"
        details += f"<b>Рейтинг:</b> {rating if rating is not None else '—'} / 10"

        self.title_label.setText(title)
        self.details_label.setText(details)

        self.cover_label.clear()
        if cover:
            cover_path = os.path.join("data/covers", cover)
            if os.path.exists(cover_path):
                pixmap = QPixmap(cover_path)
                if not pixmap.isNull():
                    scaled = pixmap.scaled(
                        190, 280,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    self.cover_label.setPixmap(scaled)
                else:
                    self.cover_label.setText("Обложка\nбитая")
            else:
                self.cover_label.setText("Файл\nне найден")
        else:
            self.cover_label.setText("Без\nобложки")

        self.film_displayed = True
        self.retry_button.setEnabled(True)

    def clear_display(self):
        self.title_label.setText("<i>Фильм ещё не выбран</i>")
        self.details_label.clear()
        self.cover_label.clear()
        self.cover_label.setText("")
        self.film_displayed = False