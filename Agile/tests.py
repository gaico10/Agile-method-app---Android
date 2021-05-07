from django.test import TestCase,SimpleTestCase
from django.urls import reverse, resolve
from Agile.views import *

class Test(SimpleTestCase):
    
    def test_SignUp_DBInsert(self):
        SV = db.users
        SV.delete_many({"ID" : "Guyco070", "EMAIL": "gaico070@gmail.com"})
        SV.delete_many({"ID" : "", "EMAIL": ""})
        user = {
            "ID": "Guyco070",
            "PASSWORD": 123456,
            "EMAIL": "gaico070@gmail.com",
            "TYPE" : "Admin",
        }
        SV.insert_one(user)
        client.close()
        is_user_inserted = SV.find_one(user) != None
        self.assertTrue(is_user_inserted)
    
    def test_LOGIN_DBFind_true(self):
        is_user_Exist = db.users.find_one({
            "ID": "Guyco070",
            "PASSWORD": 123456,
            "EMAIL": "gaico070@gmail.com",
            "TYPE" : "Admin",
        }) != None
        self.assertTrue(is_user_Exist)

    def test_LOGIN_DBFind_false(self):
        is_user_Exist = db.users.find_one({
            "ID": "abcdefg123456789",
            "PASSWORD": 112344342,
            "EMAIL": "ppp@gmail.com",
            "TYPE" : "friend",
        }) != None
        self.assertFalse(is_user_Exist)

    #5
    def test_Project_DBFind_true(self):
        Programmer_list = ["Guyco070"]
        Clients_list = ["Guyco070"]
        
        is_project_Exist = db.projects.find_one({
            "ProjectName" : "Test_project",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "Guyco070",
            "Cilents":Clients_list ,
            "Programmer": Programmer_list
        }) != None
        self.assertTrue(is_project_Exist)

    def test_CreateProjDone_DBInsert(self):
        SV = db.projects
        Programmer_list = ["Guyco070"]
        Clients_list = ["Guyco070"]
        SV.delete_one({"ProjectName" : "Test_project"})
        project = {
            "ProjectName" : "Test_project",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "Guyco070",
            "Cilents":Clients_list ,
            "Programmer": Programmer_list
        }
        SV.insert_one(project)
        client.close()
        is_project_inserted = SV.find_one(project) != None
        self.assertTrue(is_project_inserted)

    def test_Project_DBFind_false(self):
        is_project_Exist = db.projects.find_one({
            "ProjectName" : "abcdefg123456789 ",
            "Description": "This is a test project.\n Created in a single test function called - test_CreateProjDone_DBInsert.",
            "PManager": "Guyco070",
            "Cilents":None ,
            "Programmer": None
        }) != None
        self.assertFalse(is_project_Exist)

    #6
    def test_update_project_programer_DBInsert_true(self):
        SV = db.projects
        SV.find_one_and_update(
            {"ProjectName" : "Test_project"},
            {"$addToSet": {"Programmer": "Test_programmer"}}
        )

        is_programmer_inserted = "Test_programmer" in SV.find_one({"ProjectName" : "Test_project"})["Programmer"]
        client.close()
        self.assertTrue(is_programmer_inserted)

    #7
    def test_update_project_programer_DBRemoved_true(self):
        SV = db.projects
        SV.find_one_and_update(
            {"ProjectName" : "Test_project"},
            {"$pull": {"Programmer": "Test_programmer"}}
        )

        is_programmer_inserted = "Test_programmer" not in SV.find_one({"ProjectName" : "Test_project"})["Programmer"]
        client.close()
        self.assertTrue(is_programmer_inserted)

    #8
    def test_update_project_Client_DBInsert_true(self):
        SV = db.projects
        SV.find_one_and_update(
            {"ProjectName" : "Test_project"},
            {"$addToSet": {"Clients": "Test_Client"}}
        )

        is_programmer_inserted = "Test_Client" in SV.find_one({"ProjectName" : "Test_project"})["Clients"]
        client.close()
        self.assertTrue(is_programmer_inserted)

    #9
    def test_update_project_Client_DBRemoved_true(self):
        SV = db.projects
        SV.find_one_and_update(
            {"ProjectName" : "Test_project"},
            {"$pull": {"Clients": "Test_Client"}}
        )

        is_programmer_inserted = "Test_Client" not in SV.find_one({"ProjectName" : "Test_project"})["Clients"]
        client.close()
        self.assertTrue(is_programmer_inserted)

    #10
    def test_addTASK(self):
        SV = db.tasks

        projectName = " temp_projectName  "
        uStory = " testUSERSTORY "

        uStory = uStory.lstrip()
        uStory = uStory.rstrip()
        projectName = projectName.lstrip()
        projectName = projectName.rstrip()
        
        SV.delete_many({"ProjectName":projectName,"USERSTORY": uStory})
        task = {
                "ProjectName": projectName,
                "USERSTORY": uStory,
                "Tasks": "test_Tasks",
                "SDate": "test_SDate",
                "EDate": "test_EDate",
                "Programmer" : "test_Programmer",
                "status": "test_Status"
            }
        
        SV.insert_one(task)

        is_task_unserted = SV.find_one(task) != None
        self.assertTrue(is_task_unserted)

    #11
    def test_RemoveTASK(self):
        SV = db.tasks
        SV.delete_many({"ProjectName": "temp_projectName","USERSTORY": "testUSERSTORY"})
        is_task_removed = SV.find_one({"ProjectName": "temp_projectName","USERSTORY": "testUSERSTORY"}) == None
        self.assertTrue(is_task_removed)

    #13
    def test_getTasksFromDb_to_KanbanPage_TODO(self):
        todo = list(db.tasks.find({"status":"TODO"}))
        is_tasks_status_match = True
        for t in todo:
            is_tasks_status_match += t["status"] == "TODO"
        self.assertTrue(is_tasks_status_match)

    #14
    def test_getTasksFromDb_to_KanbanPage_inprogress(self):
        inprogress = list(db.tasks.find({"status":"INPROGRESS"}))
        is_tasks_status_match = True
        for t in inprogress:
            is_tasks_status_match += t["status"] == "INPROGRESS"
        self.assertTrue(is_tasks_status_match)

    #15
    def test_getTasksFromDb_to_KanbanPage_done(self):
        done = list(db.tasks.find({"status": "DONE"}))
        is_tasks_status_match = True
        for t in done:
            is_tasks_status_match += t["status"] == "DONE"
        self.assertTrue(is_tasks_status_match)
    
    #16
    def test_getTasksFromDb_to_KanbanPage_intest(self):
        intest = list(db.tasks.find({"status": "INTEST"}))
        is_tasks_status_match = True
        for t in intest:
            is_tasks_status_match += t["status"] == "INTEST"
        self.assertTrue(is_tasks_status_match)

    def test_getTasksFromDb(self):
        todo = list(db.tasks.find({"status":"TODO"}))
        inprogress=list(db.tasks.find({"status":"INPROGRESS"}))
        intest = list(db.tasks.find({"status": "INTEST"}))
        done = list(db.tasks.find({"status": "DONE"}))
        
        is_task_exist = (todo != None) & (inprogress != None) & (intest != None) & (done != None)
        self.assertTrue(is_task_exist)
    
    def test_EditTasks(self):
        projectName = " temp_projectName  "
        uStory = " testUSERSTORY "

        uStory = uStory.lstrip()
        uStory = uStory.rstrip()
        projectName = projectName.lstrip()
        projectName = projectName.rstrip()
        
        DB = db.tasks

        myquery = DB.find_one({"ProjectName":projectName,"USERSTORY": uStory})
        newvalues = {"$set": {"Tasks": "test_Tasks_after_change" }}
        DB.update_one(myquery,newvalues)

        myquery = DB.find_one({"ProjectName":projectName,"USERSTORY": uStory})
        
        self.assertEqual("test_Tasks_after_change", myquery['Tasks'])

    '''
    def test_homepage_url(self):
        response = self.client.get('')
        self.assertEquals(response.status_code, 200)

    def test_SIGNUP_url(self):

        user = {"ID": "test_user", "PASSWORD": "test_password","EMAIL":"test@gmail.com","TYPE":"Admin"}
        response = self.client.post('/SIGNUP',data=user,follow=True)
        self.assertEquals(response.status_code, 200)

    def test_LOGIN_url(self):
        response = self.client.get('/LOGIN')
        self.assertEquals(response.status_code, 200)

    def test_SignUpDone_url(self):
        response = self.client.get('/SignUpDone')
        self.assertEquals(response.status_code, 200)
    '''