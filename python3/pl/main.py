#!/usr/bin/python3
import inquirer
import os
import paramiko
import socket
import getpass

userList = "./src/users"
pw = ""

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
    clear()
    return user['user']


def manual_auth(hostname, username,pw):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((hostname, 22))
    t = paramiko.Transport(sock)
    t.start_client()
    if(len(pw) is 0):
        pw = getpass.getpass("Password for %s@%s: " % (username, hostname))
    t.auth_password(username, pw)
    chan = t.open_session()
    chan.get_pty()
    chan.invoke_shell()
    print("*** Connection successfull!\n")

    #interactive.interactive_shell(chan)
    chan.close()
    t.close()



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
    return 0

def clear():
    os.system("clear")

def main():
    clear()
    manual_auth("euler.ethz.ch","aparis",pw)
    print(pw)
    manual_auth("euler.ethz.ch","aparis",pw)
    print(pw)
    #setup()
    #user = getUser(userList)
    #case = getSSHDirs("aparis",cases)
    #action = getAction()
    #execute(user,case,action)

main()
