'''
Created on Oct 12, 2019

@author: AbilashS2
'''
from Tools.scripts.finddiv import process
import enum

KEY_START_TIME = 'Transaction Start Time'
KEY_PROCESSING_TIME = 'Transaction Processing Time'
KEY_CARD_ENTRY_MODE = 'Card Entry Mode'
KEY_MERCH_PRINT_TIME = 'Merchant Receipt Print Time'
KEY_CUST_PRINT_TIME = 'Customer Receipt Print Time'
KEY_ONLINE_TXN = 'Communication Mode'
KEY_COMMS_TIME = 'Communication Time'
KEY_TXN_NAME = 'Transaction Name'

class Filter(enum.Enum):
    Magstripe = 1
    ICCContact = 2
    ICCCTLS = 4
    OnlineTxn = 8
    Sale = 16
    Refund = 32
    Void = 64
    All = 128
    
def analyseList(dataList):
    finalList = []
    filter = Filter.All.value   
    addRec = False
    summary = PerformanceData()
    avgPerformanceTime = float()
    
    for data in dataList:        
        if (filter & Filter.All.value):
            print ('All Add')
            addRec = True
        else :
            if (filter & Filter.Magstripe.value):
                addRec = False
                if (data.is_magstripe_txn()):
                    print ("Msr Txn")
                    addRec = True
            if (filter & Filter.ICCContact.value):
                addRec = False
                if (data.is_icc_contact_txn()):
                    print ("Contact Txn")
                    addRec = True
                addRec = True
            if (filter & Filter.ICCCTLS.value):
                addRec = False
                if (data.is_icc_ctls_txn()):
                    print ("CTLS Txn")
                    addRec = True
            if (filter & Filter.OnlineTxn.value):
                addRec = False
                if (data.is_online_txn()):
                    print ("Online TXN")                    
                    addRec = True
            if (filter & Filter.Sale.value):
                addRec = False
                if (data.is_sale_txn()):
                    print ("Online TXN")                    
                    addRec = True
        if (addRec):
            finalList.append(data)
            avgPerformanceTime = avgPerformanceTime + data.get_processing_time()
    if (len(finalList) > 0):
        avgPerformanceTime = avgPerformanceTime / len(finalList)
    summary.set_processing_time(avgPerformanceTime)
    summary.set_card_entry_mode(' ')
    summary.set_transaction_name('Summary')
    summary.set_start_time(' ')
    summary.set_online_transaction(' ')
    finalList.append(summary)
    return finalList

def converToObject(final_txn_data):
    perfDataList = []
    for data in final_txn_data:
        for txn_data in final_txn_data[data]:
                perfData = PerformanceData()
                perfData.translate(txn_data)
                perfDataList.append(perfData)
    
    return analyseList(perfDataList)
 
class PerformanceData(object):
    '''
    classdocs
    '''
    txnName = 'Undefined'
    startTime = 'Undefined'
    processingTime = 0.0
    communicationTime = 0.0
    merchantReceiptPrintTime = 0.0
    customerReceiptPrintTime = 0.0
    commsMode = 'Offline'
    cardEntryMode = 'Not Available'

    def __init__(self):
        '''
        Constructor
        '''                
    def translate(self, data):        
        for field in data:
            if field == 'Info':                
                for content in data[field]:
                    if (content == KEY_START_TIME):
                        self.startTime = self.translate_start_time(data[field][content])
                    if (content == KEY_CARD_ENTRY_MODE):
                        self.cardEntryMode = data[field][content]
                    if (content == KEY_TXN_NAME):
                        self.txnName = data[field][content]
                    if (content == KEY_PROCESSING_TIME):
                        self.processingTime = float(data[field][content])
                    if (content == KEY_COMMS_TIME):
                        self.communicationTime = float(data[field][content])
                    if (content == KEY_CUST_PRINT_TIME):
                        self.customerReceiptPrintTime = float(data[field][content])
                    if (content == KEY_MERCH_PRINT_TIME):
                        self.merchantReceiptPrintTime = float(data[field][content])
                    if (content == KEY_ONLINE_TXN):
                        self.onlineTransaction = data[field][content]
                    
    def translate_start_time(self, startTime):
        newTime = startTime[4:6] + '-' + startTime[6:8] + '-' + startTime[0: 4] + 'T' + startTime[8:10] + ':' + startTime[10:12] + ':' + startTime[12:14]
        return newTime
    
    def get_header_list(self):
        headerList = []
        headerList.append(KEY_TXN_NAME)
        headerList.append(KEY_START_TIME)
        headerList.append(KEY_PROCESSING_TIME)
        headerList.append(KEY_CARD_ENTRY_MODE)
        headerList.append(KEY_COMMS_TIME)
        #headerList.append(KEY_ONLINE_TXN)
        headerList.append(KEY_MERCH_PRINT_TIME)
        headerList.append(KEY_CUST_PRINT_TIME)
        return headerList
    def get_data_in_list(self):
        dataList = []
        dataList.append(str(self.txnName))
        dataList.append(str(self.startTime))
        dataList.append(str(self.processingTime))
        dataList.append(str(self.cardEntryMode))
        dataList.append(str(self.communicationTime))
        #dataList.append(str(self.commsMode))
        dataList.append(str(self.merchantReceiptPrintTime))
        dataList.append(str(self.customerReceiptPrintTime))
        return dataList
    
    def log(self):
        print (KEY_TXN_NAME + ' ' + str(self.txnName))
        print (KEY_START_TIME + ' ' + str(self.startTime))
        print (KEY_PROCESSING_TIME + ' ' + str(self.processingTime))
        print (KEY_CARD_ENTRY_MODE + ' ' + str(self.cardEntryMode))
        print (KEY_COMMS_TIME + ' ' + str(self.communicationTime))
        print (KEY_ONLINE_TXN + ' ' + str(self.onlineTransaction))
        print (KEY_MERCH_PRINT_TIME + ' ' + str(self.merchantReceiptPrintTime))
        print (KEY_CUST_PRINT_TIME + ' ' + str(self.customerReceiptPrintTime))
        
    def set_start_time(self, startTime):
        self.startTime = startTime
        
    def set_processing_time(self, processingTime):
        self.processingTime = processingTime
    
    def set_communication_time(self, communicationTime):
        self.communicationTime = communicationTime
        
    def set_merchant_receipt_time(self, merchReceiptTime):
        self.merchantReceiptPrintTime = merchReceiptTime
    
    def set_customer_receipt_time(self, customerReceiptTime):
        self.customerReceiptPrintTime = customerReceiptTime
    
    def set_online_transaction(self, onlineTxn):
        self.onlineTransaction = onlineTxn
    
    def set_card_entry_mode(self, cardEntryMode):
        self.cardEntryMode = cardEntryMode
    
    def set_transaction_name(self, txnName):
        self.txnName = txnName
        
    def get_start_time(self):
        return self.startTime
        
    def get_processing_time(self):
        return float(self.processingTime)
    
    def get_communication_time(self):
        return self.communicationTime
        
    def get_merchant_receipt_time(self):
        return self.merchantReceiptPrintTime
    
    def get_customer_receipt_time(self):
        return self.customerReceiptPrintTime
    
    def get_online_transaction(self):
        return self.onlineTransaction
    
    def get_card_entry_mode(self, cardEntryMode):
        return self.cardEntryMode
    
    def get_transaction_name(self):
        return self.txnName
    
    def is_online_txn(self):
        return self.commsMode == 'Online'
    
    def is_magstripe_txn(self):        
        if self.cardEntryMode == 'Magstripe':
            return True
        return False        
    
    def is_icc_contact_txn(self):
        if self.cardEntryMode == 'ICCContact':
            return True
        return False
    
    def is_icc_ctls_txn(self):
        if self.cardEntryMode == 'ICCContactless':
            return True
        return False
    
    def is_sale_txn(self):
        if (self.txnName == 'Sale'):
            return True