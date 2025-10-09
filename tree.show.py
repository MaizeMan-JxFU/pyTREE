import matplotlib.pyplot as plt
import networkx as nx
from collections import deque

def visualize_tree(tree_data,mapping:dict=None):
    """
    可视化树结构
    
    参数:
    tree_data: 字典，包含树结构信息
    """
    # 创建有向图
    G = nx.DiGraph()
    
    # 添加节点和边
    for node, info in tree_data.items():
        # 添加当前节点
        G.add_node(node)
        
        # 处理子节点
        children_info = info[1]  # 第二个元素是子节点列表
        
        if children_info:
            for child_str in children_info:
                if child_str is not None:
                    # 解析子节点字符串，格式为 "节点名:距离"
                    child_parts = child_str.split(':')
                    if len(child_parts) == 2:
                        child_name, distance = child_parts
                        # 添加边和距离属性
                        G.add_edge(node, child_name, distance=round(float(distance),2))
    
    # 计算节点位置 - 使用层次布局
    pos = hierarchy_pos(G, 'root')
    
    # 绘制图形
    plt.figure(figsize=(12, 8))
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                          node_size=100, alpha=0.9)
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, edge_color='gray', 
                          arrows=True, arrowsize=20, 
                          arrowstyle='->', width=2)
    
    # 绘制节点标签
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
    
    # 绘制边标签（距离）
    edge_labels = nx.get_edge_attributes(G, 'distance')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, 
                                font_color='red', font_size=8)
    
    plt.title("Tree Structure Visualization")
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('test.png')

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    """
    为树结构创建层次布局
    
    参数:
    G: 图对象
    root: 根节点
    width: 水平宽度
    vert_gap: 垂直间隙
    vert_loc: 垂直位置
    xcenter: 水平中心
    
    返回:
    pos: 节点位置字典
    """
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, 
                  pos=None, parent=None, parsed=[]):
    """
    递归计算层次布局的辅助函数
    """
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    
    children = list(G.neighbors(root))
    if not children:
        return pos
    
    # 计算子节点数量
    num_children = len(children)
    
    # 计算子节点的水平位置
    xwidth = width / num_children
    nextx = xcenter - width/2 - xwidth/2
    
    for child in children:
        nextx += xwidth
        pos = _hierarchy_pos(G, child, width=xwidth, vert_gap=vert_gap, 
                            vert_loc=vert_loc-vert_gap, xcenter=nextx,
                            pos=pos, parent=root, parsed=parsed)
    return pos

from nwk2dict import NWK
import time
with open('tree.huge.nwk') as f:
    nwk = f.readline().strip()
t = time.time()
model = NWK(nwk)
print(round(time.time()-t,4),'Secs')
# 可视化树结构
visualize_tree(model.tree,model.mapping)