# DO Tech Shop
> Development by FastAPI

<br>

## Prepare for server
#### Install Python
> **Note**: Recommended version of Python is `3.12`

* You can get and install Python from [python.org](https://www.python.org/)
* In Windows OS, you can get Python in [Windows store](https://apps.microsoft.com/search?query=python)


#### Install Python packages
```bash
pip install -r requirements.txt
```

<br>

## Start server
#### Change directory to src folder
```bash
cd src
```

#### Start server
```
uvicorn main:app --reload
```

#### Now you can access the server documentation at http://localhost:8000/docs
