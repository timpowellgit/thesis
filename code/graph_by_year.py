import networkx as nx
graph = nx.read_gexf('../../data/echr-judgments-richmeta.gexf')
# for n in graph.nodes_iter():
# 	print graph.node[n]['date'], graph.node[n]
sg = graph.subgraph( [n for n,attrdict in graph.node.items() if int(attrdict 
['date'].split('-')[0]) < 1980 ] )
for x in sg.nodes_iter():
	print sg.node[x]['date']
# for n,attrdict in graph.node.items():
# 	# date = attrdict['date'].split('-')[0]
# 	# if int(date)< 1980:
# 	# 	print date