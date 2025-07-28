# Taxi simulator
 
## App consist of:
- Dispatcher (`dispatcher/`) - service which handler users, and taxis requests and store in the DB.
This service also use alembic for migrations.
- Postgres - with tables taxis, trips
- Taxi simulator (`taxi_simulator/`) - in docker container, simulate pickup and drop off clients
- Shell client (`client simulator/`)  - which simulate client request

## How to setup and run app
* Follow the makefile for lal possibilities
1. Init .env file base on template:
```commandline
make init-env
```
2. Fill gaps in .env file, example values below:
```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db/dispatcher_db
DISPATCHER_HOST=0.0.0.0
DISPATCHER_PORT=8080
```
3. Run app (dispatcher + taxi simulators)
```commandline
make run
```
4. Simulate client/user trip request
```commandline
pip install poetry 
poetry install
make client-request
```
5. Track logs with commands below
- dispatcher logs
```commandline
make dispatcher-logs
```
- taxi client logs
```commandline
docker logs -f --tail 100 taxi-001
docker logs -f --tail 100 taxi-002
```
## Wish TODO
- If I find time, I am going to add: 
  - add unit tests for service layer with repository layer mocks
  - add integration tests for repository layer with real DB connection between containers
  - add integration tests for endpoints with real whole flow from endpoint,
  to the DB query and back again to response.
  - Add async DB connection and async and awaited repository methods.

#### *During run, include that I used Windows (unnecessary) for it, so maybe it happen that you need to remove `\r`
* run ``sed -i 's/\r//' ./dispatcher/start.sh`` if needed.