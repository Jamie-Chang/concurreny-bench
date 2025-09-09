# concurreny-bench
Benchmark concurrency patterns

## Backpressure
Here we do a memory trace to see which version of connection limited back pressure uses the least amount of memory. 

The outgoing http request is simulated for simplicity.


| File | Description | Memory usage in bytes |
|---|---|---|
| semaphore1.py | Traditional pythonic way of using semaphore, does not limit task creation | 152,154,040 |
| semaphore2.py | Semaphore limiting task creation with callback | 1,017,116 |
| semaphore3.py | Semaphore limiting task creation with release called in the task function | 1,014,988 |
| batching.py | Using batched to process things in batches as opposed to using semaphores | 822,308 |

The interesting results is that bataching uses a lot less memory than semaphores. This is not surprising when you consider than semaphores are queuing tasks internally. Where as batching will only take the requisite number of inputs. 

The insight is pointed out to me by [@bmwant](https://github.com/Jamie-Chang/aiointerpreters/issues/3), semaphore3 avoids creating task callbacks which actually does save a bit of memory.

As usual the results can vary by environment and architecture, so test it with your own machine.
