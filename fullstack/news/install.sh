#! /usr/bin/batch

docker compose up -d

python -m venv extract/venv
source extract/venv/bin/activate
pip install -r extract/requirements.txt
deactivate

python -m venv sentiment-analysis/venv
source sentiment-analysis/venv/bin/activate
pip install -r sentiment-analysis/requirements.txt
deactivate

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate

docker-compose down