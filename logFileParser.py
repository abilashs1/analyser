'''
Created on Oct 7, 2019

@author: AbilashS2
'''
import json 
import os
from itertools import compress 
from csvGenerator import conver_info_to_csv, base_log_path
from performanceData import converToObject, KEY_START_TIME, KEY_TXN_NAME, KEY_CARD_ENTRY_MODE, KEY_COMMS_TIME, KEY_CUST_PRINT_TIME, KEY_MERCH_PRINT_TIME, KEY_ONLINE_TXN, KEY_PROCESSING_TIME

FLOW_START_IDENTIFIER = 'TransactionFlowStart'
FLOW_END_IDENTIFIER = 'TransactionFlowComplete'
FLOW_CARD_ENTRY_IDENTIFIER = 'CardEntryMode'
FLOW_MERCHANT_PRINT_IDENTIFIER = 'MerchantCopy'
FLOW_CUSTOMER_PRINT_IDENTIFIER = 'CustomerCopy'
FLOW_COMMUNICATION_IDENTIFIER = 'Communication'

ignoreList = ['Idle', 'Initializing Terminal Please Wait', 'Pfr']

def get_data_from_file(fileName):
    f = open(fileName, "r")
    data = f.read()
    f.close()
    return data

def write_list_to_file(dataList, fileName):
    
    with open(os.path.join(base_log_path, fileName), 'w') as f:
        for item in dataList:
            f.write("%s\n" % item)
            
def derive_file_name(transactionData):
    fileName = ''
    for content in transactionData:
        if content == 'Info':
            for elements in transactionData[content]:                
                fileName = fileName + transactionData[content][elements] + '_' 

    #removing last _ from file name
    if (len(fileName) > 1):
        fileName = fileName[:-1]
    else :
        fileName = 'default'                
    return fileName

def get_json_data(data):
    new_data = data.split("Performance:")
    final_dictionary = dict()
    if (len(new_data) > 1):
        final_data = new_data[1][new_data[1].find("[")+1:new_data[1].find("]")]
        final_dictionary = json.loads(final_data)
        #print (type(final_dictionary))
        #print (final_dictionary)
    return final_dictionary
    
def get_performance_data(transaction):
    transactionInfo = dict()
    transactionData = dict()
    transactionDetails = []
    for records in transaction:
        record = get_json_data(records)
        if (len(record) > 0) :
            for data in record:
                if data == 'Type':
                    if record[data] == 'Info':
                        if 'Stage' in record :
                            if (record['Stage'] == FLOW_END_IDENTIFIER) and 'ProcessingTime' in record and 'TransactionName' in record:
                                transactionInfo[KEY_TXN_NAME] = record['TransactionName']
                                transactionInfo[KEY_PROCESSING_TIME] = record['ProcessingTime']
                            if (record['Stage'] == FLOW_START_IDENTIFIER) and 'TransactionStartTime' in record:
                                transactionInfo[KEY_START_TIME] = record['TransactionStartTime']
                            if (record['Stage'] == FLOW_CARD_ENTRY_IDENTIFIER) and 'CardEntryMode' in record:
                                transactionInfo[KEY_CARD_ENTRY_MODE] = record['CardEntryMode']
                            if (record['Stage'] == FLOW_MERCHANT_PRINT_IDENTIFIER) and 'ProcessingTime' in record:
                                transactionInfo[KEY_MERCH_PRINT_TIME] = record['ProcessingTime']                                
                            if (record['Stage'] == FLOW_CUSTOMER_PRINT_IDENTIFIER) and 'ProcessingTime' in record:
                                transactionInfo[KEY_CUST_PRINT_TIME] = record['ProcessingTime']
                            if (record['Stage'] == FLOW_COMMUNICATION_IDENTIFIER) and 'ProcessingTime' in record:
                                transactionInfo[KEY_COMMS_TIME] = record['ProcessingTime']                                                                
                    if record[data] == 'Details':
                        if 'Step' in record and 'ProcessingTime' in record:
                            transactionDetail = dict()
                            transactionDetail['Step Name'] = record['Step']
                            transactionDetail['Processing Time'] = record['ProcessingTime']
                            transactionDetails.append(transactionDetail)
                            
    transactionData['Info'] = transactionInfo
    transactionData['Details'] = transactionDetails
    
    return transactionData

def translate_data_to_list(info):
    result = ''
    datalist = info.splitlines(0)
    startIndexList = []
    endIndexList = []
    
    for data in datalist:
        if FLOW_START_IDENTIFIER in data and (not any(x in data for x in ignoreList)):
            print ("Start Index")
            print (datalist.index(data))
            startIndex = datalist.index(data)
            startIndexList.append(startIndex)
    
        if FLOW_END_IDENTIFIER in data and (not any(x in data for x in ignoreList)):
            print ("End Index")
            print (datalist.index(data))
            endIndex = datalist.index(data)
            endIndexList.append(endIndex)
    
    resultIndex = list(zip(startIndexList, endIndexList))
    transactions = []
    for startIndex, endIndex in resultIndex:
        transaction = datalist[startIndex:endIndex+1]
        transactions.append(transaction)
        
    data_list = [];
    for transaction in transactions:
        performanceData = get_performance_data(transaction)
        data_list.append(performanceData)
        fileName = derive_file_name(performanceData)
        write_list_to_file(transaction, fileName)
        result = result + str(performanceData) + '\n'
    final_txn_data = dict()        
    final_txn_data['Data'] = data_list;
    
    conver_info_to_csv(converToObject(final_txn_data))
        
def translate_data_to_json(info):
    result = ''
    datalist = info.splitlines(0)
    startIndexList = []
    endIndexList = []
    
    for data in datalist:
        if FLOW_START_IDENTIFIER in data and (not any(x in data for x in ignoreList)):
            #print ("Start Index")
            #print (datalist.index(data))
            startIndex = datalist.index(data)
            startIndexList.append(startIndex)
    
        if FLOW_END_IDENTIFIER in data and (not any(x in data for x in ignoreList)):
            #print ("End Index")
            #print (datalist.index(data))
            endIndex = datalist.index(data)
            endIndexList.append(endIndex)
    
    resultIndex = list(zip(startIndexList, endIndexList))
    transactions = []
    for startIndex, endIndex in resultIndex:
        transaction = datalist[startIndex:endIndex+1]
        transactions.append(transaction)
    
    data_list = [];
    for transaction in transactions:
        performanceData = get_performance_data(transaction)
        data_list.append(performanceData)
        fileName = derive_file_name(performanceData)
        write_list_to_file(transaction, fileName)
        result = result + str(performanceData) + '\n'
    final_txn_data = dict()        
    final_txn_data['Data'] = data_list;
    
    conver_info_to_csv(converToObject(final_txn_data))
    return result