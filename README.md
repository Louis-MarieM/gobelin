# Gobelin - Financial analysis tool
It is a financial analysis module based on ML that collects and processes data. The financial objects targeted are stocks, ETFs and cryptocurrencies.


## Goal
The main goal of this project is to be an introduction to ML.

That aside, initially Gobelin will have to provide market metrics as well as short and long term investment advices.
Gobelin will collect data from several sources (libraries, APIs, etc), preprocess them then store them, and finally analyze this data by different methods in order to establish the best investment strategy.


## Prerequisites to installation
- Use Windows or Linux distribution.
- Install [Docker](https://docs.docker.com/get-started/get-docker/) (version 26.1.1 worked).

## Installation
#### Run application
- Complete the file [`.env`](/config/.env) (cf. [Configuration](#configuration)) and rename it `.env.dev` or `.env.prod` depending on the environment you want to launch.
- Place yourself in parent directory `/gobelin` (where there is docker-compose file).
- Run one of these commands:
    ```sh
    # Command for development environment
    docker-compose -f docker-compose.dev.yml --env-file config/.env.dev up --build
    ```
    ```sh
    # Command for production environment
    docker-compose -f docker-compose.prod.yml --env-file config/.env.prod up --build
    ```
- Run one of these commands to remove running containers:
    ```sh
    # Command for development environment
    docker-compose -f docker-compose.dev.yml down
    ```
    ```sh
    # Command for production environment
    docker-compose -f docker-compose.prod.yml down
    ```
#### Run tests
- Activate tests in the file [`.env`](/config/.env) (cf. [Configuration](#configuration)).
- To test every modules, run docker-compose as usual.
- To test a specific module, run instead :
    ```sh
    docker-compose -f <docker-compose file> --env-file config/<.env file> up <module-name>
    # ex: docker-compose -f docker-compose.dev.yml --env-file config/.env.dev up db-access
    ```
#### Debug mode
- In docker-compose file used, replace command line of your service by debugpy run :
    ```sh
    python -m debugpy --listen 0.0.0.0:5678 --wait-for-client <command line>
    # ex: python -m debugpy --listen 0.0.0.0:5678 --wait-for-client src/main/main.py
    ```
- In the same service, expose port 5678:
    ```xml
    ports:
      - <unused host port>:5678
      <!-- ex: 5678:5678 -->
    ```
    > [!IMPORTANT] 
    > For each service to be launched in debug mode, a different host port must be used.

- Run docker-compose as usual, then the process waits for a connection to run final command line.
- If you are using VSCode, create a `launch.json` file in Run and Debug section like the following one (replace `localRoot` and `remoteRoot` with the correct paths).
    This launch.json configures debug mode for db-access module and data-pipeline module, if an warning is raise due to mapping error, it may be a missing pathMapping in the configuration :
    ```json
    {
        "version": "0.2.0",
        "configurations": [
            {
                "name": "Debug db-access",
                "type": "debugpy",
                "request": "attach",
                "connect": {
                    "host": "localhost",
                    "port": 5678
                },
                "pathMappings": [
                    {
                        "localRoot": "${workspaceFolder}/db-access/src",
                        "remoteRoot": "/db-access/src"
                    },
                    {
                        "localRoot": "${workspaceFolder}/db-access/config",
                        "remoteRoot": "/db-access/config"
                    },
                    {
                        "localRoot": "${workspaceFolder}/data-pipeline/src",
                        "remoteRoot": "/data-pipeline/src"
                    }
                ],
                "justMyCode": true
            },
            {
            "name": "Debug data-pipeline",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5679
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}/db-access/src",
                    "remoteRoot": "/db-access/src"
                },
                {
                "localRoot": "${workspaceFolder}/data-pipeline/src",
                "remoteRoot": "/data-pipeline/src"
                }
            ],
            "justMyCode": true
            }
        ]
    }
    ```
- Then play start debugging button (F5) and command line will be executed. Your placed breakpoints will be triggered.


## Project details
#### Current architecture
Gobelin is modular and containerized, all containers are manage by docker-compose. The containers are :
- db : postgres database store in docker volume.
- [liquibase](/db/migrations/) : migration manager.
- [db-access](/db-access/README.md) : DAO layer to manage database connection pool and requests to database.
    Compiled as a package and usable by others modules.
- [data-pipeline](/data-pipeline/README.md) : ETL layer to collect, preprocess and store new data.
#### Technologies
- Docker
- Postgresql
- Liquibase
- SQLAlchemy
- Pandas (soon)
- Pytest
- Numpy (soon)
#### Nomenclature
- kebab-case : folders, files, url
- snake_case : functions, variables
- UPPERCASE : constants
- PascalCase : class

## Configuration
#### .env
- `VERSION` : to update at each merge.
- `LOG_LEVEL` : log level of every module.
- `POSTGRES_USER` : user id.
- `POSTGRES_PASSWORD` : user password.
- `POSTGRES_DB` : database name.
- `POSTGRES_PORT` : host computer port exposed.
- `DATABASE_URL_JDBC` : database access jdbc url (used by liquibase).
- `DATABASE_URL_SQLALCHEMY` : database acces url for sqlalchemy.
- `POOL_SIZE` : controls number of connections to maintain in the pool.
- `MAX_OVERFLOW` : number of maximum connections allowed beyond the pool size.
- `POOL_TIMEOUT` : timeout before failing to acquire a connection.
- `POOL_RECYCLE` : recycles connections after this many seconds.
- `ACTIVE_TESTS` : boolean to enable or disable tests of every module during deployment.

#### Database
Data schema is defined in [`/db/migrations`](/db/migrations/). All `changelog-master` files include other files and subfolders content.

To connect to the database with a SQL client (ex: DBeaver) apply this connection configuration using the file [`.env`](/config/.env) :
```sh
url : `DATABASE_URL_JDBC` with localhost as host and without identifiers (ex: jdbc:postgresql://localhost:5432/mydb)
user : `POSTGRES_USER`
password : `POSTGRES_PASSWORD`
```
Make sure 5432 port is unused before running the container.
####  Logs
Logs are configured in the `/config` folders of each module.

> ## Backlog :
> - Complete ETL layer.
>
>   ....

> ## Changelog :
> #### v0.2.0 :
> - Updated Prices table id type from bigserial to serial.
> - Updated configuration for debug mode and testing.
> - Initialization DAO layer with unit tests.
> #### v0.1.0 :
> - Initialization Docker project.
> - Initialization data schema: Markets, Assets, Prices tables.