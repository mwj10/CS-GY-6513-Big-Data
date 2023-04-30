#! /bin/bash
# cd ./frontend
flask db_reset
flask db_seed
flask run