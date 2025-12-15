```
title=More Performant User Sessions
subtitle=Migrating from MySQL to Redis-backed user sessions
tags=security-engineering, user-sessions, redis
hidden=1
```

At work we ran into a situation where lookups for user sessions in our
Flask app became the primary bottleneck for user-facing requests.

Our MySQL database has a `users` table with this schema:
```
user {
    id: uuid
    ...other fields...
    session_id: str | None
}
```

There were obvious limitations with this approach from both a technical and
user experience point of view. Annoyingly, a user could only have a single
session at a time which prevents many user's intended workflows.

Additionally, this meant that our request validation logic required at least
one round trip to the database. Our monolithic application uses a single
database for nearly all production traffic. Our `users` table is heavily utilized
by many parts of the system, meaning potential for lock contention was high, even
for the read-only replica, performance was suboptimal. TODO FIND DATA ON THIS.

Once we became aware of the extent to which this was slowing down production traffic,
we knew we needed to act. It was also convenient to include feature requests for our
user sessions into this same project. Our requirements were: 
- support multiple sessions per user
- allow admin to set global session expiration duration
- store metadata for sessions (ip address, user-agent)
- session storage/validation should not be impacted by DB contention
- all existing sessions should be migrated

We decided to use Redis to solve our problem. Rather than storing session information
directly in the database, we would instead store a JSON object in Redis, key'd by hash
of the user's session e.g.
```
hash(session_id) {
  "id": "123:abc123token...",
  "user_id": 456,
  "domain_id": 123,
  "login_at": "2024-01-15T10:30:00.123456",
  "expires_at": "2024-01-15T11:30:00.123456",
  "user_agent": "Mozilla/5.0...",
  "ip_address": "192.168.1.1"
}
```

This allowes for efficient storage and retrieval of user sessions. It also means that
our performance is predictable and no longer depends on how much read/write traffic
the `users` table is getting.

We're running this on AWS Elasticache. It's probably overkill for our current requirements,
but we are able to manage the costs easily and anticipate significant scaling ahead.