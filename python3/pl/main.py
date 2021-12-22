#!/usr/bin/python3
import inquirer
import os
import subprocess

userList = "./src/users"
def write2file(filename,text):
    fFile = open(filename,'a')
    fFile.write(text)
    fFile.close()

def importList(filename):
    with open(filename) as file:
        lines = [line.strip() for line in file]
        return lines

def getUser(filename):

    users = importList(userList);
    questions = [
    inquirer.List('user',
                message="Select user",
                choices=users,
            ),
]
    user = inquirer.prompt(questions)
    if(user['user'] == 'New'):
        print("new user is being created")
        questions = [
        inquirer.Text('New User', message="What's your name?")]
        newUser = inquirer.prompt(questions)
        write2file(filename,newUser['New User'])
        return newUser['New User']
    return user['user']

def getSSHDirs(user):
    #connect to ssh
    #check specific folder in scratch
    #return list 
    #select case from list
    # if new, mkdir
    return 0

def getAction():
    actions = ['Mesh','Solve','PostPro']
    questions = [
    inquirer.List('action',
                message="Select action",
                choices=actions,
            ),
]
    action = inquirer.prompt(questions)
    return action['action']
def setup():
    user = getUser(userList)
    #case = getCase()
    action = getAction()

def sSolve():
    # Check for mesh
    # Start solve
    return 0

def sMesh():
    # Bring master to case 
    # Start mesh
    return 0

def sPostPro():
    # Check if solved is there
    # StartPostPro
    return0
'''
def execute(user, case, action):
    match action:
        case "Mesh":
            sMesh()
        case "Solve":
            sSolve()
        case "Postpro":
            sPostPro()
    return 0
'''

def main():
    #setup()
    user = getUser(userList)
    #case = getSSHDirs("aparis",cases)
    action = getAction()
    #execute(user,case,action)

main()
