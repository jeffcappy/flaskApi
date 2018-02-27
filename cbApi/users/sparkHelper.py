from collections import OrderedDict

from pyspark.sql import Row, functions
from cbApi import apiSpark

spark = apiSpark


class UserTools():


    #TODO create unit test
    def dataFrameFromListOfDicts(self, data):
        row = self.convertToRows(data)
        df = spark.sparkContext.parallelize(row).toDF()
        df.show()
        #TODO with column for names
        #TODO sort
        return df.collect()

    def convertToRows(self, listOfDicts):
        out = list()
        l = list()
        if type(listOfDicts) is list:
            l = listOfDicts
        else:
            l.append(listOfDicts)
        for d in l:
            out.append(Row(**OrderedDict(d.items())))
        return out


if __name__ == '__main__':
    ut = UserTools()
    data = dict()
    data['firstName'] = 'jeff'
    data['lastName'] = 'cappy'
    data['age'] = '27'

    data2 = dict()
    data2['firstName'] = 'rox'
    data2['lastName'] = 'miller'
    data2['age'] = '29'

    l = [data, data2]
    ut.dataFrameFromListOfDicts(l).show()
