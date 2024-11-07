# Datastore

## Prerequisites

Create `.env` file with key `ENVIRONMENT`. Set to `DEVELOPMENT` for local, else `PRODUCTION`. Fill other fields in `.env.dev` for local development.

Setup Kafka & Zookeeper (if not setup). In project directory, run: 
```
docker-compose up -d
```

## Quickstart
1. Create virtual environment, activate, and install required packages:

    ```
    python -m venv .venv
    .venv\Scripts\activate
    ```
    or
    ```
    virtualenv .venv
    source .venv/bin/activate
    ```
    then
    ```
    pip install -r requirements.txt
    ```

2. Run consumer & store data to database with:

    ```
    python main.py
    ```