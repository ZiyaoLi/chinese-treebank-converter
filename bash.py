from nltk.tree import Tree
import codecs
from tree import MyTree

# load data
f = codecs.open("ctb.bracketed","r","utf-8")
sents = []
posit = []
while True:
    s = f.readline()
    if s == '':
        break
    if s[0] == '#':
        posit += [s.strip()]
    else:
        sents += [s.strip()]

# trans to trees
trees = []
for t in sents:
    tr = Tree.fromstring(t)
    trees += [tr]

mytrees = []
s = ""
for i, tree in enumerate(trees):
    _mytree = MyTree(tree)
    _mytree.labelDependencyTree()
    _mytree.findDependencyParent()
    s += (posit[i] + '\n' + _mytree.printDependencyConLL() + '\n')
    mytrees += [_mytree]

f = codecs.open("output.conll", "w", "utf-8")
f.write(s)
f.close()