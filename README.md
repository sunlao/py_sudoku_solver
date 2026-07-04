# py_sudoku_solver

A pythonic multi-actor async event-driven Sudoku solver as a RI for actor patterns.

This provides a working reference implementation demonstrating FIFO queue-based actor patterns, with fully independent async actors that manage their own minimal state internally. It explores service composition with event-driven orchestration where actors are responsible for retry logic, re-enqueue and messaging other actors. It provides working examples of idempotent immutable monotonic propagation and data distribution. Orchestration happens via service startup and actor events. This demonstrates functionality via event-driven orchestration with no finite state machine, orchestration state or third party scheduling

## Wiki

Vist the [Welcome Page](https://github.com/sunlao/py_sudoku_solver/wiki/Home) to understand Why Actor Models matter with additional information about implementation and project points of view

## Projct status

See the Github [Project Page](https://github.com/users/sunlao/projects/1) for implemenation status and work break down summaries

## Prerequisites

Review the [Getting Started](https://github.com/sunlao/py_sudoku_solver/wiki/Getting-Started) for more info for Mac setup and virtual environment details on how to use this repo.

## Local Development

After following prerequisites:

set local .env file with

```text
APP_CODE=pss
ENV=dev
API_PORT=80
API_PUB_PORT=8080
API_STATIC_DIR=/app/src/api/static
START_UP=true
```

- start with `make up`
- end with `make down`

## Testing

Visit [Testing Page](https://github.com/sunlao/py_sudoku_solver/wiki/Testing) for information on how this repo impelements testing
