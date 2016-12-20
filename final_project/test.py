from final_merge import *

path_name = './inputs/'
file_list = range(1, 601)
#small_input = input_less_than_20_nodes(path_name, file_list)
#print(small_input)
G = read_input(path_name, 563)
flag_bf = False
flag_greedy = True
flag_show = True

# # test calc_score_bound
# (low, high) = calc_score_bound(G)
# print('Lower bound: ' + str(low))
# print('Upper bound: ' + str(high))

# # test brute force
# if flag_bf:
# 	(score1, partition1) = brute_force(G)
# 	print('Brute force:')
# 	print(score1)
# 	print(partition1)

# test initial pass
#(score, partition, Gn) = initial_pass(G)
#print(score)
#print(partition)

# test find_largest_neighbor
#(value, largest) = find_largest_neighbor(G, 2)
#(value1, largest1) = find_largest_node(G, G.nodes())
#print(value1)
#print(largest1)

# test greedy algorithm v1
# if flag_greedy:
# 	(score2, partition2) = greedy(G)
# 	print('Greedy:')
# 	print(score2)
# 	print(partition2)

if flag_show:
	labels = dict((n, str(n) + "-" + d['value']) for n, d in G.nodes(data=True))
	nx.draw_circular(G, labels=labels, node_size=1000)
	plt.show()

#print(find_sink(G))
#print(find_source(G))


#test_partition =[[[1,2], [3]], [[4, 5, 6], [1, 2, 3, 7]]] 
#generate_output_file('test.out', test_partition)

