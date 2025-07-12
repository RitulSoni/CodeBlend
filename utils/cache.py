from abc import ABC, abstractmethod
import networkx as nx
from collections import defaultdict, OrderedDict
import random
class Cache(ABC):
    def __init__(self, capacity):
        self.capacity = capacity
        self.graph = None
        self.hits = 0
        self.misses = 0
    
    @abstractmethod
    def initialize(self, graph):
        """Initialize the cache with a graph."""
        self.graph = graph

    @abstractmethod
    def query(self, node):
        """Query the cache with a node."""
        pass
    
    def name(self, node):
        return self.__name__
    
    @abstractmethod
    def __contains__(self, node):
        pass
    
    @abstractmethod
    def clear(self):
        pass

    def reset(self):
        self.clear()
        self.hits = 0
        self.misses = 0

    def hit_rate(self):
        """Calculate and return the hit rate."""
        total = self.hits + self.misses
        return self.hits / total if total > 0 else 0

from collections import OrderedDict

class LRUCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.cache = OrderedDict()
    
    def clear(self):
        return self.cache.clear()

    def initialize(self, graph):
        self.cache.clear()
        super().initialize(graph)
        # cache `capacity` random nodes
        for node in random.sample(sorted(graph.nodes), min(self.capacity, len(graph.nodes))):
            self.cache[node] = None

    def query(self, node):
        if node in self.cache:
            # Cache hit
            self.hits += self.graph.nodes[node]['size']
            # Move the accessed node to the end to show it was recently used
            self.cache.move_to_end(node)
            return self.cache[node]
        else:
            # Cache miss
            self.misses += self.graph.nodes[node]['size']
            if len(self.cache) >= self.capacity:
                # Remove the least recently used item
                self.cache.popitem(last=False)
            # Add the new node to the cache
            self.cache[node] = None
            return self.cache[node]
    
    def __contains__(self, node):
        return node in self.cache

class LFUCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.cache = {}
        self.freq = defaultdict(int)
    
    def clear(self):
        self.cache.clear()
        self.freq.clear()
    
    def initialize(self, graph):
        self.cache.clear()
        self.freq.clear()
        super().initialize(graph)
        # cache `capacity` random nodes
        for node in random.sample(sorted(graph.nodes), min(self.capacity, len(graph.nodes))):
            self.cache[node] = None
            self.freq[node] = 0

    def query(self, node):
        if node in self.cache:
            # Cache hit
            self.hits += self.graph.nodes[node]['size']
            # Increment the frequency of the node by 'size'
            self.freq[node] += 1
            return self.cache[node]
        else:
            # Cache miss
            self.misses += self.graph.nodes[node]['size']
            if len(self.cache) >= self.capacity:
                # Find the least frequently used node
                lfu_node = min(self.freq, key=self.freq.get)
                # Remove it from the cache and frequency dictionary
                del self.cache[lfu_node]
                del self.freq[lfu_node]
            # Add the new node to the cache and set its frequency to 1
            self.cache[node] = None
            self.freq[node] = 1
            return self.cache[node]
    
    def __contains__(self, node):
        return node in self.cache

class StaticTopKInDegreeCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.cache = {}
    
    def clear(self):
        self.cache.clear()
    
    def initialize(self, graph):
        self.cache.clear()
        super().initialize(graph)
        # cache the top capacity nodes by in-degree
        for node, degree in sorted(self.graph.in_degree, key=lambda x: x[1], reverse=True)[:self.capacity]:
            self.cache[node] = None

    def query(self, node):
        if node in self.cache:
            # Cache hit
            self.hits += self.graph.nodes[node]['size']
            return self.cache[node]
        else:
            # Cache miss
            self.misses += self.graph.nodes[node]['size']
            return None
    
    def __contains__(self, node):
        return node in self.cache

class StaticTopKWeightedInDegreeCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.cache = {}
    
    def clear(self):
        self.cache.clear()
    
    def initialize(self, graph):
        self.cache.clear()
        super().initialize(graph)
        inDegrees = dict(self.graph.in_degree)
        weightedInDegrees = {node: inDegrees[node] * self.graph.nodes[node]['size'] for node in self.graph.nodes}
        # cache the top capacity nodes by weighted in-degree
        for node, degree in sorted(weightedInDegrees.items(), key=lambda x: x[1], reverse=True)[:self.capacity]:
            self.cache[node] = None

    def query(self, node):
        if node in self.cache:
            # Cache hit
            self.hits += self.graph.nodes[node]['size']
            return self.cache[node]
        else:
            # Cache miss
            self.misses += self.graph.nodes[node]['size']
            return None
    
    def __contains__(self, node):
        return node in self.cache

class LeastWeightedCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.cache = {}
        self.freq = defaultdict(int)
    
    def clear(self):
        self.cache.clear()
        self.freq.clear()
    
    def initialize(self, graph):
        self.cache.clear()
        self.freq.clear()
        super().initialize(graph)
        # cache `capacity` random nodes
        for node in random.sample(sorted(graph.nodes), min(self.capacity, len(graph.nodes))):
            self.cache[node] = None
            self.freq[node] = 0

    def query(self, node):
        if node in self.cache:
            # Cache hit
            self.hits += self.graph.nodes[node]['size']
            # Increment the frequency of the node by 'size'
            self.freq[node] += self.graph.nodes[node]['size'] * self.graph.in_degree[node]
            return self.cache[node]
        else:
            # Cache miss
            self.misses += self.graph.nodes[node]['size']
            if len(self.cache) >= self.capacity:
                # Find the least frequently used node
                lfu_node = min(self.freq, key=self.freq.get)
                # Remove it from the cache and frequency dictionary
                del self.cache[lfu_node]
                del self.freq[lfu_node]
            # Add the new node to the cache and set its frequency to 'size'
            self.cache[node] = None
            self.freq[node] = self.graph.nodes[node]['size'] * self.graph.in_degree[node]
            return self.cache[node]
    
    def __contains__(self, node):
        return node in self.cache

class StaticTopKSizeCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        self.cache = {}
    
    def clear(self):
        self.cache.clear()
    
    def initialize(self, graph):
        self.cache.clear()
        super().initialize(graph)
        # cache the top capacity nodes by size
        for node, size in sorted(nx.get_node_attributes(self.graph, 'size').items(), key=lambda x: x[1], reverse=True)[:self.capacity]:
            self.cache[node] = None

    def query(self, node):
        if node in self.cache:
            # Cache hit
            self.hits += self.graph.nodes[node]['size']
            return self.cache[node]
        else:
            # Cache miss
            self.misses += self.graph.nodes[node]['size']
            return None

    def __contains__(self, node):
        return node in self.cache

class CompositeCache(Cache):
    def __init__(self, capacity):
        super().__init__(capacity)
        staticCapacities = [1]
        self.staticCaches = [CacheType(staticCapacities[i]) for i, CacheType in enumerate([StaticTopKWeightedInDegreeCache])]
        capacity -= sum(staticCapacities)
        dynamicCapacities = [capacity // 4, capacity - (capacity // 4)]
        self.dynamicCaches = [CacheType(dynamicCapacities[i]) for i, CacheType in enumerate([LeastWeightedCache, LRUCache])]
        self.caches = self.staticCaches + self.dynamicCaches
    
    def clear(self):
        for cache in self.caches:
            cache.clear()
    
    def reset(self):
        for cache in self.caches:
            cache.reset()
    
    def initialize(self, graph):
        super().initialize(graph)
        self.clear()
        for cache in self.caches:
            cache.initialize(graph)
    
    def hit_rate(self):
        total = sum(cache.hits + cache.misses for cache in self.caches)
        return sum(cache.hits for cache in self.caches) / total if total > 0 else 0

    def query(self, node):
        for cache in self.staticCaches:
            if node in cache:
                return cache.query(node)
        else:
            for cache in self.dynamicCaches:
                if node in cache:
                    return cache.query(node)
        # cache <- weighted random choice of caches based on hit rate
        cache = random.choices(self.caches, weights=[cache.hit_rate() + 0.00001 for cache in self.caches])[0]
        return cache.query(node)
    
    def __contains__(self, node):
        return any(node in cache for cache in self.caches)