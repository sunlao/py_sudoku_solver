## Overview

AI agent safety enforced through architectural invariants.

![alt](https://github.com/sunlao/py_sudoku_solver/blob/main/docs/diagrams/AIAgentActors.svg)

## RI changes for AI Agents

Controller Actor

- issue control tokens for messages
- persist tokens with messsages in actor behavior state
- new behavior for message token validation

Side Effect Service

- validate message token

Administrator

- detect invalid actor state

Actor Container Boundary

- allow only valid messages in
- allow only valid messages out
- block all other side effects behaviors
