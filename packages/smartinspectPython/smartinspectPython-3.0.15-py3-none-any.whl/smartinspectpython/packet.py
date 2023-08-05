"""
Module: packet.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  

</details>
"""

import os
import _threading_local
import _thread


# our package imports.
from .level import Level as SILevel
from .packettype import PacketType

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class Packet:
    """
    Abstract base class for all packets in the SmartInspect library.

    This class is the base class for all packets in the SmartInspect
    library. The following table lists the available packets
    together with a short description.
    
    Packet             | Description
    -----------------  | ---------------------------------------------------------------------  
    ControlCommand     | Responsible for administrative tasks like clearing the Console.
    LogEntry           | Represents the most important packet in the entire SmartInspect concept. Is used for the majority of logging methods in the Session class.
    LogHeader          | Responsible for storing and transferring log metadata. Used by the PipeProtocol and TcpProtocol classes to support the filter and trigger functionality of the SmartInspect Router service application.
    ProcessFlow        | Responsible for managing thread and process information about your application.
    Watch              | Responsible for handling variable watches.
    
    Threadsafety:
        This class and sub-classes are not guaranteed to be thread-safe.
        To ensure thread-safety, use ThreadSafe as well as the Lock and
        Unlock methods.
    """

    PACKET_HEADER_SIZE:int = 6;
    """
    Size in bytes of the packet header prefix.
    """


    def __init__(self) -> None:
        """ 
        Initializes a new instance of the class. 
        """

        # initialize instance storage.
        self.__fLock = _threading_local.RLock()
        self.__fLevel:SILevel = SILevel.Message
        self.__fThreadSafe:bool = False
        self.__fBytes:int = 0


    @property
    def Bytes(self) -> int:
        """
        Gets the Bytes property value.

        Represents the amount of bytes needed for storing this packet
        in the standard SmartInspect binary log file format as
        represented by BinaryFormatter.
        
        Please note that this property is only set and used by the
        SmartInspect SDK. 
        """
        return self.__fBytes
            
    @Bytes.setter
    def Bytes(self, value:int):
        """ 
        Sets the Bytes property value.
        """
        self.__fBytes = value


    @property
    def HasData(self) -> bool:
        """
        Gets the HasData property value.

        Indicates if this packet contains optional data or not.

        Returns true if this packet contains optional
        data and false otherwise.
        """
        return self.Data and self.Data.getbuffer().nbytes > 0


    @property
    def Level(self) -> SILevel:
        """
        Gets the Level property value.
        
        Represents the log level of this packet.

        Every packet can have a certain log level value. Log levels
        describe the severity of a packet. Please see the Level
        enum for more information about log levels and their usage.
        """
        return self.__fLevel

    @Level.setter
    def Level(self, value:SILevel):
        """ 
        Sets the Level property value.
        """
        if (value != None):
            self.__fLevel = value


    @property
    def PacketType(self) -> PacketType:
        """
        Gets the PacketType property value.

        Represents the type of this packet.
        
        Raises:
            NotImplementedError:
                Thrown if the property method is not overridden in an inheriting class.

        Represents the type of a packet. In the SmartInspect concept,
        there are multiple packet types each serving a special purpose.
        Please see the PacketType enum for more information.
        """
        raise NotImplementedError()


    @property
    def Size(self) -> int:
        """
        Gets the Size property value.

        Calculates and returns the total memory size occupied by
        this packet.

        Raises:
            NotImplementedError:
                Thrown if the property method is not overridden in an inheriting class.

        This read-only property returns the total occupied memory
        size of this packet. This functionality is used by the
        Protocol.IsValidOption protocol feature to calculate the 
        total backlog queue size.
        """
        raise NotImplementedError()


    @property
    def ThreadSafe(self) -> bool:
        """
        Gets the ThreadSafe property value.

        Indicates if this packet is used in a multi-threaded
        SmartInspect environment.

        Set this property to true before calling Lock and Unlock
        in a multi-threaded environment. Otherwise, the Lock and
        Unlock methods do nothing. Note that setting this
        property is done automatically if this packet has been
        created by the Session class and is processed by a related
        SmartInspect object which has one or more connections which
        operate in asynchronous protocol mode.

        Setting this property must be done before using this packet
        from multiple threads simultaneously.
        """
        return self.__fThreadSafe
            
    @ThreadSafe.setter
    def ThreadSafe(self, value:bool):
        """
        Sets the ThreadSafe property value.
        """
        # if set to same value, then leave the lock object as it is.
        if (value == self.__fThreadSafe):
            return

        # set thread-safe mode.
        self.__fThreadSafe = value

        # if thread-safe requested (true), then create a new lock object.
        if (value):

            self.__fLock = _threading_local.RLock()

        # otherwise, just leave the lock object as it is since it will not be used.
        # note that the Lock and Unlock only use the lock object if thread-safe is true!


    @staticmethod
    def GetThreadId() -> int:
        """
        Returns the ID of the current thread.
        
        The ID the current thread or 0 if the caller does not have
        the required permissions to retrieve the ID of the current thread.
        
        This method is intended to be used by derived packet classes
        which make use of a thread ID. Please note that this method
        catches any SecurityException and returns 0 in this case.
        """	
        threadId:int = 0

        try:
            threadId = _thread.get_ident()
        except:
            threadId = 0

        return threadId


    @staticmethod
    def GetProcessId() -> int:
        """
        Returns the ID of the current process.

        The ID the current process or 0 if the caller does not have
        the required permissions to retrieve the ID of the current
        process.

        This method is intended to be used by derived packet classes
        which make use of a process ID. Please note that this method
        catches any SecurityException and returns 0 in this case.
        """	
        processId:int = 0

        try:
            processId = os.getpid()
        except:
            processId = 0

        return processId


    @staticmethod
    def GetStringSize(value:str) -> int:
        """
        Returns the memory size occupied by the supplied string or 0 if the
        supplied argument is null.

        Args:
            value (str):
                String value to get the size of.

        This method calculates and returns the total memory size
        occupied by the supplied string. if the supplied argument
        is null, 0 is returned.
        """
        if (value == None):
            return 0
        else:
            return len(value) * 2


    def Lock(self) -> None:
        """
        Locks this packet for safe multi-threaded packet processing
        if this packet is operating in thread-safe mode.
        
        Call this method before reading or changing properties of a
        packet when using this packet from multiple threads at the
        same time. This is needed, for example, when one or more
        SmartInspect.Connections of a SmartInspect object are told 
        to operate in Protocol.IsValidOption.  Each Lock call must 
        be matched by a call to Unlock.
        
        Before using Lock and Unlock in a multi-threaded environment
        you must indicate that this packet should operate in
        thread-safe mode by setting the ThreadSafe property to true.
        Otherwise, the Lock and Unlock methods do nothing. Note
        that setting the ThreadSafe property is done automatically
        if this packet has been created by the Session class and is
        processed by a related SmartInspect object which has one or
        more connections which operate in asynchronous protocol mode.
        """
        if (self.__fThreadSafe):

            # get lock to synchronize threads.
            self.__fLock.acquire()


    def Unlock(self) -> None:
        """
        Unlocks a previously locked packet.
        
        Call this method after reading or changing properties of a
        packet when using this packet from multiple threads at the
        same time. This is needed, for example, when one or more
        SmartInspect.Connections of a SmartInspect object are told to 
        operate in Protocol.IsValidOption.  Each Unlock call must be 
        matched by a previous call to Lock.
        
        Before using Lock and Unlock in a multi-threaded environment
        you must indicate that this packet should operate in
        thread-safe mode by setting the ThreadSafe property to true.
        Otherwise, the Lock and Unlock methods do nothing. Note
        that setting the ThreadSafe property is done automatically
        if this packet has been created by the Session class and is
        processed by a related SmartInspect object which has one or
        more connections which operate in asynchronous protocol mode.
        """
        if (self.__fThreadSafe):

            # free lock to release next thread.
            self.__fLock.release()
