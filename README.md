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

## LSTM
### API Calls
- Training all models: `/train`
- Training specific model (e.g., AAPL): `/train/<string:q_ticker>`
- Prices Data View (i.e., Actual vs Prediction): `/lstm_data_view/<string:q_ticker>`
- inference: `/inference/<string:q_ticker>` OR `/inference/<string:q_ticker>?days=` 

`days` is an optional parameter referring to the number of future days to predict


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



