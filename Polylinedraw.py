# -*- coding: utf-8 -*-

# List comprehensions in canvasMoveEvent functions are 
# adapted from Benjamin Bohard`s part of rectovaldiams plugin.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *




# Tool class
class HighOpaqueFence(QgsMapTool): 
    
    azimuth_calcul = pyqtSignal(QgsPoint, QgsPoint)   

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
        self.points = []
        allpoints = self.points
        global allpoints
        

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
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(False)
        self.rubberBandDraw.reset(False)
     


    def canvasPressEvent(self, event):
        self.isEmittingPoint = False           
                  
            
    def canvasMoveEvent(self, event):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(event.pos())
        
        if len(self.points) > 0:
            self.rubberBand.setToGeometry(
                QgsGeometry.fromPolyline([self.startPoint,self.endPoint]),None)
            if (self.startPoint is not None and self.endPoint is not None and self.startPoint != self.endPoint):
                self.azimuth_calcul.emit(self.startPoint, self.endPoint)
        

    def canvasReleaseEvent(self, event):
        self.isEmittingPoint = True
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
        if len(self.points) < 2:
            self.rubberBandDraw.reset(QGis.Line)
            self.rubberBand.reset(QGis.Line)
            self.points.append(self.startPoint)
        if len(self.points) > 2:
            self.rubberBandDraw.setToGeometry(QgsGeometry.fromPolyline(self.points),None)
            
            self.isEmittingPoint = False
        if event.button() == 2:
            self.AddLine() 
            self.reset()
            del self.points[:]
            self.deleteFeatures()
        

    def AddLine(self):
        final = allpoints[:-1]
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPolyline(final))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
        self.updateLfeature()  
        self.UpdateLength()
        self.reset()
        mc.refresh()  

    def deleteFeatures(self):
        mc = self.canvas
        layer15 =  mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = -1')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )

        mc = self.canvas
        layer15 = mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = 0')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )           
        mc.refresh()

       
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(HighOpaqueFence, self).activate()
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

    def updateLfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        data = v_layer.dataProvider()

        updat1 = data.fieldNameIndex("Group")
        updat2 = data.fieldNameIndex("Type")

        v_layer.changeAttributeValue(finalid, updat1, "Fences",True)
        v_layer.changeAttributeValue(finalid, updat2, "High Opaque Fence",True)
        
    def UpdateLength(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['Length'] = geom.length()
            v_layer.updateFeature(feat)


class HighSeeThroughFence(QgsMapTool):
      
    azimuth_calcul = pyqtSignal(QgsPoint, QgsPoint)   

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
        self.points = []
        allpoints = self.points
        global allpoints
        

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
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(False)
        self.rubberBandDraw.reset(False)
     


    def canvasPressEvent(self, event):
        self.isEmittingPoint = False           
                  
            
    def canvasMoveEvent(self, event):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(event.pos())
        
        if len(self.points) > 0:
            self.rubberBand.setToGeometry(
                QgsGeometry.fromPolyline([self.startPoint,self.endPoint]),None)
            if (self.startPoint is not None and self.endPoint is not None and self.startPoint != self.endPoint):
                self.azimuth_calcul.emit(self.startPoint, self.endPoint)
        

    def canvasReleaseEvent(self, event):
        self.isEmittingPoint = True
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
        if len(self.points) < 2:
            self.rubberBandDraw.reset(QGis.Line)
            self.rubberBand.reset(QGis.Line)
            self.points.append(self.startPoint)
        if len(self.points) > 2:
            self.rubberBandDraw.setToGeometry(QgsGeometry.fromPolyline(self.points),None)
            
            self.isEmittingPoint = False
        if event.button() == 2:
            self.AddLine() 
            self.reset()
            del self.points[:]
            self.deleteFeatures()
        

    def AddLine(self):
        final = allpoints[:-1]
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPolyline(final))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
        self.updateLfeature()  
        self.UpdateLength()
        self.reset()
        mc.refresh()  


    def deleteFeatures(self):
        mc = self.canvas
        layer15 =  mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = -1')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )

        mc = self.canvas
        layer15 = mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = 0')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )           
        mc.refresh()

       
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(HighSeeThroughFence, self).activate()
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

    def updateLfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        data = v_layer.dataProvider()

        updat1 = data.fieldNameIndex("Group")
        updat2 = data.fieldNameIndex("Type")

        v_layer.changeAttributeValue(finalid, updat1, "Fences", True)
        v_layer.changeAttributeValue(finalid, updat2, "High See Through Fence", True)
        
    def UpdateLength(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['Length'] = geom.length()
            v_layer.updateFeature(feat)


   

class LowFence(QgsMapTool):
      
    azimuth_calcul = pyqtSignal(QgsPoint, QgsPoint)   

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
        self.points = []
        allpoints = self.points
        global allpoints
        

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
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(False)
        self.rubberBandDraw.reset(False)
     


    def canvasPressEvent(self, event):
        self.isEmittingPoint = False           
                  
            
    def canvasMoveEvent(self, event):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(event.pos())
        
        if len(self.points) > 0:
            self.rubberBand.setToGeometry(
                QgsGeometry.fromPolyline([self.startPoint,self.endPoint]),None)
            if (self.startPoint is not None and self.endPoint is not None and self.startPoint != self.endPoint):
                self.azimuth_calcul.emit(self.startPoint, self.endPoint)
        

    def canvasReleaseEvent(self, event):
        self.isEmittingPoint = True
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
        if len(self.points) < 2:
            self.rubberBandDraw.reset(QGis.Line)
            self.rubberBand.reset(QGis.Line)
            self.points.append(self.startPoint)
        if len(self.points) > 2:
            self.rubberBandDraw.setToGeometry(QgsGeometry.fromPolyline(self.points),None)
            
            self.isEmittingPoint = False
        if event.button() == 2:
            self.AddLine() 
            self.reset()
            del self.points[:]
            self.deleteFeatures()
        

    def AddLine(self):
        final = allpoints[:-1]
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPolyline(final))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
        self.updateLfeature()  
        self.UpdateLength()
        self.reset()
        mc.refresh()  


    def deleteFeatures(self):
        mc = self.canvas
        layer15 =  mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = -1')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )

        mc = self.canvas
        layer15 = mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = 0')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )           
        mc.refresh()

       
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(LowFence, self).activate()
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

    def updateLfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        data = v_layer.dataProvider()

        updat1 = data.fieldNameIndex("Group")
        updat2 = data.fieldNameIndex("Type")

        v_layer.changeAttributeValue(finalid, updat1, "Fences", True)
        v_layer.changeAttributeValue(finalid, updat2, "Low Fence", True)
        
    def UpdateLength(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['Length'] = geom.length()
            v_layer.updateFeature(feat)


    


class TransparentFrontage(QgsMapTool):  
      
    azimuth_calcul = pyqtSignal(QgsPoint, QgsPoint)   

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
        self.points = []
        allpoints = self.points
        global allpoints
        

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
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(False)
        self.rubberBandDraw.reset(False)
     


    def canvasPressEvent(self, event):
        self.isEmittingPoint = False           
                  
            
    def canvasMoveEvent(self, event):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(event.pos())
        
        if len(self.points) > 0:
            self.rubberBand.setToGeometry(
                QgsGeometry.fromPolyline([self.startPoint,self.endPoint]),None)
            if (self.startPoint is not None and self.endPoint is not None and self.startPoint != self.endPoint):
                self.azimuth_calcul.emit(self.startPoint, self.endPoint)
        

    def canvasReleaseEvent(self, event):
        self.isEmittingPoint = True
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
        if len(self.points) < 2:
            self.rubberBandDraw.reset(QGis.Line)
            self.rubberBand.reset(QGis.Line)
            self.points.append(self.startPoint)
        if len(self.points) > 2:
            self.rubberBandDraw.setToGeometry(QgsGeometry.fromPolyline(self.points),None)
            
            self.isEmittingPoint = False
        if event.button() == 2:
            self.AddLine() 
            self.reset()
            del self.points[:]
            self.deleteFeatures()
        

    def AddLine(self):
        final = allpoints[:-1]
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPolyline(final))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
        self.updateLfeature()  
        self.UpdateLength()
        self.reset()
        mc.refresh()  

    def deleteFeatures(self):
        mc = self.canvas
        layer15 =  mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = -1')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )

        mc = self.canvas
        layer15 = mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = 0')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )           
        mc.refresh()

       
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(TransparentFrontage, self).activate()
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

    def updateLfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        data = v_layer.dataProvider()

        updat1 = data.fieldNameIndex("Group")
        updat2 = data.fieldNameIndex("Type")

        v_layer.changeAttributeValue(finalid, updat1, "Buildings", True)
        v_layer.changeAttributeValue(finalid, updat2, "Transparent", True)
        
    def UpdateLength(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['Length'] = geom.length()
            v_layer.updateFeature(feat)


class BlankFrontage(QgsMapTool): 
    
    azimuth_calcul = pyqtSignal(QgsPoint, QgsPoint)   

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
        self.points = []
        allpoints = self.points
        global allpoints
        

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
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(False)
        self.rubberBandDraw.reset(False)
     


    def canvasPressEvent(self, event):
        self.isEmittingPoint = False           
                  
            
    def canvasMoveEvent(self, event):
        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(event.pos())
        
        if len(self.points) > 0:
            self.rubberBand.setToGeometry(
                QgsGeometry.fromPolyline([self.startPoint,self.endPoint]),None)
            if (self.startPoint is not None and self.endPoint is not None and self.startPoint != self.endPoint):
                self.azimuth_calcul.emit(self.startPoint, self.endPoint)
        

    def canvasReleaseEvent(self, event):
        self.isEmittingPoint = True
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
        if len(self.points) < 2:
            self.rubberBandDraw.reset(QGis.Line)
            self.rubberBand.reset(QGis.Line)
            self.points.append(self.startPoint)
        if len(self.points) > 2:
            self.rubberBandDraw.setToGeometry(QgsGeometry.fromPolyline(self.points),None)
            
            self.isEmittingPoint = False
        if event.button() == 2:
            self.AddLine() 
            self.reset()
            del self.points[:]
            self.deleteFeatures()
        

    def AddLine(self):
        final = allpoints[:-1]
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPolyline(final))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
        self.updateLfeature()  
        self.UpdateLength()
        self.reset()
        mc.refresh()  

    def deleteFeatures(self):
        mc = self.canvas
        layer15 =  mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = -1')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )

        mc = self.canvas
        layer15 = mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = 0')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )           
        mc.refresh()

       
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(BlankFrontage, self).activate()
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

    def updateLfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        data = v_layer.dataProvider()

        updat1 = data.fieldNameIndex("Group")
        updat2 = data.fieldNameIndex("Type")

        v_layer.changeAttributeValue(finalid, updat1, "Building", True)
        v_layer.changeAttributeValue(finalid, updat2, "Blank", True)
        
    def UpdateLength(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['Length'] = geom.length()
            v_layer.updateFeature(feat)\



class SemiTransparentFrontage(QgsMapTool): 
    
    azimuth_calcul = pyqtSignal(QgsPoint, QgsPoint)   

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
        self.points = []
        allpoints = self.points
        global allpoints
        self.count = 0
        # 2 markers and vertex points
        self.m1 = None #QgsVertexMarker(self.canvas)
        self.m2 = None #QgsVertexMarker(self.canvas)
        self.p1 = QgsPoint()
        self.p2 = QgsPoint()
        

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
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(False)
        self.rubberBandDraw.reset(False)
     


    def canvasPressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
    
        layer = self.canvas.currentLayer()
    
        if layer <> None:
            startingPoint = QPoint(x,y)
      
            snapper = QgsMapCanvasSnapper(self.canvas)
      
            #we snap to the current layer (we don't have exclude points and use the tolerances from the qgis properties)
            (retval,result) = snapper.snapToCurrentLayer (startingPoint, QgsSnapper.SnapToVertex)
                       
            #so if we don't have found a vertex we try to find one on the backgroundlayer
            if result == []:
                (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
        self.isEmittingPoint = False           
                  
            
    def canvasMoveEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
    
        layer = self.canvas.currentLayer()
    
        if layer <> None:
            startingPoint = QPoint(x,y)
      
            snapper = QgsMapCanvasSnapper(self.canvas)
      
            #we snap to the current layer (we don't have exclude points and use the tolerances from the qgis properties)
            (retval,result) = snapper.snapToCurrentLayer (startingPoint, QgsSnapper.SnapToVertex)
                       
            #so if we don't have found a vertex we try to find one on the backgroundlayer
            if result == []:
                (retval,result) = snapper.snapToBackgroundLayers(startingPoint)

        if not self.isEmittingPoint:
            return
        self.endPoint = self.toMapCoordinates(event.pos())
        
        if len(self.points) > 0:
            self.rubberBand.setToGeometry(
                QgsGeometry.fromPolyline([self.startPoint,self.endPoint]),None)
            if (self.startPoint is not None and self.endPoint is not None and self.startPoint != self.endPoint):
                self.azimuth_calcul.emit(self.startPoint, self.endPoint)
                

    def canvasReleaseEvent(self, event):
        #Get the click
        x = event.pos().x()
        y = event.pos().y()
    
        layer = self.canvas.currentLayer()
    
        if layer <> None:
            startingPoint = QPoint(x,y)
      
            snapper = QgsMapCanvasSnapper(self.canvas)
      
            #we snap to the current layer (we don't have exclude points and use the tolerances from the qgis properties)
            (retval,result) = snapper.snapToCurrentLayer (startingPoint, QgsSnapper.SnapToVertex)
                       
            #so if we don't have found a vertex we try to find one on the backgroundlayer
            if result == []:
                (retval,result) = snapper.snapToBackgroundLayers(startingPoint)
          
            if result <> []:

                #mark the vertex 
                if self.count == 0:
                    #self.p1 = QgsPoint()
                    self.p1.setX( result[0].snappedVertex.x() )  
                    self.p1.setY( result[0].snappedVertex.y() )  
                
                    self.m1 = QgsVertexMarker(self.canvas)
                    self.m1.setIconType(1)
                    self.m1.setColor(QColor(255,0,0))
                    self.m1.setIconSize(12)
                    self.m1.setPenWidth (3)            
                    self.m1.setCenter(self.p1)

                    self.count = self.count + 1
                
                elif self.count == 1:
                    self.p2.setX( result[0].snappedVertex.x() )  
                    self.p2.setY( result[0].snappedVertex.y() )  

                    self.m2 = QgsVertexMarker(self.canvas)
                    self.m2.setIconType(1)
                    self.m2.setColor(QColor(0,0,255))
                    self.m2.setIconSize(12)
                    self.m2.setPenWidth (3)            
                    self.m2.setCenter(self.p2)

                    self.count = self.count + 1
                         
                    self.emit(SIGNAL("vertexFound(PyQt_PyObject)"), [self.p1, self.p2,  self.m1,  self.m2])     
                
                elif self.count == 2:
                    #QMessageBox.information(None,  "Cancel",  str(self.m1))
                    self.p1.setX( self.p2.x() )
                    self.p1.setY( self.p2.y() )
                    self.m1.setCenter(self.p1)
                    
                    self.p2.setX( result[0].snappedVertex.x() )  
                    self.p2.setY( result[0].snappedVertex.y() )  
                    self.m2.setCenter(self.p2)
                    
                    self.emit(SIGNAL("vertexFound(PyQt_PyObject)"), [self.p1, self.p2,  self.m1,  self.m2])
            
            else:
                #warn about missing snapping tolerance if appropriate
                pass

        self.isEmittingPoint = True
        self.startPoint = self.toMapCoordinates(event.pos())
        self.points.append(QgsPoint(self.startPoint))
        if len(self.points) < 2:
            self.rubberBandDraw.reset(QGis.Line)
            self.rubberBand.reset(QGis.Line)
            self.points.append(self.startPoint)
        if len(self.points) > 2:
            self.rubberBandDraw.setToGeometry(QgsGeometry.fromPolyline(self.points),None)
            
            self.isEmittingPoint = False
        if event.button() == 2:
            self.AddLine() 
            self.reset()
            del self.points[:]
            self.deleteFeatures()
        

    def AddLine(self):
        final = allpoints[:-1]
        mc = self.canvas
        v_layer = mc.currentLayer()
        pr = v_layer.dataProvider()
        seg = QgsFeature()
        feat = seg.geometry()
        seg.setGeometry(QgsGeometry.fromPolyline(final))
        # new feature: line from line_end to newpoint
        pr.addFeatures( [ seg ] )
        v_layer.updateExtents()
        # add the line to 
        QgsMapLayerRegistry.instance().addMapLayers([v_layer])   
        v_layer.updateExtents()

        mapRenderer = QgsMapRenderer()

        rect = v_layer.extent()
        mapRenderer.setExtent(rect)
        self.updateLfeature()  
        self.UpdateLength()
        self.reset()
        mc.refresh()  

    def deleteFeatures(self):
        mc = self.canvas
        layer15 =  mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = -1')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )

        mc = self.canvas
        layer15 = mc.currentLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Length" = 0')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )           
        mc.refresh()

       
    def canvasSelectionChanged(self,layer):
        pass

    def activate(self):
         self.reset()
         super(SemiTransparentFrontage, self).activate()
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

    def updateLfeature(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()
        
        for feat in features:
            fid = feat.id()
            idlist = [fid]
            maxid = max(idlist)
            
        finalid = int(maxid)

        print finalid

        data = v_layer.dataProvider()

        updat1 = data.fieldNameIndex("Group")
        updat2 = data.fieldNameIndex("Type")

        v_layer.changeAttributeValue(finalid, updat1, "Building", True)
        v_layer.changeAttributeValue(finalid, updat2, "Semi Transparent", True)
        
    def UpdateLength(self):
        mc = self.canvas
        v_layer = mc.currentLayer()
        features = v_layer.getFeatures()

        for feat in features:
            geom = feat.geometry()
            feat['Length'] = geom.length()
            v_layer.updateFeature(feat)

    


    
