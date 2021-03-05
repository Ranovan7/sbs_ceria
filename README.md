# SBSehati

## Backend

1. Install Dependencies
    - create .venv directory
    - run
    <br/>`# pipenv install`
    - create SECRET_KEY using
    <br/>`# openssl rand -hex 32`
    - duplicate .env-template to .env

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

## FrontEnd

1. go to frontend directory
    <br/>`# cd ./frontend/`

2. Install Dependencies
    <br/>`# npm install`

3. Run Development
    <br/>`# npm run dev`
