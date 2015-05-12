'''
Created on Mar 23, 2015

@author: guest
'''
from PyQt4 import QtGui
import PyTango
from taurus.qt.qtgui.display import TaurusLed
import os
import re

class DeviceWidget(QtGui.QFrame):
    '''
    classdocs
    '''

    def __init__(self, parent, model = None, devGr = None):
        '''
        Constructor
        '''
        super(DeviceWidget, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum,
                           QtGui.QSizePolicy.Minimum)
            
        self.model = model
#         self.devName = devName
        self.devGr = devGr
        self.mainLayout = QtGui.QFormLayout(self)
#         self.mainLayout = QtGui.QGridLayout(self)
        self.setLayout(self.mainLayout)
        self.setFrameShape(QtGui.QFrame.Box)

        self.prepareData()
#         self.prepareView()
#         self.addItemsToLayout()
#         self.modelConnection(self.model)
#         self.signalConnection()

    def prepareTitle(self):
        self.label = QtGui.QLabel(self)
#         self.label.setText(self.devGr.replace('_', '-').upper())
        self.label.setText(self.model[0].split('/')[3].split('_')[2].upper())
        self.label.setFrameShape(QtGui.QFrame.Box)
        self.mainLayout.addRow(self.label)
    
    def prepareView(self):
#         print 'Prepare view'
        self.interlockLabel = QtGui.QLabel(self)
        self.interlockLed = TaurusLed(self)
        self.interlockLed.setFixedSize(20, 20)
        self.interlockLed.setOnColor("red")
        
    def addItemsToLayout(self):
#         print 'add to layout'
        self.mainLayout.addRow(self.interlockLabel, self.interlockLed)
#         self.mainLayout.addRow(self.interlockLabel)
        
    def modelConnection(self, new_model):
#         print 'Model connection'
        if new_model:
#             print self.model
            self.interlockLabel.setText(new_model.split('/')[3].split('_')[4])
            self.interlockLed.setModel(new_model)

    def prepareData(self):
#         print 'devGr: %s' % self.devGr
#         print 'model: %s' % self.model
        self.prepareTitle()
        for i in self.model:
#             print i
            self.prepareView()
            self.addItemsToLayout()
            self.modelConnection(i)

#             self.signalConnection()

#     def signalConnection(self):
#         pass
        