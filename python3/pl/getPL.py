import inquirer
import paramiko
from sysPL import *
def getUser(filename):
    users = importList(userList);
    users.append('New')
    questions = [
    inquirer.List('user',
                message="Select user",
                choices=users,),]
    user = inquirer.prompt(questions)
    if(user['user'] == 'New'):
        print("new user is being created")
        questions = [
        inquirer.Text('New User', message="What's your name?")]
        newUser = inquirer.prompt(questions)
        write2file(filename,newUser['New User'])
        return newUser['New User']
    clear()
    return user['user']


def getAction():
    actions = ['Mesh','Solve','PostPro']
    questions = [
    inquirer.List('action',
                message="Select action",
                choices=actions,
            ),
]
    action = inquirer.prompt(questions)
    clear()
    return action['action']

def getCase(user,sftp):
    cases = lsDir(user,sftp)
    cases.append('New')
    questions = [
    inquirer.List('cases',
                message="Select case",
                choices=cases,),]
    cases = inquirer.prompt(questions)
    if(cases['cases'] == 'New'):
        print("new case is being created")
        questions = [
        inquirer.Text('New Case', message="Enter case name")]
        newCase = inquirer.prompt(questions)
        sftp.mkdir("/cluster/scratch/" + user + "/cfd/cases/" +newCase['New Case'])
        return newCase['New Case']
    clear()
    return cases['cases']


def getCondition():
    conditions = ['Straight','LS Cornering', 'HS Cornering']
    questions = [
    inquirer.List('condition',
                message="Select condition",
                choices=conditions,
            ),
]
    conditions = inquirer.prompt(questions)
    clear()
    return conditions['condition']

