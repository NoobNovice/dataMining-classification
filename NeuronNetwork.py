import math
import copy
import xlrd
from NeuronStructure import structure

class NeuronNetwork:
    I, H, O, W, B = structure(3, 3, 12, 6)
    test_table = []
    tech_table = []

    #test set
    i = [1, 0, 1, 1]
    h = [[0, 0], [0, 0], [0, 0]]
    w = [[0.3, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.3], [0.1, 0.2, 0.1, 0.2], [-0.1, -0.2, -0.1, -0.2], [-0.1, -0.2, -0.1, -0.2]]
    b = [[0.2, 0.4], [0.1, 0.2], [0.25, 0.03], [0.25, 0.03]]
    o = [0, 0]
    d = [1, 0]

    n = 0.1

    def __init__(self, sheet_index):
        data = xlrd.open_workbook("Ndata_set.xls")
        sheet = data.sheets()
        # create tech and test table
        # 70::30
        n_tech = int((sheet[sheet_index].nrows - 1) * 0.7)
        # read file in to input table
        for col in range(0, sheet[sheet_index].ncols):
            att = []
            for row in range(1, n_tech + 1):
                att.append(sheet[0].cell(row, col).value)
            self.tech_table.append(att)

        for col in range(0, sheet[sheet_index].ncols):
            att = []
            for row in range(n_tech + 1, sheet[sheet_index].nrows):
                att.append(sheet[0].cell(row, col).value)
            self.test_table.append(att)
        return

    @staticmethod
    def activation_func(v):
        y = 1 / (1 + math.exp(-v))
        return y

    @staticmethod
    def diff_func(y):
        y_diff = y * (1-y)
        return y_diff

    @staticmethod
    def zero_list(n):
        return [0] * n

    def lean(self, time):
        for t in range(time):
            # print(t)
            # Feed Forward Step
            for layer in range(len(self.w)):
                # input layer
                if layer == 0:
                    for index_h_node in range(len(self.h[0])):
                        var_sum = 0
                        for index_i_node in range(len(self.i)):
                            var_sum += self.w[layer][index_i_node * len(self.h[0]) + index_h_node] * self.i[index_i_node]
                        var_sum += self.b[0][index_h_node]
                        self.h[0][index_h_node] = self.activation_func(var_sum)
                # output layer
                elif layer == len(self.h):
                    for index_o_node in range(len(self.o)):
                        var_sum = 0
                        for index_h_node in range(len(self.h[layer - 1])):
                            var_sum += self.w[layer][index_h_node * len(self.o) + index_o_node] * self.h[-1][index_h_node]
                        var_sum += self.b[layer][index_o_node]
                        self.o[index_o_node] = self.activation_func(var_sum)
                # hidden layer
                else:
                    for index_hj_node in range(len(self.h[layer])):
                        var_sum = 0
                        for index_hi_node in range(len(self.h[layer - 1])):
                            var_sum += self.w[layer][index_hi_node * len(self.h[layer]) + index_hj_node] * self.h[layer - 1][index_hi_node]
                        var_sum += self.b[layer][index_hj_node]
                        self.h[layer][index_hj_node] = self.activation_func(var_sum)

            # Back Propagation step
            delta_weight = []
            for i in range(len(self.w)):
                arr = []
                for j in range(len(self.w[i])):
                    arr.append(0)
                delta_weight.append(arr)
            pre_g = []
            for back_layer in range(len(self.w) - 1, -1, -1):
                # output layer
                if back_layer == len(self.h):
                    print("a")
                    for index_o_node in range(len(self.o)):
                        e = self.d[index_o_node] -self.o[index_o_node]
                        g = self.diff_func(self.o[index_o_node]) * e
                        pre_g.append(g)

                        delta_bias = -1 * self.n * g * 1
                        self.b[back_layer][index_o_node] += delta_bias

                        for index_h_node in range(len(self.h[back_layer - 1])):
                            delta = -1 * self.n * g * self.h[back_layer - 1][index_h_node]
                            delta_weight[back_layer][index_h_node * len(self.o) + index_o_node] = delta
                # hidden connect output layer
                elif len(self.h) - back_layer == 1 and back_layer != 0:
                    print(back_layer)
                    print("b")
                    g_temp = copy.deepcopy(pre_g)
                    pre_g.clear()
                    for index_hj_node in range(len(self.h[len(self.h) - 1])):
                        sum_gw = 0
                        for index_o_node in range(len(self.o)):
                            sum_gw += g_temp[index_o_node] * self.w[back_layer][index_hj_node * len(self.o) + index_o_node]
                        g = self.diff_func(self.h[back_layer - 1][index_hj_node]) * sum_gw
                        pre_g.append(g)

                        delta_bias = -1 * self.n * g * 1
                        self.b[back_layer][index_hj_node] += delta_bias

                        for index_hi_node in range(len(self.h[len(self.h) - 2])):
                            delta = -1 * self.n * g * self.h[len(self.h) - 2][index_hi_node]
                            delta_weight[back_layer][index_hi_node * len(self.h[back_layer - 1]) + index_hj_node] = delta
                # hidden layer
                elif back_layer > 0:
                    print("c")
                    g_temp = copy.deepcopy(pre_g)
                    pre_g.clear()
                    for index_hj_node in range(len(self.h[back_layer - 1])):
                        sum_gw = 0
                        for index_g_node in range(len(g_temp)):
                            sum_gw += g_temp[index_g_node] * self.w[back_layer][index_hj_node * len(self.h[back_layer]) + index_o_node]
                        g = self.diff_func(self.h[back_layer - 1][index_hj_node]) * sum_gw
                        pre_g.append(g)

                        delta_bias = -1 * self.n * g * 1
                        self.b[back_layer][index_hj_node] += delta_bias

                        for index_hi_node in range(len(self.h[back_layer - 2])):
                            delta = -1 * self.n * g * self.h[back_layer - 2][index_hi_node]
                            delta_weight[back_layer][index_hi_node * len(self.h[back_layer - 1]) + index_hj_node] = delta
                # input layer
                else:
                    print(back_layer)
                    g_temp = copy.deepcopy(pre_g)
                    pre_g.clear()
                    if len(self.h) == 1:
                        print("d1")
                        for index_h_node in range(len(self.h[len(self.h) - 1])):
                            sum_gw = 0
                            for index_o_node in range(len(self.o)):
                                sum_gw += g_temp[index_o_node] * self.w[back_layer][index_h_node * len(self.o) + index_o_node]
                            g = self.diff_func(self.h[back_layer - 1][index_h_node]) * sum_gw
                            pre_g.append(g)

                            delta_bias = -1 * self.n * g * 1
                            self.b[back_layer][index_h_node] += delta_bias

                            for index_i_node in range(len(self.i)):
                                delta = -1 * self.n * g * self.i[index_i_node]
                                delta_weight[back_layer][index_i_node * len(self.h[0]) + index_h_node] = delta
                    else:
                        print("d2")
                        for index_hi_node in range(len(self.h[0])):
                            sum_gw = 0
                            for index_hj_node in range(len(self.h[1])):
                                sum_gw += g_temp[index_hj_node] * self.w[back_layer][index_hi_node * len(self.h[1]) + index_hj_node]
                            g = self.diff_func(self.h[back_layer - 1][index_hi_node]) * sum_gw
                            pre_g.append(g)

                            delta_bias = -1 * self.n * g * 1
                            self.b[0][index_hi_node] += delta_bias

                            for index_i_node in range(len(self.i)):
                                delta = -1 * self.n * g * self.i[index_i_node]
                                delta_weight[back_layer][index_i_node * len(self.h[0]) + index_hi_node] = delta

            print("\n-----------------------------------------------------------------------------------------------\n")
            for i in range(len(delta_weight)):
                print("new layer")
                for j in range(len(delta_weight[i])):
                    print("[][]" + str(i) + str(j) + " " + str(delta_weight[i][j]))
        return

    def test(self, arr_input):
        result = None
        return result

n = NeuronNetwork(0)
n.lean(1)
print(n.h)
print(n.o)