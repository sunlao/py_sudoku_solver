# py_sudoku_solver

A pythonic multi-actor async event-driven Sudoku solver as a RI for actor patterns.

This provides a working reference implementation demonstrating FIFO queue-based actor patterns, with fully independent async actors that manage their own minimal state internally. It explores service composition with event-driven orchestration where actors are responsible for retry logic, re-enqueue and messaging other actors. It provides working examples of idempotent immutable monotonic propagation and data distribution. Orchestration happens via service startup and actor events. This demonstrates functionality via event-driven orchestration with no finite state machine, orchestration state or third party scheduling

## Wiki

[Welcome Page](https://github.com/sunlao/py_sudoku_solver/wiki/Home) to understand Why Actor Models matter with additional infomration about implementation

## Prerequisites

Review the [Getting Started](https://github.com/sunlao/py_sudoku_solver/wiki/Getting-Started) for more info for Mac setup and virtual environment details.

## API docs

- FastAPI dynamically generate docs using [OpenAPI Specifications](https://swagger.io/specification/)
- During local development use:
  - `http://localhost:8080/redoc`  new version for API spec
  - `http://localhost:8080/docs`  "classic" version for API spec