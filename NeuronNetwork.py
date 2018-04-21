import math
import copy
import xlrd
import random
from NeuronStructure import structure

class NeuronNetwork:
    I, H, O, W, B = structure(3, 3, 12, 7)
    test_table = []
    tech_table = []
    n = 0.01
    D = []
    def __init__(self, sheet_index):
        data = xlrd.open_workbook("Ndata_set.xls")
        sheet = data.sheets()
        # create tech and test table
        # 70::30
        n_tech = int((sheet[sheet_index].nrows - 1) * 0.7)
        # read file in to tech table
        for col in range(0, sheet[sheet_index].ncols):
            att = []
            for row in range(1, n_tech + 1):
                att.append(sheet[0].cell(row, col).value)
            self.tech_table.append(att)
        # read file in to test table
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

    def __get_I_D__(self, table, row):
        # map label to one hot vector
        if table[-1][row] == "CL6":
            self.D = [0, 0, 0, 0, 0, 0, 1]
        elif table[-1][row] == "CL5":
            self.D = [0, 0, 0, 0, 0, 1, 0]
        elif table[-1][row] == "CL4":
            self.D = [0, 0, 0, 0, 1, 0, 0]
        elif table[-1][row] == "CL3":
            self.D = [0, 0, 0, 1, 0, 0, 0]
        elif table[-1][row] == "CL2":
            self.D = [0, 0, 1, 0, 0, 0, 0]
        elif table[-1][row] == "CL1":
            self.D = [0, 1, 0, 0, 0, 0, 0]
        else:
            self.D = [1, 0, 0, 0, 0, 0, 0]
        # cut row
        self.I.clear()
        for col in range(len(self.tech_table) - 1):
            self.I.append(self.tech_table[col][row])
        return

    def swap_teach_row(self, table):
        for j in range(len(table[0])):
            random_index = random.randint(0, len(table[0]) - 1)
            for i in range(len(table)):
                swap = table[i][j]
                table[i][j] = table[i][random_index]
                table[i][random_index] = swap
        return

    def feed_forward(self):
        for layer in range(len(self.W)):
            # input layer
            if layer == 0:
                for index_h_node in range(len(self.H[0])):
                    var_sum = 0
                    for index_i_node in range(len(self.I)):
                        var_sum += self.W[layer][index_i_node * len(self.H[0]) + index_h_node] * self.I[index_i_node]
                    var_sum += self.B[0][index_h_node]
                    self.H[0][index_h_node] = self.activation_func(var_sum)
            # output layer
            elif layer == len(self.H):
                for index_o_node in range(len(self.O)):
                    var_sum = 0
                    for index_h_node in range(len(self.H[layer - 1])):
                        var_sum += self.W[layer][index_h_node * len(self.O) + index_o_node] * self.H[-1][index_h_node]
                    var_sum += self.B[layer][index_o_node]
                    self.O[index_o_node] = self.activation_func(var_sum)
            # hidden layer
            else:
                for index_hj_node in range(len(self.H[layer])):
                    var_sum = 0
                    for index_hi_node in range(len(self.H[layer - 1])):
                        var_sum += self.W[layer][index_hi_node * len(self.H[layer]) + index_hj_node] * \
                                   self.H[layer - 1][index_hi_node]
                    var_sum += self.B[layer][index_hj_node]
                    self.H[layer][index_hj_node] = self.activation_func(var_sum)
        return

    def back_propagation(self):
        delta_weight = []
        for I in range(len(self.W)):
            arr = []
            for j in range(len(self.W[I])):
                arr.append(0)
            delta_weight.append(arr)
        pre_g = []
        for back_layer in range(len(self.W) - 1, -1, -1):
            # output layer
            if back_layer == len(self.H):
                for index_o_node in range(len(self.O)):
                    e = self.O[index_o_node] - self.D[index_o_node]
                    g = self.diff_func(self.O[index_o_node]) * e
                    pre_g.append(g)

                    delta_bias = -1 * self.n * g * 1
                    self.B[back_layer][index_o_node] += delta_bias

                    for index_h_node in range(len(self.H[back_layer - 1])):
                        delta = -1 * self.n * g * self.H[back_layer - 1][index_h_node]
                        delta_weight[back_layer][index_h_node * len(self.O) + index_o_node] = delta
            # hidden connect output layer
            elif len(self.H) - back_layer == 1 and back_layer != 0:
                g_temp = copy.deepcopy(pre_g)
                pre_g.clear()
                for index_hj_node in range(len(self.H[-1])):
                    sum_gw = 0
                    for index_o_node in range(len(self.O)):
                        sum_gw += g_temp[index_o_node] * self.W[-1][index_hj_node * len(self.O) + index_o_node]
                    g = self.diff_func(self.H[-1][index_hj_node]) * sum_gw
                    pre_g.append(g)

                    delta_bias = -1 * self.n * g * 1
                    self.B[back_layer][index_hj_node] += delta_bias

                    for index_hi_node in range(len(self.H[len(self.H) - 2])):
                        delta = -1 * self.n * g * self.H[len(self.H) - 2][index_hi_node]
                        delta_weight[back_layer][index_hi_node * len(self.H[back_layer - 1]) + index_hj_node] = delta
            # hidden layer
            elif back_layer > 0:
                g_temp = copy.deepcopy(pre_g)
                pre_g.clear()
                for index_hj_node in range(len(self.H[back_layer])):
                    sum_gw = 0
                    for index_hk_node in range(len(g_temp)):
                        sum_gw += g_temp[index_hk_node] * self.W[back_layer + 1][
                            index_hj_node * len(self.H[back_layer + 1]) + index_hk_node]
                    g = self.diff_func(self.H[back_layer][index_hj_node]) * sum_gw
                    pre_g.append(g)

                    delta_bias = -1 * self.n * g * 1
                    self.B[back_layer][index_hj_node] += delta_bias

                    for index_hi_node in range(len(self.H[back_layer - 1])):
                        delta = -1 * self.n * g * self.H[back_layer - 1][index_hi_node]
                        delta_weight[back_layer][index_hi_node * len(self.H[back_layer]) + index_hj_node] = delta
            # input layer
            else:
                g_temp = copy.deepcopy(pre_g)
                pre_g.clear()
                if len(self.H) == 1:
                    for index_h_node in range(len(self.H[len(self.H) - 1])):
                        sum_gw = 0
                        for index_o_node in range(len(self.O)):
                            sum_gw += g_temp[index_o_node] * self.W[back_layer][
                                index_h_node * len(self.O) + index_o_node]
                        g = self.diff_func(self.H[back_layer - 1][index_h_node]) * sum_gw
                        pre_g.append(g)

                        delta_bias = -1 * self.n * g * 1
                        self.B[back_layer][index_h_node] += delta_bias

                        for index_i_node in range(len(self.I)):
                            delta = -1 * self.n * g * self.I[index_i_node]
                            delta_weight[back_layer][index_i_node * len(self.H[0]) + index_h_node] = delta
                else:
                    for index_hi_node in range(len(self.H[0])):
                        sum_gw = 0
                        for index_hj_node in range(len(self.H[1])):
                            sum_gw += g_temp[index_hj_node] * self.W[back_layer][
                                index_hi_node * len(self.H[1]) + index_hj_node]
                        g = self.diff_func(self.H[back_layer - 1][index_hi_node]) * sum_gw
                        pre_g.append(g)

                        delta_bias = -1 * self.n * g * 1
                        self.B[back_layer][index_hi_node] += delta_bias

                        for index_i_node in range(len(self.I)):
                            delta = -1 * self.n * g * self.I[index_i_node]
                            delta_weight[back_layer][index_i_node * len(self.H[0]) + index_hi_node] = delta

        for col in range(len(delta_weight)):
            for row in range(len(delta_weight[col])):
                self.W[col][row] += delta_weight[col][row]
        delta_weight.clear()
        self.D.clear()
        return

    def lean(self, statement, input_table):
        lean_count = 0
        for s in range(statement):
            for j in range(len(input_table[0])):
                random_index = random.randint(0, len(input_table[0]) - 1)
                for i in range(len(input_table)):
                    swap = input_table[i][j]
                    input_table[i][j] = input_table[i][random_index]
                    input_table[i][random_index] = swap
            for flop in range(len(input_table[0])):
                self.__get_I_D__(self.tech_table, flop)
                lean_count += 1
                print(lean_count)
                # Feed Forward Step
                self.feed_forward()

                # Back Propagation step
                self.back_propagation()
        return

    def test(self, table):
        print("\n\n\n")
        hit = 0
        print(len(table[0]))
        for row in range(len(table[0])):
            self.__get_I_D__(table, row)
            print(self.I)
            print(self.D)
            # Feed Forward Step
            for layer in range(len(self.W)):
                # input layer
                if layer == 0:
                    for index_h_node in range(len(self.H[0])):
                        var_sum = 0
                        for index_i_node in range(len(self.I)):
                            var_sum += self.W[layer][index_i_node * len(self.H[0]) + index_h_node] * self.I[
                                index_i_node]
                        var_sum += self.B[0][index_h_node]
                        self.H[0][index_h_node] = self.activation_func(var_sum)
                # output layer
                elif layer == len(self.H):
                    for index_o_node in range(len(self.O)):
                        var_sum = 0
                        for index_h_node in range(len(self.H[layer - 1])):
                            var_sum += self.W[layer][index_h_node * len(self.O) + index_o_node] * self.H[-1][
                                index_h_node]
                        var_sum += self.B[layer][index_o_node]
                        self.O[index_o_node] = self.activation_func(var_sum)
                # hidden layer
                else:
                    for index_hj_node in range(len(self.H[layer])):
                        var_sum = 0
                        for index_hi_node in range(len(self.H[layer - 1])):
                            var_sum += self.W[layer][index_hi_node * len(self.H[layer]) + index_hj_node] * \
                                       self.H[layer - 1][index_hi_node]
                        var_sum += self.B[layer][index_hj_node]
                        self.H[layer][index_hj_node] = self.activation_func(var_sum)
            print(self.O)
            print("\n")
            max_label = max(self.O)
            for index in range(len(self.O)):
                if self.O[index] == max_label and self.D[index] == 1:
                    hit += 1
        print(hit)
        print(len(table[0]) - hit)
        return

nN = NeuronNetwork(6)
nN.lean(1000, nN.tech_table)
nN.test(nN.test_table)
print("\nWeight after")
for i in range(len(nN.W)):
    for j in range(len(nN.W[i])):
        print("[" + str(i) + "][" + str(j) + "]" + str(nN.W[i][j]))

print("\nBias after")
for i in range(len(nN.B)):
    for j in range(len(nN.B[i])):
        print("[" + str(i) + "][" + str(j) + "]" + str(nN.B[i][j]))

