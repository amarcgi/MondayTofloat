import requests
import json
from com.icrossing.floatdotcom.FloatDotComDetails import FloatDotCom
from datetime import date
from datetime import timedelta
from monday import MondayClient
floatDotCom = FloatDotCom()

class MondayDotcom:

    def fetchMondayDotComDetsils(self):
        apiKey = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjk0Mzk1MTU1LCJ1aWQiOjE3ODI0MzE3LCJpYWQiOiIyMDIwLTEyLTI5VDAzOjE4OjI3LjAwMFoiLCJwZXIiOiJtZTp3cml0ZSIsImFjdGlkIjo3ODE1NzM5LCJyZ24iOiJ1c2UxIn0.cN8GBBYH4tJupyyzI5DFWsKbsnB84WxAmdiIxEyN9Cg"
        apiUrl = "https://api.monday.com/v2"
        headers = {"Authorization": apiKey}
        global monday
        monday = MondayClient(apiKey)

        query = '{boards  { name id  items { name id column_values{title id type text } } } }'
        data = {'query': query}

        r = requests.post(url=apiUrl, json=data, headers=headers)  # make request
        resp = r.json()
        print(resp)
        global mondayDotCom
        mondayDotCom = resp['data']['boards']
        print('Monday Dot come Boards')
        print(mondayDotCom)
        return mondayDotCom


    def updateFlotDotComTask(self,monDashBoard, project_id, project_name):
        for item in monDashBoard['items']:
            print('Item name', item)
            task_owner = None
            hours = None
            start_date = None
            end_date = None
            notes = None
            task_name = item['name']
            integration_Status=None

            for item_columns in item['column_values']:
                # print('item_column',item_columns)
                # project_id, hours, task_owner, name,start_date,end_date
                # print(createdFloatProject['id'])
                # print(createdFloatProject['name'])
                if item_columns['title'] == 'Task Owner':
                    # print('task_owner', item_columns['text'])
                    splitter=', '
                    task_owner = item_columns['text'].split(splitter) if ', ' in item_columns['text'] else [item_columns['text']]
                    #print(f'task_owner===={task_owner}')
                elif item_columns['title'] == 'Status':
                    pass
                    # print('Status', item_columns['text'])

                elif item_columns['id'] == 'timeline':
                    # print('Duration Start Date', item_columns['text'])
                    splitter=' - '
                    time_range=item_columns['text'].split(splitter)
                    start_date = time_range[0]
                    end_date= time_range[1]

                elif item_columns['title'] == 'Notes':
                    # print('Notes', item_columns['text'])
                    notes = item_columns['text']

                elif item_columns['title'].lower() == 'Hours per Day'.lower():
                    # print('TotalHours', item_columns['text'])
                    hours = item_columns['text']

                elif item_columns['title'] == 'Button':
                    pass
                    # print('Button', item_columns['text'])

                elif item_columns['title'] == 'Integration Status':
                    integration_Status=item_columns['text']
                    integration_Status_Column_id=item_columns['id']

            if integration_Status=='SenttoFloat':
                taskExist=floatDotCom.getTaskByName(project_id,task_name)
                if taskExist is not None:
                    floatDotCom.deleteTask(taskExist['task_id'])
                    print('+++deleting task',taskExist['name'])
                floatProjectTask = floatDotCom.creatTaskForProject(project_id, hours, task_owner, task_name,
                                                                   start_date, end_date, notes)
                print('task created++++', project_id, hours, task_owner, task_name, start_date, end_date)
                board_id = monDashBoard['id']
                item_id = item['id']
                column_id = integration_Status_Column_id

                if floatProjectTask is None:
                    raise Exception('Could not able to create Task under Project')
                self.updateMondayDotcomItemColumn(board_id, item_id, column_id, {"label":"AddedtoFloat"})
            print('*' * 10)


    def updateMondayDotcomDetails(self,mondayDotComDetails):
        projects = floatDotCom.getAllProjects()
        for p in projects:
            mondayDotComDashBoard = self.getMondayDotComDashBoardByName(p['name'],mondayDotComDetails)
            if mondayDotComDashBoard is not None:
                tasks = floatDotCom.getTaskByProject(p['project_id'])
                for task in tasks:
                    dashBoardItem = self.getMondayDotComDashBoardItemByBoardIdAndItemName(
                        mondayDotComDashBoard['id'], task['name'],mondayDotComDetails)
                    if dashBoardItem is None:
                        floatDotCom.deleteTask(task['task_id'])
                        print(f"Monday Item {task['name']} under DashBoard { mondayDotComDashBoard['name'] } Got deleted")



    def getMondayDotComDashBoardByName(self, board_name,mondayDotComDetails):
        #mondayDashBoards = self.getMondayDotComDashBoard()
        for dashBoard in mondayDotComDetails:
            if dashBoard['name'] == board_name:
                return dashBoard

    def getMondayDotComDashBoard(self):
        return monday.boards.fetch_boards()

    def getMondayDotComDashBoardItem(self, board_id):
        dashBoardItems = monday.boards.fetch_items_by_board_id(board_id)
        for board in dashBoardItems['data']['boards']:
            return board['items']

    def getMondayDotComDashBoardItemByBoardIdAndItemName(self, board_id, item_name,mondayDotComDetails):
        #items = self.getMondayDotComDashBoardItem(board_id)
        for each_board in mondayDotComDetails:
            if each_board['id']==board_id:
                for item in  each_board['items']:
                    if item['name'] == item_name:
                        return item


        #for item in items:
            # print('item',item)
        #    if item['name'] == item_name:
        #       return item


    def deletProjectsFromFloat(self):
        floatProject = floatDotCom.getAllProjects()
        for project in floatProject:
            floatDotCom.deleteProject(project['project_id'])
            project_name=project['name']
            print(f'deleted project {project_name} from floatdotcom')

    def createProjecFloatDotcom(self):
        for monDashBoard in mondayDotCom:
            #create only project conatisn Float
            print('*********Started creating project*********',monDashBoard['name'])
            if monDashBoard['name'].find("Float")!=-1:
                existFloatProject=floatDotCom.getProject(monDashBoard['name'])
                if existFloatProject is None:
                    createdFloatProject= floatDotCom.createProject(monDashBoard['name'])
                    print('Project created', createdFloatProject)
                else:
                    createdFloatProject=existFloatProject
                    print(createdFloatProject['name'], 'Already exist in Float dot com')
                project_id = createdFloatProject['project_id']
                project_name = createdFloatProject['name']
                #created/Updated Dashboard item in Monday dot com
                self.updateFlotDotComTask(monDashBoard,project_id,project_name)
            print('*********Finished creating project*********')






    def updateMondayDotcomItemColumn(self,board_id, item_id, column_id, column_value):
        #print('board_id',board_id,'item_id',item_id,'column_id ',column_id,'column_value ',column_value)
        r=monday.items.change_item_value(board_id, item_id, column_id, column_value)
        print('Monday item updated+++',r)


