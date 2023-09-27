import urllib.request, json, re, sys
tree = dict()
def printDeps():
    global tree
    for i in tree.keys():
        for j in tree[i]:
            print("\"%(parent)s\" -> \"%(son)s\";" %{"parent": i, "son": j})
def dependencies(root, num):
    global tree
    patt = re.compile("^([a-zA-Z0-9-_]+)")
    search = "https://pypi.org/pypi/" + root + "/json"
    depset = set()
    if (tree.get(root) == None):
        with urllib.request.urlopen(search) as url:
            data = json.load(url)
            depend_libs = data["info"]["requires_dist"]
        if depend_libs != None and num > 0:
            for i in depend_libs:
                if (patt.match(i).group() != root):
                    depset.add(patt.match(i).group())
        tree.update([[root, depset]])
        for i in depset:
            try:
                dependencies(i, num-1)
            except BaseException:
                return
dependencies(sys.argv[1], int(sys.argv[2]))
print("digraph G{")
if (len(tree) == 1):
    if (len(tree.get(list(tree.keys())[0])) == 0):
        print("\""+list(tree.keys())[0]+"\";")
    else:
        printDeps()
else:
    printDeps()
print("}")