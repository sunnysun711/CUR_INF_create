import os
import re

CUR_DIR = os.getcwd().split(os.sep)[-1]

# 获取当前目录下的所有 .cur 和 .ani 文件
files = list(filter(lambda file: not os.path.isdir(file), os.listdir(os.getcwd())))
# 过滤出所有 .cur 和 .ani 文件
all_files = list(filter(lambda name: bool(re.findall(r'(^.*\.ani$)|(^.*\.cur$)', name)), files))

# 按文件名称排序
all_files.sort()

# 只取前15个文件
ls = all_files[:15]

# 确定第16和第17个文件，分别对应 location_select 和 person_select
location_select = None
person_select = None

# 获取第16个和第17个文件（如果存在）
if len(all_files) > 15:
    location_select = all_files[15]  # 第16个文件
if len(all_files) > 16:
    person_select = all_files[16]  # 第17个文件

# 更新 Strings_list，将第16和第17个文件作为 location-select 和 person-select
Strings_list = [
    'pointer', 'help', 'work', 'busy', 'cross', 'text', 'hand', 'unavailiable',
    'vert', 'horz', 'dgn1', 'dgn2', 'move', 'alternate', 'link'
]
Strings_list = list(
    map(lambda h, f: h + ' = \"' + f + '\"\r\n', Strings_list, ls))

# 如果存在 location_select 和 person_select 文件，则将它们添加到 Strings_list
if location_select:
    Strings_list.append(f'locationSelect = \"{location_select}\"\r\n')
if person_select:
    Strings_list.append(f'personSelect = \"{person_select}\"\r\n')

# 生成INF文件头
inf_head = r'''[Version]
signature="$CHICAGO$"

[DefaultInstall]
CopyFiles = Scheme.Cur
AddReg    = Scheme.Reg,Wreg

[DestinationDirs]
Scheme.Cur = 10,"%CUR_DIR%"

[Scheme.Reg]
HKCU,"Control Panel\Cursors\Schemes","%SCHEME_NAME%",,"%10%\%CUR_DIR%\%pointer%,%10%\%CUR_DIR%\%help%,%10%\%CUR_DIR%\%work%,%10%\%CUR_DIR%\%busy%,%10%\%CUR_DIR%\%Cross%,%10%\%CUR_DIR%\%Text%,%10%\%CUR_DIR%\%Hand%,%10%\%CUR_DIR%\%Unavailiable%,%10%\%CUR_DIR%\%Vert%,%10%\%CUR_DIR%\%Horz%,%10%\%CUR_DIR%\%Dgn1%,%10%\%CUR_DIR%\%Dgn2%,%10%\%CUR_DIR%\%move%,%10%\%CUR_DIR%\%alternate%,%10%\%CUR_DIR%\%link%,%10%\%CUR_DIR%\%locationSelect%,%10%\%CUR_DIR%\%personSelect%"'''

# 如果存在 location_select 和 person_select 文件，则将它们添加到注册表部分
if location_select:
    inf_head += f',%10%\%CUR_DIR%\%locationSelect%'
if person_select:
    inf_head += f',%10%\%CUR_DIR%\%person_select%'

inf_head += r'''

[Wreg]
HKCU,"Control Panel\Cursors",,0x00020000,"%SCHEME_NAME%"
HKCU,"Control Panel\Cursors",AppStarting,0x00020000,"%10%\%CUR_DIR%\%work%"
HKCU,"Control Panel\Cursors",Arrow,0x00020000,"%10%\%CUR_DIR%\%pointer%"
HKCU,"Control Panel\Cursors",Crosshair,0x00020000,"%10%\%CUR_DIR%\%Cross%"
HKCU,"Control Panel\Cursors",Hand,0x00020000,"%10%\%CUR_DIR%\%link%"
HKCU,"Control Panel\Cursors",Help,0x00020000,"%10%\%CUR_DIR%\%Help%"
HKCU,"Control Panel\Cursors",IBeam,0x00020000,"%10%\%CUR_DIR%\%Text%"
HKCU,"Control Panel\Cursors",No,0x00020000,"%10%\%CUR_DIR%\%Unavailiable%"
HKCU,"Control Panel\Cursors",NWPen,0x00020000,"%10%\%CUR_DIR%\%Hand%"
HKCU,"Control Panel\Cursors",SizeAll,0x00020000,"%10%\%CUR_DIR%\%move%"
HKCU,"Control Panel\Cursors",SizeNESW,0x00020000,"%10%\%CUR_DIR%\%Dgn2%"
HKCU,"Control Panel\Cursors",SizeNS,0x00020000,"%10%\%CUR_DIR%\%Vert%"
HKCU,"Control Panel\Cursors",SizeNWSE,0x00020000,"%10%\%CUR_DIR%\%Dgn1%"
HKCU,"Control Panel\Cursors",SizeWE,0x00020000,"%10%\%CUR_DIR%\%Horz%"
HKCU,"Control Panel\Cursors",UpArrow,0x00020000,"%10%\%CUR_DIR%\%alternate%"
HKCU,"Control Panel\Cursors",Wait,0x00020000,"%10%\%CUR_DIR%\%busy%"'''

# 如果存在 location_select 和 person_select 文件，添加到注册表
if location_select:
    inf_head += f'\nHKCU,"Control Panel\Cursors",LocationSelect,0x00020000,"%10%\%CUR_DIR%\%locationSelect%"'
if person_select:
    inf_head += f'\nHKCU,"Control Panel\Cursors",PersonSelect,0x00020000,"%10%\%fCUR_DIR%\%personSelect%"'

inf_head += r'''
HKLM,"SOFTWARE\Microsoft\Windows\CurrentVersion\Runonce\Setup\","",,"rundll32.exe shell32.dll,Control_RunDLL main.cpl @0,1"

'''

# 写入INF文件
with open('Install.inf', 'w', newline='') as inf:
    inf.write(inf_head)
    inf.write('[Scheme.Cur]\r\n')
    for i in ls:  # 先写入前15个文件
        inf.write('\"' + i + '\"\r\n')
    # 如果存在 location_select 和 person_select，写入它们
    if location_select:
        inf.write('\"' + location_select + '\"\r\n')
    if person_select:
        inf.write('\"' + person_select + '\"\r\n')
    inf.write('\r\n')
    inf.write('[Strings]\r\n')
    inf.write('CUR_DIR = \"Cursors\\' + CUR_DIR + '\"\r\n')
    inf.write('SCHEME_NAME = \"' + CUR_DIR + '\"\r\n')
    inf.write('SCHEME_DESCRIPTION = \"' + CUR_DIR + '\"\r\n')
    inf.writelines(Strings_list)

i = input("Do you want to install it now?")
if (i.strip() in ["", "Y", "y"]):
    #auto
    import subprocess
    s = subprocess.Popen(
        "rundll32 syssetup,SetupInfObjectInstallAction DefaultInstall 128 ./Install.inf",
        shell=True)
    s.wait()
    input("Install Success")
else:
    input(
        "Click on the file Install.inf right mouse button, the shortcut menu to choose - to install"
    )
