'''
Created on Apr 15, 2015

@author: guest
'''
from PyQt4 import QtGui
import PyTango
from taurus.qt.qtgui.display import TaurusLed
import os
import re
from time import sleep
from base_connection import BaseConnection

class ResetWidget(QtGui.QFrame):
    '''
    classdocs
    '''


    def __init__(self, parent, model = None):
        '''
        Constructor
        '''
        super(ResetWidget, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum,
                           QtGui.QSizePolicy.Minimum)
        self.model = model

        self.mainLayout = QtGui.QFormLayout(self)
#         self.mainLayout = QtGui.QGridLayout(self)
#         self.layout = QtGui.QHBoxLayout(self)
#         self.mainLayout.setLayout(1, QtGui.QFormLayout.LabelRole, self.layout)
        self.setLayout(self.mainLayout)
        self.setFrameShape(QtGui.QFrame.Box)
        
        self.prepareView()
        self.prepareData()
        
    def prepareView(self):
        self.resetLabel = QtGui.QLabel(self)
        self.resetLabel.setText('Reset: ')
        self.resetLabel.setFrameShape(QtGui.QFrame.Panel)
        self.mainLayout.addRow(self.resetLabel)
        
    def prepareData(self):
        try:
            for m in self.model:
    #             print self.devgr
                try: 
                    self.dev = BaseConnection(m)
                except Exception, e:
                    print 'Model ---> An exception occured: ',e
                else:
    #             print '2'
    #             print self.dev.name()
                    self.model_command = [ self.dev.name() + '/%s' % p for p in filter(lambda x: x[-1] in ['C','c'], self.dev.get_attribute_list()) ]
                    print 'Model command: %s' % self.model_command
                    
                if self.model_command:
                    self.resetCommand = filter(lambda x: any(i in x.lower() for i in ('reset','rps')), self.model_command)
                    print 'Reset command: %s' % self.resetCommand
                    if self.resetCommand:
                        for n in self.resetCommand:
                            print 'Reset command: %s' % n
                            self.mainLayout.addRow(self.resetButtons(self.model, n))
#                             self.prepareView()

        except Exception, e:
            print 'Prepare Data ---> An unforeseen exception occured: ', e
        
    def resetButtons(self, dev, attr):
        buttonName = {'PLC/IMAG/BOOLEAN/B_I_K00CAB02_CTL_RPS_C':'MAG PS CAB02',
                        'PLC/IMAG/BOOLEAN/B_MAG_RPS_All_C':'MAG PS Linac',
                        'PLC/IMAG/BOOLEAN/B_I_TLCAB03_CTL_RPS_C':'MAG PS CAB03',
                        'PLC/IMAG/BOOLEAN/B_R1_SGDCAB12_CTL_RPS_C':'MAG PS CAB12',
                        'PLC/IRF/BOOLEAN/B_Reset_All_C':'RF WAT Linac',
                        'PLC/IVAC/BOOLEAN/B_Reset_C':'VAC Linac ',
                        'PLC/R1-12-01-VAC/BOOLEAN/B_R1_Reset_C':'VAC Ring',
                        'PLC/R1-SGA-MAG/BOOLEAN/B_R1_Reset_C':'MAG PS Ring'
                        }
        
        print 'Reset: %s : %s' % (dev, attr)
        from PyQt4 import QtCore
        try:
            _fromUtf8 = QtCore.QString.fromUtf8
        except AttributeError:
            def _fromUtf8(s):
                return s
            
        self.rstButton = QtGui.QPushButton()
#         self.rstButton.setText(attr.split('/')[3])
        self.rstButton.setText(buttonName[attr.upper()])
        QtCore.QObject.connect(self.rstButton, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), lambda who="One": self.exeButton(attr))
        return self.rstButton
    
    def exeButton(self, attr):
        print 'Execute Button %s ' % (attr[:attr.rfind('/')])
        try: 
            self.dev = self.prepareModel(attr[:attr.rfind('/')])
        except Exception, e:
            print '-------> An exception occured: ', e
        else:
            print attr.split('/')[3]
            self.dev.write_attribute(attr.split('/')[3], 0)
            sleep(1.5)
            self.dev.write_attribute(attr.split('/')[3], 1)
    
