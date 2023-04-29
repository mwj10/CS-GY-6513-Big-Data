# Group 5 - Big Data Project Spring '23

## Contents
- [Prerequisites](#prerequisites)
- [System Requirements](#system-requirements)
    - [Minimum](#minimum)
    - [Recommeded](#recommeded)
- [How To Use](#how-to-use)
    - [Running a Docker](#running-a-docker)
    - [Testing the Docker](#testing-the-docker)
    - [Seeding Databases](#seeding-databases)
    - [Stopping the Docker](#running-a-docker)
- [Test Run](#test-run)

## Prerequisites
- [Docker](https://docs.docker.com/engine/install/)

## System Requirements
### Minimum
- 40GB docker virtual disk space
- 6GB docker memory

### Recommeded
- 60GB docker virtual disk space
- 12GB docker memory

## How To Use
### Running a Docker
- Use the following command*\** to start a docker.
- **Caution**: The first time you run the following command. It needs `10 minutes` to run.
```
$docker compose up -d
```
- *\**`-d` means we want to launch the docker in a background.
- You will see a bunch of install messages. Wait until you see the following statement saying containers are started. 
```
[+] Running 8/8
 - Container lstm-postgres                  Started  1.2s
 - Container frontend-mongo                 Started  0.6s
 - Container news-sentiment-analysis-mongo  Started  1.2s
 - Container news-extract-mongo             Started  1.2s
 - Container lstm-flask                     Started  1.7s
 - Container news-sentiment-analysis-flask  Started  2.1s
 - Container frontend-flask                 Started  1.5s
 - Container news-extract-flask             Started  2.7s
```
- After `docker compose up -d` was completed, you can use the following command to check if all of the eight containers are still running.
```
docker ps
```
![docker-ps-result](assets/docker_ps.jpg)

### Testing the Docker
- Go to http://localhost:8001, you should see
```
"result": "News extracting service is running."
```
- Go to http://localhost:8002, you should see
```
"message": "Sentiment Analysis service is running."
```
- Go to http://localhost:8003, you should see
```
"message": "LSTM service is running."
```
- Go to http://localhost:8004, you should see
>![landing-page](assets/landing_page.jpg)

### Seeding Databases
- **Caution**: make sure that all containers are running. 
- Launch http://localhost:8001/seed, wait for a few seconds and you should see:
```
"message": "News database has been seeded"
```
- **Caution**: the following command needs **20 minutes** to complete.
- Launch http://localhost:8003/seed, wait for **20 minutes** and you should see:
```
"message": "News database has been seeded"
```
### Stopping the Docker
- To stop the docker run:
```
docker compose down
```
- You should see:
```
[+] Stopping 8/8
 - Container lstm-postgres                  Stopped  1.2s
 - Container frontend-mongo                 Stopped  0.6s
 - Container news-sentiment-analysis-mongo  Stopped  1.2s
 - Container news-extract-mongo             Stopped  1.2s
 - Container lstm-flask                     Stopped  1.7s
 - Container news-sentiment-analysis-flask  Stopped  2.1s
 - Container frontend-flask                 Stopped  1.5s
 - Container news-extract-flask             Stopped  2.7s
```
## Test Run
- Simply to go http://localhost:8004 and navigate through the site.
- You can directly go to each quote by specify their symbol, e.g., http://localhost:8004/quote/AAPL (Currently, we only support DOW30).
