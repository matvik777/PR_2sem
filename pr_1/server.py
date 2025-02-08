import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 13))
server.listen()

print("Сервер запущен. Ожидание подключения...")
user, addr = server.accept()
print(f"Подключение установлено: {addr}")

while True:
    # Получение сообщения от клиента
    data = user.recv(1024)
    if not data:
        break  # Остановка, если клиент отключился
    print("Клиент:", data.decode("utf-8"))

    # Отправка сообщения клиенту
    message = input("Вы: ")
    user.send(message.encode("utf-8"))

user.close()
server.close()
