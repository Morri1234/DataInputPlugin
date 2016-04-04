# -*- coding: utf-8 -*-

# List comprehensions in canvasMoveEvent functions are 
# adapted from Benjamin Bohard`s part of rectovaldiams plugin.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from DataInputFrontages_dockwidget import DataInputFrontagesDockWidget


####################################################################CONTROLLED###################################################################################

# Tool class
class GroundControlledDefault(QgsMapTool): 
    
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(GroundControlledDefault, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Default")
        v_layer.changeAttributeValue(finalid, 3, "Ground Floor")



class GroundControlledService(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(GroundControlledService, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Service Entrance")
        v_layer.changeAttributeValue(finalid, 3, "Ground Floor")
        



class GroundControlledFire(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(GroundControlledFire, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Fire Exit")
        v_layer.changeAttributeValue(finalid, 3, "Ground Floor")



class GroundControlledUnused(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(GroundControlledUnused, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Unused")
        v_layer.changeAttributeValue(finalid, 3, "Ground Floor")



class UpperControlledDefault(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(UpperControlledDefault, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Default")
        v_layer.changeAttributeValue(finalid, 3, "Upper Floor")



class UpperControlledService(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(UpperControlledService, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Service Entrance")
        v_layer.changeAttributeValue(finalid, 3, "Upper Floor")



class UpperControlledFire(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(UpperControlledFire, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Fire Exit")
        v_layer.changeAttributeValue(finalid, 3, "Upper Floor")




class UpperControlledUnused(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(UpperControlledUnused, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Unused")
        v_layer.changeAttributeValue(finalid, 3, "Upper Floor")




class LowerControlledDefault(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(LowerControlledDefault, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Default")
        v_layer.changeAttributeValue(finalid, 3, "Lower Floor")




class LowerControlledService(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(LowerControlledService, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Service Entrance")
        v_layer.changeAttributeValue(finalid, 3, "Lower Floor")




class LowerControlledFire(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(LowerControlledFire, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Fire Exit")
        v_layer.changeAttributeValue(finalid, 3, "Lower Floor")




class LowerControlledUnused(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(LowerControlledUnused, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Controlled")
        v_layer.changeAttributeValue(finalid, 2, "Unused")
        v_layer.changeAttributeValue(finalid, 3, "Lower Floor")


####################################################################UNCONTROLLED###################################################################################



# Tool class
class GroundUNControlledDefault(QgsMapTool): 
    
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(GroundUNControlledDefault, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Uncontrolled")
        v_layer.changeAttributeValue(finalid, 2, "Default")
        v_layer.changeAttributeValue(finalid, 3, "Ground Floor")




class UpperUNControlledDefault(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(UpperUNControlledDefault, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Uncontrolled")
        v_layer.changeAttributeValue(finalid, 2, "Default")
        v_layer.changeAttributeValue(finalid, 3, "Upper Floor")





class LowerUNControlledDefault(QgsMapTool): 
    

    def __init__(self, canvas):
        self.canvas = canvas
        s = QSettings()
        s.beginGroup('Qgis')
        color = QColor(0,0,255)
        s.endGroup()
        rbDict = {}

        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw = QgsRubberBand(self.canvas, False)
        self.rubberBandDraw.setColor(color)
        self.rubberBandDraw.setWidth(1)
        self.rubberBand.setColor(color)
        self.rubberBand.setWidth(1)
        # self.rubberBand.setLineStyle(Qt.DashLine)
        self.points=[]
        points = self.points
        global points
        self.pluginIsActive = False
        self.dockwidget = DataInputFrontagesDockWidget()
        
               

        self.reset()
        self.cursor = QCursor(QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #1210f3",
                                      "                ",
                                      "       +.+      ",
                                      "      + . +     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " +.    . .    .+",
                                      " ... ...+... ...",
                                      " +.    . .     +",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "    +.     .+   ",
                                      "     +.....+    ",
                                      "      + . +     ",
                                      "       +.+      "]))
                

    def reset(self):
        pass


    def canvasPressEvent(self, event):
        pass          
                  
            
    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
                     
        if event.button() == 1:

            self.AddPoint() 
            self.updatePfeature()
            self.reset()
            
        

    def AddPoint(self):
        self.isEmittingPoint = True
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPoint(self.startPoint))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
          
        
        self.reset()
        mc.refresh()  

           
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(LowerUNControlledDefault, self).activate()
         self.emit(SIGNAL("activated()"))
         self.canvas.setCursor(self.cursor)
        

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True


    def updatePfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        v_layer.changeAttributeValue(finalid, 1, "Uncontrolled")
        v_layer.changeAttributeValue(finalid, 2, "Default")
        v_layer.changeAttributeValue(finalid, 3, "Lower Floor")




