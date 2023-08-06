import unittest,simplejson
from InCli.SFAPI import restClient,query,Sobjects

class Test_Utilities(unittest.TestCase):
    def test_limits(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0/limits'
        res = restClient.callAPI(action)

        print()


    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)

        print()

    def test_id(self):
        restClient.init('DEVNOSCAT2')
        action = '/services/data/v51.0'
        res = restClient.callAPI(action)
        for key in res.keys():
            print()
            action = res[key]
            res1 = restClient.callAPI(action)
            print(action)
            print(res1)

        print()
    
    def test_select(self):
        restClient.init('DEVNOSCAT4')

        q = f"select fields(all) from vlocity_cmt__VlocityTrackingEntry__c order by vlocity_cmt__Timestamp__c desc limit 100"
        res = query.query(q)
        for r in res['records']:
            ll = simplejson.loads(r['vlocity_cmt__Data__c'])
            json_formatted_str = simplejson.dumps(ll, indent=2, ensure_ascii=False)
            print(json_formatted_str)
            print()
    def test_delete_logs(self):
        restClient.init('NOSDEV')

        userId = Sobjects.IdF('User','username:uormaechea_nosdev@nos.pt')

        q = f"select Id from ApexLog where LogUserId='{userId}' "
        res = query.query(q)

        id_list = [record['Id'] for record in res['records']]
        
        Sobjects.deleteMultiple('ApexLog',id_list)
        print()

    def delete(self,q):
        res = query.query(q)

        id_list = [record['Id'] for record in res['records']]
        
        Sobjects.deleteMultiple('ApexLog',id_list)
        print()

    def test_delete_something(self):
        restClient.init('NOSDEV')

        delete = True
        accountId = '0013O00001CX2VzQAL'

        q0 = f"select ID from asset where AccountId = '{accountId}'"
        res0 = query.query(q0)

        q1 = f"select Id from vlocity_cmt__InventoryItem__c where vlocity_cmt__GasPressureLevel__c != null and vlocity_cmt__AccountId__c = '{accountId}' limit 100 "
        print(q1)
        res = query.query(q1)

        itemIds = [r['Id'] for r in res['records']]

        q2 = f"select Id from vlocity_cmt__InventoryItemDecompositionRelationship__c where Name like 'CLONING%' and vlocity_cmt__DestinationInventoryItemId__c in ({query.IN_clause(itemIds)}) limit 100 "
        print(q2)
        res2 = query.query(q2)

        if delete: self.delete(q2)
        if delete: self.delete(q1)
        if delete: self.delete(q0)

        s=1

    def test_getAssret(self):
        q = f"select fields(all) from asset where vlocity_cmt__RootItemId__c='{assetId}' limit 200"

    def test_delete_fulfil(self):
        restClient.init('DEVNOSCAT4')

        q = "select Id from vlocity_cmt__FulfilmentRequestDecompRelationship__c  "
        self.delete(q)

        q = "select Id from vlocity_cmt__FulfilmentRequestLineDecompRelationship__c  "
        self.delete(q)
        
        q = "select Id from vlocity_cmt__FulfilmentRequest__c  "
        self.delete(q)

        q = "select Id from vlocity_cmt__InventoryItem__c  "
        self.delete(q)

        q = "select Id from vlocity_cmt__InventoryItemDecompositionRelationship__c  "
        self.delete(q)

        q = "select Id from AssetRelationship  "
        self.delete(q)

        q = "select Id from vlocity_cmt__OrderAppliedPromotionItem__c  "
        self.delete(q)

    def test_call_something(self):
        restClient.init('NOSQSM')

       # res = restClient.requestWithConnection(action='resource/1641908190000/vlocity_cmt__OmniscriptLwcCompiler')
        res = restClient.requestRaw('https://nos--nosqms.sandbox.my.salesforce.com/resource/1641908190000/vlocity_cmt__OmniscriptLwcCompiler')

        print(res)
        print()

        

    def test_iJoin_code(self):
        restClient.init('NOSQSM')

        name = 'd9b0fe97-8d5a-b2b6-8293-f5abe8f4b675'

        q = f"select name, Content__c from Dataframe__c where name ='{name}' "

        res = query.query(q)

        print(res['records'][0]['Content__c'])
       # print(res)
        print()

    def test_update_something(self):
        restClient.init('NOSQSM')

        Sobjects.update()

    def test_inventory_stuff(self):
        restClient.init('NOSDEV')

        accountId ='0013O00001B0lHvQAJ'

        q = f"select fields(all) from asset where accountid='{accountId}' limit 100"

        call = query.query(q)

        assetIds = [asset['Id'] for asset in call['records']]

        q = f"select fields(all) from vlocity_cmt__InventoryItemDecompositionRelationship__c where vlocity_cmt__SourceAssetId__c in ({query.IN_clause(assetIds)}) limit 100"

        call2 = query.query(q)

        sourceInventoryItemIds = [rel['vlocity_cmt__SourceInventoryItemId__c'] for rel in call2['records'] if rel['vlocity_cmt__SourceInventoryItemId__c']!=None]
        destinationInventoryItemIds = [rel['vlocity_cmt__DestinationInventoryItemId__c'] for rel in call2['records'] if rel['vlocity_cmt__DestinationInventoryItemId__c'] != None]

        q = f"select fields(all) from vlocity_cmt__InventoryItem__c where Id in ({query.IN_clause(destinationInventoryItemIds)}) limit 100"

        call3 = query.query(q)

        q= f"select fields(all) from vlocity_cmt__InventoryItem__c  where vlocity_cmt__AccountId__c='{accountId}' limit 100"

        call4 = query.query(q)

        a=1