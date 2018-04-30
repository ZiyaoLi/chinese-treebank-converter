import re


class MyTree:
    def __init__(self, tree, _parent_node=None, _current_layer=0):
        self.parent = _parent_node
        self.layer = _current_layer
        if isinstance(tree, str):
            self.label = tree
            self.terminal = True
            self.children = None
            self.n_children = 0
            return
        self.label = tree.label()
        self.terminal = False
        self.children = []
        for son in tree:
            _node = MyTree(son, self, _current_layer + 1)
            self.children += [_node]
        self.n_children = len(self.children)
        return

    def __getitem__(self, i):
        return self.children[i]

    def labelDependencyTree(self, _current_n_words=1):
        # out nodes:
        if self.terminal:
            self.id = _current_n_words
            return _current_n_words + 1
        for son in self.children:
            _current_n_words = son.labelDependencyTree(_current_n_words)
        self.id = self._findHead().id
        return _current_n_words

    def _tryFetchHead(self, try_labels, reverse=False):
        if isinstance(try_labels, str):
            try_labels = (try_labels,)
        if reverse:
            for lab in try_labels:
                for i in reversed(range(self.n_children)):
                    if re.match(lab, self.children[i].label):
                        return self.children[i]
        else:
            for lab in try_labels:
                for t in self.children:
                    if re.match(lab, t.label):
                        return t
        return None

    def _findHead(self):
        if self.terminal:
            raise AttributeError("cannot call self.findHead() on terminal nodes.")
        if len(self.children) == 1:
            return self.children[0]

        t = self.label

        # coordination
        head = self._tryFetchHead("CC", reverse=True)
        if head:
            return head

        template = {
            "VP": ("V|BA|LB", "ADVP", "QP", "IP", "NP"),
            "VCD|VCP|VNV|VPT|VRD|VSB": "V",
            "TYPO": "NOI",
            "N": "NP|NN|NR|NT|QP|CLP|PN|UCP",
            "LCP": "LCP|LC",
            "DNP": "DEG|DEC",
            "DVP": "DEV|DEG",
            "DP": "DP|CLP|QP",
            "CLP": "M|CLP",
            "ADJP": "ADJP|JJ",
            "ADVP": "ADVP|AD",
            "FRAG": "NN|VV",
            "INJP": "IJ",
            "PP": "P$|PP",
            "PRN": "N|VP|IP|ADJP|QP|UCP",
            "QP": ("QP|CLP", "CD"),
            "UCP": "UCP|NP|IP|PP",
            "IP": ("IP|V", "NP|PP"),
            "CP": "CP|IP|V"
        }

        reverse = ("VCD|VCP|VNV|VPT|VRD|VSB", "N",
                   "CLP", "ADJP", "ADVP", "FRAG", "INTJ",
                   "PRN", "QP", "UCP", "IP", "CP")

        for current_label in template.keys():
            if re.match(current_label, t):
                boolReverse = (current_label in reverse)
                haha = self._tryFetchHead(template[current_label], reverse=boolReverse)
                if haha is None:
                    print(self)
                return haha

        print(self)

    def findDependencyParent(self):
        if self.terminal:
            t = self.parent
            while t.id == self.id:
                t = t.parent
                if t is None:
                    self.dependencyParent = 0
                    return
            self.dependencyParent = t.id
            return
        for son in self.children:
            son.findDependencyParent()

    def printDependencyConLL(self):
        if self.terminal:
            return "%d\t%s\t_\t_\t%s\t_\t%d\t_\t_\t_\n" % (
                self.id, self.label, self.parent.label, self.dependencyParent)
        s = ""
        for son in self.children:
            s += son.printDependencyConLL()
        return s
