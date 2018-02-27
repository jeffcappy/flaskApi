from pyspark.sql import SparkSession,Row
from collections import OrderedDict


spark = SparkSession.builder \
    .master('local') \
    .appName('cbApi') \
    .getOrCreate()
    

class UserTools():

    def dataFrameFromListOfDicts(self,data):
	row = self.convertToRows(data)
        df = spark.sparkContext.parallelize(row).toDF()
        #df.show()
        return df

    def convertToRows(self,listOfDicts):
        out = list()
        for d in listOfDicts:
	    out.append(Row(**OrderedDict(d.items())))
        return out

    def dataFromeFromDict(self,data):
        pass

    def convetToRow(self,myDict):
        pass


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
    
    l = [data,data2]
    ut.dataFrameFromListOfDicts(l).show()
