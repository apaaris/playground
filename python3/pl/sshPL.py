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
