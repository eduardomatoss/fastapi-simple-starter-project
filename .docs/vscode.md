# Debug Code using VSCODE Editor

**Example:**

``` json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Run API",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/run.py",
            "console": "integratedTerminal",
            "env": {
                "ENV_FOR_DYNACONF": "development",
                "DATABASE_URL": "",
                "DATABASE_NAME": "",
                "DATABASE_USER": "",
                "DATABASE_PASSWORD": "",
                "DATABASE_PORT": "",
            }
        }
    ]
}
```

**Example:**

``` json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "run:application",
                "--host",
                "0.0.0.0",
                "--workers",
                "1"
            ],
            "env": {
                "ENV_FOR_DYNACONF": "development",
                "DATABASE_URL": "",
                "DATABASE_NAME": "",
                "DATABASE_USER": "",
                "DATABASE_PASSWORD": "",
                "DATABASE_PORT": "",
            },
            "jinja": true
        }
    ]
}
```
