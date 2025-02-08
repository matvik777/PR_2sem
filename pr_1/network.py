import socket
import threading
import json
from machine_state import MachineState
from commands import CommandHandler

class NetworkServer:
    def __init__(self, host="127.0.0.1", tcp_port=5000, udp_port=5001):
        """Инициализация сервера"""
        self.host = host
        self.tcp_port = tcp_port
        self.udp_port = udp_port
        self.machine = MachineState()
        self.command_handler = CommandHandler(self.machine)
        
        # Создаём TCP-сервер
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.bind((self.host, self.tcp_port))
        self.tcp_server.listen(5)

        # Создаём UDP-сервер
        self.udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_server.bind((self.host, self.udp_port))

    def handle_client(self, client_socket):
        """Обработчик TCP-подключений"""
        while True:
            try:
                data = client_socket.recv(1024).decode("utf-8")
                if not data:
                    break

                response = self.command_handler.process_command(data)
                client_socket.send(response.encode("utf-8"))

            except ConnectionResetError:
                print("Клиент отключился")
                break

        client_socket.close()

    def tcp_listener(self):
        """Запуск TCP-сервера"""
        print(f"TCP-сервер запущен на {self.host}:{self.tcp_port}")
        while True:
            client_socket, addr = self.tcp_server.accept()
            print(f"Подключение от {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def udp_sender(self):
        """Отправка текущего состояния по UDP"""
        print(f"UDP-сервер запущен на {self.host}:{self.udp_port}")
        while True:
            data, addr = self.udp_server.recvfrom(1024)
            if data.decode("utf-8") == "get_status":
                status = self.machine.get_status()
                self.udp_server.sendto(json.dumps(status).encode("utf-8"), addr)

    def start(self):
        """Запуск TCP и UDP серверов в отдельных потоках"""
        tcp_thread = threading.Thread(target=self.tcp_listener)
        udp_thread = threading.Thread(target=self.udp_sender)

        tcp_thread.start()
        udp_thread.start()

        tcp_thread.join()
        udp_thread.join()

if __name__ == "__main__":
    server = NetworkServer()
    server.start()
