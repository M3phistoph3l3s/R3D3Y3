R3D3Y3 2.0
==========

Parachat Logging Software

This software creates a working log of chat messages from the chat site "chat.parachat.com" in room "Lobby-2"
This will create two (2) log files, they are as follows: 
        - R3D3Y3.log 
                The file "R3D3Y3.log" contains logs regarding the operation of the software. 
                This includes any errors, warnings and notifications about the status of the 
                execution of the software. 
        - parachat.log
                The file "parachat.log" contains the active log of messages sent in the 
                public "room" of the site "chat.parachat.com", this "room" is also known as 
                "Lobby-2". These logs are stored in the following format: 
                        (Date the message was logged)~(Time the message was logged)>> (Username): (Message text) 
                Smilies are not logged as messages are kept in plain ASCII format 
 
Times recorded by this software are affected by the time zone of the system clock. 
This software was written and tested on a Unix-like platform and has not been tested on any other platform. *Microsoft products suck* 
All handled exceptions within this software will result in the software establishing a new session automatically. 
Failure to initiate a new session will result in a 120 second pause in execution before trying again. 
 
And as always, have nice day. 
 
~William J. Appleton (Mephistopheles)
