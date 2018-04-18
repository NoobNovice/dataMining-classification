import xlrd
import xlwt
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
        wdatafile.save("data_set.xls")
        return

FoldChange()