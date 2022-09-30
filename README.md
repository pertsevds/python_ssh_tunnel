# python_ssh_tunnel
Ports and sockets forwarding tunnel over SSH with systems SSH client.

You can use it as:
 ```python
with create_ssh_tunnel(hostname="my_db_server.com", local_socket="127.0.0.1:3307", remote_socket="127.0.0.1:3306") as tunnel:
    connect_to_mysql(host="127.0.0.1", port=3307)
```

or you can use it with unix sockets:
 ```python
 with create_ssh_tunnel(hostname="my_db_server.com", local_socket="/tmp/mysql-local.sock", remote_socket="/tmp/mysql.sock") as tunnel:
    connect_to_mysql(unix_socket="/tmp/mysql-local.sock")
```
