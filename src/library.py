import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QPushButton, QHBoxLayout, QMessageBox, QHeaderView, QAbstractItemView, QLabel
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from BD import FilmDB


class FilmLibraryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Список фильмов")
        self.resize(950, 600)
        self.db = FilmDB()

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        button_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("Обновить")
        self.delete_btn = QPushButton("Удалить фильм")
        self.watch_btn = QPushButton("Пометить как просмотренный")

        button_layout.addWidget(self.refresh_btn)
        button_layout.addWidget(self.delete_btn)
        button_layout.addWidget(self.watch_btn)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        self.table = QTableWidget(0, 8)
        self.table.setHorizontalHeaderLabels([
            "ID", "Название", "Жанр", "Возраст", "Статус",
            "Добавлен", "Рейтинг", "Обложка"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        main_layout.addWidget(self.table)
        self.resize(1100, 700)

        self.refresh_btn.clicked.connect(self.load_films)
        self.delete_btn.clicked.connect(self.delete_selected_film)
        self.watch_btn.clicked.connect(self.mark_as_watched)

        self.load_films()

    def load_films(self):
        self.table.setRowCount(0)
        films = self.db.get_all_films()

        for row, film in enumerate(films):
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(str(film[0])))
            self.table.setItem(row, 1, QTableWidgetItem(film[1]))
            self.table.setItem(row, 2, QTableWidgetItem(film[2] if film[2] else ""))
            self.table.setItem(row, 3, QTableWidgetItem(film[3] if film[3] else ""))
            self.table.setItem(row, 4, QTableWidgetItem(film[4] if film[4] else "не смотрел"))
            self.table.setItem(row, 5, QTableWidgetItem(film[5] if film[5] else ""))
            rating = str(film[6]) if film[6] is not None else ""
            self.table.setItem(row, 6, QTableWidgetItem(rating))

            cover_filename = film[7]
            cover_label = QLabel()
            cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cover_label.setFixedSize(140, 200)

            if cover_filename:
                cover_path = os.path.join("covers", cover_filename)
                if os.path.exists(cover_path):
                    pixmap = QPixmap(cover_path)
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(
                            130, 190,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        cover_label.setPixmap(scaled_pixmap)
                    else:
                        cover_label.setText("\nбитый")
                else:
                    cover_label.setText("\nнет файла")
            else:
                cover_label.setText("\nнет")

            self.table.setCellWidget(row, 7, cover_label)

        
        self.table.setColumnWidth(0, 50)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 120)
        self.table.setColumnWidth(3, 80)
        self.table.setColumnWidth(4, 120)
        self.table.setColumnWidth(5, 100)
        self.table.setColumnWidth(6, 70)
        self.table.setColumnWidth(7, 150)
        self.table.verticalHeader().setDefaultSectionSize(210)
        def get_selected_film_id(self):
            selected = self.table.selectedItems()
            if not selected:
                QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите фильм из списка.")
                return None
            row = selected[0].row()
            film_id = int(self.table.item(row, 0).text())
            return film_id

    def get_selected_film_id(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            QMessageBox.warning(self, "Внимание", "Пожалуйста, выберите фильм из списка.")
            return None

        row = selected_ranges[0].topRow()
        if row < 0 or row >= self.table.rowCount():
            return None

        id_item = self.table.item(row, 0)
        if not id_item:
            return None

        try:
            film_id = int(id_item.text())
            return film_id
        except (ValueError, AttributeError):
            QMessageBox.critical(self, "Ошибка", "Невозможно определить ID фильма.")
            return None


    def delete_selected_film(self):
        film_id = self.get_selected_film_id()
        if film_id is None:
            return

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            "Вы уверены, что хотите удалить этот фильм?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.db.delete_film(film_id)
                self.load_films()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить фильм:\n{str(e)}")

    def mark_as_watched(self):
        film_id = self.get_selected_film_id()
        if film_id is None:
            return

        row = self.table.selectedItems()[0].row()
        current_status = self.table.item(row, 4).text()

        if current_status == "не смотрел":
            new_status = "смотрел 1 раз"
        elif current_status.startswith("смотрел"):
            parts = current_status.split()
            if len(parts) >= 2 and parts[1].isdigit():
                count = int(parts[1]) + 1
                new_status = f"смотрел {count} раз"
            else:
                new_status = "смотрел 2 раза"
        else:
            new_status = "смотрел 1 раз"

        self.db.update_film_status(film_id, new_status)
        self.load_films()