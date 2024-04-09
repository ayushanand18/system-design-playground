# Distributed Message Queue System with Apache Kafka (Python)
> This is a common use case where we use Kafka as a Message Queue distributed over many nodes. Each node
> is done on the basis of topics/domain seperation. Maybe say we run 3 seperate queues for 3 different types 
> of messages.

## Design
> I am an engineer but do not over-engineer stuff, (there wasn't any pun intended though :) ). So, I will keep
> things grossly simple and easy to understand, and try to deliver my though process and intuition behind the same.

### Functional Requirements
* Users must be able to submit a new message to the queue, each message containing metadata of the request, priority/category. Once enrolled into the queue, the server should return a unique ID back. A critical requirement here being to maintain idempotency of the message. The ID must be unique and must remain consistent and shared throughout its lifecycle which could be used to uniquely identify it along the journey at any time.
* Now, there must also be consumers of the Message Queue, so a naive idea is that a service must signal a `poll` to fetch next batch of messages, for simplicity without lossofgeneralisation we will take this number as 1, each consumer must request messages one at a time. To implement this, we can have a REST endpoint (although RPC is recommended but since we want to focus only on the Queue, we'd query the message using a `GET` request on browser via an endpoint).

## API Design
* `POST /message/create` - create a new message(s) onto the queue. returns a `UUID(s)` of the message(s) written. payload:
    ```json
    [{
        "timestamp": "Date", // timestamp of creation of message on client
        "title": "String", // title of the message
        "body": "String", // body or data associated with the message could be a JSON String
        "author": "UUID", // the application/service ID of the origin of message
        "topic": "String" // category of the message useful for sharding/polling
    }]
    ```
* `GET /message/poll` - poll the next available request from the Queue. returns a message object.

### Run
Instructions to run a Kafka server on `docker` are as below. The API is a simple FastAPI server with no custom configurations. Use an ASGI (eg `uvicorn`) to run it.
```sh
docker-compose up
```

## References
