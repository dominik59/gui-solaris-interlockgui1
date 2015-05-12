'''
Created on Mar 23, 2015

@author: guest
'''
import os
import sys
from PyQt4 import QtGui
import PyTango

from interlockstate import InterlockStateWidget
from interlockstate import ResetWidget

class InterlockStatusOverview(QtGui.QWidget):
    def __init__(self, parent = None):
        super(InterlockStatusOverview, self).__init__(parent)
        self.setSizePolicy(QtGui.QSizePolicy.MinimumExpanding,
                           QtGui.QSizePolicy.MinimumExpanding)
# 
        os.environ["TANGO_HOST"] = '192.168.130.200:10000'
        try:
            self.db = PyTango.Database()
        except Exception as e:
            print 'Unknown problem: %s' % e
        
        # central layout
        self.mainLayout = QtGui.QGridLayout()
#         close button
        self.closeButton = QtGui.QPushButton()
        self.closeButton.setText('Close')
#         self.mainLayout.addWidget(self.tabWidget, 0, 0)
        self.mainLayout.addWidget(self.closeButton, 1, 0)
# 
        try:
            self.interlock = InterlockStateWidget(self)
            self.mainLayout.addWidget(self.interlock, 0, 0)
        except Exception as e:
            print 'Unknown problem: %s' % e   
        
        try:
            self.devList = self.db.get_device_exported_for_class('OPCaccess')
            self.filterDev = filter(lambda x: x.split('/')[2].lower() in ['boolean'], self.devList)
#         self.ydevWidgetList = []
            if self.filterDev:  
#                 for dev_name in self.filterDev:
#                     print dev_name
                try:
                    reset_widget = ResetWidget(self, self.filterDev)
                except Exception, e:
                    print 'Fail to create widget: %s' % e
                self.mainLayout.addWidget(reset_widget, 0, 1)
        
        except Exception as e:
            print 'Unknown problem: %s' % e
        
        self.closeButton.clicked.connect(self.close)
        self.setLayout(self.mainLayout)
        
def main():
    try:
        app = QtGui.QApplication(sys.argv)
        myWidget = InterlockStatusOverview()
        myWidget.show()
        sys.exit(app.exec_())
  
    except PyTango.DevFailed, e:
        print '-------> Received a DevFailed exception:',e
    except Exception, e:
        print '-------> An unforeseen exception occured....',e
 
if __name__ == '__main__':
    main()