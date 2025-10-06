import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import tree
class TREE:
    def __init__(self,Treedic: dict):
        self._ = []
        self._getchild(Treedic)
        pass
    def _getchild(self,dic:dict,loc:tuple=(0,0),layer:int=1):
        x,y = loc
        for ind,root in enumerate(dic.keys()):
            child = dic[root]
            x,y = (loc[0]+(-1)**(ind)/layer,loc[1]+child[0]) if layer > 1 else (x,y)
            self._.append([root,loc[0],x,loc[1],y])
            self._getchild(child[1],(x,y),layer+1)

# nwk file (A:0.1,B:0.2,(C:0.3, D:0.4)E:0.5)F to dictionary
tree_dict = {
    'S':[0,
        {'A':[0.1,
              {'E':[0.2,{'Test':[0.1,{}]}],
               'F':[0.5,{}]}],
         'B':[0.5,
              {'C':[0.3,{}],
               'D':[0.4,{}]}]}]
    }
model = TREE(tree_dict)
tree_df = pd.DataFrame(model._)
# x_loc = sorted(set(tree_df[1].unique().tolist()+tree_df[2].unique().tolist()))
# x_loc_trans_dict = dict(zip(x_loc,range(len(x_loc))))
# tree_df[1] = tree_df[1].map(x_loc_trans_dict)
# tree_df[2] = tree_df[2].map(x_loc_trans_dict)
for i in tree_df.index:
    plt.plot(tree_df.loc[i][[1,2]],tree_df.loc[i][[3,4]],color='black')
    pass
plt.savefig('test.png')