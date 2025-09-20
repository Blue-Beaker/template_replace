import os,sys
import shutil
from os import path
import traceback
from binaryornot.check import is_binary

DRY_RUN=False

def listRecursive(folder:str,suffix:str=""):
    filesList:list[str]=[]
    files=os.listdir(folder)
    files.sort()
    for file in files:
        filepath=os.path.join(folder,file)
        if(os.path.isdir(filepath)):
            filesList.extend(listRecursive(filepath,suffix))
        elif(file.endswith(suffix)):
            filesList.append(filepath)
    return filesList

def renameRecursive(folder:str, replace_from:str,replace_to:str):
    filesList:list[str]=[]
    files=os.listdir(folder)
    files.sort()
    for file in files:
        filepath=os.path.join(folder,file)
        if(os.path.isdir(filepath)):
            filesList.extend(renameRecursive(filepath,replace_from,replace_to))

        renamed=replaceKeepCase(file,replace_from,replace_to)
        if(renamed!=file):
            if(not DRY_RUN):
                os.rename(os.path.join(folder,file),os.path.join(folder,renamed))
            filesList.append(f"{os.path.join(folder,file)}->{os.path.join(folder,renamed)}")
    return filesList


def replaceKeepCase(stringToReplace:str,replaceFrom:str,replaceTo:str)->str:
    i=0
    replaced=[]

    while i<stringToReplace.__len__():
        startingIndex=stringToReplace.casefold().find(replaceFrom.casefold(),i)

        if(startingIndex==-1):
            replaced.append(stringToReplace[i:])
            break
        endIndex=startingIndex+len(replaceFrom)
        
        replaced.append(stringToReplace[i:startingIndex])

        found=stringToReplace[startingIndex:endIndex]
        if(found.islower()):
            replaced.append(replaceTo.lower())
        elif(found[0].islower()):
            replaced.append(replaceTo[0].lower()+replaceTo[1:])
        else:
            replaced.append(replaceTo)
        
        # print(found,startingIndex,endIndex)

        i=endIndex

    # print(replaced)
    return "".join(replaced)


def batchRename(folder:str,replaceFrom:str,replaceTo:str):
    replacementDict:dict[str,str]={}
    for fileName in listRecursive(folder):
        renamed=replaceKeepCase(fileName,replaceFrom,replaceTo)
        if(renamed!=fileName):
            replacementDict[fileName]=renamed
    for fromName,toName in replacementDict.items():
        os.makedirs(os.path.dirname(toName), exist_ok=True)
        shutil.move(fromName,toName)

if (__name__=="__main__"):
    # print(replaceKeepCase("examplemod.dwaoduioewrda.ExampleMod.dwaeoajexampleMod","examplemod","NewName"))
    if(sys.argv.__len__()<=1):
        rootPath=input("Path to do batch rename:")
    else:
        rootPath=sys.argv[1]

    if(sys.argv.__len__()>=4):
        replaceFrom=sys.argv[2]
        replaceTo=sys.argv[3]
    else:
        inputResult=input("String to replace from [ExampleMod]:")
        replaceFrom=inputResult if inputResult.strip()!="" else "ExampleMod"
            
        inputResult2=input("String to replace to [ExampleMod2]:")
        replaceTo=inputResult2 if inputResult2.strip()!="" else "ExampleMod2"

    fileList=renameRecursive(rootPath,replaceFrom,replaceTo)

    print(fileList)
    for file in listRecursive(rootPath):
        try:
            with open(file, "r") as f:
                lines=f.readlines()
            with open(file, "w") as f:
                for line in lines:
                    f.write(replaceKeepCase(line,replaceFrom,replaceTo))
        except Exception as e:
            if(not isinstance(e, UnicodeDecodeError)):
                print(file,e)
