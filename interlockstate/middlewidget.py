from PyQt4 import QtGui
from taurus.qt.qtgui.display import TaurusLed
import os
import re
from singlewidget import DeviceWidget
from base_connection import BaseConnection

class MiddleWidget(QtGui.QFrame):

    def __init__(self, parent, model = None):
        '''
        Constructor
        '''
        super(MiddleWidget, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy.Minimum,
                           QtGui.QSizePolicy.Minimum)
        self.model = model

#         self.mainLayout = QtGui.QFormLayout(self)
#         self.mainLayout = QtGui.QGridLayout(self)
        self.mainLayout = QtGui.QHBoxLayout(self)
#         self.mainLayout.setLayout(1, QtGui.QFormLayout.LabelRole, self.layout)
        self.setLayout(self.mainLayout)
        self.setFrameShape(QtGui.QFrame.Box)
        self.prepareData()
        
    def prepareData(self):
        self.devgr = ['i_k00', 'i_k01', 'i_k02', 'i_k03', 'i_s00', 'i_s01', 'i_s02', 'i_s03', 'b_r1', 'i_tr1', 'i_trl']
#         print 'Model: %s' % self.model
        try:
#             print self.devgr
            try: 
                self.dev = BaseConnection(self.model)
            except Exception, e:
                print 'Model ---> An exception occured: ', e
            else:
#             print '2'
#             print self.dev.name()
                attrDev = [ self.dev.name() + '/%s' % p for p in filter(lambda x: x[-1] in ['A','a'], self.dev.get_attribute_list()) ]

            if attrDev:
#                 print 'Device attributes: %s ' % attrDev
                for j, i in enumerate(self.devgr):
                    self.devsGr = sorted(filter(lambda x: re.search(i, x.lower()), attrDev))
                    self.devsGr = self.chunks(self.devsGr, 25)
                    for d in self.devsGr:
                        if d:
    #                         print self.devsGr
                            newDevice = DeviceWidget(self, d, i)
    #                         print i, j
    #                         self.mainLayout.addItem(newDevice, 0, j)
                            self.mainLayout.addWidget(newDevice)
#             if self.model_command:
#                 self.resetCommand = filter(lambda x: any(i in x.lower() for i in ('reset','rps')), self.model_command)
#                 if self.resetCommand:
#                     for n in self.resetCommand:
#                         self.mainLayout.addRow(self.resetButtons(self.model, n))
#             self.setLayout(self.layout)
        except Exception, e:
            print 'Prepare Data---> An unforeseen exception occured: ',e
            self.prepareLabel(e)
            
    def prepareLabel(self, e):
        self.label = QtGui.QLabel(self)
        self.label.setText(str(e))
        self.mainLayout.addWidget(self.label)
            
            
    def chunks(self, l, n):
        n = max(1, n)
        return [l[i:i + n] for i in range(0, len(l), n)]
