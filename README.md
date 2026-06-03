# py_sudoku_solver

A multi-actor async event-driven Sudoku solver.

This provides a working reference implementation demonstrating FIFO queue-based actor patterns, with fully independent async agents that manage their own minimal state internally. It explores service composition with event-driven orchestration where actors are responsible for retry logic, re-enqueue and messaging other actors. Provides working examples of idempotent immutable monotonic propagation and data distribution.
