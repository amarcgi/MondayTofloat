#!/usr/bin/env python3

import os
from datetime import date
from datetime import timedelta

# Import the API
from float_api import FloatAPI

# Get access token from environment variable
FLOAT_ACCESS_TOKEN ='f645cd01a48459d3nrycH3Bc3D0MVqB1hHAUjbYPhtj6i7jG+kchvAbwXQo='

# Create an API object
api = FloatAPI(FLOAT_ACCESS_TOKEN, 'my_api_demo', 'me@example.org')


# Today
start_date_float = date.today().isoformat()

# 30 days in the future
end_date_float = (date.today() + timedelta(days=30)).isoformat()

class FloatDotCom:
  "This is a FloatDotCom class"
  def createProject(self,projectName):
    return api.create_project(name=projectName)

  def getAllProjects(self):
      return api.get_all_projects()

  def getAllPeoples(self):
      return api.get_all_people()

  def getAllTask(self):
    return api.get_all_tasks()

  def deleteTask(self,task_id):
      return api.delete_task(task_id)

  def deleteProject(self,project_id):
      return api.delete_project(project_id)

  def updateTaskNotes(self,taskId,notes,assignees_id):
      return api.update_task(task_id = taskId,notes = notes,people_ids=assignees_id)

  def assignTaskToPeople(self,taskId,peopleId):
      res= api.update_task(task_id = taskId,people_id = peopleId)
      print('Updating tasks++++',res)
      return res

  def doesPeopleExistinFloatDotcom(self,peoplesDetails,name):
      for people in peoplesDetails:
           if name==people['name']:
               return people




  def creatTaskForProject(self,project_id, hours, assignees, task_name,start_date,end_date,notes):
    try:
        peoplesDetails=self.getAllPeoples()
        assignees_id=[]

        for each_assignee in assignees:
            person=self.doesPeopleExistinFloatDotcom(peoplesDetails,each_assignee)
            if person is None:
               person = api.create_person(name=each_assignee)
            assignees_id.append(person['people_id'])

        task = api.create_task(project_id=project_id,
                               start_date=start_date,
                               end_date=end_date,
                               hours=hours,
                               people_id=person['people_id'],
                               name=task_name
                               )
        self.updateTaskNotes(task['task_id'],notes, assignees_id)

        #print('task created')
        return task
    except Exception as ex:
        print('ERROR',ex)
        r = api.delete_person(person['people_id'])
        print('ERROR','Creating task for the Project deleting person created',r)


  def getProject(self,name):
      f = set(['name', 'project_id'])
      projects = api.get_all_projects(fields=','.join(f))
      for p in projects:
          if p['name']==name:
              return p


  def getTaskByProject(self,project_id):
      project=api.get_project(project_id)
      tasks = api.get_all_tasks()
      project_and_task = []
      for t in tasks:
        if project['project_id'] == t['project_id']:
           project_and_task.append(t)
      return project_and_task

  def getTaskByName(self,project_id,task_name):
      project_and_task=self.getTaskByProject(project_id)
      for task in project_and_task:
          if task['name']==task_name:
              return task


  def getProjectsAndtask(self):
    f = set(['name', 'project_id'])
    projects = api.get_all_projects(fields=','.join(f))
    project_and_task = []
    tasks = api.get_all_tasks()
    for p in projects:
      p['tasks'] = []
      for t in tasks:
        if p['project_id'] == t['project_id']:
           p['tasks'].append(t)
      project_and_task.append(p)
    return project_and_task