![alt](https://github.com/sunlao/py_sudoku_solver/blob/main/docs/diagrams/ActorOverview.svg)

## Overview

This is an opinionated way to operationalize an actor. A pure actor only needs the following:

- An address to receive messages
- A mailbox to process messages sequentially
- Behaviors that implement how messages are handled
- Locally owned state that is exclusive available only to the actor

Actors can only send and receive messages. All actors behave the same regardless of domain or industry except for their behavior.

## Actor Address

The API lives and is made available by the actor runtime on

- Each actor:behavior has exactly one address that is associated to exactly one API and receives exactly one message.
- A Messages is a semantically defined and validated immutable data transport object (DTO) that contains metadata and composable immutable content.
- API's are responsible for delivering messages to the mailbox by enqueuing a DTO onto the queue
- The API emits structured logs to observability service

## Mailbox

The mailbox is started by the actor runtime

- A mailbox is operationalized by an Async non blocking fifo message queue
- Messages are exclusively enqueued by the API
- Messages are exclusively dequeued by the handler

### Handler

The actor runtime starts a handler to

- Dequeue messages from Mailbox
- Responsible for dynamically routing valid messages to the task director
- Manages retry logic for any failed task
- Emits structured logs to observability service

## Tasks

A Task encapsulates a behavior. Each task is associated to exactly one behavior. Tasks are executed on the actor runtime.

### Director

- the exclusive public method for the task
- receives and validates messages
- orchestrates behavior actions
- send behavior response to handler

### Behavior

Bespoke domain logic exclusive to an actor. Behaviors perform the following actions that are orchestrated by director

- Get static data unique to actor
- SET/GET actor state
- Transform DTO
  - DTO's Are immutable
  - Function Receives and validates a DTO on input
  - Creates a new DTO on output
- Send DTO to Actor API's
  - May send to API that owns behavior being processed
  - May send to API owned by different Actor  

## State

Actor runtime capability to manages ephemeral Actor State and caching

- Set Actor State by Caching the DTO
- Get Actor State by returning the cached DTO
