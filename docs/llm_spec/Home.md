## Welcome to the Sudoku Solver wiki

A pythonic multi-actor async event-driven Sudoku solver as a reference implementation (RI) for actor patterns.

This provides a working reference implementation demonstrating FIFO queue-based actor patterns, with fully independent async actors that manage their own minimal state internally. It explores service composition with event-driven orchestration where actors are responsible for retry logic, re-enqueue and messaging other actors. It provides working examples of idempotent immutable monotonic propagation and data distribution. Orchestration happens via service startup and actor events. This demonstrates functionality via event-driven orchestration with no finite state machine, orchestration state or third party scheduling

## Why Actor Models

Discussions of actor models often start with scale mythology: millions of actors, massive concurrency, distributed runtimes, and telecom war stories.

This RI takes a different path.

It focuses on why systems become hard to operationalize:

- policy enforcement
- complexity
- composition
- state
- ownership

Actor patterns matter because they force these concerns into explicit boundaries. State has an owner. Communication happens through messages. Behavior is isolated. Side effects are explicitly controlled. Coordination emerges from well-defined participants rather than hidden orchestration state. This RI enforces delivery and ownership characteristics at the architectural level as invariants that contributes to the following:

### Policy Enforcement

- Agentic AI and other dynamic meta-programming message systems need safe boundaries that can act as a control plane with policy enforcement of side effects
- Actor boundaries constrain with architectural invariants
- Dynamically generated behavior can only act through policy-checkable messages.

### Bugs Eliminated or Reduced

- Shared state race conditions — each actor owns its state; no concurrent mutation.
- Locking errors — avoids classes of deadlocks, livelocks, and priority inversion by eliminating shared mutable state.
- Spooky action at a distance — state changes only through messages to the owning actor.
- Hidden coupling — interactions occur through explicit message contracts rather than direct state access.
- Orphaned ownership — every piece of state has a clearly defined owner.

### Reliability and Safety Characteristics

- Failure isolation — one actor failing does not corrupt another actor's state.
- Explicit communication paths — all interactions occur through messages, not hidden side effects.
- Clear ownership boundaries — responsibility for state and behavior is unambiguous.
- Reduced coordination complexity — actors coordinate through messages rather than locks and shared state.
- Natural audibility — immutable messages provide a write-ahead-log style history of system activity.
- Replay and recovery — message histories can be replayed to reconstruct state, recover failures, and support debugging.
- Idempotent processing — explicit message boundaries make duplicate detection and safe retries straightforward.
