# CodeBlend: Intelligent Caching for Code Repository Analysis

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph_Analysis-green.svg)](https://networkx.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Authors:** Ayush Raman (ayushr3), Ritul Soni (rsoni27), Shashwat Mundra (mundra3)

A comprehensive research project exploring intelligent caching strategies, string matching algorithms, and dependency graph analysis for code repositories. This work was submitted as a final project for CS598 Systems for Generative AI.

## 🎯 Project Overview

CodeBlend addresses the challenge of efficient code analysis and retrieval through multiple interconnected research components:

1. **Advanced String Matching**: Implementation of the FASTA algorithm for fast, accurate code similarity detection
2. **Intelligent Caching Systems**: Research and comparison of various caching strategies optimized for code repository access patterns  
3. **Dependency Graph Analysis**: Graph-based modeling of code relationships and dependencies
4. **LLM Integration**: Integration with CacheBlend for fast large language model serving with cached knowledge fusion

## 🔬 Research Components

### 1. String Matching Algorithms (`Demo_Algorithms.ipynb`)

Implementation of bioinformatics-inspired algorithms adapted for code analysis:

- **FASTA Algorithm**: Fast sequence alignment for code similarity detection
- **Dynamic Programming**: Optimized Smith-Waterman alignment with diagonal banding
- **K-tuple Matching**: Efficient initial similarity detection
- **Tokenization Strategies**: Line-wise and word-wise tokenization for different analysis granularities

**Key Features:**
- Configurable scoring matrices for different code similarity metrics
- Support for both exact and fuzzy matching
- Optimization for large-scale code corpus analysis

### 2. Caching Strategy Research (`Demo_Caching.ipynb`)

Comprehensive analysis of caching algorithms optimized for code repository access patterns:

#### Implemented Cache Policies:
- **LRU (Least Recently Used)**: Traditional temporal locality optimization
- **LFU (Least Frequently Used)**: Frequency-based caching with size weighting
- **Static TopK InDegree**: Dependency-based caching using graph centrality
- **Weighted InDegree**: Size and dependency aware caching
- **Composite Caching**: Multi-strategy hybrid approach

#### Experimental Methodology:
- **Graph Generation**: Random DAGs, trees, and GNP graphs modeling code repositories
- **Realistic Access Patterns**: Dependency-driven query distributions
- **Performance Metrics**: Hit rates, timing analysis, and scalability studies
- **Parameter Sweeps**: Cache sizes (6-12), graph sizes (20-120 nodes)

#### Key Findings:
- **LRU Cache**: Highest average hit rate (79.1%) with consistent performance
- **Composite Cache**: Best overall performance (79.2%) combining multiple strategies  
- **Static Caches**: Good performance for dependency-heavy workloads
- **Scalability**: Performance analysis across varying repository sizes

### 3. Real-World Analysis (`Demo_CodeBlend.ipynb`)

Analysis of actual code repositories using dependency graph modeling:

- **Repository Mining**: Automated analysis of Python codebases (tested on matplotlib)
- **Dependency Extraction**: AST-based import analysis and relationship mapping  
- **Graph Construction**: NetworkX-based modeling of code dependencies
- **Centrality Analysis**: Identification of critical files using graph metrics
- **Cache Performance**: Real-world validation of caching strategies

### 4. Graph Generation (`Demo_RandomGraphs.ipynb`)

Sophisticated graph generation for realistic code repository simulation:

- **Random DAGs**: Modeling hierarchical dependencies
- **Random Trees**: Simulating modular code structures  
- **GNP Graphs**: General dependency networks
- **Parameterized Generation**: Configurable complexity and size distributions

## 🛠️ CacheBlend Integration

This project integrates with [CacheBlend](https://arxiv.org/pdf/2405.16444), a system for fast large language model serving with cached knowledge fusion, based on [vLLM](https://github.com/vllm-project/vllm).

### CacheBlend Features:
- **Fast LLM Inference**: Optimized serving with knowledge caching
- **Multiple Datasets**: Support for Musique, SamSum, and WikiMQA datasets
- **Comparative Analysis**: Benchmarking against standard prefill methods

## 📊 Experimental Results

### Cache Performance Analysis

Our experiments across 101 graph sizes with 30 iterations each revealed:

| Cache Strategy | Avg Hit Rate | Performance Characteristics |
|----------------|--------------|----------------------------|
| LRU Cache | 79.1% | Best for temporal locality |
| Composite Cache | 79.2% | Optimal hybrid approach |
| LFU Cache | 47.5% | Good for frequency patterns |
| Weighted InDegree | 67.3% | Excellent for dependency-heavy code |
| Static TopK Size | 63.9% | Effective for large file bias |

### Scalability Insights:
- **Cache Size Impact**: Linear improvement with larger caches (avg 0.009-0.039 hit rate increase per size unit)
- **Graph Size Robustness**: Consistent performance across repository sizes
- **Real-world Validation**: Successful application to matplotlib repository (1000+ files)

## 🚀 Installation & Setup

### Prerequisites
- Python ≥ 3.9
- CUDA ≥ 12.1 (for CacheBlend)  
- Nvidia GPU with ≥40GB memory (recommended for CacheBlend)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd CodeBlend
```

2. **Install main dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install CacheBlend (optional):**
```bash
cd CacheBlend/vllm_blend
pip install -e .
cd ../..
pip install -r CacheBlend/requirements.txt
```

### Dependencies
- `networkx`: Graph analysis and manipulation
- `numpy`: Numerical computations  
- `matplotlib`: Visualization
- `transformers`: Language model utilities
- `gitpython`: Repository analysis
- `google-generativeai`: LLM integration
- `flask`: Web interface components

## 📚 Usage Examples

### Basic Cache Analysis
```python
from utils.cache import LRUCache, LFUCache
from utils.graphutils import random_code_graph

# Generate a test repository graph
graph = random_code_graph(50)

# Initialize caches
lru_cache = LRUCache(capacity=10)
lfu_cache = LFUCache(capacity=10) 

# Test performance
lru_cache.initialize(graph)
hit_rate = lru_cache.hit_rate()
```

### FASTA String Matching
```python
from utils.stringutils import fasta_algorithm, linewise_tokenize

database = """def example_function():
    return "Hello World" """
query = """def example_func():
    return "Hello" """

# Tokenize and align
db_tokens = linewise_tokenize(database)
query_tokens = linewise_tokenize(query)

alignment, score = fasta_algorithm(db_tokens, query_tokens)
```

### Repository Analysis
```python
from utils.graphutils import build_dependency_graph

# Analyze a local repository
graph = build_dependency_graph("path/to/repository")

# Identify central files
centrality = nx.degree_centrality(graph)
critical_files = sorted(centrality.items(), key=lambda x: x[1], reverse=True)
```

### CacheBlend Integration
```bash
# Run basic LLM inference with caching
python CacheBlend/example/blend.py

# Compare with normal prefill on datasets
python CacheBlend/example/blend_musique.py
python CacheBlend/example/blend_samsum.py  
python CacheBlend/example/blend_wikimqa.py
```

## 🔬 Research Methodology

### Experimental Design
1. **Controlled Simulation**: Parameterized graph generation with realistic code characteristics
2. **Multi-dimensional Analysis**: Cache size, graph size, and algorithm variations
3. **Statistical Rigor**: Multiple iterations and averaged results
4. **Real-world Validation**: Testing on actual repositories

### Evaluation Metrics
- **Hit Rate**: Percentage of successful cache retrievals
- **Timing Analysis**: Performance overhead measurements  
- **Scalability**: Performance across varying problem sizes
- **Memory Efficiency**: Cache utilization and overhead

## 📈 Future Work

- **Machine Learning Integration**: Predictive caching using code usage patterns
- **Distributed Caching**: Multi-node cache coordination for large repositories
- **Semantic Caching**: Content-aware caching beyond syntactic similarity
- **IDE Integration**: Real-time caching for development environments
- **Cross-language Support**: Extension beyond Python to other programming languages

## 🤝 Contributing

This project was developed as academic research. For questions or collaboration opportunities, please contact the authors.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 References

- [CacheBlend: Fast Large Language Model Serving with Cached Knowledge Fusion](https://arxiv.org/pdf/2405.16444)
- [vLLM: Easy, Fast, and Cheap LLM Serving](https://github.com/vllm-project/vllm)
- NetworkX Documentation: https://networkx.org/
- Smith-Waterman Algorithm: https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm

## 📞 Contact

- **Ayush Raman**: ayushr3@illinois.edu
- **Ritul Soni**: rsoni27@illinois.edu  
- **Shashwat Mundra**: mundra3@illinois.edu

---

*This work was completed as part of CS598 Systems for Generative AI at the University of Illinois.*
