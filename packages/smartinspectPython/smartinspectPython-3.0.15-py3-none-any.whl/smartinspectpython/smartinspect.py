"""
Module: smartinspect.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description      |
| ---------- | ----------- | -----------------|
| 2023/05/30 | 3.0.0.0     | Initial Version. | 
| 2023/06/09 | 3.0.8.0     | Added InfoEvent event and RaiseInfoEvent method to convey SI informational events to interested parties (e.g. Si Console Server banner, etc).

</details>
"""

import socket
import _threading_local
from datetime import datetime

# our package imports.
from .smartinspectexception import SmartInspectException
from .dotnetcsharp import ArgumentNullException
from .invalidconnectionsexception import InvalidConnectionsException
from .loadconnectionsexception import LoadConnectionsException
from .loadconfigurationexception import LoadConfigurationException
from .erroreventargs import ErrorEventArgs
from .infoeventargs import InfoEventArgs
from .filtereventargs import FilterEventArgs
from .logentryeventargs import LogEntryEventArgs
from .logentry import LogEntry
from .watcheventargs import WatchEventArgs
from .watch import Watch
from .processfloweventargs import ProcessFlowEventArgs
from .processflow import ProcessFlow
from .controlcommandeventargs import ControlCommandEventArgs
from .controlcommand import ControlCommand
from .packet import Packet
from .level import Level as SILevel
from .protocol import Protocol
from .protocolfactory import ProtocolFactory
from .protocolcommand import ProtocolCommand
from .protocolvariables import ProtocolVariables
from .connectionsparser import ConnectionsParser, ConnectionFoundEventArgs
from .configuration import Configuration
from .sessionmanager import SessionManager
from .sessiondefaults import SessionDefaults
from .utils import Event
from .session import Session

# our package constants.
from .const import (
    VERSION
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class SmartInspect:
    """
    The SmartInspect class is the most important class in the SmartInspect Python3 library. An instance of this class is able
    to write log messages to a file or to send them directly to the SmartInspect Console using TCP. You can control these
    connections by setting the Connections property. 
    
    The SmartInspect class offers several properties for controlling the logging behavior. Besides the Connections property there
    is the Enabled property which controls if log messages should be sent or not. Furthermore, the AppName property specifies the
    application name displayed in the SmartInspect Console. And last but not least, we have the Level and DefaultLevel properties
    which specify the log level of an SmartInspect object and its related sessions.
    
    Additionally, the SmartInspect class acts as parent for sessions, which contain the actual logging methods, like, for
    example, Session.LogMessage or Session.LogObject. It is possible and common that several different sessions have the same parent
    and thus share the same connections. The Session class contains dozens of useful methods for logging any kind of data. Sessions
    can even log variable watches, generate illustrated process and thread information or control the behavior of the SmartInspect
    Console. It is possible, for example, to clear the entire log in the Console by calling the Session.ClearLog method.
    
    To accomplish these different tasks the SmartInspect concept uses several different packets. The SmartInspect class manages these
    packets and logs them to its connections. It is possibility to register event handlers for every packet type which are called
    after a corresponding packet has been sent.
    
    The error handling in the SmartInspect Python3 library is a little bit different than in other libraries. This library uses
    an event, the Error event, for reporting errors. We've chosen this way because a logging framework should not alter the behavior
    of an application by firing exceptions. The only exception you need to handle can be thrown by the Connections property if the
    supplied SmartInspect.Connections contains errors.
    
    Threadsafety:
        This class is fully thread-safe.
    """

    def __init__(self, appName:str) -> None:
        """
        Initializes a new instance of the class.

        Args:
            appName (str):
                The application name used for Log Entries. It is usually set to the name of the application which creates this object.
        """
        # initialize instance.
        self.__fLock = _threading_local.RLock()
        self.__fHostName:str = ""
        self.__fAppName:str = appName
        self.__fConnections:str = ""
        self.__fEnabled:bool = False
        self.__fIsMultiThreaded:bool = False
        self.__fLevel:SILevel = SILevel.Debug
        self.__fDefaultLevel:SILevel = SILevel.Message
        self.__fProtocols = []
        self.__fVariables:ProtocolVariables = ProtocolVariables()
        self.__fSessions:SessionManager = SessionManager()

        try:

            # Try to get the NetBIOS name of this machine.
            self.__fHostName = socket.gethostname()

        except:

            # we couldn't get the NetBIOS name of this machine,
            # so we set the HostName to an empty string.
            self.__fHostName = ""

        # define all events raised by this class.
        self.ErrorEvent = Event()
        """
        Event raised when an error occurs in SmartInspect processing.
        """
        self.FilterEvent = Event()
        """
        Event raised to allow packet filtering before a packet is sent to the protocol destination.
        """
        self.InfoEvent = Event()
        """
        Event raised when an informational event occurs in SmartInspect processing.
        """
        self.LogEntryEvent = Event()
        """
        Event raised when a Log Entry packet is sent to the protocol destination.
        """
        self.WatchEvent = Event()
        """
        Event raised when a Watch packet is sent to the protocol destination.
        """
        self.ProcessFlowEvent = Event()
        """
        Event raised when a Process Flow packet is sent to the protocol destination.
        """
        self.ControlCommandEvent = Event()
        """
        Event raised when a Control Command packet is sent to the protocol destination.
        """

        # wire up event handlers.
        self.ErrorEvent += self.OnErrorEvent
        self.InfoEvent += self.OnInfoEvent
        self.FilterEvent += self.OnFilterEvent
        self.LogEntryEvent += self.OnLogEntryEvent
        self.WatchEvent += self.OnWatchEvent
        self.ProcessFlowEvent += self.OnProcessFlowEvent
        self.ControlCommandEvent += self.OnControlCommandEvent


    def __del__(self):
        """
        Deletes an instance of the class.
        """


    @property
    def AppName(self) -> str:
        """ 
        Gets the AppName property value.

        Returns:
            The application name used for the Log Entries.

        The application name helps you to identify Log Entries from different applications in the SmartInspect Console. 
        If you set this property to null, the application name will be empty when sending Log Entries.
        """
        return self.__fAppName
    

    @AppName.setter
    def AppName(self, value:str) -> None:
        """ 
        Sets the AppName property value.
        """
        if value == None:
            self.__fAppName = ""
        else:
            self.__fAppName = value

        self.__UpdateProtocols()


    @property
    def Connections(self) -> str:
        """
        Gets the Connections property value.

        Returns:
            A connection string that contains all connections used by this SmartInspect instance.

        Raises:
            InvalidConnectionsException:
                Invalid syntax, unknown protocols or inexistent options.
        
        You can set multiple connections by separating the connections with commas. A connection consists of a protocol
        identifier like "file" plus optional protocol parameters in parentheses. If you, for example, want to log to a file, the
        Connections property must be set to "file()". You can specify the filename in the parentheses after the protocol identifier
        like this: "file(filename=\\"c:\\mylogfile.sil\\")". Please note that if the Enabled property is set to true, the connections
        try to connect to their destinations immediately. By default, no connections are used.

        See the Protocol class for a list of available protocols and ProtocolFactory for a way to add your own custom protocols.
        Furthermore have a look at the LoadConnections and LoadConfiguration methods, which can load a connections string from a file. 
        Also, for a class which assists in building connections strings, please refer to the documentation of the ConnectionsBuilder class.

        To automatically replace placeholders in the given connections string, you can use so called connection variables. Please
        have a look at the SetVariable method for more information.

        Please note that an InvalidConnectionsException exception is thrown if an invalid connections string is supplied.

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sessionref.md
        # log messages to default file 'log.sil'.
        SiAuto.Si.Connections = 'file()'

        # log messages to file 'mylog.sil'.
        SiAuto.Si.Connections = "file(filename=""mylog.sil"", append=true)"

        # log messages to default file "log.sil", as well as to the SmartInspect 
        # Console viewer running on localhost.
        SiAuto.Si.Connections = "file(append=true), tcp(host=""localhost"")"

        # log messages to default file "log.sil", as well as to file "anotherlog.sil".
        SiAuto.Si.Connections = "file(), file(filename=""anotherlog.sil"")"
        ```
        </details>
        """
        return self.__fConnections


    @Connections.setter
    def Connections(self, value:str) -> None:
        """ 
        Sets the Connections property value.
        """
        with self.__fLock:

            try:

                self.__ApplyConnections(value)

            except Exception as ex:

                self.__RaiseErrorEvent(ex)


    @property
    def DefaultLevel(self) -> SILevel:
        """ 
        Gets the DefaultLevel property value.

        Returns:
            The default log level of this SmartInspect instance and its related sessions.

        The DefaultLevel property of this SmartInspect instance represents the default log level used by its corresponding
        sessions. The default value of this property is Level.Message.

        Every method in the Session class which makes use of the parent's Level and does not take a Level argument, uses the 
        default level of its parent as log level.
        """
        return self.__fDefaultLevel
    

    @DefaultLevel.setter
    def DefaultLevel(self, value:SILevel) -> None:
        """ 
        Sets the DefaultLevel property value.
        """
        if value != None:
            self.__fDefaultLevel = value


    @property
    def Enabled(self) -> bool:
        """ 
        Gets the Enabled property value.

        Returns:
            The logging Enabled status.

        This property allows you to control if anything should be logged at all.

        If you set this property to true, all connections will try to connect to their destinations. For example, if the
        Connections property is set to "file(filename=c:\\log.sil)", the file "c:\\log.sil" will be opened to write all following
        packets to it. By setting this property to false, all connections will disconnect.
        
        Additionally, every Session method evaluates if its parent is enabled and returns immediately if this is not the case.
        This guarantees that the performance hit is minimal when logging is disabled. The default value of this property is
        false. You need to set this property to true before you can use the SmartInspect instance and its related sessions.

        Please note: If one or more connections of this SmartInspect object operate in Protocol.IsValidOption
        you must disable this object by setting this property to false before exiting your application to properly exit
        and cleanup the protocol related threads. Disabling this instance may block until the related protocol threads are
        finished.
        """
        return self.__fEnabled


    @Enabled.setter
    def Enabled(self, value:bool) -> None:
        """ 
        Sets the Enabled property value.
        """
        with self.__fLock:

            if (value):
                self.__Enable()
            else:
                self.__Disable()


    @property
    def HostName(self) -> str:
        """ 
        Gets the HostName property value.

        Returns:
            Returns the hostname of the current machine. 

        The hostname helps you to identify Log Entries from different machines in the SmartInspect Console.
        The value of this property is derived from the "socket.gethostname()" module method.
        """
        return self.__fHostName
    

    @property
    def Level(self) -> SILevel:
        """ 
        Gets the Level property value.

        Returns:
            Returns the log level of this SmartInspect instance and its related sessions.

        The Level property of this SmartInspect instance represents the log level used by its corresponding sessions to determine
        if information should be logged or not. The default value of this property is Level.Debug.

        Every method (except the Clear method family) in the Session class tests if its log level equals or is greater than the
        log level of its parent. If this is not the case, the methods return immediately and won't log anything.

        The log level for a method in the Session class can either be specified explicitly by passing a Level argument or implicitly
        by using the DefaultLevel. Every method in the Session class which makes use of the parent's log level and does not take a 
        Level argument, uses the DefaultLevel of its parent as log level.

        For more information about the default level, please refer to the documentation of the DefaultLevel property.
        """
        return self.__fLevel
    

    @Level.setter
    def Level(self, value:SILevel) -> None:
        """ 
        Sets the Level property value.
        """
        if value != None:
            self.__fLevel = value


    @property
    def SessionDefaults(self) -> SessionDefaults:
        """
        Gets the SessionDefaults property value.

        Returns:
            The default property values for new sessions.

        This property lets you specify the default property values for new sessions which will be created by or passed to the
        AddSession method. Please see the AddSession method for more information. For information about the available session
        properties, please refer to the documentation of the Session class.
        """
        return self.__fSessions.Defaults


    # TODO - how to ?
    #def ???(self, sessionName:str) -> Session:
    #    """
    #    Gets the session associated with the specified session name.
    #    /// </summary>
    #    /// <param name="sessionName">
    #    The name of the session to lookup and return. Not allowed to
    #    be null.
    #    /// 
    #    /// <returns>
    #    The requested session or null if the supplied sessionName is
    #    null or if the session is unknown.
    #    /// </returns>
    #    
    #    This indexer returns the session which has previously been
    #    added with the AddSession method and can be identified by the
    #    specified session name. If the specified session is unknown
    #    or the sessionName parameter is null, null is returned. See
    #    the GetSession method for more information.
    #    """
    #    public Session? this[string sessionName]
    #    {
    #        get { return self.__fSessions.Get(sessionName); }
    #    }


    ###################################################################################
    # Internal methods follow after this.
    # NOTE - Keep them in alphabetical order for Documentation generator!
    ###################################################################################


    def __AddConnection(self, sender:object, e:ConnectionFoundEventArgs) -> None:
        """
        Handles the ConnectionsParser.ConnectionFoundEvent event, which is raised
        when a new protocol connection string is found and about to be processed.

        Args:
            sender (object):
                The object which fired the event.
            e (ConnectionFoundEventArgs):
                Arguments that contain detailed information related to the event.
        """
        protocol:Protocol = ProtocolFactory.GetProtocol(e.Protocol, e.Options)
        if (protocol != None):

            # wire up events.   
            protocol.ErrorEvent += self.ProtocolErrorEvent
            protocol.InfoEvent += self.ProtocolInfoEvent

            # add the new instance to our active protocols list.
            self.__fProtocols.append(protocol)

            if (protocol.Asynchronous):
                self.__fIsMultiThreaded = True

            # assign common properties to the protocol.
            protocol.AppName = self.__fAppName
            protocol.HostName = self.__fHostName


    def __ApplyConfiguration(self, config:Configuration) -> None:
        """
        Applies (or enables) a loaded configuration.

        Args:
            config (Configuration):
                The configuration to apply.
        """
        if (config.Contains("appname")):
            self.__fAppName = config.ReadString("appname", self.__fAppName)

        # The `enabled' configuration value needs to be handled special,
        # because its appearance and value have a direct impact on how
        # to treat the `connections' value and the order in which to
        # apply the values:
        
        # If the `enabled' value is found, it is very important to
        # differentiate between the values true and false. If the
        # `enabled' value is false, the user obviously either wants
        # to disable this object or keep it disabled. To correctly
        # disable this SmartInspect instance, we need to do that before
        # the connections string is changed. Otherwise it can happen
        # that this SmartInspect instance temporarily uses the new
        # connections string (exactly in the case when it is already
        # enabled).
        
        # Handling an `enabled' value of true is the other way round.
        # We cannot enable this SmartInspect instance before setting
        # the `connections' value, because this would cause this
        # SmartInspect instance to temporarily use its old connections string

        connections:str = config.ReadString("connections", "")
        if (connections == None) or (len(connections) == 0):
            return

        if (config.Contains("enabled")):
        
            enabled:bool = config.ReadBoolean("enabled", False)
            if (enabled):
                self.__TryConnections(connections)
                self.__Enable()
            else:
                self.__Disable()
                self.__TryConnections(connections)

        else:

            self.__TryConnections(connections)

        if (config.Contains("level")):
            self.__fLevel = config.ReadLevel("level", self.__fLevel)

        if (config.Contains("defaultlevel")):
            self.__fDefaultLevel = config.ReadLevel("defaultlevel", self.__fDefaultLevel)


    def __ApplyConnections(self, connections:str) -> None:
        """
        Method called when the Connections property is set with a new value.

        Args:
            connections (str):
                Connections string to load.

        Raises:
            ArgumentNullException:
                The connections argument is null.

        This will remove any existing connections, replacing it / them with the 
        new connection(s) specified.
        """
        # first remove the old connections.
        self.__RemoveConnections()

        if (connections != None):

            # create the new connections and assign the connections string.
            self.__CreateConnections(connections)
            self.__fConnections = connections

            # if this instance is currently enabled, then try to connect now.
            if (self.__fEnabled):
                self.__Connect()


    def __Connect(self) -> None:
        """
        Call the Connect method of all active protocol objects. 
        If an error occurs, then we raise the Error event.
        """
        for p in self.__fProtocols:

            if (p != None):

                try:

                    p.Connect()

                except Exception as ex:

                    self.__RaiseErrorEvent(ex)


    def __CreateConnections(self, connections:str) -> None:
        """
        Processes a new connections string value, and creates a new protocol
        class to process the connection.

        Args:
            connections (str):
                The connections string to process.

        Raises:
            InvalidConnectionsException:
                Thrown if the connections string could not be processed.
        """
        self.__fIsMultiThreaded = False

        parser:ConnectionsParser = None

        try:
            
            # expand the connections string with previously set connection variables,
            # wire up events, and parse the connections string.
            parser = ConnectionsParser()
            parser.ConnectionFoundEvent += self.__AddConnection
            parser.Parse(self.__fVariables.Expand(connections))
            
        except Exception as ex:
            
            self.__RemoveConnections()
            raise InvalidConnectionsException(ex)

        finally:
            if (parser != None):
                parser.ConnectionFoundEvent.unhandle_all()


    def __Disable(self) -> None:
        """
        Disables all active protocols by calling their Disconnect methods.
        """
        if (self.__fEnabled):
            self.__Disconnect()
            self.__fEnabled = False


    def __Disconnect(self) -> None:
        """
        Call the Disconnect method of all active protocol objects. 
        If an error occurs, then we raise the Error event.
        """
        for p in self.__fProtocols:

            if (p != None):

                try:

                    p.Disconnect()

                except Exception as ex:

                    self.__RaiseErrorEvent(ex)


    def __Enable(self) -> None:
        """
        Enables all active protocols by calling their Connect methods.
        """
        if (not self.__fEnabled):
            self.__Connect()
            self.__fEnabled = True


    def __FindProtocol(self, caption:str) -> Protocol:
        """
        Searches the list of active protocols for the specified Caption string.
        
        Args:
            caption (str):
                Caption to search for.

        Returns:
            The associated protocol object if found; otherwise null.
        """
        if (caption == None):
            return None

        caption = caption.lower()

        for p in self.__fProtocols:

            if (p != None):

                if (p.Caption.lower() == caption):
                    return p

        return None


    def __ProcessPacket(self, packet:Packet) -> None:
        """
        Iterate through all available connections and write the packet. 

        Args:
            packet
                Packet to write.
        """
        with self.__fLock:
        
            # we do not use an enumerator for performance reasons here. This 
            # saves one created object for each packet.
            for i in range(len(self.__fProtocols)):

                p:Protocol = self.__fProtocols[i]
                if (p != None):
                
                    try:

                        p.WritePacket(packet)

                    except Exception as ex:

                        self.__RaiseErrorEvent(ex)


    def __RaiseControlCommandEvent(self, controlCommand:ControlCommand) -> None:
        """
        Raises the ControlCommandEvent event with ControlCommand item details.

        Args:
            controlCommand
                The ControlCommand item that was processed.

        This method is used to inform interested parties that a ControlCommand item was just processed.
        """
        try:

            # raise event.
            args:ControlCommandEventArgs = ControlCommandEventArgs(controlCommand)
            self.ControlCommandEvent(self, args)

        except Exception as ex:

            # ignore exceptions.
            pass


    def __RaiseErrorEvent(self, ex:Exception) -> None:
        """
        Raises the Error event with previously caught exception details.

        Args:
            ex (Exception):
                The exception that caused the event.

        This method is used to inform interested parties that an Error has occured.
        """
        try:

            # raise event.
            args:ErrorEventArgs = ErrorEventArgs(ex)
            self.ErrorEvent(self, args)

        except Exception as ex:

            # ignore exceptions.
            pass


    def __RaiseFilterEvent(self, packet:Packet) -> bool:
        """
        Raises the FilterEvent event with packet details.

        Args:
            packet
                The packet which is about to be processed.

        This method is used to inform interested parties that a Packet is about
        to be processed, and optionally allows them to cancel processing of the packet.

        Returns:
            True if the supplied packet shall be filtered and thus not be sent;
            Otherwise, false.
        """
        try:

            # raise event.
            args:FilterEventArgs = FilterEventArgs(packet)
            self.FilterEvent(self, args)
            return args.Cancel

        except Exception as ex:

            # ignore exceptions.
            return False


    def __RaiseLogEntryEvent(self, logEntry:LogEntry) -> None:
        """
        Raises the LogEntryEvent event with LogEntry item details.

        Args:
            logEntry
                The LogEntry item that was processed.

        This method is used to inform interested parties that a LogEntry item was just processed.
        """
        try:

            # raise event.
            args:LogEntryEventArgs = LogEntryEventArgs(logEntry)
            self.LogEntryEvent(self, args)

        except Exception as ex:

            # ignore exceptions.
            pass


    def __RaiseProcessFlowEvent(self, processFlow:ProcessFlow) -> None:
        """
        Raises the ProcessFlowEvent event with ProcessFlow item details.

        Args:
            processFlow
                The ProcessFlow item that was processed.

        This method is used to inform interested parties that a ProcessFlow item was just processed.
        """
        try:

            # raise event.
            args:ProcessFlowEventArgs = ProcessFlowEventArgs(processFlow)
            self.ProcessFlowEvent(self, args)

        except Exception as ex:

            # ignore exceptions.
            pass


    def __RaiseWatchEvent(self, watch:Watch) -> None:
        """
        Raises the WatchEvent event with Watch item details.

        Args:
            watch
                The Watch item that was processed.

        This method is used to inform interested parties that a Watch item was just processed.
        """
        try:

            # raise event.
            args:WatchEventArgs = WatchEventArgs(watch)
            self.WatchEvent(self, args)

        except Exception as ex:

            # ignore exceptions.
            pass


    @staticmethod
    def __ReadConnections(fileName:str) -> str:
        """
        Reads the connections string value from the specified file name.

        Args:
            fileName (str):
                Filename that contains the connections string.

        Returns:
            The connections string from the file.

        Raises:
            LoadConnectionsException:
                Thrown if the specified file does not contain a connections string.
        """
        config:Configuration = Configuration()

        try:

            # load the config file, and see if it has a connection string defined.
            # if so, then return the connection string.
            config.LoadFromFile(fileName)

            if (config.Contains("connections")):

                value:str = config.ReadString("connections", "")
                if (value != None) and (len(value) > 0):
                    return value

        finally:
            
            config.Clear()
            
        # otherwise raise an exception.
        raise LoadConnectionsException("Connections string was not found.", fileName)


    def __RemoveConnections(self) -> bool:
        """
        Calls the Disconnect method of all active protocol objects and clears the connections collection.
        """

        self.__Disconnect()
        self.__fIsMultiThreaded = False
        self.__fProtocols.clear()
        self.__fConnections = ""


    def __TryConnections(self, connections:str) -> bool:
        """
        Tries to apply a newly detected connections string.

        Args:        
            connections (str):
                The connections string to activate.

        Returns:
            True if the connections were activated successfully; otherwise, false.
        """
        result:bool = False

        if (connections != None):

            try:

                self.__ApplyConnections(connections)
                result = True

            except Exception as ex:

                self.__RaiseErrorEvent(ex)

        return result


    def __UpdateProtocols(self) -> None:
        """
        Updates the AppName and HostName properties of active protocols.
        This method is called when the AppName value changes.
        """
        with self.__fLock:

            for p in self.__fProtocols:

                p.AppName = self.__fAppName
                p.HostName = self.__fHostName


    def __UpdateSession(self, session:Session, toName:str, fromName:str) -> None:
        """
        Updates an entry in the internal lookup table of sessions.

        Args:
            session (Session):
                The session whose name has changed and whose entry should be updated.
            toName (str):
                The new name of the session.
            fromName (str):
                The old name of the session.

        Once the name of a session has changed, this method is called
        to update the internal session lookup table. The 'to' argument
        specifies the new name and 'from' the old name of the session.
        After this method returns, the new name can be passed to the
        GetSession method to lookup the supplied session.
        """
        self.__fSessions.Update(session, toName, fromName)


    ###################################################################################
    # Public methods follow after this.
    # NOTE - Keep them in alphabetical order for Documentation generator!
    ###################################################################################


    def AddSession(self, sessionName:str, store:bool=False) -> Session:
        """
        Adds and returns a new Session instance with this SmartInspect
        object set as parent and optionally saves it for later access.

        Args:
            sessionName (str):
                The name for the new session. Not allowed to be null.
            store (bool):
                Indicates if the newly created session should be stored 
                for later access.

        Returns:
            The new Session instance or null if the supplied sessionName
            parameter is null.

        Raises:
            ArgumentNullException:
                Thrown if sessionName is null or empty string.

        This method allocates a new session with this SmartInspect 
        instance set as parent and the supplied sessionName parameter
        set as session name. The returned session will be configured 
        with the default session properties as specified by the
        SessionDefaults property. This default configuration can be 
        overridden on a per-session basis by loading the session
        configuration with the LoadConfiguration method. Please see 
        the LoadConfiguration documentation for details.

        If the 'store' parameter is true, the created and returned 
        session is stored for later access and can be retrieved with
        the GetSession method. To remove a created session from the 
        internal list, call the DeleteSession method. 

        If this method is called multiple times with the same session 
        name, then the GetSession method operates on the session which
        got added last. If the sessionName parameter is null, this method 
        does nothing and returns null as well.
        """
        if (sessionName == None) or (len(sessionName) == 0):
            raise ArgumentNullException("sessionName")

        session:Session = Session(self, sessionName)
        self.__fSessions.Add(session, store)
        return session


    def AddSessionObject(self, session:Session) -> Session:
        """
        Adds an existing Session instance to the internal
        list of sessions and saves it for later access.

        Args:
            session (Session):
                The session to store.

        This method adds the passed session to the internal list of
        sessions and saves it for later access. The passed session
        will be configured with the default session properties as
        specified by the SessionDefaults property. This default
        configuration can be overridden on a per-session basis by
        loading the session configuration with the LoadConfiguration
        method. Please see the LoadConfiguration documentation for
        details.

        The passed session can later be retrieved with the GetSession
        method. To remove an added session from the internal list,
        call the DeleteSession method.
        """
        self.__fSessions.Add(session, True)
        return session


    def DeleteSession(self, session:Session) -> None:
        """
        Removes a session from the internal list of sessions.

        Args:
            session (Session):
                The session to remove from the lookup table of sessions.
        
        This method removes a session which has previously been added
        with and returned by the AddSession method. After this method
        returns, the GetSession method returns null when called with
        the same session name unless a different session with the same
        name has been added.
        
        This method does nothing if the supplied session argument is null.
        """
        self.__fSessions.Delete(session)


    def Dispatch(self, caption:str, action:int, state:object) -> None:
        """
        Executes a custom protocol action of a connection.
        
        Args:
            caption (str):
                The identifier of the connection. Not allowed to be null.
            action (int):
                The action to execute by the requested connection.
            state (object):
                An optional object which encapsulates additional protocol
                specific information about the custom action. Can be null.

        This method dispatches the action and state parameters to the 
        connection identified by the caption argument. If no
        suitable connection can be found, the Error event is used. The Error
        event is also used if an exception is thrown in
        the custom protocol action.

        The SmartInspect Python3 library currently implements one custom 
        protocol action in MemoryProtocol. The MemoryProtocol class
        is used for writing log packets to memory. On request, it can 
        write its internal queue of packets to a user-supplied
        stream or Protocol object with a custom protocol action.

        The request for executing the custom action and writing the 
        queue can be initiated with this Dispatch method. 

        For more information about custom protocol actions, please refer 
        to the Protocol.Dispatch method. Also have a look at the 
        Protocol.IsValidOption method which explains how to set the caption 
        of a connection.

        Please note that the custom protocol action is executed asynchronously
        if the requested connection operates in Protocol.IsValidOption

        If the supplied caption argument is null, this method does nothing and 
        returns immediately.
        """
        if (caption == None):
            return

        with self.__fLock:
        
            try:

                p:Protocol = self.__FindProtocol(caption)

                if (p == None):
                    raise SmartInspectException(str.format("No protocol could be found with the specified caption of \"{0}\".  Valid captions are: tcp|file|text|mem|pipe.", caption))

                p.Dispatch(ProtocolCommand(action, state))
            
            except Exception as ex:

                self.__RaiseErrorEvent(ex)


    def Dispose(self, disposing:bool=True) -> None:
        """
        Releases all resources of this SmartInspect object.

        Args:
            disposing
                True to dispose of both managed and unmanaged resources.

        This method disconnects and removes all internal connections
        and disables this instance. Moreover, all previously stored
        sessions will be removed.
        """

        # Here, we simply call the Dispose method of
        # all protocol objects in our collection. If an
        # error occurs we call the Error event.

        if (self.__fProtocols != None):
        
            for i in range(len(self.__fProtocols)):

                p:Protocol = self.__fProtocols[i]
                if (p != None):

                    try:

                        p.Dispose()

                    except Exception as ex:

                        self.__RaiseErrorEvent(ex)

        if (disposing):

            try:
         
                with self.__fLock:

                    self.__fEnabled = False
                    self.__RemoveConnections()

                self.__fSessions.Clear()

            finally:

                # unwire events.
                if (self.ErrorEvent != None):
                    self.ErrorEvent.unhandle_all()
                if (self.InfoEvent != None):
                    self.InfoEvent.unhandle_all()
                if (self.FilterEvent != None):
                    self.FilterEvent.unhandle_all()
                if (self.LogEntryEvent != None):
                    self.LogEntryEvent.unhandle_all()
                if (self.WatchEvent != None):
                    self.WatchEvent.unhandle_all()
                if (self.ProcessFlowEvent != None):
                    self.ProcessFlowEvent.unhandle_all()
                if (self.ControlCommandEvent != None):
                    self.ControlCommandEvent.unhandle_all()


    def GetSession(self, sessionName:str=None) -> Session:
        """
        Returns a previously added session.

        Args:
            sessionName (str):
                The name of the session to lookup and return. 
                Not allowed to be null.

        Raises:
            ArgumentNullException:
                Thrown if sessionName is null.

        Returns:
            The requested session or null if the supplied sessionName is unknown.
        
        This method returns a session which has previously been
        added with the AddSession method and can be identified by
        the supplied sessionName argument. If the requested session
        is unknown then this method returns null.

        Note that the behavior of this method can be unexpected in
        terms of the result value if multiple sessions with the same
        name have been added. In this case, this method returns the
        session which got added last and not necessarily the session
        which you expect. 

        Adding multiple sessions with the same name should therefore
        be avoided.
        """
        return self.__fSessions.Get(sessionName)


    def GetVariable(self, key:str) -> str:
        """
        Returns the value of a connection variable.

        Args:
            key (str):
                The key of the connection variable.

        Returns:
            The value for the given connection variable or null if the
            connection variable is unknown.

        Please see the SetVariable method for more information
        about connection variables.
        """
        if (key == None):
            return None
        return self.__fVariables.Get(key)


    def LoadConfiguration(self, fileName:str) -> None:
        """
        Loads the properties and sessions of this SmartInspect instance
        from a configuration file.

        Args:
            fileName (str):
                The name of the file to load the configuration from.
        
        This method loads the properties and sessions of this SmartInspect object from a file. This file should be a plain
        text file containing key/value pairs. Each key/value pair is expected to be on its own line. Empty, unrecognized lines and
        lines beginning with a ';' character are ignored.

        The Error event is used to notify the caller if an error occurs while trying to load the configuration from the
        specified file. Such errors include I/O errors like trying to open a file which does not exist, for example.

        The Error event is also used if the specified configuration file contains an invalid connections string. In this case, an
        instance of the InvalidConnectionsException exception type is passed to the Error event.

        Calling this method with the fileName parameter set to null has no effect.

        This method is useful for loading the properties and sessions of this SmartInspect instance after the deployment of an
        application. A typical use case for this method is the following scenario: imagine a customer who needs to send a log file to
        customer service to analyze a software problem. If the software in question uses this LoadConfiguration method, the customer
        service just needs to send a prepared configuration file to the customer. Now, to load the SmartInspect properties from a
        file, the customer now just needs to drop this file to the application's installation directory or any other predefined location.

        To monitor a SmartInspect configuration file for changes, please have a look at the ConfigurationTimer class.

        To automatically replace placeholders in a loaded connections string, you can use so called connection variables. Please
        have a look at the SetVariable method for more information.

        The following table lists the recognized configuration values, the corresponding SmartInspect properties and their types:

        Value         |  Property (Type)
        --------------|  ------------------------
        appname       |  AppName (string)
        connections   |  Connections (string)
        defaultlevel  |  DefaultLevel (Level)
        enabled       |  Enabled (bool)
        level         |  Level (Level)

        In addition to these properties, this method also configures any stored sessions of this SmartInspect object. Sessions that
        have been stored or will be added with the AddSession method will be configured with the properties of the related session
        entry of the passed configuration file. Please see the example section for details on how sessions entries look like.

        If no entries can be found in the configuration file for a newly added session, this session will use the default session
        properties. The default session properties can also be specified in the configuration file. Please note that the
        session defaults do not apply to the main session SiAuto.Main since this session has already been added before a
        configuration file can be loaded. The session defaults only apply to newly added sessions and do not affect existing sessions.

        The case of the configuration properties doesn't matter. This means, it makes no difference if you specify 'defaultlevel'
        or 'DefaultLevel' as key, for example.

        For a typical configuration file, please see the example below.

        To support Unicode strings, both the LoadConnections and LoadConfiguration methods are capable of auto-detecting the
        string encoding if a BOM (Byte Order Mark) is given at the start of the file. The following table lists the supported
        encodings and the corresponding BOM identifiers.

        Encoding               | BOM identifier
        -------------------    | ---------------
        UTF8                   | 0xEF, 0xBB, 0xBF
        Unicode                | 0xFF, 0xFE
        Unicode big-endian     | 0xFE, 0xFF
        
        If no BOM is given, the text is assumed to be in the ASCII format. If the configuration file has been created or edited
        with the SmartInspect Configuration Builder, the file always has a UTF8 Byte Order Mark and Unicode strings are therefore
        handled automatically.

        **Example:**
        ```python
        ; specify the SmartInspect properties.
        connections = file(filename=c:\\log.sil)
        enabled = true
        level = verbose
        defaultlevel = message
        appname = client
        
        ; set defaults for new sessions.
        sessiondefaults.active = false
        sessiondefaults.level = message
        sessiondefaults.colorbg = 0xffff7f
        
        ; configure some individual sessions.
        session.main.level = verbose
        session.client.active = true
        session.client.colorbg = 0x7fffff
        ```
        """
        if (fileName == None):
            return

        config:Configuration = Configuration()

        try:

            try:

                # load the configuration from the specified filename.
                config.LoadFromFile(fileName)

            except Exception as ex:
            
                self.__RaiseErrorEvent(LoadConfigurationException(str(ex), fileName))
                return

            with self.__fLock:

                # apply and enable the loaded configuration.
                self.__ApplyConfiguration(config)

            # load the configuration to the session manager as well.
            self.__fSessions.LoadConfiguration(config)
        
        finally:
        
            config.Clear()


    def LoadConnections(self, fileName:str, doNotEnable:bool=True) -> None:
        """
        Loads the connections string from a file and enables this SmartInspect instance.

        Args:
            fileName (str):
                The name of the file to load the connections string from.
            doNotEnable (bool):
                Specifies if this instance should not be enabled automatically.
                Default value is True.
        
        This method loads the SmartInspect Connections from a file.  This file
        should be a plain text file containing a line like in the following example:

        connections=file(filename=c:\\log.sil)

        Empty, unrecognized lines and lines beginning with a ';' character are ignored. This version of the method enables
        logging automatically.

        The Error event is used to notify the application if the specified file cannot be opened or does not contain a
        connection string.  The Connections and Enabled properties of this instance are not changed if such an error occurs.

        The Error event is also used if a connections string could be read but is found to be invalid. In this case, an instance of
        the InvalidConnectionsException exception type is passed to the Error event.

        If this doNotEnable parameter is set to true, the Enabled property is not changed. Otherwise this SmartInspect
        instance will be enabled. Calling this method with the fileName parameter set to null has no effect.

        This method is useful for customizing the connections string after the deployment of an application. A typical use case
        for this method is the following scenario: imagine a customer who needs to send a log file to customer service to analyze
        a software problem. If the software in question uses this LoadConnections method, the customer service just needs to send
        a prepared connections file to the customer. To enable the logging, the customer now just needs to drop this file to the
        application's installation directory or any other predefined location.

        See LoadConfiguration for a method which is not limited to loading the connections string, but is also capable of loading
        any other property of this object from a file.

        The LoadConnections and LoadConfiguration methods are both capable of detecting the string encoding of the connections
        and configuration files. Please see the LoadConfiguration method for details.

        To automatically replace placeholders in a loaded connections string, you can use so called connection variables. Please
        have a look at the SetVariable method for more information.
        """
        if (fileName == None):
            return

        connections:str = None

        try:
                
            # try to read the connections string.
            connections = SmartInspect.__ReadConnections(fileName)

        except Exception as ex:
            
            # catch exceptions while trying to read the connections
            # string and fire the error event.
            self.__RaiseErrorEvent(ex)

        # if no connections string was found then we are done.
        if (connections == None) or (len(connections) == 0):
            return

        with self.__fLock:
        
            # try to apply the new connections string.  
            # if successful, then enable tracing if specified.
            if (self.__TryConnections(connections)):
                if (not doNotEnable):
                    self.__Enable()


    def Now(self) -> datetime:
        """
        Gets the current date and time.

        Returns:
            The current date and time value via the "datetime.now()" module.
        """
        return datetime.now()


    def OnControlCommandEvent(self, sender:object, e:ControlCommandEventArgs) -> None:
        """
        Method that will handle the SmartInspect.ControlCommandEvent event.
        Inheriting classes can override this method to handle the event.
        
        Args:
            sender (object):
                The object which fired the event.
            e (ControlCommandEventArgs):
                Arguments that contain detailed information related to the event.

        This event can be used if custom processing of ControlCommand
        packets is needed. The event handlers are always called in the
        context of the thread which causes the event.

        If you specified that one or more connections of this SmartInspect object
        should operate in Protocol.IsValidOption, you need to protect the passed
        packet and its data by calling its Packet.Lock and Packet.Unlock methods
        before and after processing.

        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sieventhandlerclass.md
        ```
        </details>
        """
        pass


    def OnErrorEvent(self, sender:object, e:ErrorEventArgs) -> None:
        """
        Method that will handle the SmartInspect.ErrorEvent event.
        Inheriting classes can override this method to handle the event.
        
        Args:
            sender (object):
                The object which fired the event.
            e (ErrorEventArgs):
                Arguments that contain detailed information related to the event.

        This event is fired when an error occurs. An error could be
        a connection problem or wrong permissions when writing log
        files, for example. Instead of throwing exceptions, this event
        is used for error reporting in the SmartInspect Python3 library.

        The event handlers are always called in the context of the
        thread which caused the event. In Protocol.IsValidOption, this
        is not necessarily the thread that initiated the related call.
        
        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sieventhandlerclass.md
        ```
        </details>
        """
        pass


    def OnFilterEvent(self, sender:object, e:FilterEventArgs) -> bool:
        """
        Method that will handle the SmartInspect.FilterEvent event.
        Inheriting classes can override this method to handle the event.
        
        Args:
            sender (object):
                The object which fired the event.
            e (FilterEventArgs):
                Arguments that contain detailed information related to the event.

        Occurs before a packet is processed, and offers the opportunity
        to filter out packets.

        This event can be used if filtering of certain packets is
        needed. The event handlers are always called in the context
        of the thread which causes the event.
        
        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sieventhandlerclass.md
        ```
        </details>
        """
        return e.Cancel


    def OnInfoEvent(self, sender:object, e:InfoEventArgs) -> None:
        """
        Method that will handle the SmartInspect.InfoEvent event.
        Inheriting classes can override this method to handle the event.
        
        Args:
            sender (object):
                The object which fired the event.
            e (InfoEventArgs):
                Arguments that contain detailed information related to the event.

        This event is fired when an informational event occurs. An informational
        event could be the SI console server version, or a configuration
        settings file change, etc.

        The event handlers are always called in the context of the
        thread which caused the event; this is not necessarily the thread 
        that initiated the related call.
        
        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sieventhandlerclass.md
        ```
        </details>
        """
        pass


    def OnLogEntryEvent(self, sender:object, e:LogEntryEventArgs) -> None:
        """
        Method that will handle the SmartInspect.LogEntryEvent event.
        Inheriting classes can override this method to handle the event.
        
        Args:
            sender (object):
                The object which fired the event.
            e (LogEntryEventArgs):
                Arguments that contain detailed information related to the event.

        This event can be used if custom processing of LogEntry
        packets is needed. The event handlers are always called in the
        context of the thread which causes the event.

        If you specified that one or more connections of this SmartInspect object
        should operate in Protocol.IsValidOption, you need to protect the passed
        packet and its data by calling its Packet.Lock and Packet.Unlock methods
        before and after processing.

        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sieventhandlerclass.md
        ```
        </details>
        """
        pass


    def OnProcessFlowEvent(self, sender:object, e:ProcessFlowEventArgs) -> None:
        """
        Method that will handle the SmartInspect.ProcessFlowEvent event.
        Inheriting classes can override this method to handle the event.
        
        Args:
            sender (object):
                The object which fired the event.
            e (ProcessFlowEventArgs):
                Arguments that contain detailed information related to the event.

        This event can be used if custom processing of ProcessFlow
        packets is needed. The event handlers are always called in the
        context of the thread which causes the event.

        If you specified that one or more connections of this SmartInspect object
        should operate in Protocol.IsValidOption, you need to protect the passed
        packet and its data by calling its Packet.Lock and Packet.Unlock methods
        before and after processing.

        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sieventhandlerclass.md
        ```
        </details>
        """
        pass


    def OnWatchEvent(self, sender:object, e:WatchEventArgs) -> None:
        """
        Method that will handle the SmartInspect.WatchEvent event.
        Inheriting classes can override this method to handle the event.
        
        Args:
            sender (object):
                The object which fired the event.
            e (WatchEventArgs):
                Arguments that contain detailed information related to the event.

        This event can be used if custom processing of Watch
        packets is needed. The event handlers are always called in the
        context of the thread which causes the event.

        If you specified that one or more connections of this SmartInspect object
        should operate in Protocol.IsValidOption, you need to protect the passed
        packet and its data by calling its Packet.Lock and Packet.Unlock methods
        before and after processing.

        IMPORTANT: Keep in mind that adding SmartInspect log statements to the event 
        handlers can cause a presumably undesired recursive behavior!

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sieventhandlerclass.md
        ```
        </details>
        """
        pass


    def ProtocolErrorEvent(self, sender:object, e:ErrorEventArgs) -> None:
        """
        Handles the protocol ErrorEvent.

        Args:
            sender (object):
                The object which fired the event.
            e (ErrorEventArgs):
                Arguments that contain detailed information related to the event.
        """
        # This is the error event handler for connections which operate in asynchronous protocol mode. */
        self.__RaiseErrorEvent(e.Exception)


    def ProtocolInfoEvent(self, sender:object, e:InfoEventArgs) -> None:
        """
        Handles the protocol InfoEvent.

        Args:
            sender (object):
                The object which fired the event.
            e (InfoEventArgs):
                Arguments that contain detailed information related to the event.
        """
        self.RaiseInfoEvent(e.Message)


    def RaiseInfoEvent(self, message:str) -> None:
        """
        Raises the Info event with informational message details.

        Args:
            message (str):
                The message that caused the event.

        This method is used to inform interested parties that an Informational event has occured.
        """
        try:

            # raise event.
            args:InfoEventArgs = InfoEventArgs(message)
            self.InfoEvent(self, args)

        except Exception as ex:

            # ignore exceptions.
            pass


    def SendControlCommand(self, controlCommand:ControlCommand) -> None:
        """
        Logs a Control Command.

        Args:
            controlCommand
                The Control Command to log.

        At first, this method determines if the Control Command should
        really be sent by invoking the OnFilter method. If the Control
        Command passes the filter test, it will be logged and the
        SmartInspect.ControlCommand event is fired.
        """

        # Initialize the control command packet for safe multi-threaded
        # access only if this SmartInspect object has one or more
        # connections which operate in asynchronous protocol mode.
        # Also see __CreateConnections.

        if (self.__fIsMultiThreaded):
            controlCommand.ThreadSafe = True

        try:
            
            # are we filtering this entry?  if not, then process the packet.
            if (not self.__RaiseFilterEvent(controlCommand)):

                self.__ProcessPacket(controlCommand)
                self.__RaiseControlCommandEvent(controlCommand)
            
        except Exception as ex:
            
            self.__RaiseErrorEvent(ex)


    def SendLogEntry(self, logEntry:LogEntry) -> None:
        """
        Logs a Log Entry.

        Args:
            logEntry
                The Log Entry to log.

        After setting the application name and hostname of the
        supplied Log Entry, this method determines if the Log
        Entry should really be sent by invoking the OnFilter
        method. If the Log Entry passes the filter test, it will be
        logged and the SmartInspect.LogEntry event is fired.
        """

        # Initialize the log entry packet for safe multi-threaded
        # access only if this SmartInspect object has one or more
        # connections which operate in asynchronous protocol mode.
        # Also see __CreateConnections.

        if (self.__fIsMultiThreaded):
            logEntry.ThreadSafe = True

        # fill the properties we are responsible for.
        logEntry.AppName = self.__fAppName
        logEntry.HostName = self.__fHostName

        try:

            # are we filtering this entry?  if not, then process the packet.
            if (not self.__RaiseFilterEvent(logEntry)):

                self.__ProcessPacket(logEntry)
                self.__RaiseLogEntryEvent(logEntry)

        except Exception as ex:

            self.__RaiseErrorEvent(ex)


    def SendProcessFlow(self, processFlow:ProcessFlow) -> None:
        """
        Logs a Process Flow entry.

        Args:
            processFlow
                The Process Flow entry to log.

        After setting the hostname of the supplied Process Flow entry,
        this method determines if the Process Flow entry should really
        be sent by invoking the OnFilter method. If the Process Flow
        entry passes the filter test, it will be logged and the
        SmartInspect.ProcessFlow event is fired.
        """

        # Initialize the process flow packet for safe multi-threaded
        # access only if this SmartInspect object has one or more
        # connections which operate in asynchronous protocol mode.
        # Also see __CreateConnections.

        if (self.__fIsMultiThreaded):
            processFlow.ThreadSafe = True

        # fill the properties we are responsible for.
        processFlow.HostName = self.__fHostName

        try:
        
            # are we filtering this entry?  if not, then process the packet.
            if (not self.__RaiseFilterEvent(processFlow)):

                self.__ProcessPacket(processFlow)
                self.__RaiseProcessFlowEvent(processFlow)
        
        except Exception as ex:
            
            self.__RaiseErrorEvent(ex)


    def SendWatch(self, watch:Watch) -> None:
        """
        Logs a Watch.
        
        Args:
            watch
                The Watch to log.

        At first, this method determines if the Watch should really
        be sent by invoking the OnFilter method. If the Watch passes
        the filter test, it will be logged and the SmartInspect.Watch
        event is fired.
        """

        # Initialize the watch packet for safe multi-threaded
        # access only if this SmartInspect object has one or more
        # connections which operate in asynchronous protocol mode.
        # Also see __CreateConnections.

        if (self.__fIsMultiThreaded):
            watch.ThreadSafe = True

        try:
        
            # are we filtering this entry?  if not, then process the packet.
            if (not self.__RaiseFilterEvent(watch)):

                self.__ProcessPacket(watch)
                self.__RaiseWatchEvent(watch)
        
        except Exception as ex:
            
            self.__RaiseErrorEvent(ex)


    def SetVariable(self, key:str, value:str) -> None:
        """
        Adds a new or updates an existing connection variable.
        
        Args:
            key (str):
                The key of the connection variable.
            value (str):
                The value of the connection variable.

        This method sets the value of a given connection variable.
        A connection variable is a placeholder for strings in the
        SmartInspect.Connections property. When
        setting a connections string (or loading it from a file
        with LoadConfiguration), any variables which have previously
        been defined with SetVariable are automatically replaced
        with their respective values.

        The variables in the connections string are expected to
        have the following form: $variable$.

        If a connection variable with the given key already exists,
        its value is overridden. To delete a connection variable,
        use UnsetVariable. This method does nothing if the key
        or value argument is null.

        Connection variables are especially useful if you load a
        connections string from a file and would like to handle
        some protocol options in your application instead of the
        configuration file.

        For example, if you encrypt log files, you probably do not
        want to specify the encryption key directly in your
        configuration file for security reasons. With connection
        variables, you can define a variable for the encryption
        key with SetVariable and then reference this variable in
        your configuration file. The variable is then automatically
        replaced with the defined value when loading the
        configuration file.

        Another example deals with the directory or path of a log
        file. If you include a variable in the path of your log
        file, you can later replace it in your application with
        the real value. This might come in handy if you want to
        write a log file to an environment specific value, such
        as an application data directory, for example.
        """
        if (key != None) and (value != None):
            self.__fVariables.Put(key, value)


    def UnsetVariable(self, key:str) -> str:
        """
        Unset's an existing connection variable.

        Args:
            key (str):
                The key of the connection variable to delete.

        This method deletes the connection variable specified by the
        given key. Nothing happens if the connection variable doesn't
        exist or if the key argument is null.
        """
        if (key != None):
            self.__fVariables.Remove(key)


    @staticmethod
    def Version() -> str:
        """
        Gets the version number of the SmartInspect Python3 library.
        
        Returns:
            The version number of the SmartInspect Python3 library. 
            The returned string always has the form "MAJOR.MINOR.RELEASE.BUILD".
        """
        return VERSION
