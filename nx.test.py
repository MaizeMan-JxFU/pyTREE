import networkx as nx
import matplotlib.pyplot as plt
from nwk2dict import NWK
import time
from hierarchy_pos import hierarchy_pos
with open('tree.test.nwk') as f:
    nwk = f.readline().strip()
t = time.time()
model = NWK(nwk)
print(round(time.time()-t,4),'Secs')
weighted_edges = []
for node,edges in model.tree.items():
    for edge in edges[1]:
        weighted_edges.extend([(node,edge.split(':')[0],float(edge.split(':')[1]))])
G = nx.Graph()
G.add_weighted_edges_from(weighted_edges)
pos = hierarchy_pos(G,'root',)
subax1 = plt.subplot(111)
nx.draw_networkx_nodes(G, pos,node_shape=['o'])
nx.draw_networkx_edges(G, pos)
for i,loc in pos.items():
    if i != 'root':
        text = model.mapping[int(i)]
        if 'YZW' in text:
            plt.text(*loc,text,ha='center',va='center',rotation=90,fontsize=8)
plt.tight_layout()
plt.savefig('test.png',dpi=300)