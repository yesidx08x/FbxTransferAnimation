import RLPy
import os

fbxfile = r"E://temp//fbxIclone//fbx//avatar.fbx"
motionpath = r"E://temp//fbxIclone//fbx//Tpose.rlmotion"
avatar_name = "0.Zane(0)"

# load object
avatar = RLPy.RScene.FindObject( RLPy.EObjectType_Avatar, avatar_name )
#print(type(avatar),avatar.GetName())
RLPy.RScene.SelectObject(avatar)
fbxfile = os.path.join(os.path.dirname,avatar_name+'.fbx')

# export fbx for Unreal
export_option = RLPy.EExportFbxOptions__None
export_option2 = RLPy.EExportFbxOptions2__None
export_option3 = RLPy.EExportFbxOptions3__None
export_option = export_option | RLPy.EExportFbxOptions_AutoSkinRigidMesh
export_option = export_option | RLPy.EExportFbxOptions_ExportRootMotion
export_option = export_option | RLPy.EExportFbxOptions_ZeroMotionRoot
export_option = export_option | RLPy.EExportFbxOptions_ExportPbrTextureAsImageInFormatDirectory
export_option = export_option | RLPy.EExportFbxOptions_InverseNormalY
export_option2 = export_option2 | RLPy.EExportFbxOptions2_UnrealEngine4BoneAxis
export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameDuplicateBoneName
export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameDuplicateMaterialName
export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameTransparencyWithPostFix
export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameBoneRootToGameType
export_option2 = export_option2 | RLPy.EExportFbxOptions2_RenameBoneToLowerCase
export_option2 = export_option2 | RLPy.EExportFbxOptions2_ResetBoneScale
export_option2 = export_option2 | RLPy.EExportFbxOptions2_ResetSelfillumination
export_option2 = export_option2 | RLPy.EExportFbxOptions2_ExtraWordForUnityAndUnreal
export_option2 = export_option2 | RLPy.EExportFbxOptions2_BakeMouthOpenMotionToMesh
export_option2 = export_option2 | RLPy.EExportFbxOptions2_UnrealIkBone
export_option2 = export_option2 | RLPy.EExportFbxOptions2_UnrealPreset

'''
RLPy.EExportTextureFormat_Default
RLPy.EExportTextureFormat_Bmp
RLPy.EExportTextureFormat_Jpeg
RLPy.EExportTextureFormat_Tga
RLPy.EExportTextureFormat_Png
RLPy.EExportTextureFormat_Tif
'''
original_size = RLPy.EExportTextureSize_Original
default_format = RLPy.EExportTextureFormat_Default 

#result = RLPy.RFileIO.ExportFbxFile( avatar, fbxfile, export_option, export_option2, export_option3, original_size, default_format, motionpath )
result = RLPy.RFileIO.ExportFbxFile( avatar, fbxfile,export_option, export_option2, export_option3,default_format)
print(result.GetStatusCode())
#print(result.IsError())