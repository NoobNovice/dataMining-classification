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
    h = [[0, 0]]
    w = [[0.3, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.3], [0.1, 0.2, 0.1, 0.2]]
    b = [[0.2, 0.4], [0.1, 0.2]]
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
        y_diff = y(1-y)
        return y_diff

    # def lean(self, time):
    #     for t in range(time):
    #         # Feed Forward Step
    #         for layer in range(len(self.W)):
    #             # input layer
    #             if layer == 0:
    #                 for index_h_node in range(len(self.H[0])):
    #                     var_sum = 0
    #                     for index_i_node in range(len(self.I)):
    #                         var_sum += self.W[layer][index_i_node * len(self.H[0]) + index_h_node] * self.I[index_i_node]
    #                     var_sum += self.B[0][index_h_node]
    #                     self.H[0][index_h_node] = self.activation_func(var_sum)
    #             # output layer
    #             if layer == len(self.H[layer]):
    #                 for index_o_node in range(len(self.O)):
    #                     var_sum = 0
    #                     for index_h_node in range(len(self.H[layer - 1])):
    #                         var_sum += self.W[layer][index_h_node * len(self.O) + index_o_node] * self.H[-1][index_h_node]
    #                     var_sum += self.B[layer][index_o_node]
    #                     self.O[index_o_node] = self.activation_func(var_sum)
    #             else:
    #                 for index_hj_node in range(len(self.H[layer])):
    #                     var_sum = 0
    #                     for index_hi_node in range(len(self.H[layer - 1])):
    #                         var_sum += self.W[layer][index_hi_node * len(self.H[layer]) + index_hj_node] * self.H[layer - 1][index_hi_node]
    #                     var_sum += self.B[layer][index_hj_node]
    #                     self.H[layer][index_hj_node] = self.activation_func(var_sum)
    #
    #         # Back Propagation step
    #     return

    def lean(self, time):
        for t in range(time):
            # Feed Forward Step
            for layer in range(len(self.w)):
                # input layer
                print(layer)
                if layer == 0:
                    for index_h_node in range(len(self.h[0])):
                        var_sum = 0
                        for index_i_node in range(len(self.i)):
                            print(str(self.w[layer][index_i_node * len(self.h[0]) + index_h_node]) + "*" + str(self.i[index_i_node]))
                            var_sum += self.w[layer][index_i_node * len(self.h[0]) + index_h_node] * self.i[index_i_node]
                        var_sum += self.b[0][index_h_node]
                        print(var_sum)
                        self.h[0][index_h_node] = self.activation_func(var_sum)
                        print(self.h[0][index_h_node])
                        print("\n")
                elif layer == len(self.h):
                    for index_o_node in range(len(self.o)):
                        var_sum = 0
                        for index_h_node in range(len(self.h[layer - 1])):
                            print(str(self.w[layer][index_h_node * len(self.h[0]) + index_o_node]) + "*" + str(self.h[-1][index_h_node]))
                            var_sum += self.w[layer][index_h_node * len(self.o) + index_o_node] * self.h[-1][index_h_node]
                        var_sum += self.b[layer][index_o_node]
                        print(var_sum)
                        self.o[index_o_node] = self.activation_func(var_sum)
                        print(self.o[index_o_node])
                        print("\n")
                else:
                    for index_hj_node in range(len(self.h[layer])):
                        var_sum = 0
                        for index_hi_node in range(len(self.h[layer - 1])):
                            print(str(self.w[layer][index_hi_node * len(self.h[layer]) + index_hj_node]) + "*" + str(self.h[layer - 1][index_hi_node]))
                            var_sum += self.w[layer][index_hi_node * len(self.h[layer]) + index_hj_node] * self.h[layer - 1][index_hi_node]
                        var_sum += self.b[layer][index_hj_node]
                        print(var_sum)
                        self.h[layer][index_hj_node] = self.activation_func(var_sum)
                        print(self.h[layer][index_hj_node])
                        print("\n")
            # Back Propagation step
        return

    def test(self, arr_input):
        result = None
        return result

n = NeuronNetwork(0)
n.lean(1)
print(n.h)
print(n.o)