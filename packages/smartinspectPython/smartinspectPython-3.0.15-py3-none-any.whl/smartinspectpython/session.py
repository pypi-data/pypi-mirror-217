"""
Module: session.py

<details>
  <summary>Revision History</summary>

| Date       | Version     | Description
| ---------- | ----------- | ----------------------
| 2023/05/30 | 3.0.0.0     | Initial Version.  
| 2023/06/15 | 3.0.9.0     | Changed the Session.CurrentMethodName, CurrentMethodNameClass, and CurrentMethodNameClassNamespace properties to static methods.
| 2023/06/17 | 3.0.11.0    | Added *args support to Session class methods: LogDebug, LogVerbose, LogMessage, LogWarning, LogException, and LogFatal methods.
| 2023/06/17 | 3.0.12.0    | Changed Session EnterMethod, LeaveMethod to include source file.  
|            |             | Added default title to LogAppDomain method.
|            |             | Added exception handling in Session.LogSystem for user name value.  It was failing on Windows WSL systems, returning some sort of permissions error.
| 2023/06/23 | 3.0.13.0    | Changed Session LogAssigned method to properly format the LogMessage title value.
| 2023/06/28 | 3.0.14.0    | Changed Session class to use temporary logger to capture exception details in LogException method.

</details>
"""

import datetime
import logging
import tempfile
import _threading_local
from threading import Thread, currentThread
from io import BufferedReader, BytesIO, StringIO, TextIOWrapper
from datetime import datetime
import platform
import sys
import os
import inspect
from inspect import FrameInfo
from typing import Collection
from array import array
import sqlite3

# our package imports.
from .level import Level, Level as SILevel
from .color import Color
from .viewerid import ViewerId
from .logentrytype import LogEntryType
from .logentry import LogEntry
from .controlcommandtype import ControlCommandType
from .controlcommand import ControlCommand
from .watchtype import WatchType
from .watch import Watch
from .processflowtype import ProcessFlowType
from .processflow import ProcessFlow
from .sourceid import SourceId
from .viewerid import ViewerId
from .viewercontext import ViewerContext
from .dataviewercontext import DataViewerContext
from .textcontext import TextContext
from .binaryformatter import BinaryFormatter
from .binaryviewercontext import BinaryViewerContext
from .binarycontext import BinaryContext
from .valuelistviewercontext import ValueListViewerContext
from .inspectorviewercontext import InspectorViewerContext
from .listviewercontext import ListViewerContext
from .tableviewercontext import TableViewerContext
from .objectrenderer import ObjectRenderer
from .utils import DataTypeHelper

# the following causes a circular import error:
#from .smartinspect import SmartInspect

# our package constants.
from .const import (
    DEFAULT_COLOR_VALUE,
    UNKNOWN_VALUE
)

# auto-generate the "__all__" variable with classes decorated with "@export".
from .utils import export


@export
class Session:
    """
    Logs all kind of data and variables to the SmartInspect Console
    or to a log file.
    
    The Session class offers dozens of useful methods for sending
    any kind of data with the assistance of its Session.Parent.
    Sessions can send simple messages, warnings, errors and
    more complex things like pictures, objects, exceptions, system
    information and much more. They are even able to send variable
    watches, generate illustrated process and thread information
    or control the behavior of the SmartInspect Console. It is
    possible, for example, to clear the entire log in the Console by
    calling the ClearLog method.

    Please note that log methods of this class do nothing and return
    immediately if the session is currently not active (Active=False),
    its parent is disabled (Parent.Enabled=False), or the Level is not
    sufficient.

    Threadsafety:
        This class is fully thread-safe.
    """

    def __init__(self, parent, name:str) -> None:
        """
        Initializes a new Session instance with the
        default color and the specified parent and name.

        Args:
            parent (SmartInspect):
                The parent of the new session.
            name (str):
                The name of the new session.
        """

        #  initialize instance.
        self.__fLock = _threading_local.RLock()
        self.__fParent = parent
        self.__fLevel:SILevel = Level.Message
        self.__fName:str = ""
        self.__fActive:bool = True  # active by default
        self.__fIsStored:bool = False
        self.__fColorBG = Color(DEFAULT_COLOR_VALUE)
        self.__fCounters = {}
        self.__fCheckpoints = {}

        if (name != None):
            self.__fName = name

        self.ResetColor()

        # configure temporary logger and stream to capture exception message logging.
        self.__fTempLogger = logging.getLogger('smartinspectpython_temp_log')
        self.__fTempLogger.setLevel(logging.ERROR)
        self.__fTempLoggingStream = StringIO()
        handler = logging.StreamHandler(stream=self.__fTempLoggingStream)
        self.__fTempLogger.addHandler(handler)


    @property
    def __IsStored(self) -> bool:
        """ 
        Gets the __IsStored property value.

        Returns:
            True if this session is stored in the session tracking list
            and false otherwise.

        Indicates if this session is stored in the session tracking
        list of its Parent.

        See the SmartInspect.GetSession and SmartInspect.AddSession
        methods for more information about session tracking.
        """
        return self.__fIsStored
    

    @__IsStored.setter
    def __IsStored(self, value:bool) -> None:
        """ 
        Sets the __IsStored property value.
        """
        if value != None:
            self.__fIsStored = value


    @property
    def Active(self) -> bool:
        """ 
        Gets the Active property value.

        Returns:
            True if this session can send log message data to the active
            protocols; otherwise, False to suspend logging activity.

        Specifies if the session is currently active.  

        If this property is set to false, all logging methods of this
        class will return immediately and do nothing. Please note that
        the Parent of this session also needs to be SmartInspect.Enabled
        in order to log information.

        This property is especially useful if you are using multiple
        sessions at once and want to deactivate a subset of these
        sessions. To deactivate all your sessions, you can use the
        SmartInspect.Enabled property of the Parent.
        """
        return self.__fActive
    

    @Active.setter
    def Active(self, value:bool) -> None:
        """ 
        Sets the Active property value.
        """
        if value != None:
            self.__fActive = value


    @property
    def ColorBG(self) -> Color:
        """ 
        Gets the ColorBG property value.

        Returns:
            The background color used for this session in the SmartInspect Console.

        The session color helps you to identify Log Entries from
        different sessions in the SmartInspect Console by changing
        the background color.
        """
        return self.__fColorBG
    
    @ColorBG.setter
    def ColorBG(self, value:Color) -> None:
        """ 
        Sets the ColorBG property value.
        """
        if value != None:
            if (value.A != 0):
                # ensure it is transparent.
                self.__fColorBG = Color.FromArgb(0, value.R, value.G, value.B)
            else:
                self.__fColorBG = value


    @property
    def Level(self) -> SILevel:
        """ 
        Gets the Level property value.

        Returns:
            The log level of this Session object.

        Each Session object can have its own log level. A log message
        is only logged if its log level is greater than or equal to
        the log level of a session AND the session Parent. Log levels
        can thus be used to limit the logging output to important
        messages only.
        """
        if (self.__fLevel == None):
            return self.__fParent.DefaultLevel
        return self.__fLevel
    

    @Level.setter
    def Level(self, value:SILevel) -> None:
        """ 
        Sets the Level property value.
        """
        if value != None:
            self.__fLevel = value


    @property
    def Name(self) -> str:
        """ 
        Gets the Name property value.

        Returns:
            The session name used for Log Entries.
        
        The session name helps you to identify Log Entries from
        different sessions in the SmartInspect Console. If you set
        this property to null, the session name will be empty when
        sending Log Entries.
        """
        return self.__fName
    

    @Name.setter
    def Name(self, value:str) -> None:
        """ 
        Sets the Name property value.
        """
        name:str = ""

        if (value != None):
            name = value

        if (self.__fIsStored):
            self.__fParent.__UpdateSession(self, name, self.__fName)

        self.__fName = name


    @property
    def Parent(self):
        """ 
        Gets the Name property value.

        Returns:
            The parent SmartInspect instance that owns the session.

        The parent of a session is a SmartInspect instance. It is
        responsible for sending the packets to the SmartInspect Console
        or for writing them to a file. If the SmartInspect.Enabled
        property of the parent is false, all logging methods
        of this class will return immediately and do nothing.
        """
        return self.__fParent
    

    ###################################################################################
    # Internal methods follow after this.
    #
    # NOTE - Keep them in alphabetical order for Documentation generator!
    ###################################################################################


    def __GetThreadTitle(self, thread:Thread, titlePrefix:str=None) -> str:
        """
        Formulates a thread title if one was not supplied by the user.
        
        Args:
            thread (Thread):
                Thread to obtain titling information from.
            titlePrefix (str):
                Title prefix to add thread-derived title to.

        Returns:
            The thread title in the form of "prefix: thread.name (id = thread.id)".
        """
        # if no thread object supplied then don't bother.
        if (thread == None):
            return "No Thread Object"

        title:str = titlePrefix

        # if thread name not set, then use the thread id value.
        name:str = thread.name
        if ((name == None) or (len(name) == 0)):
            name = "Id = " + str(thread.ident)
        else:
            name += " (Id = " + str(thread.ident) + ")"

        # if title not set, then use default title.
        if ((title == None) or (len(title) == 0)):
            title = "Thread info:"

        return title + " " + name


    def __LogObjectBuildContext(self, groupTitle:str, instance:object, members, ctx:InspectorViewerContext, excludeNonPublic:bool, excludeBuiltIn:bool, excludeMethods:bool=False, excludeProperties:bool=False) -> None:
        """
        Adds inspect.getmember() data block to a context viewer for logging.

        Args:
            groupTitle (str):
                The block title to display in the Console.
            instance (object):
                The object whose fields and properties should be logged.
            members (object):
                Data returned from the call to inspect.getmembers() function.
            excludeNonPublic (bool):
                Specifies if non public member items (e.g. "_x" prefix) should 
                be excluded from the log data.
            excludeBuiltIn (bool):
                Specifies if non public "built-in" member items (e.g. "__x" prefix) should 
                be excluded from the log data.
            excludeMethods (bool):
                Specifies if method or function member items (e.g. "<bound method" or "<function " prefixes)
                should be excluded from the log data.
            excludeProperties (bool):
                Specifies if members decorated with a "@property" attribute should be 
                excluded from the log data.
        """
        # Example of inspect.getmembers() output:
        # - PropertyBool : True
        # - PropertyString : 'This is a string property value'
        # - PublicEvent : <bound method InstanceGetMembersTestClass.PublicEvent of <__main__.InstanceGetMembersTestClass object at 0x0000026B84569AC0>>
        # - PublicFunctionString : <bound method InstanceGetMembersTestClass.PublicFunctionString of <__main__.InstanceGetMembersTestClass object at 0x0000026B84569AC0>>
        # - PublicMethod : <bound method InstanceGetMembersTestClass.PublicMethod of <__main__.InstanceGetMembersTestClass object at 0x0000026B84569AC0>>
        # - PublicStaticFunction : <function InstanceGetMembersTestClass.PublicStaticFunction at 0x0000026B859F1EE0>
        # - PublicStaticMethod : <function InstanceGetMembersTestClass.PublicStaticMethod at 0x0000026B859F1E50>
        # - STATIC_VAR_BOOL : True
        # - STATIC_VAR_INT : 69
        # - STATIC_VAR_STRING : 'Static String'
        # - _InstanceGetMembersTestClass__fPropertyBool : True
        # - _InstanceGetMembersTestClass__fPropertyBoolDynamic : True
        # - _InstanceGetMembersTestClass__fPropertyString : 'This is a string property value'
        # - _InstanceGetMembersTestClass__fPropertyStringDynamic : 'This is a INTERNAL string property value'

        iList:list[str] = []

        # add member data to context viewer.
        for name, data in members:

            # are we excluding nonpublic members?
            if (excludeNonPublic) and (name.startswith('_')):
                continue

            # are we excluding built-in members?
            if (excludeBuiltIn) and (name.startswith('__')):
                continue

            # exclude functions and methods - just looking for field or property values here.
            if ((excludeMethods) and (str(data).startswith("<"))):
                continue

            # are we excluding @property methods?
            if (excludeProperties):
                attr = getattr(type(instance), name, None)
                if (attr != None): 
                    if (isinstance(attr, property)):
                        continue

            sb:str = ""

            try:
            
                sb += ctx.EscapeItem(name)
                sb += "="
                sb += ctx.EscapeItem(ObjectRenderer.RenderObject(data))
            
            except Exception as ex:
            
                sb += "<not accessible>"

            # add context entry to the list.
            iList.append(sb)
            sb = ""

        # sort context items - the member name is the first thing displayed
        # in the item, so the list is sorted by member name.
        # note that in Python, UPPER-case items are sorted above lower-case items,
        # so we use the "key=str.lower) syntax to force the case-insensitive sort.
        iList.sort(key=str.lower)

        # begin a new group and append the list to the inspector context.
        ctx.StartGroup(groupTitle)
        for line in iList:
            ctx.AppendLine(str(line))

        # clear list.
        iList.clear()


    def __SendContext(self, level:Level, title:str, lt:LogEntryType, ctx:ViewerContext, colorValue:int=None) -> None:
        """
        Sends a LogEntry packet of information that contains viewer context.

        Args:
            level (Level):
                Level to set in the LogEntry.
            title (str):
                Title to set in the LogEntry.
            lt
                LogEntryType to set in the LogEntry.
            ctx
                ViewerContext to set in the LogEntry.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.__SendLogEntry(level, title, lt, ctx.ViewerId, colorValue, ctx.ViewerData)


    def __SendControlCommand(self, ct:ControlCommandType, data:BytesIO) -> None:
        """
        Sends a ControlCommand packet of information.

        Args:
            ct
                ControlCommandType to set in the ControlCommand.
            data
                Data to set in the ControlCommand.
        """
        controlCommand:ControlCommand = ControlCommand(ct)
        controlCommand.Data = data
        controlCommand.Level = SILevel.Control
        self.__fParent.SendControlCommand(controlCommand)


    def __SendLogEntry(self, level:Level, title:str, lt:LogEntryType, vi:ViewerId, colorValue:int=None, data:BytesIO=None) -> None:
        """
        Sends a LogEntry packet of information.

        Args:
            level (Level):
                Level to set in the LogEntry.
            title (str):
                Title to set in the LogEntry.
            lt
                LogEntryType to set in the LogEntry.
            vi
                ViewerId to set in the LogEntry.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
            data
                Data to set in the LogEntry.
        """
        # validations.
        if (title == None):
            title = ""

        logEntry:LogEntry = LogEntry(lt, vi)

        # set the properties we already know.
        logEntry.Timestamp = self.__fParent.Now()
        logEntry.Title = title
        logEntry.SessionName = self.__fName # our session name
        logEntry.Level = level

        if (data != None):
            logEntry.Data = data

        # was a background color specified?
        # if no, then use default (white) background color assigned to this session.
        # if yes, then ensure it is transparent.
        if (colorValue == None):
            logEntry.ColorBG = self.__fColorBG
        else:
            colorObj:Color = Color(colorValue)
            if (colorObj.A != 0):
                colorObj = Color.FromArgb(0, colorObj.R, colorObj.G, colorObj.B)
            logEntry.ColorBG = colorObj

        # send the new Log Entry.
        self.__fParent.SendLogEntry(logEntry)


    def __SendProcessFlow(self, level:SILevel, title:str, pt:ProcessFlowType) -> None:
        """
        Sends a ProcessFlow packet of information.

        Args:
            level (Level):
                Level to set in the LogEntry.
            title (str):
                Title to set in the LogEntry.
            pt
                ProcessFlowType to set in the LogEntry.
        """
        processFlow:ProcessFlow = ProcessFlow(pt)
        processFlow.Timestamp = self.__fParent.Now()
        processFlow.Title = title
        processFlow.Level = level
        self.__fParent.SendProcessFlow(processFlow)


    def __SendWatch(self, level:SILevel, name:str, value:str, wt:WatchType) -> None:
        """
        Sends a Watch packet of information.

        Args:
            level (Level):
                Level to set in the LogEntry.
            name
                Name to set in the LogEntry.
            value
                Value to set in the LogEntry.
            wt
                WatchType to set in the LogEntry.
        """
        watch:Watch = Watch(wt)
        watch.Timestamp = self.__fParent.Now()
        watch.Name = name
        watch.Value = value
        watch.Level = level
        self.__fParent.SendWatch(watch)


    def __UpdateCheckpoint(self, name:str, increment:bool) -> int:
        """
        Updates a named checkpoint counter in a thread-safe manner.
        
        Args:
            name
                Checkpoint counter name to update.
            increment
                True to increment the named counter; False to decrement.

        Returns:
            The updated named checkpoint counter value.
        """
        value:int = 0

        with self.__fLock:

            if name in self.__fCheckpoints.keys():
                value = int(self.__fCheckpoints[name])
            else:
                value = 0

            if (increment):
                value = value + 1
            else:
                value = value - 1

            self.__fCheckpoints[name] = value

        return value


    def __UpdateCounter(self, name:str, increment:bool) -> int:
        """
        Updates a named counter in a thread-safe manner.
        
        Args:
            name
                Counter name to update.
            increment
                True to increment the named counter; False to decrement.

        Returns:
            The updated named counter value.
        """
        value:int = 0

        with self.__fLock:

            if name in self.__fCounters.keys():
                value = int(self.__fCounters[name])
            else:
                value = 0

            if (increment):
                value = value + 1
            else:
                value = value - 1

            self.__fCounters[name] = value

        return value


    ###################################################################################
    # Public Log methods follow after this.
    #
    # NOTE - Keep them in alphabetical order for Documentation generator!
    ###################################################################################


    def AddCheckpoint(self, level:SILevel=None, name:str=None, details:str=None, colorValue:int=None) -> None:
        """
        Increments the counter of a named checkpoint and logs a
        message with a custom log level and an optional message.

        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the checkpoint to increment.
            details (str):
                An optional message to include in the resulting log entry.
                Can be null / None.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method increments the counter for the given checkpoint
        and then logs a message using "%checkpoint% #N" as title where
        %checkpoint% stands for the name of the checkpoint and N for
        the incremented counter value. The initial value of the counter
        for a given checkpoint is 0. Specify the details parameter to
        include an optional message in the resulting log entry. You
        can use the ResetCheckpoint method to reset the counter to 0
        again. 
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                name = "Checkpoint"
        
            try:

                # update checkpoint value.                
                value:int = self.__UpdateCheckpoint(name, True)

                # format checkpoint message details.
                subtitle:str = ""
                if (details != None):
                    subtitle = str.format(" ({0})", details)
                title:str = str.format("{0} #{1}{2}", name, str(value), subtitle)

                # send log entry packet.
                self.__SendLogEntry(level, title, LogEntryType.Checkpoint, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("AddCheckpoint: " + str(ex))


    def ClearAll(self, level:SILevel=None) -> None:
        """
        Resets the whole Console.

        Args:
            level (Level):
                The log level of this method call.

        This method resets the whole Console. This means that all
        Watches, Log Entries, Process Flow entries and AutoViews
        will be deleted.
        """
        if (self.IsOn(level)):

            try:
                
                # send control command.
                self.__SendControlCommand(ControlCommandType.ClearAll, None)

            except Exception as ex:
                
                self.LogInternalError("ClearAll: " + str(ex))


    def ClearAutoViews(self, level:SILevel=None) -> None:
        """
        Clears all AutoViews in the Console.

        Args:
            level (Level):
                The log level of this method call.
        """
        if (self.IsOn(level)):

            try:
                
                # send control command.
                self.__SendControlCommand(ControlCommandType.ClearAutoViews, None)

            except Exception as ex:
                
                self.LogInternalError("ClearAutoViews: " + str(ex))


    def ClearLog(self, level:SILevel=None) -> None:
        """
        Clears all Log Entries in the Console.

        Args:
            level (Level):
                The log level of this method call.
        """
        if (self.IsOn(level)):

            try:
                
                # send control command.
                self.__SendControlCommand(ControlCommandType.ClearLog, None)

            except Exception as ex:
                
                self.LogInternalError("ClearLog: " + str(ex))


    def ClearProcessFlow(self, level:SILevel=None) -> None:
        """
        Clears all Process Flow entries in the Console.

        Args:
            level (Level):
                The log level of this method call.
        """
        if (self.IsOn(level)):

            try:
                
                # send control command.
                self.__SendControlCommand(ControlCommandType.ClearProcessFlow, None)

            except Exception as ex:
                
                self.LogInternalError("ClearProcessFlow: " + str(ex))


    def ClearWatches(self, level:SILevel=None) -> None:
        """
        Clears all Watches in the Console.

        Args:
            level (Level):
                The log level of this method call.
        """
        if (self.IsOn(level)):

            try:
                
                # send control command.
                self.__SendControlCommand(ControlCommandType.ClearWatches, None)

            except Exception as ex:
                
                self.LogInternalError("ClearWatches: " + str(ex))


    @staticmethod
    def CurrentMethodName() -> str:
        """ 
        Returns the fully-qualified method name of the current stack level in the
        form of "MethodName".

        Returns:
            The fully-qualified method name of the current stack level in the
            form of "MethodName".

        Reflection is used to determine the method name.
        If method info could not be queried, "&lt;Unknown&gt;" is returned.
        
        No exception will be thrown by this method.
        """
        return Session.GetMethodName(1, False)


    @staticmethod
    def CurrentMethodNameClass() -> str:
        """ 
        Returns the fully-qualified method name of the current stack level in the
        form of "ClassName.MethodName".

        Returns:
            The fully-qualified method name of the current stack level in the
            form of "ClassName.MethodName".

        Reflection is used to determine the method name.
        If method info could not be queried, "&lt;Unknown&gt;" is returned.
        
        No exception will be thrown by this method.
        """
        return Session.GetMethodName(1, True)


    @staticmethod
    def CurrentMethodNameClassNamespace() -> str:
        """ 
        Returns the fully-qualified method name of the current stack level in the
        form of "Namespace.ClassName.MethodName".

        Returns:
            The fully-qualified method name of the current stack level in the
            form of "Namespace.ClassName.MethodName".

        Reflection is used to determine the method name.
        If method info could not be queried, "&lt;Unknown&gt;" is returned.
        
        No exception will be thrown by this method.
        """
        return Session.GetMethodName(1, True)


    def DecCounter(self, level:SILevel=None, name:str=None) -> None:
        """
        Decrements a named counter by one and automatically
        sends its name and value as integer watch with a custom log
        level.

        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the counter to log.

        The Session class tracks a list of so called named counters.
        A counter has a name and a value of type integer. This method
        decrements the value for the specified counter by one and then
        sends a normal integer watch with the name and value of the
        counter. The initial value of a counter is 0. To reset the
        value of a counter to 0 again, you can call ResetCounter.

        See IncCounter for a method which increments the value of a
        named counter instead of decrementing it.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("DecCounter: name argument is null.")
                return
        
            try:
                
                # send watch packet.
                value:int = self.__UpdateCounter(name, False)
                self.__SendWatch(level, name, str(value), WatchType.Integer)

            except Exception as ex:
                
                self.LogInternalError("DecCounter: " + str(ex))


    def EnterMethod(self, level:SILevel=None, methodName:str=None) -> None:
        """
        Enters a method by using a custom log level.
        The resulting method name consists of the FullName of the
        type of the supplied instance parameter, followed by a dot
        and the supplied methodName argument.
        
        Args:
            level (Level):
                The log level of this method call.
            methodName (str):
                The name of the method; otherwise null to retrieve the 
                current method name from inspect data.
        
        The EnterMethod method notifies the Console that a new
        method has been entered. The Console includes the method in
        the method hierarchy. If this method is used consequently, a
        full call stack is visible in the Console which helps locating
        bugs in the source code. Please see the LeaveMethod method as 
        the counter piece to EnterMethod.
        
        If the methodName is null, then the currently executing method name
        is derived from calling inspect.stack.  The function name, module name,
        and source line number are displayed.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            # if method name was not specified then get it from the stack frame.
            if (methodName is None):
                methodName = Session.GetMethodName(1, True)  # start=1 excludes our EnterMethod
        
            try:
                
                # send two packets: one log entry, and one process flow entry.
                self.__SendLogEntry(level, methodName, LogEntryType.EnterMethod, ViewerId.Title)
                self.__SendProcessFlow(level, methodName, ProcessFlowType.EnterMethod)

            except Exception as ex:
                
                self.LogInternalError("EnterMethod: " + str(ex))


    def EnterProcess(self, level:SILevel=None, processName:str=None) -> None:
        """
        Enters a new process by using a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            processName (str):
                The name of the process.
        
        The EnterProcess method notifies the Console that a new
        process has been entered. The Console displays this process
        in the Process Flow toolbox. Please see the LeaveProcess
        method as the counter piece to EnterProcess.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            # validations.
            if (processName == None):
                processName = ""
        
            try:
                
                # send two packets: one for process name entry, and one for process thread entry.
                self.__SendProcessFlow(level, processName, ProcessFlowType.EnterProcess)
                self.__SendProcessFlow(level, "Main Thread", ProcessFlowType.EnterThread)

            except Exception as ex:
                
                self.LogInternalError("EnterProcess: " + str(ex))


    def EnterThread(self, level:SILevel=None, threadName:str=None) -> None:
        """
        Enters a new thread by using a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            threadName (str):
                The name of the thread.
        
        The EnterThread method notifies the Console that a new
        thread has been entered. The Console displays this thread
        in the Process Flow toolbox. Please see the LeaveThread
        method as the counter piece to EnterThread.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            # validations.
            if (threadName == None):
                threadName = ""
        
            try:
                
                # send process thread entry packet.
                self.__SendProcessFlow(level, threadName, ProcessFlowType.EnterThread)

            except Exception as ex:
                
                self.LogInternalError("EnterThread: " + str(ex))


    @staticmethod
    def GetMethodName(stackLevel:int=0, includeNameSpace:bool=False, includeClassName:bool=False) -> str:
        """
        Returns the callers method name for the specified stack level.
        
        Args:
            stackLevel (int):
        	    The Stack Frame level to query - defaults to 1 if zero is specified.
            includeSourcePos (bool):
                True to append the module name and source line # to the method name; 
                otherwise False (default) to return only the method name.
            includeNameSpace
                True to prefix the returned method name with the name-space identifier; otherwise False to
                not return the name-space identifier.
            includeClassName
                True to prefix the returned method name with the class name; otherwise False to
                not return the class name.
        
        Returns:
            The callers method name.
        
        Reflection is used to determine the method name for the specified stack level.  
        If method info could not be queried, "&lt;Unknown&gt;" is returned.
        
        No exception will be thrown by this method.
        """   
        
        UNKNOWN: str = "<Unknown>"
        methodName: str = UNKNOWN
        className: str = None

        try:
            # the call stack.
            stack:list[FrameInfo] = inspect.stack()

            # bypass the 0 frame index, as that would be the function we are currently in.
            stackLevel = stackLevel + 1

            # validations.
            if (stackLevel < 1):
                stackLevel = 1
            if (stackLevel > len(stack) - 1):
                stackLevel = len(stack) - 1

            # get the stack frame the caller is interested in.
            stackFrame:FrameInfo = stack[stackLevel]
            if (stackFrame == None):
                return methodName

            # extract the parts of the stack frame.
            filepath, line, funcname, context = stackFrame[1:5]
            methodName = funcname.strip()

            # if not including source position info then we are done.
            if (not includeNameSpace):
                return methodName

            # drop the path and extension from the file name.
            moduleName = os.path.basename(filepath)
            #moduleNameNoExt = os.path.splitext(os.path.basename(filepath))[0]

            # add source position to method name.
            if (includeNameSpace) and (moduleName != None):
                methodName += " ({0}, line {1})".format(moduleName, line)

            # return to caller.
            return methodName

        except Exception as ex:

            return UNKNOWN


    def IncCounter(self, level:SILevel=None, name:str=None) -> None:
        """
        Increments a named counter by one and automatically
        sends its name and value as integer watch with a custom log
        level.

        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the counter to log.
        
        The Session class tracks a list of so called named counters.
        A counter has a name and a value of type integer. This method
        increments the value for the specified counter by one and then
        sends a normal integer watch with the name and value of the
        counter. The initial value of a counter is 0. To reset the
        value of a counter to 0 again, you can call ResetCounter.

        See DecCounter for a method which decrements the value of a
        named counter instead of incrementing it.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("IncCounter: name argument is null.")
                return
        
            try:
                
                # send watch packet.
                value:int = self.__UpdateCounter(name, True)
                self.__SendWatch(level, name, str(value), WatchType.Integer)

            except Exception as ex:
                
                self.LogInternalError("IncCounter: " + str(ex))


    def IsOn(self, level:SILevel=None) -> bool:
        """ 
        Indicates if information can be logged for a certain log level or not.  

        Args:
            level (Level):
                The log level to check for.

        Returns:
            True if information can be logged and false otherwise.
        
        This method is used by the logging methods in this class
        to determine if information should be logged or not. When
        extending the Session class by adding new log methods to a
        derived class it is recommended to call this method first.
        """
        # use the session level if level not specified on the method call.
        if (level == None):
            level = self.__fParent.DefaultLevel

        return self.__fActive and \
                self.__fParent.Enabled and \
                (level >= self.__fLevel) and \
                (level >= self.__fParent.Level)


    def LeaveMethod(self, level:SILevel=None, methodName:str=None) -> None:
        """
        Leaves a method by using a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            methodName (str):
                The name of the method; otherwise null to retrieve the 
                current method name from inspect data.
        
        The LeaveMethod method notifies the Console that a method
        has been left. The Console closes the current method in the
        method hierarchy. If this method is used consequently, a full
        call stack is visible in the Console which helps locating bugs
        in the source code. Please see the EnterMethod method as the 
        counter piece to EnterMethod.
       
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            # if method name was not specified then get it from the stack frame.
            if (methodName is None):
                methodName = Session.GetMethodName(1, True)  # start=1 excludes our EnterMethod
        
            try:
                
                # send two packets: one log entry, and one process flow entry.
                self.__SendLogEntry(level, methodName, LogEntryType.LeaveMethod, ViewerId.Title)
                self.__SendProcessFlow(level, methodName, ProcessFlowType.LeaveMethod)

            except Exception as ex:
                
                self.LogInternalError("LeaveMethod: " + str(ex))


    def LeaveProcess(self, level:SILevel=None, processName:str=None) -> None:
        """
        Leaves a process by using a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            processName (str):
                The name of the process.
        
        The LeaveProcess method notifies the Console that a process
        has finished. The Console displays this change in the Process
        Flow toolbox. Please see the EnterProcess method as the
        counter piece to LeaveProcess.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            # validations.
            if (processName == None):
                processName = ""
        
            try:
                
                # send two packets: one for process thread exit, and one for process name exit.
                self.__SendProcessFlow(level, "Main Thread", ProcessFlowType.LeaveThread)
                self.__SendProcessFlow(level, processName, ProcessFlowType.LeaveProcess)

            except Exception as ex:
                
                self.LogInternalError("LeaveProcess: " + str(ex))


    def LeaveThread(self, level:SILevel=None, threadName:str=None) -> None:
        """
        Leaves a thread by using a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            threadName (str):
                The name of the thread.
        
        The LeaveThread method notifies the Console that a thread
        has finished. The Console displays this change in the Process
        Flow toolbox. Please see the EnterThread method as the
        counter piece to LeaveThread.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            # validations.
            if (threadName == None):
                threadName = ""
        
            try:
                
                # send process thread exit packet.
                self.__SendProcessFlow(level, threadName, ProcessFlowType.LeaveThread)

            except Exception as ex:
                
                self.LogInternalError("LeaveThread: " + str(ex))


    def LogAppDomain(self, level:SILevel=None, title:str=None, colorValue:int=None) -> None:
        """
        Logs information about an application and its setup with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs information about the current application and its setup.
        This is not quite the same as the C# equivalent, but it does log similar properties.
        """
        if (not self.IsOn(level)):
            return

        ctx:InspectorViewerContext = InspectorViewerContext()
        try:

            # default title if one was not supplied.
            if (title == None) or (len(title) == 0):
                title = "Application Domain details"

            basename:str = UNKNOWN_VALUE
            dirname:str = UNKNOWN_VALUE

            if (len(sys.argv) > 0):
                basename = os.path.basename(sys.argv[0])
                dirname = os.path.dirname(sys.argv[0])

            ctx.StartGroup("General")
            ctx.AppendKeyValue("Executable Name", basename)
            ctx.AppendKeyValue("Executable Directory", dirname)
            ctx.AppendKeyValue("Arguments (sys.argv)", str(sys.argv))

            ctx.StartGroup("Setup")
            ctx.AppendKeyValue("Current Working Directory", os.getcwd())
            ctx.AppendKeyValue("Python Version", platform.python_version())

            # send the packet.
            self.__SendContext(level, title, LogEntryType.Text, ctx, colorValue)
        
        except Exception as ex:
        
            self.LogInternalError("LogAppDomain: " + str(ex))


    def LogArray(self, level:SILevel=None, title:str=None, oArray:array=None, colorValue:int=None) -> None:
        """
        Logs the content of an array with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console - "Current stack trace" is used if one is not supplied.
            oArray (array):
                The array to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method iterates through the supplied array and calls ObjectRenderer.RenderObject to
        render every element into a string. These elements will be displayed in a listview in the Console.
        """
        self.LogCollection(level, title, oArray, colorValue)


    def LogAssert(self, condition:bool=None, title:str=None, colorValue:int=None) -> None:
        """
        Logs an assert message if a condition is false with
        a log level of Level.Error.
        
        Args:
            condition (bool):
                The condition to check.
            title (str):
                The title of the Log Entry.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        An assert message is logged if this method is called with a
        condition parameter of the value false. No LogEntry
        is generated if this method is called with a
        condition parameter of the value true.

        A typical usage of this method would be to test if a variable
        is not set to null before you use it. To do this, you just need
        to insert a LogAssert call to the code section in question with
        "instance != null" as first parameter. If the reference is null
        and thus the expression evaluates to false, a message is logged.
        """
        if (self.IsOn(SILevel.Error)):

            try:

                if (not condition):

                    # send the packet.
                    self.__SendLogEntry(SILevel.Error, title, LogEntryType.Assert, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogAssert: " + str(ex))


    def LogAssigned(self, level:SILevel=None, name:str=None, value:object=None, colorValue:int=None) -> None:
        """
        Logs whether a variable is assigned or not with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the variable.
            value (object):
                The variable value which should be checked for null.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        If the value argument is null, then ": Not assigned",
        otherwise ": Assigned" will be appended to the name before
        the LogEntry is sent.

        This method is useful to check source code for null references
        in places where you experienced or expect problems and want to
        log possible null references.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogAssigned: name argument is null.")
                return

            # not sure why SI authors chose to use "Logmessage" here, since a "level" was 
            # passed and an "IsOn(level)" check is performed.
            # this will only log a message if the level is Message or less!

            try:

                # send log entry packet.
                if (value != None):
                    self.LogMessage(str.format("{0}: Assigned", name), colorValue=colorValue)
                    #self.LogText(level, str.format("{0}: Assigned", name), "", colorValue)
                else:
                    self.LogMessage(str.format("{0}: Not assigned", name), colorValue=colorValue)
                    #self.LogText(level, str.format("{0}: Not assigned", name), "", colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogAssigned: " + str(ex))


    def LogBinary(self, level:SILevel=None, title:str=None, buffer:bytes=None, offset:int=None, count:int=None, colorValue:int=None) -> None:
        """
        Logs a byte array with a custom log level and
        displays it in a hex viewer.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            buffer (bytes):
                The byte array to display in the hex viewer.
            offset (int):
                The byte offset (zero-based) of buffer at which to display data from.
            count (int):
                The amount of bytes to display.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        if (self.IsOn(level)):

            # validations.
            if (offset == None) and (count != None):
                self.LogInternalError("LogBinary: count argument is required if offset argument is not null.")
                return

            if (offset != None) and (count == None):
                self.LogInternalError("LogBinary: offset argument is required if count argument is not null.")
                return

            if (offset != None) and (count != None) and (buffer != None):
                if ((offset + count) > len(buffer)):
                    self.LogInternalError("LogBinary: offset + count arguments exceed the length of the buffer.")
                    return

            ctx:BinaryViewerContext = BinaryViewerContext()
            try:

                if ((offset == None) and (count == None)):                
                    ctx.AppendBytes(buffer)
                else:
                    ctx.AppendBytes(buffer[offset:offset + count])

                # send the packet.
                self.__SendContext(level, title, LogEntryType.Binary, ctx, colorValue)
                
            except Exception as ex:
                
                self.LogInternalError("LogBinary: " + str(ex))
                

    def LogBinaryFile(self, level:SILevel=None, title:str=None, fileName:str=None, colorValue:int=None) -> None:
        """
        Logs a binary file and displays its content in
        a hex viewer using a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The binary file to display in a hex viewer.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.Binary, ViewerId.Binary, colorValue)


    def LogBinaryStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a binary stream with a custom log level and
        displays its content in a hex viewer.
        
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedReader):
                The binary stream to display in a hex viewer.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Binary, ViewerId.Binary, colorValue)


    def LogBitmapFile(self, level:SILevel=None, title:str=None, fileName:str=None, colorValue:int=None) -> None:
        """
        Logs a bitmap file and displays it in the Console
        using a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The bitmap file to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.Graphic, ViewerId.Bitmap, colorValue)


    def LogBitmapStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a stream with a custom log level and
        interprets its content as a bitmap.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedReader):
                The stream to display as bitmap.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Graphic, ViewerId.Bitmap, colorValue)


    def LogBool(self, level:SILevel=None, name:str=None, value:bool=None, colorValue:int=None) -> None:
        """
        Logs a bool value with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (bool):
                The variable value.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a boolean variable.
        A title like "name = True" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogBool: name argument is null.")
                return

            try:

                # use "True"/"False" in case other boolean values passed (e.g. 0/1, yes/no, on/off, etc).
                v:str
                if (value == True):
                    v:str = "True"
                else:
                    v:str = "False"

                # send log entry packet.
                title:str = str.format("{0} = {1}", name, v)
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogBool: " + str(ex))


    def LogByte(self, level:SILevel=None, name:str=None, value:int=None, includeHex:bool=False, colorValue:int=None) -> None:
        """
        Logs a byte value with an optional hexadecimal representation 
        and custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (int):
                The variable value.
            includeHex (bool):
                Indicates if a hexadecimal representation should be included (True) or not (False).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a single byte variable.
        A title like "name = 10" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogByte: name argument is null.")
                return

            try:

                vhex:str = ""
                if (includeHex):
                    vhex = " (" + hex(value).upper() + ")"
                    if (value < 0):
                        vhex = vhex.replace("-","")     # remove minus sign for negative values.
                    vhex = vhex.replace("0X","0x")      # make "0X" lower-case since hex values will be in upper-case

                # send log entry packet.
                title:str = str.format("{0} = {1}{2}", name, str(value), vhex)
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogByte: " + str(ex))


    def LogChar(self, level:SILevel=None, name:str=None, value:chr=None, colorValue:int=None) -> None:
        """
        Logs a chr value with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (chr):
                The variable value.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a chr variable.
        A title like "name = 'c'" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogChar: name argument is null.")
                return

            try:

                # send log entry packet.
                title:str = str.format("{0} = '{1}'", name, str(value))
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogChar: " + str(ex))


    def LogCollection(self, level:SILevel=None, title:str=None, oColl:Collection=None, colorValue:int=None) -> None:
        """
        Logs the content of a collection with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console; "Current stack trace" is used if one is not supplied.
            oColl (Collection):
                The collection to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method iterates through the supplied collection and calls ObjectRenderer.RenderObject to
        render every value into a string. These values will be displayed in a listview in the Console.
        """
        self.LogEnumerable(level, title, oColl, colorValue)


    def LogColored(self, level:SILevel=None, colorValue:int=None, title:str=None) -> None:
        """
        Logs a colored message with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
            title (str):
                The message to log.
        """
        if (self.IsOn(level)):

            try:
                
                # send the packet.
                self.__SendLogEntry(level, title, LogEntryType.Message, ViewerId.Title, colorValue, None)

            except Exception as ex:
                
                self.LogInternalError("LogColored: " + str(ex))


    def LogConditional(self, level:SILevel=None, condition:bool=None, title:str=None, colorValue:int=None) -> None:
        """
        Logs a conditional message with a custom log level. The message 
        is created with a format string and a related array of arguments.

        Args:
            level (Level):
                The log level of this method call.
            condition (bool):
                The condition to evaluate.
            title (str):
                The title of the conditional message.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        
        This method only sends a message if the passed 'condition'
        argument evaluates to true. If 'condition' is false, this
        method has no effect and nothing is logged. This method is
        thus the counter piece to LogAssert.

        This version of the method accepts a format string and a
        related array of arguments. These parameters will be passed to
        the String.Format method and the resulting string will be the
        conditional message.
        """
        if (self.IsOn(level)):

            try:

                if (condition):

                    # send the packet.
                    self.__SendLogEntry(level, title, LogEntryType.Conditional, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogConditional: " + str(ex))


    def LogCurrentAppDomain(self, level:SILevel=None, title:str=None, colorValue:int=None) -> None:
        """
        Logs information about the current application and its setup with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs information about the current application and its setup.
        This is not quite the same as the C# equivalent, but it does log similar properties.
        """
        self.LogAppDomain(level, title, colorValue)


    def LogCurrentStackTrace(self, level:SILevel=None, title:str=None, limit:int=None, colorValue:int=None) -> None:
        """
        Logs the current stack trace with a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console; "Current stack trace" is used if one is not supplied.
            limit (int):
                The number of frames to print (specify None to print all remaining frames).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the current stack trace. The resulting LogEntry contains all methods including the
        related classes that are currently on the stack. Furthermore, the filename, line and columns numbers are included.

        Please note that the stack frame information results will NOT include 2 frames that are used
        by the SmartInspect API to process the frame data.
        """
        if (self.IsOn(level)):

            # default title if one was not supplied.
            if ((title == None) or (len(title) == 0)):
                title = "Current stack trace"

            try:

                # get current stack trace.
                strace:list[FrameInfo] = inspect.stack()

                # skip our "LogCurrentStackTrace" method and start at the caller to this function.
                startFrame:int = 1

                # call overloaded method.
                self.LogStackTrace(level, title, strace, startFrame, limit, colorValue)

            except Exception as ex:
            
                self.LogInternalError("LogCurrentStackTrace: " + str(ex))


    def LogCurrentThread(self, level:SILevel=None, title:str=None, colorValue:int=None) -> None:
        """
        Logs information about the current thread with a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs information about the current thread. This
        includes its name, its current state and more.

        LogCurrentThread is especially useful in a multi-threaded
        program like in a network server application. By using this
        method you can easily track all threads of a process and
        obtain detailed information about them.

        See LogThread for a more general method which can handle any thread.
        public void LogCurrentThread(Level level, string title)
        """
        if (self.IsOn(level)):

            # get reference to the current thread.
            thread:Thread = currentThread()

            # set default title if one was not supplied.
            if ((title == None) or (len(title) == 0)):
                title = self.__GetThreadTitle(thread, "Current thread info:")

            # call LogThread method to do the rest.
            self.LogThread(level, title, thread, colorValue)


    def LogCustomContext(self, level:SILevel=None, title:str=None, lt:LogEntryType=None, ctx:ViewerContext=None, colorValue:int=None) -> None:
        """
        Logs a custom viewer context with a custom log level.
        viewer ID and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            lt (LogEntryType):
                The custom Log Entry type.
            ctx (ViewerContext):
                The viewer context which holds the actual data and the appropriate viewer ID.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        if (self.IsOn(level)):
        
            try:
           
                if (ctx == None):
                    self.LogInternalError("LogCustomContext: ctx argument is null.");
                else:
                    self.__SendContext(level, title, lt, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogCustomContext: " + str(ex))


    def LogCustomFile(self, level:SILevel=None, title:str=None, fileName:str=None, lt:LogEntryType=None, vi:ViewerId=None, colorValue:int=None) -> None:
        """
        Logs the content of a file using a custom
        Log Entry type, viewer ID and title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The file to log.
            lt (LogEntryType)
                The custom Log Entry type.
            vi (ViewerId):
                The custom viewer ID which specifies the way the Console
                handles the file content.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the content of the supplied file using a
        custom Log Entry type and viewer ID. The parameters control
        the way the content of the file is displayed in the Console.
        Thus you can extend the functionality of the SmartInspect
        library with this method.
        """
        if (self.IsOn(level)):
        
            ctx:BinaryContext = BinaryContext(vi)
            try:
            
                ctx.LoadFromFile(fileName)
                self.__SendContext(level, title, lt, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogCustomFile: " + str(ex))


    def LogCustomReader(self, level:SILevel=None, title:str=None, reader:TextIOWrapper=None, lt:LogEntryType=None, vi:ViewerId=None, colorValue:int=None) -> None:
        """
        Logs the content of a text reader using a custom Log
        Entry type and viewer ID and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            reader (TextIOWrapper):
                The text reader to log.
            lt (LogEntryType):
                The custom Log Entry type.
            vi (ViewerId):
                The custom viewer ID which specifies the way the Console
                handles the reader content.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the content of the supplied reader using 
        custom Log Entry type and viewer ID. The parameters control
        the way the content of the reader is displayed in the Console.
        Thus you can extend the functionality of the SmartInspect
        library with this method.
        """
        if (self.IsOn(level)):
        
            ctx:TextContext = TextContext(vi)
            try:
            
                ctx.LoadFromReader(reader)
                self.__SendContext(level, title, lt, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogCustomReader: " + str(ex))


    def LogCustomStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, lt:LogEntryType=None, vi:ViewerId=None, colorValue:int=None) -> None:
        """
        Logs the content of a stream using a custom Log
        Entry type and viewer ID and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedReader):
                The stream to log (BufferedReader).
            lt (LogEntryType):
                The custom Log Entry type.
            vi (ViewerId):
                The custom viewer ID which specifies the way the Console
                handles the stream content.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the content of the supplied stream using a
        custom Log Entry type and viewer ID. The parameters control
        the way the content of the stream is displayed in the Console.
        Thus you can extend the functionality of the SmartInspect
        Python library with this method.
        """
        if (self.IsOn(level)):
        
            ctx:BinaryContext = BinaryContext(vi)
            try:
            
                ctx.LoadFromStream(stream)
                self.__SendContext(level, title, lt, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogCustomStream: " + str(ex))


    def LogCustomText(self, level:SILevel=None, title:str=None, text:str=None, lt:LogEntryType=None, vi:ViewerId=None, colorValue:int=None) -> None:
        """
        Logs custom text using a custom Log Entry type and
        viewer ID and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            text (str):
                The text to log.
            lt (LogEntryType):
                The custom Log Entry type.
            vi (ViewerId):
                The custom viewer ID which specifies the way the Console
                handles the text content.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        if (self.IsOn(level)):
        
            ctx:TextContext = TextContext(vi)
            try:
            
                ctx.LoadFromText(text)
                self.__SendContext(level, title, lt, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogCustomText: " + str(ex))


    def LogDateTime(self, level:SILevel=None, name:str=None, value:datetime=None, colorValue:int=None) -> None:
        """
        Logs a datetime value with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (str):
                The variable value.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a datetime variable.
        A title like "name = 05/15/2023 02:15:30 PM" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogDateTime: name argument is null.")
                return

            try:

                # send log entry packet.
                title:str = str.format("{0} = {1}", name, str(value))
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogDateTime: " + str(ex))


    def LogDebug(self, title:str, *args, colorValue:int=None) -> None:
        """
        Logs a debug message with a log level of Level.Debug.

        Args:
            title (str):
                The message to log.
            *args:
                Format arguments for the title argument.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        if (self.IsOn(SILevel.Debug)):

            try:
                
                # format title if *args was supplied.
                if (title) and (args):
                    title = (title % args)

                # send the packet.
                self.__SendLogEntry(SILevel.Debug, title, LogEntryType.Debug, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogDebug: " + str(ex))


    def LogDictionary(self, level:SILevel=None, title:str=None, oDict:dict=None, colorValue:int=None) -> None:
        """
        Logs the content of a dictionary with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console; "Current stack trace" is used if one is not supplied.
            oDict (dict):
                The dictionary to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method iterates through the supplied dictionary and calls ObjectRenderer.RenderObject to
        render every key/value pair into a string. These pairs will be displayed in a key/value viewer 
        in the Console.
        """
        if (self.IsOn(level)):

            if (oDict == None):
                self.LogInternalError("LogDictionary: oDict argument is null.")
                return

            ctx:ValueListViewerContext = ValueListViewerContext()

            try:
            
                # add all keys and values to the context viewer.
                for key in oDict.keys():

                    val:object = oDict[key]

                    if (key == oDict):
                        strKey = "<cycle>"
                    else:
                        strKey = ObjectRenderer.RenderObject(key)

                    if (val == oDict):
                        strVal = "<cycle>"
                    else:
                        strVal = ObjectRenderer.RenderObject(val)

                    ctx.AppendKeyValue(strKey, strVal)

                # send the packet.
                self.__SendContext(level, title, LogEntryType.Text, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogDictionary: " + str(ex))


    def LogComplex(self, level:SILevel=None, name:str=None, value:complex=None, colorValue:int=None) -> None:
        """
        Logs a complex value with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (float):
                The variable value.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a complex variable.
        A title like "name = 3.14159" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogComplex: name argument is null.")
                return

            try:

                # send log entry packet.
                title:str = str.format("{0} = {1}", name, str(value))
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogComplex: " + str(ex))


    def LogEnumerable(self, level:SILevel=None, title:str=None, oList:list=None, colorValue:int=None) -> None:
        """
        Logs the content of a list with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console; "Current stack trace" is used if one is not supplied.
            oList (list):
                The list to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method iterates through the supplied list and calls ObjectRenderer.RenderObject to
        render every element into a string. These elements will be displayed in a listview in the Console.
        """
        if (self.IsOn(level)):

            if (oList == None):
                self.LogInternalError("LogEnumerable: oList argument is null.")
                return

            ctx:ListViewerContext = ListViewerContext()

            try:
            
                # add all items to the context viewer.
                for item in oList:

                    if (item == oList):
                        ctx.AppendLine("<cycle>")
                    else:
                        ctx.AppendLine(ObjectRenderer.RenderObject(item))

                # send the packet.
                self.__SendContext(level, title, LogEntryType.Text, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogEnumerable: " + str(ex))


    def LogError(self, title:str, *args, colorValue:int=None) -> None:
        """
        Logs a error message with a log level of Level.Error.

        Args:
            title (str):
                The message to log.
            *args:
                Format arguments for the title argument.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        if (self.IsOn(SILevel.Error)):

            try:
                
                # format title if *args was supplied.
                if (title) and (args):
                    title = (title % args)

                # send the packet.
                self.__SendLogEntry(SILevel.Error, title, LogEntryType.Error, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogError: " + str(ex))


    def LogException(self, title:str=None, ex:Exception=None, colorValue:int=None):
        """
        Logs the content of an exception with a custom
        title and a log level of Level.Error.
        
        Args:
            title (str):
                The title to display in the Console.
            ex (Exception):
                The exception to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        
        This method extracts the exception message and stack trace
        from the supplied exception and logs an error with this data.
        It is especially useful if you place calls to this method in
        exception handlers. See LogError for a more general method
        with a similar intention.

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sessionref.md
        try:
            logsi.LogMessage("Forcing a divide by zero error ...")
            1/0   # force an exception
            logsi.LogMessage("You should not see this message due to the above exception.")
        except Exception as ex:
            logsi.LogException("*** Caught exception!", ex)
            logsi.LogException(None, ex)
        ```
        </details>
        """
        if (self.IsOn(SILevel.Error)):
            
            if (ex == None):
                self.LogInternalError("LogException: ex argument is null.")
            else:

                try:

                    # capture exception details to string via standard Python (temporary) logger.
                    # we first clear the stream, then capture the recent exception details.
                    self.__fTempLoggingStream.seek(0)
                    self.__fTempLoggingStream.truncate(0)
                    self.__fTempLogger.exception(ex,exc_info=True)
                    self.__fTempLoggingStream.flush()
                    errdtls:str = self.__fTempLoggingStream.getvalue()

                    # if title not specified, then use the exception string as a title.                    
                    if (title == None):
                        title = str(ex)

                    # prepare a custom context with the exception details and traceback info.
                    ctx:DataViewerContext = DataViewerContext()
                    ctx.LoadFromText(errdtls)

                    # send the packet.
                    self.__SendContext(SILevel.Error, title, LogEntryType.Error, ctx, colorValue)
                    
                except Exception as ex2:
                    
                    self.LogInternalError("LogException: " + str(ex2))


    def LogFatal(self, title:str, *args, colorValue:int=None) -> None:
        """
        Logs a fatal error message with a log level of Level.Fatal.

        Args:
            title (str):
                The message to log.
            *args:
                Format arguments for the title argument.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method is ideally used in error handling code such as
        exception handlers. If this method is used consequently, it
        is easy to troubleshoot and solve bugs in applications or
        configurations. See LogError for a method which does not
        describe fatal but recoverable errors.

        <details>
            <summary>View Sample Code</summary>
        ```python
        .. include:: ../docs/include/samplecode_sessionref.md
        logsi.LogFatal("This is a fatal error message in RED.", KnownColorValues.Red.value)
        logsi.LogFatal("This is a fatal error message in regular background color.")
        ```
        </details>
        """
        if (self.IsOn(SILevel.Fatal)):

            try:
                
                # format title if *args was supplied.
                if (title) and (args):
                    title = (title % args)

                # send the packet.
                self.__SendLogEntry(SILevel.Fatal, title, LogEntryType.Fatal, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogFatal: " + str(ex))


    def LogFloat(self, level:SILevel=None, name:str=None, value:float=None, colorValue:int=None) -> None:
        """
        Logs a float value with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (float):
                The variable value.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a float variable.
        A title like "name = 3.14159" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogFloat: name argument is null.")
                return

            try:

                # send log entry packet.
                title:str = str.format("{0} = {1}", name, str(value))
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogFloat: " + str(ex))


    def LogHtml(self, level:SILevel=None, title:str=None, html:str=None, colorValue:int=None) -> None:
        """
        Logs HTML code with a custom log level and
        displays it in a web browser.
        
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            html (str):
                The HTML source code to display.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        
        This method logs the supplied HTML source code. The source
        code is displayed as a website in the web viewer of the Console.
        """
        self.LogCustomText(level, title, html, LogEntryType.WebContent, ViewerId.Web, colorValue)


    def LogHtmlFile(self, level:SILevel=None, title:str=None, fileName:str=None, colorValue:int=None) -> None:
        """
        Logs an HTML file and displays the content in a
        web browser using a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The HTML file to display.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the HTML source code of the supplied file. The
        source code is displayed as a website in the web viewer of the Console. 
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.WebContent, ViewerId.Web, colorValue)


    def LogHtmlReader(self, level:SILevel=None, title:str=None, reader:TextIOWrapper=None, colorValue:int=None) -> None:
        """
        Logs a text reader with a custom log level and displays
        the content in a web browser.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            reader (TextIOWrapper):
                The text reader to display (TextReader).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the HTML source code of the supplied reader.
        The source code is displayed as a website in the web viewer of
        the Console.
        """
        self.LogCustomReader(level, title, reader, LogEntryType.WebContent, ViewerId.Web, colorValue)


    def LogHtmlStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a stream with a custom log level and displays
        the content in a web browser.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedReader):
                The stream to display.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the HTML source code of the supplied stream.
        The source code is displayed as a website in the web viewer of
        the Console. 
        """
        self.LogCustomStream(level, title, stream, LogEntryType.WebContent, ViewerId.Web, colorValue)


    def LogIconFile(self, level:SILevel=None, title:str=None, fileName:str=None, colorValue:int=None) -> None:
        """
        Logs a Windows icon file and displays it in the
        Console using a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The Windows icon file to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.Graphic, ViewerId.Icon, colorValue)


    def LogIconStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a stream with a custom log level and
        interprets its content as Windows icon.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedReader):
                The stream to display as Windows icon.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Graphic, ViewerId.Icon, colorValue)


    def LogInt(self, level:SILevel=None, name:str=None, value:int=None, includeHex:bool=False, colorValue:int=None) -> None:
        """
        Logs an integer value with an optional hexadecimal representation 
        and custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (int):
                The variable value.
            includeHex (bool):
                Indicates if a hexadecimal representation should be included (True) or not (False).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a integer variable.
        A title like "name = 10" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogInt: name argument is null.")
                return

            try:

                vhex:str = ""
                if (includeHex):
                    vhex = " (" + hex(value).upper() + ")"
                    if (value < 0):
                        vhex = vhex.replace("-","")     # remove minus sign for negative values.
                    vhex = vhex.replace("0X","0x")      # make "0X" lower-case since hex values will be in upper-case

                # send log entry packet.
                title:str = str.format("{0} = {1}{2}", name, str(value), vhex)
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogInt: " + str(ex))


    def LogInternalError(self, title:str, colorValue:int=None) -> None:
        """
        Logs an internal error with a log level of Level.Error.

        Args:
            title (str):
                A string which describes the internal error.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs an internal error. Such errors can occur
        if session methods are invoked with invalid arguments. For
        example, if you pass an invalid format string to LogMessage,
        the exception will be caught and an internal error with the
        exception message will be sent.

        This method is also intended to be used in derived classes
        to report any errors in your own methods.
        """
        if (self.IsOn(SILevel.Error)):
            self.__SendLogEntry(SILevel.Error, title, LogEntryType.InternalError, ViewerId.Title, colorValue)


    def LogJpegFile(self, level:SILevel=None, title:str=None, fileName:str=None, colorValue:int=None) -> None:
        """
        Logs a JPEG file and displays it in the Console
        using a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The JPEG file to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.Graphic, ViewerId.Jpeg, colorValue)


    def LogJpegStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a stream with a custom log level and
        interprets its content as JPEG image.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BuffereReader):
                The stream to display as JPEG image.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Graphic, ViewerId.Jpeg, colorValue)


    def LogMessage(self, title:str, *args, colorValue:int=None) -> None:
        """
        Logs a message with a log level of Level.Message.

        Args:
            title (str):
                The message to log.
            *args:
                Format arguments for the title argument.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        if (self.IsOn(SILevel.Message)):

            try:
                
                # format title if *args was supplied.
                if (title) and (args):
                    title = (title % args)

                # send the packet.
                self.__SendLogEntry(SILevel.Message, title, LogEntryType.Message, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogMessage: " + str(ex))


    def LogMetafileFile(self, level:SILevel=None, title:str=None, fileName:str=None, colorValue:int=None) -> None:
        """
        Logs a Windows Metafile file and displays it in
        the Console using a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The Windows Metafile file to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.Graphic, ViewerId.Metafile, colorValue)


    def LogMetafileStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a stream with a custom log level and
        interprets its content as Windows Metafile image.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedReader):
                The stream to display as Windows Metafile image.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Graphic, ViewerId.Metafile, colorValue)


    def LogObject(self, level:SILevel=None, title:str=None, instance:object=None, excludeNonPublic:bool=False, excludeBuiltIn:bool=True, excludeFunctions:bool=True, colorValue:int=None) -> None:
        """
        Logs fields and properties of an object with a custom log level. 
        Lets you specify if non public members should also be logged.
        
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            instance (object):
                The object whose fields and properties should be logged.
            excludeNonPublic (bool):
                Specifies if non public member items (e.g. "_x" prefix) should 
                be excluded from the log data.
            excludeBuiltIn (bool):
                Specifies if non public "built-in" member items (e.g. "__x" prefix) should 
                be excluded from the log data.
            excludeFunctions (bool):
                Specifies if routine, function, and method data is included in the log data.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs all field and property names and their
        current values of an object. These key/value pairs will be
        displayed in the Console in an object inspector like viewer.

        You can specify if non public or only public members should
        be logged by setting the excludeNonPublic argument to true or false,
        respectively.
        """
        if (not self.IsOn(level)):
            return

        if (instance == None):
            self.LogInternalError("LogObject: instance argument is null.")
            return

        try:

            ctx:InspectorViewerContext = InspectorViewerContext()
            instanceType = type(instance)
            iList:list[str] = []

            # Example of inspect.getmembers(instance, None) output:
            # - PropertyBool : True
            # - PropertyString : 'This is a string property value'
            # - PublicEvent : <bound method InstanceGetMembersTestClass.PublicEvent of <__main__.InstanceGetMembersTestClass object at 0x0000026B84569AC0>>
            # - PublicFunctionString : <bound method InstanceGetMembersTestClass.PublicFunctionString of <__main__.InstanceGetMembersTestClass object at 0x0000026B84569AC0>>
            # - PublicMethod : <bound method InstanceGetMembersTestClass.PublicMethod of <__main__.InstanceGetMembersTestClass object at 0x0000026B84569AC0>>
            # - PublicStaticFunction : <function InstanceGetMembersTestClass.PublicStaticFunction at 0x0000026B859F1EE0>
            # - PublicStaticMethod : <function InstanceGetMembersTestClass.PublicStaticMethod at 0x0000026B859F1E50>
            # - STATIC_VAR_BOOL : True
            # - STATIC_VAR_INT : 69
            # - STATIC_VAR_STRING : 'Static String'
            # - _InstanceGetMembersTestClass__fPropertyBool : True
            # - _InstanceGetMembersTestClass__fPropertyBoolDynamic : True
            # - _InstanceGetMembersTestClass__fPropertyString : 'This is a string property value'
            # - _InstanceGetMembersTestClass__fPropertyStringDynamic : 'This is a INTERNAL string property value'

            # --------------------------------------------------------------------------------------------------
            # get all members of the instance and add field types to the context viewer.
            # --------------------------------------------------------------------------------------------------
            members = inspect.getmembers(instance, None)
            self.__LogObjectBuildContext("Fields", instance, members, ctx, excludeNonPublic, excludeBuiltIn, True, True)

            # --------------------------------------------------------------------------------------------------
            # get all properties decorated with "@property" attribute.
            # --------------------------------------------------------------------------------------------------
            members = inspect.getmembers(type(instance), lambda o: isinstance(o, property)) 

            # add member data to context viewer.
            for name, data in members:

                sb:str = ""

                try:

                    # map the property object.
                    propobj:property = data

                    # try to determine if this is a "private" property.  if the "fget()"
                    # method of the property definition contains a "._" value then it usually
                    # indicates a "private" property. 
                    # Example fget, private property: '<function Session.__IsStored at 0x000001FCEDE96550>'
                    # Example fget, public  property: '<function Session.Active at 0x000001FCEDE75650>'

                    propobjfgetdef = str(propobj.fget)
                    if (propobjfgetdef != None):
                        if (propobjfgetdef.find("._") != -1):
                            if (excludeNonPublic):
                                continue
            
                    sb += ctx.EscapeItem(name)
                    sb += "="
                    sb += ctx.EscapeItem(ObjectRenderer.RenderObject(propobj.fget(instance)))
            
                except Exception as ex:
            
                    sb += "<not accessible>"

                # add context entry to the list.
                iList.append(sb)
                sb = ""

            # sort context items - the member name is the first thing displayed
            # in the item, so the list is sorted by member name.
            # note that in Python, UPPER-case items are sorted above lower-case items,
            # so we use the "key=str.lower) syntax to force the case-insensitive sort.
            iList.sort(key=str.lower)

            # begin a new group and append the list to the inspector context.
            ctx.StartGroup("Properties")
            for line in iList:
                ctx.AppendLine(str(line))

            iList.clear()

            # --------------------------------------------------------------------------------------------------
            # get everything else about the instance.
            # --------------------------------------------------------------------------------------------------

            # are we including routines, functions, and methods?
            if (not excludeFunctions):

                # get routine members (e.g. non-static methods) of the instance and add field types to the context viewer.
                members = inspect.getmembers(instance, predicate=inspect.isroutine)
                self.__LogObjectBuildContext("Routines", instance, members, ctx, excludeNonPublic, excludeBuiltIn, False)

                # get function members (e.g. static methods) of the instance and add field types to the context viewer.
                members = inspect.getmembers(instance, predicate=inspect.isfunction)
                self.__LogObjectBuildContext("Functions", instance, members, ctx, excludeNonPublic, excludeBuiltIn, False)

                # get method members (e.g. non-static methods) of the instance and add field types to the context viewer.
                members = inspect.getmembers(instance, predicate=inspect.ismethod)
                self.__LogObjectBuildContext("Methods", instance, members, ctx, excludeNonPublic, excludeBuiltIn, False)

            # send the packet.
            self.__SendContext(level, title, LogEntryType.Object, ctx, colorValue);

        except Exception as ex:
                
            self.LogInternalError("LogObject: " + str(ex))


    def LogObjectValue(self, level:SILevel=None, name:str=None, value:object=None, colorValue:int=None) -> None:
        """
        Logs a object value with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (object):
                The variable value.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a object variable.
        A title like "name = My Object" will be displayed in the Console.
        If the value is null, then a title like "name = null" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogObject: name argument is null.")
                return

            try:

                # send log entry packet.
                title:str = ""
                if (value == None):
                    title = str.format("{0} = null", name)
                else:
                    title = str.format("{0} = {1}", name, str(value))
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogObject: " + str(ex))


    def LogPngFile(self, level:SILevel=None, title:str=None, fileName:str=None, colorValue:int=None) -> None:
        """
        Logs a PNG file and displays it in the Console
        using a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The PNG file to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        Note that this method is only supported in the SI Console Viewer v3.4+.  Previous versions
        of the Si Console will display "A viewer for the selected Log Entry could not be found" error.
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.Graphic, ViewerId.Png, colorValue)


    def LogPngStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a stream with a custom log level and
        interprets its content as PNG image.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BuffereReader):
                The stream to display as PNG image.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        Note that this method is only supported in the SI Console Viewer v3.4+.  Previous versions
        of the Si Console will display "A viewer for the selected Log Entry could not be found" error.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Graphic, ViewerId.Png, colorValue)


    def LogReader(self, level:SILevel=None, title:str=None, reader:TextIOWrapper=None, colorValue:int=None) -> None:
        """
        Logs a reader with a custom log level and
        displays the content in a read-only text field.
        
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            reader (TextIOWrapper):
                The text reader to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomReader(level, title, reader, LogEntryType.Text, ViewerId.Data, colorValue)


    def LogSeparator(self, level:SILevel=None, colorValue:int=None) -> None:
        """
        Logs a simple separator with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method instructs the Console to draw a separator.
        A separator is intended to group related LogEntry
        and to separate them visually from others. This
        method can help organizing Log Entries in the Console.
        """
        if (self.IsOn(level)):
            self.__SendLogEntry(level, "", LogEntryType.Separator, ViewerId.NoViewer, colorValue)


    def LogSource(self, level:SILevel=None, title:str=None, source:str=None, id:SourceId=None, colorValue:int=None) -> None:
        """
        Logs source code that is displayed with syntax
        highlighting in the Console using a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            source (str):
                The source code to log.
            id (SourceId):
                Specifies the type of source code.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method displays the supplied source code with syntax
        highlighting in the Console. The type of the source code can be
        specified by the 'id' argument. Please see the SourceId enum for
        information on the supported source code types.
        """
        self.LogCustomText(level, title, source, LogEntryType.Source, id, colorValue)


    def LogSourceFile(self, level:SILevel=None, title:str=None, fileName:str=None, id:SourceId=None, colorValue:int=None) -> None:
        """
        Logs the content of a file as source code with
        syntax highlighting using a custom title and custom log
        level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The name of the file which contains the source code.
            id (SourceId):
                Specifies the type of source code.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method displays the source file with syntax highlighting
        in the Console. The type of the source code can be specified by
        the 'id' argument. Please see the SourceId enum for information
        on the supported source code types.
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.Source, id, colorValue)        


    def LogSourceReader(self, level:SILevel=None, title:str=None, reader:TextIOWrapper=None, id:SourceId=None, colorValue:int=None) -> None:
        """
        Logs the content of a text reader as source code with
        syntax highlighting using a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            reader (TextIOWrapper):
                The text reader which contains the source code.
            id (SourceId):
                Specifies the type of source code.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method displays the content of a reader with syntax
        highlighting in the Console. The type of the source code can be
        specified by the 'id' argument. Please see the SourceId enum for
        information on the supported source code types.
        """
        self.LogCustomReader(level, title, reader, LogEntryType.Source, id, colorValue)


    def LogSourceStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, id:SourceId=None, colorValue:int=None) -> None:
        """
        Logs the content of a stream as source code with
        syntax highlighting using a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedReader):
                The stream which contains the source code.
            id (SourceId):
                Specifies the type of source code.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method displays the content of a stream with syntax
        highlighting in the Console. The type of the source code can be
        specified by the 'id' argument. Please see the SourceId enum for
        information on the supported source code types.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Source, id, colorValue)


    def LogSql(self, level:SILevel=None, title:str=None, source:str=None, colorValue:int=None) -> None:
        """
        Logs a string containing SQL source code with a
        custom log level. The SQL source code is displayed with syntax
        highlighting in the Console.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            source (str):
                The SQL source code to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method displays the supplied SQL source code with syntax
        highlighting in the Console.

        It is especially useful to debug or track dynamically generated
        SQL source code.
        """
        self.LogSource(level, title, source, SourceId.Sql, colorValue)


    def LogSqliteDbCursorData(self, level:SILevel=None, title:str=None, cursor:sqlite3.Cursor=None, colorValue:int=None) -> None:
        """
        Logs the contents of a Sqlite Cursor with a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            cursor (Cursor):
                The cursor data to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs all data of the supplied cursor, using a "for row in cursor:" statement.
        Note that this WILL move the position of the cursor, and the position is not restored.
        """
        if (not self.IsOn(level)):
            return

        methodName:str = "LogSqliteDbCursorData"

        if (cursor == None):
            self.LogInternalError("{0}: cursor argument is null.".format(methodName))
            return

        # default title if one was not supplied.
        if (title == None) or (len(title) == 0):
            title = "Sqlite Cursor Data"

        # sqllite cursor description is a tuple (of 7 items) containing the description of columns.
        # as of this writing, only the first tuple index item is populated, which is the column name.
        columns:list[(str,None,None,None,None,None,None)] = cursor.description
        if (columns == None):
            self.LogInternalError("{0}: cursor did not return any rows.".format(methodName))
            return;

        ctx:TableViewerContext = TableViewerContext()

        try:
        
            # formulate column header (e.g. "Col1", "Col2", etc).
            sb:str = ""
            for column in columns:
                sb += "\"{0}\", ".format(column[0])

            # drop the ending comma-space delimiter from the built string.
            sb = sb[:-2]

            # write the column header.
            ctx.AppendHeader(sb)

            # write all rows in the cursor.
            rowcnt:int = 0
            for row in cursor:

                # add column data for the row to the context view.
                ctx.BeginRow()
                for i in range(len(columns)):
                    ctx.AddRowEntry(str(row[i]))
                ctx.EndRow()
                rowcnt = rowcnt + 1

            # modify the title with the data row count.
            title += " ({0} rows)".format(str(rowcnt))

            # send the packet.
            self.__SendContext(level, title, LogEntryType.DatabaseStructure, ctx, colorValue)
        
        except Exception as ex:
            
            self.LogInternalError("{0}: {1}".format(methodName, str(ex)))


    def LogSqliteDbSchemaCursor(self, level:SILevel=None, title:str=None, cursor:sqlite3.Cursor=None, colorValue:int=None) -> None:
        """
        Logs the schema of a Sqlite Cursor with a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            cursor (Cursor):
                The cursor schema to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the schema of the supplied cursor, by querying its "description" property value.  
        It does not move the position of the cursor.

        A cursor schema contains the name of every column in the cursor.
        Note that this data could be different than what is actually defined in the database table that
        the schema is derived from, as the SELECT statement used to query the database could limit the 
        columns returned.
        """
        if (not self.IsOn(level)):
            return

        if (cursor == None):
            self.LogInternalError("LogSqliteCursorSchema: cursor argument is null.")
            return

        # default title if one was not supplied.
        if (title == None) or (len(title) == 0):
            title = "Sqlite Cursor Schema"

        # sqllite cursor description is a list (7 items) containing the description of columns.
        # as of this writing, only the first (of 7) list items is populated, which is the column name.
        columns:list[(str,None,None,None,None,None,None)] = cursor.description
        if (columns == None):
            self.LogInternalError("LogSqliteCursorSchema: table is empty.");
            return;

        ctx:TableViewerContext = TableViewerContext()

        try:
        
            # write the header first.
            ctx.AppendHeader("\"Column Name\"")

            # write the columns.
            for column in columns:

                # map the column schema.
                sColName:str = str(column[0])

                # add column info to the context view.
                ctx.BeginRow()
                ctx.AddRowEntry(sColName)
                ctx.EndRow()

            # send the packet.
            self.__SendContext(level, title, LogEntryType.DatabaseStructure, ctx, colorValue)
        
        except Exception as ex:
            
            self.LogInternalError("LogSqliteCursorSchema: " + str(ex))


    def LogSqliteDbSchemaForeignKeyList(self, level:SILevel=None, title:str=None, conn:sqlite3.Connection=None, tableName:str=None, sortByName:bool=False, colorValue:int=None) -> None:
        """
        Logs the schema of a Sqlite DB Table Foreign Key List with a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            conn (Connection):
                Sqlite database connection object.
            tableName (str):
                The name of the table to obtain schema information for.
            sortByName (bool):
                Sorts the log data by Table Name (True) or by ID (False, default).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method queries the schema information by executing the following SQL statement:
        "SELECT * FROM pragma_foreign_key_list('<tablename>');"

        This will log the following details returned from the schema information query:
        ID, Sequence, Table, From, To, On Update, On Delete, Match
        """
        if (not self.IsOn(level)):
            return

        methodName:str = "LogSqliteDbSchemaForeignKeyList"

        if (conn == None):
            self.LogInternalError("{0}: conn argument is null.".format(methodName))
            return

        if ((tableName == None) or (len(tableName) == 0)):
            self.LogInternalError("{0}: tableName argument is null or an empty string.".format(methodName))
            return

        # default title if one was not supplied.
        if (title == None) or (len(title) == 0):
            title = "Sqlite DB Schema Information: Table \"{0}\" - Foreign Key List".format(tableName)
            if (sortByName):
                title += " (sorted by table name)"

        tblSchema:list = None

        try:

            # more info on the return results of this schema query can be found here:
            # https://www.sqlite.org/pragma.html#pragma_foreign_key_list

            # sql to query db for schema info.
            sql:str = "SELECT * FROM pragma_foreign_key_list('{0}');".format(tableName)

            # execute sql.
            cursor:sqlite3.Cursor = conn.execute(sql)
            tblSchema = cursor.fetchall()

            # results contain information about the table foreign key list:
            # id, seq, table, from, to, on_update, on_delete, match
            if ((tblSchema == None) or (len(tblSchema)) == 0):
                self.LogInternalError("{0}: table name \"{1}\" does not exist.".format(methodName, tableName));
                return;

            # sort schema info by colum name if requested.
            if (sortByName):
                tblSchema.sort(key=lambda x: x[2])
            
        except Exception as ex:
            
            self.LogInternalError("{0}: DB Schema Foreign Key List Error for table \"{1}\" - {2}".format(methodName, tableName, str(ex)))
            return

        ctx:TableViewerContext = TableViewerContext()

        try:
        
            # write the header first.
            ctx.AppendHeader("ID, Sequence, Table, From, To, \"On Update\", \"On Delete\", Match")

            # write the columns.
            for column in tblSchema:

                # map the column schema.
                sColId:str = str(column[0])
                sColSeq:str = str(column[1])
                sColTable:str = str(column[2])
                sColFrom:str = str(column[3])
                sColTo:str = str(column[4])
                sColOnUpdate:str = str(column[5])
                sColOnDelete:str = str(column[6])
                sColMatch:str = str(column[7])

                # add column info to the context view.
                ctx.BeginRow()
                ctx.AddRowEntry(sColId)
                ctx.AddRowEntry(sColSeq)
                ctx.AddRowEntry(sColTable)
                ctx.AddRowEntry(sColFrom)
                ctx.AddRowEntry(sColTo)
                ctx.AddRowEntry(sColOnUpdate)
                ctx.AddRowEntry(sColOnDelete)
                ctx.AddRowEntry(sColMatch)
                ctx.EndRow()

            # send the packet.
            self.__SendContext(level, title, LogEntryType.DatabaseStructure, ctx, colorValue)
        
        except Exception as ex:
            
            self.LogInternalError("{0}: {1}".format(methodName, str(ex)))


    def LogSqliteDbSchemaIndexList(self, level:SILevel=None, title:str=None, conn:sqlite3.Connection=None, tableName:str=None, sortByName:bool=False, colorValue:int=None) -> None:
        """
        Logs the schema of a Sqlite DB Table Index List with a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            conn (Connection):
                Sqlite database connection object.
            tableName (str):
                The name of the table to obtain schema information for.
            sortByName (bool):
                Sorts the log data by Index Name (True) or by ID (False, default).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method queries the schema information by executing the following SQL statement:
        "SELECT * FROM pragma_index_list('<tablename>');"

        This will log the following details returned from the schema information query:
        Sequence, Name, Unique, Origin, Partial
        """
        if (not self.IsOn(level)):
            return

        methodName:str = "LogSqliteDbSchemaIndexList"

        if (conn == None):
            self.LogInternalError("{0}: conn argument is null.".format(methodName))
            return

        if ((tableName == None) or (len(tableName) == 0)):
            self.LogInternalError("{0}: tableName argument is null or an empty string.".format(methodName))
            return

        # default title if one was not supplied.
        if (title == None) or (len(title) == 0):
            title = "Sqlite DB Schema Information: Table \"{0}\" - Index List".format(tableName)
            if (sortByName):
                title += " (sorted by index name)"

        tblSchema:list = None

        try:

            # more info on the return results of this schema query can be found here:
            # https://www.sqlite.org/pragma.html#pragma_index_list

            # sql to query db for schema info.
            sql:str = "SELECT * FROM pragma_index_list('{0}');".format(tableName)

            # execute sql.
            cursor:sqlite3.Cursor = conn.execute(sql)
            tblSchema = cursor.fetchall()

            # results contain information about the table foreign key list:
            # id, seq, table, from, to, on_update, on_delete, match
            if ((tblSchema == None) or (len(tblSchema)) == 0):
                self.LogInternalError("{0}: table name \"{1}\" does not exist.".format(methodName, tableName));
                return;

            # sort schema info by colum name if requested.
            if (sortByName):
                tblSchema.sort(key=lambda x: x[1])
            
        except Exception as ex:
            
            self.LogInternalError("{0}: DB Schema Index List Error for table \"{1}\" - {2}".format(methodName, tableName, str(ex)))
            return

        ctx:TableViewerContext = TableViewerContext()

        try:
        
            # write the header first.
            ctx.AppendHeader("Sequence, Name, \"Is Unique?\", Origin, \"Is Partial?\"")

            # write the columns.
            for column in tblSchema:

                # map the column schema.
                sColSeq:str = str(column[0])
                sColName:str = str(column[1])
                sColUnique:str = str(column[2])
                sColOrigin:str = str(column[3])
                sColPartial:str = str(column[4])

                # the "origin" column value signifies one of the following:
                # c  = index was created by a CREATE INDEX statement.
                # u  = index was created by a UNIQUE constraint.
                # pk = index was created by a PRIMARY KEY constraint.
                if (sColOrigin == "c"):
                    sColOrigin += " (CREATE INDEX)"
                elif (sColOrigin == "u"):
                    sColOrigin += " - (UNIQUE constraint)"
                elif (sColOrigin == "pk"):
                    sColOrigin += " - (PRIMARY KEY constraint)"

                # add column info to the context view.
                ctx.BeginRow()
                ctx.AddRowEntry(sColSeq)
                ctx.AddRowEntry(sColName)
                ctx.AddRowEntry(DataTypeHelper.BoolToStringYesNo(sColUnique))
                ctx.AddRowEntry(sColOrigin)
                ctx.AddRowEntry(DataTypeHelper.BoolToStringYesNo(sColPartial))
                ctx.EndRow()

            # send the packet.
            self.__SendContext(level, title, LogEntryType.DatabaseStructure, ctx, colorValue)
        
        except Exception as ex:
            
            self.LogInternalError("{0}: {1}".format(methodName, str(ex)))


    def LogSqliteDbSchemaTableInfo(self, level:SILevel=None, title:str=None, conn:sqlite3.Connection=None, tableName:str=None, sortByName:bool=False, colorValue:int=None) -> None:
        """
        Logs the schema of a Sqlite DB Table with a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            conn (Connection):
                Sqlite database connection object.
            tableName (str):
                The name of the table to obtain schema information for.
            sortByName (bool):
                Sorts the log data by Table Name (True) or by ID (False, default).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method queries the schema information by executing the following SQL statement:
        "SELECT * FROM pragma_table_info('<tablename>');"

        This will log the following details returned from the schema information query:
        - id, name, data type, not null, default value, primary key, hidden column.
        """
        if (not self.IsOn(level)):
            return

        methodName:str = "LogSqliteDbSchemaTableInfo"

        if (conn == None):
            self.LogInternalError("{0}: conn argument is null.".format(methodName))
            return

        if ((tableName == None) or (len(tableName) == 0)):
            self.LogInternalError("{0}: tableName argument is null or an empty string.".format(methodName))
            return

        # default title if one was not supplied.
        if (title == None) or (len(title) == 0):
            title = "Sqlite DB Schema Information: Table \"{0}\" - Table Info".format(tableName)
            if (sortByName):
                title += " (sorted by name)"

        tblSchema:list = None

        try:

            # more info on the return results of this schema query can be found here:
            # https://www.sqlite.org/pragma.html#pragma_table_xinfo

            # sql to query db for schema info.
            sql:str = "SELECT * FROM pragma_table_xinfo('{0}');".format(tableName)

            # execute sql.
            cursor:sqlite3.Cursor = conn.execute(sql)
            tblSchema = cursor.fetchall()

            # results contain information about the table.
            # 'cid', 'name', 'type', 'notnull', 'dflt_value', 'pk', 'hidden'
            if ((tblSchema == None) or (len(tblSchema)) == 0):
                self.LogInternalError("{0}: table name \"{1}\" does not exist.".format(methodName, tableName));
                return;

            # sort schema info by colum name if requested.
            if (sortByName):
                tblSchema.sort(key=lambda x: x[1])
            
        except Exception as ex:
            
            self.LogInternalError("{0}: DB Schema Table Info Error for table \"{1}\" - {2}".format(methodName, tableName, str(ex)))
            return

        ctx:TableViewerContext = TableViewerContext()

        try:
        
            # write the header first.
            ctx.AppendHeader("ID, \"Column Name\", Type, \"Not NULL?\", \"Default Value\", \"Is Primary Key?\", Hidden")

            # write the columns.
            for column in tblSchema:

                # map the column schema.
                sColId:str = str(column[0])
                sColName:str = str(column[1])
                sColType:str = str(column[2])
                sColNotNull:bool = bool(column[3])
                sColDefaultValue:str = ""
                if (column[4] != None):
                    sColDefaultValue = str(column[4])                   
                sColPrimaryKey:bool = bool(column[5])
                sColHidden:str = str(column[6])

                # the "hidden" column value signifies one of the following:
                # 0 = normal column
                # 1 = hidden column in a virtual table
                # 2 = dynamic column
                # 3 = stored generated column 
                if (sColHidden == "0"):
                    sColHidden += " (normal)"
                elif (sColHidden == "1"):
                    sColHidden += " - (virtual)"
                elif (sColHidden == "2"):
                    sColHidden += " - (dynamic)"
                elif (sColHidden == "3"):
                    sColHidden += " - (stored generated)"
                else:
                    sColHidden += " - unknown"

                # add column info to the context view.
                ctx.BeginRow()
                ctx.AddRowEntry(sColId)
                ctx.AddRowEntry(sColName)
                ctx.AddRowEntry(sColType)
                ctx.AddRowEntry(DataTypeHelper.BoolToStringYesNo(sColNotNull))
                ctx.AddRowEntry(sColDefaultValue)
                ctx.AddRowEntry(DataTypeHelper.BoolToStringYesNo(sColPrimaryKey))
                ctx.AddRowEntry(sColHidden)
                ctx.EndRow()

            # send the packet.
            self.__SendContext(level, title, LogEntryType.DatabaseStructure, ctx, colorValue)
        
        except Exception as ex:
            
            self.LogInternalError("{0}: {1}".format(methodName, str(ex)))


    def LogSqliteDbSchemaTables(self, level:SILevel=None, title:str=None, conn:sqlite3.Connection=None, sortByName:bool=False, colorValue:int=None) -> None:
        """
        Logs the schema table names defined in a Sqlite DB with a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            conn (Connection):
                Sqlite database connection object.
            sortByName (bool):
                Sorts the log data by Table Name (True) or by entry order (False, default).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method queries the schema information by executing the following SQL statement:
        "SELECT * FROM sqlite_schema WHERE type ='table';"

        This will log the following details returned from the schema information query:
        - type, name, tbl_name, rootpage, sql
        """
        if (not self.IsOn(level)):
            return

        methodName:str = "LogSqliteDbSchemaTables"

        if (conn == None):
            self.LogInternalError("{0}: conn argument is null.".format(methodName))
            return

        # default title if one was not supplied.
        if (title == None) or (len(title) == 0):
            title = "Sqlite DB Schema Information: Tables"
            if (sortByName):
                title += " (sorted by name)"

        tblSchema:list = None

        try:

            # more info on the return results of this schema query can be found here:
            # https://www.sqlitetutorial.net/sqlite-show-tables/

            # sql to query db for schema info.
            sql:str = "SELECT * FROM sqlite_schema WHERE type IN ('table','view');"

            # execute sql.
            cursor:sqlite3.Cursor = conn.execute(sql)
            tblSchema = cursor.fetchall()

            # results contain information about the table.
            # type, name, tbl_name, rootpage, sql
            if ((tblSchema == None) or (len(tblSchema)) == 0):
                self.LogInternalError("{0}: table list could not be queried.".format(methodName));
                return;

            # sort schema info by colum name if requested.
            if (sortByName):
                tblSchema.sort(key=lambda x: x[1])
            
        except Exception as ex:
            
            self.LogInternalError("{0}: DB Schema Table List Error - {1}".format(methodName, str(ex)))
            return

        ctx:TableViewerContext = TableViewerContext()

        try:
        
            # write the header first.
            ctx.AppendHeader("Type, Name, \"Table Name\", \"Root Page\", \"SQL\"")

            # write the columns.
            for column in tblSchema:

                # map the column schema.
                sColType:str = str(column[0])
                sColName:str = str(column[1])
                sColTableName:str = str(column[2])
                sColRootPage:str = str(column[3])
                sColSql:str = str(column[4])

                # add column info to the context view.
                ctx.BeginRow()
                ctx.AddRowEntry(sColType)
                ctx.AddRowEntry(sColName)
                ctx.AddRowEntry(sColTableName)
                ctx.AddRowEntry(sColRootPage)
                ctx.AddRowEntry(sColSql)
                ctx.EndRow()

            # send the packet.
            self.__SendContext(level, title, LogEntryType.DatabaseStructure, ctx, colorValue)
        
        except Exception as ex:
            
            self.LogInternalError("{0}: {1}".format(methodName, str(ex)))


    def LogStackTrace(self, level:SILevel=None, title:str=None, strace:list[FrameInfo]=None, startFrame:int=0, limit:int=None, colorValue:int=None) -> None:
        """
        Logs a stack trace with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            strace (object):
                 StackTrace instance to log.
            startFrame (int):
                The offset of the first frame preceding the caller to print (default 0).
            limit (int):
                The number of frames to print (specify None to print all remaining frames).
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the supplied stack trace. The resulting LogEntry contains all methods including the
        related classes lists. Furthermore the filename, line and columns numbers are included.
        """
        if (self.IsOn(level)):

            if (strace == None):
                self.LogInternalError("LogStackTrace: strace argument cannot be null.")
                return

            if (startFrame == None):
                startFrame = 0

            # default title if one was not supplied.
            if ((title == None) or (len(title) == 0)):
                title = "Stack trace"

            try:

                # create the context viewer.
                ctx:ListViewerContext = ListViewerContext()

                HEADER_FMT = "Call stack at {0}, line {1} in function {2}, frames {3} to {4} of {5}:"
                STACK_FMT = "{0}, line {1} in function {2}."

                # the caller stack frame is the specified starting frame in the list, as they control
                # what they want the starting point to be.
                callerFrame = strace[startFrame]

                # index of the first frame to print.
                begin = startFrame
    
                # index of the last frame to print.
                if limit:
                    end = min(begin + limit, len(strace))
                else:
                    end = len(strace)
    
                # write the caller stack frame header to the context viewer.
                file, line, func = callerFrame[1:4]
                sbhdr = str.format(HEADER_FMT, file, line, func, startFrame, end - 1, len(strace))
                ctx.AppendLine(sbhdr)

                # write the remaining stack frames to the context viewer (up to the specified limit).
                for frame in strace[begin:end]:

                    file, line, func = frame[1:4]
                    sbframe = str.format(STACK_FMT, file, line, func)
                    ctx.AppendLine(sbframe)

                # send the packet.
                self.__SendContext(level, title, LogEntryType.Text, ctx, colorValue)

            except Exception as ex:
            
                self.LogInternalError("LogStackTrace: " + str(ex))


    def LogStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a stream with a custom log level and displays
        the content in a read-only text field.
        
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedStream):
                The stream to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Text, ViewerId.Data, colorValue)


    def LogString(self, level:SILevel=None, name:str=None, value:str=None, colorValue:int=None) -> None:
        """
        Logs a string value with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (str):
                The variable value.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs the name and value of a string variable.
        A title like "name = \"Value\"" will be displayed in the Console.
        """
        if (self.IsOn(level)):

            # validations.
            if (name == None):
                self.LogInternalError("LogString: name argument is null.")
                return

            try:

                # send log entry packet.
                title:str = str.format("{0} = \"{1}\"", name, value)
                self.__SendLogEntry(level, title, LogEntryType.VariableValue, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogString: " + str(ex))


    def LogSystem(self, level:SILevel=None, title:str=None, colorValue:int=None) -> None:
        """
        Logs information about the system using a custom title and custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        The logged information include the version of the operating
        system, the Python version and more. This method is
        useful for logging general information at the program startup.
        This guarantees that the support staff or developers have
        general information about the execution environment.
        """
        if (self.IsOn(level)):

            # set default title if one was not supplied.
            if ((title == None) or (len(title) == 0)):
                title = "System Information"

            # get operating system bit depth.
            osbitdepth:str = "32-bit"
            if (sys.maxsize > 2**32):
                osbitdepth:str = "64-bit"

            ctx:InspectorViewerContext = InspectorViewerContext()

            try:
             
                ctx.StartGroup("Operating System Information");
                ctx.AppendKeyValue("Name", platform.system())
                ctx.AppendKeyValue("Version", platform.version())
                ctx.AppendKeyValue("Release", platform.release())
                ctx.AppendKeyValue("Platform", platform.platform())
                ctx.AppendKeyValue("Machine Architecture", platform.machine())
                ctx.AppendKeyValue("Bit Depth", osbitdepth)

                ctx.StartGroup("Machine Information");
                ctx.AppendKeyValue("Machine Name", platform.node())
                try:
                    ctx.AppendKeyValue("User Login", os.getlogin())
                except Exception as ex:
                    ctx.AppendKeyValue("User Login", "Error: " + str(ex))
                ctx.AppendKeyValue("Current directory", os.getcwd())

                ctx.StartGroup("Python Environment");
                ctx.AppendKeyValue("Version", platform.python_version())
                ctx.AppendKeyValue("Revision", platform.python_revision())
                ctx.AppendKeyValue("Build Date", str(platform.python_build()[1]))
                ctx.AppendKeyValue("Branch", platform.python_branch())
                ctx.AppendKeyValue("Compiler", platform.python_compiler())
                ctx.AppendKeyValue("Implementation", platform.python_implementation())

                # send the packet.
                self.__SendContext(level, title, LogEntryType.System, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogSystem: " + str(ex))


    def LogText(self, level:SILevel=None, title:str=None, text:str=None, colorValue:int=None) -> None:
        """
        Logs a string with a custom log level and displays
        it in a read-only text field.
        
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            text (str):
                The text to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomText(level, title, text, LogEntryType.Text, ViewerId.Data, colorValue)


    def LogTextFile(self, level:SILevel=None, title:str=None, fileName:str=None, colorValue:int=None) -> None:
        """
        Logs a text file and displays the content in a
        read-only text field using a custom title and custom log
        level.
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            fileName (str):
                The file to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomFile(level, title, fileName, LogEntryType.Text, ViewerId.Data, colorValue)


    def LogTextReader(self, level:SILevel=None, title:str=None, reader:TextIOWrapper=None, colorValue:int=None) -> None:
        """
        Logs a text reader with a custom log level and
        displays the content in a read-only text field.
        
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            reader (TextIOWrapper):
                The text reader to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomReader(level, title, reader, LogEntryType.Text, ViewerId.Data, colorValue)


    def LogTextStream(self, level:SILevel=None, title:str=None, stream:BufferedReader=None, colorValue:int=None) -> None:
        """
        Logs a stream with a custom log level and displays
        the content in a read-only text field.
        
        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            stream (BufferedStream):
                The stream to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        self.LogCustomStream(level, title, stream, LogEntryType.Text, ViewerId.Data, colorValue)


    def LogThread(self, level:SILevel=None, title:str=None, thread:Thread=None, colorValue:int=None) -> None:
        """
        Logs information about a thread with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title to display in the Console.
            thread (Thread):
                The thread to log.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method logs information about the supplied thread. This
        includes its name, its current state and more.

        LogThread is especially useful in a multi-threaded program
        like in a network server application. By using this method you
        can easily track all threads of a process and obtain detailed
        information about them.
        """
        if (self.IsOn(level)):

            if (thread == None):
                self.LogInternalError("LogThread: thread argument is null.")
                return

            # set default title if one was not supplied.
            if ((title == None) or (len(title) == 0)):
                title = self.__GetThreadTitle(thread, None)

            ctx:ValueListViewerContext = ValueListViewerContext()
        
            try:

                # gather information about the thread.           
                ctx.AppendKeyValue("Thread Name", thread.name)
                ctx.AppendKeyValue("Is Alive?", str(thread.is_alive()))

                if (thread.is_alive):
                
                    #ctx.AppendKeyValue("Priority", thread. .Priority.ToString())
                    ctx.AppendKeyValue("ID", str(thread.ident))
                    ctx.AppendKeyValue("Native ID", str(thread.native_id))
                    ctx.AppendKeyValue("Is Daemon?", str(thread.isDaemon()))

                # send the packet.
                self.__SendContext(level, title, LogEntryType.Text, ctx, colorValue)
            
            except Exception as ex:
            
                self.LogInternalError("LogThread: " + str(ex))


    def LogValue(self, level:SILevel=None, name:str=None, value=None, colorValue:int=None) -> None:
        """
        Logs the name and value of a variable with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The variable name.
            value (object):
                The variable value.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.

        This method just calls the appropriate "LogX" method (e.g. LogString, LogInt, etc) 
        based upon the type of value as determined by isinstance.  Note that it is faster to
        call the "LogX" method directly - this method is provided for C# SI compatibility.
        """
        if (self.IsOn(level)):

            if (value == None):
                self.LogObjectValue(level, name, value, colorValue)
            elif isinstance(value, str):
                self.LogString(level, name, value, colorValue)
            elif isinstance(value, bool):
                self.LogBool(level, name, value, colorValue)
            elif isinstance(value, int):
                self.LogInt(level, name, value, colorValue)
            elif isinstance(value, float):
                self.LogFloat(level, name, value, colorValue)
            elif isinstance(value, datetime):
                self.LogDateTime(level, name, value, colorValue)
            #elif isinstance(value, chr):               # <- force user to call LogChar directly, as this was causing exceptions in testing!
            #    self.LogChar(level, name, value)
            else:
                self.LogObjectValue(level, name, value, colorValue)


    def LogVerbose(self, title:str, *args, colorValue:int=None) -> None:
        """
        Logs a verbose message with a log level of Level.Verbose.

        Args:
            title (str):
                The message to log.
            *args:
                Format arguments for the title argument.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        if (self.IsOn(SILevel.Verbose)):

            try:
                
                # format title if *args was supplied.
                if (title) and (args):
                    title = (title % args)

                # send the packet.
                self.__SendLogEntry(SILevel.Verbose, title, LogEntryType.Verbose, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogVerbose: " + str(ex))


    def LogWarning(self, title:str, *args, colorValue:int=None) -> None:
        """
        Logs a warning message with a log level of Level.Warning.

        Args:
            title (str):
                The message to log.
            *args:
                Format arguments for the title argument.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
        """
        if (self.IsOn(SILevel.Warning)):

            try:
                
                # format title if *args was supplied.
                if (title) and (args):
                    title = (title % args)

                # send the packet.
                self.__SendLogEntry(SILevel.Warning, title, LogEntryType.Warning, ViewerId.Title, colorValue)

            except Exception as ex:
                
                self.LogInternalError("LogWarning: " + str(ex))


    def ResetCallstack(self, level:SILevel=None) -> None:
        """
        Resets the call stack by using a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
        
        This method instructs the Console to reset the call stack
        generated by the EnterMethod and LeaveMethod methods. It
        is especially useful if you want to reset the indentation
        in the method hierarchy without clearing all log entries.
        """
        if (self.IsOn(level)):

            try:

                # send log entry packet.
                self.__SendLogEntry(level, "", LogEntryType.ResetCallstack, ViewerId.NoViewer)

            except Exception as ex:
                
                self.LogInternalError("ResetCallstack: " + str(ex))


    def ResetCheckpoint(self, name:str=None) -> None:
        """
        Resets a named checkpoint counter.
        
        Args:
            name (str):
                The name of the checkpoint to reset.

        This method resets the counter of the given named checkpoint.
        Named checkpoints can be incremented and logged with the
        AddCheckpoint method.
        """
        # validations.
        if (name == None):
            name = "Checkpoint"

        with self.__fLock:

            if name in self.__fCheckpoints.keys():
                self.__fCheckpoints.pop(name)


    def ResetColor(self) -> None:
        """
        Resets the session background color to its default value.

        The default background color of a session is white transparent.
        """
        self.__fColorBG = Color(DEFAULT_COLOR_VALUE)


    def ResetCounter(self, name:str=None) -> None:
        """
        Resets a named counter to its initial value of 0.
        
        Args:
            name (str):
                The name of the counter to reset.

        This method resets the integer value of a named counter to 0
        again. If the supplied counter is unknown, this method has no
        effect. Please refer to the IncCounter and DecCounter methods
        for more information about named counters.
        """
        # validations.
        if (name == None):
            self.LogInternalError("ResetCounter: name argument is null.")
            return

        with self.__fLock:

            if name in self.__fCounters.keys():
                self.__fCounters.pop(name)


    def SendCustomControlCommand(self, level:SILevel, ct:ControlCommandType, data:BytesIO=None) -> None:
        """
        Logs a custom Control Command with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            ct (ControlCommandType):
                The Control Command type to use.
            data (BytesIO):
                Optional data stream which can be null.               
        """
        if (not self.IsOn(level)):
            return

        try:

            if (data == None):
                self.__SendControlCommand(ct, None)
                return

            oldPosition:int = 0

            # save original stream position (if possible).
            if (data.seekable):
                    
                oldPosition = data.tell()
                data.Position = 0

            try:
                    
                # send the packet.
                self.__SendControlCommand(ct, data)
                    
            finally:
                    
                # restore stream position (if possible).
                if (data.seekable):
                    data.seek(oldPosition)
                    
        except Exception as ex:
                
            self.LogInternalError("SendCustomControlCommand: " + str(ex))


    def SendCustomLogEntry(self, level:Level, title:str, lt:LogEntryType, vi:ViewerId, colorValue:int=None, data:BytesIO=None) -> None:
        """
        Logs a custom Log Entry with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title of the new Log Entry.
            lt (LogEntryType):
                The Log Entry type to use.
            vi (ViewerId):
                The Viewer ID to use.
            colorValue (int):
                Background color value (in ARGB integer form) for the message.
                Refer to the KnownColorValues class in the color module for common color values.
                Specify None to use default background color.
            data
                Optional data stream which can be null (or None).

        This method is useful for implementing custom Log Entry
        methods. For example, if you want to display some information
        in a particular way in the Console, you can just create a
        simple method which formats the data in question correctly and
        logs them using this SendCustomLogEntry method.
        """
        if (self.IsOn(level)):

            try:

                if (data != None):
                
                    # Use the LogCustomStream method, because the
                    # supplied stream needs to be processed correctly.
                    self.LogCustomStream(level, title, data, lt, vi)
                
                else:
                
                    # send log entry packet.
                    self.__SendLogEntry(level, title, lt, vi, colorValue, None)

            except Exception as ex:
                
                self.LogInternalError("SendCustomLogEntry: " + str(ex))


    def SendCustomProcessFlow(self, level:SILevel, title:str, pt:ProcessFlowType) -> None:
        """
        Logs a custom Process Flow entry with a custom log level.

        Args:
            level (Level):
                The log level of this method call.
            title (str):
                The title of the new Process Flow entry.
            pt (ProcessFlowType)
                The Process Flow type to use.
        """
        if (self.IsOn(level)):

            try:

                # send process flow packet.
                self.__SendProcessFlow(level, title, pt)

            except Exception as ex:
                
                self.LogInternalError("SendCustomProcessFlow: " + str(ex))


    def SendCustomWatch(self, level:SILevel=None, name:str=None, value=None, watchType:WatchType=None) -> None:
        """
        Logs a custom Watch with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (object):
                The value of the Watch.
            watchType (WatchType):
                The Watch type to use
        
        This method is useful for implementing custom Watch methods.
        For example, if you want to track the status of an instance of
        a specific class, you can just create a simple method which
        extracts all necessary information about this instance and logs
        them using this SendCustomWatch method.
        """
        # just invoke the Watch method, since they are the same calling parameters.
        # the SendCustomWatch method is provided for C# SI compatibility.
        self.Watch(level, name, value, watchType)


    def Watch(self, level:SILevel=None, name:str=None, value=None, watchType:WatchType=None) -> None:
        """
        Logs a Watch value by using the specified (or default) log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value:
                The bool value to display as Watch value.
            watchType (WatchType):
                WatchType to set in the LogEntry.

        "null" will be displayed if value=None.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            try:

                title:str = ""
                wt:WatchType = None

                # validations.
                if (name == None):
                    name = ""

                if (value == None):
                    value = "null"

                if (watchType != None):
                    wt = watchType

                # determine the value format and watch type to use, based on the type
                # of the value. The latter can be overridden via the `watchType`
                # argument, which can also affect formatting (e.g. WatchType.Address).
                if isinstance(value, str):
                    wt = WatchType.String
                    title = str.format("{0}", value)
                elif isinstance(value, bool):
                    wt = WatchType.Boolean
                    title = value and 'True' or 'False'
                elif isinstance(value, int):
                    wt = WatchType.Integer
                    title = str.format("{0}", str(value))
                elif isinstance(value, float):
                    wt = WatchType.Float
                    title = str.format("{0}", str(value))
                elif watchType == WatchType.Address:
                    wt = watchType
                    title = str.format("{0}", str(id(value)))
                elif isinstance(value, bytes):
                    wt = WatchType.Integer
                    title = str.format("{0}", str(int.from_bytes(value, byteorder='big')))
                elif isinstance(value, datetime):
                    wt = WatchType.Timestamp
                    title = str.format("{0}", str(value))
                else:
                    wt = WatchType.String
                    title = str.format("{0}", value)

                # send watch entry.
                self.__SendWatch(level, name, title, wt)

            except Exception as ex:
                
                self.LogInternalError("Watch: " + str(ex))


    def WatchBool(self, level:SILevel=None, name:str=None, value:bool=False) -> None:
        """
        Logs a boolean Watch with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (bool):
                The bool value to display as Watch value.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            # use "True"/"False" in case other boolean values passed (e.g. 0/1, yes/no, on/off, etc).
            if (value == True):
                v:str = "True"
            else:
                v:str = "False"
            self.__SendWatch(level, name, v, WatchType.Boolean)


    def WatchByte(self, level:SILevel=None, name:str=None, value:int=0, includeHex:bool=False) -> None:
        """
        Logs a byte Watch with an optional hexadecimal representation and custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (int):
                The byte value to display as Watch value.
            includeHex (bool):
                Indicates if a hexadecimal representation should be included.
        
        This method logs a byte Watch. You can specify if a
        hexadecimal representation should be included as well
        by setting the includeHex parameter to true.

        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            v:str = str(value)
            if (includeHex):
                vhex:str = " (" + hex(value).upper() + ")"
                vhex = vhex.replace("0X","0x")      # make "0X" lower-case since hex values will be in upper-case
                v += vhex
            
            self.__SendWatch(level, name, v, WatchType.Integer)


    def WatchChar(self, level:SILevel=None, name:str=None, value:chr=0) -> None:
        """
        Logs a chr Watch with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (chr):
                The chr value to display as Watch value.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            v:str = str(value)
            self.__SendWatch(level, name, v, WatchType.Char)


    def WatchComplex(self, level:SILevel=None, name:str=None, value:complex=None) -> None:
        """
        Logs a complex Watch with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (complex):
                The complex value to display as Watch value.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            v:str = str(value)
            self.__SendWatch(level, name, v, WatchType.Integer)


    def WatchDateTime(self, level:SILevel=None, name:str=None, value:datetime=None) -> None:
        """
        Logs a datetime Watch with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (datetime)
                The datetime value to display as Watch value.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            v:str = str(value)
            self.__SendWatch(level, name, v, WatchType.Timestamp)


    def WatchFloat(self, level:SILevel=None, name:str=None, value:float=0) -> None:
        """
        Logs a float Watch with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (float):
                The float value to display as Watch value.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            v:str = str(value)
            self.__SendWatch(level, name, v, WatchType.Integer)


    def WatchInt(self, level:SILevel=None, name:str=None, value:int=0, includeHex:bool=False) -> None:
        """
        Logs an integer Watch with an optional hexadecimal representation and custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (int):
                The integer value to display as Watch value.
            includeHex (bool):
                Indicates if a hexadecimal representation should be included.
        
        This method logs a integer Watch. You can specify if a
        hexadecimal representation should be included as well
        by setting the includeHex parameter to true.

        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            v:str = str(value)
            if (includeHex):
                vhex:str = " (" + hex(value).upper() + ")"
                if (value < 0):
                    vhex = vhex.replace("-","")     # remove minus sign for negative values.
                vhex = vhex.replace("0X","0x")      # make "0X" lower-case since hex values will be in upper-case
                v += vhex
            
            self.__SendWatch(level, name, v, WatchType.Integer)


    def WatchObject(self, level:SILevel=None, name:str=None, value:object=None) -> None:
        """
        Logs an object Watch with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (object):
                The object value to display as Watch value.

        The value of the resulting Watch is the return value of the
        "str(value)" method of the supplied object.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            if (value != None):
                v = "" + str(value)
                self.__SendWatch(level, name, v, WatchType.Object)
            else:
                self.LogInternalError(str.format("WatchObject: value argument is null for watch name \"{0}\".", "" + name));


    def WatchString(self, level:SILevel=None, name:str=None, value:str=None) -> None:
        """
        Logs a string Watch with a custom log level.
        
        Args:
            level (Level):
                The log level of this method call.
            name (str):
                The name of the Watch.
            value (str):
                The string value to display as Watch value.
        
        This method uses the SmartInspect.DefaultLevel value if the level
        parameter is set to None (default).  Otherwise, the specified level
        is utilized.
        """
        if (self.IsOn(level)):

            self.__SendWatch(level, name, value, WatchType.String)


    #def Track(self, func):
    #    """
    #    Decorator to add process flow tracking around the wrapped function.
    #    """
    #    def wrapped(*args, **kwargs):
    #        self.EnterMethod(func.__name__)
    #        try:
    #            return func(*args, **kwargs)
    #        finally:
    #            self.LeaveMethod(func.__name__)
    #    return wrapped

    #__Logging process flow using the decorator:__

    #```python
    #>>> @logger.track
    #>>> def append(self, obj):
    #>>>     pass   # do something
    #```
