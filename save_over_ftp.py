import ftplib
import os
import time


def recursive_download(handler, destination, remote_dir):
    if not os.path.exists(destination):
        print(f'create dir "{destination}"')
        os.makedirs(destination)

    tree = handler.mlsd(remote_dir) 
    
    for el in tree:
        if isdir(el):
            recursive_download(handler, destination + "/" + el[0], remote_dir + "/" + el[0])
        else:
            download(handler, el, destination, remote_dir)

def download(handler,file, destination, remote_dir):
    filename = file[0]
    print(f'download "{filename}"')
    with open(f"{destination}/{filename}", "wb") as localfile:
        ftp.retrbinary(f'RETR {remote_dir}/{filename}', localfile.write, 1024)

def isdir(el):
    if el[1]['type'] == 'dir':
        return True
    else:
        return False


def get_conf(file):
    global mysite    
    global username  
    global password  
    global remote_dir
    
    print(f"Loading {file}")
    config = dict()
    with open(file, "r") as conffile:
        params = conffile.read().strip().split("\n")
        for el in params:
            el    = el.split("#")[0].strip()
            if el != '':
                name  = el.split("=")[0].strip()
                value = el.split("=")[1].strip()
                config[name] = value

    mysite     = config["mysite"]
    print(f"[CONFIG] : mysite = {mysite}")
    username   = config["username"]
    print(f"[CONFIG] : username = {username}")
    password   = config["password"]
    print(f"[CONFIG] : password = {password}")
    remote_dir = config["remote_dir"]
    print(f"[CONFIG] : remote_dir = {remote_dir}")




if __name__ == "__main__":




    try:
        get_conf("nitroserv.config")
        local_dir  = "backups/" + str(round(time.time())) + remote_dir
        
        print("connexion....")
        ftp = ftplib.FTP(mysite, username, password)
        print("connected !")

        recursive_download(ftp, local_dir,remote_dir)

    except Exception as e:
        input(f"[ERROR] : {e}")
    else:
        input("Press enter...")
