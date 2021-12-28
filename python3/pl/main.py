#!/usr/bin/python3

import inquirer
import os
import paramiko
import socket
import getpass

#-------------------------
# TODO: check if file has right extension
#       wget from github into specific filename
#       set absolute paths
#-------------------------


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


def sshMagic(username):
    if(username == ''):
        username = getUser(userList)
    hostname = "euler.ethz.ch"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, 22))
    t = paramiko.Transport(sock)
    t.start_client()
    pw = getpass.getpass("Password for %s@%s: " % (username, hostname))
    
    t.auth_password(username, pw)
    sftp = paramiko.SFTPClient.from_transport(t)
    return username, sftp

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

def lsDir(user,sftp):
    dirs = []
    dirs = sftp.listdir("/cluster/scratch/" + user + "/cfd/cases/")
    return dirs

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


def sSolve(cond,fil): #TODO -> easy
    # Check for meshed
    # Start solve
    print('Starting Solvei for ' + cond  + ' on file ' + fil)
    return 0

def sMesh(cond,fil): #TODO -> integration with java macro
    # Bring master to case 
    # Start mesh
    print('Starting Mesh for ' + cond  + ' on file ' + fil)
    return 0

def sPostPro(cond,fil): #TODO -> integration with java macro
    # Check if solved is there
    # StartPostPro
    print('Starting PostPro for '+ cond + ' on file ' + fil)
    return 0

def exct(action,cond,user,case,sftp):
    if action == 'Mesh':
        fil = selectFile(user,case,action,sftp)
        sMesh(cond,fil)
    elif action == 'Solve':
        fil = selectFile(user,case,action,sftp)
        sSolve(cond,fil)
    else:
        fil = selectFile(user,case,action,sftp)
        sPostPro(cond,fil)

def selectFile(user,case,action,sftp):
    
    sftp.chdir('/cluster/scratch/' + user + '/cfd/cases/' + case + '/')
    files = sftp.listdir()
    if action == 'Mesh':
        files.append('New')
    questions = [
    inquirer.List('mesh',
                message="Select file",
                choices=files,),]
    mesh = inquirer.prompt(questions)
    if(mesh['mesh'] == 'New'):
        print("new file is being created")
        questions = [
        inquirer.Text('New Mesh', message="Enter simulation name?")]
        newMesh = inquirer.prompt(questions)
        ## Wget/curl here
        print('wgetting new .sim file')
        #write2file(filename,newUser['New User'])
        return newMesh['New Mesh']
    clear()
    return mesh['mesh']
    



def clear():
    os.system("clear")

def main():
    user  = ''
    user, sftp = sshMagic(user) #First login
    case = getCase(user,sftp)
    condition = getCondition()
    #fil = selectFile(user,cases,'Solve', sftp)
    exct(getAction(),condition,user,case,sftp)


    #t.close()

main()
