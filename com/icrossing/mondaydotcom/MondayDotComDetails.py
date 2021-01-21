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





    def updateFlotDotComTask(self,monDashBoard, project_id, project_name):
        for item in monDashBoard['items']:
            print('Item name', item)
            assignee = None
            hours = None
            start_date = None
            end_date = None
            notes = None
            task_name = item['name']
            integration_Status=None

            for item_columns in item['column_values']:
                # print('item_column',item_columns)
                # project_id, hours, assignee, name,start_date,end_date
                # print(createdFloatProject['id'])
                # print(createdFloatProject['name'])
                if item_columns['title'] == 'Assignee':
                    # print('Assignee', item_columns['text'])
                    splitter=', '
                    assignee = item_columns['text'].split(splitter) if ', ' in item_columns['text'] else [item_columns['text']]
                    #print(f'Assignee===={assignee}')
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
                floatProjectTask = floatDotCom.creatTaskForProject(project_id, hours, assignee, task_name,
                                                                   start_date, end_date, notes)
                print('task created++++', project_id, hours, assignee, task_name, start_date, end_date)
                board_id = monDashBoard['id']
                item_id = item['id']
                column_id = integration_Status_Column_id

                if floatProjectTask is None:
                    raise Exception('Could not able to create Task under Project')
                self.updateMondayDotcomItemColumn(board_id, item_id, column_id, {"label":"AddedtoFloat"})
            print('*' * 10)


    def pushDataFromMondayToFloat(self):
        for monDashBoard in mondayDotCom:
            floatProject = floatDotCom.getProject(monDashBoard['name'])
            #Add New Project in float dot com
            if floatProject is None:
                try:
                    createdFloatProject = floatDotCom.createProject(monDashBoard['name'])
                    print('Project created float dot com', createdFloatProject)
                    project_id = createdFloatProject['project_id']
                    project_name = createdFloatProject['name']
                    # get monday dashboard items
                    self.updateFlotDotComTask(monDashBoard,project_id,project_name)
                except Exception as ex:
                    print('ERROR as', ex)
                    print('Something went wrong while creating Task for  Project', project_name)
                    floatDotCom.deleteProject(project_id)
            #Update Existing Project
            if floatProject is not None:
                try:
                    print('Project already exist in float dot com', floatProject)
                    createdFloatProject = floatProject
                    project_id = createdFloatProject['project_id']
                    project_name = createdFloatProject['name']
                    project_task=floatDotCom.getTaskByProject(project_id)
                    for task in project_task:
                        #print('Delete exiting Task for Project from floatDotcom',task)
                        floatDotCom.deleteTask(task['task_id'])
                        taskName=task['name']
                        print(f'Deleted exiting Task {taskName} for Project {project_name} from floatDotcom')
                    # get monday dashboard items
                    self.updateFlotDotComTask(monDashBoard, project_id, project_name)
                except Exception as ex:
                    print('ERROR as', ex)
                    print('Something went wrong while creating Task for updating Project', project_name)

            #Delete the floatdotcomeProject



    def deletProjectsFromFloat(self):
        floatProject = floatDotCom.getAllProjects()
        for project in floatProject:
            floatDotCom.deleteProject(project['project_id'])
            project_name=project['name']
            print(f'deleted project {project_name} from floatdotcom')

    def createProjecFloatDotcom(self):
        for monDashBoard in mondayDotCom:
            #create only project conatisn Float
            print('*********Started creating project*********')
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


