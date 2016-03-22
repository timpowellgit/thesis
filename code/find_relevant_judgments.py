import networkx as nx
import re
import os
import shutil

irrelevant = []
graph = nx.read_gexf('../data/echr-judgments-richmeta.gexf')
comparewith = [re.sub('/','_',x) for x in graph.nodes()]
for x in os.listdir('../data/echr-copy-1'):
	if x not in comparewith:
		irrelevant.append(x)
		shutil.rmtree(os.path.join('../data/echr-copy-1',x))
print len(irrelevant)
print len(os.listdir('../data/echr-copy-1'))