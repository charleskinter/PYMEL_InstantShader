''' This Script was written by Charles Kinter Charles@kinters.net
To install:
1: Put instantShaderUI.py and instantShaderClass.py in your C:\Users\'user'\Documents\maya\scripts folder 
2. Add new shelf item with the following script:
				import instantShaderUI
				iscWindow()
To use:
1. Select object to assign to if desired. 
2. Select Shader from drop down and hit create.				
3. Select folder of images for your shader (will be name of shader). Must be in 'jpg','gif','png','tif','bmp' formats.
4. If files are named with correct prefixes shader will be created. 
   If not you will be prompted to fix each prefix and then the shader will be created.
5. Your newly created shader will be selected, take a moment to verify settings and enjoy.
'''   
   
   
import pymel.core as pm
from pymel.all import *
import instantShaderClassV2 as isc
def iscWindow():
    if pm.window('iscWin', exists=True):
        pm.deleteUI('iscWin', window=True)
    shaderlist = {'Blinn':'isc.InstantBlinn(path)','Lambert':'isc.InstantLambert(path)','Phong':'isc.InstantPhong(path)','Arnold aiStandardSurface':'isc.InstantaiStandardSurface(path)'}
    iscWin = pm.window('iscWin',title='Charles Kinters instant shader',rtf=True, h=256)
    menuBar = pm.menuBarLayout(w=100)
    contactMenu  = pm.menu(label = 'Help')
    contactLink = pm.menuItem(label = 'Website: http://charles.kinters.net',command = 'pm.launch(web="http://charles.kinters.net/sample-page/contact-me/")')
    iscWinlayout = pm.rowColumnLayout('iscWinlayout')
    iscWintitle = pm.text(label = 'Please select the type of Instant Shader you wish to create.',align = 'left')

    iscMenu = pm.optionMenu('iscMenu',label='Shader Type?')
    skip = pm.menuItem( label='Please Select Shader')
    for option in shaderlist.keys():
        pm.menuItem( label=option )
    iscPath = pm.folderButtonGrp(label = 'Path to texture folder:', cl3=('left','left','left'))
    btnLayout = pm.rowColumnLayout('butns',nc=2,p='iscWinlayout')    
    SubmitButton = pm.button(label ='Create',c =Callback(CreateShader,iscMenu,shaderlist,iscPath),p='butns')
    close = pm.button(label='Close', command=('pm.deleteUI(\"' +iscWin + '\", window=True)') ,p='butns')
    pm.showWindow(iscWin)

def CreateShader(iscMenu,shaders,iscpath):
    selobj = pm.ls(sl=True)
    selection = iscMenu.getValue()
    if selection != 'Please Select Shader':
        path = iscpath.getText()
        createme = shaders[selection]
        shader = eval(createme)
        print type(shader)
        if selobj !=[]:
            pm.select(selobj)
            pm.hyperShade(assign=shader.createdShader[0])
            pm.select(shader.createdShader[0])
        else:
            pm.select(shader.createdShader[0])
        
iscWindow()        
