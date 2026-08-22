![alt](https://github.com/sunlao/py_sudoku_solver/blob/main/docs/Operationalization.svg)

This RI introduces opinions about how to operationalize an Actor-Model by creating a domain actor hierarchy for actors and introducing two domain agnostic actor-like shapes. In addition it shows explicitly how to interact with observability.

## Domain Actor Hierarchy

- Controller - actor lifecycle
- Actors - task actors

## External Side Effect Service

- Creates an operational boundary at a platform level for side effects
- unlocks policy enforcement for mapping domain actor behavior to allowed side effect actions.
- Internally it follows a similar pattern to an actor
- Reusable across domains
- Behaviors are strictly focused on serializing a side effect DTO to its corresponding connector and external system interface
- Intentionally relaxes actor purity at the operational boundary
  - Manages side effects externally to actor

## Administrator

- Creates an operational boundary at a platform level for administration
- Internally it follows a similar pattern to an actor
- Reusable across domains
- Behaviors are strictly focused on aggregating actor health and support actions
- Intentionally relaxes actor purity at the operational boundary
  - Provides APIs and visualizations for support engineers
  - Is aware of actor health
  - Can restart the Controller

## Observability

- clear platform boundary between administration and observability
- Actors and services emit APM logs and metrics
- Observability polls for heartbeat and hardware state
- Observability may execute self healing for Administrator
