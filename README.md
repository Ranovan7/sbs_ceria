# SBSehati

## Backend

1. Install Dependencies
    - create .venv directory
    - run
    <br/>`# pipenv install`
    - fill .env with format like .env-template

2. Create Database and Admin
    - enter pipenv environment using command
    <br/>`# pipenv shell`
    - create database
    <br/>`# python commands.py create-db`
    - create admin user
    <br/>`# python commands.py create-admin <username>`

3. Run Locally
    - to start server run
    <br/>`# pipenv run uvicorn main:app --reload`
    - to start server using pipenv environment
    <br/>`# pipenv shell`
    <br/>`# uvicorn main:app --reload`
