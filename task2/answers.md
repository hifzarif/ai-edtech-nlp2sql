# Task 2 Solutions (Junior Software Engineer - Python + AI/ML)

This document answers all questions from Task 2 (Sections A-E), with correctness, clarity, and complexity notes where applicable.

## Section A: Advanced Python Internals

### Q1. Python memory management, reference counting, circular references
- Python primarily uses **reference counting**: each object tracks how many references point to it; when count reaches 0, memory is reclaimed.
- It also has a **cyclic garbage collector** to detect reference cycles that ref-count alone cannot free.
- Example cycle: `a.ref = b` and `b.ref = a` while no external refs exist.
- CPython uses arenas/pools for efficient small-object allocation.

### Q2. GIL and mitigation
- **GIL (Global Interpreter Lock)** allows only one thread to execute Python bytecode at a time in CPython.
- Good for memory safety and simple C-extension integration, but limits CPU-bound multi-threading.
- Mitigation:
  - Use **multiprocessing** for CPU-bound work.
  - Use **asyncio** or threads for I/O-bound work.
  - Offload heavy numeric operations to libraries releasing GIL (NumPy, some C extensions).

### Q3. `__new__` vs `__init__`, `staticmethod` vs `classmethod`
- `__new__(cls, ...)` creates and returns instance (runs before `__init__`), important for immutable types.
- `__init__(self, ...)` initializes already-created instance.
- `staticmethod`: no implicit first arg; utility function in class namespace.
- `classmethod`: receives class `cls`; often used for alternate constructors.

### Q4. Custom context manager (`__enter__`/`__exit__`) and `contextlib`
- Implemented in `task2/solutions.py`:
  - `FileLogger` using `__enter__` and `__exit__`
  - `timer_context()` using `contextlib.contextmanager`

### Q5. Descriptor for validating positive integers
- Implemented as `PositiveInteger` descriptor in `task2/solutions.py`.
- Enforces value type/int and positivity on assignment.

### Q6. Decorator with arguments, retry decorator
- Implemented as `retry(max_attempts, delay_seconds, exceptions)` in `task2/solutions.py`.

### Q7. Generators vs iterators and memory implications
- **Iterator**: object implementing `__iter__` and `__next__`.
- **Generator**: special iterator produced by function using `yield`.
- Generators are lazy and memory-efficient for large streams since they do not materialize full collections.

## Section B: Data Structures & Design

### Q8. LRU Cache with O(1)
- Implemented with hashmap + doubly linked list in `LRUCache`.
- Complexity:
  - `get`: O(1)
  - `put`: O(1)

### Q9. Trie with insert/search/prefix
- Implemented in `Trie`.
- Complexity for string length `m`:
  - Insert: O(m)
  - Search: O(m)
  - Prefix search: O(m)

### Q10. Heap and min-heap implementation
- Heap: complete binary tree satisfying heap-order property.
- Min-heap root is smallest; supports efficient priority operations.
- Implemented `MinHeap`:
  - Insert: O(log n)
  - Extract-min: O(log n)
  - Peek: O(1)

### Q11. Insert/Delete/GetRandom in O(1)
- Implemented as `RandomizedSet` using dynamic array + value->index map.
- Complexity:
  - Insert: O(1) average
  - Delete: O(1) average (swap with last + pop)
  - `get_random`: O(1)

### Q12. Immutability and concurrency
- Immutable objects cannot change after creation; helps avoid shared-state races.
- Easier reasoning in concurrent programs and safer caching/hashing.
- Examples: tuple, frozenset, string (shallow immutability caveat for contained mutable refs).

### Q13. Consistent hashing and use cases
- Maps keys to points on a ring; nodes own ranges.
- Adding/removing node remaps only a fraction of keys.
- Use cases: distributed caches (Redis clusters), load balancing, sharded DB routing.

## Section C: Algorithms

### Q14. Kth largest efficiently
- Implemented with min-heap of size `k`: `kth_largest(nums, k)`.
- Complexity: O(n log k), space O(k).

### Q15. Quick Sort and complexity
- Implemented as `quick_sort`.
- Average: O(n log n), worst: O(n^2), recursion space average O(log n).

### Q16. Longest substring without repeating characters
- Sliding window + hashmap implementation: `longest_substring_without_repeating`.
- Complexity: O(n) time, O(min(n, alphabet)) space.

### Q17. Cycle detection in directed and undirected graphs
- Directed: DFS coloring (`has_cycle_directed`) -> O(V+E).
- Undirected: DFS parent tracking (`has_cycle_undirected`) -> O(V+E).

### Q18. Topological sorting and use cases
- Implemented Kahn's algorithm: `topological_sort`.
- Complexity: O(V+E).
- Use cases: course scheduling, build systems, task dependency ordering.

### Q19. Number of islands
- DFS flood-fill implementation: `num_islands`.
- Complexity: O(R*C) time, O(R*C) worst-case recursion/stack.

### Q20. Dynamic programming + coin change
- DP bottom-up implementation: `coin_change`.
- Complexity: O(amount * len(coins)) time, O(amount) space.

## Section D: Performance & Concurrency

### Q21. Threading vs multiprocessing vs asyncio
- **Threading**: shared memory, low startup, good for I/O-bound tasks, GIL limits CPU-bound throughput.
- **Multiprocessing**: separate processes, true CPU parallelism, higher IPC overhead.
- **Asyncio**: single-threaded event loop with cooperative multitasking; excellent for high-concurrency I/O.

### Q22. Example where asyncio outperforms threading
- Implemented in `asyncio_io_demo` in `task2/solutions.py`.
- For many concurrent network/file waits, asyncio typically scales with lower memory and context-switch overhead.

### Q23. Profiling and optimization
1. Measure first (`cProfile`, `py-spy`, `scalene`, tracing).
2. Locate hotspots (CPU, allocations, I/O waits).
3. Improve algorithms/data structures before micro-optimizations.
4. Reduce unnecessary allocations and repeated work (memoization/caching).
5. Re-profile to validate gains.

## Section E: System Design

### Q24. URL Shortener Design
**Requirements**
- Shorten long URL -> unique short code.
- Redirect short code -> original URL.
- High read throughput, low latency, analytics optional.

**High-level components**
- API service (`POST /shorten`, `GET /{code}`).
- ID/code generator (base62 or hash + collision handling).
- Storage (SQL/NoSQL): `code -> long_url, created_at, expiry, owner`.
- Cache (Redis) for hot redirects.
- Analytics pipeline (async queue + worker).

**Scalability**
- Read-heavy: cache + CDN edge redirects.
- Replicated stateless app servers behind LB.
- DB sharding by code prefix if needed.

**Reliability**
- Idempotency keys for repeated shorten requests.
- Rate limiting + abuse detection.
- Expiry + cleanup jobs.

### Q25. High-throughput Log Analytics System
**Requirements**
- Ingest logs at high rate, query by time/service/severity, near real-time dashboards.

**Architecture**
1. Producers -> message bus (Kafka/Pulsar).
2. Stream processors (Flink/Spark/Kafka Streams) parse/enrich/aggregate.
3. Storage:
   - Hot: Elasticsearch/OpenSearch/ClickHouse for fast queries
   - Cold: object storage (S3-like) for retention
4. Query API + dashboards (Grafana/Kibana-like).

**Design choices**
- Partition by time + service for scale.
- Schema evolution via versioned event contracts.
- Exactly-once or at-least-once depending on cost/latency.
- Backpressure handling and dead-letter queues.

**Operational concerns**
- Multi-tenant quotas, RBAC, alerting, SLOs.
- Data retention and privacy controls.
