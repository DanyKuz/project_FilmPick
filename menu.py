import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget

class MenuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FilmPick Menu")
        self.setGeometry(100, 100, 300, 200)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        self.new_film = QPushButton("Новый фильм")
        self.library = QPushButton("Список фильмов")
        self.random_pick = QPushButton("Случайный фильм")
        
        layout.addWidget(self.new_film)
        layout.addWidget(self.library)
        layout.addWidget(self.random_pick)
        
        self.new_film.clicked.connect(self.show_new_film)
        self.library.clicked.connect(self.show_library)
        self.random_pick.clicked.connect(self.show_random_film)
    
    def show_new_film(self):
        print("Создаю новый фильм")
    
    def show_library(self):
        print("Показываю список фильмов")

    def show_random_film(self):
        print("Показываю случайный фильм")
    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MenuWindow()
    window.show()
    sys.exit(app.exec())