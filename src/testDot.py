import pydot
graph = pydot.Dot("test_graph", graph_type = "graph", bgcolor = "yellow")

edge = []
a = pydot.Node('a', label = "Faa", shape = "Circle")
b = pydot.Node('b', label = "Fbb", shape = "Box")
graph.add_node(a)
graph.add_node(b)
edge.append(pydot.Edge('a', 'b', color = "orange"))
graph.add_edge(edge[-1])

c = pydot.Node('c', label = "Fcc", shape = "Circle")
d = pydot.Node('d', label = "Fdd", shape = "Box")
graph.add_node(c)
graph.add_node(d)
edge.append(pydot.Edge('d', 'b', color = "orange"))
graph.add_edge(edge[-1])

graph.write_png('src/test_graph.png')