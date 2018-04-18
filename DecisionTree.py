import math
import copy
import xlrd
from TreeNode import TreeNode as Node

class DecisionTree:
    __level = 0
    __threshold = 0
    __tech_table = []
    __test_table = []
    __label = []
    __root = None

    def __init__(self, level, threshold, sheet_index):
        self.__level = level
        self.__threshold = threshold
        data = xlrd.open_workbook("Ddata_set.xls")
        sheet = data.sheets()

        # create tech and test table
        # 70::30
        n_tech = int((sheet[sheet_index].nrows - 1) * 0.7)
        # read file in to input table
        for col in range(0, sheet[sheet_index].ncols):
            att = []
            for row in range(0, n_tech + 1):
                att.append(sheet[0].cell(row, col).value)
            self.__tech_table.append(att)

        for col in range(0, sheet[sheet_index].ncols):
            att = []
            for row in range(n_tech + 1, sheet[sheet_index].nrows):
                att.append(sheet[0].cell(row, col).value)
            self.__test_table.append(att)

        # for att in range(0, len(self.__tech_table) - 1):
        #     self.__att_check.append(False)
        self.__label = self.__classifiedAtt__(len(self.__tech_table) - 1, self.__tech_table)
        self.__root = Node(None, None, None)
        self.__generateTree__(0, self.__root, self.__tech_table)
        print("tree is create")
        return

    @staticmethod
    def __classifiedAtt__(att, table):
        temp = copy.copy(table[att])
        temp.pop(0)
        send_att = []
        send_att.append(temp[0])
        while True:
            if len(temp) == 0:
                break
            count = 0
            while True:
                if send_att[count] == temp[0]:
                    temp.pop(0)
                    break
                if count == len(send_att) - 1:
                    send_att.append(temp[0])
                    temp.pop(0)
                    break
                count += 1
        return send_att

    @staticmethod
    def __info__(att_arr):
        arr = copy.copy(att_arr)
        result = 0
        sum = 0
        for temp in range(len(arr)):
            sum += arr[temp]
            arr[temp] += 1

        for value in arr:
            result += (-value / sum * math.log(value / sum, 2))
        return result

    def __attCount__(self, col, x, table, word):
        temp = copy.copy(table)
        if word == "nl":
            count = 0
            for row in range(1, len(temp[col])):
                if x == temp[col][row]:
                    count += 1
            return count

        if word == "l":
            count_list = []
            for time in range(len(self.__label)):
                count_list.append(0)

            for row in range(0, len(temp[col])):
                if x == temp[col][row]:
                    for index in range(0, len(self.__label)):
                        if self.__label[index] == temp[len(temp) - 1][row]:
                            count_list[index] += 1
                            break
            return count_list

    def __infoAtt__(self, att, table):
        result = 0
        attlist = self.__classifiedAtt__(att, table)
        for value in attlist:
            prob = self.__attCount__(att, value, table, "nl") / (len(table[0]) - 1)
            info = self.__info__(self.__attCount__(att, value, table, "l"))
            result += prob * info
        return result

    def __gainAtt__(self, att, table):
        label_arr = []
        for index in self.__label:
            label_arr.append(self.__attCount__(-1, index, table, "nl"))
        return self.__info__(label_arr) - self.__infoAtt__(att, table)

    @staticmethod
    def __cropTable__(att, value, table):
        # head table
        send_table = []
        for time in range(len(table)):
            arr = []
            send_table.append(arr)
            send_table[time].append(table[time][0])

        for row in range(len(table[att])):
            if table[att][row] == value:
                for col in range(len(table)):
                    send_table[col].append(table[col][row])
        send_table.pop(att)
        return send_table

    def __generateTree__(self, cur_level, cur_node, table):
        # root case
        c_arr = []
        if cur_node.parent == None:
            gain_max = self.__threshold
            att_max = -1
            for i in range(0, len(table) - 1):
                gain = self.__gainAtt__(i, table)
                if gain_max < gain:
                    gain_max = gain
                    att_max = i
            cur_node.parent = cur_node
            cur_node.att_split = table[att_max][0]
            path_list = self.__classifiedAtt__(att_max, table)
            for path in path_list:
                child_node = Node(cur_node, None, path)
                t =self.__cropTable__(att_max, path, table)
                c_arr.append(child_node)
                self.__generateTree__(cur_level + 1, child_node, t)
            cur_node.child = c_arr
            return
        # general case
        elif cur_level <= self.__level:
            gain_max = self.__threshold
            att_max = -1
            for att in range(0, len(table) - 1):
                gain = self.__gainAtt__(att, table)  # chain error
                if gain_max < gain:
                    gain_max = gain
                    att_max = att
            cur_node.att_split = table[att_max][0]
            if gain_max == self.__threshold:  # label case
                max_count = 0
                label = None
                for value in self.__label:
                    temp = self.__attCount__(-1, value, table, "nl")
                    if max_count < temp:
                        max_count = temp
                        label = value
                cur_node.label = label
                return
            else:
                path_list = self.__classifiedAtt__(att_max, table)
                for path in path_list:
                    child_node = Node(cur_node, None, path)
                    t = self.__cropTable__(att_max, path, table)
                    c_arr.append(child_node)
                    self.__generateTree__(cur_level + 1, child_node, t)
                cur_node.child = c_arr
                return
        # break case
        else:
            max_count = 0
            label = None
            for value in self.__label:
                temp = self.__attCount__(-1, value, table, "nl")
                if max_count < temp:
                    max_count = temp
                    label = value
            cur_node.label = label
            cur_node.att_split = table[len(table) - 1][0]
            return

    def get_root(self):
        return self.__root

    def prediction(self, arr2D_input, view_node):
        if view_node.label != None:
            return view_node.label
        else:
            for i in range(0, len(arr2D_input) - 1):
                if view_node.att_split == arr2D_input[i][0]:
                    for j in range(0, len(view_node.child)):
                        if view_node.child[j].att_split_value == arr2D_input[i][1]:
                            return self.prediction(arr2D_input, view_node.child[j])
        return None

    def show_tree(self, view_node):
        print(view_node)
        print(view_node.parent.att_split)
        print(view_node.att_split_value)
        print(view_node.att_split)
        if view_node.child != None:
            print("num child " + str(len(view_node.child)))
            for x in view_node.child:
                self.show_tree(x)
        else:
            print("label is " + str(view_node.label))
        return

    def accuracy(self):
        hit = 0
        miss = 0
        for row in range(1, len(self.__test_table[0])):
            print("time " + str(row))
            test_case = []
            for col in range(0, len(self.__test_table)):
                att = []
                att.append(self.__tech_table[col][0])
                att.append(self.__test_table[col][row])
                test_case.append(att)
            result = self.prediction(test_case, self.__root)
            print(result)
            print(test_case[12][1])
            if result == test_case[12][1]:
                hit += 1
            else:
                miss += 1
            print("hit " + str(hit))
            print("miss " + str(miss))
            print("\n")
        acc = (hit/(hit+miss))*100
        print(acc)
        return acc