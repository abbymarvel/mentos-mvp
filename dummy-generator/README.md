# MVP Dummy Real-Time Data Generator

## Quickstart

1. With docker & docker engine installed: 

    ```
    cd broker
    docker-compose up -d
    ```
    then `cd` back to root directory.

2. Setup virtual environment:

    ```
    python -m venv .venv
    .venv\Scripts\activate.bat
    ```
    or
    ```
    virtualenv .venv
    source .venv/bin/activate
    ```

3. Install required packages:

    ```
    pip install -r requirements.txt
    ```

4. As separate processes, run:

    ```
    python main-consumer.py
    ```
    and
    ```
    python main-producer.py
    ```