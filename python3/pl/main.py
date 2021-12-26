#!/usr/bin/python3

import inquirer
import os
import paramiko
import socket
import getpass

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

def sSolve(): #TODO -> easy
    # Check for meshed
    # Start solve
    print('Starting Solve')
    return 0

def sMesh(): #TODO -> integration with java macro
    # Bring master to case 
    # Start mesh
    print('Starting Mesh')
    return 0

def sPostPro(): #TODO -> integration with java macro
    # Check if solved is there
    # StartPostPro
    print('Starting PostPro')
    return 0

def exct(action):
    if action == 'Mesh':
        sMesh()
    elif action == 'Solve':
        sSolve()
    else:
        sPostPro()


def clear():
    os.system("clear")

def main():
    user  = ''
    user, sftp = sshMagic(user) #First login
    cases = getCase(user,sftp)
    exct(getAction())


    #t.close()

main()
