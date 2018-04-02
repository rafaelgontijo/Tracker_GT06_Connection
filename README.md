TRACKER GT06 CONNECTION
===================

This is a sample files to your get information on your tracker.<br/>
currently, GT06 Connection, get login(s) message(s), position(s) information(s) and heartbeat messages(s).


OBSERVATION
===========
This is not a full project, but is a example for your implementation. (Adapt to your Django project or other python framework's project <br/>
Others informations (Alarm, fence, server call to tracker and others) is not implemented.<br/>


USAGE
===========
configure your track to call a server in port 55000.<br/>
In python terminal, run the code:

    import GT06Connection
    gt06 = GT06Connection()
    gt06.listner()


OTHERS AND THANKS
=================
the file to generate the crc, i'm not a owner, i did a small change, however i lost the source, if you know, let me know, to i'm put here

<br/><br/>
Sorry for my bad inglish
