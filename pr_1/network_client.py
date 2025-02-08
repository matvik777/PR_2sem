import socket
import json

class NetworkClient:
    def __init__(self, host="127.0.0.1", tcp_port= 5000, upd_port = 5001):
        self.host = host
        self.tcp_port = tcp_port
        self.upd_port = upd_port
    def send_command(self, command):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
                
                tcp_socket.connect((self.host, self.tcp_port))
                tcp_socket.sendall(json.dumps(command).encode("utf-8"))
                response = tcp_socket.recv(1024).decode("utf-8")
                return json.loads(response)
        except Exception as e:
            return {"error": f"Ошибка соединения: {e}"}
    
    def get_status(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as upd_socket:
                upd_socket.sendto(b"get_status", (self.host, self.upd_port))
                data, _ = upd_socket.recvfrom(1024)
                return json.loads(data.decode("utf-8"))
                
        except Exception as e:
            return {"error": f"Ошибка получения статуса: {e}"}
if __name__ == "__main__":
    client = NetworkClient()
    print(f"Клиент создан. Подключение к {client.host}:{client.tcp_port}")
    print(client.send_command({"cmd": "move", "x": 100, "y": 200, "speed": 5}))
    print(client.send_command({"cmd": "turn_on"}))
    print(client.send_command({"cmd": "turn_off"}))
    print(client.send_command({"cmd": "reset"}))

