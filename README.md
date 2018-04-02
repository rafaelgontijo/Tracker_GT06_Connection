TRACKER GT06 CONNECTION
===================

This is a sample files to your get information on your tracker,

currently, GT06 Connection, get login(s) message(s), position(s) information(s) and heartbeat messages(s)


OBSERVATION
===========
This is not a full project, but is a example for your implementation. (Adapt to your Django project or other python framework's project)
Others informations (Alarm, fence, server call to tracker and others) is not implemented


USAGE
===========
configure your track to call a server in port 55000.
In python terminal, run the code:

    import GT06Connection
    gt06 = GT06Connection()
    gt06.listner()

Sorry for my bad inglish