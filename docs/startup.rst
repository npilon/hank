Getting Started
===============


Plan
    A decorated Python callable; a specification of how to do work.

Task
    A specification of work to be done; specifies a plan and parameters

Message
    A serialized task in a queue or other message dispatch system

Worker
    A process that executes plans based on tasks

Dispatcher
    An object that handles the mechanics of submitting and performing tasks

Work order
    Tasks can be connected together by flow operators to orchestrate more complex objectives

Work Site
    How a worker is configured to acquire tasks for a dispatcher to perform
