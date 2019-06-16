# -*- coding: utf-8 -*-
"""
/***************************************************************************
 CatchmentAnalyser
                             Catchment Analyser
 Network based catchment analysis
                              -------------------
        begin                : 2016-05-19
        author               : Laurens Versluis
        copyright            : (C) 2016 by Space Syntax Limited
        email                : l.versluis@spacesyntax.com
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

import os

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'catchment_analyser_dialog_base.ui'))


class CatchmentAnalyserDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(CatchmentAnalyserDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # Output internal GUI signals
        self.nameCheck.stateChanged.connect(self.activateName)
        self.distancesText.setPlaceholderText("Separate with a comma")
        self.networkText.setPlaceholderText("Save as temporary layer...")
        self.networkSaveButton.clicked.connect(self.setNetworkOutput)
        self.cancelButton.clicked.connect(self.stopRunning)
        self.analysisButton.clicked.connect(self.setRunning)

        # Setup the progress bar
        self.analysisProgress.setMinimum(0)
        self.analysisProgress.setMaximum(100)
        self.is_running = False


    def setNetworkLayers(self, names):
        layers = ['-----']
        if names:
            layers = []
            layers.extend(names)
            self.analysisButton.setEnabled(True)
        else:
            self.analysisButton.setEnabled(False)
        self.networkCombo.clear()
        self.networkCombo.addItems(layers)

    def getNetwork(self):
        return self.networkCombo.currentText()

    def setCostFields(self, names):
        self.costCombo.clear()
        if names:
            #self.costCheck.setEnabled(True)
            self.costCombo.addItems(['length'] + names)
        else:
            fields = ['-----']
            self.costCombo.addItems('length')
            self.costCombo.addItems(fields)

    def getCostField(self):
        if self.costCombo.currentText() == '':
            cost_field = None
        else:
            cost_field = self.costCombo.currentText()
        return cost_field

    def setOriginLayers(self, names):
        layers = ['-----']
        if names:
            layers = []
            layers.extend(names)
            self.analysisButton.setEnabled(True)
        else:
            self.nameCheck.setEnabled(False)
            self.analysisButton.setEnabled(False)
        self.originsCombo.clear()
        self.originsCombo.addItems(layers)

    def getOrigins(self):
        return self.originsCombo.currentText()

    def activateName(self):
        if self.nameCheck.isChecked():
            self.nameCombo.setEnabled(True)
        else:
            self.nameCombo.setEnabled(False)

    def setNameFields(self, names):
        self.nameCombo.clear()
        if names:
            self.nameCheck.setEnabled(True)
            self.nameCombo.addItems(names)
        else:
            self.nameCheck.setEnabled(False)
            fields = ['-----']
            self.nameCombo.addItems(fields)

    def getName(self):
        if self.nameCheck.isChecked():
            return self.nameCombo.currentText()
        else:
            return None

    def getDistances(self):
        if self.distancesText.text():
            distances = self.distancesText.text().split(',')
            return distances

    def getNetworkTolerance(self):
        return self.networkTolSpin.value()

    def getPolygonTolerance(self):
        return self.polygonTolSpin.value()

    def setNetworkOutput(self):
        file_name = QtGui.QFileDialog.getSaveFileName(self, "Save output file ", "catchment_network", '*.shp')
        if file_name:
            self.networkText.setText(file_name)

    def getNetworkOutput(self):
        return self.networkText.text()

    def setRunning(self):
        self.is_running = True

    def stopRunning(self):
        if self.is_running:
            self.is_running = False
        else:
            self.closeDialog()

    def closeEvent(self, QCloseEvent):
        self.closeDialog()

    def closeDialog(self):
        self.costCombo.clear()
        self.costCombo.setEnabled(True)
        self.nameCombo.clear()
        self.nameCombo.setEnabled(False)
        self.nameCheck.setCheckState(False)
        self.distancesText.clear()
        self.networkTolSpin.setValue(1)
        self.polygonTolSpin.setValue(20)
        self.networkText.clear()
        self.analysisProgress.reset()
        self.close()





