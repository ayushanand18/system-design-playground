# Geohashing based Proximity Service with Redis (Python)
> This is a common use case where one needs to get nearest locations/places in a fixed distance radius, such as 
> Yelp/Maps etc. A popular way to do that is using geohasing and storing locations in an in-memory store so that 
> search is fast. We will create an API with FastAPI and integrate the store of our choice - Redis.

## Design
> I generally do not over-engineer stuff which I create, so I will keep this stuff as simple as possible, and at the same time jot down all my ideas down here so that it's easy to skim through in the future.

### API Design
The overall design of the API looks very simple, with the following routes:
* `GET` `/api/locations/search/:longitude/:latitude/:distance` - Return nearest locations around [longitude, latitude] within distance. Returns a tuple of `location_id`s
* `POST` `/api/locations/create` - Create a new location at specified point. Returns a `location_id`.
    ```json
    {
        longitude: double,
        latitude: double,
        data: json
    }
    ```
* `GET` `/api/location/:id` - Get information about a specific `location_id` (:id)

### How is data stored in Redis?
Again, we'll only store what's absolutely required. We'll store two keys for a location as:
* (`location:{location_id}`, `geohash`) eg (`location:001`, `4221`
* (`data:{location_id}`, `{data: json, latitude: double, longitude: double}`)

We are storing the geohash and actual metadata on different keys because we want faster searches so there should be
least memory overhead on the geohash index. Also, we would like to rank results very quickly so we might store
geohashes for a longer time and fetch data of locations from Redis or DB. Fetching metadata of location should be
second priority I believe.

## Run
+ Install and run on ubuntu, and run `redis-server`

## References
+ https://redis.com/solutions/use-cases/session-management/