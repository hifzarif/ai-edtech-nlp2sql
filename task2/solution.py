from __future__ import annotations

import asyncio
import random
import time
from collections import defaultdict, deque
from contextlib import contextmanager
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Dict, Iterable, List, Optional, Set, Tuple


# Q4: Custom context manager (__enter__/__exit__)
class FileLogger:
    def __init__(self, path: str):
        self.path = path
        self.fp = None

    def __enter__(self):
        self.fp = open(self.path, "a", encoding="utf-8")
        self.fp.write("start\n")
        return self.fp

    def __exit__(self, exc_type, exc, tb):
        if self.fp:
            self.fp.write("end\n")
            self.fp.close()
        return False


# Q4: contextlib context manager
@contextmanager
def timer_context(label: str = "block"):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = (time.perf_counter() - start) * 1000
        print(f"{label}: {elapsed:.2f} ms")


# Q5: Descriptor for positive integers
class PositiveInteger:
    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, int):
            raise TypeError("Value must be an int")
        if value <= 0:
            raise ValueError("Value must be positive")
        setattr(obj, self.private_name, value)


class Order:
    quantity = PositiveInteger()

    def __init__(self, quantity: int):
        self.quantity = quantity


# Q6: Retry decorator with arguments
def retry(max_attempts: int = 3, delay_seconds: float = 0.0, exceptions=(Exception,)):
    def decorator(fn: Callable):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < max_attempts and delay_seconds > 0:
                        time.sleep(delay_seconds)
            raise last_exc

        return wrapper

    return decorator


# Q8: LRU Cache O(1)
@dataclass
class _Node:
    key: int
    value: int
    prev: Optional["_Node"] = None
    nxt: Optional["_Node"] = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.map: Dict[int, _Node] = {}
        self.head = _Node(0, 0)
        self.tail = _Node(0, 0)
        self.head.nxt = self.tail
        self.tail.prev = self.head

    def _remove(self, node: _Node) -> None:
        p, n = node.prev, node.nxt
        if p:
            p.nxt = n
        if n:
            n.prev = p

    def _append(self, node: _Node) -> None:
        p = self.tail.prev
        p.nxt = node
        node.prev = p
        node.nxt = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.map:
            return -1
        node = self.map[key]
        self._remove(node)
        self._append(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.map:
            self._remove(self.map[key])
            del self.map[key]
        node = _Node(key, value)
        self.map[key] = node
        self._append(node)
        if len(self.map) > self.capacity:
            lru = self.head.nxt
            self._remove(lru)
            del self.map[lru.key]


# Q9: Trie
class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.end = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


# Q10: Min-Heap
class MinHeap:
    def __init__(self):
        self.arr: List[int] = []

    def _up(self, i: int) -> None:
        while i > 0:
            p = (i - 1) // 2
            if self.arr[p] <= self.arr[i]:
                break
            self.arr[p], self.arr[i] = self.arr[i], self.arr[p]
            i = p

    def _down(self, i: int) -> None:
        n = len(self.arr)
        while True:
            l, r = 2 * i + 1, 2 * i + 2
            smallest = i
            if l < n and self.arr[l] < self.arr[smallest]:
                smallest = l
            if r < n and self.arr[r] < self.arr[smallest]:
                smallest = r
            if smallest == i:
                break
            self.arr[i], self.arr[smallest] = self.arr[smallest], self.arr[i]
            i = smallest

    def insert(self, x: int) -> None:
        self.arr.append(x)
        self._up(len(self.arr) - 1)

    def peek(self) -> int:
        if not self.arr:
            raise IndexError("Heap is empty")
        return self.arr[0]

    def extract_min(self) -> int:
        if not self.arr:
            raise IndexError("Heap is empty")
        root = self.arr[0]
        last = self.arr.pop()
        if self.arr:
            self.arr[0] = last
            self._down(0)
        return root


# Q11: Insert/Delete/GetRandom O(1)
class RandomizedSet:
    def __init__(self):
        self.values: List[int] = []
        self.index: Dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.index:
            return False
        self.index[val] = len(self.values)
        self.values.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.index:
            return False
        idx = self.index[val]
        last = self.values[-1]
        self.values[idx] = last
        self.index[last] = idx
        self.values.pop()
        del self.index[val]
        return True

    def get_random(self) -> int:
        return random.choice(self.values)


# Q14: Kth largest
def kth_largest(nums: List[int], k: int) -> int:
    import heapq

    heap: List[int] = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]


# Q15: Quick sort
def quick_sort(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + mid + quick_sort(right)


# Q16: Longest substring without repeating characters
def longest_substring_without_repeating(s: str) -> int:
    last_seen: Dict[str, int] = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        best = max(best, right - left + 1)
    return best


# Q17: Cycle detection (directed)
def has_cycle_directed(graph: Dict[int, List[int]]) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = defaultdict(int)

    def dfs(node: int) -> bool:
        color[node] = GRAY
        for nei in graph.get(node, []):
            if color[nei] == GRAY:
                return True
            if color[nei] == WHITE and dfs(nei):
                return True
        color[node] = BLACK
        return False

    for node in graph:
        if color[node] == WHITE and dfs(node):
            return True
    return False


# Q17: Cycle detection (undirected)
def has_cycle_undirected(graph: Dict[int, List[int]]) -> bool:
    visited: Set[int] = set()

    def dfs(node: int, parent: int) -> bool:
        visited.add(node)
        for nei in graph.get(node, []):
            if nei not in visited:
                if dfs(nei, node):
                    return True
            elif nei != parent:
                return True
        return False

    for node in graph:
        if node not in visited and dfs(node, -1):
            return True
    return False


# Q18: Topological sort (Kahn's algorithm)
def topological_sort(num_nodes: int, edges: List[Tuple[int, int]]) -> List[int]:
    graph = defaultdict(list)
    indegree = [0] * num_nodes
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1

    q = deque([i for i in range(num_nodes) if indegree[i] == 0])
    order = []
    while q:
        cur = q.popleft()
        order.append(cur)
        for nei in graph[cur]:
            indegree[nei] -= 1
            if indegree[nei] == 0:
                q.append(nei)
    return order if len(order) == num_nodes else []


# Q19: Number of islands
def num_islands(grid: List[List[str]]) -> int:
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    count = 0

    def dfs(r: int, c: int) -> None:
        if r < 0 or c < 0 or r >= rows or c >= cols or grid[r][c] != "1":
            return
        grid[r][c] = "0"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                count += 1
                dfs(r, c)
    return count


# Q20: Coin change
def coin_change(coins: List[int], amount: int) -> int:
    INF = amount + 1
    dp = [INF] * (amount + 1)
    dp[0] = 0
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a:
                dp[a] = min(dp[a], dp[a - c] + 1)
    return -1 if dp[amount] == INF else dp[amount]


# Q22: asyncio example (I/O-bound)
async def _fake_io(delay: float) -> float:
    start = time.perf_counter()
    await asyncio.sleep(delay)
    return time.perf_counter() - start


async def asyncio_io_demo(n_tasks: int = 100, delay: float = 0.05) -> float:
    start = time.perf_counter()
    await asyncio.gather(*(_fake_io(delay) for _ in range(n_tasks)))
    return time.perf_counter() - start
