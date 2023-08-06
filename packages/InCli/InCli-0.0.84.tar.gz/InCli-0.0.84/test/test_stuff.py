import unittest
from InCli.SFAPI import restClient,CPQ,account,Sobjects,utils,query,jsonFile,debugLogs
import traceback


class Test_Stuff(unittest.TestCase):

  def test_update_order_items(self):
    restClient.init("NOSQSM")
    time ='2023-05-30T14:06:57.000+0000'

    q = "select Id,vlocity_cmt__CatalogItemReferenceDateTime__c from orderitem  where orderid = '8017a000002kYQqAAM' limit 100 "

    res = query.query(q)

    for item in res['records']:
      data = {
        'vlocity_cmt__CatalogItemReferenceDateTime__c' : None
      }
      res2 = Sobjects.update(item['Id'],data)

    a=1
     