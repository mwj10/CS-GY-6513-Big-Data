# Big Data Project Spring '23
## Setup
### Install Dokcer
https://docs.docker.com/engine/install/

### Download and Run Postgres Docker Container
- `docker pull postgres`
- `docker run --name postgres -e POSTGRES_PASSWORD=123 -d postgres`

### Download and Run MangoDB Docker Container
- `docker pull mongo`
- `docker run -d -p 27017-27019:27017-27019 --name mango mongo`
