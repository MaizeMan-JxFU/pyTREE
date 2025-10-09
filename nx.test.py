import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pandas as pd
import numpy as np
from nwk2dict import NWK
import time
from hierarchy_pos import hierarchy_pos,trans_pos
with open(r"tree.huge.nwk") as f: # "C:\Users\82788\Desktop\mergeGainAMP.B73v4.ftree.nwk" tree.huge.nwk
    nwk = f.readline().strip()
t = time.time()
model = NWK(nwk)
weighted_edges = []
for node,edges in model.tree.items():
    for edge in edges[1]:
        weighted_edges.extend([(node,edge.split(':')[0],float(edge.split(':')[1]))])
G = nx.Graph()
G.add_weighted_edges_from(weighted_edges)
pos = trans_pos(hierarchy_pos(G,'root',),G,True)
fig, subax1 = plt.subplots(figsize = (8, 8))
group = pd.read_csv('tag_1.csv',sep=r'\t',index_col=1,engine='python').fillna('others')
if False:
    texts = []
    for i,loc in pos.items():
        if i != 'root':
            text = model.mapping[int(i)]
            if text in group[group['group'].isin(['A','B'])].index:
                d = 180/np.pi*np.arctan((loc[1]+1e-8)/(loc[0]+1e-8))
                ha = 'right' if loc[0] < 0 else 'left'
                subax1.text(*loc,group.loc[text]['tag_en'],ha=ha,va='center',fontsize=8,rotation=d)
edge_colors = ['black'] * len(G.edges())
arrowsize = [1] * len(G.edges())
color_dict = {'A':'red','B':'green','others':'grey'}
size_dict = {'A':2,'B':2,'others':.5}
for i, edge in enumerate(G.edges()):
    u, v = edge
    u = model.mapping[int(u)] if u!='root' else 'root'
    v = model.mapping[int(v)] if v!='root' else 'root'
    if u in group.index:
        edge_colors[i] = color_dict[group.loc[u]['group']]
        arrowsize[i] = size_dict[group.loc[u]['group']]
    elif v in group.index:
        edge_colors[i] = color_dict[group.loc[v]['group']]
        arrowsize[i] = size_dict[group.loc[v]['group']]
nx.draw_networkx_nodes(G, pos, node_shape=['s'])
# nx.draw_networkx_labels(G, pos,)
nx.draw_networkx_edges(G, pos,alpha=1,edge_color=edge_colors,width=arrowsize)
circle = patches.Circle((0, 0), radius=1, edgecolor='grey', facecolor='none')
subax1.add_patch(circle)
subax1.scatter(0,0,color='black',edgecolors=None,alpha=.6)
plot_edge = (-1.01,1.01)
subax1.set_xlim(plot_edge)
subax1.set_ylim(plot_edge)
plt.tight_layout()
plt.savefig('test.png',dpi=600)
print(round(time.time()-t,4),'Secs')
