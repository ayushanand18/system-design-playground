# Redis
A distributed and performant Key-Value Store pupoular for caching.

# Instructions
I am running an Ubuntu VM, so I'll pick up instructions for Linux to Install Redis first.
+ ```shell
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

    sudo apt-get update
    sudo apt-get install redis
    ``` 
+ After I am done installing Redis on my machine, let me run the stack using Docker.
    ```shell
    docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest
    ```
+ Now go over to the 8001 port for the RedisInsight, and you will be able to a dashboard to manage Redis, store keys, see server load and many other actions.
+ You can create new key-value data in Redis either using GUI on Redis Insight or using CLI or Redis Clients for Python/GO/others.
