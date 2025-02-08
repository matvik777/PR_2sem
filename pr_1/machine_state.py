class MachineState:
    def __init__(self, max_x= 500, max_y=500):
        #Конструктор состояния станка
        self.x = 0
        self.y = 0
        self.speed =1
        self.laser_on = False
        self.max_x = max_x
        self.max_y = max_y
    
    def update_position(self, x, y):
        if 0 <= x <= self.max_x and 0 <= y <= self.max_y:
            self.x = x
            self.y = y
        else:
            print(f"Ошибка: Координаты ({x}, {y}) выходят за границы {self.max_x}x{self.max_y}")
            
    def set_speed(self, speed):
        if 1 <= speed <= 10:
            self.speed = speed
            
        else:
            print("Ошибка: Скорость должна быть в диапазоне 1-10")
    
    def toggle_laser(self, state: bool):
        self.laser_on = state
        
    def get_status(self):
        return {
            "x": self.x,
            "y": self.y,
            "speed": self.speed,
            "laser_on": self.laser_on
        }
        
if __name__ == "__main__":
    machine = MachineState()
    
    machine.update_position(100,200)
    print(machine.get_status())
    
    machine.set_speed(5)
    print(machine.get_status())
    
    machine.toggle_laser(True)
    print(machine.get_status())
    
    machine.update_position(600, 0)