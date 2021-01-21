#!/usr/bin/env python3

import os
from datetime import date
from datetime import timedelta

# Import the API
from float_api import FloatAPI

# Get access token from environment variable
FLOAT_ACCESS_TOKEN ='8663a032a76cd873nBda6dDfSMib7YX1siw3XuLaz8LXcp9Ug1tryU3GZis='

# Create an API object
api = FloatAPI(FLOAT_ACCESS_TOKEN, 'my_api_demo', 'me@example.org')


# Today
start_date = date.today().isoformat()

# 30 days in the future
end_date = (date.today() + timedelta(days=30)).isoformat()
print(start_date)

def creatTaskForProject(project_id, hours, peopleName, name):
    person = api.create_person(name=peopleName)
    # Create a test task
    task = api.create_task(project_id=project_id,
                           start_date=date.today().isoformat(),
                           end_date=end_date,
                           hours=10,
                           people_id=person['people_id'],
                           name=name)

#creatTaskForProject('4172914',10,'Tanvi','AkkiTask')
#print('task created')
#for p in api.get_all_projects():
#    print(p)



class FloatDotCom:
  "This is a FloatDotCom class"
  def createProject(self,projectName):
    return api.create_project(name=projectName)

  def getAllProjects(self):
      return api.get_all_projects()

  def getAllTask(self):
    return api.get_all_tasks()

 # def deleteTask(self,task_id):
 #     return api.delete_task(task_id)

  def deleteProject(self,project_id):
      return api.delete_project(project_id)

  def updateTaskNotes(self,taskId,notes):
      return api.update_task(task_id = taskId,notes = notes)

  def creatTaskForProject(self,project_id, hours, peopleName, name):
    person = api.create_person(name=peopleName)
    # Create a test task
    task = api.create_task(project_id=project_id,
                           start_date=date.today().isoformat(),
                           end_date=date.today().isoformat(),
                           hours=10,
                           people_id=person['people_id'],
                           name=name
                           )
    print('task created')



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







#creatTaskForProject1('','','','')

#print("\nPeople:")
#for p in api.get_all_people(fields='name,people_id'):
#  print(p)

#print("\nPeople reports:")
#for r in api.get_people_reports(start_date, end_date):
#   print(r)

#print("\nProjects:")
#for p in api.get_all_projects():
#  print(p)

#print("#\List of Projects")
#f = set(['name', 'project_id'])
#projects = api.get_all_projects(fields=','.join(f))
#tasks = api.get_all_tasks()
#project_and_task = []
#for p in projects:
#  print(p)
#  p['task']=[]
#  print(p)
#  for t in tasks:
#    if p['project_id']==t['project_id']:
#       p['task'].append(t)
#  print(p)
#  project_and_task.append(p)






#print("\nProject reports:")
#for r in api.get_project_reports(start_date, end_date):
#  print(r.keys())

#print("\nTasks:")
#for t in api.get_all_tasks(fields='name'):
#  print(t)






#print("\n Create Tasks:")
  # Create a test person
#  person = api.create_person(name='Akki')
  # Create a test task
#  task = api.create_task(
#      project_id = 4148262,
#    start_date = date.today().isoformat(),
#    end_date = date.today().isoformat(),
#    hours = 10,
#    people_id = person['people_id'],
#    name='taskArpana'
#   )
# print('task created')


#print("\nAll clients:")
#for c in api.get_all_clients():
#  print(c)

#print("\nAll departments:")
#for d in api.get_all_departments():
#  print(d)

#print("\nAll accounts:")
#for a in api.get_all_accounts():
#  print(a)

# Create a project
#project = api.create_project(name='Project FooBar ')
#print(project)

# Delete a project
#result = api.delete_project(project['project_id'])
#print(result)

# Create a client
#client = api.create_client(name="Client FooBar")
#print(client)

# Delete a client
#result = api.delete_client(client['client_id'])
#print(result)

