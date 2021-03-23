Getting Started
===============


job
    A decorated Python callable; a specification of how to do work.
    A special case is a task, which does celery-style argument dispatch.

Work Order
    A specification of work to be done; specifies a job and parameters

Message
    A serialized work order in a queue or other message dispatch system

Worker
    A process that executes jobs based on work orders

Dispatcher
    An object that handles the mechanics of submitting and accepting work orders

Work flow
    Work orders can be connected together by flow operators to orchestrate more complex objectives
