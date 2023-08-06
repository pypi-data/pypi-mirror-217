from . import query,Sobjects
import time

def complete_orchestration_plan(orderId):

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

        active = [r for r in res2['records'] if r['vlocity_cmt__State__c'] in ['Fatally Failed',"Failed"]]
        if len(active) == 0:
            time.sleep(5)
     #       finished = True
     #       continue

        for r in active:
            print(f"{r['Name']} {r['vlocity_cmt__State__c']}")
            data = {
                'vlocity_cmt__State__c':'Completed'
            }
            rr = Sobjects.update(r['Id'],data,sobjectname='vlocity_cmt__OrchestrationItem__c')
        
def waitfor_orchestration_plan(orderId):
    q_plan = f"select fields(all) from vlocity_cmt__OrchestrationPlan__c where vlocity_cmt__OrderId__c = '{orderId}'  limit 100"

    finished = False
    iterations = 0
    while finished == False and iterations<10:
        res = query.query(q_plan)
        iterations = iterations + 1 

        if len(res['records']) == 0:
            time.sleep(10)
        else:
            finished = True
            
     
