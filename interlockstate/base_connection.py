class BaseConnection(object):
    def __new__(self, model):
        import PyTango
        try:
            return PyTango.DeviceProxy(model)
        except PyTango.DevFailed, e:
            print 'Prepare Model ---> Received a DevFailed exception:', e
		
