import networkx as nx
import numpy as np
import random

def kosarajus(G: nx.DiGraph) -> nx.DiGraph:
    """
    Given a directed graph G, uses Kosaraju's algorithm to find strongly connected components
    and constructs a directed acyclic graph (DAG) by collapsing these components into single nodes.
    The attributes of each node in the DAG are set to be the subnodes (nodes in the original graph) 
    that belong to that SCC.

    Args:
        G: The input directed graph.

    Returns:
        A directed acyclic graph (DAG) derived from the input graph, with subnodes as attributes.
    """

    # Find strongly connected components using Kosaraju's algorithm
    scc = list(nx.strongly_connected_components(G))

    # Create a new DAG
    dag = nx.DiGraph()

    # Add nodes to the DAG (one for each SCC) and set subnodes as attributes
    for i, component in enumerate(scc):
        dag.add_node(i, subnodes=list(component))  # Set subnodes as an attribute

    # Add edges to the DAG based on connections between SCCs
    for u, v in G.edges():
        u_scc = next((i for i, comp in enumerate(scc) if u in comp), None)
        v_scc = next((i for i, comp in enumerate(scc) if v in comp), None)
        if u_scc != v_scc:
            dag.add_edge(u_scc, v_scc)

    return dag

def dag_to_levels(dag: nx.DiGraph):
    if not nx.is_directed_acyclic_graph(dag):
        raise ValueError("Input graph is not a DAG")
    level_arr = []
    graph_copy = dag.copy()
    sources = list(set([node for node in graph_copy.nodes if graph_copy.in_degree(node) == 0]))
    while len(graph_copy.nodes) > 0:
        level_arr.append(sources)
        neighbors = [neighbor for source in sources for neighbor in graph_copy[source]]
        graph_copy.remove_nodes_from(sources)
        sources = list(set([node for node in neighbors if graph_copy.in_degree(node) == 0]))
    return level_arr

def collapsed_level_order(G: nx.DiGraph):
    '''
    Given a directed graph G, returns a list of levels where each level is a list of sets denoting SCCs.
    '''
    SCC = kosarajus(G)
    levels = dag_to_levels(SCC)
    return [[set(SCC.nodes[node]['subnodes']) for node in level] for level in levels]

def loose_level_order(G: nx.DiGraph, key="content"):
    '''
    Given a directed graph G, returns a list of levels where each level is a list of nodes in that level.
    '''
    dag = G.copy()
    make_dag(dag, key)
    levels = dag_to_levels(dag)
    return levels


def remove_cycle_from_digraph(G, key):
    try:
        # Find a cycle in the graph
        cycle = nx.find_cycle(G, orientation='original')
        
        # Find an edge to remove based on node sizes
        for u, v, _ in cycle:
            if len(G.nodes[u][key]) > len(G.nodes[v][key]):
                G.remove_edge(u, v)
                return True  # Cycle was found and an edge was removed
    except nx.NetworkXNoCycle:
        pass  # No cycle found
    
    return False  # No cycle was found

def make_dag(G, key):
    while remove_cycle_from_digraph(G, key):
        pass

def mst_from_node(G, node):
    '''
    Given a graph G and a node, returns the minimum spanning tree of the graph with the given node as the root.
    '''
    return nx.minimum_spanning_tree(G, algorithm='prim', weight='weight', source=node)


def random_code_tree(n):
    # Create a directed graph (initially a tree)
    G = nx.DiGraph()

    # Generate file sizes using a lognormal distribution
    file_sizes = np.random.lognormal(mean=5, sigma=1, size=n)
    
    # Add nodes with file size attributes
    for i in range(n):
        G.add_node(i, size=file_sizes[i], complexity=random.uniform(0, 1))

    # Create a tree structure where branching factor is proportional to file size
    for i in range(1, n):  # Start from 1 since 0 is the root
        # Probability of being chosen as a parent is proportional to file size
        parent = np.random.choice(range(i), p=file_sizes[:i] / np.sum(file_sizes[:i]))
        G.add_edge(i, parent)

    # Add random cross-tree dependencies to simulate real-world complexity
    num_cross_dependencies = n // 5  # Add ~20% cross-dependencies
    for _ in range(num_cross_dependencies):
        src = np.random.randint(0, n)
        tgt = np.random.randint(0, n)
        if src != tgt and not nx.has_path(G, tgt, src):  # Avoid cycles
            G.add_edge(src, tgt)

    return G

def random_code_dag(n):
    # Create a directed acyclic graph
    G = nx.DiGraph()

    # Generate file sizes using a lognormal distribution
    file_sizes = np.random.lognormal(mean=5, sigma=1, size=n)
    # Add nodes with file size attributes
    for i in range(n):
        G.add_node(i, size=file_sizes[i], complexity=random.uniform(0, 1))

    # Add edges to simulate dependencies, preferring smaller files to depend on larger ones
    for i in range(n):
        num_dependencies = np.random.poisson(2)  # Average number of dependencies
        if i > 0:
            # Sort potential dependencies by size in descending order (larger files first)
            potential_dependencies = sorted(range(i), key=lambda x: file_sizes[x], reverse=True)
            # Bias selection towards larger files by taking the top candidates
            dependencies = np.random.choice(
                potential_dependencies,
                size=min(num_dependencies, i),
                replace=False
            )
            for dep in dependencies:
                G.add_edge(dep, i)

    return G

def random_gnp(n):
    p = random.uniform(0, 0.1)  # Random probability of edge creation
    # Create a random directed graph
    G = nx.gnp_random_graph(n, p, directed=True)

    # Add random file sizes to nodes
    for node in G.nodes:
        G.nodes[node]['size'] = np.random.lognormal(mean=5, sigma=1)
        G.nodes[node]['complexity'] = random.uniform(0, 1)

    return G

def random_code_graph(n):
    family = [random_code_tree, random_code_dag, random_gnp]
    weights = [1, 0, 0]
    return np.random.choice(family, p=weights)(n)