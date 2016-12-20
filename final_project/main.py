from pathlib import Path
import copy
import random
import networkx as nx
import matplotlib.pyplot as plt

def brute_force(G): 
# updated 12.1: only use G, no need to create subgraph; modify v1,v2 to avoid duplicate search
# input: graph G
# output: final probability (score) and the the partition list
    score = 0
    partition = []
    V = G.nodes()
    # base case
    if len(V) == 1:
        v = G.nodes()[0]
        return (int(G.node[v]['value']), [[v]])
    if len(V) == 0:
        return (0, [])

    for j in range(0,len(V)):
        v1 = V[j]
        for k in range(j, len(V)):  
            v2 = V[k]
            #print('v1: ' + str(v1) + ', v2: ' + str(v2)) # for debug purpose
            if v1 == v2:                
                val = G.node[v1]['value']
    
                eo = G.out_edges(v1)
                ei = G.in_edges(v1)
                G.remove_node(v1) 
                (sub_score, sub_partition) = brute_force(G) 
                G.add_node(v1)
                G.add_edges_from(eo+ei)
                G.node[v1]['value'] = val

                sub_score += int(val)

                if sub_score > score:
                    score = sub_score
                    partition = sub_partition
                    partition.append([v1])
            else:
                paths = list(nx.all_simple_paths(G, source=v1, target=v2))
                if len(paths) > 0:
                    for path in paths:                        
                        eo = G.out_edges(path)
                        ei = G.in_edges(path)
                        path_score = 0
                        path_val = {}
                        for i in path:
                            path_score += int(G.node[i]['value'])     
                            path_val[i] = G.node[i]['value']
                        n = len(path)
                        path_score *= n

                        G.remove_nodes_from(path) 
                        (sub_score, sub_partition) = brute_force(G)
                        G.add_nodes_from(path)
                        G.add_edges_from(eo+ei)            
                        for i in path:
                            G.node[i]['value'] = path_val[i]

                        sub_score += path_score
                        if sub_score > score:
                            score = sub_score
                            partition = sub_partition
                            partition.append(path)
    return (score, partition)



def calc_path_score(G, path):
# input: graph G
#        the list of nodes in the path
# output: the score: sum * n
    n = len(path)
    score = 0
    for s in path:
        score += int(G.node[s]['value'])
    return score * n


def find_sink(G):
# input: graph G
# output: the list of sinks in the graph
    sinks = []
    for i in G.nodes():
        edges = G.edge[i]
        if len(edges) == 0:
            sinks.append(i)
    return sinks


def find_source(G): 
# input: graph G
# output: the list of sources in the graph
    sources = []
    Gr = G.reverse(copy = True)
    for i in Gr.nodes():
        edges = Gr.edge[i]
        if len(edges) == 0:
            sources.append(i)
    return sources
    

def input_less_than_n_nodes(path_name, file_list, n):
# input: path name (end with '/')
#        file_list: the integer list of files to be checked
# output: list of file numbers with less than or equal to n nodes
    output = []
    for i in file_list:
        f = open(path_name + str(i) + '.in', 'r')
        N = int(f.readline().rstrip('\n'));
        if N <= n:
            output.append(i)
        f.close()
    return output


def generate_output_file(file_list, all_scores, all_partitions, all_names, name): 
# input: file_name: all partition list
#        all_scores: list of all scores
#        all_partitions: 3D list, D1: input, D2: partitions, D3: nodes in each partition
#        algm_name: the name of the algorithm, example: 'greedy', 'longest'
# output: .out file
#         .score file records the score
    f = open('partition_' + name + '.out', 'w')
    for n in all_partitions:  # input number
        s = ''
        for p in n:           # partitions of an input
            for i in p:       # nodes of a partition
                s += str(i-1) + ' ' # -1 make node start from 0
            s = s[:-1]
            s += '; '
        s += '\n'
        f.write(s)
    f.close()

    f = open('score_' + name + '.csv', 'w')
    count = 0
    for n in all_scores:
        f.write(str(file_list[count]) + ', ' + str(n) + ', ' + all_names[count] + '\n')
        count += 1
    f.close()


def remove_trivial(Gn):
# input: the original input graph G
# output: the score acquired from single nodes and single path, 
#         the partition of the single nodes and single path,
#         the new graph Gn
# This function finds single nodes and path with no branches in order to 
# get a simplified graph
    score = 0
    partition = []
    sources = find_source(G)
    sinks = find_sink(G)
    for s in sources:
        for t in sinks:
            # single nodes
            if s == t:
                score += int(G.node[s]['value'])
                partition.append([s])
                Gn.remove_node(s)
            else:
                paths = list(nx.all_simple_paths(G, s, t))
                if len(paths) == 1:
                    flag = True
                    path = paths[0]
                    for v in path:
                        if len(G.edge[v]) > 1:
                            flag = False
                            break
                    if flag:
                        temp = 0
                        n = len(path)
                        for v in path:
                            temp += int(G.node[v]['value'])
                        score += temp * n
                        partition.append(path)
                        Gn.remove_nodes_from(path)
    return (score, partition, Gn)



def greedy(G_org):
# alg: start with source, find largest neighbor, largest neighbor
# alg: if no source, start with largest vertex
# return: score and partition list
    G = nx.DiGraph(G_org)
    score = 0
    partition = []
    while len(G.nodes()) > 0:
        (path_score, path) = find_path_greedy(G)
        score += path_score
        partition.append(path)
        # for debug purpose
        # print(path_score)
        # print(path)
        # print(G.nodes())
    return (score, partition)


def greedy_random(G_org):
    G = nx.DiGraph(G_org)
    score = 0
    partition = []
    while len(G.nodes()) > 0:
        (path_score, path) = find_path_greedy_random(G)
        score += path_score
        partition.append(path)
    return (score, partition)

def greedy_weighted_random(G_org):
    G = nx.DiGraph(G_org)
    score = 0
    partition = []
    while len(G.nodes()) > 0:
        (path_score, path) = find_path_greedy_weighted_random(G)
        score += path_score
        partition.append(path)
    return (score, partition)


def greedy_sink(G_org):
# same as greedy algorithm, but starts searching from sinks
    G = G_org.reverse(copy=True)
    (score, partition) = greedy(G)
    # reverse the node order to form path in oroginal graph
    partition_new = []
    for i in partition:
        i.reverse()
    return (score, partition)


def greedy_sink_random(G_org):
# same as greedy algorithm, but starts searching from sinks
    G = G_org.reverse(copy=True)
    (score, partition) = greedy_random(G)
    # reverse the node order to form path in oroginal graph
    partition_new = []
    for i in partition:
        i.reverse()
    return (score, partition)


def greedy_sink_weighted_random(G_org):
# same as greedy algorithm, but starts searching from sinks
    G = G_org.reverse(copy=True)
    (score, partition) = greedy_weighted_random(G)
    # reverse the node order to form path in oroginal graph
    partition_new = []
    for i in partition:
        i.reverse()
    return (score, partition)


def find_path_greedy(G):
# The function that finds a path in the graph G using basic greedy method
    sources = find_source(G)
    # start from source if there is source
    if len(sources) > 0:
        (value, current) = find_largest_node(G, sources)
    else:
        (value, current) = find_largest_node(G, G.nodes())
    # search path with largest neighbors
    path_score = value
    path = [current]
    while (current is not None):
        (value, next) = find_largest_neighbor(G, current)
        G.remove_node(current)
        if next is None:
            break
        path_score += value
        path.append(next)
        current = next
    path_score *= len(path)
    return (path_score, path)


def find_path_greedy_random(G):
# The function that finds a path in the graph G using greedy method with 
# randomized node selection based on node values
    sources = find_source(G)
    if len(sources) == 0:
        sources = G.nodes()
    (value, current) = random_select_from(G, sources)
    path_score = value
    path = [current]
    while (current is not None):
        neighbors = list(G.edge[current].keys())
        (value, next) = random_select_from(G, neighbors)
        G.remove_node(current)
        if next is None:
            break
        path_score += value
        path.append(next)
        current = next
    path_score *= len(path)
    return (path_score, path)


def find_path_greedy_weighted_random(G):
# The function that finds a path in the graph G using greedy method with 
# randomized node selection based on node values
    sources = find_source(G)
    if len(sources) == 0:
        sources = G.nodes()
    (value, current) = weighted_random_select_from(G, sources)
    path_score = value
    path = [current]
    while (current is not None):
        neighbors = list(G.edge[current].keys())
        (value, next) = weighted_random_select_from(G, neighbors)
        G.remove_node(current)
        if next is None:
            break
        path_score += value
        path.append(next)
        current = next
    path_score *= len(path)
    return (path_score, path)
    

def read_input(path_name, input_number):
# input: path_name: pathname of input files
#        input_number: number of input file
# output: Graph, with nodes 1 to N having attribute 'value'
# example usage: read_input('./input/', 600) reads ./input/600.in as a graph
    G = nx.DiGraph()
    fn = path_name + str(input_number) + '.in'
    f = open(fn, 'r')
    N = int(f.readline().rstrip('\n'))
    print('File name: ' + fn + ', Number of nodes: ' + str(N))
    G.add_nodes_from(range(1, N+1))

    for i in range(1, N+1):
        line = f.readline().strip().split()
        for j in range(1, i):
            if line[j-1] == '1':
                G.add_edge(i, j)
        G.node[i]['value'] = line[i-1]
        for j in range(i+1, N+1):
            if line[j-1] == '1':
                G.add_edge(i, j)
    f.close()
    # for test: show the graph
    # labels = dict((n, d['value']) for n, d in G.nodes(data=True))
    # nx.draw(G, labels=labels)
    # plt.show()
    return G
   

# helper functions
def calc_score_bound(G):
# calculate the lower and upper bound of score
    data = dict((n, d['value']) for n, d in G.nodes(data=True))
    values = list(map(int, data.values()))
    n = len(values)
    low = sum(values)
    high = low * n
    return (low, high)

def find_largest_node(G, nodes):
# input: graph G
#        node: the node to be searched
# output: the value and number of the largest node in the list
    value = -1
    result = None
    for n in nodes:
        v = int(G.node[n]['value'])
        if v > value:
            value = v
            result = n
    return (value, result)

def find_largest_neighbor(G, node):
# input: graph G
#        node: the node to be searched
# output: the value and number of the largest neighbor. If no child, return None
    value = -1
    result = None
    neighbors = G.edge[node]
    if len(neighbors) > 0:
        for n in neighbors:
            v = int(G.node[n]['value'])
            if v > value:
                value = v
                result = n
    return (value, result)

def random_select_from(G, nodes):
# randomly select a neighbor based on probability linear to the value of 
# the neighbors
    if len(nodes) == 0:
        return (0, None)
    selected = random.choice(nodes)
    value = int(G.node[selected]['value'])
    return (value, selected)


def weighted_random_select_from(G, nodes):
# randomly select a neighbor based on probability linear to the value of 
# the neighbors
    if len(nodes) == 0:
        return (0, None)
    weighted_nodes = []
    for i in nodes:
        weighted_nodes += [i] * (int(G.node[i]['value'])+1) # +1 to avoid zero value problem
    selected = random.choice(weighted_nodes)
    value = int(G.node[selected]['value'])
    return (value, selected)


def calc_path_score(G, path):
# input: graph G
#        the list of nodes in the path
# output: the score: sum * n
    n = len(path)
    score = 0
    for s in path:
        score += int(G.node[s]['value'])
    return score * n
            

def verify_partition(G_org, partition):
# verify that the partition is valid on graph
    G = nx.DiGraph(G_org)
    for p in partition:
        current = p[0]
        for i in range(1, len(p)):
            next = p[i]
            if not G.has_edge(current, next):
                print("Wrong edge: " + str(current) + '-->' + str(next))
                return False
            current = next
        G.remove_nodes_from(p)
    return True


def maximun_result(scores, partitions, algms):
# find the maximum score in all the possible scores and the corresponding
# partition and algorithm.
    i = scores.index(max(scores))
    s = scores[i]
    p = partitions[i]
    a = algms[i]
    return (s, p, a)



def longest_path_backward(G):
    remove_cycle(G)
    Gr = G.reverse(copy = True)
    V = nx.topological_sort(Gr)
    (score, partition) = find_longest_path_backward(Gr, V)
    return score, partition
    

def find_longest_path_backward(G, V):
    #show(G)
    partition = []
    path = []
    score = 0
    
    for v in V:
        P = G.predecessors(v)
        if not P:
            G.node[v]['preval'] = int(G.node[v]['value'])
            G.node[v]['prenode'] = [v]
        else:
            preval_list = [G.node[p]['preval'] for p in P]
            max_index = [i for i, j in enumerate(preval_list) if j == max(preval_list)]
            if len(max_index) == 1:
                u = P[max_index[0]]
            else:
                u = P[random.choice(max_index)]
            G.node[v]['prenode'] = copy.copy(G.node[u]['prenode'])
            G.node[v]['prenode'].append(v)
            G.node[v]['preval'] = (G.node[u]['preval']/len(G.node[u]['prenode'])+int(G.node[v]['value']))*(1 + len(G.node[u]['prenode']))

    val_list = [G.node[v]['preval'] for v in V]
    max_val_index = [i for i, j in enumerate(val_list) if j == max(val_list)]
    u = V[random.choice(max_val_index)]
    path = G.node[u]['prenode']
    score += G.node[u]['preval']
    G.remove_nodes_from(path)
    path.reverse()
    partition = [path]
    

    for v in path:
        V.remove(v)
    if not V:
        return score, partition
    else:
        sub_score, sub_partition= find_longest_path_backward(G,V)
        for p in sub_partition:
            partition.append(p)
        score += sub_score
        return score, partition

    
def longest_path_forward(G):
    remove_cycle(G)
    V = nx.topological_sort(G)
    (score, partition) = find_longest_path(G, V)
    return score, partition
    
def find_longest_path(G, V):
    #show(G)
    partition = []
    path = []
    score = 0
    
    for v in V:
        P = G.predecessors(v)
        if not P:
            G.node[v]['preval'] = int(G.node[v]['value'])
            G.node[v]['prenode'] = [v]
        else:
            preval_list = [G.node[p]['preval'] for p in P]
            max_index = [i for i, j in enumerate(preval_list) if j == max(preval_list)]
            if len(max_index) == 1:
                u = P[max_index[0]]
            else:
                u = P[random.choice(max_index)]
            G.node[v]['prenode'] = copy.copy(G.node[u]['prenode'])
            G.node[v]['prenode'].append(v)
            G.node[v]['preval'] = (G.node[u]['preval']/len(G.node[u]['prenode'])+int(G.node[v]['value']))*(1 + len(G.node[u]['prenode']))

    val_list = [G.node[v]['preval'] for v in V]
    max_val_index = [i for i, j in enumerate(val_list) if j == max(val_list)]
    u = V[random.choice(max_val_index)]
    path = G.node[u]['prenode']
    score += G.node[u]['preval']
    G.remove_nodes_from(path)
    partition = [path]

    for v in path:
        V.remove(v)
    if not V:
        return score, partition
    else:
        sub_score, sub_partition= find_longest_path(G,V)
        for p in sub_partition:
            partition.append(p)
        score += sub_score
        return score, partition


def remove_cycle(G):
    V = G.nodes()
    random.shuffle(V)
    for v in V:
        G.node[v]['visited'] = False
    for v in V:
        if not G.node[v]['visited']:
            explore(G,v)


def explore(G,v):
    G.node[v]['visited'] = True
    P = G.successors(v)
    if not P:
        return
    else:
        for u in P:
            if not G.node[u]['visited']:
                explore(G,u)
            else:
                if nx.has_path(G,u,v):
                    G.remove_edge(v,u)


# ***********************************************************************
def run_all(path_name):
# main function to calculate scores for all inputs
    all_partitions = []
    all_scores = []
    all_algms = []
    # **** all input
    file_list = range(1, 601)
    # **** input with 20 nodes or less
    # file_list = [13, 14, 15, 23, 24, 25, 26, 27, 40, 41, 42, 45, 49, 50, 52, 54, 55, 56, 57, 61, 73, 74, 75, 79, 87, 100, 101, 102, 105, 108, 112, 113, 118, 136, 137, 138, 142, 148, 163, 165, 193, 194, 195, 208, 209, 210, 211, 212, 214, 226, 227, 232, 254, 255, 256, 257, 258, 259, 262, 274, 275, 276, 280, 283, 284, 289, 290, 291, 301, 304, 305, 306, 310, 319, 325, 328, 329, 330, 346, 364, 370, 371, 385, 386, 387, 388, 389, 390, 403, 404, 405, 412, 413, 414, 421, 423, 439, 441, 445, 451, 452, 454, 460, 469, 475, 493, 499, 500, 502, 504, 505, 506, 507, 511, 517, 518, 544, 545, 546, 547, 548, 562, 563, 564, 565, 573, 598, 599, 600]
    
    for i in file_list:
        print(i)
        G = read_input(path_name, i)
        scores = []
        partitions = []
        algms = []
        continue_flag = True
        (low, high) = calc_score_bound(G)
        print('Lower bound: ' + str(low))
        print('Upper bound: ' + str(high))

        # longest path
        for i in range(0, 10): # run for N times
            if continue_flag:
                Gn = nx.DiGraph(G) # copy G
                (score, partition) = longest_path_forward(Gn)
                verify_partition(G, partition)
                if score == high:
                    continue_flag = False
                print('Longest Path Forward #' + str(i+1) + ': ' + str(score))
                scores.append(score)
                partitions.append(partition)
                algms.append('lp')

            if continue_flag:
                Gn = nx.DiGraph(G) # copy G
                (score, partition) = longest_path_backward(Gn)
                verify_partition(G, partition)
                if score == high:
                    continue_flag = False
                print('Longest Path Backward #' + str(i+1) + ': ' + str(score))
                scores.append(score)
                partitions.append(partition)
                algms.append('lpb')
        

        # greedy basic
        if continue_flag:
            (score, partition) = greedy(G)
            verify_partition(G, partition)
            if score == high:
                continue_flag = False
            print('Greedy basic: ' + str(score))
            scores.append(score)
            partitions.append(partition)
            algms.append('g')

        # greedy sink
        if continue_flag:
            (score, partition) = greedy_sink(G)
            verify_partition(G, partition)
            if score == high:
                continue_flag = False
            print('Greedy sink:  ' + str(score))
            scores.append(score)
            partitions.append(partition)
            algms.append('gs')

        # randomized
        for i in range(0, 10): # run for N times
            if continue_flag:
                # greedy with random selection
                (score, partition) = greedy_random(G)
                verify_partition(G, partition)
                if score == high:
                    continue_flag = False
                print('Greedy random #' + str(i+1) + ':  ' + str(score))
                scores.append(score)
                partitions.append(partition)
                algms.append('gr')

            if continue_flag:
                # greedy sink with random selection
                (score, partition) = greedy_sink_random(G)
                verify_partition(G, partition)
                if score == high:
                    continue_flag = False
                print('Greedy sink random #' + str(i+1) + ':  ' + str(score))
                scores.append(score)
                partitions.append(partition)
                algms.append('gsr')

            if continue_flag:
                # greedy with weighted random selection
                (score, partition) = greedy_weighted_random(G)
                verify_partition(G, partition)
                if score == high:
                    continue_flag = False
                print('Greedy weighted random #' + str(i+1) + ':  ' + str(score))
                scores.append(score)
                partitions.append(partition)
                algms.append('gwr')

            if continue_flag:
                # greedy sink with weighted random selection
                (score, partition) = greedy_sink_weighted_random(G)
                verify_partition(G, partition)
                if score == high:
                    continue_flag = False
                print('Greedy sink weighted random #' + str(i+1) + ':  ' + str(score))
                scores.append(score)
                partitions.append(partition)
                algms.append('gswr')

        # get the maximum of all
        (score, partition, algm) = maximun_result(scores, partitions, algms)
        print('Final max score: ' + str(score))
        print('Final partition length: ' + str(len(partition)))
        print('Final algorithm: ' + algm)
        print()
        # print(longest_path(G))
        all_partitions.append(partition)
        all_scores.append(score)
        all_algms.append(algm)
    generate_output_file(file_list, all_scores, all_partitions, all_algms, 'all')


######################################### main function ##########################################
if __name__ == "__main__":
    path_name = './inputs_new/'
    run_all(path_name)
    

