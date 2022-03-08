# ea-memcached16 EA4 container based package

This package sets up a user specific memcached container.

## Using it

Any thing that can talk to memcached can use it via the unix socket `~/<CONTAINER_NAME>/memcache.sock`.

A quick example would be:

**Note**: to keep it simple this example assumes you:
   1. You have `socat` installed
   2. You have this shell function:
      ```
      hello-socket()
      {
          echo "Hello Socket ($$)" | socat -v UNIX-CONNECT:$1 STDIN
      }
      ```
   3. The container name is `ea-memcached16.user1.01`

As the user:

```
user1$ hello-socket /home/user1/ea-memcached16.user1.01/memcache.sock
< 2022/03/08 15:25:40.185992  length=22 from=0 to=21
Hello Socket (707172)
user1$

```

As another user:

```
user2$ hello-socket /home/user1/ea-memcached16.user1.01/memcache.sock
2022/03/08 15:26:55 socat[711950] E connect(5, AF=1 "/home/user1/ea-memcached16.user1.01/memcache.sock", 56): Permission denied
user2$
```

## Security

This is secure overall because the unix socket is owned by the user so no other non-root users can get/set data in this memcached.

You can add a layer of separation on the app level by installing it more than once to have different containers so that individual apps can have their own memcached.
