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
- Complete [`.env`](/config/.env) file (cf. [Configuration](#configuration)) and rename it `.env.dev` or `.env.prod` depending on the environment you want to launch.
- Place yourself in parent directory `/gobelin` (where there is docker-compose file).
- Execute one of these commands:
    ```sh
    docker-compose -f docker-compose.dev.yml --env-file config/.env.dev up --build  # Command for development environment
    ```
    ```sh
    docker-compose -f docker-compose.prod.yml --env-file config/.env.prod up --build  # Command for production environment
    ```
- Execute one of these commands to remove running containers:
    ```sh
    docker-compose -f docker-compose.dev.yml down  # Command for development environment
    ```
    ```sh
    docker-compose -f docker-compose.prod.yml down  # Command for production environment
    ```


## Project details
#### Current architecture
Gobelin is modular and containerized, all containers are manage by docker-compose. The containers are :
- db : postgres database store in docker volume.
- [liquibase](/db/migrations/) : migration manager.
- [db-access](/db-access/README.md) : DAO layer to manage database connection pool and requests to database.
- [data-pipeline](/data-pipeline/README.md) : ETL layer to collect, preprocess and store new data.
#### Technologies
- Docker
- Postgresql
- Liquibase
- SQLAlchemy (soon)
- Pandas (soon)
- Numpy (soon)
#### Nomenclature
- kebab-case : folders, files, url
- snake_case : functions, variables
- UPPERCASE : constants
- PascalCase : class

## Configuration
#### .env
- `VERSION` : to update at each merge.
- `LOG_LEVEL` :
- `POSTGRES_USER` : user id.
- `POSTGRES_PASSWORD` : user password.
- `POSTGRES_DB` : database name.
- `POSTGRES_PORT` : host computer port exposed.
- `DATABASE_URL` : database access url.
#### Database
Data schema is defined in `/db/migrations`.
####  Logs
Logs are configured in the `/src` folders of each module.


> ## Backlog :
> - Changelog section in `README.md`.
> - Complete `README.md` throughout the project.
> - Create data schema using Liquibase.
> - Complete DAO layer.
> - Create DAO unit and integration tests.
> - Complete ETL layer.
>
>   ....