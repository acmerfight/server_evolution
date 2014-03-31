#coding=utf-8

import socket
import select

EOL1 = "\n\n"
EOL2 = "\n\r\n"
response = 'HTTP/1.0 200 OK\r\nDate: Mon, 1 Jan 1996 01:01:01 GMT\r\n'
response += 'Content-Type: text/plain\r\nContent-Length: 13\r\n\r\n'
response += 'Hello, world!'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
    #import ipdb
    #ipdb.set_trace()
    for fileno, event in events:
        if fileno == server.fileno():
            conn, addr = server.accept()
            conn.setblocking(0)
            epoll_fd.register(conn.fileno(), select.EPOLLIN)
            connections[conn.fileno()] = conn
            requests[conn.fileno()] = ""
            responses[conn.fileno()] = response
        elif event & select.EPOLLIN:
            requests[fileno] += connections[fileno].recv(1024)
            if EOL1 in requests[fileno] or EOL2 in requests[fileno]:
                epoll_fd.modify(fileno, select.EPOLLOUT)
        elif event & select.EPOLLOUT:
            bytes_written = connections[fileno].send(responses[fileno])
            responses[fileno] = responses[fileno][bytes_written:]
            if len(responses[fileno]) == 0:
                epoll_fd.modify(fileno, 0)
                connections[fileno].shutdown(socket.SHUT_RDWR)
        elif event & select.EPOLLHUP:
            epoll_fd.unregister(fileno)
            connections[fileno].close()
            del connections[fileno]
