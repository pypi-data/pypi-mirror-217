import subprocess
import os
import sys
import time
import oss2
import http.client
import json
import logging
import calendar
from pathlib import Path
from ttauto_crawler import binary
import shutil
import zipfile
import platform
import requests
import datetime
import ftplib
from PIL import Image
from io import BytesIO
from threading import Thread, current_thread, Lock

def realCommand(cmd):
    if sys.platform != "win32":
        return "./" + " ".join(cmd)
    else:
        return cmd
    
def ffmpegBinary(searchPath):      
    binaryFile = ""
    if sys.platform == "win32":
        binaryFile = os.path.join(binary.ffmpegPath(searchPath), "win", "ffmpeg.exe")
    elif sys.platform == "linux":
        machine = platform.machine().lower()
        if machine == "x86_64" or machine == "amd64":
            machine = "amd64"
        else:
            machine = "arm64"
        binaryFile = os.path.join(binary.ffmpegPath(searchPath), "linux", machine, "ffmpeg")
    elif sys.platform == "darwin":
        binaryFile = os.path.join(binary.ffmpegPath(searchPath), "darwin", "ffmpeg")
    
    if len(binaryFile) > 0 and sys.platform != "win32":
        cmd = subprocess.Popen(f"chmod 755 {binaryFile}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        while cmd.poll() is None:
            logInfo(cmd.stdout.readline().rstrip().decode('utf-8'))

    if os.path.exists(binaryFile):
        return os.path.dirname(binaryFile), os.path.basename(binaryFile)
    else:
        return "", ""
    
def processMoov(file):
    tmpPath = f"{file}.mp4"
    binary_dir, binary_file = ffmpegBinary("")
    command = [binary_file, "-i", file, "-movflags", "faststart", "-y", tmpPath]
    command = realCommand(command)
    logInfo(f"ffmpegProcess: {command}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True,cwd=binary_dir)
        if result.returncode == 0:
            logInfo(result.stdout.decode(encoding="utf8", errors="ignore"))
            os.remove(file)
            os.rename(tmpPath, file)
        else:
            logInfo("====================== ffmpeg error ======================")
            logInfo(result.stderr.decode(encoding="utf8", errors="ignore"))
            logInfo("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        logInfo("====================== process error ======================")
        logInfo(e)
        logInfo("======================      end      ======================")

def ffmpegTest():
    binDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bin")
    testImage = os.path.join(binDir, "ffmpeg", "test.jpg")
    ffmpegProcess(["-i", testImage])
    
def ffmpegProcess(args):
    binary_dir, binary_file = ffmpegBinary("")
    command = [binary_file] + args
    command = realCommand(command)
    logInfo(f"ffmpegProcess: {command}")
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True,cwd=binary_dir)
        if result.returncode == 0:
            logInfo(result.stdout.decode(encoding="utf8", errors="ignore"))
        else:
            logInfo("====================== ffmpeg error ======================")
            logInfo(result.stderr.decode(encoding="utf8", errors="ignore"))
            logInfo("======================     end      ======================")
    except subprocess.CalledProcessError as e:
        logInfo("====================== process error ======================")
        logInfo(e)
        logInfo("======================      end      ======================")

def getOssImageSize(p):
    try:
        s = requests.session()
        s.headers.update({'Connection':'close'})
        res = s.get(p)
        image = Image.open(BytesIO(res.content), "r")
        s.close()
        return image.size
    except:
        return 0, 0

def getLocalImageSize(p):
    try:
        image = Image.open(BytesIO(p), "r")
        return image.size
    except:
        return 0, 0

def deepFtpUpload50(file, ftp, remote_dir=''):
    append_dir = f'{remote_dir}'
    if len(remote_dir) > 0:
        remote_path = f'video/{append_dir}/'
        try:
            ftp.cwd(remote_path)
        except ftplib.error_perm as e:
            if e.args[0].startswith('550'):
                # 如果远程目录不存在，则创建它
                ftp.mkd(remote_path)
                ftp.cwd(remote_path)

    s = []
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            ftp.storbinary(f'STOR {os.path.basename(file)}', f)
        s.append(f"ftp://192.168.50.113/video/{append_dir}{os.path.basename(file)}")
    elif os.path.isdir(file):
        for filename in os.listdir(file):
            local_file = os.path.join(file, filename)
            if os.path.isfile(local_file):
                with open(local_file, 'rb') as file:
                    ftp.storbinary(f'STOR {filename}', file)
                s.append(f"ftp://192.168.50.113/video/{append_dir}{filename}")
            elif os.path.isdir(local_file):
                subdir = os.path.join(remote_dir, filename)
                s.append(ftpUpload50(local_file, ftp, subdir))
    return s

def ftpUpload50(file, ftp = None):
    if not ftp:
        ftp = ftplib.FTP('192.168.50.113')
        ftp.login('ftpuser', 'ftpuser')

    remote_path = f'video/'
    try:
        ftp.cwd(remote_path)
    except ftplib.error_perm as e:
        if e.args[0].startswith('550'):
            # 如果远程目录不存在，则创建它
            ftp.mkd(remote_path)
            ftp.cwd(remote_path)

    s = deepFtpUpload50(file, ftp, "")
    ftp.quit()
    return s

def deepFtpUpload3(file, ftp, remote_dir=''):
    append_dir = f'{remote_dir}'
    if len(remote_dir) > 0:
        remote_path = f'1TB01/data/video/{append_dir}/'
        try:
            ftp.cwd(remote_path)
        except ftplib.error_perm as e:
            if e.args[0].startswith('550'):
                # 如果远程目录不存在，则创建它
                ftp.mkd(remote_path)
                ftp.cwd(remote_path)

    s = []
    if os.path.isfile(file):
        with open(file, 'rb') as f:
            ftp.storbinary(f'STOR {os.path.basename(file)}', f)
        s.append(f"http://192.168.3.220/01/video/{append_dir}{os.path.basename(file)}")
    elif os.path.isdir(file):
        for filename in os.listdir(file):
            local_file = os.path.join(file, filename)
            if os.path.isfile(local_file):
                with open(local_file, 'rb') as file:
                    ftp.storbinary(f'STOR {filename}', file)
                s.append(f"http://192.168.3.220/01/video/{append_dir}{filename}")
            elif os.path.isdir(local_file):
                subdir = os.path.join(remote_dir, filename)
                s.append(ftpUpload3(local_file, ftp, subdir))
    return s

def ftpUpload3(file, ftp = None):
    if not ftp:
        ftp = ftplib.FTP('192.168.3.220')
        ftp.login('xinyu100', 'xinyu100.com')

    remote_path = f'1TB01/data/video/'
    try:
        ftp.cwd(remote_path)
    except ftplib.error_perm as e:
        if e.args[0].startswith('550'):
            # 如果远程目录不存在，则创建它
            ftp.mkd(remote_path)
            ftp.cwd(remote_path)

    s = deepFtpUpload3(file, ftp, "")
    ftp.quit()
    return s

def ftpUpload(file):
    try:
        return ftpUpload50(file)
    except:
        return ftpUpload3(file)

def largeDiskPath():
    path = ""
    if sys.platform == "win32":
        disk = ["c:/","d:/","e:/","f:/","g:/","h:/","i:/","j:/","k:/","l:/","m:/","n:/","o:/","p:/"]
        for d in disk:
            free = 0
            try:
                total, used, free = shutil.disk_usage(d)
            except:
                continue
            if free > 0:
                freeGB = free / 1024.0 / 1024.0 / 1024.0
                if freeGB > 300:
                    path = d
                    break
        if len(path) <= 0:
            path = os.path.dirname(os.path.abspath(__file__))
    elif sys.platform == "linux":
        return "/home"
    elif sys.platform == "darwin":
        return "/"
    if len(path) <= 0:
        return ""
    dir = os.path.join(path, "ttauto_crawler_file")
    if os.path.exists(dir) == False:
        os.makedirs(dir)
    return dir

def ftpClient():
    ftp = None
    try:
        ftp = ftplib.FTP('192.168.50.113', 'ftpuser', 'ftpuser')
    except:
        ftp = ftplib.FTP('192.168.3.220', 'xinyu100', 'xinyu100.com')
    if ftp == None:
        raise Exception("no ftp!")
    return ftp

def saveToCounter(groupId, downloadCount):
    ftp = ftpClient()
    ftp.cwd("ttauto_data/")
    file_list = ftp.nlst()
    filename = "ttauto_crawler_config.txt"
    local_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    if filename in file_list:
        with open(local_file, 'wb') as f:
            ftp.retrbinary('RETR ' + filename, f.write)
    else:
        with open(local_file, 'w') as f:
            json.dump({}, f)
    #get config
    with open(local_file, 'r') as f:
        data = json.load(f)
    #update
    key = datetime.datetime.now().strftime('%Y-%m-%d')
    if key in data:
        data[key]["groupid"] = data[key]["groupid"] + "," + str(groupId)
        data[key]["count"] = data[key]["count"] + downloadCount
    else:
        data[key] = {
            "groupid" : str(groupId),
            "count" : downloadCount,
            "notify" : False
        }
    yesterday = (datetime.datetime.now() + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')
    needNotifyGroups = None
    needNotifyCounts = None
    if yesterday in data and data[yesterday]["notify"] == False and datetime.datetime.now().hour > 9:
        data[yesterday]["notify"] = True
        needNotifyGroups = data[yesterday]["groupid"]
        needNotifyCounts = data[yesterday]["count"]
    #save
    with open(local_file, 'w') as f:
        json.dump(data, f)
    with open(local_file, 'rb') as file:
        ftp.storbinary(f'STOR {filename}', file)
    ftp.quit()
    os.remove(local_file)
    return needNotifyGroups, needNotifyCounts, yesterday

def videoInfo(file):
    w = 0
    h = 0
    bitrate = 0
    fps = 0
    duration = 0

    binary_dir, binary_file = ffmpegBinary("")
    command = [binary_file, "-i", file]
    command = realCommand(command)
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, shell=True,cwd=binary_dir)
        str = ""
        if result.returncode == 0:
            str = result.stdout.decode(encoding="utf8", errors="ignore")
        else:
            str = result.stderr.decode(encoding="utf8", errors="ignore")
        if str.find("yuv420p") > 0 and str.find("fps") > 0:
            s1 = str[str.find("yuv420p"):str.find("fps")+3].replace(' ', "")
            s1_split = s1.split(",")
            for s1_it in s1_split:
                s2 = s1_it
                if s2.find("[") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("(") > 0:
                    s2 = s2[0:s2.find("[")]
                if s2.find("x") > 0:
                    sizes = s2.split("x")
                    if len(sizes) > 1:
                        w = sizes[0]
                        h = sizes[1]
                if s2.find("kb/s") > 0:
                    bitrate = s2[0:s2.find("kb/s")]
                if s2.find("fps") > 0:
                    fps = s2[0:s2.find("fps")]
        if str.find("Duration:") > 0 and str.find(", start:") > 0:
            s2 = str[str.find("Duration:")+9:str.find(", start:")].replace(' ', "")
            s2_split = s2.split(":")
            if len(s2_split) > 2:
                hour = float(s2_split[0])
                min = float(s2_split[1])
                second  = float(s2_split[2])
                duration = hour*3600 + min*60 + second
    except subprocess.CalledProcessError as e:
        logInfo("====================== process error ======================")
        logInfo(e)
        logInfo("======================      end      ======================")
    return float(w),float(h),float(bitrate),float(fps),float(duration)

def logInfo(s, pppp=False):
    logging.info(f"{current_thread().name} {s}")
    if pppp == True:
        print(f"{current_thread().name} {s}")