# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DataInputFrontages
                                 A QGIS plugin
 DataInputFrontages
                              -------------------
        begin                : 2016-01-18
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Abhimanyu Acharya
        email                : a.acharya@spacesyntax.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, Qt, QVariant, pyqtSlot
from PyQt4.QtGui import QAction, QIcon, QFileDialog, QMessageBox, QProgressBar,QComboBox
# Initialize Qt resources from file resources.py


# Import the code for the DockWidget
from DataInputFrontages_dockwidget import DataInputFrontagesDockWidget
import processing
from qgis.core import *
from qgis.gui import *
import os
from Polylinedraw import HighOpaqueFence, HighSeeThroughFence, LowFence, TransparentFrontage, SemiTransparentFrontage, BlankFrontage
from Pointdraw import GroundControlledDefault, GroundControlledService, GroundControlledFire, GroundControlledUnused, UpperControlledDefault, UpperControlledService, UpperControlledFire, UpperControlledUnused, LowerControlledDefault, LowerControlledService, LowerControlledFire, LowerControlledUnused, GroundUNControlledDefault, UpperUNControlledDefault, LowerUNControlledDefault
import resources
from PyQt4 import QtCore, QtGui
from poopup_dialog import poopupDialog
from trace_dialog import traceDialog
from tracescommit_dialog import tracescommitDialog


class DataInputFrontages:
    dialogClosed = QtCore.pyqtSignal()
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'DataInputFrontages_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Urban Data Input')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Urban Data Input')
        self.toolbar.setObjectName(u'Urban Data Input')

        #print "** INITIALIZING DataInputFrontages"

        self.pluginIsActive = False
        self.dockwidget = None
        self.canvas = self.iface.mapCanvas()
        self.dlg = poopupDialog()
        self.dlg.pushButton.clicked.connect(self.deleteFeatures)
        self.dlg.pushButton_2.clicked.connect(self.deletelinesrunclose)

        self.dlg2 = traceDialog()
        self.dlg3 = tracescommitDialog()





    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('DataInputFrontages', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/DataInputFrontages/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Urban Data Input'),
            callback=self.run,
            parent=self.iface.mainWindow())


    #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    ##############################################################################FRONTAGES#############################################################################################

    def closeEvent(self, event):
        self.dialogClosed.emit()
        return QtGui.QDockWidget.closeEvent(self, event)


    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        print "** CLOSING DataInputFrontages"

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)


        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        
        self.dockwidget = None

        self.pluginIsActive = False


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""

        #print "** UNLOAD DataInputFrontages"
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&DataInputFrontages'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar

#Delete Lines for Frontages with NULL value

    def deletelinesrun(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()

    def deletelinesrunclose(self):
        self.dlg.close()
        
#Import draw tools


    def DrawTransparent(self):
        self.transparenttool = TransparentFrontage( self.canvas )
        self.canvas.setMapTool(self.transparenttool)
        

    def DrawSemiTransparent(self):
        self.semitransparenttool = SemiTransparentFrontage( self.canvas )
        self.canvas.setMapTool(self.semitransparenttool)

    def DrawBlank(self):
        self.blank = BlankFrontage( self.canvas )
        self.canvas.setMapTool(self.blank)

    def DrawHighOpaqueFence(self):
        self.highopaquefencetool = HighOpaqueFence( self.canvas )
        self.canvas.setMapTool(self.highopaquefencetool)

    def DrawSTFence(self):
        self.highstfencetool = HighSeeThroughFence( self.canvas )
        self.canvas.setMapTool(self.highstfencetool)

    def DrawLowFence(self):
        self.lowfencetool = LowFence( self.canvas )
        self.canvas.setMapTool(self.lowfencetool)

#Load Thematic Style    

    def CustomThematic(self):
        if self.dockwidget.comboBox_F12.currentText() == "SSL Standard":
            mc = self.canvas
            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/frontages.qml"
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(qml_path)
            mc.refresh()
            

        else:
            mc = self.canvas
            plugin_path = self.dockwidget.lineEdit_F5.text()
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(plugin_path)
            mc.refresh()

    #Add New thematic to combobox

    def select_input_qml(self):
        filenameLU = QFileDialog.getOpenFileName(self.dockwidget, "Select Input File","", '*.qml')
        self.dockwidget.comboBox_F12.addItem(filenameLU)
        self.dockwidget.lineEdit_F5.setText(filenameLU)
        self.dockwidget.comboBox_F12.setItemText(1,"Custom Thematic")
        self.dockwidget.comboBox_F12.setItemText(2,"Custom Thematic 1")
        self.dockwidget.comboBox_F12.setItemText(3,"Custom Thematic 2")
        self.dockwidget.comboBox_F12.setItemText(4,"Custom Thematic 3") 
        self.dockwidget.comboBox_F12.setItemText(5,"Custom Thematic 4")

    #Open/Load/Save File

    def select_output_file(self):
        filename = QFileDialog.getSaveFileName(self.dockwidget, "Select Save Location ","", '*.shp')
        self.dockwidget.lineEdit_2.setText(filename)

    def select_input_file(self):
        filename = QFileDialog.getOpenFileName(self.dockwidget, "Select Input File ","", '*.shp')
        self.dockwidget.lineEdit.setText(filename)

    def select_existing_file(self):
        filename = QFileDialog.getOpenFileName(self.dockwidget, "Load Existing File ","", '*.shp')
        self.dockwidget.lineEdit_3.setText(filename)

    def Loadfile(self):
        location1 = self.dockwidget.lineEdit_3.text()
        input5 = self.iface.addVectorLayer(location1, "Frontages", "ogr")

        if not input5:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location1 )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location1 )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        input5.startEditing()

        plugin_path = os.path.dirname(__file__)
        qml_path = plugin_path + "/frontages.qml"
        input7 = self.iface.activeLayer()
        input7.loadNamedStyle(qml_path)

        self.dockwidget.lineEdit_3.setPlaceholderText('Select Load Location')
        mc = self.canvas
        layer78 = mc.currentLayer()
        if layer78.geometryType() == 1: 
            self.dockwidget.pushButton_f.setEnabled(True)
            self.dockwidget.pushButton_g.setEnabled(True)
            self.dockwidget.pushButton_h.setEnabled(True)
            self.dockwidget.pushButton_i.setEnabled(True)
            self.dockwidget.pushButton_j.setEnabled(True)
            self.dockwidget.pushButton_k.setEnabled(True) 
            self.dockwidget.pushButton_l.setEnabled(True)
            self.dockwidget.pushButton_m.setEnabled(True)
            self.dockwidget.pushButton_n.setEnabled(True)
            self.dockwidget.pushButton_o.setEnabled(True)
            self.dockwidget.pushButton_p.setEnabled(True)
            self.dockwidget.pushButton_q.setEnabled(True)
            self.dockwidget.pushButton_xx.setEnabled(True)
            self.dockwidget.comboBox_F12.setEditable(True)
            self.dockwidget.pushButton_s.setEnabled(True)
            self.dockwidget.toolButton_r.setEnabled(True)

        self.dockwidget.lineEdit_3.setPlaceholderText('Select Load Location...')

#Create Polylines from plogons and save a frontages layer
    def explode(self):
        
        input1 = self.dockwidget.lineEdit.text()
        processing.runandload("qgis:polygonstolines",input1,"memory:line2poly")
        input2 = self.iface.activeLayer()
        processing.runandload("qgis:explodelines",input2,"memory:Exploded")

        input3 = self.iface.activeLayer()
        location = self.dockwidget.lineEdit_2.text()
        QgsVectorFileWriter.writeAsVectorFormat(input3, location, "System", None, "ESRI Shapefile")

        removelayer = QgsMapLayerRegistry.instance().mapLayersByName( "memory:line2poly" )[0]
        QgsMapLayerRegistry.instance().removeMapLayers( [removelayer.id()] )
        removelayer = QgsMapLayerRegistry.instance().mapLayersByName( "memory:Exploded" )[0]
        QgsMapLayerRegistry.instance().removeMapLayers( [removelayer.id()] )

        input4 = self.iface.addVectorLayer(location, "Frontages", "ogr")

        if not input4:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        input4.startEditing()
               

        edit1 = input4.dataProvider()
        edit1.addAttributes( [ QgsField("Group", QVariant.String),
                QgsField("Type",  QVariant.String),
                QgsField("Length", QVariant.Double) ] )
        input4.commitChanges()
        input4.startEditing()

        plugin_path = os.path.dirname(__file__)
        qml_path = plugin_path + "/frontages.qml"
        input7 = self.iface.activeLayer()
        input7.loadNamedStyle(qml_path)
        
        self.dockwidget.lineEdit_2.setPlaceholderText('Select Save Location...')
        self.dockwidget.lineEdit.setPlaceholderText('Select Input File...')

        mc = self.canvas
        layer78 = mc.currentLayer()
        if layer78.geometryType() == 1: 
            self.dockwidget.pushButton_f.setEnabled(True)
            self.dockwidget.pushButton_g.setEnabled(True)
            self.dockwidget.pushButton_h.setEnabled(True)
            self.dockwidget.pushButton_i.setEnabled(True)
            self.dockwidget.pushButton_j.setEnabled(True)
            self.dockwidget.pushButton_k.setEnabled(True)
            self.dockwidget.pushButton_l.setEnabled(True)
            self.dockwidget.pushButton_m.setEnabled(True)
            self.dockwidget.pushButton_n.setEnabled(True)
            self.dockwidget.pushButton_o.setEnabled(True)
            self.dockwidget.pushButton_p.setEnabled(True)
            self.dockwidget.pushButton_q.setEnabled(True)
            self.dockwidget.pushButton_xx.setEnabled(True)
            self.dockwidget.comboBox_F12.setEditable(True)
            self.dockwidget.pushButton_s.setEnabled(True)
            self.dockwidget.toolButton_r.setEnabled(True)


#Redundant Doesnt work

    def deleteFeatures(self):
        mc = self.canvas
        layer15 = self.iface.activeLayer()
        request = QgsFeatureRequest().setFilterExpression(u'"Group" IS NULL')
        ids = [f.id() for f in layer15.getFeatures(request)]
        layer15.startEditing()
        layer15.dataProvider().deleteFeatures( ids )
        

        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Facades with "NULL" data deleted' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )
        mc.refresh()
        self.dlg.close()


#Update Selection
    
    def updateTransparent(self):
        layer1 = self.iface.activeLayer()

        features = layer1.selectedFeatures()  
        
        for feat in features:
            feat['Group'] = "Building"
            feat['Type'] = "Transparent"
            geom = feat.geometry()
            feat['Length'] = geom.length()
            layer1.updateFeature(feat)
        
        

        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated : Transparent' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )
                  
        layer1.startEditing()  

    def updateSemiTransparent(self):
        layer1 = self.iface.activeLayer()

        features = layer1.selectedFeatures()  
        
        for feat in features:
            feat['Group'] = "Building"
            feat['Type'] = "Semi Transparent"
            geom = feat.geometry()
            feat['Length'] = geom.length()
            layer1.updateFeature(feat)
        
        

        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated : Semi Transparent' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )
                  
        layer1.startEditing()

    def updateBlank(self):
        layer1 = self.iface.activeLayer()

        features = layer1.selectedFeatures()  
        
        for feat in features:
            feat['Group'] = "Building"
            feat['Type'] = "Blank"
            geom = feat.geometry()
            feat['Length'] = geom.length()
            layer1.updateFeature(feat)
        
          

        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated : Blank' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )
                  
        layer1.startEditing() 

    def updateFenceHighOpaque(self):
        layer1 = self.iface.activeLayer()

        features = layer1.selectedFeatures()  
        
        for feat in features:
            feat['Group'] = "Fences"
            feat['Type'] = "High Opaque Fence"
            geom = feat.geometry()
            feat['Length'] = geom.length()
            layer1.updateFeature(feat)
        
         

        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated : High Opaque Fence' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )
                  
        layer1.startEditing()    

    def updateFenceHighSeeThrough(self):
        layer1 = self.iface.activeLayer()

        features = layer1.selectedFeatures()  
        
        for feat in features:
            feat['Group'] = "Fences"
            feat['Type'] = "High See Through Fence"
            geom = feat.geometry()
            feat['Length'] = geom.length()
            layer1.updateFeature(feat)
        
         

        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated : High See Through Fence' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )
                  
        layer1.startEditing()


    def updateFenceLow(self):
        layer1 = self.iface.activeLayer()

        features = layer1.selectedFeatures()  
        
        for feat in features:
            feat['Group'] = "Fences"
            feat['Type'] = "Low Fence"
            geom = feat.geometry()
            feat['Length'] = geom.length()
            layer1.updateFeature(feat)
        
          

        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated : Low Fence' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )
                  
        layer1.startEditing()


    #Update Combobox with required file types


    def Frnt_updatelist(self):
        layers = self.iface.legendInterface().layers()
        self.dockwidget.comboBox_3.clear()
        self.dockwidget.comboBox_4.clear()
        layer_list4 = []
        layer_list5 = []

        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon:
                self.dockwidget.comboBox_3.setEditable(True)
                layer_list4.append(layer.name())    

        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Line:
                self.dockwidget.comboBox_4.setEditable(True)
                layer_list5.append(layer.name())  

        self.dockwidget.comboBox_4.addItems(layer_list5)
        self.dockwidget.comboBox_3.addItems(layer_list4)

    #Spatial join for matching ID

    def Frnt_spatialjoin(self):
        indexname1 = self.dockwidget.comboBox_3.currentText()
        layer1 = QgsMapLayerRegistry.instance().mapLayersByName( indexname1 )[0]
        layer1_pr = layer1.dataProvider()
        layer1_IDX  = layer1.fieldNameIndex('ID')
        layer1_caps  = layer1_pr.capabilities()

        indexname2 = self.dockwidget.comboBox_4.currentText()
        layer2 = QgsMapLayerRegistry.instance().mapLayersByName( indexname2 )[0]
        layer2_pr = layer2.dataProvider()
        layer2_IDX  = layer2.fieldNameIndex('ID')
        layer2_caps  = layer2_pr.capabilities()

                  

        layer2.getFeatures()
        layer1.getFeatures()

        for buildfeat in layer1.getFeatures():
            for entfeat in layer2.getFeatures():
                if entfeat.geometry().intersects(buildfeat.geometry()) == True:
                    layer2.startEditing()
                    layer2ID = entfeat.attributes()[layer2_IDX]
                    if layer2_caps & QgsVectorDataProvider.ChangeAttributeValues:
                        entfeat['ID'] = buildfeat['ID']
                        layer2.updateFeature(entfeat)
                        layer2.commitChanges()





    
    ###################################################################################ENTRANCES#############################################################################################
    #Load/Save File selection

    def select_output_file_E(self):
        filename = QFileDialog.getSaveFileName(self.dockwidget, "Select Save Location ","", '*.shp')
        self.dockwidget.lineEdit_E4.setText(filename)

    def select_existing_file_E(self):
        filename = QFileDialog.getOpenFileName(self.dockwidget, "Load Existing File ","", '*.shp')
        self.dockwidget.lineEdit_E7.setText(filename)

    #Create New File

    def createEntrances(self):
        # create layer
        
        vl = QgsVectorLayer("Point", "Entrances1", "memory")
        pr = vl.dataProvider()

        QgsMapLayerRegistry.instance().addMapLayer(vl)  

        input3 = self.iface.activeLayer()
        location = self.dockwidget.lineEdit_E4.text()
        QgsVectorFileWriter.writeAsVectorFormat(input3, location, "System", None, "ESRI Shapefile")

        removelayer1 = QgsMapLayerRegistry.instance().mapLayersByName( "Entrances1" )[0]
        QgsMapLayerRegistry.instance().removeMapLayers( [removelayer1.id()] )

        input4 = self.iface.addVectorLayer(location, "Entrances", "ogr")

        if not input4:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        input4.startEditing()
               

        edit1 = input4.dataProvider()
        edit1.addAttributes( [ QgsField("ID", QVariant.Int),
                QgsField("Category",  QVariant.String),
                QgsField("Sub Category", QVariant.String),
                QgsField("Access Level", QVariant.String) ] )
        input4.commitChanges()
        input4.startEditing()

        plugin_path = os.path.dirname(__file__)
        qml_path = plugin_path + "/entrances.qml"
        input7 = self.iface.activeLayer()
        input7.loadNamedStyle(qml_path)
        self.dockwidget.comboBox_E12.setEditable(True)
        
        
    #Load File    

    def Loadfile_E(self):
        location1 = self.dockwidget.lineEdit_E7.text()
        input5 = self.iface.addVectorLayer(location1, "Entrances", "ogr")

        if not input5:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location1 )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location1 )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        input5.startEditing()

        plugin_path = os.path.dirname(__file__)
        qml_path = plugin_path + "/entrances.qml"
        input7 = self.iface.activeLayer()
        input7.loadNamedStyle(qml_path)

        self.dockwidget.lineEdit_E7.setPlaceholderText('Select Load Location')
        self.dockwidget.comboBox_E12.setEditable(True)


    #Update Selection

    def updateControlled(self):
        layer1 = self.iface.activeLayer()

        features = layer1.selectedFeatures()
        selectedLayerText = self.dockwidget.comboBox_E1.currentText()

        if self.dockwidget.radioButton_E2.isChecked():
            layer1.startEditing()
            for feat in features:

                feat['Category'] = "Controlled"
                feat['Sub Catego'] = "Default"
                feat['Access Lev'] = selectedLayerText
                layer1.updateFeature(feat)
                layer1.commitChanges()

        if self.dockwidget.radioButton_E4.isChecked():
            layer1.startEditing()
            for feat in features:

                feat['Category'] = "Controlled"
                feat['Sub Catego'] = "Service Entrance"
                feat['Access Lev'] = selectedLayerText
                layer1.updateFeature(feat)
                layer1.commitChanges()

        if self.dockwidget.radioButton_E3.isChecked():
            layer1.startEditing()
            for feat in features:

                feat['Category'] = "Controlled"
                feat['Sub Catego'] = "Fire Exit"
                feat['Access Lev'] = selectedLayerText
                layer1.updateFeature(feat)
                layer1.commitChanges()

        if self.dockwidget.radioButton_E1.isChecked():
            layer1.startEditing()
            for feat in features:

                feat['Category'] = "Controlled"
                feat['Sub Catego'] = "Unused"
                feat['Access Lev'] = selectedLayerText
                layer1.updateFeature(feat)
                layer1.commitChanges()
     
        
       
        
        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated : Controlled' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )


    def updateUNcontrolled(self):
        layer1 = self.iface.activeLayer()
        layer1.startEditing()

        features = layer1.selectedFeatures()
        selectedLayerText = self.dockwidget.comboBox_E1.currentText()
        

        if self.dockwidget.radioButton_E2.isChecked():
            layer1.startEditing()
            for feat in features:

                feat['Category'] = "Uncontrolled"
                feat['Sub Catego'] = "Default"
                feat['Access Lev'] = selectedLayerText
                layer1.updateFeature(feat)
                layer1.commitChanges()

        if self.dockwidget.radioButton_E4.isChecked():
            layer1.startEditing()
            for feat in features:

                feat['Category'] = "Uncontrolled"
                feat['Sub Catego'] = "Service Entrance"
                feat['Access Lev'] = selectedLayerText
                layer1.updateFeature(feat)
                layer1.commitChanges()

        if self.dockwidget.radioButton_E3.isChecked():
            layer1.startEditing()
            for feat in features:

                feat['Category'] = "Uncontrolled"
                feat['Sub Catego'] = "Fire Exit"
                feat['Access Lev'] = selectedLayerText
                layer1.updateFeature(feat)
                layer1.commitChanges()

        if self.dockwidget.radioButton_E1.isChecked():
            layer1.startEditing()
            for feat in features:

                feat['Category'] = "Uncontrolled"
                feat['Sub Catego'] = "Unused"
                feat['Access Lev'] = selectedLayerText
                layer1.updateFeature(feat)
                layer1.commitChanges()

        features2 = layer1.getFeatures()
        for feat2 in features2:
            feat2['ID'] = int(feat2.id())
            layer1.updateFeature(feat2)
            layer1.commitChanges()


        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated : Uncontrolled' )
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 )   

    #Load Draw Tools         
    
    def GroundControlledDefault(self):
        self.GroundControlledDefaulttool = GroundControlledDefault( self.canvas )
        self.canvas.setMapTool(self.GroundControlledDefaulttool)

    def GroundControlledService(self):
        self.GroundControlledServicetool = GroundControlledService( self.canvas )
        self.canvas.setMapTool(self.GroundControlledServicetool)

    def GroundControlledFire(self):
        self.GroundControlledFiretool = GroundControlledFire( self.canvas )
        self.canvas.setMapTool(self.GroundControlledFiretool)

    def GroundControlledUnused(self):
        self.GroundControlledUnusedtool = GroundControlledUnused( self.canvas )
        self.canvas.setMapTool(self.GroundControlledUnusedtool)

    def UpperControlledDefault(self):
        self.UpperControlledDefaulttool = UpperControlledDefault( self.canvas )
        self.canvas.setMapTool(self.UpperControlledDefaulttool)

    def UpperControlledService(self):
        self.UpperControlledServicetool = UpperControlledService( self.canvas )
        self.canvas.setMapTool(self.UpperControlledServicetool)

    def UpperControlledFire(self):
        self.UpperControlledFiretool = UpperControlledFire( self.canvas )
        self.canvas.setMapTool(self.UpperControlledFiretool)

    def UpperControlledUnused(self):
        self.UpperControlledUnusedtool = UpperControlledUnused( self.canvas )
        self.canvas.setMapTool(self.UpperControlledUnusedtool)

    def LowerControlledDefault(self):
        self.LowerControlledDefaulttool = LowerControlledDefault( self.canvas )
        self.canvas.setMapTool(self.LowerControlledDefaulttool)

    def LowerControlledService(self):
        self.LowerControlledServicetool = LowerControlledService( self.canvas )
        self.canvas.setMapTool(self.LowerControlledServicetool)

    def LowerControlledFire(self):
        self.LowerControlledFiretool = LowerControlledFire( self.canvas )
        self.canvas.setMapTool(self.LowerControlledFiretool)

    def LowerControlledUnused(self):
        self.LowerControlledUnusedtool = LowerControlledUnused( self.canvas )
        self.canvas.setMapTool(self.LowerControlledUnusedtool)

    def GroundUNControlledDefault(self):
        self.GroundUNControlledDefaulttool = GroundUNControlledDefault( self.canvas )
        self.canvas.setMapTool(self.GroundUNControlledDefaulttool)

    def UpperUNControlledDefault(self):
        self.UpperUNControlledDefaulttool = UpperUNControlledDefault( self.canvas )
        self.canvas.setMapTool(self.UpperUNControlledDefaulttool)

    def LowerUNControlledDefault(self):
        self.LowerUNControlledDefaulttool = LowerUNControlledDefault( self.canvas )
        self.canvas.setMapTool(self.LowerUNControlledDefaulttool)


    #Load Custom Thematic

    def Ent_CustomThematic(self):
        if self.dockwidget.comboBox_E12.currentText() == "SSL Standard - General":
            mc = self.canvas
            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/entrances.qml"
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(qml_path)
            mc.refresh()
            

        if self.dockwidget.comboBox_E12.currentText() == "SSL Standard - Detailed":
            mc = self.canvas
            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/entrances_detailed.qml"
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(qml_path)
            mc.refresh()

        else:
            mc = self.canvas
            plugin_path = self.dockwidget.lineEdit_E8.text()
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(plugin_path)
            mc.refresh()


    #Add new thematic styles to Combobox           
            

    def Ent_select_input_qml2(self):
        filenameLU = QFileDialog.getOpenFileName(self.dockwidget, "Select Input File","", '*.qml')
        self.dockwidget.comboBox_E12.addItem(filenameLU)
        self.dockwidget.lineEdit_E8.setText(filenameLU)
        self.dockwidget.comboBox_E12.setItemText(2,"Custom Thematic")
        self.dockwidget.comboBox_E12.setItemText(3,"Custom Thematic 1")
        self.dockwidget.comboBox_E12.setItemText(4,"Custom Thematic 2")
        self.dockwidget.comboBox_E12.setItemText(5,"Custom Thematic 3") 
        self.dockwidget.comboBox_E12.setItemText(6,"Custom Thematic 4")
       

    #Update combobox with correct file type
    def Ent_updatelist(self):
        layers = self.iface.legendInterface().layers()
        self.dockwidget.comboBox.clear()
        self.dockwidget.comboBox_2.clear()
        layer_list2 = []
        layer_list3 = []

        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Polygon:
                 self.dockwidget.comboBox.setEditable(True)
                 layer_list2.append(layer.name())    

        for layer in layers:
            if layer.type() == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point:
                self.dockwidget.comboBox_2.setEditable(True)
                layer_list3.append(layer.name())  

        self.dockwidget.comboBox_2.addItems(layer_list3)
        self.dockwidget.comboBox.addItems(layer_list2)

    #Spatial Join to update ID
    def Ent_spatialjoin(self):
        indexname1 = self.dockwidget.comboBox.currentText()
        layer1 = QgsMapLayerRegistry.instance().mapLayersByName( indexname1 )[0]
        layer1_pr = layer1.dataProvider()
        layer1_IDX  = layer1.fieldNameIndex('ID')
        layer1_caps  = layer1_pr.capabilities()

        indexname2 = self.dockwidget.comboBox_2.currentText()
        layer2 = QgsMapLayerRegistry.instance().mapLayersByName( indexname2 )[0]
        layer2_pr = layer2.dataProvider()
        layer2_IDX  = layer2.fieldNameIndex('ID')
        layer2_caps  = layer2_pr.capabilities()

                  

        layer2.getFeatures()
        layer1.getFeatures()

        for buildfeat in layer1.getFeatures():
            for entfeat in layer2.getFeatures():
                if entfeat.geometry().intersects(buildfeat.geometry()) == True:
                    layer2.startEditing()
                    layer2ID = entfeat.attributes()[layer2_IDX]
                    if layer2_caps & QgsVectorDataProvider.ChangeAttributeValues:
                        entfeat['ID'] = buildfeat['ID']
                        layer2.updateFeature(entfeat)
                        layer2.commitChanges()

                   
                                                  
###################################################################################LAND USE#############################################################################################
    #Save/Load File Select
    def select_output_file_LU(self):
        filename = QFileDialog.getSaveFileName(self.dockwidget, "Select Save Location ","", '*.shp')
        self.dockwidget.lineEdit_6.setText(filename)

    def select_input_file_LU(self):
        filename = QFileDialog.getOpenFileName(self.dockwidget, "Select Input File ","", '*.shp')
        self.dockwidget.lineEdit_4.setText(filename)

    def select_existing_file_LU(self):
        filename = QFileDialog.getOpenFileName(self.dockwidget, "Load Existing File ","", '*.shp')
        self.dockwidget.lineEdit_7.setText(filename)

    def Loadfile_LU(self):
        location1 = self.dockwidget.lineEdit_7.text()
        input5 = self.iface.addVectorLayer(location1, "Land Use", "ogr")

        if not input5:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location1 )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location1 )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        input5.startEditing()
        
        plugin_path = os.path.dirname(__file__)
        qml_path = plugin_path + "/landuses.qml"
        input7 = self.iface.activeLayer()
        input7.loadNamedStyle(qml_path)

        self.dockwidget.lineEdit_3.setPlaceholderText('Select Load Location')

        attrlist=[]
        layer = self.iface.activeLayer()
        fields = layer.pendingFields()
        for field in fields:
            attrlist.append(field.name())

        print attrlist

        s = set(attrlist)
            
        
        self.dockwidget.lineEdit_2.setPlaceholderText('Select Load Location')

        if 'GF_SubCate' in s:
            self.dockwidget.checkBox.setCheckable(True)
            self.dockwidget.checkBox.setChecked(2)
            self.dockwidget.lineEdit_8.setEnabled(True)
            self.dockwidget.lineEdit_9.setEnabled(True)
            self.dockwidget.lineEdit_10.setEnabled(True)
            self.dockwidget.comboBox_11.setEditable(True)

        if 'FF_SubCate' in s:
            self.dockwidget.checkBox.setCheckable(True)
            self.dockwidget.checkBox.setChecked(2)
            self.dockwidget.checkBox_2.setCheckable(True)
            self.dockwidget.checkBox_2.setChecked(2)
            self.dockwidget.lineEdit_8.setEnabled(True)
            self.dockwidget.lineEdit_9.setEnabled(True)
            self.dockwidget.lineEdit_10.setEnabled(True)
            self.dockwidget.comboBox_11.setEditable(True)

        if 'UF_SubCate' in s:
            self.dockwidget.checkBox.setCheckable(True)
            self.dockwidget.checkBox.setChecked(2)
            self.dockwidget.checkBox_2.setCheckable(True)
            self.dockwidget.checkBox_2.setChecked(2)
            self.dockwidget.checkBox_3.setCheckable(True)
            self.dockwidget.checkBox_3.setChecked(2)
            self.dockwidget.lineEdit_8.setEnabled(True)
            self.dockwidget.lineEdit_9.setEnabled(True)
            self.dockwidget.lineEdit_10.setEnabled(True)
            self.dockwidget.comboBox_11.setEditable(True)    

        self.dockwidget.lineEdit_7.clear()
        self.dockwidget.lineEdit_7.setPlaceholderText('Select Load Location...') 

    #Create New File  

    def LUNewFile(self):
               
        location1 = self.dockwidget.lineEdit_4.text()
        input5 = self.iface.addVectorLayer(location1, "ToRemove", "ogr")

        if not input5:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location1 )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location1 )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )


        input1 = self.iface.activeLayer()
        location = self.dockwidget.lineEdit_6.text()
        QgsVectorFileWriter.writeAsVectorFormat(input1, location, "System", None, "ESRI Shapefile")

        removelayer = QgsMapLayerRegistry.instance().mapLayersByName( "ToRemove" )[0]
        QgsMapLayerRegistry.instance().removeMapLayers( [removelayer.id()] )
        
        input4 = self.iface.addVectorLayer(location, "Land Use", "ogr")

        if not input4:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        input4.startEditing()

        if self.dockwidget.checkBox_4.checkState() == 0 and self.dockwidget.checkBox_5.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Floors", QVariant.Int), QgsField("Height", QVariant.Int),
              QgsField("GF_Category", QVariant.String), QgsField("GF_SubCategory",  QVariant.String),
              QgsField("GF_SSx_Code", QVariant.String), QgsField("GF_NLUD_Code", QVariant.String), QgsField("GF_TCPA_Code",
              QVariant.String), QgsField("GF_Description", QVariant.String), QgsField("Area", QVariant.Double)] )
            
            input4.commitChanges()
            input4.startEditing()
            self.dockwidget.checkBox.setCheckable(True)
            self.dockwidget.checkBox.setChecked(2)
            self.dockwidget.lineEdit_8.setEnabled(True)
            self.dockwidget.lineEdit_9.setEnabled(True)
            self.dockwidget.lineEdit_10.setEnabled(True)
            self.dockwidget.comboBox_11.setEditable(True)
            
                       

        elif self.dockwidget.checkBox_4.checkState() == 2 and self.dockwidget.checkBox_5.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Floors", QVariant.Int), QgsField("Height", QVariant.Int),  
                QgsField("GF_Category", QVariant.String), QgsField("GF_SubCategory",  QVariant.String), 
                QgsField("GF_SSx_Code", QVariant.String), QgsField("GF_NLUD_Code", QVariant.String), 
                QgsField("GF_TCPA_Code", QVariant.String), QgsField("GF_Description", QVariant.String),
                QgsField("FF_Category", QVariant.String), QgsField("FF_SubCategory",  QVariant.String), 
                QgsField("FF_SSx_Code", QVariant.String), QgsField("FF_NLUD_Code", QVariant.String), 
                QgsField("FF_TCPA_Code", QVariant.String), QgsField("FF_Description", QVariant.String), 
                QgsField("Area", QVariant.Double)] )

            input4.commitChanges()
            input4.startEditing()
            self.dockwidget.checkBox.setCheckable(True)
            self.dockwidget.checkBox.setChecked(2)
            self.dockwidget.checkBox_2.setCheckable(True)
            self.dockwidget.checkBox_2.setChecked(2)
            self.dockwidget.lineEdit_8.setEnabled(True)
            self.dockwidget.lineEdit_9.setEnabled(True)
            self.dockwidget.lineEdit_10.setEnabled(True)
            self.dockwidget.comboBox_11.setEditable(True)

        elif self.dockwidget.checkBox_4.checkState() == 2 and self.dockwidget.checkBox_5.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Floors", QVariant.Int), QgsField("Height", QVariant.Int),
              QgsField("GF_Category", QVariant.String), QgsField("GF_SubCategory",  QVariant.String), 
              QgsField("GF_SSx_Code", QVariant.String), QgsField("GF_NLUD_Code", QVariant.String), 
              QgsField("GF_TCPA_Code", QVariant.String), QgsField("GF_Description", QVariant.String),
              QgsField("FF_Category", QVariant.String), QgsField("FF_SubCategory",  QVariant.String), 
              QgsField("FF_SSx_Code", QVariant.String), QgsField("FF_NLUD_Code", QVariant.String), 
              QgsField("FF_TCPA_Code", QVariant.String), QgsField("FF_Description", QVariant.String), 
              QgsField("UF_Category", QVariant.String), QgsField("UF_SubCategory",  QVariant.String), 
              QgsField("UF_SSx_Code", QVariant.String), QgsField("UF_NLUD_Code", QVariant.String), 
              QgsField("UF_TCPA_Code", QVariant.String), QgsField("UF_Description", QVariant.String), 
              QgsField("Area", QVariant.Double)] )

            input4.commitChanges()
            input4.startEditing()
            self.dockwidget.checkBox.setCheckable(True)
            self.dockwidget.checkBox.setChecked(2)
            self.dockwidget.checkBox_2.setCheckable(True)
            self.dockwidget.checkBox_2.setChecked(2)
            self.dockwidget.checkBox_3.setCheckable(True)
            self.dockwidget.checkBox_3.setChecked(2)
            self.dockwidget.lineEdit_8.setEnabled(True)
            self.dockwidget.lineEdit_9.setEnabled(True)
            self.dockwidget.lineEdit_10.setEnabled(True)

               

        plugin_path = os.path.dirname(__file__)
        qml_path = plugin_path + "/landuses.qml"
        input7 = self.iface.activeLayer()
        input7.loadNamedStyle(qml_path)

        self.dockwidget.lineEdit_4.clear()
        self.dockwidget.lineEdit_6.clear()
        self.dockwidget.lineEdit_4.setPlaceholderText('Select Save Location...')
        self.dockwidget.lineEdit_6.setPlaceholderText('Select Input File...')

    #Selection Update
    def LuGFUpdate(self):
        layer = self.iface.activeLayer()       
            
        features = layer.selectedFeatures()

        LUCategory = self.dockwidget.comboBox_5.currentText()
        LUSubCat = self.dockwidget.comboBox_8.currentText()
        LUFloors = self.dockwidget.lineEdit_8.text()
        LUHeight = self.dockwidget.lineEdit_9.text()
        LUDescrip = self.dockwidget.lineEdit_10.text()

        layer.startEditing()

        #Ground Floor
        
        if self.dockwidget.checkBox.checkState() == 2:
            if self.dockwidget.comboBox_5.currentText() == "Agriculture":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "AG"
                    feat['GF_NLUD_Co'] = "U010"
                    feat['GF_TCPA_Co'] = "B2"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Community":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "C"
                    feat['GF_NLUD_Co'] = "U082"
                    feat['GF_TCPA_Co'] = "D1"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Catering" and self.dockwidget.comboBox_8.currentText() == "Restaurant and Cafes":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "CA"
                    feat['GF_NLUD_Co'] = "U093"
                    feat['GF_TCPA_Co'] = "A3"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()#

            if self.dockwidget.comboBox_5.currentText() == "Catering" and self.dockwidget.comboBox_8.currentText() == "Drinking Establishments":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "CA"
                    feat['GF_NLUD_Co'] = "U094"
                    feat['GF_TCPA_Co'] = "A4"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Catering" and self.dockwidget.comboBox_8.currentText() == "Hot Food Takeaways":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "CA"
                    feat['GF_NLUD_Co'] = "-"
                    feat['GF_TCPA_Co'] = "A5"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Education":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "ED"
                    feat['GF_NLUD_Co'] = "U083"
                    feat['GF_TCPA_Co'] = "D1"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Government":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "GOV"
                    feat['GF_NLUD_Co'] = "U120"
                    feat['GF_TCPA_Co'] = "-"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Hotels":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "H"
                    feat['GF_NLUD_Co'] = "U072"
                    feat['GF_TCPA_Co'] = "C1"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Industry":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "I"
                    feat['GF_NLUD_Co'] = "U101"
                    feat['GF_TCPA_Co'] = "B2"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Leisure" and self.dockwidget.comboBox_8.currentText() == "Art and Culture":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "LE"
                    feat['GF_NLUD_Co'] = "U040"
                    feat['GF_TCPA_Co'] = "D1"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_5.currentText() == "Leisure" and self.dockwidget.comboBox_8.currentText() == "Amusement or Sports":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "LE"
                    feat['GF_NLUD_Co'] = "-"
                    feat['GF_TCPA_Co'] = "D2"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()   

            if self.dockwidget.comboBox_5.currentText() == "Medical" and self.dockwidget.comboBox_8.currentText() == "Hospitals" :
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "M"
                    feat['GF_NLUD_Co'] = "U081"
                    feat['GF_TCPA_Co'] = "C2"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Medical" and self.dockwidget.comboBox_8.currentText() == "Health centres" :
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "M"
                    feat['GF_NLUD_Co'] = "-"
                    feat['GF_TCPA_Co'] = "D1"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Offices":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "O"
                    feat['GF_NLUD_Co'] = "U102"
                    feat['GF_TCPA_Co'] = "B1"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_5.currentText() == "Parking" and self.dockwidget.comboBox_8.currentText() == "Car Parks":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "P"
                    feat['GF_NLUD_Co'] = "U053"
                    feat['GF_TCPA_Co'] = "-"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Parking" and self.dockwidget.comboBox_8.currentText() == "Other Vehicles":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "P"
                    feat['GF_NLUD_Co'] = "U054"
                    feat['GF_TCPA_Co'] = "-"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Retail":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "R"
                    feat['GF_NLUD_Co'] = "U091"
                    feat['GF_TCPA_Co'] = "A1"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_5.currentText() == "Residential" and self.dockwidget.comboBox_8.currentText() == "Institutions":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "RE"
                    feat['GF_NLUD_Co'] = "U071"
                    feat['GF_TCPA_Co'] = "C2"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_5.currentText() == "Residential" and self.dockwidget.comboBox_8.currentText() == "Dwellings":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "RE"
                    feat['GF_NLUD_Co'] = "U073"
                    feat['GF_TCPA_Co'] = "C2"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()     

            if self.dockwidget.comboBox_5.currentText() == "Services" and self.dockwidget.comboBox_8.currentText() == "Commercial":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "S"
                    feat['GF_NLUD_Co'] = "U092"
                    feat['GF_TCPA_Co'] = "A1"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()  


            if self.dockwidget.comboBox_5.currentText() == "Services" and self.dockwidget.comboBox_8.currentText() == "Financial":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "S"
                    feat['GF_NLUD_Co'] = "-"
                    feat['GF_TCPA_Co'] = "A2"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_5.currentText() == "Storage":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "ST"
                    feat['GF_NLUD_Co'] = "U103"
                    feat['GF_TCPA_Co'] = "B8"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Transport" and self.dockwidget.comboBox_8.currentText() == "Transport Terminals":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "TR"
                    feat['GF_NLUD_Co'] = "U052"
                    feat['GF_TCPA_Co'] = ""
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Transport" and self.dockwidget.comboBox_8.currentText() == "Goods Terminals":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "TR"
                    feat['GF_NLUD_Co'] = "U055"
                    feat['GF_TCPA_Co'] = ""
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Utilities":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "U"
                    feat['GF_NLUD_Co'] = "U060"
                    feat['GF_TCPA_Co'] = "-"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Under Construction":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "UC"
                    feat['GF_NLUD_Co'] = "-"
                    feat['GF_TCPA_Co'] = "-"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Under Developed":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "UD"
                    feat['GF_NLUD_Co'] = "U130"
                    feat['GF_TCPA_Co'] = "-"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Unknown/Undefined":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "UN"
                    feat['GF_NLUD_Co'] = "-"
                    feat['GF_TCPA_Co'] = "-"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_5.currentText() == "Vacant Building":
                for feat in features:
                    layer.startEditing()
                    feat['GF_Categor'] = LUCategory
                    feat['GF_SubCate'] = LUSubCat
                    feat['Height'] = LUHeight
                    feat['Floors'] = LUFloors
                    feat['GF_SSx_Cod'] = "V"
                    feat['GF_NLUD_Co'] = "U110"
                    feat['GF_TCPA_Co'] = "-"
                    feat['GF_Descrip'] = LUDescrip
                    layer.updateFeature(feat)
                    layer.commitChanges()

        self.dockwidget.lineEdit_8.clear()
        self.dockwidget.lineEdit_9.clear()
        self.dockwidget.lineEdit_10.clear()



        #First Floor

        LUFCategory = self.dockwidget.comboBox_6.currentText()
        LUFSubCat = self.dockwidget.comboBox_9.currentText()

        if self.dockwidget.checkBox_2.checkState() == 2:
            if self.dockwidget.comboBox_6.currentText() == "Agriculture":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] =  LUFSubCat
                    feat['FF_SSx_Cod'] = "AG"
                    feat['FF_NLUD_Co'] = "U010"
                    feat['FF_TCPA_Co'] = "B2"


                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Community":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    feat['FF_SSx_Cod'] = "C"
                    feat['FF_NLUD_Co'] = "U082"
                    feat['FF_TCPA_Co'] = "D1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Catering" and self.dockwidget.comboBox_9.currentText() == "Restaurant and Cafes":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    feat['FF_SSx_Cod'] = "CA"
                    feat['FF_NLUD_Co'] = "U093"
                    feat['FF_TCPA_Co'] = "A3"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()#

            if self.dockwidget.comboBox_6.currentText() == "Catering" and self.dockwidget.comboBox_9.currentText() == "Drinking Establishments":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    feat['FF_SSx_Cod'] = "CA"
                    feat['FF_NLUD_Co'] = "U094"
                    feat['FF_TCPA_Co'] = "A4"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Catering" and self.dockwidget.comboBox_9.currentText() == "Hot Food Takeaways":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "CA"
                    feat['FF_NLUD_Co'] = "-"
                    feat['FF_TCPA_Co'] = "A5"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Education":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                   
                    feat['FF_SSx_Cod'] = "ED"
                    feat['FF_NLUD_Co'] = "U083"
                    feat['FF_TCPA_Co'] = "D1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Government":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "GOV"
                    feat['FF_NLUD_Co'] = "U120"
                    feat['FF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Hotels":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    feat['FF_SSx_Cod'] = "H"
                    feat['FF_NLUD_Co'] = "U072"
                    feat['FF_TCPA_Co'] = "C1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Industry":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "I"
                    feat['FF_NLUD_Co'] = "U101"
                    feat['FF_TCPA_Co'] = "B2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Leisure" and self.dockwidget.comboBox_9.currentText() == "Art and Culture":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "LE"
                    feat['FF_NLUD_Co'] = "U040"
                    feat['FF_TCPA_Co'] = "D1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_6.currentText() == "Leisure" and self.dockwidget.comboBox_9.currentText() == "Amusement or Sports":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "LE"
                    feat['FF_NLUD_Co'] = "-"
                    feat['FF_TCPA_Co'] = "D2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()   

            if self.dockwidget.comboBox_6.currentText() == "Medical" and self.dockwidget.comboBox_9.currentText() == "Hospitals" :
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "M"
                    feat['FF_NLUD_Co'] = "U081"
                    feat['FF_TCPA_Co'] = "C2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Medical" and self.dockwidget.comboBox_9.currentText() == "Health centres" :
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "M"
                    feat['FF_NLUD_Co'] = "-"
                    feat['FF_TCPA_Co'] = "D1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Offices":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "O"
                    feat['FF_NLUD_Co'] = "U102"
                    feat['FF_TCPA_Co'] = "B1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_6.currentText() == "Parking" and self.dockwidget.comboBox_9.currentText() == "Car Parks":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "P"
                    feat['FF_NLUD_Co'] = "U053"
                    feat['FF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Parking" and self.dockwidget.comboBox_9.currentText() == "Other Vehicles":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "P"
                    feat['FF_NLUD_Co'] = "U054"
                    feat['FF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Retail":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "R"
                    feat['FF_NLUD_Co'] = "U091"
                    feat['FF_TCPA_Co'] = "A1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_6.currentText() == "Residential" and self.dockwidget.comboBox_9.currentText() == "Institutions":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    feat['FF_SSx_Cod'] = "RE"
                    feat['FF_NLUD_Co'] = "U071"
                    feat['FF_TCPA_Co'] = "C2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_6.currentText() == "Residential" and self.dockwidget.comboBox_9.currentText() == "Dwellings":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "RE"
                    feat['FF_NLUD_Co'] = "U073"
                    feat['FF_TCPA_Co'] = "C2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()     

            if self.dockwidget.comboBox_6.currentText() == "Services" and self.dockwidget.comboBox_9.currentText() == "Commercial":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "S"
                    feat['FF_NLUD_Co'] = "U092"
                    feat['FF_TCPA_Co'] = "A1"
                   
                    layer.updateFeature(feat)
                    layer.commitChanges()  


            if self.dockwidget.comboBox_6.currentText() == "Services" and self.dockwidget.comboBox_9.currentText() == "Financial":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "S"
                    feat['FF_NLUD_Co'] = "-"
                    feat['FF_TCPA_Co'] = "A2"
                   
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_6.currentText() == "Storage":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "ST"
                    feat['FF_NLUD_Co'] = "U103"
                    feat['FF_TCPA_Co'] = "B8"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Transport" and self.dockwidget.comboBox_9.currentText() == "Transport Terminals":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] =LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "TR"
                    feat['FF_NLUD_Co'] = "U052"
                    feat['FF_TCPA_Co'] = ""
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Transport" and self.dockwidget.comboBox_9.currentText() == "Goods Terminals":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "TR"
                    feat['FF_NLUD_Co'] = "U055"
                    feat['FF_TCPA_Co'] = ""
                   
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Utilities":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "U"
                    feat['FF_NLUD_Co'] = "U060"
                    feat['FF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Under Construction":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "UC"
                    feat['FF_NLUD_Co'] = "-"
                    feat['FF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Under Developed":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "UD"
                    feat['FF_NLUD_Co'] = "U130"
                    feat['FF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Unknown/Undefined":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                    
                    feat['FF_SSx_Cod'] = "UN"
                    feat['FF_NLUD_Co'] = "-"
                    feat['FF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_6.currentText() == "Vacant Building":
                for feat in features:
                    layer.startEditing()
                    feat['FF_Categor'] = LUFCategory
                    feat['FF_SubCate'] = LUFSubCat
                   
                    feat['FF_SSx_Cod'] = "V"
                    feat['FF_NLUD_Co'] = "U110"
                    feat['FF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()


        #Upper Floor

        LUFCategory2 = self.dockwidget.comboBox_7.currentText()
        LUFSubCat2 = self.dockwidget.comboBox_10.currentText()

        if self.dockwidget.checkBox_3.checkState() == 2:
            if self.dockwidget.comboBox_7.currentText() == "Agriculture":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] =  LUFSubCat2
                    feat['UF_SSx_Cod'] = "AG"
                    feat['UF_NLUD_Co'] = "U010"
                    feat['UF_TCPA_Co'] = "B2"


                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Community":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    feat['UF_SSx_Cod'] = "C"
                    feat['UF_NLUD_Co'] = "U082"
                    feat['UF_TCPA_Co'] = "D1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Catering" and self.dockwidget.comboBox_10.currentText() == "Restaurant and Cafes":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    feat['UF_SSx_Cod'] = "CA"
                    feat['UF_NLUD_Co'] = "U093"
                    feat['UF_TCPA_Co'] = "A3"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()#

            if self.dockwidget.comboBox_7.currentText() == "Catering" and self.dockwidget.comboBox_10.currentText() == "Drinking Establishments":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    feat['UF_SSx_Cod'] = "CA"
                    feat['UF_NLUD_Co'] = "U094"
                    feat['UF_TCPA_Co'] = "A4"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Catering" and self.dockwidget.comboBox_10.currentText() == "Hot Food Takeaways":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "CA"
                    feat['UF_NLUD_Co'] = "-"
                    feat['UF_TCPA_Co'] = "A5"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Education":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                   
                    feat['UF_SSx_Cod'] = "ED"
                    feat['UF_NLUD_Co'] = "U083"
                    feat['UF_TCPA_Co'] = "D1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Government":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "GOV"
                    feat['UF_NLUD_Co'] = "U120"
                    feat['UF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Hotels":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    feat['UF_SSx_Cod'] = "H"
                    feat['UF_NLUD_Co'] = "U072"
                    feat['UF_TCPA_Co'] = "C1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Industry":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "I"
                    feat['UF_NLUD_Co'] = "U101"
                    feat['UF_TCPA_Co'] = "B2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Leisure" and self.dockwidget.comboBox_10.currentText() == "Art and Culture":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "LE"
                    feat['UF_NLUD_Co'] = "U040"
                    feat['UF_TCPA_Co'] = "D1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_7.currentText() == "Leisure" and self.dockwidget.comboBox_10.currentText() == "Amusement or Sports":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "LE"
                    feat['UF_NLUD_Co'] = "-"
                    feat['UF_TCPA_Co'] = "D2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()   

            if self.dockwidget.comboBox_7.currentText() == "Medical" and self.dockwidget.comboBox_10.currentText() == "Hospitals" :
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "M"
                    feat['UF_NLUD_Co'] = "U081"
                    feat['UF_TCPA_Co'] = "C2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Medical" and self.dockwidget.comboBox_10.currentText() == "Health centres" :
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "M"
                    feat['UF_NLUD_Co'] = "-"
                    feat['UF_TCPA_Co'] = "D1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Offices":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "O"
                    feat['UF_NLUD_Co'] = "U102"
                    feat['UF_TCPA_Co'] = "B1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_7.currentText() == "Parking"and self.dockwidget.comboBox_10.currentText() == "Car Parks":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "P"
                    feat['UF_NLUD_Co'] = "U053"
                    feat['UF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Parking"and self.dockwidget.comboBox_10.currentText() == "Other Vehicles":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "P"
                    feat['UF_NLUD_Co'] = "U054"
                    feat['UF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Retail":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "R"
                    feat['UF_NLUD_Co'] = "U091"
                    feat['UF_TCPA_Co'] = "A1"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_7.currentText() == "Residential" and self.dockwidget.comboBox_10.currentText() == "Institutions":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    feat['UF_SSx_Cod'] = "RE"
                    feat['UF_NLUD_Co'] = "U071"
                    feat['UF_TCPA_Co'] = "C2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_7.currentText() == "Residential" and self.dockwidget.comboBox_10.currentText() == "Dwellings":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "RE"
                    feat['UF_NLUD_Co'] = "U073"
                    feat['UF_TCPA_Co'] = "C2"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()     

            if self.dockwidget.comboBox_7.currentText() == "Services" and self.dockwidget.comboBox_10.currentText() == "Commercial":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "S"
                    feat['UF_NLUD_Co'] = "U092"
                    feat['UF_TCPA_Co'] = "A1"
                   
                    layer.updateFeature(feat)
                    layer.commitChanges()  


            if self.dockwidget.comboBox_7.currentText() == "Services" and self.dockwidget.comboBox_10.currentText() == "Financial":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "S"
                    feat['UF_NLUD_Co'] = "-"
                    feat['UF_TCPA_Co'] = "A2"
                   
                    layer.updateFeature(feat)
                    layer.commitChanges()  

            if self.dockwidget.comboBox_7.currentText() == "Storage":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "ST"
                    feat['UF_NLUD_Co'] = "U103"
                    feat['UF_TCPA_Co'] = "B8"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Transport" and self.dockwidget.comboBox_10.currentText() == "Transport Terminals":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] =LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "TR"
                    feat['UF_NLUD_Co'] = "U052"
                    feat['UF_TCPA_Co'] = ""
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Transport" and self.dockwidget.comboBox_10.currentText() == "Goods Terminals":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "TR"
                    feat['UF_NLUD_Co'] = "U055"
                    feat['UF_TCPA_Co'] = ""
                   
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Utilities":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "U"
                    feat['UF_NLUD_Co'] = "U060"
                    feat['UF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Under Construction":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "UC"
                    feat['UF_NLUD_Co'] = "-"
                    feat['UF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Under Developed":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "UD"
                    feat['UF_NLUD_Co'] = "U130"
                    feat['UF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Unknown/Undefined":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                    
                    feat['UF_SSx_Cod'] = "UN"
                    feat['UF_NLUD_Co'] = "-"
                    feat['UF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

            if self.dockwidget.comboBox_7.currentText() == "Vacant Building":
                for feat in features:
                    layer.startEditing()
                    feat['UF_Categor'] = LUFCategory2
                    feat['UF_SubCate'] = LUFSubCat2
                   
                    feat['UF_SSx_Cod'] = "V"
                    feat['UF_NLUD_Co'] = "U110"
                    feat['UF_TCPA_Co'] = "-"
                    
                    layer.updateFeature(feat)
                    layer.commitChanges()

        LU_list = ["","Agriculture","Community","Catering","Education","Government","Hotels","Industry","Leisure","Medical","Offices","Parking","Retail","Residential","Services","Storage","Transport","Utilities", "Under Construction", "Under Developed", "Unknown/Undefined","Vacant Building"] 
            
            
        self.dockwidget.comboBox_5.clear()
        self.dockwidget.comboBox_6.clear()
        self.dockwidget.comboBox_7.clear()
        self.dockwidget.comboBox_8.clear()
        self.dockwidget.comboBox_9.clear()
        self.dockwidget.comboBox_10.clear()
        self.dockwidget.comboBox_5.addItems(LU_list)
        self.dockwidget.comboBox_6.addItems(LU_list)
        self.dockwidget.comboBox_7.addItems(LU_list)

        

        msgBar = self.iface.messageBar()
        msg = msgBar.createMessage( u'Selection Updated')
        msgBar.pushWidget( msg, QgsMessageBar.INFO, 5 ) 

    #Add custom Thematic styles to combobox


    def select_inputThematic_file_LU(self):
            filenameLU = QFileDialog.getOpenFileName(self.dockwidget, "Select Input File","", '*.qml')
            self.dockwidget.comboBox_11.addItem(filenameLU)
            self.dockwidget.lineEdit_11.setText(filenameLU)
            self.dockwidget.comboBox_11.setItemText(3,"Custom Thematic")
            self.dockwidget.comboBox_11.setItemText(4,"Custom Thematic 1")
            self.dockwidget.comboBox_11.setItemText(5,"Custom Thematic 2")
            self.dockwidget.comboBox_11.setItemText(6,"Custom Thematic 3") 
            self.dockwidget.comboBox_11.setItemText(7,"Custom Thematic 4")  

            
    #Load Thematic Style

    def LUThematics(self):
        if self.dockwidget.comboBox_11.currentText() == "SSL Code":
            mc = self.canvas
            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/landuses.qml"
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(qml_path)
            mc.refresh()
            

        if self.dockwidget.comboBox_11.currentText() == "TCPA Code":
            mc = self.canvas
            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/landuses_TCPA.qml"
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(qml_path)
            mc.refresh()

        if self.dockwidget.comboBox_11.currentText() == "NLUD Code":
            mc = self.canvas
            plugin_path = os.path.dirname(__file__)
            qml_path = plugin_path + "/landuses_NLUD.qml"
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(qml_path)
            mc.refresh()

        else:
            mc = self.canvas
            plugin_path = self.dockwidget.lineEdit_11.text()
            input7 = self.iface.activeLayer()
            input7.loadNamedStyle(plugin_path)
            mc.refresh()              

    #Update land Use Category combobox - GF
    def GFChecked(self):

        if self.dockwidget.checkBox.checkState() == 2:
            self.dockwidget.comboBox_5.clear()
            print True
            LU_list = ["","Agriculture","Community","Catering","Education","Government","Hotels","Industry","Leisure","Medical","Offices","Parking","Retail","Residential","Services","Storage","Transport","Utilities", "Under Construction", "Under Developed", "Unknown/Undefined","Vacant Building"] 
            self.dockwidget.pushButton_L3.setEnabled(True)
            self.dockwidget.comboBox_5.setEditable(True)
            self.dockwidget.comboBox_5.addItems(LU_list)
            self.dockwidget.lineEdit_8.setEnabled(True)
            self.dockwidget.lineEdit_9.setEnabled(True)
            self.dockwidget.lineEdit_10.setEnabled(True)

        if self.dockwidget.checkBox.checkState() == 0:
            self.dockwidget.comboBox_5.clear()
            self.dockwidget.comboBox_8.clear()
            print False
            LU_list =[]
            self.dockwidget.pushButton_L3.setEnabled(False)
            self.dockwidget.comboBox_5.setEditable(False)
            self.dockwidget.comboBox_8.setEditable(False)
            self.dockwidget.comboBox_5.addItems(LU_list) 
            self.dockwidget.comboBox_8.addItems(LU_list)
            self.dockwidget.lineEdit_8.setEnabled(False)
            self.dockwidget.lineEdit_9.setEnabled(False)
            self.dockwidget.lineEdit_10.setEnabled(False)

    #Update land use subcategory combobox based on land use category combobox - GF
    def GFsubcat(self):

        if self.dockwidget.comboBox_5.currentText() == "":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_5.currentText() == "Agriculture":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_5.currentText() == "Community":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Catering":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(True)
            LU_list_sub1 =["Restaurant and Cafes","Drinking Establishments","Hot Food Takeaways"]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_5.currentText() == "Education":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_5.currentText() == "Government":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Hotels":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_5.currentText() == "Industry":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Offices":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Retail":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Leisure":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(True)
            LU_list_sub2 =["Art and Culture","Amusement or Sports"]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub2) 

        if self.dockwidget.comboBox_5.currentText() == "Medical":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(True)
            LU_list_sub3 =["Hospitals","Health centres"]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub3)

        if self.dockwidget.comboBox_5.currentText() == "Parking":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(True)
            LU_list_sub4 =["Car Parks","Other Vehicles"]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub4)

        if self.dockwidget.comboBox_5.currentText() == "Residential":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(True)
            LU_list_sub5 =["Institutions","Dwellings"]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub5)   

        if self.dockwidget.comboBox_5.currentText() == "Services":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(True)
            LU_list_sub6 =["Commercial","Financial"]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub6)

        if self.dockwidget.comboBox_5.currentText() == "Storage":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Transport":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(True)
            LU_list_sub7 =["Transport Terminals","Goods Terminals"]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub7)

        if self.dockwidget.comboBox_5.currentText() == "Utilities":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Under Construction":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Under Developed":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Unknown/Undefined":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_5.currentText() == "Vacant Building":
            self.dockwidget.comboBox_8.clear()
            self.dockwidget.comboBox_8.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_8.addItems(LU_list_sub1)


    #Update land Use Category combobox - FF
    def FFChecked(self):

        if self.dockwidget.checkBox_2.checkState() == 2:
            self.dockwidget.comboBox_6.clear()
            print True
            LU_list = ["","Agriculture","Community","Catering","Education","Government","Hotels","Industry","Leisure","Medical","Offices","Parking","Retail","Residential","Services","Storage","Transport","Utilities", "Under Construction", "Under Developed", "Unknown/Undefined","Vacant Building"] 
            
            self.dockwidget.comboBox_6.setEditable(True)
            self.dockwidget.comboBox_6.addItems(LU_list)

        if self.dockwidget.checkBox_2.checkState() == 0:
            self.dockwidget.comboBox_6.clear()
            self.dockwidget.comboBox_9.clear()
            print False
            LU_list =[]
            
            self.dockwidget.comboBox_6.setEditable(False)
            self.dockwidget.comboBox_9.setEditable(False)
            self.dockwidget.comboBox_6.addItems(LU_list) 
            self.dockwidget.comboBox_9.addItems(LU_list)

    #Update land use subcategory combobox based on land use category combobox - FF
    def FFsubcat(self):

        if self.dockwidget.comboBox_6.currentText() == "":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_6.currentText() == "Agriculture":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_6.currentText() == "Community":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Catering":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(True)
            LU_list_sub1 =["Restaurant and Cafes","Drinking Establishments","Hot Food Takeaways"]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_6.currentText() == "Education":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_6.currentText() == "Government":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Hotels":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_6.currentText() == "Industry":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Offices":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Retail":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Leisure":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(True)
            LU_list_sub2 =["Art and Culture","Amusement or Sports"]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub2) 

        if self.dockwidget.comboBox_6.currentText() == "Medical":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(True)
            LU_list_sub3 =["Hospitals","Health centres"]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub3)

        if self.dockwidget.comboBox_6.currentText() == "Parking":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(True)
            LU_list_sub4 =["Car Parks","Other Vehicles"]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub4)

        if self.dockwidget.comboBox_6.currentText() == "Residential":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(True)
            LU_list_sub5 =["Institutions","Dwellings"]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub5)   

        if self.dockwidget.comboBox_6.currentText() == "Services":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(True)
            LU_list_sub6 =["Commercial","Financial"]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub6)

        if self.dockwidget.comboBox_6.currentText() == "Storage":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Transport":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(True)
            LU_list_sub7 =["Transport Terminals","Goods Terminals"]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub7)

        if self.dockwidget.comboBox_6.currentText() == "Utilities":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Under Construction":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Under Developed":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Unknown/Undefined":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_6.currentText() == "Vacant Building":
            self.dockwidget.comboBox_9.clear()
            self.dockwidget.comboBox_9.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_9.addItems(LU_list_sub1)


     #Update land Use Category combobox - UF
    def UFChecked(self):

        if self.dockwidget.checkBox_3.checkState() == 2:
            self.dockwidget.comboBox_7.clear()
            print True
            LU_list = ["","Agriculture","Community","Catering","Education","Government","Hotels","Industry","Leisure","Medical","Offices","Parking","Retail","Residential","Services","Storage","Transport","Utilities", "Under Construction", "Under Developed", "Unknown/Undefined","Vacant Building"] 
            
            self.dockwidget.comboBox_7.setEditable(True)
            self.dockwidget.comboBox_7.addItems(LU_list)

        if self.dockwidget.checkBox_3.checkState() == 0:
            self.dockwidget.comboBox_7.clear()
            self.dockwidget.comboBox_10.clear()
            print False
            LU_list =[]
            
            self.dockwidget.comboBox_7.setEditable(False)
            self.dockwidget.comboBox_10.setEditable(False)
            self.dockwidget.comboBox_7.addItems(LU_list) 
            self.dockwidget.comboBox_10.addItems(LU_list)

    #Update land use subcategory combobox based on land use category combobox - FF
    def UFsubcat(self):

        if self.dockwidget.comboBox_7.currentText() == "":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_7.currentText() == "Agriculture":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_7.currentText() == "Community":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Catering":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(True)
            LU_list_sub1 =["Restaurant and Cafes","Drinking Establishments","Hot Food Takeaways"]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_7.currentText() == "Education":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_7.currentText() == "Government":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Hotels":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1) 

        if self.dockwidget.comboBox_7.currentText() == "Industry":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Offices":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Retail":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Leisure":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(True)
            LU_list_sub2 =["Art and Culture","Amusement or Sports"]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub2) 

        if self.dockwidget.comboBox_7.currentText() == "Medical":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(True)
            LU_list_sub3 =["Hospitals","Health centres"]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub3)

        if self.dockwidget.comboBox_7.currentText() == "Parking":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(True)
            LU_list_sub4 =["Car Parks","Other Vehicles"]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub4)

        if self.dockwidget.comboBox_7.currentText() == "Residential":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(True)
            LU_list_sub5 =["Institutions","Dwellings"]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub5)   

        if self.dockwidget.comboBox_7.currentText() == "Services":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(True)
            LU_list_sub6 =["Commercial","Financial"]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub6)

        if self.dockwidget.comboBox_7.currentText() == "Storage":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Transport":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(True)
            LU_list_sub7 =["Transport Terminals","Goods Terminals"]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub7)

        if self.dockwidget.comboBox_7.currentText() == "Utilities":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Under Construction":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Under Developed":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Unknown/Undefined":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

        if self.dockwidget.comboBox_7.currentText() == "Vacant Building":
            self.dockwidget.comboBox_10.clear()
            self.dockwidget.comboBox_10.setEditable(False)
            LU_list_sub1 =[]   
            self.dockwidget.comboBox_10.addItems(LU_list_sub1)

###################################################################################Traces#############################################################################################
    #Select Folder to Save Traces and Stop Files
    def select_output_file_TR(self):
        filename = QFileDialog.getExistingDirectory(self.dockwidget, "Select Folder ", '')
        self.dockwidget.lineEdit_T5.setText(filename)

    #Launch pop up 
    def runtracesetup(self):
        # show the dialog
        self.dlg2.show()
        # Run the dialog event loop
        result = self.dlg2.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

    #Update Category List from User input
    def updatcategory(self):
        
        Category_List = []
        cattext = self.dlg2.lineEdit_T1.text()
        Category_List.append(cattext)

        for cat in Category_List:
            self.dlg2.listWidget_T2.addItem(cat)

        self.dlg2.lineEdit_T1.clear()        


    #Remove category 
    def removecat(self):
        listItems=self.dlg2.listWidget_T2.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.dlg2.listWidget_T2.takeItem(self.dlg2.listWidget_T2.row(item))


    #Add Stop type from user input
    def updatstop(self):
        
        Stop_List = []
        stoptext = self.dlg2.lineEdit_T2.text()
        Stop_List.append(stoptext)

        for stop in Stop_List:
            self.dlg2.listWidget_T3.addItem(stop) 

        self.dlg2.lineEdit_T2.clear()        


    #Remove Stop
    def removestop(self):
        listItems=self.dlg2.listWidget_T3.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.dlg2.listWidget_T3.takeItem(self.dlg2.listWidget_T3.row(item))

    #Create New File
    def createtracesfile(self):
        vl = QgsVectorLayer("LineString", "Traces1", "memory")
        pr = vl.dataProvider()

        QgsMapLayerRegistry.instance().addMapLayer(vl)  

        input3 = self.iface.activeLayer()
        location = self.dockwidget.lineEdit_T5.text()
        tracedir = '\\ProjectNumber_ProjectName_Traces.shp'
        location1 = location + tracedir
        QgsVectorFileWriter.writeAsVectorFormat(input3, location1, "System", None, "ESRI Shapefile")

        removelayer1 = QgsMapLayerRegistry.instance().mapLayersByName( "Traces1" )[0]
        QgsMapLayerRegistry.instance().removeMapLayers( [removelayer1.id()] )

        stopdir = '\\ProjectNumber_ProjectName_Stops.shp'
        location2 = location + stopdir

        vl1 = QgsVectorLayer("Point", "Stops1", "memory")
        pr1 = vl1.dataProvider()

        QgsMapLayerRegistry.instance().addMapLayer(vl1) 

        input4 = self.iface.activeLayer()
        QgsVectorFileWriter.writeAsVectorFormat(input4, location2, "System", None, "ESRI Shapefile")

        removelayer2 = QgsMapLayerRegistry.instance().mapLayersByName( "Stops1" )[0]
        QgsMapLayerRegistry.instance().removeMapLayers( [removelayer2.id()] )

       

        print location1
        print location2

        input4 = self.iface.addVectorLayer(location1, "Traces", "ogr")
        
        if not input4:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        input4.startEditing()                
               

        edit1 = input4.dataProvider()
        edit1.addAttributes( [ QgsField("Trace_ID", QVariant.Int),
                QgsField("Day",  QVariant.Int),
                QgsField("Time_Period", QVariant.String),
                QgsField("Category", QVariant.String) ] )
        input4.commitChanges()
        input4.startEditing()     

        if self.dlg2.checkBox_T1.checkState() == 2 and self.dlg2.checkBox_T2.checkState() == 2 and self.dlg2.checkBox_T3.checkState() == 2 and self.dlg2.checkBox_T4.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Entry", QVariant.String),QgsField("Exit", QVariant.String),
                QgsField("Gender",  QVariant.Int),
                QgsField("Group_Size", QVariant.String),
                QgsField("Duration", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 2 and self.dlg2.checkBox_T2.checkState() == 2 and self.dlg2.checkBox_T3.checkState() == 2 and self.dlg2.checkBox_T4.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Entry", QVariant.String),QgsField("Exit", QVariant.String),
                QgsField("Gender",  QVariant.Int),             
                QgsField("Duration", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 2 and self.dlg2.checkBox_T2.checkState() == 2 and self.dlg2.checkBox_T3.checkState() == 0 and self.dlg2.checkBox_T4.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Entry", QVariant.String),QgsField("Exit", QVariant.String),
                QgsField("Gender",  QVariant.Int),
                QgsField("Group_Size", QVariant.String)] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 2 and self.dlg2.checkBox_T2.checkState() == 0 and self.dlg2.checkBox_T3.checkState() == 2 and self.dlg2.checkBox_T4.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Entry", QVariant.String),QgsField("Exit", QVariant.String),
                QgsField("Group_Size", QVariant.String),
                QgsField("Duration", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 0 and self.dlg2.checkBox_T2.checkState() == 2 and self.dlg2.checkBox_T3.checkState() == 2 and self.dlg2.checkBox_T4.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [QgsField("Gender",  QVariant.Int),
                QgsField("Group_Size", QVariant.String),
                QgsField("Duration", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 2 and self.dlg2.checkBox_T2.checkState() == 2 and self.dlg2.checkBox_T3.checkState() == 0 and self.dlg2.checkBox_T4.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Entry", QVariant.String),QgsField("Exit", QVariant.String),
                QgsField("Gender",  QVariant.Int)] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 2 and self.dlg2.checkBox_T2.checkState() == 0 and self.dlg2.checkBox_T3.checkState() == 0 and self.dlg2.checkBox_T4.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Entry", QVariant.String),QgsField("Exit", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 2 and self.dlg2.checkBox_T2.checkState() == 0 and self.dlg2.checkBox_T3.checkState() == 0 and self.dlg2.checkBox_T4.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Entry", QVariant.String),QgsField("Exit", QVariant.String), QgsField("Duration", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 2 and self.dlg2.checkBox_T2.checkState() == 0 and self.dlg2.checkBox_T3.checkState() == 2 and self.dlg2.checkBox_T4.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Entry", QVariant.String),QgsField("Exit", QVariant.String), QgsField("Group_Size", QVariant.String)] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 0 and self.dlg2.checkBox_T2.checkState() == 0 and self.dlg2.checkBox_T3.checkState() == 2 and self.dlg2.checkBox_T4.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Group_Size", QVariant.String),
                QgsField("Duration", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 0 and self.dlg2.checkBox_T2.checkState() == 0 and self.dlg2.checkBox_T3.checkState() == 0 and self.dlg2.checkBox_T4.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Duration", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 0 and self.dlg2.checkBox_T2.checkState() == 0 and self.dlg2.checkBox_T3.checkState() == 2 and self.dlg2.checkBox_T4.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Group_Size", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 0 and self.dlg2.checkBox_T2.checkState() == 2 and self.dlg2.checkBox_T3.checkState() == 0 and self.dlg2.checkBox_T4.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Gender",  QVariant.Int) ] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 0 and self.dlg2.checkBox_T2.checkState() == 2 and self.dlg2.checkBox_T3.checkState() == 2 and self.dlg2.checkBox_T4.checkState() == 0:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Gender",  QVariant.Int), QgsField("Group_Size", QVariant.String)] )
            input4.commitChanges()
            input4.startEditing()

        elif self.dlg2.checkBox_T1.checkState() == 0 and self.dlg2.checkBox_T2.checkState() == 2 and self.dlg2.checkBox_T3.checkState() == 0 and self.dlg2.checkBox_T4.checkState() == 2:
            edit1 = input4.dataProvider()
            edit1.addAttributes( [ QgsField("Gender",  QVariant.Int), QgsField("Duration", QVariant.String) ] )
            input4.commitChanges()
            input4.startEditing()


        input6 = self.iface.addVectorLayer(location2, "Stops", "ogr")

        if not input6:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer failed to load!' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        else:
            msgBar = self.iface.messageBar()
            msg = msgBar.createMessage( u'Layer loaded:' + location )
            msgBar.pushWidget( msg, QgsMessageBar.INFO, 10 )

        input6.startEditing()

        edit2 = input6.dataProvider()  
        edit2.addAttributes( [ QgsField("ID", QVariant.Int), QgsField("Day",  QVariant.Int), QgsField("Time_Period", QVariant.String),
         QgsField("Trace ID", QVariant.String),QgsField("Stop_Type", QVariant.String) ] )
        input6.commitChanges()
        

        if self.dlg2.checkBox_T5.checkState() == 2:
            edit5 = input6.dataProvider()
            edit5.addAttributes( [ QgsField("Arrival_time", QVariant.String), QgsField("Departure_time", QVariant.String)]  ) 
            input6.commitChanges()
            input6.startEditing()

        else:
            pass

        catitems = []
        for index in xrange(self.dlg2.listWidget_T2.count()):
            catitems.append(self.dlg2.listWidget_T2.item(index).text())
        
        self.dlg3.comboBox_T15.addItems(catitems) 

        stopitems = []
        for index in xrange(self.dlg2.listWidget_T3.count()):
            stopitems.append(self.dlg2.listWidget_T3.item(index).text())
        """self.dockwidget.comboBox_T12.addItems(stopitems)"""
        

        finaltime = []
        for index in xrange(self.dlg2.listWidget.count()):
            finaltime.append(self.dlg2.listWidget.item(index).text())     
        self.dockwidget.comboBox_T41.addItems(finaltime)  



        self.dlg2.accept()


    #Launch Trace commit Pop up
    def tracescommit(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg3.show()
        # Run the dialog event loop
        result = self.dlg3.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            pass

        self.dlg3.comboBox_T15.setEnabled(True)
        self.dlg3.comboBox_T27.setEnabled(True)
        self.dlg3.comboBox_T31.setEnabled(True)
        self.dlg3.comboBox_T32.setEnabled(True)
        self.dockwidget.comboBox_T41.setEnabled(True)
        
        i= self.dockwidget.lineEdit_T112.text()
        inti = int(i)
        finalid = str(inti+1)
        self.dockwidget.lineEdit_T112.setText(finalid)

        id2 = str(inti)

        self.dlg3.lineEdit_T113.setText(id2)

    
        
        

   #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            #print "** STARTING DataInputFrontages"

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = DataInputFrontagesDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)

            # show the dockwidget
            # TODO: fix to allow choice of dock locationhttp://doc.qt.io/qt-4.8/qcombobox.html#activated
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
            self.Ent_updatelist()

            self.Frnt_updatelist()            

            
            layer_list = ["Ground Floor","Upper Floor","Lower Floor"]
            self.dockwidget.comboBox_E1.addItems(layer_list) 

            LU_Thematiclist = ["SSL Code","TCPA Code","NLUD Code"]
            self.dockwidget.comboBox_11.addItems(LU_Thematiclist) 
            self.dockwidget.comboBox_11.setEditable(False)

            E_Thematiclist = ["SSL Standard - General","SSL Standard - Detailed"]
            self.dockwidget.comboBox_E12.addItems(E_Thematiclist) 
            self.dockwidget.comboBox_E12.setEditable(False)


            F_Thematiclist = ["SSL Standard"]
            self.dockwidget.comboBox_F12.addItems(F_Thematiclist)   

            tracetimelist = [ "07:00 - 07:30","07:30 - 08:00","08:00 - 08:30","08:30 - 09:00","9:00 - 09:30","9:30 - 10:00","10:00 - 10:30","10:30 - 11:00",
            "11:00 - 11:30","11:30 - 12:00","12:00 - 12:30","12:30 - 13:00","13:00 - 13:30","13:30 - 14:00","14:00 - 14:30","14:30 - 15:00","15:00 - 15:30","15:30 - 16:00","16:00 - 16:30",
            "16:30 - 17:00","17:00 - 17:30","17:30 - 18:00","18:00 - 18:30","18:30 - 19:00","19:00 - 19:30","19:30 - 20:00","20:00 - 20:30","20:30 - 21:00","21:00 - 21:30","21:30 - 22:00"]
            self.dlg2.listWidget.clear()
            for time in tracetimelist:
                self.dlg2.listWidget.addItem(time)




            Entry =[ "A","B","C","D","E","F","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","----------------","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
            self.dlg3.comboBox_T31.addItems(Entry)   
            Exit =[ "A","B","C","D","E","F","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z","----------------","1","2","3","4","5","6","7","8","9","10","11","12","13","14","15"]
            self.dlg3.comboBox_T32.addItems(Exit)  

            Genderlist = ["","Male", "Female"] 
            self.dlg3.comboBox_T27.addItems(Genderlist)

            


            self.dockwidget.pushButton_L3.setEnabled(False)
            self.dockwidget.comboBox_5.setEditable(False)
            self.dockwidget.comboBox_6.setEditable(False)
            self.dockwidget.comboBox_7.setEditable(False)
            self.dockwidget.checkBox.setCheckable(False)
            self.dockwidget.checkBox_2.setCheckable(False)
            self.dockwidget.checkBox_3.setCheckable(False)
            self.dockwidget.lineEdit_8.setEnabled(False)
            self.dockwidget.lineEdit_9.setEnabled(False)
            self.dockwidget.lineEdit_10.setEnabled(False)          


            

            #GF
            self.dockwidget.checkBox.stateChanged.connect(self.GFChecked)
            self.dockwidget.comboBox_5.activated.connect(self.GFsubcat)
            #FF
            self.dockwidget.checkBox_2.stateChanged.connect(self.FFChecked)
            self.dockwidget.comboBox_6.activated.connect(self.FFsubcat)
            #UF
            self.dockwidget.checkBox_3.stateChanged.connect(self.UFChecked)
            self.dockwidget.comboBox_7.activated.connect(self.UFsubcat)

                         
                

            self.dockwidget.pushButton_f.setEnabled(False)
            self.dockwidget.pushButton_g.setEnabled(False)
            self.dockwidget.pushButton_h.setEnabled(False)
            self.dockwidget.pushButton_i.setEnabled(False)
            self.dockwidget.pushButton_j.setEnabled(False)
            self.dockwidget.pushButton_k.setEnabled(False)
            self.dockwidget.pushButton_l.setEnabled(False)
            self.dockwidget.pushButton_m.setEnabled(False)
            self.dockwidget.pushButton_n.setEnabled(False)
            self.dockwidget.pushButton_o.setEnabled(False)
            self.dockwidget.pushButton_p.setEnabled(False)
            self.dockwidget.pushButton_q.setEnabled(False)
            self.dockwidget.pushButton_xx.setEnabled(False)
            self.dockwidget.comboBox_F12.setEditable(False)
            

###################################################################################FRONTAGES#############################################################################################
        # add layer from file  
               
            self.dockwidget.toolButton_b.clicked.connect(self.select_output_file)
            self.dockwidget.toolButton_a.clicked.connect(self.select_input_file)
            self.dockwidget.pushButton_c.clicked.connect(self.explode)
            self.dockwidget.pushButton_e.clicked.connect(self.Loadfile)
            self.dockwidget.toolButton_d.clicked.connect(self.select_existing_file)

        #Draw Lines
            self.dockwidget.pushButton_f.clicked.connect(self.DrawTransparent)
            self.dockwidget.pushButton_g.clicked.connect(self.DrawSemiTransparent)
            self.dockwidget.pushButton_h.clicked.connect(self.DrawBlank)
            self.dockwidget.pushButton_i.pressed.connect(self.DrawHighOpaqueFence)
            self.dockwidget.pushButton_j.clicked.connect(self.DrawSTFence)
            self.dockwidget.pushButton_k.clicked.connect(self.DrawLowFence)

        #Selection Update
            self.dockwidget.pushButton_l.clicked.connect(self.updateTransparent)
            self.dockwidget.pushButton_m.clicked.connect(self.updateSemiTransparent)
            self.dockwidget.pushButton_n.clicked.connect(self.updateBlank)
            self.dockwidget.pushButton_o.pressed.connect(self.updateFenceHighOpaque)
            self.dockwidget.pushButton_p.clicked.connect(self.updateFenceHighSeeThrough)
            self.dockwidget.pushButton_q.clicked.connect(self.updateFenceLow)
        
        #Custom Thematic
            self.dockwidget.toolButton_r.clicked.connect(self.select_input_qml)
            self.dockwidget.pushButton_s.clicked.connect(self.CustomThematic)
            

        #Delete extra lines
            self.dockwidget.pushButton_xx.clicked.connect(self.deletelinesrun)

        #Spatial Join
            self.dockwidget.pushButton_F2.clicked.connect(self.Frnt_updatelist)
            self.dockwidget.pushButton_F1.clicked.connect(self.Frnt_spatialjoin)

###################################################################################ENTRANCES#############################################################################################
        #Create File
            self.dockwidget.toolButton_b_2.clicked.connect(self.select_output_file_E)
            self.dockwidget.toolButton_d2.clicked.connect(self.select_existing_file_E)
            self.dockwidget.pushButton_c_2.clicked.connect(self.createEntrances)
            self.dockwidget.pushButton_e_2.clicked.connect(self.Loadfile_E)

        #Selection Update
            self.dockwidget.pushButton_E3.clicked.connect(self.updateControlled)
            self.dockwidget.pushButton_E4.clicked.connect(self.updateUNcontrolled)

        #Draw Points
            self.dockwidget.pushButton_E2.clicked.connect(self.GroundControlledDefault)
            self.dockwidget.pushButton_E3_2.clicked.connect(self.GroundControlledService)
            self.dockwidget.pushButton_E4_2.clicked.connect(self.GroundControlledFire)
            self.dockwidget.pushButton_E5.clicked.connect(self.GroundControlledUnused)
            self.dockwidget.pushButton_E6.clicked.connect(self.GroundUNControlledDefault)
            self.dockwidget.pushButton_E7.clicked.connect(self.UpperControlledDefault)
            self.dockwidget.pushButton_E8.clicked.connect(self.UpperControlledService)
            self.dockwidget.pushButton_E9.clicked.connect(self.UpperControlledFire)
            self.dockwidget.pushButton_E10.clicked.connect(self.UpperControlledUnused)
            self.dockwidget.pushButton_E11.clicked.connect(self.UpperUNControlledDefault)
            self.dockwidget.pushButton_E12.clicked.connect(self.LowerControlledDefault)
            self.dockwidget.pushButton_E13.clicked.connect(self.LowerControlledService)
            self.dockwidget.pushButton_E14.clicked.connect(self.LowerControlledFire)
            self.dockwidget.pushButton_E15.clicked.connect(self.LowerControlledUnused)
            self.dockwidget.pushButton_E16.clicked.connect(self.LowerUNControlledDefault)

        #Thematic
            self.dockwidget.toolButton_E1.clicked.connect(self.Ent_select_input_qml2)
            self.dockwidget.pushButton_ET.clicked.connect(self.Ent_CustomThematic)
            

        #Spatial Join
            self.dockwidget.pushButton_E5_2.clicked.connect(self.Ent_updatelist)
            self.dockwidget.pushButton_E6_2.clicked.connect(self.Ent_spatialjoin)


###################################################################################LAND USES#############################################################################################
         #Create and Load File
            self.dockwidget.toolButton_L8.clicked.connect(self.select_input_file_LU)
            self.dockwidget.toolButton_L4.clicked.connect(self.select_output_file_LU)
            self.dockwidget.pushButton_L5.clicked.connect(self.LUNewFile)

            self.dockwidget.toolButton_L6.clicked.connect(self.select_existing_file_LU)
            self.dockwidget.pushButton_L7.clicked.connect(self.Loadfile_LU)
        #Update
            self.dockwidget.pushButton_L3.clicked.connect(self.LuGFUpdate)
        #Thematic
            self.dockwidget.pushButton_LU1.clicked.connect(self.LUThematics)
            self.dockwidget.toolButton_LU.clicked.connect(self.select_inputThematic_file_LU)


###################################################################################TRACES#############################################################################################

            self.dockwidget.pushButton_T2.clicked.connect(self.runtracesetup)
            self.dockwidget.toolButton_T1.clicked.connect(self.select_output_file_TR)
            self.dlg2.pushButton_T3.clicked.connect(self.updatcategory)
            self.dlg2.pushButton_T4.clicked.connect(self.removecat)
            self.dlg2.pushButton_T6.clicked.connect(self.updatstop)
            self.dlg2.pushButton_T7.clicked.connect(self.removestop)
            self.dlg2.pushButton_T5.clicked.connect(self.createtracesfile)
            self.dockwidget.pushButton_T10.clicked.connect(self.tracescommit)




    
        


