# python_ssh_tunnel
Ports and sockets forwarding tunnel over SSH with systems SSH client.

You can use it like this to tunnel MySQL over SSH with TCP ports:
 ```python
import pymysql
from ssh_tunnel import create_ssh_tunnel

with create_ssh_tunnel(
    hostname="my_db_server.com",
    local_socket="127.0.0.1:3307",
    remote_socket="127.0.0.1:3306",
) as tunnel:
    with pymysql.connect(
        host="127.0.0.1",
        port=3307,
        user="user",
        password="password",
        database="database",
        cursorclass=pymysql.cursors.DictCursor,
    ) as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `table`"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
```

or you can use it with unix sockets:
 ```python
import pymysql
from ssh_tunnel import create_ssh_tunnel

with create_ssh_tunnel(
    hostname="my_db_server.com",
    local_socket="/tmp/mysql-local.sock",
    remote_socket="/tmp/mysql.sock",
) as tunnel:
    with pymysql.connect(
        unix_socket="/tmp/mysql-local.sock",
        user="user",
        password="password",
        database="database",
        cursorclass=pymysql.cursors.DictCursor,
    ) as connection:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM `table`"
            cursor.execute(sql)
            result = cursor.fetchone()
            print(result)
```
