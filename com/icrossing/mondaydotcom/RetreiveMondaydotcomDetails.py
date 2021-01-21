import requests
import json
from com.icrossing.floatdotcom.RetriveFloatdotcomDetails import FloatDotCom

apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjkzNDgwNDM3LCJ1aWQiOjE3NjQ5MTY1LCJpYWQiOiIyMDIwLTEyLTE0VDE1OjUwOjMzLjAwMFoiLCJwZXIiOiJtZTp3cml0ZSJ9.UrBAf9KTn-UkyBM2LvrRjWICBwqWWarB5DooSWvM_2s"
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey}

query = '{boards  { name id  items { name column_values{title id type text } } } }'
data = {'query': query}

r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
resp = r.json()
print(resp)
mondayDotComeboard = resp['data']['boards']
print('Monday Dot come Boards')
print(mondayDotComeboard)
# 843502442
floatdotCom = FloatDotCom()
print('Float Dot come Taskes')
floatdotComProjectAndTask = floatdotCom.getProjectsAndtask()
print(floatdotComProjectAndTask)


# Find the logic to new Board added in Monday.com
def addNewBoardMondaydotcom():
    for monBoardName in mondayDotComeboard:
        matcheBoardName = False
        matchFloatDotcomeProjectname = None
        for project in floatdotComProjectAndTask:
            if project['name'] == monBoardName['name']:
                print('matched', monBoardName['name'])
                matcheBoardName = True
                matchFloatDotcomeProjectname = project
                break
        if matcheBoardName:
            print('Matched Board name with float Project ', monBoardName['name'])
            print('Item in mondaydotcom ', monBoardName['items'])
            print('Task in floatdotcome ', matchFloatDotcomeProjectname['tasks'])
            monBroardItems = monBoardName['items']
            floatdotComTasks = matchFloatDotcomeProjectname['tasks']

            # Item addedd
            for item in monBroardItems:
                itemMatched = False
                for task in floatdotComTasks:
                    if item['name'] == task['name']:
                        itemMatched = True
                        break
                if not itemMatched:
                    print('Item added', item)
                    personName = None
                    for boardItemDetails in item['column_values']:
                        if boardItemDetails['type'] == 'person':
                            personName = boardItemDetails['text']
                    floatdotCom.creatTaskForProject(matchFloatDotcomeProjectname['project_id'], 10, personName,
                                                    item['name'])
                    print('Task added to Project FloatDotcome', item['name'], matchFloatDotcomeProjectname['name'])

            # Item deleted
            for task in floatdotComTasks:
                itemMatched = False
                for item in monBroardItems:
                    if item['name'] == task['name']:
                        itemMatched = True
                        break
                if not itemMatched:
                    print('Task is going deleted', task)
                    floatdotCom.deleteTask(task['task_id'])
                    print('Task deleted from FloatDotcome', task)


            # item Attribute Updated
            for boardItem in monBroardItems:
                for task in floatdotComTasks:
                    if boardItem['name'] == task['name']:
                        boardItemNotes = None
                        for boardItemDetails in boardItem['column_values']:
                            if boardItemDetails['title'] == 'Notes':
                                boardItemNotes = boardItemDetails['text']
                        flotDotcomTaskNotes = task['notes']
                        if boardItemNotes != flotDotcomTaskNotes:
                            print('task Id', task['task_id'], ' boardItemNotes ', boardItemNotes)
                            floatdotCom.updateTaskNotes(task['task_id'], boardItemNotes)
                            print('Updated Notes in Floatdotcome')

        if not matcheBoardName:
            print('New Board added in Mondaydotcom', monBoardName['name'])
            created_project = floatdotCom.createProject(monBoardName['name'])
            print('Project Created FloatDotcom', created_project)
            # {'project_id': 4151402, 'name': 'Tanvi', 'client_id': None, 'color': '0095D8', 'notes': None, 'tags': [], 'non_billable': 0, 'budget_type': 0, 'budget_total': None, 'default_hourly_rate': None, 'tentative': 0, 'active': 1, 'project_manager': 552143, 'all_pms_schedule': 0, 'created': '2020-11-16 10:46:25', 'modified': '2020-11-16 10:46:25'}
            for boardItem in monBoardName['items']:
                print('New Board Item', boardItem['name'])
                personName = ''
                for boardItemDetails in boardItem['column_values']:
                    if boardItemDetails['type'] == 'person' or boardItemDetails['multiple-person']:
                        personName = boardItemDetails['text']
                floatdotCom.creatTaskForProject(created_project['project_id'], 10, personName, boardItem['name'])
                print('Created  Task in FloatDoctcom', boardItem['name'])


def deleteBoardMondaydotcom():
    # Find the logic to  Deleted Board in Monday.com
    print('Deleted Items*************')
    for project in floatdotComProjectAndTask:
        matched = False
        for monBoardName in mondayDotComeboard:
            if project['name'] == monBoardName['name']:
                print('matched', monBoardName['name'])
                matched = True
                break
        if not matched:
            print('Deleted Board in Mondaydotcom', project)
            floatdotCom.deleteProject(project['project_id'])
            print('Deleted project in Floatdotcom', project)
            # for projectTask in project['tasks']:
            #    print('Deleted Task Id ', projectTask['task_id'], ' projectId ', projectTask['project_id'])


addNewBoardMondaydotcom()
deleteBoardMondaydotcom()


def addedItem(l1, l2):
    for monBoardName in l1:
        matcheBoardName = False
        matchFloatDotcomeProjectname = None
        for project in l2:
            if project['name'] == monBoardName['name']:
                print('matched', monBoardName['name'])
                matcheBoardName = True
                matchFloatDotcomeProjectname = project
                break
        if not matcheBoardName:
            print('New Board added in Mondaydotcom', monBoardName['name'])
            created_project = floatdotCom.createProject(monBoardName['name'])
            print('Project Created FloatDotcom', created_project)
            # {'project_id': 4151402, 'name': 'Tanvi', 'client_id': None, 'color': '0095D8', 'notes': None, 'tags': [], 'non_billable': 0, 'budget_type': 0, 'budget_total': None, 'default_hourly_rate': None, 'tentative': 0, 'active': 1, 'project_manager': 552143, 'all_pms_schedule': 0, 'created': '2020-11-16 10:46:25', 'modified': '2020-11-16 10:46:25'}
            for boardItem in monBoardName['items']:
                print('New Board Item', boardItem['name'])
                personName = ''
                for boardItemDetails in boardItem['column_values']:
                    if boardItemDetails['type'] == 'person' or boardItemDetails['multiple-person']:
                        personName = boardItemDetails['text']
                floatdotCom.creatTaskForProject(created_project['project_id'], 10, personName, boardItem['name'])
                print('Created  Task in FloatDoctcom', boardItem['name'])

#    if item['name']=='AmarBoard1':
#        floatdotCom.createProject(item['name'])
#        print('Created Project In float.com=',item['name'])
