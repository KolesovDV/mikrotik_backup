#!/usr/bin/python

import paramiko
import datetime
import os
import time
from create_folders_inside_ftp import ftpmkdir, ftpmvdir
from differences import diff_rsc_files
from datetime import timedelta
from preference import FtpdIP,ftpUser,ftpPass,BackMovePath,  MKRPort,FtpdPORT, MKRUser,MKRPasswd 

CurrentDate   = datetime.date.today()
Yesterday = CurrentDate + timedelta(-1)
ssh=paramiko.SSHClient()

def uploadbcptoftp(mkrip):
 print("connecting is going")
 try:
  Upload_BACKUP_filesToFtp = "tool fetch address=" + str(FtpdIP) + " port=" + str(FtpdPORT) +" mode=ftp dst-path=" + str(mkrip) + "_" + str(CurrentDate) + ".backup src-path=" + str(mkrip) + "_" + str(CurrentDate)+ ".backup" + " user=" + str(ftpUser) + " password=" + str(ftpPass) + " upload=yes"
  Upload_RSC_filesToFtp = "tool fetch address=" + str(FtpdIP) + " port=" + str(FtpdPORT) +" mode=ftp dst-path=" + str(mkrip) + "_" + str(CurrentDate) + ".rsc src-path=" + str(mkrip) + "_" + str(CurrentDate)+ ".rsc" + " user=" + str(ftpUser) + " password=" + str(ftpPass) + " upload=yes"

  print ("uploading local backup to ftp.. /" + Upload_BACKUP_filesToFtp)
  ssh.exec_command(Upload_BACKUP_filesToFtp)
  ssh.exec_command(Upload_RSC_filesToFtp)
  time.sleep(2)
 except:
  print("ftp unavailable")
  

def createlocalbcp(mkrip):
  try:
    #ssh=paramiko.SSHClient()
    CreateLocal_BACKUP_files = "system backup save dont-encrypt=yes  name=" + str(mkrip) + "_" + str(CurrentDate) + ".backup"
    CreateLocal_RSC_files = "export file=" + str(mkrip) + "_" + str(CurrentDate)

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print ("password")
    ssh.connect(mkrip,port = MKRPort, username=MKRUser,password=MKRPasswd,look_for_keys=False, allow_agent=False )
    print("connected")
    ssh.exec_command(CreateLocal_BACKUP_files)
    ssh.exec_command(CreateLocal_RSC_files)
    time.sleep(5)
    print ("local backup created..") 
  except:
      print("imposible to make backup")

def removelocalbcp(mkrip):
  try:
    RemoveLocal_BACKUP_files = 'file remove "' + str(mkrip) + "_" + str(CurrentDate) + ".backup" + '"'
    RemoveLocal_RSC_files = 'file remove "' + str(mkrip) + "_" + str(CurrentDate) + ".rsc"+ '"'
    print ("removing local backup.. /" + RemoveLocal_BACKUP_files)
    ssh.exec_command(RemoveLocal_BACKUP_files)
    ssh.exec_command(RemoveLocal_RSC_files)
    time.sleep(2)
    print ("local backup removed..")
    #uploadbcptoftp(mkrip)
  except:
      print("imposible to remove backup")

def main():
 print("backup starting")
 for i in range(202,250,1):
    ip = "192.168.%d.1" % (i)
    try: 
        print(ip)
        ftpmkdir(BackMovePath + str(CurrentDate)+"/"+ip)
        time.sleep(2)
        createlocalbcp(ip)
        uploadbcptoftp(ip)
        removelocalbcp(ip)
        ssh.close()
        ftpmvdir(BackMovePath + str(ip) + "_" + str(CurrentDate)+".backup",BackMovePath + str(CurrentDate) + "/" +str(ip)+"/" + ip +  "_" + str(CurrentDate)+".backup")
        ftpmvdir(BackMovePath + str(ip) + "_" + str(CurrentDate)+".rsc",   BackMovePath + str(CurrentDate) + "/"+ str(ip)+"/" + ip +  "_" + str(CurrentDate)+".rsc")
        diff_rsc_files(BackMovePath +str(CurrentDate)+ "/" +str(ip)+"/" + ip + "_" + str(CurrentDate)+ ".rsc",BackMovePath +str(Yesterday)+ "/" +str(ip)+"/" + ip + "_" + str(Yesterday)+ ".rsc",BackMovePath + str(CurrentDate)+ "/" +str(ip)+ "/" + ip + "_" + str(CurrentDate) )
        time.sleep(2)
    except:
        print("error making backups")

if __name__ == "__main__":
    main()
