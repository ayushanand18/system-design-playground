# Session Management with Redis (Python)
> It creates a simple FastAPI server that manages sessions of users using Redis.

## Design
> I generally do not over-engineer stuff which I create, so I will keep this stuff as simple as possible, and at the same time jot down all my ideas down here so that it's easy to skim through in the future.

The overall design of the api looks very simple. Whenever a user signs in then we create a session and update the user's details. Note that by session management we mean that our use case is to "manage only one concurrent session per user". So, a user is not allowed to create multiple sessions at the same point of time.

To do this, we simply store the `session_id` for each user in the cache. Now, for each session also we'll store some session details for example the `last_active_time`, `creation_time`, and `user_id`. So with each session, we store everything we must know around it, and we'll have TTL policy around sessions too, so that expired sessions get erased.

Now, what will happen if the `session_id` of a particular `user_id` is expired?
* According to the TTL policy, the session (`session_id`) will be deleted.
* So, whenever the user tries to login again i.e. wehave to generate a new `session_id` for the `user_id` there we will check the prevous session exists or not, if it exists then we'll delete the old `session_id` from the cache and assign a new `session_id` to the user. this way whenever the user wants to do some operations with the old `session_id`, the internal APIs when doing a `GET_SESSION` shall result into an error that "the session does not exists" and eventually log the user out.
* If however, the old session has expired, then we simply clean it up.

There is another thing that we should keep in mind, that `user_id` also have a TTL polic with them. This will be 1.5x of the `session_id` TTL, so that a user can refresh sessions easily while maintaining that the cluster is not overloadedwith stale `user_id` records.

## Run
+ Install and run on ubuntu, and run `redis-server`

## References
+ https://redis.com/solutions/use-cases/session-management/