import numpy as np
import matplotlib.pyplot as plt

class TREE:
    def __init__(self,Treedic: dict):
        print(Treedic)
        self.ax = plt.gca()
        self._getchild(Treedic)
        plt.savefig('test.png')
        pass
    def _getchild(self,dic:dict,loc:tuple=(-1,0),layer:int=1):
        x,y = loc
        for ind,root in enumerate(dic.keys()):
            print(root,layer)
            child = dic[root]
            x = loc[0]+(-1)**(ind)/layer
            y = loc[1]+child[0]
            print([loc[0],x],[loc[1],y])
            # self.ax.text(*loc,root,ha='center')
            self.ax.text(x,y,root,ha='center',va='center')
            self.ax.scatter(x,y,color='red')
            self.ax.plot([loc[0],x],[loc[1],y],color='black')
            self._getchild(child[1],(x,y),layer+1)

# nwk file (A:0.1,B:0.2,(C:0.3, D:0.4)E:0.5)F to dictionary
tree_dict = {
    'S':[0,
        {'A':[0.1,
              {'E':[0.2,{}],
               'F':[0.5,{}]}],
         'B':[0.5,
              {'C':[0.3,{}],
               'D':[0.4,{}]}]}]
    }
TREE(tree_dict)