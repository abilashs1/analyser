'''
Created on Oct 11, 2019

@author: AbilashS2
'''
import os
import csv
from performanceData import PerformanceData

base_log_path = os.path.join("c:/", "VFI", "logs")
  
def createConfigFile(rows):    
        fileName = os.path.join(base_log_path, 'performance_data.csv')
        with open(fileName, 'w', newline='') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=',',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for row in rows:
                if (len(row) > 0):
                    filewriter.writerow(row)

def conver_info_to_csv(perfDataList):
    rows = list()
    if (len(perfDataList) > 0):
        rows.append(perfDataList[0].get_header_list())
        
        for perfData in perfDataList:            
            rows.append(perfData.get_data_in_list())
    createConfigFile(rows)