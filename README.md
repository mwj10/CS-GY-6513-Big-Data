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


## Sentiment Analysis

### Dependencies
python == 3.10
### Installation
- `pip install Flask`
- `pip install transformers`
- `pip install torch torchvision torchaudio`

### Activate Virtual Environment
- `. venv/bin/activate`


### To Run the Python Scripts
- To run app.py: with the virtual environment activated, open Terminal and direct to the sentiment-analysis Folder, use the command `flask --app app run`
- To run local.py: with the virtual environment activated, open Terminal and direct to the sentiment-analysis Folder, use the command `python3 local.py`


## Frontend

### How to (without docker)
1. Install dependencies as in `requirements.txt`
2. Update `config.py` according to your settings
3. Seed database using `flask db_seed`
4. Reset seeded database use: `flask db_reset`





