import unittest
from InCli import InCli
from InCli.SFAPI import restClient,query,Sobjects

class Test_OM(unittest.TestCase):
    def test_main(self):
        restClient.init('NOSDEV')

        orchestrationPlanId = 'a453O000000FBKLQA4'
        orderId = '8013O000003mfcPQAQ'

        finished = False
        while finished == False:
            q_plan = f"select fields(all) from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = '{orderId}'  limit 100"

            res = query.query(q_plan)

            if res['records'][0]['vlocity_cmt__State__c'] == 'Completed':
                finished = True
                continue

            orchestrationPlanId = res['records'][0]['Id']

            q = f"select fields(all) from vlocity_cmt__OrchestrationItem__c where vlocity_cmt__OrchestrationPlanId__c = '{orchestrationPlanId}'  limit 200"

            res2 = query.query(q)

            active = [r for r in res2['records'] if r['vlocity_cmt__State__c'] in ['Fatally Failed']]
            for r in active:
                print(f"{r['Name']} {r['vlocity_cmt__State__c']}")
                data = {
                    'vlocity_cmt__State__c':'Completed'
                }
                rr = Sobjects.update(r['Id'],data,sobjectname='vlocity_cmt__OrchestrationItem__c')
                a=1
            

        a=1
        
