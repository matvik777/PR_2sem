from PyQt6.QtWidgets import QApplication
from laser_canvas import LaserCanvas

app = QApplication([])
canvas = LaserCanvas()
canvas.show()
app.exec()
