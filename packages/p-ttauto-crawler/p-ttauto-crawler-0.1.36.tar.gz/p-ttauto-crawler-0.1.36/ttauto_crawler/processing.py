import os
from ttauto_crawler import utils
from ttauto_crawler import txt2proj
from template_generator import binary as genertor_binary
from template_generator import template as genertor_template
import shutil
import subprocess
import random
from urllib.parse import *

def clearDir(curGroupId):
    s1 = curOutputDir(curGroupId)
    if os.path.exists(s1):
        shutil.rmtree(s1)

def curOutputDir(curGroupId):
    s = os.path.join(utils.largeDiskPath(), ".out", str(curGroupId))
    if os.path.exists(s) == False:
        os.makedirs(s)
    return s

def secondToDuration(d):
    hour = int(d / 3600)
    sec = float(d % 60)
    min = int((d - sec) % 3600 / 60)
    hour_str = str(hour).rjust(2).replace(" ", "0")
    min_str = str(min).rjust(2).replace(" ", "0")
    sec_str = ""
    if sec >= 10:
        sec_str = str(sec)
    else:
        sec_str = f"0{str(sec)}"
    return f"{hour_str}:{min_str}:{sec_str}"

def processAllImage(curGroupId, data, curDownloadDir, tpname, addRandomText, img2videoCnt, tag, page=0):
    src = curDownloadDir
    dst = curOutputDir(curGroupId)
    templateDir = ""
    if len(tpname) > 0:
        templateDir = os.path.join(genertor_binary.randomEffectPath(""), tpname)
    s = []
    for root,dirs,files in os.walk(src):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")].lower()
            ext = file[file.rindex("."):].lower()
            if ext in [".jpg", ".png", ".jpeg", ".bmp"]:
                s.append(os.path.join(root, file))
        if root != files:
            break

    idx = 0
    while len(s) > img2videoCnt:
        s1 = []
        allcnt = len(s)
        for i in range(img2videoCnt):
            rd_idx = random.randint(0, allcnt-1)
            tmp_s = s[rd_idx]
            s.remove(tmp_s)
            allcnt -= 1
            s1.append(tmp_s)
        if len(templateDir) > 0:
            data.append({
                    "input":s1,
                    "template": templateDir,
                    "params":{},
                    "output": os.path.join(dst, f"img2video_{page}_{idx}.mp4")})
        else:
            gentemplate = txt2proj.imgsToTemplate(s1, addRandomText, tag)
            data.append({
                    "input":[],
                    "template": gentemplate,
                    "params":{},
                    "output": os.path.join(dst, f"img2video_{page}_{idx}.mp4")})
        idx+=1

def videoToTemplate(curGroupId, data, curDownloadDir, tpname, addRandomText, splitDuration, verticalScreen, tag, page=0):
    src = curDownloadDir
    dst = curOutputDir(curGroupId)
    templateDir = ""
    if len(tpname) > 0:
        templateDir = os.path.join(genertor_binary.randomEffectPath(""), tpname)
    for root,dirs,files in os.walk(curDownloadDir):
        for file in files:
            if file.find(".") <= 0:
                continue
            name = file[0:file.index(".")]
            ext = file[file.rindex("."):]
            if ext == ".mp4":
                w,h,bitrate,fps,video_duration = utils.videoInfo(os.path.join(src, file))
                if w <= 0 or bitrate <= 0:
                    continue
                if verticalScreen == True:
                    h = w * (16.0 / 9.0)
                srcVideo = os.path.join(src, f"{name}{ext}")
                dstVideo = os.path.join(dst, f"{name}_{page}_{tpname}{ext}")
                if splitDuration > 0 and video_duration > splitDuration * 1.5:
                    idx = 0
                    while (idx * splitDuration) < video_duration:
                        split_duration = splitDuration
                        if ((idx+1) * splitDuration) > video_duration:
                            split_duration = video_duration - (idx * splitDuration)
                        if split_duration < splitDuration / 2:
                            #ignore too short slice
                            break
                        tmpPath = os.path.join(curDownloadDir, f"{name}_autoremove_{idx}.mp4")
                        dstVideo = os.path.join(dst, f"{name}_{page}_{idx}_{tpname}{ext}")
                        if os.path.exists(tmpPath) == False:
                            # -c:v copy -c:a copy  # must be recodec for some undecode bug
                            cmd = ["-ss", secondToDuration(idx * splitDuration), "-i", srcVideo, "-t", secondToDuration(split_duration), "-y", tmpPath]
                            utils.ffmpegProcess(cmd)
                        if os.path.exists(tmpPath) and os.stat(tmpPath).st_size > 10000: #maybe source video is wrong, check output file is large than 10k
                            realTemplateDir = templateDir
                            if addRandomText and tpname != "template8":
                                if len(templateDir) > 0:
                                    tempDir = txt2proj.newTemplateWithText(templateDir, w, h, split_duration, tag)
                                else:
                                    tempDir = txt2proj.singleVideoToTemplate(tmpPath, True, w, h, split_duration, tag)
                                realTemplateDir = tempDir
                            if len(realTemplateDir):
                                data.append({
                                    "input":[tmpPath],
                                    "template": realTemplateDir,
                                    "params":{},
                                    "output": dstVideo})
                            else:
                                shutil.copyfile(tmpPath, dstVideo)
                        idx+=1
                else:
                    realTemplateDir = templateDir
                    if addRandomText:
                        if len(templateDir) > 0:
                            tempDir = txt2proj.newTemplateWithText(templateDir, w, h, video_duration, tag)
                        else:
                            tempDir = txt2proj.singleVideoToTemplate(srcVideo, True, w, h, video_duration, tag)
                        realTemplateDir = tempDir
                    if len(realTemplateDir):
                        data.append({
                            "input":[srcVideo],
                            "template": realTemplateDir,
                            "params":{},
                            "output": dstVideo})
                    else:
                        shutil.copyfile(srcVideo, dstVideo)
        if root != files:
            break

def needAdaptiveSize(crawler_template_name, addRandomText, splitDuration, img_to_video, verticalScreen):
    if len(crawler_template_name) > 0 and img_to_video > 0:
        return False
    else:
        return True

def realProcessToVideo(curDownloadDir,curGroupId, crawler_template_name,addRandomText,splitDuration,img_to_video,verticalScreen,tag,page=0):
    data = []
    official_template_list = []
    #videos
    if len(crawler_template_name) > 0:
        for tpname in crawler_template_name:
            templateDir = os.path.join(genertor_binary.randomEffectPath(""), tpname)
            official_template_list.append(templateDir)
            utils.logInfo(f"      ==={curGroupId} video to template with {tpname}", True)
            videoToTemplate(curGroupId, data, curDownloadDir, tpname, addRandomText, splitDuration, verticalScreen, tag, page)
    else:
        utils.logInfo(f"      ==={curGroupId} video to empty template", True)
        videoToTemplate(curGroupId, data, curDownloadDir, "", addRandomText, splitDuration, verticalScreen, tag, page)
    #imgs
    if img_to_video > 0:
        if len(crawler_template_name) > 0:
            for tpname in crawler_template_name:
                templateDir = os.path.join(genertor_binary.randomEffectPath(""), tpname)
                official_template_list.append(templateDir)
                utils.logInfo(f"      ==={curGroupId} {img_to_video} image to video with {tpname}", True)
                processAllImage(curGroupId, data, curDownloadDir, tpname, addRandomText, img_to_video, tag, page)
        else:
            utils.logInfo(f"      ==={curGroupId} {img_to_video} image to video", True)
            processAllImage(curGroupId, data, curDownloadDir, "", addRandomText, img_to_video, tag, page)
    #process template
    froceAdaptiveSize = False
    if needAdaptiveSize(crawler_template_name, addRandomText, splitDuration, img_to_video, verticalScreen):
        froceAdaptiveSize = True
    if len(data) > 0:
        try:
            utils.logInfo(f"      ==={curGroupId} begin skymedia", True)
            genertor_template.executeTemplate(data, "", froceAdaptiveSize, False, False)
        except subprocess.CalledProcessError as e:
            utils.logInfo("====================== process error ======================", True)
            utils.logInfo(e)
            utils.logInfo("======================      end      ======================")
        finally:
            for it in data:
                if it["template"] not in official_template_list:
                    if os.path.exists(it["template"]):
                        shutil.rmtree(it["template"])
    

def processToVideo(curDownloadDir, params):
    curGroupId = params["curGroupId"]
    crawler_template_name = params["crawler_template_name"]
    addRandomText = params["addRandomText"]
    splitDuration = params["splitDuration"]
    img_to_video = params["img_to_video"]
    verticalScreen = params["verticalScreen"]
    one_zip_switch = params["one_zip_switch"]
    tag = params["tag"]
    
    if one_zip_switch:
        dirs = [os.path.join(root, dir) for root, dirs, files in os.walk(curDownloadDir)
                for dir in dirs]
        idx = 0
        for d in dirs:
            utils.logInfo(f"      ==={curGroupId} one_zip_switch process: {d} to video", True)
            realProcessToVideo(d, curGroupId, crawler_template_name,addRandomText,splitDuration,img_to_video,verticalScreen,tag,idx)
            idx+=1
            utils.logInfo(f"      ==={curGroupId} finish", True)
    else:
        realProcessToVideo(curDownloadDir,curGroupId, crawler_template_name,addRandomText,splitDuration,img_to_video,verticalScreen,tag,0)
        
    outputDir = curOutputDir(curGroupId)
    file_list = os.listdir(outputDir)
    return outputDir, len(file_list)