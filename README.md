# BDAssignment1
## Requirements
- Docker
    - Install guide [here](https://docs.docker.com/engine/install/)
    
## Running
### 1. Stop Mongod Service (Daemon)
- Only applies if you are currently running MongoDB on your local machine.
- Ensure that no local MongoDB service (mongod) is running.
- Differ by OS or if using Docker Desktop

On linux:

```shell
sudo systemctl stop mongod 
```

### 2. Start Docker Service (Daemon)
- This process differs depending on OS
    - Or if you are using Docker Desktop
- Consult the [install guide](https://docs.docker.com/engine/install/).

On Linux:

```shell
sudo systemctl start docker
```


### 3. Launch the container
- First, cd into the root of the project directory
- Run the following command:

```shell
docker compose up -d
```

## Using
### Dependencies
- If all went to plan, the docker container will have automatically:
    - Installed all dependencies
    - Launched the mongod service
    - Seeded the database
    - Launched the webapp

### Mongo Shell
- Accessing the mongoshell via `mongosh` will launch MongoBD shell within the container

### Open the WebApp
- The WebApp will running at [localhost:3000](http:localhost:3000)
