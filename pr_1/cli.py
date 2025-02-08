from network_client import NetworkClient
def main():
    client = NetworkClient()
    
    while True:
        print("\nДоступные команды:")
        print("1. move <x> <y> <speed>")
        print("2. turn_on")
        print("3. turn_off")
        print("4. get_status")
        print("5. reset")
        print("6. exit")
        
        command = input("\nВведите команду: ")
        if command == "exit":
            print("Выход...")
            break
        elif command.startswith("move"):
            try:
                _, x, y, speed = command.split()
                x, y, speed = int(x), int(y), int(speed)
                print(client.send_command({"cmd": "move", "x": x, "y": y, "speed": speed}))
            except ValueError:
                print("Ошибка: Неизвестный формат. Используйте: move <x> <y> <speed>")
        elif command == "turn_on":
            print(client.send_command({"cmd": "turn_on"}))
        elif command == "turn_off":
            print(client.send_command({"cmd": "turn_off"}))
        elif command == "get_status":
            print(client.send_command({"cmd": "get_status"}))
        elif command == "reset":
            print(client.send_command({"cmd": "reset"}))
        else:
            print("Ошибка: Неизвестная команда")
            
if __name__ == "__main__":
    main()