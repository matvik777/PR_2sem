from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel,QSpinBox
from laser_canvas import LaserCanvas
from network_client import NetworkClient

class LaserApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление лазером")
        self.client = NetworkClient()
        self.canvas = LaserCanvas()
        #обновление статуса
        
        # Поля ввода
        self.x_input = QSpinBox()
        self.y_input = QSpinBox()
        self.speed_input = QSpinBox()
        
        self.x_input.setRange(0, 500)
        self.y_input.setRange(0, 500)
        self.speed_input.setRange(1, 10)
        
        #Подписи
        self.label_x = QLabel("X:")
        self.label_y = QLabel("Y:")
        self.label_speed = QLabel("Скорость:")
        
        #кнопки
        
        self.btn_move = QPushButton("Переместить")
        self.btn_on = QPushButton("Включить лазер")
        self.btn_off = QPushButton("Выключить лазер")
        self.btn_reset = QPushButton("reset")
        self.btn_status = QPushButton("Обновить статус")
        
        #Горищонтальный макет для ввода координат
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label_x)
        input_layout.addWidget(self.x_input)
        input_layout.addWidget(self.label_y)
        input_layout.addWidget(self.y_input)
        input_layout.addWidget(self.label_speed)
        input_layout.addWidget(self.speed_input)

                
        
        
        #вертикальный макет для кнопок
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.btn_move)
        button_layout.addWidget(self.btn_on)
        button_layout.addWidget(self.btn_off)
        button_layout.addWidget(self.btn_reset)
        button_layout.addWidget(self.btn_status)
        
        #Общий макет (сначала ввод, потом кнопки)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.canvas)
        main_layout.addLayout(input_layout)
        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        #Подключаем кнопки к обработчикам
        self.btn_move.clicked.connect(self.send_move_command)
        self.btn_on.clicked.connect(lambda: self.client.send_command({"cmd": "turn_on"}))
        self.btn_off.clicked.connect(lambda: self.client.send_command({"cmd": "turn_off"}))
        self.btn_reset.clicked.connect(lambda: self.client.send_command({"cmd": "reset"}))
        self.btn_status.clicked.connect(self.update_status)
        
    
    def update_status(self):
        status = self.client.get_status()
        print(f"Текущий статус: {status}")           

    def send_move_command(self):
        x = self.x_input.value()
        y = self.y_input.value()
        speed = self.speed_input.value()
        
        self.client.send_command({"cmd": "move", "x": x, "y": y, "speed": speed })
        print(f"Двигаем лазер в {x}, {y}")
        self.canvas.update_laser_position(x, y, speed)
        
        
        

if __name__ == "__main__":
    app = QApplication([])
    window = LaserApp()
    window.show()
    app.exec()