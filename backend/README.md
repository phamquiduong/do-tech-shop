# DO Tech Shop
> Development by Django Rest Framework

<br>

## Prepare for server
### Python environment
#### Step 1: Get Python
> **Note**: Recommended version of Python is `3.12`

* You can get and install Python from [python.org](https://www.python.org/)
* In Windows OS, you can get Python in [Windows store](https://apps.microsoft.com/search?query=python)


#### Step 2: Install Python packages
```bash
pip install -r requirements.txt
```

<br>

### PostgreSQL database
#### Step 1: Get Docker desktop
* Visit [docker.com](https://www.docker.com/products/docker-desktop/) get and install docker desktop

> **Note:** You need to install WSL2 on Windows before installing Docker Desktop

#### Step 2: Change directory to docker folder
```bash
cd docker
```

#### Step 3: Prepare environment variables
Copy `.env.example` file to `.env` file
```bash
cp .env.example .env
```
> Then change value of variables

#### Step 4: Start database server
```bash
docker-compose up -d
```

<br>

## Migrate database
```bash
.\migrate.bat
```

<br>

## Start server
Run bash start server
```bash
.\start_server.bat
```

> **Note:** To stop server press `Ctrl-C`

#### Now you can access the server documentation at http://localhost:8000/docs/swagger/
