import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 13))

while True:
    # Отправка сообщения серверу
    message = input("Вы: ")
    client.send(message.encode("utf-8"))

    # Получение ответа от сервера
    data = client.recv(1024)
    if not data:
        break  # Остановка, если сервер отключился
    print("Сервер:", data.decode("utf-8"))

client.close()
