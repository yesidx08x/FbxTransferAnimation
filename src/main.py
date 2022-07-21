import os,RLPy
import copy,shutil
import tempfile
#from subNode import SkeletonTreeView
from math import *
import PySide2
from PySide2 import *
#from PySide2.shiboken2 import wrapInstance
global ap_version
ap_version=RLPy.RApplication.GetProductVersion()[0]
rl_plugin_info = None

if ap_version == 7:
    rl_plugin_info = {"ap": "iClone", "ap_version": "7.0"}
    from PySide2.shiboken2 import wrapInstance
    from PySide2.QtWidgets import QDialog, QApplication
elif ap_version == 8: 
    rl_plugin_info = {"ap": "iClone", "ap_version": "8.0"}
    from shiboken2 import wrapInstance
    from PySide2.QtWidgets import QDialog, QApplication

ui = {}  # User interface globals
events = {}  # Callback event globals
fbxfile = r"E://temp//fbxIclone//fbx//avatar.fbx"
avatar_name = "0.Zane(0)"
prop_name = ''
camera_name = ''
rlmotion = ''
all_avatars =[None]
all_props =[None]
all_cameras =[None]
# UE4Editor-Cmd.exe "C:\projects\MyProject.uproject" -ExecutePythonScript="c:\my_script.py"
ue4cmd = 'D:/UE_4.27/Engine/Binaries/Win64/UE4Editor-Cmd.exe'

class EventCallback(RLPy.REventCallback):
    def __init__(self):
        RLPy.REventCallback.__init__(self)

    def OnObjectAdded(self):
        update_ui()

    def OnObjectDeleted(self):
        update_ui()


class DialogCallback(RLPy.RDialogCallback):

    def __init__(self):
        RLPy.RDialogCallback.__init__(self)
        self.__closed = False

    def OnDialogHide(self):
        global events
        if self.__closed:
            RLPy.REventHandler.UnregisterCallback(events["callback_id"])
            events.clear()
            ui.clear()

    def OnDialogShow(self):
        try:
            global ui
            if "dialog" in ui and "window" in ui:
                if ui["window"].IsFloating():
                    ui["dialog"].adjustSize()
        except Exception as e:
            print(e)

    def OnDialogClose(self):
        ui["window"].UnregisterAllEventCallbacks()
        self.__closed = True
        return True

def copyFbx(fbxfile,destpath):
    if not os.path.isdir(os.path.abspath(destpath)):
        os.makedirs(os.path.abspath(destpath))
    try:
        reslut = shutil.copy(os.path.abspath(fbxfile),os.path.abspath(os.path.join(destpath,os.path.basename(fbxfile))))
        print(reslut)
        return reslut
    except Exception  as ex:
        print(ex)
        return None

def newImotionPy(key,pypath,args):
    asset_name, iclone_folder, project_path, game_sequence, game_rlcontent = args
    f = open(file = pypath,encoding = "utf-8", mode = 'r')
    orinL = f.readlines()
    f.close()
    if key == 'avatar':
        newVarL = ["import os,re\n",
        "import unreal\n",
        "asset_name = '{0}'\n".format(asset_name),
        "new_name = re.sub(r'[_.)]','',asset_name).replace('(','_')\n"
        "iclone_folder = '{0}'\n".format(iclone_folder),
        "project_path = '{0}'\n".format(project_path),
        "fbx_name = '{0}.{1}({2}).fbx'.format(asset_name[0],re.sub(r'[0-9,_.()]','',asset_name),asset_name[-2])\n",
        "_FBX_file = '{0}/{1}/{2}'.format(project_path, iclone_folder,fbx_name)\n",
        "game_sequence = '{0}'\n".format(game_sequence),
        "game_rlcontent = '{0}'\n".format(game_rlcontent),
        "sequence_path = '{0}/MyLevelSequence'.format(game_sequence)\n",
        "actor_path = '{0}/{1}/{1}'.format(game_rlcontent, new_name)\n",
        "animation_path = '/Game/{0}/{1}'.format(iclone_folder, asset_name.replace('.','_').replace('(','_').replace(')','_'))\n",
        "_skeleton_path = '{0}/{1}/{1}_Skeleton'.format(game_rlcontent,new_name)\n"]
        endExecL = ["\n    option = buildAnimationImportOptions(_skeleton_path)\n",
        "    animation_task = buildImportTask(file_name=_FBX_file, destinataion_path='/Game/icloneFBX', options=option)\n",
        "    executeImportTasks([animation_task])\n"]
    elif key == 'prop':
        newVarL = ["import os,re\n",
        "import unreal\n",
        "asset_name = '{0}'\n".format(asset_name),
        "new_name = re.sub(r'[.)]','',asset_name).replace('(','_')\n"
        "iclone_folder = '{0}'\n".format(iclone_folder),
        "project_path = '{0}'\n".format(project_path),
        "fbx_name = '{0}.{1}({2}).fbx'.format(asset_name[0],re.sub(r'[0-9,_.()]','',asset_name),asset_name[-2])\n",
        "_FBX_file = '{0}/{1}/{2}.fbx'.format(project_path, iclone_folder,asset_name)\n",
        "game_sequence = '{0}'\n".format(game_sequence),
        "game_rlcontent = '{0}'\n".format(game_rlcontent),
        "sequence_path = '{0}/MyLevelSequence'.format(game_sequence)\n",
        "actor_path = '{0}/{1}/{1}'.format(game_rlcontent, new_name)\n",
        "animation_path = '/Game/{0}/{1}'.format(iclone_folder, asset_name.replace('.','_').replace('(','_').replace(')','_'))\n",
        "_skeleton_path = '{0}/{1}/{1}_Skeleton'.format(game_rlcontent,new_name)\n"]
        endExecL = ["\n    option = buildAnimationImportOptions(_skeleton_path)\n",
        "    animation_task = buildImportTask(file_name=_FBX_file, destinataion_path='/Game/icloneFBX', options=option)\n",
        "    executeImportTasks([animation_task])\n"]
    elif key == 'camera':
        newVarL = ["import os,re\n",
        "import unreal\n",
        "asset_name = '{0}'\n".format(asset_name),
        "new_name = re.sub(r'[.)]','',asset_name).replace('(','_')\n"
        "iclone_folder = '{0}'\n".format(iclone_folder),
        "project_path = '{0}'\n".format(project_path),
        "fbx_name = '{0}.{1}({2}).fbx'.format(asset_name[0],re.sub(r'[0-9,_.()]','',asset_name),asset_name[-2])\n",
        "_FBX_file = '{0}/{1}/{2}.fbx'.format(project_path, iclone_folder,asset_name)\n",
        "game_sequence = '{0}'\n".format(game_sequence),
        "game_rlcontent = '{0}'\n".format(game_rlcontent),
        "sequence_path = '{0}/MyLevelSequence'.format(game_sequence)\n",
        "actor_path = '{0}/{1}/{1}'.format(game_rlcontent, new_name)\n",
        "animation_path = '/Game/{0}/{1}'.format(iclone_folder, asset_name.replace('.','_').replace('(','_').replace(')','_'))\n",
        "_skeleton_path = '{0}/{1}/{1}_Skeleton'.format(game_rlcontent,new_name)\n"]
        endExecL = ["\n    importCamera(sequence=sequence_path, import_filename=_FBX_file) #camera import\n"]
    newVarL.extend(orinL[14:])
    newVarL.extend(endExecL)

    tmp_pyfile = tempfile.NamedTemporaryFile().name+'.py'
    with open(file = tmp_pyfile,mode = 'w', encoding = "utf-8") as f:
        f.writelines(newVarL)
        f.flush()
        f.close()
    return tmp_pyfile

# 外部程序导出Prop和Camera的FBX
def clickExportFBX(fbxfile,project):
    # -exportfbx -exfile e:\dd.fbx -start 1 -end 390 -project test.iProject
    if ap_version == 7:
        execfile = os.path.dirname(__file__) + "/clickIClone7.exe"
    elif ap_version == 8:
        execfile = os.path.dirname(__file__) + "/clickIClone8.exe"
    print('fbx>>'+fbxfile)
    start = ui["widget"].start_frame.text()
    end = ui["widget"].start_frame.text()
    cmdtext ='\"{0}\" -exportfbx -exfile \"{1}\" -start {1} -end {2} -project {3}'.format(execfile,os.path.abspath(fbxfile),start,end,project)
    #cmdfile = fbxfile[:-4]+'_mfbx.cmd'
    #print(cmdfile)
    #f=open(cmdfile,'w')
    #f.write(cmdtext)
    #f.close()
    #reslut = subprocess.run(cmdtext, shell=True) 
    #reslut=os.system(cmdfile)
    #print(reslut)
    return cmdtext

def getArgs(avatar_name,ue_path):
    asset_name = avatar_name
    fbxpath = ui["widget"].fbxpath.text()
    #ui["widget"].fbxpath.text() '/Content/'
    if not os.path.isdir(fbxpath):
        os.makedirs(fbxpath)
    iclone_folder = fbxpath.replace('\\','/').split('/')[-1] #'icloneFBX'
    project_path = os.path.join(ue_path,'Content').replace('\\','/')
    game_sequence = '/Game/Sequences'
    game_rlcontent ='/Game/RLContent'
    args = asset_name, iclone_folder, project_path, game_sequence, game_rlcontent
    return args

def cmdOut(cmdfile):
    import subprocess
    subprocess.run(cmdfile,shell=False)

def runCmd(key,fbxfile,avatar_name,uepath,newline):
    import re
    ue_path=os.path.dirname(uepath)
    #asset_name, iclone_folder, project_path, game_sequence, game_rlcontent = args
    py_file = os.path.dirname(__file__) + "/imotion.py"
    print(py_file)
    args=getArgs(avatar_name,ue_path)
    tmp_logfile = tempfile.NamedTemporaryFile().name+'.log'
    tmp_pyfile = newImotionPy(key,py_file,args)
    # debug方法"D:/UE_4.27/Engine/Binaries/Win64/UE4Editor.exe" "E:/test/uasset/MyCppProject/MyCppProject.uproject" -run=pythonscript -script="C:\Users\YANGYO~1\AppData\Local\Temp\tmp162a9j8y.py">e:\112.txt
    cmdtext = '\"{0}\" \"{1}\" -ExecutePythonScript=\"{2}\"'.format(ue4cmd ,uepath, tmp_pyfile)
    cmdfile = fbxfile[:-4]+'.cmd'
    cmdfile = re.sub("[^a-z^A-Z^0-9^/^:^.^_]", "", cmdfile)
    print(cmdfile)
    f=open(cmdfile,'w')
    f.writelines([newline+'\n',cmdtext])
    f.close()
    from threading import Thread
    nthrd = Thread(target=cmdOut, args=(cmdfile,))
    nthrd.daemon=True
    nthrd.start()
    return

def exportFbx():
    global ui, fbxfile, avatar_name,rlmotion,prop_name,camera_name
    output_assetDict ={}
    if ui["widget"].checkAvatar.isChecked():
        output_assetDict['avatar']={}
        current_avatar = all_avatars[ui["widget"].control.currentIndex()]
        avatar_name = current_avatar.GetName()
        avatar = RLPy.RScene.FindObject( RLPy.EObjectType_Avatar, avatar_name )
        RLPy.RScene.SelectObject(avatar)
        output_assetDict['avatar']['asset']=avatar
        output_assetDict['avatar']['name']=avatar_name
        output_assetDict['avatar']['rlmotion']=avatar_name+'.rlmotion'
    if ui["widget"].checkProp.isChecked():
        output_assetDict['prop']={}
        current_prop = all_props[ui["widget"].prop.currentIndex()]
        prop_name = current_prop.GetName()
        prop = RLPy.RScene.FindObject( RLPy.EObjectType_Prop, prop_name )
        RLPy.RScene.SelectObject(prop)
        output_assetDict['prop']['asset']=prop
        output_assetDict['prop']['name']=prop_name
        output_assetDict['prop']['rlmotion']=prop_name+'.iProp'
    if ui["widget"].checkCamera.isChecked():
        output_assetDict['camera']={}
        current_camera = all_cameras[ui["widget"].camera.currentIndex()]
        camera_name = current_camera.GetName()
        camera = RLPy.RScene.FindObject( RLPy.EObjectType_Camera, camera_name )
        RLPy.RScene.SelectObject(camera)
        output_assetDict['camera']['asset']=camera
        output_assetDict['camera']['name']=camera_name
        output_assetDict['camera']['rlmotion']=camera_name+'.iCam'

    fbxpath = ui["widget"].fbxpath.text()
    uepath = ui["widget"].uepath.text()
    #'C:\Users\Public\Documents\Reallusion\Custom\iClone 7 Custom'
    custom_data_path = RLPy.RApplication.GetCustomDataPath()

    if not os.path.isfile(uepath):
        print('>>>Error: Need output UE4 Project File!')
        return
    if not os.path.isdir(fbxpath):
        print('>>>Error: Need output path!')
        return
    for key in output_assetDict.keys():
        if output_assetDict[key]['name']=='None':
            print('>>>Error: Need output {0} Name!'.format(str(key).upper()))
            return
        output_assetDict[key]['fbxfile'] = os.path.join(fbxpath,output_assetDict[key]['name']+'.fbx').replace('/','\\')
        #include_motion_path = os.path.join(fbxpath,rlmotion)
        if key == 'avatar':
            output_assetDict[key]['include_motion_path'] = r'{0}/{1}.rlmotion'.format(os.path.join(custom_data_path,'Motion'),output_assetDict[key]['name'])
        if key == 'prop':
            output_assetDict[key]['include_motion_path'] = r'{0}/{1}.iProp'.format(os.path.join(custom_data_path,'Props'),output_assetDict[key]['name'])
        if key == 'camera':
            output_assetDict[key]['include_motion_path'] = r'{0}/{1}.iCam'.format(os.path.join(custom_data_path,'Camera'),output_assetDict[key]['name'])
        print(output_assetDict[key]['include_motion_path'])
    # texture format
    default_format = RLPy.EExportTextureFormat_Default
    if ui["widget"].format.currentIndex() == 1: #'Bmp':
        default_format = RLPy.EExportTextureFormat_Bmp
    elif ui["widget"].format.currentIndex() == 2: #'Jpeg':
        default_format = RLPy.EExportTextureFormat_Jpeg
    elif ui["widget"].format.currentIndex() == 3:#'Tga':
        default_format = RLPy.EExportTextureFormat_Tga
    elif ui["widget"].format.currentIndex() == 4: #'Png':
        default_format = RLPy.EExportTextureFormat_Png
    elif ui["widget"].format.currentIndex() == 5: #'Tif':
        default_format = RLPy.EExportTextureFormat_Tif
    
    # export fbx for Unreal
    export_option = RLPy.EExportFbxOptions__None
    export_option2 = RLPy.EExportFbxOptions2__None
    export_option3 = RLPy.EExportFbxOptions3__None
    export_option = export_option | RLPy.EExportFbxOptions_FbxKey
    if ui["widget"].RemoveAllMesh.isChecked():
        export_option = export_option | RLPy.EExportFbxOptions_RemoveAllMesh
    if ui["widget"].AutoSkinRigidMesh.isChecked():
        export_option = export_option | RLPy.EExportFbxOptions_AutoSkinRigidMesh
    if ui["widget"].ExportRootMotion.isChecked():
        export_option = export_option | RLPy.EExportFbxOptions_ExportRootMotion
    if ui["widget"].ZeroMotionRoot.isChecked():
        export_option = export_option | RLPy.EExportFbxOptions_ZeroMotionRoot
    if ui["widget"].ExportPbrTextureAsImageInFormatDirectory.isChecked():
        export_option = export_option | RLPy.EExportFbxOptions_ExportPbrTextureAsImageInFormatDirectory
    if ui["widget"].InverseNormalY.isChecked():
        export_option = export_option | RLPy.EExportFbxOptions_InverseNormalY
    if ui["widget"].UnrealEngine4BoneAxis.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_UnrealEngine4BoneAxis
    if ui["widget"].RenameDuplicateBoneName.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameDuplicateBoneName
    if ui["widget"].RenameDuplicateMaterialName.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameDuplicateMaterialName
    if ui["widget"].RenameTransparencyWithPostFix.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameTransparencyWithPostFix
    if ui["widget"].RenameBoneRootToGameType.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameBoneRootToGameType
    if ui["widget"].RenameBoneToLowerCase.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameBoneToLowerCase
    if ui["widget"].ResetBoneScale.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_ResetBoneScale
    if ui["widget"].ResetSelfillumination.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_ResetSelfillumination
    if ui["widget"].ExtraWordForUnityAndUnreal.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_ExtraWordForUnityAndUnreal
    if ui["widget"].BakeMouthOpenMotionToMesh.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_BakeMouthOpenMotionToMesh
    if ui["widget"].UnrealIkBone.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_UnrealIkBone
    if ui["widget"].UnrealPreset.isChecked():
        export_option2 = export_option2 | RLPy.EExportFbxOptions2_UnrealPreset

    original_size = RLPy.EExportTextureSize_Original
    destpath = os.path.join(os.path.dirname(uepath),'Content','icloneFBX')
    main_widget = wrapInstance(int(RLPy.RUi.GetMainWindow()), PySide2.QtWidgets.QWidget)
    title=main_widget.windowTitle()
    project = title.split('-')[-1].strip()
    newline=''
    for key in output_assetDict.keys():
        if key == 'avatar':
            result = RLPy.RFileIO.ExportFbxFile( output_assetDict[key]['asset'], output_assetDict[key]['fbxfile'],export_option, export_option2, export_option3,original_size,default_format,output_assetDict[key]['include_motion_path'])
        #else:
            #result = RLPy.RFileIO.ExportFbxFile( output_assetDict[key]['asset'], output_assetDict[key]['fbxfile'],export_option, export_option2, export_option3,original_size,default_format,'e:/cone.iMotionPlus')
            print('''1:RLPy.RStatus.Success
                        2:RLPy.RStatus.Failure
                        3:RLPy.RStatus.InsufficientMemory
                        4:RLPy.RStatus.LicenseFailure
                        5:RLPy.RStatus.IncompatibleVersion
                        6:RLPy.RStatus.InvalidParameter
                        7:RLPy.RStatus.UnknownParameter
                        8:RLPy.RStatus.NotImplemented
                        10:RLPy.RStatus.Deprecated
                        11:RLPy.RStatus.NotFound
                        12:RLPy.RStatus.EndOfFile''')
            print('>>>Information:{0}'.format(result.GetStatusCode()))
        elif key == 'prop':
            RLPy.RScene.SelectObject(prop)
            newline = clickExportFBX(output_assetDict[key]['fbxfile'],project)
        elif key == 'camera':
            RLPy.RScene.SelectObject(camera)
            newline = clickExportFBX(output_assetDict[key]['fbxfile'],project)
        copyFbx(output_assetDict[key]['fbxfile'],destpath)
        runCmd(key,output_assetDict[key]['fbxfile'],output_assetDict[key]['name'],uepath,newline)
    return

def fbxfileSet():
    fbx_folder = PySide2.QtWidgets.QFileDialog.getExistingDirectory()
    ui["widget"].fbxpath.setText(fbx_folder)
    return

def ueFolderSet():
    ue_folder,_ = PySide2.QtWidgets.QFileDialog.getOpenFileName(None,'打开UE4项目文件','./','Project Files(*.uproject)')
    ui["widget"].uepath.setText(ue_folder)
    return

def reset_ui():
    global ui
    # Dropdowns
    ui["widget"].control.setCurrentIndex(0)
    ui["widget"].camera.setCurrentIndex(0)
    ui["widget"].prop.setCurrentIndex(0)
    ui["widget"].format.setCurrentIndex(0)
    # Frame Duration
    if ap_version == 7:
        start_frame = RLPy.RTime.GetFrameIndex(RLPy.RGlobal.GetStartTime(), RLPy.RGlobal.GetFps())
        end_frame = RLPy.RTime.GetFrameIndex(RLPy.RGlobal.GetEndTime(), RLPy.RGlobal.GetFps())
    if ap_version == 8:
        start_frame = RLPy.GetFrameIndex( RLPy.RGlobal_GetStartTime(),RLPy.RGlobal_GetFps())
        end_frame = RLPy.GetFrameIndex( RLPy.RGlobal_GetEndTime(),RLPy.RGlobal_GetFps())
    ui["widget"].start_frame.setValue(start_frame)
    ui["widget"].end_frame.setValue(end_frame)
    update_ui()

def update_ui():
    global ui, events,all_avatars,all_props,all_cameras

    fps = RLPy.RGlobal.GetFps()
    avatars = RLPy.RScene.GetAvatars()
    props = RLPy.RScene.GetProps()
    cameras = RLPy.RScene.FindObjects(RLPy.EObjectType_Camera)
    
    current_avatar = all_avatars[ui["widget"].control.currentIndex()]
    current_prop = all_props[ui["widget"].prop.currentIndex()]
    current_camera = all_cameras[ui["widget"].camera.currentIndex()]
    current_fbxpath = ui["widget"].fbxpath.text()
    # add avatars
    ui["widget"].control.blockSignals(True)
    ui["widget"].control.clear()
    ui["widget"].control.addItem("None")   
    i=0
    for i in range(len(avatars)):
        all_avatars.append(avatars[i])
        ui["widget"].control.addItem(avatars[i].GetName())
        if avatars[i] == current_avatar:
            ui["widget"].control.setCurrentIndex(i+1)
    ui["widget"].control.blockSignals(False)
    # add props
    ui["widget"].prop.blockSignals(True)
    ui["widget"].prop.clear()
    ui["widget"].prop.addItem("None")    
    i=0
    for i in range(len(props)):
        all_props.append(props[i])
        ui["widget"].prop.addItem(props[i].GetName())
        if props[i] == current_prop:
            ui["widget"].prop.setCurrentIndex(i+1)
    ui["widget"].prop.blockSignals(False)
    # add cameras
    ui["widget"].camera.blockSignals(True)
    ui["widget"].camera.clear()
    ui["widget"].camera.addItem("None")  
    i=0
    for i in range(len(cameras)):
        all_cameras.append(cameras[i])
        ui["widget"].camera.addItem(cameras[i].GetName())
        if cameras[i] == current_camera:
            ui["widget"].camera.setCurrentIndex(i+1)
    ui["widget"].camera.blockSignals(False)
    return

def show_window():
    global ui, events

    if "window" in ui:  # If the window already exists...
        if ui["window"].IsVisible():
            RLPy.RUi.ShowMessageBox(
                "FBX Transfer Animation- Operation Error",
                "The current FBX Transfer for UE4 session is still running.  You must first close the window to start another session.",
                RLPy.EMsgButton_Ok)
        else:
            ui["window"].Show()
        return

    # Create an iClone Dock Widget
    ui["window"] = RLPy.RUi.CreateRDockWidget()
    ui["window"].SetWindowTitle("FBX Transfer Animation For UE4")
    ui["window"].SetAllowedAreas(RLPy.EDockWidgetAreas_RightDockWidgetArea | RLPy.EDockWidgetAreas_LeftDockWidgetArea)

    # Load UI file
    ui_file = QtCore.QFile(os.path.dirname(__file__) + "/FBX_Transfer_Animation.ui")
    ui_file.open(QtCore.QFile.ReadOnly)
    ui["widget"] = QtUiTools.QUiLoader().load(ui_file)
    ui_file.close()

    # Assign the UI file to the Pyside dock widget and show it
    ui["dialog"] = wrapInstance(int(ui["window"].GetWindow()), QtWidgets.QDockWidget)
    ui["dialog"].setWidget(ui["widget"])

    # Add UI functionality
    ui["widget"].control.currentIndexChanged.connect(update_ui)
    ui["widget"].prop.currentIndexChanged.connect(update_ui)
    ui["widget"].camera.currentIndexChanged.connect(update_ui)
    ui["widget"].format.currentIndexChanged.connect(update_ui)
    ui["widget"].loadBTN.clicked.connect(fbxfileSet)
    ui["widget"].loadueBTN.clicked.connect(ueFolderSet)
    ui["widget"].updateBTN.clicked.connect(reset_ui)
    ui["widget"].exportBTN.clicked.connect(exportFbx)

    # Register events
    events["callback"] = EventCallback()
    events["callback_id"] = RLPy.REventHandler.RegisterCallback(events["callback"])
    events["dialog_callback"] = DialogCallback()
    ui["window"].RegisterEventCallback(events["dialog_callback"])

    # Show the UI
    ui["window"].Show()
    reset_ui()


def initialize_plugin():
    # Create Pyside interface with iClone main window
    ic_dlg = wrapInstance(int(RLPy.RUi.GetMainWindow()), QtWidgets.QMainWindow)
    # Check if the menu item exists
    plugin_menu = ic_dlg.menuBar().findChild(QtWidgets.QMenu, "pysample_menu")
    if plugin_menu is None:
        # Create Pyside layout for QMenu named "Python Samples" and attach it to the Plugins menu
        plugin_menu = wrapInstance(int(RLPy.RUi.AddMenu("Python Samples", RLPy.EMenu_Plugins)), QtWidgets.QMenu)
        plugin_menu.setObjectName("pysample_menu")  # Setting an object name for the menu is equivalent to giving it an ID
    # Add the "Smooth Camera Follow" menu item to Plugins > Python Samples
    menu_action = plugin_menu.addAction("FBX Transfer Animation")
    # Show the dialog window when the menu item is triggered
    menu_action.triggered.connect(show_window)


def run_script():
    initialize_plugin()