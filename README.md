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

## FrontEnd

1. go to frontend directory
    <br/>`# cd ./frontend/`

2. Install Dependencies
    <br/>`# npm install`

3. Copy frontend/static/config_template.json to frontend/static/config.json

4. Run Development
    <br/>`# npm run dev -- --open`

5. Build FrontEnd Files
    <br/>`# npm run build`

6. Once Built, running backend/FastAPI will serve both frontend (/<page>) and api (/api/<service>) endpoint, so running only
    </br>`# pipenv run uvicorn main:app --reload`</br>
    will run the complete app
