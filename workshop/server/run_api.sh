#!/bin/bash

source .venv/bin/activate
uvicorn api.api:app --reload --host 0.0.0.0 --port 8000