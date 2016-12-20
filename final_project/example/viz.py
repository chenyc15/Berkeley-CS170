from graphviz import Digraph

for fname in ['1', '2', '3']:
    with open(fname + '.in') as f:
        dot = Digraph()
        n = int(next(f))
        A = []
        for line in f:
            A.append(list(map(int, line.rstrip().split(' '))))
        for i in range(n):
            dot.node(str(i), str(A[i][i]))

        for i in range(n):
            for j in range(n):
                if A[i][j] and i != j:
                    dot.edge(str(i), str(j))

        dot.render(fname + '.gv', view=True)
