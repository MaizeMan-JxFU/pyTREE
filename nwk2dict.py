import re
import time

class NWKKIT:
    def __init__(self,nwk:str):
        self.nwk = nwk
        self.child_dict = {}
        self._get_leaf()
        pass
    def _get_leaf(self,leaf:str=''):
        self.nwk = self.nwk.replace(leaf,'leaf') if leaf != '' else self.nwk
        pattern = r'\([^()]*\)' if leaf == '' else r'\((?=.*leaf)[^()]*\)' # 从最内侧叶节点开始匹配
        leafs = re.findall(pattern,self.nwk)
        child = ''.join(re.findall(r'\((.*?)\)',leaf)).split(',')
        self.child_dict = dict(zip([i.split(':')[0] for i in child],[float(i.split(':')[1]) for i in child])) if len(child)>1 else None
        for leaf in leafs:
            parent_child = ''.join(re.findall(r'\((.*?)\)',leaf)).split(',') # leaf在左边则是平行节点，在右边则是父子节点
            print('child:',self.child_dict,'parent:',parent_child)
            print('*'*100)
            self._get_leaf(leaf)

class NWK:
    def __init__(self,nwk:str):
        nwk = nwk.replace(' ','').replace(';','').strip()
        nwk = self._recode(nwk)
        self.pattern = r'\([^()]*\)' # 匹配最内侧子树
        self.tree = {}
        while '(' in nwk:
            nwk = self._get_innerNode(nwk)
        pass
    def _get_innerNode(self,nwk:str):
        innerNode = re.search(self.pattern,nwk).group()
        nwk_after = nwk[nwk.index(innerNode):]
        Node1 = re.search(rf'\)(.*?)\)',nwk_after)
        Node2 = re.search(rf'\)(.*?)\,',nwk_after)
        Node = None
        parentNode = 'root'
        if Node1 != None:
            Node1 = Node1.group()[1:-1]
            if Node1.count(':')==1:
                Node = Node1 
        if Node2 != None:
            Node2 = Node2.group()[1:-1]
            if Node2.count(':')==1:
                Node = Node2
        if Node != None: # 存在节点才有父节点
            nwk_after_after = nwk_after[nwk_after.index(Node):]
            parentNode1 = re.search(rf'\)(.*?)\)',nwk_after_after)
            parentNode2 = re.search(rf'\)(.*?)\,',nwk_after_after)
            if parentNode1 != None:
                parentNode1 = parentNode1.group()[1:-1]
                if parentNode1.count(':')==1:
                    parentNode = parentNode1 
            if parentNode2 != None:
                parentNode2 = parentNode2.group()[1:-1]
                if parentNode2.count(':')==1:
                    parentNode = parentNode2
            innerNode_dict = innerNode[1:-1].split(',')
            innerNode_dict = dict(zip([i.split(':')[0] for i in innerNode_dict],[i.split(':')[1] for i in innerNode_dict]))
            self.tree[Node.split(':')[0]] = [Node.split(':')[1],innerNode[1:-1].split(','),parentNode]
        else:
            innerNode_dict = innerNode[1:-1].split(',')
            innerNode_dict = dict(zip([i.split(':')[0] for i in innerNode_dict],[i.split(':')[1] for i in innerNode_dict]))
            self.tree['root'] = [None,innerNode[1:-1].split(','),parentNode]
        nwk = nwk.replace(innerNode,'')
        return nwk
    def _recode(self, nwk):
        pattern = r'([(,)])([^(]*?):'
        counter = 1
        mapping = {}

        def replacement(match):
            nonlocal counter
            prefix = match.group(1)
            content = match.group(2)
            # 为当前匹配分配索引
            index = counter
            counter += 1
            # 记录映射
            mapping[index] = content
            return f"{prefix}{index}:"
        new_nwk = re.sub(pattern, replacement, nwk)
        self.mapping = mapping
        return new_nwk

if __name__ == '__main__':
    with open('tree.huge.nwk') as f:
        nwk = f.readline().strip()
    t = time.time()
    model = NWK(nwk)
    print(model.tree)
    print(round(time.time()-t,4),'Secs')