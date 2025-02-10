from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QColor, QPixmap
from PyQt6.QtCore import Qt, QTimer

class LaserCanvas(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(500, 500)
        self.pixmap = QPixmap(500, 500)
        self.pixmap.fill(Qt.GlobalColor.white)
        self.setPixmap(self.pixmap)

        # Начальные координаты лазера (по центру)
        self.laser_x = 250
        self.laser_y = 250

        self.trail = [(self.laser_x, self.laser_y)]
        
        self.draw_trail()
        self.draw_grid()
        self.draw_laser()

        # Список точек для пошагового движения
        self.path = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.move_step)  # Связываем таймер с шагами движения

    def draw_grid(self):
        """Рисует сетку на поле 500x500"""
        painter = QPainter(self.pixmap)
        painter.setPen(QColor(200, 200, 200))
        for i in range(0, 501, 10):
            painter.drawLine(i, 0, i, 500)
            painter.drawLine(0, i, 500, i)

    def draw_trail(self):
        if len(self.trail) < 2:
            return
        painter = QPainter(self.pixmap)
        painter.setPen(QColor(0,0,255))
        
        for i in range(len(self.trail)-1):
            x1 ,y1 = self.trail[i]
            x2, y2 = self.trail[i + 1]
            painter.drawLine(x1, y1, x2 , y1)

    def draw_laser(self):
        """Рисует лазер на текущих координатах"""
        painter = QPainter(self.pixmap)
        painter.setPen(QColor(255, 0, 0))
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(self.laser_x - 3, self.laser_y - 3, 6, 6)
        self.setPixmap(self.pixmap)

    def update_laser_position(self, x, y, speed=1):
        """Запускает движение лазера в указанную точку с заданной скоростью"""
        self.path = self.bresenham_line(self.laser_x, self.laser_y, x, y)
        interval = int(100 / speed)  # Чем выше скорость, тем меньше задержка
        self.timer.start(interval)

    def move_step(self):
        """Перемещает лазер по точкам из списка path"""
        if self.path:
            self.laser_x, self.laser_y = self.path.pop(0)
            self.trail.append((self.laser_x, self.laser_y))
            
            self.pixmap.fill(Qt.GlobalColor.white)  # Очищаем экран
            self.draw_grid()  # Перерисовываем сетку
            self.draw_trail()
            self.draw_laser()  # Рисуем лазер
        else:
            self.timer.stop()  # Останавливаем таймер, когда точки кончились

    def bresenham_line(self, x1, y1, x2, y2):
        """Алгоритм Брезенхэма: возвращает список точек для движения"""
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

        return points
