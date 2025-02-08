import json
from machine_state import MachineState

class CommandHandler:
    def __init__(self, machine_state):
        self.machine = machine_state
        
    def process_command(self, command_json):
        
        try:
            command = json.loads(command_json)
            cmd_type = command.get("cmd")
            
            print(f" {cmd_type}")
            
            if cmd_type == "move":
                return self.handle_move(command)
            elif cmd_type == "turn_on":
                return self.handle_turn_on()
            elif cmd_type == "turn_off":
                return self.handle_turn_off()
            elif cmd_type == "get_status":
                return self.handle_get_status()
            elif cmd_type == "reset":
                return self.handle_reset()
            else:
                return json.dumps({"error": "Неизвестная команда"})
        except json.JSONDecodeError:
            return json.dumps({"error": "Неверный формат JSON"})
        
    def handle_move(self, command):
        x = command.get("x")
        y = command.get("y")
        speed = command.get("speed", self.machine.speed)
        
        if x is None or y is None:
            return json.dumps({"error": "Отсутствуют координаты"})        
        
        if not (1 <= speed <= 10):
            return json.dumps({"error": "Скорость должна быть от 1 до 10"})
        if not (0<= x <= self.machine.max_x and 0 <= y <= self.machine.max_y):
            return json.dumps({"error": "Координаты выходят за границы поля"})
        self.machine.set_speed(speed)
        self.machine.update_position(x, y)
        
        return json.dumps({"status": "moving", "x": self.machine.x, "y": self.machine.y, "speed": self.machine.speed})
    
    def handle_turn_on(self):
        
        self.machine.toggle_laser(True)
        return json.dumps({"status": "laser_on"})
    
    def handle_turn_off(self):
        self.machine.toggle_laser(False)
        return json.dumps({"status": "laser_off"})
    
    def handle_get_status(self):
        return json.dumps(self.machine.get_status())
    
    def handle_reset(self):
        self.machine.x = 0
        self.machine.y = 0
        self.machine.speed = 1
        self.machine.laser_on = False
        return json.dumps({"status": "reset_done", "x" : 0, "y" : 0, "speed": 0, "laser_on": False})
    
if __name__ == "__main__":
    machine = MachineState()
    handler = CommandHandler(machine)
    
    print(handler.process_command('{"cmd": "move", "x": 100, "y": 200, "speed": 5}'))
    print(handler.process_command('{"cmd": "turn_on"}'))
    print(handler.process_command('{"cmd": "get_status"}'))
    print(handler.process_command('{"cmd": "move", "x": 600, "y": 100}'))  # Ошибка выхода за границы
    