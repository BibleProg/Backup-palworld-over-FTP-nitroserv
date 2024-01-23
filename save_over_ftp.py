import ftplib
import os


def recursive_download(handler, destination, remote_dir):
    if not os.path.exists(destination):
        print("created dir " + '"' + destination + '"')
        os.makedirs(destination)

    tree = handler.mlsd(remote_dir) 
    
    for el in tree:
        if isdir(el):
            recursive_download(handler, destination + "/" + el[0], remote_dir + "/" + el[0])
        else:
            download(handler, el, destination, remote_dir)

def download(handler,file, destination, remote_dir):
    filename = file[0]
    print('download "' + filename + '"')
    with open(destination+"/"+filename, "wb") as localfile:
        ftp.retrbinary('RETR ' + remote_dir+"/"+filename, localfile.write, 1024)

def isdir(el):
    if el[1]['type'] == 'dir':
        return True
    else:
        return False



if __name__ == "__main__":

    mysite     = "ftp.nitroserv.games"
    username   = ""
    password   = ""
    remote_dir = "Palworld/Pal/Saved/SaveGames/"
    local_dir  = str(round(time.time())) + "Palworld/Pal/Saved/SaveGames/"
 
    print("connexion....")
    ftp = ftplib.FTP(mysite, username, password)
    print("connected !")

    recursive_download(ftp, local_dir,remote_dir)

    input("Press enter...")
