import xlrd
import xlwt
import copy
import random as rm

class FoldChange:
    __table = []
    __rows = 0
    __cols = 0

    def __init__(self):
        # open write file excel
        wdatafile = xlwt.Workbook(encoding="utf-8")

        # open read file excel
        datafile = xlrd.open_workbook('original_dataset.xls')
        rsheet = datafile.sheets()

        self.__rows = rsheet[0].nrows
        self.__cols = rsheet[0].ncols

        # read file in to input table
        for col in range(0, self.__cols):
            att = []
            for row in range(0, self.__rows):
                att.append(rsheet[0].cell(row, col).value)
            self.__table.append(att)


        # # preprocess data
        # for col in range(0, 10):
        #     bound_list = self.__bound__(self.__table[col])
        #     for row in range(1, self.__rows):
        #         if self.__table[col][row] >= bound_list[0] and self.__table[col][row] <= bound_list[1]:
        #             self.__table[col][row] = 1
        #         elif self.__table[col][row] >= bound_list[1] and self.__table[col][row] <= bound_list[2]:
        #             self.__table[col][row] = 2
        #         else:
        #             self.__table[col][row] = 3

        # random row and write in new file
        for count in range(0, 10):
            wsheet = wdatafile.add_sheet("sheet" + str(count))
            for time in range(1, self.__rows):
                index = rm.randint(1, self.__rows - 1)
                print(index)
                for col in range(0, self.__cols):
                    swap = self.__table[col][time]
                    self.__table[col][time] = self.__table[col][index]
                    self.__table[col][index] = swap

            for row in range(0, self.__rows):
                for col in range(0, self.__cols):
                    wsheet.write(row, col, self.__table[col][row])
        wdatafile.save("Ndata_set.xls")
        return

    def __bound__(self, att_arr):
        send_bound = []
        arr = copy.copy(att_arr)
        arr.pop(0)
        low = min(arr)
        high = max(arr)
        range_arr = (high - low) / 3
        for i in range(0, 3):
            low += range_arr
            send_bound.append(low)
        return send_bound

FoldChange()