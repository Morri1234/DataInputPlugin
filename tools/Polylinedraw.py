# -*- coding: utf-8 -*-

# List comprehensions in canvasMoveEvent functions are 
# adapted from Benjamin Bohard`s part of rectovaldiams plugin.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math

# Tool class
class OvalFromCenterTool(QgsMapTool):
   canvasDoubleClicked = QtCore.pyqtSignal(object, object)
   
   def __init__(self, canvas,layer,Vertex_list,mergeDlg):
        QgsMapTool.__init__(self, canvas)
        self.canvas = canvas
        self.layer=layer
        self.Vertex_list=Vertex_list
        self.mergeDlg=mergeDlg
        self.rb = QgsRubberBand(self.canvas, QGis.Line)
        self.rb.setColor(QColor(255, 0, 0))
        self.rb.setWidth(2)
        self.rb.reset()

    def canvasPressEvent(self, event):

        if event.button() == 1:
            print "helo"
            x = event.pos().x()
            y = event.pos().y()
            Lpoint = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)

    def canvasMoveEvent(self, event):
        pass

    def canvasReleaseEvent(self, event):
        #Get the click
        if event.button() == 2:
            print "hello right"
            x = event.pos().x()
            y = event.pos().y()
            Rpoint = self.canvas.getCoordinateTransform().toMapCoordinates(x, y)
            self.Vertex_list.append(Rpoint)
            print self.Vertex_list

    def canvasSelectionChanged(self,layer):

        pass
    def activate(self):
        pass

    def deactivate(self):
        pass

    def isZoomTool(self):
        return False

    def isTransient(self):
        return False

    def isEditTool(self):
        return True
            