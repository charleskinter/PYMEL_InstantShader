import pymel.core as pm
from pymel.all import *
import os
class InstantShader(object):
    def __init__(self):
        self.supportedextentions = ['jpg','gif','png','tif','bmp']
        self.selection = pm.ls(sl=True)
        print self.selection
        self.name = os.path.basename(self.folder)
        self.files = os.listdir(self.folder)
        print self.files 
        self.filelist = []
        self.mapDict ={}
        self.filenodes = []
	
    def connectFileNodes(self,item): #Connect up file nodes
        texture = item
        print texture
        if texture.split('_')[0] in self.cmapAttr.keys():
            attribute = str(self.createdShader[0]+'.'+self.cmapAttr[texture.split('_')[0]])
            try:
                print attribute
                pm.connectAttr(texture.outColor, attribute)
            except:
                print attribute
                pm.connectAttr(texture.outAlpha, attribute)
        
        if texture.split('_')[0] == 'Norm':                    
                attribute = str(self.createdShader[0]+'.normalCamera')
                bump2dnode = pm.shadingNode('bump2d',name='Normal_%s'%texture.split('_')[1], asUtility=True)
                pm.connectAttr(texture.outAlpha, bump2dnode.bumpValue)
                pm.connectAttr(bump2dnode.outNormal,attribute)
                pm.setAttr(bump2dnode.bumpInterp, 2)
        
        if texture.split('_')[0] == 'Bump':                    
                attribute = str(self.createdShader[0]+'.normalCamera')
                bump2dnode = pm.shadingNode('bump2d',name='Bump_%s'%texture.split('_')[1], asUtility=True)
                pm.connectAttr(texture.outAlpha, bump2dnode.bumpValue)
                pm.connectAttr(bump2dnode.outNormal,attribute)
       
        if texture.split('_')[0] == 'Disp':                    
               attribute = str(self.createdShader[1]+'.displacementShader')
               disp2dnode = pm.shadingNode('displacementShader',name='Disp_%s'%texture.split('_')[1], asUtility=True)
               pm.connectAttr(texture.outAlpha, disp2dnode.displacement)
               pm.connectAttr(disp2dnode.displacement,attribute)        
			   
      
        
    def processFolder(self): #parse files in folder and either fix the prefix or connect up the file nodes'        
        for item in self.files:
            if '.' in item:     
                if (item.split('.')[1]) in self.supportedextentions:
                    self.filelist.append(item)
        for item in self.filelist: 
            if item.split('_')[0] in self.mapDict.keys():
                self.mapDict[item.split('_')[0]] = item
                self.connectFileNodes(self.processtex(item))
            else:
                self.fixPrefix(item)
    
    
                    
    def AddPrefix(self,item,premenu,windows,*args): #adds a prefix if needed  
        prefix = premenu.getValue()
        if prefix != 'Skip':
            print item
            print prefix
            print 'worked'
            newthing = self.folder+'/'+prefix+'_'+item
            oldthing = self.folder+'/'+item
            print oldthing
            print newthing     
            os.rename(oldthing,newthing)
            pm.deleteUI(windows, window=True)
            self.mapDict[prefix] = str(prefix+'_'+item)
            print item
            newnode = self.processtex(self.mapDict[prefix]) 
            self.connectFileNodes(newnode) 
        else:
            print 'skipped'        
            pm.deleteUI(windows, window=True)     
	

			
    def fixPrefix(self,item): #Prompts User For Prefixes
        
        print 'broke',item
        fixprefixwindow = pm.window()
        layout = pm.columnLayout()
        title = pm.text(label = 'The file %s does not have the correct prefix \n Please select the correct one below or Skip.'%(item))
        prefixMenu = pm.optionMenu(label='Correct Prefix?')
        skip = pm.menuItem( label='Skip')
        for option in self.mapDict.keys():
            pm.menuItem( label=option )
        SubmitButton = pm.button(label ='Submit',c =Callback(self.AddPrefix,item,prefixMenu,fixprefixwindow))
        close = pm.button(label='Close', command=('pm.deleteUI(\"' +fixprefixwindow + '\", window=True)') )
        pm.showWindow(fixprefixwindow) 
        
        
 
    
    def processtex(self,item): #Connect place 2d Texture nodes to File Nodes)    
        
        fileTruename = item.split(".")
        fileNode = pm.shadingNode('file',name='%s'%fileTruename[0], asTexture=True)
        fullfile = self.folder + '\\' + item 
        fileNode.setAttr('fileTextureName',str(fullfile))
        p2d = pm.shadingNode('place2dTexture', name='is2d%s'%fileTruename[0], asUtility=True)
        fileNode.filterType.set(0)
        pm.connectAttr(p2d.outUV, fileNode.uvCoord)
        pm.connectAttr(p2d.outUvFilterSize, fileNode.uvFilterSize)
        pm.connectAttr(p2d.vertexCameraOne, fileNode.vertexCameraOne)
        pm.connectAttr(p2d.vertexUvOne, fileNode.vertexUvOne)
        pm.connectAttr(p2d.vertexUvThree, fileNode.vertexUvThree)
        pm.connectAttr(p2d.vertexUvTwo, fileNode.vertexUvTwo)
        pm.connectAttr(p2d.coverage, fileNode.coverage)
        pm.connectAttr(p2d.mirrorU, fileNode.mirrorU)
        pm.connectAttr(p2d.mirrorV, fileNode.mirrorV)
        pm.connectAttr(p2d.noiseUV, fileNode.noiseUV)
        pm.connectAttr(p2d.offset, fileNode.offset)
        pm.connectAttr(p2d.repeatUV, fileNode.repeatUV)
        pm.connectAttr(p2d.rotateFrame, fileNode.rotateFrame)
        pm.connectAttr(p2d.rotateUV, fileNode.rotateUV)
        pm.connectAttr(p2d.stagger, fileNode.stagger)
        pm.connectAttr(p2d.translateFrame, fileNode.translateFrame)
        pm.connectAttr(p2d.wrapU, fileNode.wrapU)
        pm.connectAttr(p2d.wrapV, fileNode.wrapV)          
        print fileNode,' connected'
        return fileNode
        
    def applyShader(self):
        if len(self.selection) > 0:
            for item in self.selection:
                pm.select(item)
                print 'item is',item
                pm.hyperShade(a=self.createdShader)
                 
                 


        
class InstantaiStandardSurface(InstantShader):
    '''	Instant AI Standard Surface Shader
		By Charles Kinter
		Usage assign variable to InstantaiStandardSurface(PATH) where PATH is a string to your folder of textures'''	
    def __init__(self,folder):
        self.folder = folder
        super(InstantaiStandardSurface,self).__init__()
        self.mapDict= {'DifC':'','DifR':'','Metl':'','SpeC':'','TraC':'','SubC':'','CoaC':'','CoaR':'','EmiC':'','EmiW':'','Opac':'','Bump':'','Norm':'','Disp':''}
        self.cmapAttr ={'DifC':'baseColor','DifR':'diffuseRoughness','Metl':'metalness','SpeC':'specularColor','TraC':'transmissionColor','SubC':'subsurfaceColor','CoaC':'coatColor','CoaR':'coatRoughness','EmiC':'emissionColor','EmiW':'emission','Opac':'opacity'}
        self.createdShader = pm.createSurfaceShader('aiStandardSurface',name=self.name)
        self.processFolder()
        for item in self.filenodes:
            print item
            self.connectFileNodes(item) 
        self.applyShader()



class InstantBlinn(InstantShader):
    '''	Instant Blinn Shader
		By Charles Kinter
		Usage assign variable to InstantaiStandardSurface(PATH) where PATH is a string to your folder of textures'''	
    def __init__(self,folder):
        self.folder = folder
        super(InstantBlinn,self).__init__()
        self.mapDict= {'Bump':'','Norm':'','Disp':'','Color':'','Incd':'','SpeC':'','Tran':'','AmbC':'','RefC':''}
        self.cmapAttr ={'Color':'color','Incd':'incandescence','SpeC':'specularColor','Tran':'transparency','AmbC':'ambientColor','RefC':'reflectedColor'}
        self.createdShader = pm.createSurfaceShader('blinn',name=self.name)
        self.processFolder()
        for item in self.filenodes:
            print item
            self.connectFileNodes(item)
        self.applyShader()    
             
class InstantPhong(InstantShader):
    '''	Instant Phong Shader
		By Charles Kinter
		Usage assign variable to InstantaiStandardSurface(PATH) where PATH is a string to your folder of textures'''	
    def __init__(self,folder):
        self.folder = folder
        super(InstantPhong,self).__init__()
        self.mapDict= {'Bump':'','Norm':'','Disp':'','Color':'','Incd':'','SpeC':'','Tran':'','AmbC':'','RefC':''}
        self.cmapAttr ={'Color':'color','Incd':'incandescence','SpeC':'specularColor','Tran':'transparency','AmbC':'ambientColor','RefC':'reflectedColor'}
        self.createdShader = pm.createSurfaceShader('phong',name=self.name)
        self.processFolder()
        for item in self.filenodes:
            print item
            self.connectFileNodes(item)
        self.applyShader()
        
class InstantLambert(InstantShader):
    '''	Instant Lambert Shader
		By Charles Kinter
		Usage assign variable to InstantaiStandardSurface(PATH) where PATH is a string to your folder of textures'''	
    def __init__(self,folder):
        self.folder = folder
        super(InstantLambert,self).__init__()
        self.mapDict= {'Bump':'','Norm':'','Disp':'','Color':'','Incd':'','SpeC':'','Tran':'','AmbC':'','RefC':''}
        self.cmapAttr ={'Color':'color','Incd':'incandescence','SpeC':'specularColor','Tran':'transparency','AmbC':'ambientColor','RefC':'reflectedColor'}
        self.createdShader = pm.createSurfaceShader('lambert',name=self.name)
        self.processFolder()
        for item in self.filenodes:
            print item
            self.connectFileNodes(item)
        self.applyShader()
                          


