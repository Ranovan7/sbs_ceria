# SBSehati

1. Install Dependencies
    - create .venv directory
    - run
    `pipenv install`
    - duplicate .env-template to .env

2. Create Database and Admin
    - enter pipenv environment using command
    `pipenv shell`
    - create database
    `python commands.py create-db`
    - create admin user
    `python commands.py create-admin <username>`

3. Run Locally
    - to start server run
    `pipenv run uvicorn main:app --reload`
    - to start server using pipenv environment
    `pipenv shell`
    `uvicorn main:app --reload`
