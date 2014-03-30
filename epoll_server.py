#coding=utf-8

import socket
import select

response = 'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += 'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += 'Hello, world!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
server.bind(('', 8080))
server.listen(10)
server.setblocking(0)

epoll_fd = select.epoll()
epoll_fd.register(server.fileno(), select.EPOLLIN)

connections = {}
requests = {}
responses = {}

while True:
    events = epoll_fd.poll()
    for fileno, event in events:
        if fileno == server.fileno:
            conn, addr = server.accept()
            conn.setblocking(0)
            epoll_fd.register(conn.fileno(), select.EPOLLIN)
            requests[conn.fileno] = ""
            responses[conn.fileno] = response
        elif:
            pass
