import os,re
import unreal
asset_name = '0Zane_0'
iclone_folder = 'icloneFBX'
project_path = 'E:/test/uasset/MyCppProject/Content'
# 0.Zane(0)
fbx_name = '{0}.{1}({2}).fbx'.format(asset_name[0],re.sub(r'[0-9,_]','',asset_name),asset_name[-1])
_FBX_file = '{0}/{1}/{2}'.format(project_path, iclone_folder,fbx_name)
game_sequence = '/Game/Sequences'
game_rlcontent = '/Game/RLContent'
sequence_path = '{0}/MyLevelSequence'.format(game_sequence)
actor_path = '{0}/{1}/{1}'.format(game_rlcontent, asset_name)
animation_path = '/Game/{0}/{1}_'.format(iclone_folder, asset_name)
_skeleton_path = '{0}/{1}/{1}_Skeleton'.format(game_rlcontent,asset_name)

def create_level_sequence(asset_name, package_path = '{0}/'.format(game_sequence)):
    # 创建LevelSequence资源
    #fps_seq=unreal.FrameRate(numerator=25, denominator=1)
    sequence = unreal.AssetToolsHelpers.get_asset_tools().create_asset(asset_name, package_path, unreal.LevelSequence, unreal.LevelSequenceFactoryNew())
    #sequence.set_display_rate(fps_seq)
    return sequence

def getOrAddPossessableInSequenceAsset(sequence_path='',actor=None):
    sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path)) # 绑定 sequence 资产
    #possessable = sequence_asset.add_possessable(object_to_possess=actor) # 添加 actor 资产到 sequence
    possessable = sequence_asset.add_spawnable_from_instance(actor)
    return possessable

def addSkeletalAnimationTrackOnPossessable(animation_path='', possessable=None):
    # Get Animation 获取动画
    animation_asset = unreal.AnimSequence.cast(unreal.load_asset(animation_path))
    params = unreal.MovieSceneSkeletalAnimationParams() # 电影场景骨骼动画参数
    params.set_editor_property('Animation', animation_asset)
    # Add track 添加轨道
    animation_track = possessable.add_track(track_type=unreal.MovieSceneSkeletalAnimationTrack) # 添加轨道，类型为动画类型
    # Add section 添加动画片段
    animation_section = animation_track.add_section()
    animation_section.set_editor_property('Params', params)
    animation_section.set_range(0, animation_asset.get_editor_property('sequence_length'))

def addSkeletalAnimationTrackOnActor(actor_path,animation_path):
    create_level_sequence('MyLevelSequence')
    
    #actor_in_world = unreal.GameplayStatics.get_all_actors_of_class(unreal.EditorLevelLibrary.get_editor_world(), unreal.SkeletalMeshActor)()[0]
    possessable_in_sequence = getOrAddPossessableInSequenceAsset(sequence_path, unreal.load_asset(actor_path))
    print(type(possessable_in_sequence))
    addSkeletalAnimationTrackOnPossessable(animation_path, possessable_in_sequence)

def buildAnimationImportOptions(skeleton_path):
    ''' 动画导入Options '''   
    options = unreal.FbxImportUI()
    options.mesh_type_to_import = unreal.FBXImportType.FBXIT_ANIMATION
    options.import_rigid_mesh=False
    options.import_as_skeletal=False
    options.set_editor_property('automated_import_should_detect_type', False)
    options.set_editor_property('import_animations', True) # 导入动画时选这个
    options.set_editor_property('import_mesh', False)
    options.set_editor_property('import_as_skeletal', False)
    options.set_editor_property('import_materials', False)

    options.skeleton = unreal.load_asset(skeleton_path)  # 在这里选择目标骨架
    options.anim_sequence_import_data.set_editor_property(
        'import_translation', unreal.Vector(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property(
        'import_rotation', unreal.Rotator(0.0, 0.0, 0.0))
    options.anim_sequence_import_data.set_editor_property(
        'import_uniform_scale', 1.0)
    options.anim_sequence_import_data.set_editor_property(
        'animation_length', unreal.FBXAnimationLengthImportType.FBXALIT_EXPORTED_TIME)
    options.anim_sequence_import_data.set_editor_property(
        'remove_redundant_keys', False)
    
    return options

def buildImportTask(file_name='None', destinataion_path='/Game/icloneFBX', options=None):
    task = unreal.AssetImportTask()
    task.set_editor_property('automated', True)
    task.set_editor_property('destination_name', '')
    task.set_editor_property('destination_path', destinataion_path)
    task.set_editor_property('filename', file_name)
    task.set_editor_property('replace_existing', True)
    task.set_editor_property('save', True)
    task.set_editor_property('options', options) 
    return task

def executeImportTasks(tasks):
    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks(tasks)
    for task in tasks:
        for path in task.get_editor_property('imported_object_paths'):
            print('Improted: %s' % path)

def importCamera(sequence=None,import_filename='None'):
    create_level_sequence('MyLevelSequence')
    sequence_asset = unreal.LevelSequence.cast(unreal.load_asset(sequence_path))
    world = unreal.EditorLevelLibrary.get_editor_world()
    bindings = sequence_asset.get_bindings()
    # Set Options
    import_options = unreal.MovieSceneUserImportFBXSettings()
    import_options.set_editor_property("create_cameras",True)
    import_options.set_editor_property("reduce_keys",False)
    # 4.27
    unreal.SequencerTools.import_level_sequence_fbx(world, sequence_asset, bindings, import_options, import_filename)
    unreal.EditorAssetLibrary.save_loaded_asset(sequence_asset, False)

if __name__ == "__main__":
# avatar and prop import
#option = buildAnimationImportOptions(_skeleton_path)
#animation_task = buildImportTask(file_name=_FBX_file, destinataion_path='/Game/icloneFBX', options=option)
#executeImportTasks([animation_task])
# no use=>addSkeletalAnimationTrackOnActor(_actor_path,_animation_path)
#importCamera(sequence=sequence_path, import_filename=_FBX_file) #camera import