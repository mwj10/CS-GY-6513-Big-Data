#! /usr/bin/batch

docker compose up -d

python -m venv news/extract/venv
source news/extract/venv/bin/activate
pip install -r news/extract/requirements.txt
deactivate

python -m venv news/sentiment-analysis/venv
source news/sentiment-analysis/venv/bin/activate
pip install -r news/sentiment-analysis/requirements.txt
deactivate

python -m venv news/venv
source news/venv/bin/activate
pip install -r news/requirements.txt
deactivate

python -m venv lstm/venv
source lstm/venv/bin/activate
pip install -r lstm/requirements.txt
deactivate

docker-compose down