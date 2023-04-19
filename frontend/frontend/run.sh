#! /bin/bash

flask db_reset
flask db_seed
flask run