# Orchestration Node

This server is intended to trigger Globus-Gladier flows upon new data becoming avaliable. Experiemental & a testbed.

## Orchestration Logic

The Globus-Gladier logic itself can be found in this [repo](https://github.com/LivePublication/gladier-globus-orchestration).

## Execution

Run the fastAPI server with the custom uvicorn config - e.g. `uvicorn main:app --config uvicorn_config.py`