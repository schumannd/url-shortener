# Tinify URL Service

A URL tinification service powered by [flask](https://github.com/pallets/flask), [postgresql](https://www.postgresql.org/) and [docker](https://github.com/docker)

### To run the service

docker-compose up

navigate to: http://localhost:9999/


### To run tests

docker-compose -f docker-compose.test.yml up


### Process

My solution provides the following required API points:

- /shorten-url
  - accepts a POST parameter 'url'
  - returns a JSON response with key 'code'
- /expand-url
  - accepts a POST parameter 'code'
  - returns a JSON response with key 'url'

Additionally I implemented user facing views that allow the url tinification service to be used. They are reachable under the root route '/' (http://localhost:9999 when running locally)

To generate the corresponding code for each URL I clean it and calculate it's MD5 hash. This hash is then base62 encoded and the first 8 characters are taken as the shortened URL code.

I do manual collision detection and resolution by adding a random alphanumeric character to the URL and recalculating the code up to 10 times.

A code length of 8 provides a hash function value range of 62^8.
As a rule of thumb a hash function with range of size N can hash around sqrt(N) values before running into collisions.
Therefore we can expect to hash aroung 62^4 ~ 14 Million unique URLs before that happens.
The collision resolution should push this number up a few orders of magnitude before the system fails.


The API views are unit tested with the redis store being mocked for testing.

As a final step redis needs to be made persistent as we don't want to lose URL mappings in a case of an unscheduled server restart. For this we enable AOF (Append-only file) persistence.


### Things that should be implemented

- staticfiles hosting
- logging / monitoring
- automated code linting (flake8, isort etc.)
- integration testing
- caching with LRU eviction