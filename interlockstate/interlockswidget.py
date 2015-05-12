'''
Created on Mar 23, 2015

@author: guest
'''
import os
from PyQt4 import QtGui
import PyTango
from middlewidget import MiddleWidget
import re

class InterlockStateWidget(QtGui.QTabWidget):
    '''
    classdocs
    '''

    def __init__(self, parent = None):
        '''
        Constructor
        '''
        super(InterlockStateWidget, self).__init__(parent)
        
        self.setSizePolicy(QtGui.QSizePolicy.Minimum,
                           QtGui.QSizePolicy.Minimum)
#         os.environ["TANGO_HOST"] = '192.168.130.200:10000'
        try:
            self.db = PyTango.Database()
        except Exception as e:
            print 'Connection to Tango db problem: %s' % e
            
#         self.mainLayout = QtGui.QFormLayout(self)
#         self.tabWidget = QtGui.QTabWidget()
#         self.setLayout(self.mainLayout)
        self.createYagWidgets()
        
    def createYagWidgets(self):
        
        tabNames = {'PLC/IMAG/BOOLEAN':'Linac-Magnets',
                    'PLC/IRF/BOOLEAN':'Linac-RF',
                    'PLC/IVAC/BOOLEAN':'Linac-Vacuum',
                    'PLC/IWAT/BOOLEAN':'Linac-Water',
                    'PLC/R1-02-03-VAC/BOOLEAN':'Ring-02-03-VAC',
                    'PLC/R1-04-05-VAC/BOOLEAN':'Ring-04-05-VAC',
                    'PLC/R1-06-07-VAC/BOOLEAN':'Ring-06-07-VAC',
                    'PLC/R1-08-09-VAC/BOOLEAN':'Ring-08-09-VAC',
                    'PLC/R1-10-11-VAC/BOOLEAN':'Ring-10-11-VAC',
                    'PLC/R1-12-01-VAC/BOOLEAN':'Ring-12-01-VAC',
                    'PLC/R1-C134-MAG/BOOLEAN':'Ring-Magnets',
                    'PLC/R1-NEG-VAC/BOOLEAN':'Ring-NEG',
                    'PLC/R1-SGA-MAG/BOOLEAN':'Ring-SGA-MAG',
                    'PLC/R1-SGB-MAG/BOOLEAN':'Ring-SGB-MAG',
                    'PLC/R1-SGC-MAG/BOOLEAN':'Ring-SGC-MAG',
                    'PLC/R1-SGD-MAG/BOOLEAN':'Ring-SGD-MAG'
                    }
        
        excludedDevices = ['PLC/R1-NEG-VAC/BOOLEAN']
        
        self.devList = self.db.get_device_exported_for_class('OPCaccess')

#         self.devList = ['PLC/IMAG/BOOLEAN', 'PLC/IRF/BOOLEAN', 'PLC/IVAC/BOOLEAN', 'PLC/IWAT/BOOLEAN', 
#                          'PLC/R1-02-03-VAC/BOOLEAN', 'PLC/R1-04-05-VAC/BOOLEAN', 'PLC/R1-06-07-VAC/BOOLEAN', 
#                          'PLC/R1-08-09-VAC/BOOLEAN', 'PLC/R1-10-11-VAC/BOOLEAN', 'PLC/R1-12-01-VAC/BOOLEAN', 
#                          'PLC/R1-C134-MAG/BOOLEAN', 'PLC/R1-NEG-VAC/BOOLEAN', 'PLC/R1-SGA-MAG/BOOLEAN', 
#                          'PLC/R1-SGB-MAG/BOOLEAN', 'PLC/R1-SGC-MAG/BOOLEAN', 'PLC/R1-SGD-MAG/BOOLEAN']
         
        self.filterDev = filter(lambda x: x.split('/')[2].lower() in ['boolean'], self.devList)
        self.selectedDev = sorted(filter(lambda x: x.upper() not in excludedDevices, self.filterDev))
#         print 'Excluded %s' % self.excluded
#         print self.filterDev

        if self.selectedDev:
            for dev_name in self.selectedDev:
#                 print dev_name
#                 try:
#                     self.devs = PyTango.DeviceProxy(dev_name)
#                     print self.devs.get_attribute_list()
#                 except Exception as e:
#                     print 'Connection to Tango db problem: %s' % e
#                 print dev_name
                try: 
                    new_widget = MiddleWidget(self, dev_name)
                except Exception, e:
                    print 'Fail to create widget: %s' % e
                else:
    #             self.devWidgetList.append(new_widget)
    #             column = (len(self.yagWidgetList) - 1) % 5
    #             row = (len(self.yagWidgetList) - 1) / 5
    #             self.gridLayout.addWidget(new_widget, row, column)
#                 self.widgetList.append(new_widget)
#                 column = (len(self.widgetList) - 1) % 5
#                 row = (len(self.widgetList) - 1) / 10
#                 self.mainLayout.addWidget(new_widget, row, column)
#                     print dev_name
                    self.addTab(new_widget, tabNames[dev_name])
