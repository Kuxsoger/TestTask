# Build System Microservice

## Installation

### Docker container
1. Run `docker-compose up`
2. Access service at `127.0.0.1:8000`

### Local
1. Create virtual environment `python -m venv venv`
2. Activate virtual environment
    1. Unix: `source venv/bin/activate`
    2. Windows: `venv\Scripts\activate.bat`
3. Install dependencies `pip install -r requirements-dev.txt`
4. Run `uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload`
5. Access service at `127.0.0.1:8000`


## Usage
Service has only one endpoint `POST /get_tasks` to get all tasks ordered for 
specified build:

It accepts JSON body with build name:
```
{
    "build": "build_name"
}
```

Example of request:
```
curl -X POST http://localhost:8000/get_tasks -H "Content-Type: application/json" -d '{"build":"voice_central"}'
```

For Swagger documentation use `GET /docs`

## Run tests

### Docker container
1. Run `docker-compose -f docker-compose-tests.yml up`
2. Enjoy test results

### Local
1. Repeat 1-3 steps from <b>Installation Local</b> section
2. Run `pytest tests`
3. Enjoy test results