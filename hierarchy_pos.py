import networkx as nx
from math import pi,cos,sin
import numpy as np
def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    为无向树图创建层次布局，保证所有叶子节点水平间隔一致
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
    # 预计算每个节点下的叶子节点数量和位置
    def _count_leaves(node, parent=None, visited=None):
        if visited is None:
            visited = set()
        visited.add(node)
        neighbors = list(G.neighbors(node))
        if parent is not None and parent in neighbors:
            neighbors.remove(parent)
        if len(neighbors) == 0:
            # 叶子节点
            return 1, [node]
        else:
            total_leaves = 0
            all_leaves = []
            for neighbor in neighbors:
                if neighbor not in visited:
                    count, leaves = _count_leaves(neighbor, node, visited)
                    total_leaves += count
                    all_leaves.extend(leaves)
            return total_leaves, all_leaves
    # 获取所有叶子节点和它们的计数
    total_leaves, all_leaves = _count_leaves(root)
    leaf_positions = {}
    leaf_width = width / total_leaves if total_leaves > 0 else width
    for i, leaf in enumerate(all_leaves):
        leaf_positions[leaf] = (i * leaf_width + leaf_width/2 - width/2 + xcenter, -1000)  # 临时y值
    def _hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5, 
                      pos=None, parent=None, visited=None):
        if pos is None:
            pos = {}
        if visited is None:
            visited = set()
        # 如果是叶子节点，使用预计算的位置
        if root in leaf_positions:
            x, _ = leaf_positions[root]
            pos[root] = (x, vert_loc)
            visited.add(root)
            return pos
        # 非叶子节点：计算其子树的叶子节点范围
        _, subtree_leaves = _count_leaves(root, parent, set())
        if not subtree_leaves:
            # 如果没有叶子（理论上不会发生），使用默认位置
            pos[root] = (xcenter, vert_loc)
            visited.add(root)
            return pos
        # 找到子树中所有叶子节点的最小和最大x位置
        min_x = min(leaf_positions[leaf][0] for leaf in subtree_leaves)
        max_x = max(leaf_positions[leaf][0] for leaf in subtree_leaves)
        # 当前节点的x位置是其子树叶子节点范围的中心
        current_x = (min_x + max_x) / 2
        pos[root] = (current_x, vert_loc)
        visited.add(root)
        neighbors = list(G.neighbors(root))
        # 移除父节点（如果存在）
        if parent is not None and parent in neighbors:
            neighbors.remove(parent)
        # 递归处理子节点
        for neighbor in neighbors:
            if neighbor not in visited:
                pos = _hierarchy_pos(G, neighbor, width, vert_gap,
                                    vert_loc-vert_gap, xcenter,
                                    pos, root, visited)
        
        return pos
    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)