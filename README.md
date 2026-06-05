# py_sudoku_solver

A pythonic multi-actor async event-driven Sudoku solver as a RI for actor patterns.

This provides a working reference implementation demonstrating FIFO queue-based actor patterns, with fully independent async actors that manage their own minimal state internally. It explores service composition with event-driven orchestration where actors are responsible for retry logic, re-enqueue and messaging other actors. It provides working examples of idempotent immutable monotonic propagation and data distribution. Orchestration happens via service startup and actor events. This demonstrates functionality via event-driven orchestration with no finite state machine, orchestration state or third party scheduling
