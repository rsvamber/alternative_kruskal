# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'

# %%
import heapq
import time

SAVE_GRAPHS_FOLDER = "rozlozeni_dat\\"

# %% [markdown]
# ## FUNCTIONS

# %%
# nalezeni vrcholu v grafu
def find_vertices_in_tree(tree):
    vertices = set()
    for edge in tree:
        vertices.add(edge[1])
        vertices.add(edge[2])
    return vertices

# spocitani celkove vahy minimalnistry grafu pro ucely testovani
def count_minimum_spanning_tree_weight(tree):
    count = 0
    for edge in tree:
        count += int(edge[0])
    return count

# nacteni datasetu z @filepath
def load_dataset(filepath):
    vertices = set()
    graph = {
        'edges':set([]),
        'vertices':set([]),
    }
    try:
        f = open(filepath, "r")
        for x in f:
            x = x.replace(' ', '')
            split_line = x.split(',')
            split_line[2] = split_line[2].replace('\n', '')
            graph['edges'].add((int(split_line[2]),split_line[1],split_line[0]))
            graph['vertices'].add(split_line[0])
            graph['vertices'].add(split_line[1])
        f.close()
        return graph
    except:
        return -1


# prihradkove razeni nad @graph
def bucket_sort(graph):
    edges = graph['edges']
    max_value = max(edges)[0]
    bucket_size = max_value / len(edges)

    buckets = []
    for _ in edges:
        buckets.append([])

    for edge in edges:
        if int(edge[0] / bucket_size) == len(buckets):
            buckets[int(edge[0] / bucket_size)-1].append(edge)
        else:
            buckets[int(edge[0] / bucket_size)].append(edge)
    for bucket in buckets:
        sorted(bucket)
    return(buckets)

# nalezeni neprazdne prihradky od indexu @index
def find_non_empty_bucket(buckets, index):
    for i in range(index, len(buckets)):
        if len(buckets[i]) != 0:
            return i, buckets[i]
    return -1

# %%
# funkce pro vypis casu spusteni dvou metod pomoci magic module %timeit
def time_execution(DATASET):


    # pro asserty
    time1 = []
    time2 = []

    for _ in range(0, 4):
        start_time1 = time.process_time_ns()
        tree1 = alternative_kruskal(load_dataset(DATASET))
        time1.append(time.process_time_ns() - start_time1)
        start_time2 = time.process_time_ns()
        tree2 = og_kruskal(load_dataset(DATASET))
        time2.append(time.process_time_ns() - start_time2)
    


    print("Asserting minimum spanning trees...")
    assert(len(tree1) == len(tree2))
    assert(count_minimum_spanning_tree_weight(tree1) == count_minimum_spanning_tree_weight(tree2))
    assert(find_vertices_in_tree(tree1) == find_vertices_in_tree(tree2))
    print("Assert passed. Executing...\n")

    print("Time of execution of my kruskal implementation on the dataset '{}'".format(DATASET))
    print(str((sum(time1) / len(time1)) / 1000000000.0)+" s")

    print("-----------------------------------------------------------------------")

    print("Timing of the original kruskal implementation on the dataset {}".format(DATASET))
    print(str((sum(time2) / len(time2)) / 1000000000.0)+" s")
    print("\n")

# %%
parent = dict()
rank = dict()

# funkce pro vytvoreni setu
def make_set(vertice):
    parent[vertice] = vertice
    rank[vertice] = 0

# funkce find pro union & find
def find(vertice):
    if parent[vertice] != vertice:
        parent[vertice] = find(parent[vertice])
    return parent[vertice]

# funkce union pro union & find
def union(vertice1, vertice2):
    root1 = find(vertice1)
    root2 = find(vertice2)
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]: rank[root2] += 1

# ma alternativni implementace kruskalova algoritmu
def alternative_kruskal(graph):

    # vytvareni setu pro kazdy vrchol
    for vertice in graph['vertices']:
        make_set(vertice)

    minimum_spanning_tree = set()
    # index intervalu prihradky 
    j = 0

    # min halda
    h = []

    # vytvoreni prihradek
    buckets = bucket_sort(graph)
    while len(minimum_spanning_tree) < len(graph['vertices']) - 1:
        if(len(h) == 0):
            index_and_bucket = find_non_empty_bucket(buckets, j)
            empty_bucket = index_and_bucket[1]
            j = index_and_bucket[0]
            # pridani obsahu prihradky na haldu
            for val in empty_bucket:
                heapq.heappush(h, val)
        # nalezeni a vymazani hrany s danym ohodnocenim
        #edge = find_and_remove_edge(graph, min(h))

        #edge = min(h)
        # vymazani hrany z haldy
        edge = heapq.heappop(h)

        # vynulovani prazdne prihradky
        if len(h) == 0:
            buckets[j] = []
        
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            minimum_spanning_tree.add(edge)
            union(vertice1, vertice2)

    return minimum_spanning_tree

# originalni implementace s vyuzitim union & find od israelst (https://github.com/israelst/Algorithms-Book--Python/blob/master/5-Greedy-algorithms/kruskal.py)
def og_kruskal(graph):
    for vertice in graph['vertices']:
        make_set(vertice)

    minimum_spanning_tree = set()
    edges = list(graph['edges'])
    edges.sort()
    for edge in edges:        
    
        weight, vertice1, vertice2 = edge
        if find(vertice1) != find(vertice2):
            union(vertice1, vertice2)
            minimum_spanning_tree.add(edge)

    return minimum_spanning_tree

# %% [markdown]
# ## Time execution experiments
# %% [markdown]
# ### DATASET 1

# %%
DATASET = 'data/1.csv' 

# %%
time_execution(DATASET)

# %% [markdown]
# ### DATASET 2

# %%
DATASET = 'data/2.csv' 

# %%
time_execution(DATASET)

# %% [markdown]
# ### DATASET 3

# %%
DATASET = 'data/3.csv' 
# %%
time_execution(DATASET)

# %% [markdown]
# ### DATASET 4

# %%
DATASET = 'data/4.csv' 
# %%
time_execution(DATASET)


# %% [markdown]
### DATASET 5


# %%
DATASET = 'data/5.csv' 
# %%
time_execution(DATASET)


# %%
DATASET = 'data/6.csv' 
# %%
time_execution(DATASET)


# %%
DATASET = 'data/7.csv' 
# %%
time_execution(DATASET)



