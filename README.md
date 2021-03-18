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

## Frontend

1. go to spa directory
    <br/>`# cd ./spa/`

2. Install Dependencies
    <br/>`/spa # npm install`

3. Copy spa/.env-template to spa/.env

4. Run Development
    <br/>`/spa # npm run dev`

5. Build FrontEnd/SPA Static Files
    <br/>`/spa # npx sapper export`

6. Once Built, running backend/FastAPI will serve both frontend (/<page>) and api (/api/<service>) endpoint, so running code below on development
    </br>`# pipenv run uvicorn main:app --reload`</br>
    will run the complete app
