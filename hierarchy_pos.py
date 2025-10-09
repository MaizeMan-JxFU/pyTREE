import networkx as nx
import pandas as pd
import numpy as np

def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    为无向树图创建层次布局
    '''
    if not nx.is_tree(G):
        raise TypeError('不能为非树图使用层次布局')
    if root is None:
        # 对于无向图，选择度数为1的节点作为根（通常是叶子节点）
        roots = [n for n in G.nodes() if G.degree(n) == 1]
        if len(roots) == 0:
            # 如果没有度数为1的节点，选择任意节点
            roots = list(G.nodes())
        root = roots[0]
    def _hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5, 
                      pos=None, parent=None, visited=None):
        if pos is None:
            pos = {}
        if visited is None:
            visited = set()
        pos[root] = (xcenter, vert_loc)
        visited.add(root)
        neighbors = list(G.neighbors(root))
        # 移除父节点（如果存在）
        if parent is not None and parent in neighbors:
            neighbors.remove(parent)
        if len(neighbors) != 0:
            dx = width / len(neighbors)
            nextx = xcenter - width/2 + dx/2
            for neighbor in neighbors:
                if neighbor not in visited:
                    pos = _hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap,
                                        vert_loc=vert_loc-vert_gap, xcenter=nextx,
                                        pos=pos, parent=root, visited=visited)
                    nextx += dx
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)

def trans_pos(pos: dict,G,circle:bool=False):
    _ = []
    y = []
    for node,xy in pos.items():
        _.append([node,*xy])
        y.append(-nx.dijkstra_path_length(G, 'root', node, weight='weight'))
    _ = pd.DataFrame(_,columns=['node','x','y'])
    _['y'] = y
    _['x'] = _['x'].map(dict(zip(sorted(_['x'].unique()),range(len(_['x'].unique())))))
    if circle:
        _['r'] = -_['y']
        _['r'] = (_['r']-_['r'].min())/np.ptp(_['r'])
        _['d'] = 360*(_['x']-_['x'].min())/np.ptp(_['x'])*np.pi/180
        _['x'] = np.sin(_['d'])*_['r']
        _['y'] = np.cos(_['d'])*_['r']
    for i in _.index:
        pos[_.loc[i,'node']] = tuple(_.loc[i,['x','y']])
    return pos