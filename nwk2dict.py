import re
import time
with open('tree.mini.nwk') as f:
    nwk = f.readline().strip()
class NWKKIT:
    def __init__(self,nwk:str):
        self.nwk = nwk
        self.nwk_dict = {}
        self._get_leaf()
        pass
    def _get_leaf(self,leaf:str=''):
        self.nwk = self.nwk.replace(leaf,'leaf') if leaf != '' else self.nwk
        pattern = r'\([^()]*\)' if leaf == '' else r'\((?=.*leaf)[^()]*\)' # 从最内侧叶节点开始匹配
        leafs = re.findall(pattern,self.nwk)
        child = ''.join(re.findall(r'\((.*?)\)',leaf)).split(',')
        child = dict(zip([i.split(':')[0] for i in child],[i.split(':')[1] for i in child])) if len(child)>1 else None
        for leaf in leafs:
            parent_child = ''.join(re.findall(r'\((.*?)\)',leaf)).split(',') # leaf在左边则是平行节点，在右边则是父子节点
            print('child:',child,'parent:',parent_child)
            print('*'*100)
            self._get_leaf(leaf)
t = time.time()
NWKKIT(nwk)
print(round(time.time()-t,4),'Secs')