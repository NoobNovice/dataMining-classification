from DecisionTree import DecisionTree as Dt

tree = Dt(5, 0, 0)
tree.show_tree(tree.get_root())
# tree.accuracy()
# test set
i = [1, 0, 1, 1]
h = [[0, 0], [0, 0], [0, 0]]
w = [[0.3, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.3], [0.1, 0.2, 0.1, 0.2], [-0.1, -0.2, -0.1, -0.2], [-0.1, -0.2, -0.1, -0.2]]
b = [[0.2, 0.4], [0.1, 0.2], [0.25, 0.03], [0.25, 0.03]]
o = [0, 0]
d = [1, 0]
