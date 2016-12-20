from main import *
import itertools

def check_small_optimal(path_name, score_file_name):
# This function checks the small graphs (<10 nodes) reaches optimal
# using brute force search
	f = open(score_file_name, 'r')
	data = f.read().split('\n')
	data = data[:-1]
	all_scores = []
	for i in data:
		all_scores.append(int(float(i.split(', ')[1])))
	# print(all_scores)
	for i in range(1, 601):
		G = read_input(path_name, i)
		if len(G.nodes()) <= 8:
			(best_score, partition) = brute_force(G)
			score = all_scores[i-1]
			if score != best_score:
				print(" Brute force score: " + str(best_score))
				print(" Current score: " + str(score))
			else:
				print(' Current score is good.')

def drop_edge(G_orig):
	G = nx.DiGraph(G_orig)
	best_score = 0
	best_partition = []
	V = G.nodes()
	T_all = []
	S = []
	for v in V:
		L = G.successors(v)
		if len(L) > 1:
			S.append(v)
			T_all.append(L)
	for T in list(itertools.product(*T_all)): #choose one set of successors for each node
		Gn = G.copy()
		Gn.remove_edges_from(G.out_edges(S))
		for i in range(len(T)):
			Gn.add_edge(S[i],T[i])
		(score,partition) = drop_in_edge(Gn)
		if score > best_score:
			best_score = copy.copy(score)
			best_partition = copy.copy(partition)
	return (best_score, best_partition)


def drop_in_edge(G_orig):
	#embedded in drop edge
	G = nx.DiGraph(G_orig)
	best_score = 0
	best_partition = []
	V = G.nodes()
	T_all = []
	S = []
	for v in V:
		L = G.predecessors(v)
		if len(L) > 1:
			S.append(v)
			T_all.append(L)
	for T in list(itertools.product(*T_all)): #choose one set of successors for each node
		Gn = G.copy()
		Gn.remove_edges_from(G.in_edges(S))
		for i in range(len(T)):
			Gn.add_edge(T[i],S[i])
		(score,partition) = simple_graph(Gn)
		if score > best_score:
			best_score = copy.copy(score)
			best_partition = copy.copy(partition)
	return (best_score, best_partition)

def simple_graph(G):
	# each node has at most one successor
	score = 0
	partition = []
	V = G.nodes()
	for v in V:
		G.node[v]['visited'] = False
	for v in V:
		if not G.node[v]['visited']:
			if not G.predecessors(v): #source
				if not G.successors(v): #single vertex
					score += int(G.node[v]['value'])
					partition.append([v])
					G.node[v]['visited'] = True
				else: # source
					#t: successor
					#s: current node
					s = copy.copy(v)
					sub_score = 0
					sub_partition = []
					while not G.node[s]['visited']:
						sub_score += int(G.node[s]['value'])
						sub_partition.append(s)
						G.node[s]['visited'] = True
						if not G.successors(s):
							break
						else:
							t = G.successors(s)[0]
							s = copy.copy(t)
					score += sub_score*len(sub_partition)
					partition.append(sub_partition)

	for v in V:
		if not G.node[v]['visited']:
			if G.predecessors(v): #source   
				#must be in cycle
				#t: successor
				#s: current node
				s = copy.copy(v)
				sub_score = 0
				sub_partition = []
				while not G.node[s]['visited']:
					t = G.successors(s)[0]
					sub_score += int(G.node[s]['value'])
					sub_partition.append(s)
					G.node[s]['visited'] = True
					if not G.successors(s):
						break
					else:
						t = G.successors(s)[0]
						s = copy.copy(t)
				score += sub_score*len(sub_partition)
				partition.append(sub_partition) 

	return (score,partition)

def check_fullmark(path_name, score_file, not_fullmark_file):
	fsi = open(new_score_file, 'r')
	fso = open(not_fullmark_file, 'w')
	score = fsi.read().split('\n')[:-1]
	for i in range(0,len(score)):
		s = int(float(score[i].split(', ')[1]))
		G = read_input(path_name, i+1)
		(low, high) = calc_score_bound(G)
		if s < high:
			fso.write(score[i].split(', ')[0]+', '+str(s) + ', ' + score[i].split(', ')[2][:-1] + ', ' + str(high) + '\n')
			print('Input #' + str(i+1) + ': score ' + str(s) + ' bound ' + str(high))
	fsi.close()
	fso.close()
	print('Not fullmark scores saved to: ' + not_fullmark_file)


def merge_new(new_score_file, old_score_file, new_partition_file, old_partition_file, 
	output_score_file, output_partition_file):
# merge new score and partition files to old files and show improvement
	fs1 = open(new_score_file, 'r')
	fp1 = open(new_partition_file, 'r')
	fs2 = open(old_score_file, 'r')
	fp2 = open(old_partition_file, 'r')
	fso = open(output_score_file, 'w')
	fpo = open(output_partition_file, 'w')
	score1 = fs1.read().split('\n')[:-1]
	score2 = fs2.read().split('\n')[:-1]
	partition1 = fp1.read().split('\n')[:-1]
	partition2 = fp2.read().split('\n')[:-1]
	score_new = []
	score_out = []

	for i in score1:
		score_new.append(i.split(', '))
	for i in score2:
		score_out.append(i.split(', '))
	# print(len(score_out))
	for num in range(0, len(score1)):
		i = int(score_new[num][0])-1
		s1 = int(float(score1[num].split(', ')[1]))
		s2 = int(float(score2[i].split(', ')[1]))
		if s1 > s2:
			print('Input #' + str(i+1) + ': ' + str(s2) + ' --> ' + str(s1))
			score_out[i][1] = str(s1)
			score_out[i][2] = score_new[num][2]
			partition2[i] = partition1[num]
	for item in score_out:
		fso.write(item[0] + ', ' + item[1] + ', ' + item[2] + '\n')
	for item in partition2:
		fpo.write(item + '\n')
	fs1.close()
	fs2.close()
	fso.close()
	fp1.close()
	fp2.close()
	fpo.close()
	print('Scores saved to: ' + output_score_file)
	print('Partition saved to: ' + output_partition_file)


######################################### main function ##########################################
if __name__ == "__main__":
	path_name = './inputs_new/'

	# check_small_optimal(path_name, score_file_name)
	new_score_file = 'score_part.csv'
	old_score_file = 'score_all_test2.csv'
	new_partition_file = 'partition_part.out'
	old_partition_file = 'partition_all_test2.out'
	output_score_file = 'score_all_test3.csv'
	output_partition_file = 'partition_all_test3.out'
	merge_new(new_score_file, old_score_file, new_partition_file, old_partition_file, 
		output_score_file, output_partition_file)


