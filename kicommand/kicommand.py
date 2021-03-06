# -*- coding: utf-8 -*-

# In python2, Use print function with parenthesis
from __future__ import print_function
import collections
from collections import defaultdict, Counter
from itertools import compress,cycle
# pcbnew.GetUnLoadableWizards()
# pcbnew.GetWizardsBackTrace()

# handle python3 or python2. In python2, import izip as zip
try:
    zip 
except NameError:
    from itertools import izip as zip

import itertools
import pcbnew
import time
import os, sys
#reload(sys)
#sys.setdefaultencoding('UTF8')
import traceback
import math
import re
from textwrap import wrap
import wx
import operator
import codecs

try:
    import kicommand_fonts 
    from wxpointutil import wxPointUtil
    import svgutil
    import kicommand_gui
    from point_in_polygon import wn_PnPoly, cn_PnPoly
except:
    from .point_in_polygon import wn_PnPoly, cn_PnPoly
    from . import kicommand_fonts
    from .wxpointutil import wxPointUtil
    from . import kicommand_gui
    import svgutil


# added to the module in Python 3.3. Alternatively you could use the code below which will also work in earlier Python versions.
# https://stackoverflow.com/a/8348914
try:
    import textwrap
    textwrap.indent
except AttributeError:  # undefined function (wasn't added until Python 3.3)
    def indent(text, amount, ch=' '):
        padding = amount * ch
        return ''.join(padding+line for line in text.splitlines(True))
else:
    def indent(text, amount, ch=' '):
        return textwrap.indent(text, amount * ch)
        
sys.modules['kicommand_fonts'] = kicommand_fonts

#font = kicommand_fonts.fontmanager().getfonttable('osi23')
# fontmanager = None # kicommand_fonts.fontmanager()
# font = None # fontmanager.getfont('NotoSans-Regular')
class fonts:
    _fontmanager = None
    _font = None
    @classmethod
    def getfontmanager(selfclass):
        if not selfclass._fontmanager:
            selfclass._fontmanager = kicommand_fonts.fontmanager()
        return selfclass._fontmanager
    @classmethod
    def getfont(selfclass,fontstring=None):
        if not selfclass._font or fontstring:
            if not selfclass._fontmanager:
                selfclass._fontmanager = kicommand_fonts.fontmanager()
            if not fontstring:
                fontstring = 'NotoSans-Regular'
            selfclass._font = selfclass._fontmanager.getfont(fontstring)
        return selfclass._font
        
# added for Python 3 compatibility, 
# define basestring so all the "isinstance(x,basestring)" functions will work.
try:
    basestring
except NameError:
    basestring = str
  
_dictionary = {'user':{}, 'persist':{}, 'command':{}}
# collections.OrderedDict
_stack = []

def getPcbnewWindow():
    try:
        return [x for x in wx.GetTopLevelWindows() if x.GetTitle().startswith('Pcbnew')][0]
    except:
       return None

#

# examples:

# : lines drawings DRAWSEGMENT filtertype copy GetShapeStr call Line = filter ;
# clear lines selected copy connected swap angle delist 0 swap -f rotate

# : horizontal lines copy selected connected lines selected angle delist 0 swap -f rotate ;

# : horizontal lines copy selected swap 1 pick connected swap angle delist 0 swap -f rotate ;

# : makeangle lines copy selected swap 1 pick connected swap angle delist 2 pick swap -f rotate pop ;
#drawings DRAWSEGMENT filtertype copy GetShapeStr call Line = filter copy selected


#
# Select all line segments and connect closest edges to make a closed polygon:
# drawings DRAWSEGMENT filtertype copy GetShapeStr call Line = filter copy selected connect

# drawings selected 465,30 mm pcbnew wxPoint callargs 100 zip2 Rotate callargs


# pcbnew list wxPoint attr


# pcbnew list 460,30 mm wxPoint callargs

# This code is in bad shape at the moment.
# Lot's of extra stuff that really doesn't belong
# Lot's of printing that the user really doesn't need.

# :persist wxpoint pcbnew list swap wxPoint callargs ; 
# 20170906 - Greg Smith
#     Created
# 20170918 - Greg Smith
#
#     Added builtins, fcall, fcallargs to enable getting the 'range' function
#     "clear builtins range index list 5 int list print fcallargs"
#     For some reason, builtins appears on the stack as a dictionary, which
#     won't work with 'call' or 'callargs', so 'fcall', 'fcallargs', and 'sindex'
#     were created.
#
#     Added sindex to allow accessing Python dictionaries with string indexes.
#     
#     Fixed pick command, was only returning top of stack.
#
#     Reworked 'int' command so that it returns a single value, not list, if there
#     is a single string without a comma. This allows the creation of a single
#     value on the stack (motivated in this case to enable 'index' to work well
#     with lists or dictionaries).
#     ": range int list builtins range index list swap print fcallargs ;"
#
#     Reworked 'float', 'index', 'mm', 'mil', 'mils' similarly to int.
#
#     Added quoted string using "double quotes". All spaces inside the quote
#     marks are retained. Words are split on the double quote mark such that the 
#     following are equal:
#     1 2 3 " 4 5 6 " 7 8 9
#     1 2 3" 4 5 6 "7 8 9
#     If in a file, pairs of quote marks must be on the same line.
#
#     Added load and save commands for the user dictionary. Lightly tested.
#
#
#
#
#

# r('clear : valuetext modules Value call ; : referencetext modules Reference call ; : moduletext modules GraphicalItems calllist EDA_TEXT filtertype ;')
# r('clear moduletext valuetext append referencetext append toptext append copy GetTextBox call corners swap copy GetCenter call swap GetTextAngle call rotatepoints drawsegments')
# copy copy Value call swap Reference call append swap GraphicalItems calllist append toptext append         copy GetTextBox call corners swap copy GetCenter call swap GetTextAngleDegrees call rotatepoints drawsegments

        # This allows simple command strings to be executed within pcbnew
        # The command string is in postfix format, and the current commands are:
        # Arguments, if any, are taken from the top of the stack.
        # and results, if any, are placed back on the stack.

        # copytop        - Copy the top of the stack.
        # modules        - Put all modules on the stack.
        # pads           - Put all pads on the stack.
        # tracks         - Put all tracks on the stack.
        # selected       - Filter top of the stack for selected items.
        # notselected    - Filter top of the stack for unselected items.
        # setselect      - Set items on the top of the stack to selected.
        # clearselect    - Set items on the top of the stack to unselected.
        # matchreference - Filter list of modules for matching a reference.
        # getpads        - Get all pads on the list of modules.

        # command_stack.kc(command_string)
        #
        # Sample command_string:
        #
        # 'modules' - return the list of modules
        # 'modules selected' - return the list of selected modules
        # 'modules selected clearselect' - unselect all selected modules
        # 'modules setselect' - select all modules (this seems to have no visual effect)
        # 'pads setselect' - select all pads
        # 'pads clearselect' - unselect all pads
        # 'modules getpads setselect' - select all pads of all modules
        # 'modules getpads clearselect' - unselect all pads of all modules
        # 'modules U1 matchreference getpads setselect' - select the pads of the module with reference 'U1'

        # Create a list of modules paired with their center in tuple format.
        # 'modules copytop GetReference call swap GetCenter call copytop 'x attr swap 'y attr zip2 zip2'

        # Create a list of text within modules:
        # 'modules GraphicalItems calllist EDA_TEXT filtertype GetShownText call'
        # 'clear modules GraphicalItems calllist EDA_TEXT filtertype GetShownText call'
        
        # Get all top text on the F.SilkS layer. Print the text.
        # 'clear toptext F.SilkS layernums onlayers GetShownText call'
        
        # Get all Module Values and References text on the B.SilkS layer. Print the text.
        # 'clear modules copytop Value call swap Reference call append B.SilkS layernums onlayers GetShownText call'
        
        # Get all lines within modules, then display their shape type:
        # 'clear modules GraphicalItems calllist drawsegment filtertype 
        #      copytop GetShapeStr call Line = filter GetShapeStr call'

# There are two types of statements that test values.
# 1) Results in filtering the current list into a smaller list, and
# 2) Results in a list of values (possibly True/False) of the same length and
#    in the same order as the tested list.
# Here, we call these 1) Filter (F), and 2) Value (V)
# The filter command explicity tests the list on the top of the stack (c[1])
# and filters the next in the stack (c[0]) based on the boolean evaluation
# of c[1].
# 

# class menu(pcbnew.ActionPlugin):
    # def defaults( self ):
        # """Support for ActionPlugin"""
        # self.name = "Command Stack"
        # self.category = "Command"
        # self.description = "Execute a postfix command stack."
    # def Run(self):
        # kc()
        

        #http://interactivepython.org/runestone/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html

        # if hasattr(pcbnew,'ActionPlugin')
# All commands are in _dictionary under one of three keys:
#    user, persist, and command.
# user and persist commands are command strings based on other
#    defined commands, and organized with the 
#    UserCommand() namedtuple.
# command commands are defined as python statements or functions
#    organized with the Command() namedtuple.
# command statements are defined with the lambda command within
#    a Command initialization.
# command functions are defined within the class commands
#    and the Command() namedtuples are constructed from
#    function attributes. (Not all command functions have been
#    ported to the class commands, some are still at the module
#    top level.)

Command = collections.namedtuple('Command','numoperands execute category helptext')
UserCommand = collections.namedtuple('UserCommand','execute category helptext command')
UserCommand.__str__ = lambda x: ': {} "{} {}" {} ;'.format(x.command,x.category,x.helptext,' '.join(x.execute))
            
#DrawParams = collections.namedtuple('DrawParams','thickness width height layer cpolyline zonepriority')
# DrawParams = collections.namedtuple('DrawParams','t w h l zt zp')
# param Usage:
# 0.3,1,1 mm F.Cu,NO_HATCH,0 split append t,w,h,l,zt,zp param
# 0.3,1,1 mm t,w,h param
# F.Cu,NO_HATCH,0 l,zt,zp param

# : drawparams list append t,w,h,l param ;
# : drawparams 'l param t,w,h param ;
# clear toptextobj selected topoints pairwise Dwgs.User tosegments
# clear toptextobj selected copy GetThickness call swap topoints pairwise Dwgs.User tosegments

#uc.execute(uc.string)

def decodestring(encoded_string):
    if sys.version_info >= (3,):
        return bytes(encoded_string, "utf-8").decode("unicode_escape") # python3 
    else:
        return encoded_string.decode('string_escape').encode('utf-8') # python2

# def GETPARAMS():
    # return _user_stacks['Params'][-1]
    
def PARAM(values, keys):
    # output('keys: {}\nvals: {}'.format(keys,values))
    if isinstance(values,basestring):
        values = values.split(',')
    keys = keys.split(',')
    
    if not hasattr(values,'__iter__'):
        values = [values]
    for k,v in zip(keys,values):
        _user_stacks['Params'][-1][k] = v

class gui(kicommand_gui.kicommand_panel):
    """Inherits from the form wxFormBuilder. Supplies
       functions that tie the gui to the functions below."""
    # def __init__(self):   

        # super(gui,self).__init__(parent)
        # self.Raise()
        # self.Show()
        
    combolist = []
    #self.entrybox.SetItems(combolist)
    def process(self,e):
        try:
            commandstring = self.entrybox.GetValue()
            kc(commandstring)
            self.entrybox.Clear()
            self.outputbox.ShowPosition(self.outputbox.GetLastPosition())
            if commandstring != '':
                self.combolist.insert(0,commandstring)
                self.entrybox.SetItems(self.combolist)
            #self.entrybox.Append(commandstring)
            self.entrybox.SetFocus()
            #output(str(self.combolist))
            self.entrybox.Update()
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno)  
            output(str(e))
            wx.MessageDialog(self.GetParent(),"Error on line %s: %s\n%s"%
               (exc_tb.tb_lineno, str(e), traceback.format_exc())).ShowModal()

import inspect
_KICAD_CONFIG = pcbnew.GetKicadConfigPath()

_KICOMMAND_CONFIG = os.path.join(pcbnew.GetKicadConfigPath(),'kicommand')
if not os.path.exists(_KICAD_CONFIG):
    os.mkdir(_KICAD_CONFIG)
    
if not os.path.exists(_KICOMMAND_CONFIG):
    os.mkdir(_KICOMMAND_CONFIG)

#teststempfile = os.path.join(kicommand_config,'tests.txt')

USERSAVEPATH = _KICOMMAND_CONFIG
USERSAVEPATHOLD = os.path.join(os.path.expanduser('~'),'kicad','kicommand')
#os.chdir(USERSAVEPATH)

KICOMMAND_MODULE_DIR = os.path.dirname(inspect.stack()[0][1])
LOADABLE_DIR = os.path.join(KICOMMAND_MODULE_DIR,'loadable')
USERLOADPATH = ':'.join((_KICOMMAND_CONFIG,USERSAVEPATHOLD,LOADABLE_DIR))
# PROJECTPATH = os.path.dirname(pcbnew.GetBoard().GetFileName())
# for i in range(len(inspect.stack())):
    # print(i,inspect.stack()[i][1])

_newcommanddictionary = None
_compile_mode = False

def setcompilemode(val=True, dictionary='user'):
    global _compile_mode
    global _newcommanddictionary
    _newcommanddictionary = dictionary
    _compile_mode=val
    
def LOAD(name,path=USERLOADPATH):
    for p in path.split(':'):
        new_path = os.path.join(p, name)
        if not os.path.isfile(new_path):
            continue
        with open(new_path,'r') as f: kc(f.read())

"""Tracks whether compile mode is on, allowing new command definitions.
   This is affected by the commands : and ;"""
_command_definition = []

_user_stacks = defaultdict(list)

_user_stacks['Params'].append({ 
                                't':0.3*pcbnew.IU_PER_MM,
                                'w':1*pcbnew.IU_PER_MM,
                                'h':1*pcbnew.IU_PER_MM,
                                'l':pcbnew.Dwgs_User, 
                                'zt':pcbnew.ZONE_CONTAINER.NO_HATCH,
                                'zp':0
                             })
                             
#_user_stacks['Board'].append(pcbnew.GetBoard())

# 50,1 int getunicoderange stringtogeom TTranslate,mm,0,50,TScale,native,0.9,0.9,mm  split swap append newdrawing refresh

def output(*args):

    MAXTEXTBOXTEXT = 32000
    w = KiCommandAction.getWindow()
    if w is None or getattr(w,'outputbox',None) is None:
        # wx.MessageDialog(None,'outputbox not defined').ShowModal()
        # Here's the simple 'print' definition of output
        for arg in args:
            print(arg,end=' ')
        print()
    else:
        #text = w.outputbox.Value
        tempstring = u' '.join(map(unicode,args)) # was "str" instead of "unicode"
        tempstring += '\n'
        if (len(tempstring)) > MAXTEXTBOXTEXT:
            tempstring = tempstring[int(max(0,len(tempstring)-MAXTEXTBOXTEXT)):]
            #start = len(tempstring)-MAXTEXTBOXTEXT
            w.outputbox.Value = tempstring
        else:
            w.outputbox.AppendText(tempstring)
    

def kc(commandstring,returnval=0,suspendStackNumPrint=False):
    """returnval -1 return entire stack, 0 return top, >0 return that number of elements from top of list as a list."""
# Items beginning with single quote are entered onto the stack as a string (without the quote)
# Items beginning with double quote swallow up elements until a word ends in a double quote,
# and enters the entire item on the stack as a string (without the quotes)
# Commands beginning with ? are conditional. The top of the stack is popped,
# and if it was True, then the command is executed.
    try:
        global _stack
        global _compile_mode
        global _command_definition
        global _dictionary
        #output( _dictionary ['command'].keys())
        #output( str(_stack))
        
        # if not aplugin:
            # KiCommandAction().register()
        # if not aplugin:
            # print("Error registering plugin with PCBNEW")
        #print(type(commandstring))
		
        #output(str(['%s:%d'%(dictname,len(_dictionary[dictname])) for dictname in ('user','persist','command')]))
		
        commandlines = commandstring.splitlines()
        commandslist = []
        for commandstring in commandlines:
            #print('processing {%s}'%commandstring)
            #commandslist = []
            qend = 0
            while True:
                qindex = commandstring.find('"',qend)
                if qindex == -1:
                    break;
                # wx.MessageDialog(None,'PRE '+commandstring[qend:qindex-1]).ShowModal()
                commandslist.extend(commandstring[qend:qindex].split())
                qend = commandstring.find('"',qindex+1)
                if qend == -1:
                    raise SyntaxError('A line must contain an even number of double quotes.')
                commandslist.append(commandstring[qindex+1:qend])
                # wx.MessageDialog(None,'Q {'+commandstring[qindex+1:qend]+'}').ShowModal()
                qend += 1
                
            # wx.MessageDialog(None,'END {'+commandstring[qend:]+'}').ShowModal()
            commandslist.extend(commandstring[qend:].split())
        # wx.MessageDialog(None,'{'+'}{'.join(commandslist)+'}').ShowModal()
        #print('{','}{'.join(commandslist),'}')
        #for command in commandslist:
        # converted to iterator so next() can be optionally executed in the handling of the loop syntax
        commandlist = iter(commandslist)
        try:
            nextcommand = commandlist.next()
        except:
            nextcommand = None
        while nextcommand is not None:
            command = nextcommand
            if command == ';':
                _compile_mode = False
                comm = _command_definition[:1]
                if not comm: # delete all commands in the user dictionary: ': ;'
                    _dictionary['user'] = {}
                    try:
                        nextcommand = commandlist.next()
                    except:
                        nextcommand = None
                    continue
                comm = comm[0]
                cdef = _command_definition[1:]
                if cdef:
                    # if the first term contains a space, then
                    # the category and helptext are taken from that parameter.
                    cat = ''
                    help = ''
                    firstspace = cdef[0].find(' ')
                    if firstspace != -1:
                        cathelp = cdef.pop(0)
                        cat = cathelp[:firstspace]
                        help = cathelp[firstspace+1:]                        
                        help = decodestring(inspect.cleandoc(' '.join(help.split())))
                        _dictionary[_newcommanddictionary][comm] = UserCommand(cdef,cat,help,comm)
                    #output( "COMMAND %s DEFINITION %s\nCategory: {%s} Help: {%s}"%(comm,cdef,cat,help))
                    else:
                        _dictionary[_newcommanddictionary][comm] = UserCommand(cdef,'','',comm)
                        #_dictionary[_newcommanddictionary][comm] = ' '.join(cdef)
                else: # delete a command in the user dictionary: ': COMMAND ;'
                    del(_dictionary['user'][_command_definition[0]])
                _command_definition = []
                try:
                    nextcommand = commandlist.next()
                except:
                    nextcommand = None
                continue

            if _compile_mode:
                _command_definition.append(command)
                try:
                    nextcommand = commandlist.next()
                except:
                    nextcommand = None
                # bypass further interpretation since we're just collecting words for defining commands
                continue

            if command.startswith('?') and len(command)>1:
                # Either a loop or a conditional
                #print('loop or cond')
                if not _stack.pop():
                    # Here, we've failed the conditional, so we reset the nextcommand and continue
                    # this works for the plain conditional or the loop command
                    #print('next! (a)')
                    try:
                        nextcommand = commandlist.next()
                    except:
                        nextcommand = None
                    continue
                # At this point, the condition is true
                
                if command[1] == '?': # this is a loop command
                    print('loop')
                    # replace the ??command with ?command
                    # but later, don't change nextcommand and it will continue to be the looped command
                    command = command[1:]
                else:
                    #print('next! (b)')
                    try:
                        nextcommand = commandlist.next()
                    except:
                        nextcommand = None
                
                # here we've reduced the loop command to the conditional command.
                # and the conditional is true, and we've already handled nextcommand if needed.
                command = command[1:]
                        
            else:
                #print('next! (c)')
                try:
                    nextcommand = commandlist.next()
                except:
                    nextcommand = None

            # after here, we don't have to update nextcommand again. The purpose of nextcommand is to handle loops just above

            if command.startswith("'"):
                _stack.append(command[1:])
                continue

            found = False
            #output('Dictionaries')
            for dictname in ('user','persist','command'):
                #output(dictname,' : ',str(_dictionary[dictname]))
                if command not in _dictionary[dictname]:
                    continue
                commandToExecute = _dictionary[dictname][command]
                if isinstance(commandToExecute,Command):
                    #output('%s is Command'%command)
                    numop = commandToExecute.numoperands
                    if len(_stack) < numop:
                        raise TypeError('%s expects %d arguments on the stack.'%(command,numop))
                    if numop:
                        result = commandToExecute.execute(_stack[-numop:])
                        _stack = _stack[:-numop]
                    else:
                        result = commandToExecute.execute([]) # TODO should this be [] ?
                        
                    if result is not None:
                        _stack.append(result)
                elif isinstance(commandToExecute,UserCommand):
                    #output('%s is UserCommand'%command)
                    kc(' '.join(commandToExecute.execute),suspendStackNumPrint=True)
                elif isinstance(commandToExecute,basestring):
                    #output('%s is commandstring'%command)
                    kc(commandToExecute,suspendStackNumPrint=True)
                found = True
                break
            if not found:
                _stack.append(command)
            
        if len(_stack) and not suspendStackNumPrint:
            output( len(_stack), 'operands left on the stack.' )
        try:
            pcbnew.UpdateUserInterface()
        except:
            pass
        #print('User dictionary',_dictionary['user'])
        if returnval == 0:
            if _stack:
                return _stack[-1]
            else:
                return None
        elif returnval == -1:
            return _stack
        elif returnval > 0:
            #returnval = -1 - returnval
            return _stack[-returnval:]
    except Exception as e:
        # print(traceback.format_exc())
        #e = sys.exc_info()[0]
        #print("Error: %s" % e)
        raise
            
class KiCommandAction(pcbnew.ActionPlugin):
    """implements ActionPlugin"""
    # global aplugin
    __window = None
    __instance = None
    # if window is "X"ed, __window == wx._core._wxPyDeadObject
    @classmethod
    def getInstance(selfclass):
       if selfclass.__instance is None:
           selfclass()
       return selfclass.__instance
        
    @classmethod
    def getWindow(selfclass):
        if selfclass.__instance is None:
            selfclass()
        #print ('Dead: ',isinstance(selfclass.__window,wx._core._wxPyDeadObject))
        # Weird: _wxPyDeadObject is gone from wx._core recently
        if selfclass.__window is None or (hasattr(wx._core,'_wxPyDeadObject') and isinstance(selfclass.__window,wx._core._wxPyDeadObject)):
            selfclass.getInstance().Run()
        if isinstance(selfclass.__window,wx.Panel) and not selfclass.__window.IsShown():
            selfclass.__window.Destroy()
            selfclass.getInstance().Run()
            

        return selfclass.__window
        
    def __init__(self):
        self.defaults()
        if self.__class__.__instance is not None:
            raise Exception("Use getInstance() to get the singleton instance.")
        else:
            self.__class__.__instance = self

    def defaults(self):
        self.name = "KiCommand"
        self.category = "Command"
        self.description = "Select, modify and interrogate pcbnew objects with a simple command script."
        self.show_toolbar_button = False # Optional, defaults to False
        self.icon_file_name = "" # os.path.join(os.path.dirname(__file__), 'simple_plugin.png') # Optional, defaults to ""

    def Run(self):
        try:
            parent = [x for x in wx.GetTopLevelWindows() if x.GetTitle().startswith('Pcbnew')][0]
        except:
            # top level windows not set up yet
            #wx.MessageDialog(None,'KiCommand Window setup failed. pcbnew window not available.').ShowModal()
            return
        # global aplugin
        # if aplugin:
            # return
        # else:
            # aplugin = self
        # parent =      \
            # filter(lambda w: w.GetTitle().startswith('Pcbnew'), 
                # wx.GetTopLevelWindows()
            # )[0]
        # better for Python3
        # Test for the __window variable. Is it Shown()?
        # wx.MessageDialog(None,'Window {}'.format(self.__class__.__window)).ShowModal()
        # try:
            # wx.MessageDialog(None,'Window {}'.format(self.__class__.__window.IsShown())).ShowModal()
        # except:
            # pass

        if self.__class__.__window:
            if self.__class__.__window.IsShown():
                # bring to front
                #self.__class__.__window.Restore()
                self.__class__.__window.Raise()
                return
            #else:
                # Using Destroy() here crashes KiCAD.
                # I'm not sure how to get rid of the reference to the window.
                # Below, we just replace the reference to __window
                # with a new window.
                # This might be a source of a memory leak.
                #self.__class__.__window.Destroy()
                #time.sleep(1)
            
        self.__class__.__window=gui(parent)
        pane = wx.aui.AuiPaneInfo()                       \
         .Caption( u"KiCommand" )                   \
         .Center()                                \
         .Float()                                 \
         .FloatingPosition( wx.Point( 346,268 ) ) \
         .Resizable()                             \
         .FloatingSize( wx.Size( int(1220),int(652) ) )       \
         .Layer( 0 )                                 

        manager = wx.aui.AuiManager.GetManager(parent)
        manager.AddPane( self.__class__.getWindow(), pane )
        manager.Update()

        kc('help')

KiCommandAction().register()

        
def retNone(function,*args):
    function(*args)

def UNDOCK():
    wx.aui.AuiManager.GetManager(KiCommandAction.getWindow()).GetPane(KiCommandAction.getWindow()).Float()
    # wx.aplugin.g.Float() #mgr.GetPane(text1).Float()
    # self.mgr.GetPane(text1).Float()
    # wx.aui.AuiManager.GetPane(wx.aplugin.g, item)
def STACK():
    for obj in _stack:
        output(obj)
def PRINT():
    """print the top of the stack"""
    output(_stack[-1])

import pprint        
def PPRINT():
    """pretty print the top of the stack"""
    output(pprint.pformat(_stack[-1]))
        
def CLEAR():
    global _stack
    _stack = []
    return None
    
def SWAP():
    global _stack
    _stack[-1],_stack[-2]=_stack[-2],_stack[-1]
# clear modules selected Reference call 0 bool list list SetVisible stack

def tosegments(*c):
    tracklist,layer = c
    #print('tracklist: ',tracklist)
    layerID = getLayerID(layer)
        
    segments = []
    for tlist in tracklist:
        for t in tlist:
            # s=t.GetStart()
            # e=t.GetEnd()
            s,e = get_ds_ends(t)
            
            try:
                width = t.GetWidth()
            except:
                width = _user_stacks['Params'][-1]['t']
            if not isinstance(s,pcbnew.wxPoint):
                s = pcbnew.wxPoint(*s)
            if not isinstance(e,pcbnew.wxPoint):
                e = pcbnew.wxPoint(*e)
            segments.append(draw_segmentwx(
                s,
                e,
                layer=layerID,
                thickness=width))
    return segments
        
def getLayerID(layer):
    if isinstance(layer,int):
        return layer
    try:
        layerID = getBoard().GetLayerID(str(layer))
        if layerID != -1:
            return layerID
    except:
        pass

    try:
        return int(layer)
    except:
        raise ValueError ("Layer name or layer ID (as int or string) expected.")

def draw_segmentlist(input, layer=pcbnew.Eco2_User, thickness=0.015*pcbnew.IU_PER_MM):
    """Draws the vector (wxPoint_vector of polygon vertices) on the given
       layer and with the given thickness.
       close indicates whether the polygon needs to be closed
       (close=False means the last point is equal to the first point).
       The drawing will use this input to draw a closed polygon."""
    # input is either: string (of comma seperated points)
    # list of strings of comma separated points
    # list of wxPoint
    # list of lists of wxPoint

    
    # string: single polyline a single list of comma separated values
    # list of numbers: single polyline
    # list of wxPoints: single polyline
    
    # list of strings: multiple polylines, each string is a polyline
    # list of list of numbers: multiple polylines
    # list of list of wxPoints: multple polylines
    
    layer = getLayerID(layer)

    if isinstance(input,basestring):
        #input = [input.split(',')]
        return drawlistofpolylines([input], layer, thickness)
        
    if not hasattr(input,'__getitem__'):
        input = list(input)

    if isinstance(input[0],(float,int,pcbnew.wxPoint)):
        input = [input]
        #print('478 triggered',input)
        
    return drawlistofpolylines(input,layer,thickness)
    
    # Here, input must be an iterable
    if not hasattr(input,'__iter__'):
        raise TypeError('%s expects argument to be a list or string.'%('command'))

    
    if not hasattr(input[0],'__iter__'):
        return drawlistofpolylines([input],layer,thickness)
    
    return drawlistofpolylines(input,layer,thickness)
    # Now, input is an actual list (of strings, or as it was passed to this function)
    # convert a list of strings (possibly comma separated) into a list of floats
    if isinstance(input[0],basestring):
        temp = []
        input = map(lambda y: safe_float(y),map(lambda x: temp.extend(x),[i.split(',') for i in input]))
    # Now, input is a list of
    # 1) individual floats,
    # 2) wxPoints,
    # 3) wxPoint lists,
    # 4) list of point pairs, or
    # 5) list of list of point pairs
    if not hasattr(input[0],'__iter__') and not isinstance(input[0],pcbnew.wxPoint):
    #if isinstance(input[0],float):
        a = iter(input)
        input = [zip(a, a)]
    
    if isinstance(input[0],pcbnew.wxPoint):
        input = [input]
    # Now we have a list of wxPoints or list of lists of wxPoints
    #output( input)
    # temp = []
    # for item in input:
        # if isinstance(item, pcbnew.wxPoint):
            # temp.append(item)
        # else:
            # temp.extend(item)
    # input = temp
    
    #output( type(vector))
    drawlistofpolylines(input,layer,thickness)
        
    allsegments = []
    segments = []
    for shape in input:
        #for segment in shape:
        if isinstance(shape[0],(float,int)):
            a = iter(shape)
            shape = [pcbnew.wxPoint(int(x),int(y)) for x,y in zip(a, a)]
        for i in range(len(shape)-1):
            segments.append(draw_segmentwx(
                shape[i],
                shape[i+1],
                layer=layer,
                thickness=thickness))
        allsegments.append(segments)
        segments = []
    return allsegments
    
    
def drawlistofpolylines(input_lop,layer,thickness):
    #print('in polylines: ',input_lop)
    allsegments = []
    segments = []
    for shape in input_lop:
        # shape is always a single list of items to be considered a polyline
        # Either 
        # 1) string to be split, a list of numbers to be used alternately
        #    in which case, each number or converted number is alternately x then y.
        # 2) or a list of wxPoint, or a list of __getitem__ objects with two values
        #    in which case each list value is an x/y pair.
        numbers = shape
        if isinstance(numbers,basestring):
            #output('string2')
            #numbers = map(lambda x: float(x),shape.split(','))
            numbers = [float(x) for x in shape.split(',')]

        if not hasattr(numbers[0],'__getitem__'):
            #print('zip triggered')
            a=iter(numbers)
            numbers = [(safe_int(x),safe_int(y)) for x,y in zip(a, a)]
        for i in range(len(numbers)-1):
            s = numbers[i]
            e = numbers[i+1]

            if not isinstance(numbers[i],pcbnew.wxPoint): # or not isinstance(numbers[i],pcbnew.wxPoint):
                try:
                    s = pcbnew.wxPoint(numbers[i][0],numbers[i][1])
                    e = pcbnew.wxPoint(numbers[i+1][0],numbers[i+1][1])
                except:
                    continue
            segments.append(draw_segmentwx(s,e,layer=layer,thickness=thickness))
# test commands:
# Test single list of numbers:
# 0,0,1,1 mm drawsegments
# Test single list of list of numbers:
# 0,0,1,1 mm list drawsegments
# Test single list of numbers:
# 0,0,1,1,2,2,3,3 mm list drawsegments
# Test two lists of numbers:
# 0,0,1,1 mm list 2,2,3,3 mm list append drawsegments
# 0,0,1000000,1000000 ,2000000,2000000,3000000,3000000 append drawsegments
# 0,0,1000000,1000000,2000000,2000000,3000000,3000000 drawsegments
# 0,0,1000000,1000000 list 2000000,2000000,3000000,3000000 list append drawsegments
# 0,0 mm wxpoint 1,1 mm wxpoint append 2,2 mm wxpoint append 3,3 mm wxpoint append drawsegments
# 0,0 mm wxpoint 1,1 mm wxpoint append list 2,2 mm wxpoint 3,3 mm wxpoint append list append drawsegments
        allsegments.append(segments)
        segments = []
    return allsegments
# r('0 FLOAT LIST 0 FLOAT LIST 100 MM LIST 100 MM LIST APPEND APPEND APPEND DRAWSEGMENTS')
# r('0,0,100,100 MM DRAWSEGMENTS')
def close_enough(a,b):
    return abs(a-b)<(5*32) 
def GRID(dseglist,grid):
    grid = int(grid)
    for seg in dseglist:
            if isinstance(seg, (pcbnew.DRAWSEGMENT, pcbnew.TRACK) ):
                for gp,sp in ((seg.GetStart,seg.SetStart),(seg.GetEnd,seg.SetEnd)):
                    p = gp()
                    newp=pcbnew.wxPoint(int(round(p[0]/grid)*grid),int(round(p[1]/grid)*grid))
                    sp(newp)
            else: # this works for BOARD_ITEMs
                for gp,sp in ((seg.GetPosition,seg.SetPosition),):
                    p = gp()
                    newp=pcbnew.wxPoint(int(round(p[0]/grid)*grid),int(round(p[1]/grid)*grid))
                    sp(newp)
        
# Scale to 100 mm and make one of the segments parallel to angle 0
# 100 mm 0 clear drawings selected copy connect copy regular copy copy length delist 100 mm swap /f scale copy delist list angle delist 0 swap -f rotate
# 100 mm 0 drawings selected copy connect copy regular copy copy length delist stack 4 pick swap /f scale copy delist list angle delist 2 pick swap -f rotate stack



# Usage: SIDELENGTH PARALLELANGLE regularsize
# regularsize takes the selected segments, joins them into a regular polygon, then
# sizes the edges to the specified length, and places one of the edges parallel
# to the specified angle

# : regularsize drawings selected copy connect copy regular copy copy length delist stack 4 pick swap /f scale copy delist list angle delist 2 pick swap -f rotate pop pop ;

def SCALE(dseglist,factor):
    # find midpoint of all points
    num = 2*len(dseglist)
    pairs = map(lambda seg: get_ds_ends(seg),dseglist)
    points = [item for sublist in pairs for item in sublist]
    xs, ys = itertools.tee(points)
    xsum, ysum = sum(x[0] for x in xs), sum(y[1] for y in ys)
    center = pcbnew.wxPoint(xsum/num,ysum/num)
    
    #output('Center: %s'%(center))
    for seg in dseglist:
        for gp,sp in ((seg.GetStart,seg.SetStart),(seg.GetEnd,seg.SetEnd)):
            p = gp()
            v=p-center
            newp=wxPointUtil.scale(v,float(factor))+center
            sp(newp)
        
def LENGTH(dseglist):
    return map(lambda seg: wxPointUtil.distance(*get_ds_ends(seg)), dseglist)
    
def REGULAR(dseglist):
    """create a regular polygon from the set of connected and closed segments"""
    ordered = order_segments(dseglist)
    ordered = ordered[0]
    
    # for seg in dseglist:
        # output( "s,e=",get_ds_ends(seg))
    # output('len ordered=',len(ordered))
    # for seg in ordered:
        # output( "ordered s,e=",get_ds_ends(seg))

    numsides = len(dseglist)
    
    # this makes the sides equal to largest of existing sides:
    sidelength = max(map(lambda seg: wxPointUtil.distance(*get_ds_ends(seg)), dseglist))
        
    # this makes the sides equal to average of existing sides:
    # sidelength = 0
    # for seg in dseglist:
        # sidelength += wxPointUtil.distance(*get_ds_ends(seg))
    #sidelength = sidelength / numsides

    # positive polarity is this end is common to the next seg.
    polarity = []
    s,e = get_ds_ends(ordered[0]) # only need e here
    for i in range(len(ordered)-1):
        sn,en = get_ds_ends(ordered[(i+1)%len(ordered)])
        polarity.append((close_enough(e[0],sn[0]) and close_enough(e[1],sn[1])) or 
                        (close_enough(e[0],en[0]) and close_enough(e[1],en[1])))
        e = en
    polarity.append(polarity[0])
    angle = 2*math.pi / numsides
    
    # get angle of first segment, use this as the starting angle
    # if positive polarity, end is the anchor
    

    
    angleincrement = 2*math.pi/numsides
    for i in range(len(ordered)-1):
        if polarity[i]:
            anchor,free = get_ds_ends(ordered[i])
        else:
            free,anchor = get_ds_ends(ordered[i])
        
        if i == 0:
            firstanchor = anchor
            vector = free - anchor
            startangle = -math.atan2(vector[1],vector[0]) # - is kicad angle polarity CCW
            #wxPointUtil.scale(vector*sidelength/mag(vector))

        angle = startangle+2*math.pi*i/numsides
        # output( 'anchor,free,angle=',anchor,free,angle*180/math.pi)
        vector = wxPointUtil.towxPoint(sidelength,angle)

        endpoint = anchor+vector
        # TODO: update to work with S_ARC
        if polarity[i]:
            ordered[i].SetEnd(endpoint)  
            # if i==0:
                # output( 'setend')
        else:
            ordered[i].SetStart(endpoint)
            # if i==0:
                # output( 'setstart')
        if polarity[i+1]:
            ordered[i+1].SetStart(endpoint) 
            # output( 'setstart')
        else:
            ordered[i+1].SetEnd(endpoint)
            # output( 'setend')

        # ordered[i].SetEnd(endpoint) if polarity[i] else ordered[i].SetStart(endpoint)
        # ordered[i+1].SetStart(endpoint) if polarity[i+1] else ordered[i+1].SetEnd(endpoint)
#    ordered[-1].SetEnd(firstanchor) if polarity[-1] else ordered[-1].SetStart(firstanchor)
def get_ds_ends(dseg):
    try:
        shape = dseg.GetShape()
    except:
        try:
            return dseg.GetStart(), dseg.GetEnd()
        except:
            try:
                return dseg[0],dseg[1]
            except:
                #print(type(dseg))
                output ('error get get_ds_ends')
                return
    if shape == pcbnew.S_SEGMENT:
        return dseg.GetStart(), dseg.GetEnd()
    elif shape == pcbnew.S_ARC:
        # Start, Center, Angle define the S_ARC
        start = dseg.GetArcStart()
        center = dseg.GetCenter()
        angle = dseg.GetAngle()/10.0
        radians = angle*math.pi/180
        radians = dseg.GetAngle() * math.pi / 1800
        # Get vector C->S = VCS
        # Rotate(S - C, CCW Angle) + C = new end point
        #b=VC; a=VR; b+a = VS;  => VR = VS - VC
        CS = start-center
        CE = wxPointUtil.rotatexy(CS,radians)
        #VS = a+b; VC=b VCS=a
        end = CE + center
        return start, end
        # Also .GetArcEnd()
    elif shape == pcbnew.S_CURVE:
        output  ('Warning: KiCommand cannot determine S_CURVE end points. Skipping.')
    else:
        output('Warning: There are no endpoints to %s'%dseg.GetShapeStr())
        return None
   
    return dseg.GetStart(), dseg.GetEnd()
def get_drawsegment_points(dseglist):
    return dseg.GetStart(), dseg.GetEnd()
def CONNECT(dseglist):
    """given a list of almost-connected DRAWSEGMENTs, move their endpoints such that they are coincident. It is assumed
    that each segment connects to two others, except perhaps the 'end' segments."""

    # put all points of start and end into a dictionary
    # where value = segment
    #output( dseglist)
    points = defaultdict(set)
    #dsegse = defaultdict(set)
    for dseg in dseglist:
        s,e = get_ds_ends(dseg)
        s = point_round128(s)
        e = point_round128(e)
        st = (s[0],s[1])
        et = (e[0],e[1])
        points[st].add(dseg)
        points[et].add(dseg)
        #dsegse[dseg]
    # if a point is already the vertex for two segments, remove it from needing
    # to be attached. (this is debatable, perhaps it should be able to be
    # attached to, but doesn't NEED to be attached to anything else)
    
    # for each, create list of all others by sorted by distance (squared)
    unconnected=filter(lambda x: len(points[x]) == 1, points.keys())

    # distances2 contains list of points and distance2s from the corresponding point in unconnected.
    distances2 = defaultdict(list)
    # d2 key is rounded point;
    #   [key][i] is a tuple
    #   [key][i][0] is the other point (rounded) and 
    #   [key][i][1] is the distance
    for i,p in enumerate(unconnected):
        distances2[p] = \
        [(unconnected[j],wxPointUtil.distance2(unconnected[i],unconnected[j])) for j in range(0,len(unconnected)) if i!=j] # 0 should be i+1

    # for dseg in dseglist:
        # s=dseg.GetStart()
        # e=dseg.GetEnd()
        # (s[0],s[1])
        # (e[0],e[1])
    

    # now sort the unconnected points' distances to each other
    for distanceslist in distances2.values():
        distanceslist.sort(key=lambda dist:dist[1])

    # for i in unconnected:
        # output( '\n',i,':')
    # for p,d in distances2.iteritems():
        # output( '\n',p)
        # output( '\t',d)
        
    # output( "distances2 = ",distances2.keys())
    pointset = set(points.keys())
    
    for point in unconnected:
    #for point in points.keys():
        # output( "point = ",point)
        if point not in pointset:
            continue
        # If the two points are each others closest points, then connect them.
        
        point2 = distances2[point][0][0]
        # output( 'p  : ',point,)
        # output( 'p2 : ',point2,)
        # output( 'dp : ',distances2[point][0][0],) # this should be point2
        # output( 'dp2: ',distances2[point2][0][0]) # this should be point1
        
        if point == distances2[point2][0][0]:
            newpoint = point
            for pchange,newpoint in ((point,point2),(point2,point)):
                try: pointset.remove(pchange)
                except: pass
                try: pointset.remove(newpoint)
                except: pass
                #seg = points[pchange][0] # should be only one segment in the list for this point.
                (seg,) = points[pchange] # get the one element in the set
                if seg.GetShapeStr() != 'Line':
                    continue
                segstart,segend = get_ds_ends(seg)
                segstart = point_round128(segstart)
                segend = point_round128(segend)
                # here we reset one side of the DRAWSEGMENT or the other.
                # For a line (i.e. S_SEGMENT), we simply change the
                # Start or End point.
                # for an arc, it's a little harder.
                # For example, if the start changes then the end will change
                # unless the center point or the angle are changed.

                
                if segstart[0] == pchange[0] and segstart[1] == pchange[1]:
                    # output('setstart %s %s %s'%(seg.GetShapeStr(),str(get_ds_ends(seg)),str(seg)))
                    seg.SetStart(pcbnew.wxPoint(newpoint[0],newpoint[1]))
                    # output('setstart %s %s %s'%(seg.GetShapeStr(),str(get_ds_ends(seg)),str(seg)))
                elif segend[0] == pchange[0] and segend[1] == pchange[1]:
                    # output('setend %s %s %s'%(seg.GetShapeStr(),str(get_ds_ends(seg)),str(seg)))
                    seg.SetEnd(pcbnew.wxPoint(newpoint[0],newpoint[1]))
                    # output('setend %s %s %s'%(seg.GetShapeStr(),str(get_ds_ends(seg)),str(seg)))
                # else:
                    # output( "Warning, bug in code.: ",pchange, segstart, segend)
                break
    # for i in range(len(unconnected)):
        # output( '\n',unconnected[i],':')
        # for d in distances2[i]:
            # output( '\t',d)
def is_connected(w,v):
    return wxPointUtil.distance2(w,v) < 200*200

### Unfinished
def order_segments_new(dseglist):
    # use a distance calculation
    seglistcopy = list(dseglist)
    pointlist = [list(get_ds_ends(seg)) for seg in seglistcopy]
    
    for firstindex in range(0,len(seglistcopy)-1):
        dstarts = [ \
        (pointlist[firstindex][1][0]-pointlist[secondindex][0][0])**2 + \
        (pointlist[firstindex][1][1]-pointlist[secondindex][0][1])**2 \
        for secondindex in range(firstindex+1,len(seglistcopy))]
        dends = [ \
        (pointlist[firstindex][1][0]-pointlist[secondindex][1][0])**2 + \
        (pointlist[firstindex][1][1]-pointlist[secondindex][1][1])**2 \
        for secondindex in range(firstindex+1,len(seglistcopy))]
        # find the closes start point, and its squared distance
        index, value = max(enumerate(my_list), key=operator.itemgetter(1))
# max(enumerate(pointlist),key=operator.itemgetter(
# wxPointUtil.distance(pointlist[firstindex][1],pointlist[secondindex][0])
# wxPointUtil.distance(pointlist[firstindex][1],pointlist[secondindex][1])
    # print(dstarts)
    starts = [pointlist[0][1]*pointlist[0][1]+pointlist[secondindex][0]*pointlist[secondindex][0] for secondindex in range(firstindex+1,len(seglistcopy))]

def order_segments(dseglist):
    # fixed with gridboxes
    segs_by_box = defaultdict(set)
    boxes_by_seg = {}
    dseglist = list(dseglist)

    for seg in dseglist:
        # Get start end ending points in the segment
        s,e = get_ds_ends(seg)
        # Get the gridboxes surrounding each point
        gbs = gridboxes(s)
        gbe = gridboxes(e)
        # output(str(s)+' gbs: '+str(gbs))
        # output(str(e)+' gbe: '+str(gbe))
        # any of the boxes points to the opposite end of the segment


        # Create a dictionary with key of box and value of opposing endpoint
        sdict={}
        for b in gbs:
            sdict[b] = e
            # output(str(b))
            segs_by_box[b].add(seg)
            
        # Do the same for each endpoint -> startpoint.
        edict={}
        for b in gbe:
            # output(str(b))
            edict[b] = s
            segs_by_box[b].add(seg)
            
        boxes_by_seg[seg] = {s:sdict,e:edict}
        """bbs is a structure that you can look up all the boxes the 
        opposing point of the segment exists in."""

    # output ('sbb keys:')
    # for box,segs in segs_by_box.iteritems():
        # seglist=list(segs)
        # output(str(box),len(segs))
        # for seg in seglist:
            # output('\t',get_ds_ends(seg))
    # now create a structure where a segment points to all connected segments
    # output('sbb %s'%str(segs_by_box))
    # output('bbs %s'%str(boxes_by_seg))
    # output('box:seglist')
    # for b,seglist in segs_by_box.iteritems():
        # output('({}) {}: {}'.format(len(seglist),str(b),str(seglist)))
    # output('end box:seglist')
    
    connected = defaultdict(set)
    for b,seglist in segs_by_box.iteritems():
        for seg1 in seglist:
            for seg2 in seglist:
                if seg1 != seg2:
                    # output('adding')
                    connected[seg1].add(seg2)
                    connected[seg2].add(seg1)
                    
    # output ('BEGIN connected set')    
    # for seg,connectedset in connected.iteritems():    
        # output('({}) {}: {}'.format(len(connectedset),seg,connectedset))
    # output ('DONE connected set')    
    # output('connected:')
    # for seg,seglist in connected.iteritems():
        # output('%s'%str(get_ds_ends(seg)))
        # for cseg in seglist:
            # output('\t%s'%str(get_ds_ends(cseg)))
    # now a sanity check
    for seg,seglist in connected.iteritems():
        if len(seglist) > 2:
            # doesn't capture three segments at one box/point
            output('Error: segment {} connected to more than 2 other segments: {}'.format(
                str(get_ds_ends(seg)),', '.join(map(lambda x: str(get_ds_ends(x)),seglist))))
            return dseglist
    
    segset = set()
    ordered_and_split = [[]]
    # organize the segments into connected lists.
    # Make sure we consider each segment
    for seg in dseglist:
        currentseg = seg
        lastseg = seg
        # This while loop finds all segments connected to 'seg' 
        while currentseg is not None and currentseg not in segset:
            segset.add(currentseg) # add current segment to those already considered.
            # 'connected' lists all connected segments of 'currentseg'
            csegs = list(connected.get(currentseg,None))
            # output("Length of csegs {}".format(len(csegs)))
            # csegs should be one or two segments
            # one of those connected segments will be lastseg
            if lastseg in csegs:
                csegs.remove(lastseg)
            # output('added to oas')
            # add currentseg to the latest ordered_and_split list
            ordered_and_split[-1].append(currentseg)
            lc = len(csegs)            
            if lc == 0:
                ordered_and_split.append([])
                currentseg = None
            elif lc == 1:
                lastseg = currentseg
                currentseg = csegs[0]
            else: # lc = > 1
                # it's not an error if this is the first segment considered. All others should have 0 or 1 connected segments.
                if currentseg != lastseg:
                    output('Error: segment {} connected to more than 2 other segments: {}'.format(
                        str(get_ds_ends(currentseg)),', '.join(map(lambda x: str(get_ds_ends(x)),csegs))))
                # just choose the first one in the list
                lastseg = currentseg
                currentseg = csegs[0]
                # output('Error: segment connected to more than 2 other segments: %s'%
                    # str(get_ds_ends(currentseg)))
        # try:
            # if ordered_and_split[-1][-1] in connected(ordered_and_split[-1][0]):
                # ordered_and_split[-1].append(ordered_and_split[-1][0])
        # except:
            # pass
    if not ordered_and_split[-1]:
        ordered_and_split.pop()
    return ordered_and_split

    
def order_segments_old(dseglist):
    # TODO: 
    # output('len(dseglist)=%s'%len(dseglist))
    segs_by_point = defaultdict(set)
    points_by_seg = {}
    # for seg in dseglist:
        # output( "segment: ",get_ds_ends(seg))
    #output( "dseglist = ",list(dseglist))
    
    for seg in dseglist:
        s,e = get_ds_ends(seg)
        s = point_round128(s)
        e = point_round128(e)
        st=(s[0],s[1])
        et=(e[0],e[1])
        points_by_seg[seg] = {st:et,et:st}

        #output( seg)
        s,e = get_ds_ends(seg)
        for p in s,e:
            p = point_round128(p)
            segs_by_point[(p[0],p[1])].add(seg)

    if not len(points_by_seg):
        return

    # for p,segs in segs_by_point.iteritems():
        # for seg in segs:
            # output( "s_by_p point ",p,"seg ",get_ds_ends(seg))
    # find first lonely vertex
    #output( segs_by_point)
    for currentpoint,seglist in segs_by_point.iteritems():
        if len(seglist)==1:
            break
    ordered = []
    
    while segs_by_point[currentpoint]:
        #output( "currentpoint = ",currentpoint)
        currentseg = list(segs_by_point[currentpoint])[0] # get one element in the set
        #(currentseg,) = segs_by_point[currentpoint] # get the one element in the set
        #output( 'currentset = ',currentseg)
        ordered.append(currentseg)
        #output( 'added ',currentseg)
        currentpoint = points_by_seg[currentseg][currentpoint] # sort of a doubly linked list, get the point on the segment, not currently used.
        segs = segs_by_point.get(currentpoint,None)
        if not segs:
            break 
        try:
            segs.remove(currentseg)
        except:
            break
    return ordered

def MAKEANGLE(dseglist,degrees):
    output('makeangle not implemented.')
    return dseglist

def point_iterator(seglist):
    for seg in seglist:
        yield seg.GetStart()
        yield seg.GetEnd()
        
        
def connected_pairs(dseglist):
    segs_by_box = defaultdict(set)
    boxes_by_seg = {}
    dseglist = list(dseglist)

    for seg in dseglist:
        # Get start end ending points in the segment
        s,e = get_ds_ends(seg)
        # Get the gridboxes surrounding each point
        gbs = gridboxes(s)
        gbe = gridboxes(e)
        # output(str(s)+' gbs: '+str(gbs))
        # output(str(e)+' gbe: '+str(gbe))
        # any of the boxes points to the opposite end of the segment


        # Create a dictionary with key of box and value of opposing endpoint
        sdict={}
        for b in gbs:
            sdict[b] = e
            # output(str(b))
            segs_by_box[b].add(seg)
            
        # Do the same for each endpoint -> startpoint.
        edict={}
        for b in gbe:
            # output(str(b))
            edict[b] = s
            segs_by_box[b].add(seg)
            
        boxes_by_seg[seg] = {s:sdict,e:edict}
        """bbs is a structure that you can look up all the boxes the 
        opposing point of the segment exists in."""

    # output ('sbb keys:')
    # for box,segs in segs_by_box.iteritems():
        # seglist=list(segs)
        # output(str(box),len(segs))
        # for seg in seglist:
            # output('\t',get_ds_ends(seg))
    # now create a structure where a segment points to all connected segments
    # output('sbb %s'%str(segs_by_box))
    # output('bbs %s'%str(boxes_by_seg))
    # output('box:seglist')
    # for b,seglist in segs_by_box.iteritems():
        # output('({}) {}: {}'.format(len(seglist),str(b),str(seglist)))
    # output('end box:seglist')
    
    connected = defaultdict(set)
    for b,seglist in segs_by_box.iteritems():
        for seg1 in seglist:
            for seg2 in seglist:
                if seg1 != seg2:
                    # output('adding')
                    connected[seg1].add(seg2)
                    connected[seg2].add(seg1)
                    
    # output ('BEGIN connected set')    
    # for seg,connectedset in connected.iteritems():    
        # output('({}) {}: {}'.format(len(connectedset),seg,connectedset))
    return connected
    
def draw_arc_to_segments(radius,dseglist):
    # output('len(segments)=%s'%len(dseglist))
    done = []
    pairs = connected_pairs(dseglist)
    if isiter(radius):
        radius = radius[0]
    for seg, segset in pairs.iteritems():
        for seg2 in segset:
            s = set((seg,seg2))
            if s not in done:
                draw_arc_to_lines(radius,seg,seg2)
                done.append(s)
    # for ordered in orderedlol:
        # for i in range(len(ordered)-1):
            # draw_arc_to_lines(radius[0],ordered[i],ordered[i+1])
def draw_arc_to_segments_old(radius,dseglist):
    # output('len(segments)=%s'%len(dseglist))

    orderedlol = order_segments(dseglist)
    # output('len(orderedlol)=%s'%len(orderedlol))
    for ordered in orderedlol:
        for i in range(len(ordered)-1):
            draw_arc_to_lines(radius[0],ordered[i],ordered[i+1])
def ANGLE(dseglist):
    angles = []
    for seg in dseglist:
        s,e = get_ds_ends(seg)
        v=e-s
        angles.append( -math.atan2(v[1],v[0]) * 180/math.pi )

    return angles
    
def ROTATE(dseglist,angle):
    angle = float(angle)
    allpoints = []
    for seg in dseglist:
        #allpoints.extend(get_ds_ends(seg))
        allpoints.append(seg.GetCenter())
    xcenter = 0
    ycenter = 0
    for p in allpoints:
        xcenter += p[0]
        ycenter += p[1]
    n = len(allpoints)
    center = pcbnew.wxPoint(xcenter / n, ycenter / n)
    for seg in dseglist:
        shape = seg.GetShape()
        if shape == pcbnew.S_SEGMENT:
            seg.SetStart(pcbnew.wxPoint(*rotate_point(seg.GetStart(),center,angle,ccw=True)))
            seg.SetEnd(pcbnew.wxPoint(*rotate_point(seg.GetEnd(),center,angle,ccw=True)))
        # elif shape == pcbnew.S_CIRCLE:
            # seg.SetCenter(pcbnew.wxPoint(*rotate_point(seg.GetCenter(),center,angle,ccw=True)))
        else: # pcbnew.S_ARC and possibly others
            seg.Rotate(center,angle*10.0)
        
def lines_intersect(p,q,w,v):
    # get intersection
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    r=w-p
    s=v-q
    
    # intersection = (p+tr = q+us)
    # dot vx wy - vy wx
    drs = wxPointUtil.dot_other(r,s)
    # output( "drs,r,s=",drs, r, s)
    qmp = q-p
    t = wxPointUtil.dot_other(qmp,s)/ float(drs)
    u = wxPointUtil.dot_other(qmp,r)/ float(drs)
    # output( "p,q,r,s,drs,qmp,t,u ",p,q,r,s,drs,qmp,t,u)
    intersection = p+wxPointUtil.scale(r,t) # ,q+wxPointUtil.scale(s,u))
    i2 = q + wxPointUtil.scale(s,u)
    
    x1=p[0]
    y1=p[1]
    x2=q[0]
    y2=q[1]
    x3=w[0]
    y3=w[1]
    x4=v[0]
    y4=v[1]
    x2112 = (x2*y1-x1*y2)
    x4334 = (x4*y3-x3*y4)

    divisor = (x2-x1)*(y4-y3)-(x4-x3)*(y2-y1)
    if divisor == 0:
        return None
    xi = (x2112*(x4-x3) - x4334*(x2-x1))/divisor
    yi = (x2112*(y4-y3) - x4334*(y2-y1)) / divisor


    return pcbnew.wxPoint(xi,yi)


def draw_arc_to_lines(radius,pqseg,wvseg):
    p=pqseg.GetStart()
    q=pqseg.GetEnd()
    w=wvseg.GetStart()
    v=wvseg.GetEnd()
    
    # w = p+r; v=q+s
    # output( radius,p,q,w,v)
    #draw_segment(p[0],p[1],q[0],q[1],layer=pcbnew.Eco1_User)
    #draw_segment(w[0],w[1],v[0],v[1],layer=pcbnew.Eco1_User)

    intersection = None
    if p==w or p==v:
        intersection = pcbnew.wxPoint(p[0],p[1])
    if q==w or q==v:
        intersection = pcbnew.wxPoint(q[0],q[1])
    
    if intersection is None:
        intersection = lines_intersect(p,q,w,v)
        #output( "intersection = ",intersection,"; i2 = ",i2)
    # output( "intersection,p,q,w,v = ",intersection, p,q,w,v)
    # find the closest endpoint on each line to the intersection.
    dp = wxPointUtil.distance2(intersection,p)
    dq = wxPointUtil.distance2(intersection,q)
    dw = wxPointUtil.distance2(intersection,w)
    dv = wxPointUtil.distance2(intersection,v)
    
    # put the edges in order (closest to intersection is [0])
    wvswapped = False
    if dw<dv:
        wv = (w,v)
    else:
        wv = (v,w)
        wvswapped = True
    pq,pqswapped = ((p,q),False) if dp<dq else ((q,p),True)

    # output( 'pq,wv=', pq,wv)
    # draw_segment(wv[1].x,wv[1].y,intersection.x,intersection.y)
    # draw_segment(pq[1].x,pq[1].y,intersection.x,intersection.y)
    # angle between lines, radians
    # output( 'vi ',wv[1]-intersection, '; qi ',pq[1]-intersection)
    # output( 'dot ',wxPointUtil.dot_other(wv[1]-intersection,pq[1]-intersection))
    # tangentpoints
    # scale(wxPointUtil.unit(wv[1]-intersection)
    # output( 'i3=',intersection)
    vi = wv[1]-intersection
    qi = pq[1]-intersection
    # note that with atan2
    # atan2:  45 = 1, 1; 135 =-1, 1; -135 =-1,-1; -45 = 1,-1
    # kicad:  45 = 1,-1; 135 =-1,-1; -135 =-1, 1; -45 = 1, 1
    # so: -45->45; -135->135; 135->-135; 45->-45
    # overall: kicad coordinates = - atan2 coordinates

    awv = -math.atan2(vi[1],vi[0]) # also converts to -y, 4-quadrant answer
    apq = -math.atan2(qi[1],qi[0]) # also converts to -y, 4-quadrant answer

    # after mod 2pi, values between pi/2 to 3pi/2 means the angle is greater than 180
    
    #if math.pi/2 < (awv-apq)%2*math.pi < math.pi*3/2:
    #if 0 < (apq-awv)%(2*math.pi) < math.pi:
    if 0 > (awv-apq):
        # here, apq is bigger
        theta = (apq - awv)%(2*math.pi)
        bigger='p'
        fromnorm = wv[1]
    else:
        # here, awv is bigger
        theta = (awv - apq)%(2*math.pi)
        fromnorm = pq[1]
        bigger='w'
        
    theta = (apq - awv)%(2*math.pi)
    bigger='p'
    fromnorm = wv[1]

    norm = wxPointUtil.normal(fromnorm-intersection)
    norm = wxPointUtil.scale(norm,radius/wxPointUtil.mag(norm))    
    arcangle = ((math.pi + theta)%(2*math.pi))*180/math.pi
    
        
    # determine order, 'internal' angle defined by less than 180
    #theta = math.acos(wxPointUtil.dot_other(wv[1]-intersection,pq[1]-intersection))
    # output( 'awv,apq = ',awv*180/math.pi,apq*180/math.pi)
    #theta = (awv + apq) % 2*math.pi

    # output( 'theta= ',theta)
    #  CB/PB=tan(theta/2) => dist(intersection,tangent_line) = radius/tan(theta/2.0)
    distance_intersection_to_tangent = abs(radius/math.tan(theta/2.0))
    # output( 'dist int to tan',distance_intersection_to_tangent)
    # unit = wxPointUtil.unit(vi) - wxPointUtil.unit(qi)
    # distance_intersection_to_tangent = radius/math.tan(unit[0],unit[1])
    # output( 'dist int to tan',distance_intersection_to_tangent)
    # find the tangent points
    wvtpoint = intersection + wxPointUtil.scale(wv[1]-intersection,distance_intersection_to_tangent/wxPointUtil.distance(intersection,wv[1]))
    pqtpoint = intersection + wxPointUtil.scale(pq[1]-intersection,distance_intersection_to_tangent/wxPointUtil.distance(intersection,pq[1]))

    # center = lines_intersect(wxPointUtil.normal(wvtpoint-intersection)+intersection,wvtpoint,
                             # wxPointUtil.normal(pqtpoint-intersection)+intersection,pqtpoint)
                             
    arcstart = wvtpoint if bigger=='w' else pqtpoint
    center = wvtpoint if bigger=='p' else pqtpoint
    center = center + norm
    
    # draw_segment(arcstart[0],arcstart[1],center[0],center[1])
    
    thickness = int((pqseg.GetWidth()+wvseg.GetWidth())/2.0)
    # output( thickness, pqseg.GetWidth(), wvseg.GetWidth())
    
    
    if theta%(2*math.pi) > math.pi:
        p,start = (wvtpoint,pqtpoint)
    else:
        p,start = (pqtpoint,wvtpoint)
        theta = -theta
        
    n = wxPointUtil.normal(p-intersection)
    n = wxPointUtil.scale(n,radius/wxPointUtil.mag(n))    
    c = p+n
    arcangle = ((math.pi + theta)%(2*math.pi))*180/math.pi

    
    # for p,start in (wvtpoint,pqtpoint),(pqtpoint,wvtpoint):
        # n = wxPointUtil.normal(p-intersection)
        # n = wxPointUtil.scale(n,radius/wxPointUtil.mag(n))    
        # c = p+n
        # arcangle = ((math.pi + theta)%(2*math.pi))*180/math.pi
        # if theta%(2*math.pi) > math.pi:
            # break
        # #draw_segment((p+n)[0],(p+n)[1],p[0],p[1])
        # theta = -theta
    draw_arc(start[0],start[1],c[0],c[1],arcangle,layer=pqseg.GetLayer(),thickness=thickness)

    #draw_arc(arcstart[0],arcstart[1],center[0],center[1],arcangle,layer=pqseg.GetLayer(),thickness=thickness)
    if wvswapped:
        wvseg.SetEnd(wvtpoint)
    else:
        wvseg.SetStart(wvtpoint)
    if pqswapped:
        pqseg.SetEnd(pqtpoint)
    else:
        pqseg.SetStart(pqtpoint)

    return

    angle = ((awv-apq)*180/math.pi)
    if -math.pi < theta*2 < math.pi:
        leftfirst = (pq,wv)
        anglebase = awv
        tangentfirst = (pqtpoint,wvtpoint)
    else:
        leftfirst = (wv,pq)
        anglebase = apq
        tangentfirst = (wvtpoint,pqtpoint)
        angle = -angle
            
    sign = (theta % 2*math.pi) - math.pi
    sign = sign/abs(sign)
    sign = 1

    # bisect leftfirst[0][1] leftfirst[1][1]
    lf01 = leftfirst[0][1]
    lf11 = leftfirst[1][1]
    centerlinepoint = wxPointUtil.scale(lf01-intersection,wxPointUtil.mag(lf11)/wxPointUtil.mag(lf01)) + lf11
    
    rotatevector = lambda v,a: pcbnew.wxPoint(v[0]*math.cos(a)-v[1]*math.sin(a),v[0]*math.sin(a)+v[1]*math.cos(a))

    centerlinepoint = rotatevector(lf01-intersection,math.pi-apq)+intersection
    # vectorsangle = lambda vector1,vector2: math.atan2(vector2.y, vector2.x) - math.atan2(vector1.y, vector1.x);
    
    # test rotatevector:
    # initial=pcbnew.wxPoint(100000000,100000000)
    # sides=8
    # for i in range(sides):
        # rot = rotatevector(initial,i*2*math.pi/sides)
        # draw_segment(0,0,rot[0],rot[1],layer=pcbnew.Eco1_User)
    
    
    # unittuple = lambda x:(x[0]/wxPointUtil.mag(x),x[1]/wxPointUtil.mag(x))
    # scaletuple = lambda x,y:(x[0]*y,x[1]*y)
    # ulf01i = unittuple(leftfirst[0][1]-intersection)
    # ulf11i = unittuple(leftfirst[1][1]-intersection)
    
    # output( 'lf01=',leftfirst[0][1],' ; lf11=',leftfirst[1][1],' ; intersection=',intersection)
    # output( 'lf01-i = ',leftfirst[0][1]-intersection, '; lf11-i = ',leftfirst[1][1]-intersection)
    # output( 'unit = ',(lf01i[0]/wxPointUtil.mag(lf01i),lf01i[1]/wxPointUtil.mag(lf01i)), '; unit = ',(lf11i[0]/wxPointUtil.mag(lf11i),lf11i[1]/wxPointUtil.mag(lf11i)))
    # output( 'mag = ',wxPointUtil.mag(leftfirst[0][1]-intersection))
    # lfadd=lf01i
    # centerlinepoint = wxPointUtil.scale(unittuple(lf01i) + unittuple(lf11i),0.5)
    # output( 'centerlinepoint, intersection = ',centerlinepoint,intersection)
    centervector = centerlinepoint - intersection
    cangle = -math.atan2(centervector[1],centervector[0])
    #draw_segment(centerlinepoint[0],centerlinepoint[1],intersection[0],intersection[1],layer=pcbnew.Dwgs_User)
    
    # output( 'anglebase,cangle,a/2 = ',anglebase*180/math.pi,cangle*180/math.pi,(awv+apq)*90/math.pi,"   awv,apq = ",awv*180/math.pi,apq*180/math.pi )
    arcstart = tangentfirst[1]
    # angle = ((awv-apq)*180/math.pi)

    # output( 'i4=',intersection)

    # output( 'wvtpoint,pqtpoint ',wvtpoint,pqtpoint)
    # # # # # if wvswapped:
        # # # # # wvseg.SetEnd(wvtpoint)
    # # # # # else:
        # # # # # wvseg.SetStart(wvtpoint)
    # # # # # if pqswapped:
        # # # # # pqseg.SetEnd(pqtpoint)
    # # # # # else:
        # # # # # pqseg.SetStart(pqtpoint)
    # Now determine which is the "start", the arc is defined going CCW/Leftward
    # The start point is on the vector with the smallest angle when mod 360
    
    
    # if ((awv%2*math.pi)-(apq%2*math.pi)) > 0: #% (2*math.pi) < math.pi:
        # arcstart = wvtpoint
        # angle = ((awv-apq)*180/math.pi)
    # else:
        # arcstart = pqtpoint
        # angle = ((awv-apq)*180/math.pi)

    
   
    # # polar/rectangular conversions
    # x,y = r*math.cos(tr),r*math.sin(tr)
    # x,y = r*math.cos(td*math.pi/2),r*math.sin(td*math.pi/2)
    # r,tr = math.sqrt(math.pow(x,2),math.pow(y,2)), math.arctan(y/x)
    # r,td = math.sqrt(math.pow(x,2),math.pow(y,2)), math.arctan(y/x)*180/math.pi

    # output( 'i5=',intersection)
    # unit = scale(w,1/dist(w))
    wvtpi = wvtpoint-intersection
    pqtpi = pqtpoint-intersection
    
    lefttpi = arcstart-intersection
    # output( 'center calc info: ',wvtpi,)
    # center = pqtpoint+wxPointUtil.scale(pcbnew.wxPoint(pqtpi[1],-pqtpi[0]),radius/
                                        # math.sqrt(pqtpi[0]*pqtpi[0]+pqtpi[1]*pqtpi[1]))

    center = arcstart+wxPointUtil.scale(pcbnew.wxPoint(lefttpi[1],-lefttpi[0]),sign*radius/
                                        math.sqrt(lefttpi[0]*lefttpi[0]+lefttpi[1]*lefttpi[1]))
    # center = arcstart+wxPointUtil.scale(pcbnew.wxPoint(-lefttpi[1],lefttpi[0]),sign*radius/
                                        # math.sqrt(lefttpi[0]*lefttpi[0]+lefttpi[1]*lefttpi[1]))

                                        
    center2 = wvtpoint+wxPointUtil.scale(pcbnew.wxPoint(-wvtpi[1],wvtpi[0]),radius/
                                        math.sqrt(wvtpi[0]*wvtpi[0]+wvtpi[1]*wvtpi[1]))

    #draw_segment(center[0],center[1],intersection[0],intersection[1],layer=pcbnew.Dwgs_User)
    # output( 'i6=',intersection)
    ci = center - intersection
    acenter = -math.atan2(ci[1],ci[0])
    # output( 'awv,center,apq = ',awv,acenter,apq)
    # output( 'pqtpoint, intersection = ',pqtpoint,intersection)
    pqtpi = pqtpoint-intersection
    # output( 'pqtpi = ',pqtpi)
    center3 = pqtpoint+wxPointUtil.scale(wxPointUtil.normal(pqtpi),radius/
                                        math.sqrt(pqtpi[0]*pqtpi[0]+pqtpi[1]*pqtpi[1]))

                                        
    center4 = pqtpoint+wxPointUtil.scale(pcbnew.wxPoint(pqtpi[1],-pqtpi[0]),radius/
                                        math.sqrt(pqtpi[0]*pqtpi[0]+pqtpi[1]*pqtpi[1]))

    #draw_segment(center3[0],center3[1],center4[0],center4[1],layer=pcbnew.Dwgs_User)

    # wvtpoint-intersection+normal()
    
    #intersect_to_pqtpoint is adjacent
    # output( "angle,s,c=",angle, arcstart,center)
    # draw_segment(arcstart[0],arcstart[1],center[0],center[1])
    # draw_segment(wvtpoint[0],wvtpoint[1],center[0],center[1],layer=pcbnew.Eco1_User)
    # draw_segment(pqtpoint[0],pqtpoint[1],center[0],center[1],layer=pcbnew.Eco1_User)
    # draw_segment(pqtpoint[0],pqtpoint[1],wvtpoint[0],wvtpoint[1],layer=pcbnew.Eco1_User)

    thickness = int((pqseg.GetWidth()+wvseg.GetWidth())/2.0)
    # output( thickness, pqseg.GetWidth(), wvseg.GetWidth())
    draw_arc(arcstart[0],arcstart[1],center[0],center[1],angle,layer=pqseg.GetLayer(),thickness=thickness)
    # 
    # C= math.tan(theta/2.0)
    # if dw < dv :
        # wv = (w,v)
    # else:
        # wv = (v,w)
        
def draw_arc(x1,y1,x2,y2,angle,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):
    """Point 1 is start, point 2 is center. Draws the arc indicated by the x,y values
    on the given layer and with the given thickness."""
    board = getBoard()
    layer = getLayerID(layer)
    ds=pcbnew.DRAWSEGMENT(board)
    ds.SetShape(pcbnew.S_ARC)
    ds.SetLayer(layer)
    ds.SetWidth(max(1,int(thickness)))
    
    # # Line Segment:
    # ds.SetStart(pcbnew.wxPoint(x1,y1))
    # ds.SetEnd(pcbnew.wxPoint(x2,y2))
    
    # Arc
    # output( angle,pcbnew.wxPoint(x1,y1),pcbnew.wxPoint(x2,y2), "thickness=",thickness)
    ds.SetArcStart(pcbnew.wxPoint(x1,y1))
    ds.SetAngle(float(angle)*10)
    ds.SetCenter(pcbnew.wxPoint(x2,y2))
    
    board.Add(ds)
    return ds
    # Need two algorithms:
    # Given two lines and a corner radius,
    #    what is the SetStart() and SetCenter() values?
    

def draw_segment(x1,y1,x2,y2,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):
    """Draws the line segment indicated by the x,y values
    on the given layer and with the given thickness."""
    layer = getLayerID(layer)
    board = getBoard()
    ds=pcbnew.DRAWSEGMENT(board)
    board.Add(ds)
    ds.SetStart(pcbnew.wxPoint(x1,y1))
    ds.SetEnd(pcbnew.wxPoint(x2,y2))
    ds.SetLayer(layer)
    ds.SetWidth(max(1,int(thickness)))
    return ds

def draw_segmentwx(startwxpoint,endwxpoint,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):
    """Draws the line segment indicated by the x,y values
    on the given layer and with the given thickness."""
    layer = getLayerID(layer)
    board = getBoard()
    if pcbnew.IsCopperLayer(layer):
        ds=pcbnew.TRACK(board)
    else:
        ds=pcbnew.DRAWSEGMENT(board)
    board.Add(ds)
    #print(startwxpoint)
    ds.SetStart(startwxpoint)
    ds.SetEnd(endwxpoint)
    ds.SetLayer(layer)
    ds.SetWidth(max(1,int(thickness)))
    return ds

# def layer(layer):
    # try:
        # return int(layer)
    # except:
        # return getBoard().GetLayerID(layer)
    
def draw_text(text,pos,size,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):
    """Draws the line segment indicated by the x,y values
    on the given layer and with the given thickness."""
    
# 'Hello 100,100 MM 10,10 MM 1 MM F.SilkS DRAWTEXT'
# '0,0,100,100 MM DRAWSEGMENTS'
    # output("Text at position {}, {}".format(pos[0],pos[1]))
    size = pcbnew.wxSize(size[0],size[1])
    pos = pcbnew.wxPoint(pos[0],pos[1])
    board = getBoard()
    thickness = int(thickness)
    layer = getLayerID(layer)
    
    #ds=pcbnew.DRAWSEGMENT(board)
    ds=pcbnew.TEXTE_PCB(board)
    board.Add(ds)
    # ds.SetStart(pcbnew.wxPoint(x1,y1))
    # ds.SetEnd(pcbnew.wxPoint(x2,y2))
    #ds.SetLayer(layer)
    #ds.SetWidth(max(1,int(thickness)))
    
    ds.SetTextPos(pos) # wxPoint
    ds.SetTextAngle(0.0)
    ds.SetText(text)
    ds.SetThickness(thickness)
    ds.SetTextSize(size)
    ds.SetLayer(layer)
    return ds
    # SetTextWidth(x)
    # SetTextHeight(x)
    # SetItalic()
    # SetBold(x)
    # SetVisible(x)
    # SetMirrored(x)
    # SetMultilineAllowed(x)
    # SetHorizJustify(x)
    # SetVertJustify(x)
    # SetEffects(x)
# ?    SetTextPos(x)
    # Offset(x)
    # LenSize(x)
    
    # SetHighlighted()
    # SetBrightened()
    # SetSelected()
    # SetState(x,y)
    
    
def CALLLIST(modulelist,function):
    """works with function 'Pads' or 'GraphicalItems'"""
    items = []
    for m in modulelist:
        items.extend(getattr(m,function)())
    return items
    
def gridboxes(w,getdict=None,setdict=None,setelement=None):
    """returns a set of grid boxes (upper left corners) that
    correspond to point w
    if getdict is set, then gridboxes is used to retreive its elements
    if setdict is set, then gridboxes is used to set its elements"""
    # 
    # Put each point in 4 boxes.
    # when searching, search 4 boxes.
    # Union of all hits should be considered "connected"
    #

    # Min capture distance is increment away in any direction
    # Max capture distance is +/- 4.25*increment away
    #   (3 diagonals of increment square)
    #
    # Usage:
    #
    # for setting values:
    # map(lambda x: seg_by_point[x].append(seg),gridboxes(point))
    #
    # for retrieving segs:
    # seglist = []
    # map(lambda x: seglist.extend(seg_by_point[x]),gridboxes(point))
    #
    round_bits = 5
    increment = 1 << round_bits
    mask = -1 << round_bits
    
    c1 = w[0] & mask
    r1 = w[1] & mask
    r0 = r1 - increment
    c0 = c1 - increment
    #output('rb=%d inc=%x mask=%x'%(round_bits,increment,mask))
    # Boxes to place/search
    boxes = ((c0,r0),(c0,r1),(c1,r0),(c1,r1))
    if getdict is not None:
        seglist = []
        map(lambda x: seglist.extend(getdict[x]),boxes)
        #output('seglist=%s'%str(seglist))
        return seglist
    if setdict is not None:
        map(lambda x: setdict[x].append(setelement),boxes)
        return None

    return boxes
    
def point_round128(w):
    mask = -1 << 5
    #return w
    return w.__class__(int(w[0])&mask,int(w[1])&mask)


    # # TODO: maybe add layer, CPolyLine, and priority to drawparams
# def newzone(points, netname, layer, CPolyLine=pcbnew.CPolyLine.NO_HATCH, priority=0):
    # """NOT IMPLEMENTED"""
    # # CPolyLine values: NO_HATCH, DIAGONAL_FULL, DIAGONAL_EDGE
    
    # priority = int(priority)

    # if isinstance(CPolyLine,basestring):
        # CPolyLine = getattr(pcbnew.CPolyLine,CPolyLine)
        
    # try:
        # layer = int(layer)
    # except:
        # layer = board.GetLayerID(layer)


    # nets = board.GetNetsByName()
    
    # # for netname,layername in (("+5V", "B.Cu"), ("GND", "F.Cu")):
    # netinfo = nets.find(netname).value()[1]
    # #layer = layertable[layername]
    # newarea = board.InsertArea(netinfo.GetNet(), priority, layer, points[0][0], points[0][1], CPolyLine)
    # newoutline = newarea.Outline()

    # # if you get a crash here, it's because you're on an older version of pcbnew.
    # # the data structs for polygons has changed a little. The old struct has a
    # # method called AppendCorner. Now it's just Append. Also, the call to CloseLastContour,
    # # commented below used to be needed to avoid a corrupt output file.
    # for p in range(1,len(points)):
        # newoutline.Append(points[p][0],points[p][1]);
        
    # # newoutline.Append(boardbbox.xl, boardbbox.yh);
    # # newoutline.Append(boardbbox.xh, boardbbox.yh);
    # # newoutline.Append(boardbbox.xh, boardbbox.yl);
    # # this next line shouldn't really be necessary but without it, saving to
    # # file will yield a file that won't load.
    # # newoutline.CloseLastContour()

    # # don't know why this is necessary. When calling InsertArea above, DIAGONAL_EDGE was passed
    # # If you save/restore, the zone will come back hatched.
    # # before then, the zone boundary will just be a line.
    # # Omit this if you are using pcbnew.CPolyLine.NO_HATCH
    # #pcbnew.CPolyLine. (DIAGONAL_EDGE, DIAGONAL_FULL, NO_HATCH)
    # if CPolyLine != pcbnew.CPolyLine.NO_HATCH:
        # newarea.Hatch()
        
def SETLENGTH(initlist, length):
    """NOT IMPLEMENTED"""
    # Get GraphicalItems and Drawings.
    allitems = list(getBoard().GetDrawings())
    for m in getBoard().GetModules():
        allitems.extend(m.GraphicalItems())
    wholelist = filter(lambda x: isinstance(x,pcbnew.DRAWSEGMENT),allitems)
    
    # Given the segment list, determine the connected segments.
    # Get the start and end points of each item in the wholelist
    se = map(lambda x: get_ds_ends(x),wholelist)
    d = defaultdict(list)
    
    # For each segment point, set the dictionary to indicate which gridboxes the item is in.
    for i,item in enumerate(wholelist):
        gridboxes(se[i][0],setdict=d,setelement=item)
        gridboxes(se[i][1],setdict=d,setelement=item)
    i = 0
    retValue = list(initlist)
    retValueSet = set()
    
    # now check each item in the initlist, and see if any points in the wholelist
    # are in the same gridbox.
    while i < len(retValue):
        if i > 1000:
            break
        # get the segment end points
        se = get_ds_ends(retValue[i])
        
        # 
        try: d[key].remove(retValue[i]) 
        except: pass
        retValue.extend(gridboxes(se[0],getdict=d))
        try: d[key].remove(retValue[i]) 
        except: pass
        newset = set(gridboxes(se[1],getdict=d))
        
        for member in newset:
            if member not in retValueSet:
                retValueSet.add(member)
        i += 1
    return list(set(retValue)) # remove duplicates
    
def CONNECTED(wholelist, initlist):
    # Make generic and approximate
    # output('1')

    se = map(lambda x: get_ds_ends(x),wholelist)
    #output(str(se))
    # output('2a')
    #output(str([list]))
    # output('2b')
    d = defaultdict(list)
    # output('3')
    for i,item in enumerate(wholelist):
        # d[point_round128(se[i][0])].append(item)
        # d[point_round128(se[i][1])].append(item)
        # output('se[%d]= %s; item=%s'%(i,se[i],str(item)))
        gridboxes(se[i][0],setdict=d,setelement=item)
        gridboxes(se[i][1],setdict=d,setelement=item)
        # s=point_round128(se[i][0])
        # e=point_round128(se[i][1])
        # output('s=%s'%str(s))
        # output('e=%s'%str(e))
        # output('s0=%s'%str(s[0]))
        # output('s1=%s'%str(s[1]))
        # d[tuple(s)].append(item)
        # d[tuple(e)].append(item)
    # output('4')
    # k=d.keys()[0]
    # output('d = '+str(len(d))+str((k,d[k])))
    # for i in d.keys()[:10]:
            
        # output('key=%s val=%s'%(i,d[i]))
    # s = map(lambda x: (x.GetStart().x,x.GetStart().y),wholelist)
    # e = map(lambda x: (x.GetEnd().x,x.GetEnd().y),wholelist)
    # d = defaultdict(list)
    # for i,item in enumerate(wholelist):
        # d[s[i]].append(item)
        # d[e[i]].append(item)
    # Now we have items by rounded coordinates for fast lookup
    i = 0
    retValue = list(initlist)
    retValueSet = set()
    
    # output('initlist = '+str(initlist))
    while i < len(retValue):
        if i > 1000:
            break
        #output('rV len=%s'%len(retValue))
        se = get_ds_ends(retValue[i])
        #output(str(se))
        
        #s=point_round128(se[0])
        # output('s = '+str(s))
        #key=tuple(s) # start x and y
        #key=(retValue[i].GetStart().x,retValue[i].GetStart().y)
        # output('key = %s'%str(key))
        try: d[key].remove(retValue[i]) 
        except: pass
        # output('found connection 1')
        
        # retValue.extend(d[key])
        retValue.extend(gridboxes(se[0],getdict=d))
        #e=point_round128(se[1])
        # output('e = '+str(e))
        #key=tuple(e) # end x and y
        #key=(retValue[i].GetEnd().x,retValue[i].GetEnd().y)
        try: d[key].remove(retValue[i]) 
        except: pass
        # output('found connection 2')
        newset = set(gridboxes(se[1],getdict=d))
        
        for member in newset:
            if member not in retValueSet:
                # output('adding member')
                #retValue.append(member)
                retValueSet.add(member)
        i += 1
    # output('i=%d'%i)
    return list(set(retValue)) # remove duplicates

def bbintersect(seg1,seg2):
    s1bb = seg1.GetBoundingBox()
    s2bb = seg2.GetBoundingBox()
    return True

DEBUG = False
def CUT():

    cuttees = filter(
        lambda x: isinstance(x,pcbnew.DRAWSEGMENT) and x.GetShape() == pcbnew.S_SEGMENT,
        getBoard().GetDrawings())

    cutter = filter(lambda x:x.IsSelected(),cuttees)[0]
    scutter,ecutter = get_ds_ends(cutter)
    if DEBUG:
        output("Cutting {} segments with {}".format(len(cuttees),str(cutter)))
    bb = cutter.GetBoundingBox()
    cutl,cutr,cutt,cutb = bb.GetLeft(),bb.GetRight(),bb.GetTop(),bb.GetBottom()
    within = []
    for cuttee in cuttees:
        if cuttee == cutter:
            # output('=')
            if DEBUG:
                output("Cuttee is cutter")
            continue
        if not isinstance(cuttee,pcbnew.DRAWSEGMENT):
            if DEBUG:
                output("Cuttee is not DRAWSEGMENT")
            continue
        if cuttee.GetShape() != pcbnew.S_SEGMENT:
            if DEBUG:
                output("Cuttee shape is not S_SEGMENT: {}".format(cuttee.GetShape()))
            continue
        #output(get_ds_ends(cuttee))
        bb = cuttee.GetBoundingBox()
        segl,segr,segt,segb = bb.GetLeft(),bb.GetRight(),bb.GetTop(),bb.GetBottom()
        if segr < cutl or segl > cutr or segb < cutt or segt > cutb:
            if DEBUG:
                output("Cuttee outside cutter bounding box")
            continue
        #output('!')

        # Get intersection point
        s,e = get_ds_ends(cuttee)
        if DEBUG:
            output("Evaluating {}".format(get_ds_ends(cuttee)))
        intersect = lines_intersect(s,e,scutter,ecutter)
        #output('intersect',intersect,'s',s,'e',e,'scut',scutter,'ecut',ecutter)
        if intersect is None:
            if DEBUG:
               output('intersect returned None')
            continue
        
        
        if ((s[0] <= intersect[0] <= e[0]) or (e[0] <= intersect[0] <= s[0])) and \
           ((s[1] <= intersect[1] <= e[1]) or (e[1] <= intersect[1] <= s[1])) and \
        ((scutter[0] <= intersect[0] <= ecutter[0]) or (ecutter[0] <= intersect[0] <= scutter[0])) and \
        ((scutter[1] <= intersect[1] <= ecutter[1]) or (ecutter[1] <= intersect[1] <= scutter[1])):

            if intersect[0] == s[0] and intersect[1] == s[1]:
                continue
        # see if intersection point is within s and e
        #if (s[0] < intersect[0] < e[0]) and (s[1] < intersect[1] < e[1]) and \
           #(scutter[0] < intersect[0] < ecutter[0]) and (scutter[1] < intersect[1] < ecutter[1]):
            if DEBUG:
                output("Cutting {}".format(get_ds_ends(cuttee)))
            newe = tuple(e)
            cuttee.SetEnd(intersect)
            draw_segment(intersect[0],intersect[1],newe[0],newe[1],layer=cuttee.GetLayer(),thickness=cuttee.GetWidth())
        else:
            if DEBUG:
                output("Cuttee {} doesn't intersect cutter {}. Intersect point: {}".format(get_ds_ends(cuttee),get_ds_ends(cutter),intersect))

            #output('new segment',intersect, e)
            #output('cut',s,e,'at',intersect)        
        # within.append(cuttee) 
    #pcbnew.UpdateUserInterface()
    #cutter.UnLink()
    getBoard().GetDrawings().Remove(cutter)
    #cutter.DeleteStructure()
    return None
def DRAWPARAMS(dims,layer):
 	# GR_TEXT_HJUSTIFY_LEFT = _pcbnew.GR_TEXT_HJUSTIFY_LEFT
 	# GR_TEXT_HJUSTIFY_CENTER = _pcbnew.GR_TEXT_HJUSTIFY_CENTER
 	# GR_TEXT_HJUSTIFY_RIGHT = _pcbnew.GR_TEXT_HJUSTIFY_RIGHT
 	# GR_TEXT_VJUSTIFY_TOP = _pcbnew.GR_TEXT_VJUSTIFY_TOP
 	# GR_TEXT_VJUSTIFY_CENTER = _pcbnew.GR_TEXT_VJUSTIFY_CENTER
 	# GR_TEXT_VJUSTIFY_BOTTOM = _pcbnew.GR_TEXT_VJUSTIFY_BOTTOM
    
    # Text,0,0,Hello,this,is,interesting,and,very,very,very,long split newdrawing 
    # copy
    # copy
    # pcbnew list GR_TEXT_HJUSTIFY_RIGHT attr delist
    # SetHorizJustify callargs
    # GetHorizJustify call
    # The following works when the text object is a single item or a list of one or more
    # currently, the "delist" is important
    # copy copy pcbnew list GR_TEXT_HJUSTIFY_LEFT attr delist print SetHorizJustify callargs pop GetHorizJustify call print pop refresh
    #
    # : justifyl "Text [TEXTOBJ_LIST] Horizontal left justify text object" pcbnew list GR_TEXT_HJUSTIFY_LEFT attr delist SetHorizJustify callargs ;
    # : justifyc "Text [TEXTOBJ_LIST] Horizontal center justify text object" pcbnew list GR_TEXT_HJUSTIFY_CENTER attr delist SetHorizJustify callargs ;
    # : justifyr "Text [TEXTOBJ_LIST] Horizontal right justify text object" pcbnew list GR_TEXT_HJUSTIFY_RIGHT attr delist SetHorizJustify callargs ;
    # : justifym "Text [TEXTOBJ_LIST] Vertical left justify text object" pcbnew list GR_TEXT_VJUSTIFY_CENTER attr delist SetVertJustify callargs ;
    # : justifyt "Text [TEXTOBJ_LIST] Vertical top justify text object" pcbnew list GR_TEXT_VJUSTIFY_TOP attr delist SetVertJustify callargs ;
    # : justifyb "Text [TEXTOBJ_LIST] Vertical bottom justify text object" pcbnew list GR_TEXT_VJUSTIFY_BOTTOM attr delist SetVertJustify callargs ;
    #
    # SetHorizJustify (self, aType) 
    # SetVertJustify (self, aType)




    t,w,h = dims.split(',') if isinstance(dims,basestring) else dims \
    if hasattr(dims,'__iter__') else [dims]

    layerID = getLayerID(layer)

    _user_stacks['Params'][-1].update({'t':t,'w':w,'h':h,'l':layer})

def list_to_paired_list(input):
    a = iter(input)
    input = [pcbnew.wxPoint(int(x),int(y)) for x,y in zip(a, a)]
    return input

def convert_to_points(input):
    #output( 'ctp1: ',input
    if isinstance(input,basestring):
        input = map(lambda x: float(x),input.split(','))
    
    if (not hasattr(input,'__iter__')) :
        input=[input]
    #output( 'input: ',input,'hasget ',hasattr(input,'__getitem__'),'firsthasiter ',hasattr(input[0],'__iter__')
    if  hasattr(input,'__getitem__') and not hasattr(input[0],'__iter__'):
        input=[input]

    #output( 'ctp2: ',input
    # input is now a list of list(s). It could be either
    # list of strings, numbers, or wxPoints.
    
    input = [list_to_paired_list(i) if isinstance(i[0],(basestring,float,int)) else i for i in input]
            
    return input
    # if isinstance(input[0],pcbnew.wxPoint):
        # input = [input]
    # else:
        # output( 'ctp2.1: ',input,hasattr(input[0],'__iter__')
        # if not hasattr(input[0],'__iter__'):
            # input = [input]
        # output( 'ctp2.2: ',input
        # for i in input:
            # list_to_paired_list(i)
    # output( 'ctp3: ',input)
    # return input

# proposed binary geom:
# from enum import Enum
# class BG_TYPE(Enum):
    # polygon = 1
    # hole = 2
    # line = 3

class binarygeom:
    # for now, we'll support only a stream of 16-bit integers with the high bits indicating shape type
    # we'll also presume that all polygons/holes are in the same DRAWSEGMENT polygon, to be subsequently fractured.
    numtypebits = 4
    type16mask = -1 << (16-numtypebits)
    type8mask = -1 << (8-numtypebits)
    def __init__(self):
        self._binaryarray = None
        self.next = self.__next__
        pass
    # def __iter__(self):
        # iba = iter(self._binaryarray)
        # for byte1 in iba:
            # byte2 = iba.next()
            # if byte1 & type8mask:
                # # this is a new shape
                # shape = byte1>>(8-numtypebits) & (numtypebits - 1)
                # byte1 = byte1 & (8-numtypebits)-1
        # # how do we differentiate between a shape and a point?
        # # we'll abandon __iter__ until I figure this out
    # def __next__(self):
        # pass
    def getdrawsegment(layer=None,width=None):
        ds = pcbnew.DRAWSEGMENT()
        ds.SetShape(pcbnew.S_POLYGON)
        if layer is not None:
            ds.SetLayer(getLayerID(layer))
        if width is not None:
            ds.SetWidth(int(width))

        #xxx
        iba = iter(self._binaryarray)
        for byte1 in iba:
            byte2 = iba.next()
            if byte1 & type8mask:
                # this is a new shape
                shape = byte1>>(8-numtypebits) & (numtypebits - 1)
                byte1 = byte1 & (8-numtypebits)-1
                
        
class streamgeom:
    def __init__(self):
        self._transformstack = []
    def streamgeom(self,inputiterable):
        # Argtype
        # p - point, converted by units
        # P - point, converted by units, followed by all points
        # n - number, converted by units
        # N - number, not converted by units
        # s - string
        # S - string followed by all strings
        if len(self._transformstack) == 0:
            self._transformstack.append(matrixTransform2d())
        
        argdict = {
            'Group':' '
            ,'Line':'pp'
            ,'CircleC':'pn'
            ,'CircleR':'ppn'
            ,'CircleO':'ppp'
            ,'CircleP':'pp'
            ,'ArcC':'ppN'
    #        ,'ArcR':'ppn'
            ,'ArcO':'ppp'
    #        ,'ArcP':'ppp'
            ,'Polygon':'p'
            ,'Polygon.':'p' # continuation polygon. Must be preceded by a polygon. Will be put into the prior DRAWSEGMENT S_POLYGON
            ,'Hole':'p'
            ,'Polyline':'p'
            ,'Bezier':'pppp'
            ,'Layer':'s'
            ,'Text':'pT'
            ,'Point':'p'
            ,'Position':'f'
            ,'PositionMM':'f'
            ,'PositionMils':'f'
            ,'PositionMil':'f'
            ,'Thickness':'n'
            ,'Dot':'n'
            ,'Via':'s'
            ,'Corner':'n'
            ,'PolylineRounded':'nP'
            ,'TMatrix':'nnnnnnnnn'
            ,'TTranslate':'f'
            ,'TScale':'NN'
            ,'TShear':'f'
            ,'TRotate':'N'
            ,'S':'N'
            ,'Sy':'N'
            ,'+T':'f'
            ,'R':'N'
            ,'Z':'f'
            ,'Sx':'N'
            ,'S':'N'
            ,'T+':' '
            ,'T':'NN'
            ,'Tmm':'NN'
            ,'Tmil':'NN'
            ,'Tmils':'NN'
            ,'T-':' '
            ,'mm':' '
            ,'mil':' '
            ,'mils':' '
        }
        transformation={
            # 'TMatrix':lambda params,o:        self._transformstack[-1].assign(*params[0])
            # ,'TTranslate':lambda params,o:    self._transformstack[-1].translate(*tuple(params[0]))
            # ,'TScale':lambda params,o:        self._transformstack[-1].scale(params,origin=o)
            # ,'TShear':lambda params,o:        self._transformstack[-1].shear(*params[0],origin=o)
            # ,'TRotate':lambda params,o:       self._transformstack[-1].rotate(*params[0],origin=o)
            # ,'mm':lambda params,o:       self._transformstack[-1].scale((pcbnew.IU_PER_MM,pcbnew.IU_PER_MM),origin=o)
            # ,'mil':lambda params,o:       self._transformstack[-1].scale((pcbnew.IU_PER_MILS,pcbnew.IU_PER_MILS),origin=o)
            # ,'mils':lambda params,o:       self._transformstack[-1].scale((pcbnew.IU_PER_MILS,pcbnew.IU_PER_MILS),origin=o)
            'S':lambda params:       self._transformstack[-1].scale((params[0],params[0]),pre=True)#,origin=self._transformstack[-1].transform((0,0)))
            ,'Sy':lambda params:       self._transformstack[-1].scale((1,params[0]),pre=True)#,origin=self._transformstack[-1].transform((0,0)))
            ,'+T':lambda params:    self._transformstack[-1].translate(*params[0],pre=True)
            # ,'T':lambda params:    self._transformstack[-1].translate(*self._transformstack[-1].transform(params[0]),origin=self._transformstack[-1].transform((0,0)))
            ,'R':lambda params:    self._transformstack[-1].rotate(params[0],pre=True)#,origin=self._transformstack[-1].transform((0,0)))
            ,'Z':lambda params:    self._transformstack[-1].shear(*params[0])#,origin=self._transformstack[-1].transform((0,0)))
            ,'T+':lambda params:    self._transformstack.append(self._transformstack[-1].copyTransform())
            ,'T-':lambda params:    self._transformstack.pop()
            ,'T':lambda params:    self._transformstack[-1].translate(*params,pre=False)
            ,'Tmm':lambda params:   self._transformstack[-1].translate(params[0]*pcbnew.IU_PER_MM,params[1]*pcbnew.IU_PER_MM,pre=False)
            ,'Tmil':lambda params:   self._transformstack[-1].translate(params[0]*pcbnew.IU_PER_MILS,params[1]*pcbnew.IU_PER_MILS,pre=False)
            ,'Tmils':lambda params:   self._transformstack[-1].translate(params[0]*pcbnew.IU_PER_MILS,params[1]*pcbnew.IU_PER_MILS,pre=False)

            # 
            # elif geom[0].startswith('Position'):
                # if geom[0].tolower().endswith('mm'):
                # if geom[0].tolower().endswith('mil') or geom[0].tolower().endswith('mils'):

    #        params=((x,y),)
        #Ts, Tt, Tr, Tz, T1 (one)= identity? 
        # Or even just S, T, R, Z? They could be extended to Sx, Sy, Tx, Ty, Zx, and Zy if you only want to specify x or y transform. 
        }
        # Transform,Type(S),N...
        # Transform,Matrix,n11,n21,n31,n12,n22,n32,n13,n23,n33 assigs the given n[col][row] numbers to the transformation matrix (first row is n11,n21,n31)
        # Transform,Translate,x,y - moves the coordinate frame
        # Transform,Scale,x,y     - scales the coordinate frame relative to the current point
        # Transform,Rotate,d      - rotates the coordinate frame around the current point by d degrees
        # Transform,Shear,x,y     - shears the coordinate frame relative to the current point

        unitconversion = {
            'mm':pcbnew.IU_PER_MM
            ,'mil':pcbnew.IU_PER_MILS
            ,'mils':pcbnew.IU_PER_MILS
            ,'native':1.0
            ,'nm':1.0
        }
    # Line,mm,20,10,22,12 split newdrawing refresh
    # ArcC,mm,20,10,22,12,90 split newdrawing refresh
    # ArcM,mm,22,12,20,12.8,18,12 split newdrawing refresh
    # CircleP,mm,-10,-10,5 split newdrawing refresh
    # Polygon,mm,30,0,30,1,25,1 split newdrawing refresh
    # Bezier,mm,30,0,30,1,25,1 split newdrawing refresh

        iterstack = [iter(inputiterable)]
        outlist = []
        currentarg = None # argtypes.next()
        argpending = []

        lengthmultiplier = 1.0
        while iterstack:
            try:
                val = iterstack[-1].next()
            except:
                iterstack.pop()
                continue
            # if not isiter(val):
                #output('processing {}'.format(val))
            # output('VAL = {}'.format(val))
            if currentarg == 'T':
                if val == 'EndText':
                    currentarg = None
                    if outlist:
                        yield outlist
                        del outlist[:]
                else:
                    outlist.append(val)
                continue
                
            # output('Item: {}'.format(val))
            #  Polygon,mm,0,0,10,0,10,10,0,10
            argtype = isinstance(val, collections.Hashable)
            if argtype:
                argtype = argdict.get(val,False)
                currentmult = unitconversion.get(val,None)
                if currentmult is not None:
                    # output('Found unit {}'.format(val))
                    self._transformstack[-1].scale((currentmult,currentmult))
                    onezero = self._transformstack[-1].transform((1,0))
                    lengthmultiplier = math.sqrt(onezero[0]*onezero[0]+onezero[1]*onezero[1])
                    continue
                if argtype:
                    if outlist:
                        texec = transformation.get(outlist[0],None)
                        if texec:
                            # output("Transform origin right before output yield")
                            #output('{}'.format(','.join(map(str,outlist))))
                            # output("Transforming origin point with {}".format(outlist))
                            #output("texec arg 0 = {}".format(outlist[1:]))
                            texec(outlist[1:])
                            # currentarg = argiter.next()
                            # output('currentarg {}'.format(currentarg))
                        else:
                            yield outlist
                        del outlist[:]
                    # output("Found {}".format(val))
                    
                    argiter = itertools.cycle(argtype)
                    currentarg = argiter.next()
                    
                    
                    

                    outlist.append(val)
                    continue
            #currentarg = argiter.next()
            if currentarg == 'P':
                argiter = itertools.cycle('p')
                currentarg = argiter.next()
            if isinstance(val,pcbnew.wxPoint):
                if currentarg not in 'pf':
                    raise TypeError('{} expected, got {}'.format(currentarg,type(val)))
    #            outlist.append(pcbnew.wxPoint(*self._transformstack[-1].transform(val)))
                if currentarg == 'p':
                    # output("Transform existing point right before output append")
                    outlist.append(pcbnew.wxPoint(*self._transformstack[-1].transform(val)))
                else:
                    outlist.append(val)
                    
                currentarg = argiter.next()
                continue
            if isiter(val):
                iterstack.append(iter(val))
                continue
            if currentarg == 's':
                outlist.append(str(val))
                continue
            if currentarg == 'S':
                outlist.append(str(val))
                argiter = itertools.cycle('s')
                currentarg = argiter.next()
                continue
            if isinstance(val,basestring):
                    val = float(val)
                    
            if isinstance(val,(float,int)):
                if currentarg == 'N':
                    outlist.append(val)
                    currentarg = argiter.next()
                    continue
                if currentarg == 'n':
                    outlist.append(val*lengthmultiplier)
                    currentarg = argiter.next()
                    continue
                else:
                    argpending.append(val*lengthmultiplier)
                        
                    if currentarg in "pf" and len(argpending) == 2:
                        if currentarg == 'f':
                            #output("Not transforming point before assembling from argpending from {}".format(argpending))
                            #outlist.append(tuple(argpending))
                            outlist.append(pcbnew.wxPoint(*argpending))
                        else:
                            # output("Transform point right before assembling from argpending from {}".format(argpending))
                            outlist.append(pcbnew.wxPoint(*self._transformstack[-1].transform(argpending)))
                            # output("to {}".format(outlist[-1]))
                        del argpending[:]
                        currentarg = argiter.next()
                        continue
        if outlist:
            yield outlist
# TTranslate,mm,0,110 split ab\ncd stringtogeom append newdrawing refresh
# Point,0,0,Dot,mm,1,TTranslate,mm,0,10,Point,0,0,Dot,2,TTranslate,mm,0,10,Point,0,0,Dot,3 split newdrawing refresh
# Point,0,0,TTranslate,mm,0,0,TScale,native,3.5,3.5,mm,Polygon,-5,-5,5,-5,5,5,-5,5  split newdrawing refresh
# Point,0,0,Dot,100000,S,2,T,0,1000000,Point,0,0,Dot,2000000,T,0,10000000,Point,0,0,Dot,3000000 split newdrawing refresh

def listtoargs(argtypestring, inlist):
    # Convert an inlist into an outlist based on argtypes.
    # argyptestring is a string of characters:
    # p : point (can be a wxPoint, two numbers (either in a list/tuple or not)
    # n : number, (float, int, or string)
    # returns a linear list of arguments of type specified by argtypestring
    # 
    # useful to have {'Line':'pp', 'ArcA': 

        # https://stackoverflow.com/a/1625013
    # def grouper(n, iterable, fillvalue=None):
        # "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
        # args = [iter(iterable)] * n
    # return itertools.zip_longest(*args, fillvalue=fillvalue)
    
    # def mygrouper(n, iterable):
        # args = [iter(iterable)] * n
        # return ([e for e in t if e != None] for t in itertools.zip_longest(*args))
        
    # zip(*(iter(the_list),) * group_size) # input is exact multiple, drops last if incomplete
    # itertools.izip_longest(*(iter(range(10)),) * 3) # input is not exact multiple, fills with None
    iterstack = [iter(inlist)]
    outlist = []
    argtypes = itertools.cycle(argtypestring)
    currentarg = argtypes.next()
    argpending = []
    
    while iterstack:
        try:
            val = iterstack[-1].next()
        except:
            iterstack.pop()
            continue
        if isinstance(val,pcbnew.wxPoint):
            if currentarg != "p":
                raise TypeError('wxPoint expected, got {}'.format(type(val)))
            outlist.append(val)
            currentarg = argtypes.next()
            continue
        if isiter(val):
            iterstack.append(iter(val))
            continue
        if isinstance(val,basestring):
            val = float(val)
            
        if isinstance(val,(float,int)):
            if currentarg == "n":
                outlist.append(val)
                currentarg = argtypes.next()
                continue
            else:
                argpending.append(val)
                if currentarg == "p" and len(argpending) == 2:
                    outlist.append(pcbnew.wxPoint(*argpending))
                    del argpending[:]
                    currentarg = argtypes.next()
                    continue
    return itertools.izip_longest(*(iter(outlist),) * len(argtypestring)) # input is not exact multiple, fills with None
    # after return, raise exception if returnval[-1] is None
    # return outlist
    
# https://github.com/openscopeproject/InteractiveHtmlBom/blob/d14cdc935bfcd5e903237219ccd7f4fb5cea6075/InteractiveHtmlBom/ecad/kicad.py#L108
def parse_poly_set(polygon_set):
    result = []
    for polygon_index in range(polygon_set.OutlineCount()):
        outline = polygon_set.Outline(polygon_index)
        if not hasattr(outline, "PointCount"):
            self.logger.warn("No PointCount method on outline object. "
                             "Unpatched kicad version?")
            return result
        parsed_outline = ['Polygon']
        for point_index in range(outline.PointCount()):
            cp = outline.CPoint(point_index)
            parsed_outline.append([cp.x,cp.y])
        #parsed_outline.append('Polygon')
        result.extend(parsed_outline)
    return result

def parse_zones(zone_containers):
    if isinstance(zone_containers,pcbnew.ZONE_CONTAINER):
        return parse_poly_set(zone_containers.GetFilledPolysList())
    result = []
    for zone in zone_containers:  # type: pcbnew.ZONE_CONTAINER, zc is not Iterable neither is zc.Iterate()
        # ignoring GetMinThickness, GetNetname and GetLayer() # GetMinThickness,GetNetname,GetLayer
        result.append(parse_poly_set(zone.GetFilledPolysList()))
    return result

def makeline(start,end):
    output("line: start={} end={}".format(start,end))

# Used for converting three points on circumference to circle or arc
# first, matrix functions
# from https://stackoverflow.com/a/39881366
def transposeMatrix(m):
    return map(list,zip(*m))

def getMatrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def getMatrixDeterminant(m):
    #base case for 2x2 matrix
    if len(m) == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]

    determinant = 0
    for c in range(len(m)):
        determinant += ((-1)**c)*m[0][c]*getMatrixDeterminant(getMatrixMinor(m,0,c))
    return determinant

def getMatrixInverse(m):
    determinant = getMatrixDeterminant(m)
    #special case for 2x2 matrix:
    if len(m) == 2:
        return [[m[1][1]/determinant, -1*m[0][1]/determinant],
                [-1*m[1][0]/determinant, m[0][0]/determinant]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(m)):
        cofactorRow = []
        for c in range(len(m)):
            minor = getMatrixMinor(m,r,c)
            cofactorRow.append(((-1)**(r+c)) * getMatrixDeterminant(minor))
        cofactors.append(cofactorRow)
    cofactors = transposeMatrix(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/determinant
    return cofactors

# from https://stackoverflow.com/a/45203136
def getVectorMatrixMultiply(v, G):
    result = []
    for i in range(len(G[0])): #this loops through columns of the matrix
        total = 0
        for j in range(len(v)): #this loops through vector coordinates & rows of matrix
            total += v[j] * G[j][i]
        result.append(total)
    return result
def getMatrixMultiply(F, G):
    result = []
    for j in range(len(G)): #this loops through a column of F & rows of G
        total = list(range(len(G[0])))
        for i in range(len(G[0])): #this loops through columns of the matrix
            total[i] += F[i][j] * G[j][i]
        result.append(total)
    return result

# Calculate center (h,k) and radius (r) from three points.
# from http://mathforum.org/library/drmath/view/55239.html
         # |x1^2+y1^2  y1  1|        |x1  x1^2+y1^2  1|
         # |x2^2+y2^2  y2  1|        |x2  x2^2+y2^2  1|
         # |x3^2+y3^2  y3  1|        |x3  x3^2+y3^2  1|
     # h = ------------------,   k = ------------------
             # |x1  y1  1|               |x1  y1  1|
           # 2*|x2  y2  1|             2*|x2  y2  1|
             # |x3  y3  1|               |x3  y3  1|
             
# r = sqrt[(x1-h)^2+(y1-k)^2]
def centerFromPoints(p1,p2,p3):
  
  x1,y1 = p1
  x2,y2 = p2
  x3,y3 = p3
  
  if (x1==x2 and y1==y2) or (x1==x3 and y1==y3) or (x2==x3 and y2==y3):
    raise TypeError("All points must be different {}, {}, {}.".format(p1,p2,p3))
    
  a = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - x3 * y2
  if abs(a) < 1e-10:
    raise TypeError("Divisor is close to zero {}.".format(a))
  
  b = ((x1 * x1 + y1 * y1) * (y3 - y2) 
        + (x2 * x2 + y2 * y2) * (y1 - y3)
        + (x3 * x3 + y3 * y3) * (y2 - y1))
 
  c = ((x1 * x1 + y1 * y1) * (x2 - x3) 
        + (x2 * x2 + y2 * y2) * (x3 - x1) 
        + (x3 * x3 + y3 * y3) * (x1 - x2))
 
  x = -b / (2 * a)
  y = -c / (2 * a)

  return (x,y)

sign = lambda a: (a>0) - (a<0)
def centerFromPointsAndRadius(a,b,r):
    # from http://mathforum.org/library/drmath/view/53027.html
    x1,y1 = a
    x2,y2 = b
    dx = x2 - x1
    dy = y1 - y2
    q = math.sqrt(dx*dx + dy*dy)
    x3 = (x1+x2)/2.0
    y3 = (y1+y2)/2.0

    x = x3 + sign(r)*math.sqrt(r*r-q*q/4)*dy/q
    y = y3 + sign(r)*math.sqrt(r*r-q*q/4)*dx/q
    return (x,y)

def centerFromPoints_old(a,b,c):
    denominator = [[2*a[0], 2*a[1], 2],[2*b[0],2*b[1],2],[2*c[0],2*c[1],2]]
    denominator = getMatrixInverse(denominator)
    #output('Denom={}'.format(denominator))
    h = [
            [a[0]*a[0]+a[1]*a[1], a[1], 1],
            [b[0]*b[0]+b[1]*b[1], b[1], 1],
            [c[0]*c[0]+c[1]*c[1], c[1], 1]
        ]
    #output('H before mult={}'.format(h))
    h = getMatrixMultiply(h,denominator)
    #output('H after  mult={}'.format(h))
    k = [
            [a[0], a[0]*a[0]+a[1]*a[1], 1],
            [b[0], b[0]*b[0]+b[1]*b[1], 1],
            [c[0], c[0]*c[0]+c[1]*c[1], 1]
        ]
    k = getMatrixMultiply(k,denominator)
    # r = sqrt[(a[0]-h)^2+(a[1]-k)^2]
    return (h,k)#,r)
    
            

def reflected_point(point,around):
    return 2*around[0]-point[0],2*around[1]-point[1]

def arctopoints(center,start,angle,arcerror = 0.1,arcunits=2500):
    'maxerror as a percentage (0.0-1.0) of radius'
    # If an arc has sweep angle a, radius r, then the greatest distance between the chord with the same endpoints and the arc is r*(1-cos(a/2). If you subdivide this arc by putting n equally spaced points along it, then the maximum distance between the arc and the segmented line will be r*(1-cos(a/(2*(n+1)))).

    # So if you want to keep the greatest distance below E, say, then you could put n new points along the arc, with n chosen so that n+1 >= a/(2*acos(1 - E/r))
    r = wxPointUtil.distance(center,start)
    maxerror = max(arcerror/r,arcunits)
    if _user_stacks['Params'][-1].get('debug',None):
        output('maxerror = max(arcerror/r,arcunits) = {}/{},{} = {}'.format(arcerror,r,arcunits,maxerror))
    nmin = int(angle/(2*math.acos(1-maxerror)))+1 # (=nmin+1) # was maxerror/r
    startvector = (start[0] - center[0],start[1] - center[1])
    startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi
    endangledeg = startangledeg + angle
    
    xy = wxPointUtil.toxy(r,(theta+startangledeg)*math.pi/180)
    return [(xy[0]+center[0],xy[1]+center[1]) for theta in itertools.starmap(operator.mul,itertools.izip(xrange(0,nmin+1),itertools.cycle((float(angle)/nmin,))))]


# public class Bezier
# {
    # public PointF P1;   // Begin Point
    # public PointF P2;   // Control Point
    # public PointF P3;   // Control Point
    # public PointF P4;   // End Point

    # // Made these global so I could diagram the top solution
    # public Line L12;
    # public Line L23;
    # public Line L34;

    # public PointF P12;
    # public PointF P23;
    # public PointF P34;

    # public Line L1223;
    # public Line L2334;

    # public PointF P123;
    # public PointF P234;

    # public Line L123234;
    # public PointF P1234;

    # public Bezier(PointF p1, PointF p2, PointF p3, PointF p4)
    # {
        # P1 = p1; P2 = p2; P3 = p3; P4 = p4;
    # }

     # # <summary>
     # # Consider the classic Casteljau diagram
     # # with the bezier points p1, p2, p3, p4 and lines l12, l23, l34
     # # and their midpoint of line l12 being p12 ...
     # # and the line between p12 p23 being L1223
     # # and the midpoint of line L1223 being P1223 ...
     # # </summary>
     # # <param name="lines"></param>
    # def SplitBezier(p1,p2,p3,p4):
        # L12 = new Line(this.P1, this.P2);
        # L23 = new Line(this.P2, this.P3);
        # L34 = new Line(this.P3, this.P4);

        # P12 = L12.MidPoint();
        # P23 = L23.MidPoint();
        # P34 = L34.MidPoint();

        # L1223 = new Line(P12, P23);
        # L2334 = new Line(P23, P34);

        # P123 = L1223.MidPoint();
        # P234 = L2334.MidPoint();

        # L123234 = new Line(P123, P234);

        # P1234 = L123234.MidPoint();

        # # Check if points P1, P1234 and P2 are colinear (enough).
        # # This is very simple-minded algo... there are better...
        # float t1 = (P2.Y - P1.Y) * (P3.X - P2.X);
        # float t2 = (P3.Y - P2.Y) * (P2.X - P1.X);

        # float delta = Math.Abs(t1 - t2);

        # if delta < 0.1; // Hard-coded constant
            # return
        # else:
            # Bezier bz1 = new Bezier(this.P1, P12, P123, P1234);
            # bz1.SplitBezier(lines);

            # Bezier bz2 = new Bezier(P1234, P234, P34, this.P4);
            # bz2.SplitBezier(lines);
        # return;
    # }



def _B(coorArr, i, j, t):
    if j == 0:
        return coorArr[i]
    return _B(coorArr, i, j - 1, t) * (1 - t) + _B(coorArr, i + 1, j - 1, t) * t

def beziertopoints(start,c1,c2,end,steps=5):
    # steps = 30
    # n = random.randint(3, 6) # number of control points
    # coorArrX = []
    # coorArrY = []
    # for k in range(n):
        # x = random.randint(0, imgx - 1)
        # y = random.randint(0, imgy - 1)
        # coorArrX.append(x)
        # coorArrY.append(y)

    (coorArrX,coorArrY) = zip(start,c1,c2,end)
    n = 4 # number of points (start+control+end)
    
    points=[]
    # plot the curve
    numSteps = steps
    for k in range(numSteps):
        t = float(k) / (numSteps - 1)
        x = int(_B(coorArrX, 0, n - 1, t))
        y = int(_B(coorArrY, 0, n - 1, t))
        try:
            points.append((x,y))
        except:
            pass    
    return points

# TTF font winding, inside/outside, etc.

# http://twardoch.github.io/test-fonts/varia/160413-EvenOddTT/
# Also, "For simple glyphs, you should set bit 6 of the first Outline Flag byte to 1 if the unhinted glyph outline has overlapping contours or if variation controls or hinting controls can ever cause any of the contours to overlap. Otherwise this bit should be set to 0."

def IsWindingCW(points):
    # output('finding winding with {} points'.format(len(points)))
    startpoints = iter(points)
    endpoints = itertools.islice(points,1,None)
    result = sum(itertools.starmap(lambda s,e: (e[0] - s[0])*(e[1] + s[1]),itertools.izip(startpoints,endpoints)))
    return (result > 0)
    
    
# from https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule    
# Using Even-Odd rule 

# Tutorial: https://www.wikiwand.com/en/Point_in_polygon (no code or math)

# https://stackoverflow.com/a/47027051 (a conclusion, but not sure if it applies in all cases
# https://groups.google.com/d/msg/comp.fonts/v8jAqZ0uris/tXqbzCZ-4J8J Apple Fonts Guy

def is_point_in_path(x, y, poly): # -> bool:
    """Determine if the point is in the path.

    Args:
      x -- The x coordinates of point.
      y -- The y coordinates of point.
      poly -- a list of tuples [(x, y), (x, y), ...]

    Returns:
      True if the point is in the path.
    """
    num = len(poly)
    i = 0
    j = num - 1
    c = False
    for i in range(num):
        if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                                  (poly[j][1] - poly[i][1])):
            c = not c
        j = i
    return c

# would also be nice to handle projection
# https://www.cis.rit.edu/class/simg782/lectures/lecture_02/lec782_05_02.pdf


# Noto-sans-cjk-jp-regular setfont \u0030 stringtogeom Tmm,216,-5 split swap append newdrawing refresh

# Noto-sans-cjk-jp-regular setfont 250 getunicoderows stringtogeom newdrawing refresh
# 280 getunicoderows stringtogeom newdrawing refresh
# Noto-sans-cjk-jp-regular setfont \u24DE stringtogeom newdrawing refresh
# Noto-sans-cjk-jp-regular setfont \u24C6 stringtogeom newdrawing refresh
def getpolygonholes(polygonlist,debug=False):
    debug=False
    # here we implement a simple algorithm
    # assume "solid right" that is 
    # polygons are supposed to be CW and holes are supposed to be CCW, according to the spec.
    # however, font files are not consistent.
    # what appears to work is to use wn_PnPoly, which requires a CW polygon
    # we determine winding so we can feed either the polygonlist or reversed to wn_PnPoly
    
    windings = [IsWindingCW(polygonlist[i]) for i in range(len(polygonlist))]
    orderedlist = []
    
    # this is just a list that starts with
    # "Polygon" and has "Polygon." thereafter.
    pname = itertools.chain.from_iterable((('Polygon',),(itertools.cycle(('Polygon.',)))))
    polys = []
    holes = []
    # for i in range(len(polygonlist)):
        # if windings[i]:
            # poly = polygonlist[i]
        # else:
            # poly = reversed(polygonlist[i])
            
            
            
    intest = wn_PnPoly
    # intest = point_in_polygon.wn_PnPoly
    childrenbyparent = defaultdict(list) #{-1:[]}

    listlen = len(polygonlist)
    # for p in range(listlen):
        # if IsWindingCW(polygonlist[p]):
            # print('CW  {}'.format(p))
        # else:
            # print('CCW {}'.format(p))
            

    # Keep track of how many polygons the indexed polygon is within.
    incount = [0] * len(polygonlist)
    # would this work? (seems to)
    getcw = lambda i: windings[i] and polygonlist[i] or reversed(polygonlist[i])
    for p in range(listlen):
        for c in range(p+1,listlen):
            # if windings[p]:
                # ptest = polygonlist[p]
            # else:
                # ptest = reversed(polygonlist[p])
            # if windings[c]:
                # ctest = polygonlist[c]
            # else:
                # ctest = reversed(polygonlist[c])

            # print('{} vs {}: cn_PnPoly = {}'.format(c,p,intest(polygonlist[c][0], tuple(polygonlist[p]))))
            # print('{} vs {}: cn_PnPoly = {}'.format(p,c,intest(polygonlist[p][0], tuple(polygonlist[c]))))
            if intest(polygonlist[c][0], getcw(p)) != 0:
                # c is in p
                #print(' {} in {}'.format(polygonlist[c][0], map(str,polygonlist[p])))
                incount[c] += 1
                #childrenbyparent[p].append(c)
                #childrenbyparent[-1].append(p)
            elif intest(polygonlist[p][0], getcw(c)) != 0:
                incount[p] += 1
                #print(' {} in {}'.format(polygonlist[p][0], map(str,polygonlist[c])))
                #childrenbyparent[c].append(p)
                #childrenbyparent[-1].append(c)
            # else:
                # childrenbyparent[-1].append(p)
                # childrenbyparent[-1].append(c)

        # for p,c in childrenbyparent.items():
            # itertools.chain.from_iterable(
            
    pname = itertools.chain.from_iterable((('Polygon',),(itertools.cycle(('Polygon.',)))))
    for i in range(len(polygonlist)):
        if incount[i] % 2 == 0:
            orderedlist.append((pname.next(),i))
    for i in range(len(polygonlist)):
        if incount[i] % 2 == 1:
            orderedlist.append(('Hole',i))
    if debug:
        for i in range(len(polygonlist)):
            output('{}: CW? {}; in: {}'.format(i,windings[i],incount[i]))
    return orderedlist
            
    if debug:
        for i in range(len(polygonlist)):
            output('{}: CW? {}; in: {}'.format(i,windings[i],incount[i]))
        output('brute force: {}'.format(childrenbyparent))
        # Noto-sans-cjk-jp-regular setfont 280 getunicoderows stringtogeom newdrawing refresh
        # Noto-sans-cjk-jp-regular setfont 'a stringtogeom print
        # print('polylist: {}'.format(polygonlist))
        # childrenbyparent.clear()
    # At this point, childrenbyparent is flattened, and now we just make sure
    # all nodes are in the structure.
    toplevelparents = set(range(len(polygonlist)))
    #toplevelparents.discard(p)
    
    for p,clist in childrenbyparent.items():
        for c in clist:
            toplevelparents.discard(c)
    childrenbyparent[-1].extend(toplevelparents)
    if debug:
        output('brute force2: {}'.format(childrenbyparent))

    currentparent = -1
    # #output('# polygons = {}'.format(len(polygonlist)))
    # found = False
    # for inewpoly in range(len(polygonlist)):
        # if debug:
            # output('Checking polygon {}'.format(inewpoly))
        # currentparent = -1
        # while currentparent is not None:
            # found = False
            # ipparent = 0
            # for pparent in childrenbyparent[currentparent]:
                
                # #output('is {} inside #{} ({})'.format(str(polygonlist[inewpoly][0]),pparent,polygonlist[pparent]))
                # #output('is #{} inside #{}?'.format(inewpoly,pparent))
                # #output('(point {} inside {}?)'.format(tuple(polygonlist[inewpoly][0]),map(tuple,polygonlist[pparent])))
                # #output('intest returned {}'.format(intest(polygonlist[inewpoly][0], polygonlist[pparent])))
                # if intest(polygonlist[inewpoly][0], tuple(polygonlist[pparent])) != 0:
                    # # if inewpoly is within the current pparent, we want to continue to dive into
                    # # geometries within the current pparent. We can ignore other geometries outside of
                    # # the current pparent since a geometry can be within only one.
                    # if debug:
                        # print('inewpoly {} in {}'.format(inewpoly,pparent))
                    # #output('yes')
                    # # inewpoly is descendent of pparent, keep looking at further children 
                    # currentparent = pparent
                    # #output('ancestor of {} is {}'.format(inewpoly,currentparent))
                    # found = True
                    # break
            # if not found:
                # break
        # if currentparent is not None:
            # if debug:
                # print('adding current {} to inewpoly {}'.format(currentparent,inewpoly))
            # childrenbyparent[currentparent].append(inewpoly)
    # # Now, if inewpoly is not within any other geometries, we want to check to see
    # # which geometries might be within inewpoly. Only need to check the children of currentparent
    # if not found:
        # for pparent in list(childrenbyparent[currentparent]): # make a copy of the list in case we modify
            # if pparent == inewpoly:
                # continue
            # if intest(polygonlist[pparent][0], polygonlist[inewpoly]) != 0:
                # if debug:
                    # print('point {} in inewpoly {}'.format(pparent,inewpoly))
                # childrenbyparent[currentparent].remove(pparent)
                # childrenbyparent[inewpoly].append(pparent)
    # #output('childrenbyparent before: {}'.format(childrenbyparent))        
    
    # # Now all the children of -1 are polygons
    # # their children are holes

    # # Now go through the tree and convert grand children into top-level parents.
    # currentparent = -1
    # orderedlist = []
    
    # Now go through the tree and output with dependencies in order and with poly/hole identifier 
    # go through all keys and move grand children to top level
    # output('length of geom list = {}'.format(len(polygonlist)))
    countbreak = 0
    currentparentlist = True
    while currentparentlist and countbreak < 1000:
        currentparentlist = list(childrenbyparent[currentparent])
        for parent in currentparentlist:
            currentgrandchildren = []
            for child in list(childrenbyparent[parent]):
                childschildren = list(childrenbyparent[child])
                
                currentgrandchildren.extend(childschildren)
                childrenbyparent.pop(child, None) # del childrenbyparent[gc]
            childrenbyparent[-1].extend(list(currentgrandchildren))
            currentparentlist = currentgrandchildren
            countbreak += 1
        # output('Grandchildren: {}'.format(grandchildren))        
        # for grandchild in grandchildren:
            # del childrenbyparent[grandchild]
        # childrenbyparent[-1].extend(list(grandchildren))
    if debug:
        output('childrenbyparent after: {}'.format(childrenbyparent))        

    # : rangeline "" getunicoderange 3 pull swap concat \n concat ; : nextrange ""  1 pull 2 pull 1 pick + int delist swap 1 pick list 1 pick append stack ; : r "Execute one unicode range into elements." nextrange rangeline ; clear -149 int 150 int "" r r r r r r r r r r r r r r r r r r r r  print stringtogeom Thickness,1,TTranslate,0,224000,TScale,1000,1000 split swap append newdrawing refresh
    # parentwinding = [IsWindingCW(polygonlist[p]) for p in childrenbyparent[-1]]
    # childwinding = [map(lambda c: IsWindingCW(polygonlist[c]),clist) for clist in [childrenbyparent[p] for p in childrenbyparent[-1]]]
    # allchild = list(itertools.chain.from_iterable(childwinding))
    # if (allchild and not all(allchild)) or any(parentwinding):
        # output('Warning: \nParent winding {}\nChilds winding {}'.format(parentwinding,childwinding))
    # now we have two levels. Parents are polygons and children are holes.
    # iterable of the word 'Polygon' followed by 'Polygon.'

    pname = itertools.chain.from_iterable((('Polygon',),(itertools.cycle(('Polygon.',)))))
    for parent in childrenbyparent[-1]:
        #polygonlist[parent].insert(0,'Polygon')
        orderedlist.append((pname.next(),parent))
        #orderedlist.append(polygonlist[parent])
        #polygonlist[parent])
        for child in childrenbyparent[parent]:
            orderedlist.append(('Hole',child))
            #polygonlist[child].insert(0,'Hole')
            #orderedlist.append(polygonlist[child])

    return orderedlist
        
            
            
            
            
# wn_PnPoly(polygonlist[c][0], tuple(polygonlist[p]))            
        # almost:
        # if IsWindingCW(polygonlist[i]):
            # polys.append(i)
        # else:
            # holes.append(i)
    for p in polys:
        orderedlist.append((pname.next(),p))
    for p in holes:
        orderedlist.append(('Hole',p))
    if holes and not polys:
        #output('holes without polygons')
        del orderedlist[:] # orderedlist.clear()
        pname = itertools.chain.from_iterable((('Polygon',),(itertools.cycle(('Polygon.',)))))
        for p in range(len(polygonlist)):
            orderedlist.append((pname.next(),p))
    return orderedlist
def getpolygonholes_july(polygonlist,debug=False):
    # here we implement a simple algorithm
    # assume "solid right" that is 
    # polygons are CW and holes are CCW
    orderedlist = []
    
    # this is just a list that starts with
    # "Polygon" and has "Polygon." thereafter.
    pname = itertools.chain.from_iterable((('Polygon',),(itertools.cycle(('Polygon.',)))))
    polys = []
    holes = []
    for i in range(len(polygonlist)):
        if IsWindingCW(polygonlist[i]):
            poly = polygonlist[i]
        else:
            poly = reversed(polygonlist[i])
# wn_PnPoly(polygonlist[c][0], tuple(polygonlist[p]))            
        # almost:
        # if IsWindingCW(polygonlist[i]):
            # polys.append(i)
        # else:
            # holes.append(i)
    for p in polys:
        orderedlist.append((pname.next(),p))
    for p in holes:
        orderedlist.append(('Hole',p))
    if holes and not polys:
        #output('holes without polygons')
        del orderedlist[:] # orderedlist.clear()
        pname = itertools.chain.from_iterable((('Polygon',),(itertools.cycle(('Polygon.',)))))
        for p in range(len(polygonlist)):
            orderedlist.append((pname.next(),p))
    return orderedlist
    # 280 getunicoderows stringtogeom newdrawing refresh
def getpolygonholes_june(polygonlist,debug=False):
    #debug = True
    # childrenbyparent = {iparent1: [children]} # list of children indexed by parentindex. Index of -1 is list of top level nodes.
    # using a Depth First Traversal, Preorder (Root, Children)
    # find the first polygon that contains a random point of the current polygon
    # childrenbyparent[firstfound].append(ipolygon) 
    intest = wn_PnPoly
    # intest = point_in_polygon.wn_PnPoly
    childrenbyparent = defaultdict(list) #{-1:[]}
    if debug:
        listlen = len(polygonlist)
        for p in range(listlen):
            if IsWindingCW(polygonlist[p]):
                print('CW  {}'.format(p))
            else:
                print('CCW {}'.format(p))
        for p in range(listlen):
            for c in range(p+1,listlen):
                print('{} vs {}: cn_PnPoly = {}'.format(c,p,intest(polygonlist[c][0], tuple(polygonlist[p]))))
                print('{} vs {}: cn_PnPoly = {}'.format(p,c,intest(polygonlist[p][0], tuple(polygonlist[c]))))
                if intest(polygonlist[c][0], polygonlist[p]) != 0:
                    # c is in p
                    print(' {} in {}'.format(polygonlist[c][0], map(str,polygonlist[p])))
                    childrenbyparent[p].append(c)
                elif intest(polygonlist[p][0], polygonlist[c]) != 0:
                    print(' {} in {}'.format(polygonlist[p][0], map(str,polygonlist[c])))
                    childrenbyparent[c].append(p)

        print('brute force: {}'.format(childrenbyparent))
        print('polylist: {}'.format(polygonlist))
        childrenbyparent.clear()
    currentparent = -1
    #output('# polygons = {}'.format(len(polygonlist)))
    found = False
    for inewpoly in range(len(polygonlist)):
        if debug:
            output('Checking polygon {}'.format(inewpoly))
        currentparent = -1
        while currentparent is not None:
            found = False
            ipparent = 0
            for pparent in childrenbyparent[currentparent]:
                
                #output('is {} inside #{} ({})'.format(str(polygonlist[inewpoly][0]),pparent,polygonlist[pparent]))
                #output('is #{} inside #{}?'.format(inewpoly,pparent))
                #output('(point {} inside {}?)'.format(tuple(polygonlist[inewpoly][0]),map(tuple,polygonlist[pparent])))
                #output('intest returned {}'.format(intest(polygonlist[inewpoly][0], polygonlist[pparent])))
                if intest(polygonlist[inewpoly][0], tuple(polygonlist[pparent])) != 0:
                    # if inewpoly is within the current pparent, we want to continue to dive into
                    # geometries within the current pparent. We can ignore other geometries outside of
                    # the current pparent since a geometry can be within only one.
                    if debug:
                        print('inewpoly {} in {}'.format(inewpoly,pparent))
                    #output('yes')
                    # inewpoly is descendent of pparent, keep looking at further children 
                    currentparent = pparent
                    #output('ancestor of {} is {}'.format(inewpoly,currentparent))
                    found = True
                    break
            if not found:
                break
        if currentparent is not None:
            if debug:
                print('adding current {} to inewpoly {}'.format(currentparent,inewpoly))
            childrenbyparent[currentparent].append(inewpoly)
    # Now, if inewpoly is not within any other geometries, we want to check to see
    # which geometries might be within inewpoly. Only need to check the children of currentparent
    if not found:
        for pparent in list(childrenbyparent[currentparent]): # make a copy of the list in case we modify
            if pparent == inewpoly:
                continue
            if intest(polygonlist[pparent][0], polygonlist[inewpoly]) != 0:
                if debug:
                    print('point {} in inewpoly {}'.format(pparent,inewpoly))
                childrenbyparent[currentparent].remove(pparent)
                childrenbyparent[inewpoly].append(pparent)
    #output('childrenbyparent before: {}'.format(childrenbyparent))        
    
    # Now all the children of -1 are polygons
    # their children are holes

    # Now go through the tree and convert grand children into top-level parents.
    currentparent = -1
    orderedlist = []
    
    # Now go through the tree and output with dependencies in order and with poly/hole identifier 
    # go through all keys and move grand children to top level
    # output('length of geom list = {}'.format(len(polygonlist)))
    countbreak = 0
    currentparentlist = True
    while currentparentlist and countbreak < 1000:
        currentparentlist = list(childrenbyparent[currentparent])
        for parent in currentparentlist:
            currentgrandchildren = []
            for child in list(childrenbyparent[parent]):
                childschildren = list(childrenbyparent[child])
                
                currentgrandchildren.extend(childschildren)
                childrenbyparent.pop(child, None) # del childrenbyparent[gc]
            childrenbyparent[-1].extend(list(currentgrandchildren))
            currentparentlist = currentgrandchildren
            countbreak += 1
        # output('Grandchildren: {}'.format(grandchildren))        
        # for grandchild in grandchildren:
            # del childrenbyparent[grandchild]
        # childrenbyparent[-1].extend(list(grandchildren))
    if debug:
        output('childrenbyparent after: {}'.format(childrenbyparent))        

    # : rangeline "" getunicoderange 3 pull swap concat \n concat ; : nextrange ""  1 pull 2 pull 1 pick + int delist swap 1 pick list 1 pick append stack ; : r "Execute one unicode range into elements." nextrange rangeline ; clear -149 int 150 int "" r r r r r r r r r r r r r r r r r r r r  print stringtogeom Thickness,1,TTranslate,0,224000,TScale,1000,1000 split swap append newdrawing refresh
    parentwinding = [IsWindingCW(polygonlist[p]) for p in childrenbyparent[-1]]
    childwinding = [map(lambda c: IsWindingCW(polygonlist[c]),clist) for clist in [childrenbyparent[p] for p in childrenbyparent[-1]]]
    allchild = list(itertools.chain.from_iterable(childwinding))
    # if (allchild and not all(allchild)) or any(parentwinding):
        # output('Warning: \nParent winding {}\nChilds winding {}'.format(parentwinding,childwinding))
    # now we have two levels. Parents are polygons and children are holes.
    # iterable of the word 'Polygon' followed by 'Polygon.'
    pname = itertools.chain.from_iterable((('Polygon',),(itertools.cycle(('Polygon.',)))))
    for parent in childrenbyparent[-1]:
        #polygonlist[parent].insert(0,'Polygon')
        orderedlist.append((pname.next(),parent))
        #orderedlist.append(polygonlist[parent])
        #polygonlist[parent])
        for child in childrenbyparent[parent]:
            orderedlist.append(('Hole',child))
            #polygonlist[child].insert(0,'Hole')
            #orderedlist.append(polygonlist[child])

    return orderedlist

# determine the ordering of non-intersecting polygons, then assign Hole to the appropriate ones
# return the indexex of holes
# This is the even/odd rule applied to non-intersecting polygons.
def order_polygons_try(self,polygonlist):
    # Simple structure to indicate hierarchy.
    # childrenbyparent = {index:[child indexes inside index polygon]
    # parent = {childindex: parentindex}
    # childless = [index of polygons without children]
    for i,p in enumerate(polygonlist):
        insideany = False
        for nki,nokids in enumerate(childless):
            if False: # random_point_on_p is inside nokids:
                parent[p] = nokids
                childless[nki] = i
                insideany = True
                # childless.remove(nokids)
                # childless.append(i)
                break
        if insideany:
            continue
        # now do a depth-first
        # GAH, unfinished. Don't know if should start depth-first or breadth-first search
        # after ordered, parentless are polygons, holes are the immediate childlren, then grandchildren are polygons, etc.
        
class matrixTransform2d:
    _currentTransformation = None
    _dimensions = None
    def __init__(self,dimensions=3):
        self._dimensions = dimensions
        self._currentTransformation = [[0] * self._dimensions for row in xrange(self._dimensions)]
        for i in xrange(self._dimensions):
            self._currentTransformation[i][i] = 1.0
        # flip around the x axis to compensate for KiCAD's reversed y coordinates
        #self._currentTransformation[1][1] = -1.0 # flip on x axis  ((1,0,0),(0,-1,0),(0,0,1))
        #self._currentTransformation[0][0] = -1.0 # flip on y axis ((-1,0,0),(0,1,0),(0,0,1))
         # operator.setitem(a, b, c) # Set the value of a at index b to c.
    def zero(self):
        for i in xrange(self._dimensions):
            for j in xrange(self._dimensions):
                self._currentTransformation[i][j] = 0.0
    def identity(self):
        self.zero()
        for i in xrange(self._dimensions):
            self._currentTransformation[i][i] = 1.0
    def copyArray(self):
        return [[element for element in row] for row in self._currentTransformation]
    def copyTransform(self):
        m=matrixTransform2d()
        m._currentTransformation = self.copyArray()
        return m
    def multiply(self, G):
        result = []
        for j in range(len(G)): #this loops through a column of F & rows of G
            total = list(range(len(G[0])))
            for i in range(len(G[0])): #this loops through columns of the matrix
                total[i] += self._currentTransformation[i][j] * G[j][i]
            result.append(total)
        return result
    def multiplyInPlace(self, otherMatrix, pre=False):
        'If pre, self = self * other; else self = other * self'
        # create a temporary copy to hold the source numbers
        if pre:
            secondMatrix = otherMatrix
            firstMatrix = self.copyArray()
        else:
            firstMatrix = otherMatrix
            secondMatrix = self.copyArray()
        resultMatrix = self._currentTransformation
        # secondMatrix=([16,17,18],[19,110,111],[112,113,114])
        # firstMatrix = ([6,7,8],[9,10,11],[12,13,14])
        # the follwoing would be used if the result wasn't the same size as the first matrix
        # resultMatrix = [[0] * len(firstMatrix[0]) for row in xrange(len(secondMatrix))]
        
        #result row, column is the row of the first and the column of the second. Mult then summed.
        # for col in xrange(len(secondMatrix[0])):
            # for row in xrange(len(firstMatrix)):
                # print(': ',list(
                    # itertools.izip_longest(
                        # iter(firstMatrix[row]),
                        # itertools.imap(lambda x: x[col],secondMatrix),
                        # fillvalue=1)       # fill value is useful when firstMatrix is a x/y point, but if this is hte case, point must be a list of lists (well, of one list). And then, the len(firstMatrix[0]) wouldn't be correct for col.  
                        # ))
        # use iterators and place the results into the existing resultMatrix
        for col in xrange(len(secondMatrix[0])):
            for row in xrange(len(firstMatrix)):
                resultMatrix[row][col] = \
                    sum(itertools.starmap(operator.mul,
                    itertools.izip_longest(
                        iter(firstMatrix[row]),
                        itertools.imap(lambda x: x[col],secondMatrix),
                        fillvalue=1)       # fill value is useful when firstMatrix is a x/y point, but if this is hte case, point must be a list of lists (well, of one list). And then, the len(firstMatrix[0]) wouldn't be correct for col.  
                        ))
    def multiplyInPlace_old(self, secondMatrix):
        # create a temporary copy to hold the source numbers
        firstMatrix = self.copy()
        resultMatrix = self._currentTransformation
        # firstMatrix=([16,17,18],[19,110,111],[112,113,114])
        # secondMatrix = ([6,7,8],[9,10,11],[12,13,14])
        # the follwoing would be used if the result wasn't the same size as the first matrix
        # resultMatrix = [[0] * len(secondMatrix[0]) for row in xrange(len(firstMatrix))]
        
        # use iterators and place the results into the existing resultMatrix
        for col in xrange(len(secondMatrix[0])):
            for row in xrange(len(firstMatrix)):
                resultMatrix[row][col] = \
                    sum(itertools.starmap(operator.mul,
                    itertools.izip_longest(
                        iter(self._currentTransformation[row]),
                        itertools.imap(lambda x: x[col],secondMatrix),
                        fillvalue=1) # fill value is useful when secondMatrix is a x/y point, but if this is hte case, point must be a list of lists (well, of one list). And then, the len(secondMatrix[0]) wouldn't be correct for col.
                        ))
    def xmultiplyInPlace(self, firstMatrix):
        # create a temporary copy to hold the source numbers
        secondMatrix = self.copy()
        resultMatrix = self._currentTransformation
        # firstMatrix=([16,17,18],[19,110,111],[112,113,114])
        # secondMatrix = ([6,7,8],[9,10,11],[12,13,14])
        # the follwoing would be used if the result wasn't the same size as the first matrix
        # resultMatrix = [[0] * len(secondMatrix[0]) for row in xrange(len(firstMatrix))]
        
        # use iterators and place the results into the existing resultMatrix
        for col in xrange(len(secondMatrix[0])):
            for row in xrange(len(firstMatrix)):
                print(list(
                itertools.izip_longest(
                                iter(self._currentTransformation[row]),
                                itertools.imap(lambda x: x[col],secondMatrix),
                                fillvalue=1)
                ))
        for col in xrange(len(secondMatrix[0])):
            for row in xrange(len(firstMatrix)):
                resultMatrix[row][col] = \
                    sum(itertools.starmap(operator.mul,
                    itertools.izip_longest(
                        iter(self._currentTransformation[row]),
                        itertools.imap(lambda x: x[col],secondMatrix),
                        fillvalue=1) # fill value is useful when secondMatrix is a x/y point, but if this is hte case, point must be a list of lists (well, of one list). And then, the len(secondMatrix[0]) wouldn't be correct for col.
                        ))

    # http://graphics.cs.cmu.edu/nsp/course/15-462/Spring04/slides/04-transform.pdf
    # This site seems to say that transposing may be necessary (pg 13-14)
    # And https://www.math.hmc.edu/~dk/math40/math40-lect07.pdf (page 4) says (AB)T = BT AT
    # Suppose we have the following transformations applied in this order (I=identity = IT):
    # Dp , CDp, BCDp, ABCDp 
    # After the first transformation,
    # Dp = Dp
    # (CD)p = 
   
    def transform(self,point):
        m=self._currentTransformation
        p=point
        # return [m[0][0] * p [0] + m[0][1] * p[1] + m[0][2],  m[1][0] * p [1] + m[1][1] * p[1] + m[1][2]]
        return [m[0][0] * p [0] + m[0][1] * p[1] + m[0][2],  m[1][0] * p[0] + m[1][1] * p[1] + m[1][2]]
                    
    def translate(self,x,y,origin=None,pre=False):
        # x,y = self.transform((x,y))
        # zero = self.transform((0,0))
        #x,y = self.transform((x,y))
        if origin is None:
            zero = (0,0)
        else:
            zero = self.transform(origin)
        self.multiplyInPlace(((1,0,x-zero[0]),(0,1,y-zero[1]),(0,0,1)),pre=pre)
        #output("translated to {}, {}".format(x,y))
        #output("Zero is now {}, {}".format(*self.transform((0,0))))
    def scale(self,xyfactors,origin=None,pre=False): # scale includes reflection ((-1,1) is around yaxis; (1,-1) is around xaxis) 
        if origin:
            self.translate(-origin[0],-origin[1])
        # output("scaled by {}, {}".format(*xyfactors))
        self.multiplyInPlace(((xyfactors[0],0,0),(0,xyfactors[1],0),(0,0,1)),pre=pre)
        if origin:
            self.translate(*origin)
    def rotate(self,degrees,origin=None,pre=False):
        if origin:
            self.translate(-origin[0],-origin[1])
        r = math.radians(degrees)
        s=math.sin(r)
        c=math.cos(r)
        self.multiplyInPlace(((c,-s,0),(s,c,0),(0,0,1)),pre=pre)
        if origin:
            self.translate(*origin)
    def shear(self,xyfactors,origin=None,pre=False): # m[0][1] = xyfactors[0]; m[1][0] = xyfactors[1] 
        if origin:
            self.translate(-origin[0],-origin[1])
        self.multiplyInPlace(((1,xyfactors[0],0),(xyfactors[1],1,0),(0,0,1)),pre=pre)
        if origin:
            self.translate(*origin)

import struct

def unichar(i):
    try:
        return unichr(i)
    except ValueError:
        return struct.pack('i', i).decode('utf-32')

def f_stringseparator(p_string, separator=',', n=20):
    if not isinstance(p_string, basestring):    # str or unicode
        p_string = str(p_string)                # convert only non-strings
    return separator.join(p_string[i:i+n] for i in range(0, len(p_string), n))
    #for CJK font, 4.5 minutes to generate geoms, 2.5 minutes to create polygons.
class commands:
    classinstance = None
    
    # def getglyph(self,listofcodes)
        
    def getunicoderows(self,*c):
        """Font [STARTANDCOUNT] STARTANDCOUNT is a list of numbers start,count. Returns count number of characters start index of all unicode characters from the active font."""
        ustr = u''.join([unichar(ord) for ord in sorted(fonts.getfont()._unicode_codepoint_lookup.keys())])#.decode('unicode-escape')
        return f_stringseparator(ustr,separator='\n',n=int(c[0][0]))

    def getunicoderange(self,*c):
        """Font [STARTANDCOUNT] STARTANDCOUNT is a list of numbers start,count. Returns count number of characters start index of all unicode characters from the active font."""
        ustr = u''.join([unichar(ord) for ord in sorted(fonts.getfont()._unicode_codepoint_lookup.keys())])#.decode('unicode-escape')
        # output("getur={}".format(c))
        start,count = int(c[0][0][0]),int(c[0][0][1])
        # output('start={} count={}'.format(start,count))
        if count == 0:
            return ustr[start:]
        else:
            return ustr[start:start+count]
    
    def NEWNET(self,netname):
        """Draw [NETNAME] Create a new net with name netname."""

        board = getBoard() 

        # First create a new NETINFO_ITEM instance.
        netinfo = pcbnew.NETINFO_ITEM(board, netname)

        # Add this net to 'board', this will assign a 'net code' to your net.
        board.AppendNet(netinfo)

        # return the net code
        return netinfo.GetNet()
        
        #Learn the net code:
        #print(netinfo.GetNet())
        #Assign net to a certain track:
        #track.SetNetCode(netinfo.GetNet())
    
    def getpads(self,items):
        """Elements [MODULES] Get pads of each module in MODULES."""
        items = items[0]
        p = []
        for i in items:
            p.extend(list(i.Pads()))
        return p
    
    def select(self,items):
        'Action [OBJECTLIST] Select the objects'
        filter(lambda x: x.SetSelected(), items[0])
    
    def deselect(self,items):
        'Action [OBJECTLIST] Deselect the objects'
        filter(lambda x: x.ClearSelected(), items[0])
    
    def pads(self,empty):
        """Elements Get all pads"""
        p=[]
        for m in getBoard().GetModules():
            p.extend(list(m.Pads()))
        return p
    
    def AREAS(self,empty):
        """Elements,Area Return all Areas of the board (includes Zones and Keepouts). zones,keepouts"""
        b = getBoard()
        return [b.GetArea(i) for i in range(b.GetAreaCount())]
        
    def ZONES(self,ignore):
        """Elements,Area Return all non-keepout areas of the board. areas,keepouts"""
        b = getBoard()
        return filter(lambda c: not c.GetIsKeepout(),[b.GetArea(i) for i in range(b.GetAreaCount())])

    # Example: clear toptextobj selected copy GetThickness call list swap topoints pairwise F.SilkS tosegments copy 2 pick SetWidth callargs pop F.Cu tocopper
    # : texttosegments "Draw [TEXTOBJLIST LAYER] Copies text objects in TEXTOBJLIST to LAYER." swap copy GetThickness call list swap topoints pairwise swap tosegments copy 2 pick SetWidth callargs pop ;
    
    
    # : texttosegments "Draw [TEXTOBJLIST LAYER] Copies text objects in TEXTOBJLIST to LAYER." swap copy GetThickness call list swap topoints pairwise 2 pick tosegments copy 2 pick SetWidth callargs pop swap pop swap pop ;
    
    # Usage: clear toptextobj selected Dwgs.User texttosegments F.Cu tocopper
    def TOPOINTS(self,itemlist):
        """Draw,Geometry [EDA_TEXTLIST] a list of EDA_TEXT items, which are converted to point pairs suitable for TODRAWSEGMENTS"""
        #print('itemlist: ',itemlist)
        # if not (hasattr(itemlist, '__getitem__') or hasattr(itemlist, '__iter__')):
            # #print('making into list')
            # itemlist = [itemlist]
        strokes = []
        #for items in itemlist:
        for t in itemlist[0]:
        
            strokes.append(pcbnew.wxPoint_Vector(0))
            t.TransformTextShapeToSegmentList(strokes[-1])
            # orient TEXTE_MODULE strokes to the board
            # TEXTE_MODULE: oddly, the combination of draw rotation and 
            # orientation is what's needed to determine the correct
            # segments transformation only for TEXTE_MODULE object.

            # orientation is specified ccw (leftward) from positive x-axis
            if isinstance(t,pcbnew.TEXTE_MODULE):
                orientation = t.GetDrawRotation()\
                             -t.GetTextAngle() 
                              
                #print(t.GetText(), orientation)
                strokes[-1] = self.get_rotated_vector(strokes[-1],t.GetCenter(),orientation)
        return strokes
    
    def pairwise(self,iterable):
        "Conversion [LISTOFLISTS] [s] -> [[s0, s1], [s2, s3], [s4, s5], ...]"
        #list(map(list, zip(a, b)))

        valuelist = []
        #print('iterable: ',iterable)
        for item in iterable[0]:
            a = iter(item)
            valuelist.append(list(zip(a, a)))
        return valuelist
    
    def KEEPOUTS(self,empty):
        """Elements,Area Return all Keepout Areas of the board. areas,zones"""
        b = getBoard()
        return filter(lambda c: c.GetIsKeepout(),[b.GetArea(i) for i in range(b.GetAreaCount())])
    
    def AREACORNERS(self,arealist):
        """Geometry,Area [AREALIST] Get AREALIST corners."""
        b=getBoard()
        areacorners = [[a.GetCornerPosition(i) 
            for i in range(a.GetNumCorners())] 
                for a in arealist[0]]
        return areacorners

    def toggleselect(self,objectlist):
        """Geometry,Area [OBJECTLIST] Toggle selection of each object in OBJECTLIST."""
        for i in objectlist[0]:
            if i.IsSelected():
                i.ClearSelected()
            else:
                i.SetSelected()


    # Test:
    # "m 81.38357,74.230848 5.612659,1.870887 5.211757,3.474503 2.138156,2.138157 10.958048,-6.1472 0.53454,5.078121 -1.06908,4.009044 -2.80633,4.276312 -2.539056,1.603616 1.202716,4.276312 9.48806,-2.939963 13.36348,8.686253 -8.95353,-0.4009 -2.13815,5.34539 -5.21176,-2.67269 -4.67722,4.54358 -2.40542,-3.0736 -4.009046,6.94901 -3.741775,4.27631 -4.142676,2.53906 1.870887,3.34087 v 3.34087 l -4.409948,2.53906 h -2.806329 l -2.80633,-0.53454 -0.267271,-2.00452 1.469982,-1.60362 0.668176,-0.4009 -0.53454,-1.73726 -4.142676,0.53454 -4.677217,-0.93544 -3.34087,-0.66817 -1.336347,-0.13364 -2.405428,3.87541 -1.469982,1.33635 -1.603616,0.66817 -5.479026,-0.66817 -2.405425,-2.80633 -0.133636,-1.60362 3.207235,-3.34087 1.870887,-2.53906 -2.80633,-2.93996 -2.672696,-4.40995 -0.668174,-2.40543 -4.409945,5.47903 -3.207234,-5.34539 -5.078121,2.13815 -3.474506,-6.14719 -8.285356,0.26726 13.229844,-8.418985 10.022607,4.81085 0.400905,-5.34539 -3.741775,-2.138156 -2.405425,-3.474503 -0.668173,-3.073601 v -7.884451 l 13.363474,5.078121 3.608139,-2.939965 5.211757,-2.271789 3.875408,-1.33635 2.138156,0.133636 3.207234,-3.474503 4.677217,-2.939965 2.405425,-0.668174 z" 1 mm fromsvg drawsegments
    # https://www.w3.org/TR/SVG11/paths.html#PathDataGeneralInformation

    # "M172 1745q17 67 70 67q75 0 75 -65q0 -24 -6 -48l-65 -263q-18 -70 -74 -70q-72 0 -72 68q0 22 10 63z"
    
    # need a function to output  
    # either "geoms" or "pointlistoflists" and
    # either "simplified" or "accurate" (maybe accuracy/error as input where 0=simplified?)
    def fromsvgcontours(self,svgdpath,debug=False,simplified=0):
        """Geometry,Conversion [PATH_D_ATTRIBUTE] Converts SVG path element "d attribute"
            derived from TTF contours to a list geoms suitable for the newdrawing command. 
            We only have to consider M, L, and Q. newdrawing,"""
        return svgutil.fromsvgcontours(svgdpath,debug=debug,simplified=simplified)
        
    def fromsvg(self,inputs):
        """Geometry,Conversion [PATH_D_ATTRIBUTE SCALE] Converts SVG path element "d attribute"
            to a list geoms suitable for the newdrawing command. Applies SCALE
            to all coordinates. newdrawing,"""
            

        #print(path)
        transform = matrixTransform2d()
        svgdpath = inputs[0]
        # if isinstance(inputs[1],basestring):
            # inputnumbers = split(inputs[1])
        # else:
            # inputnumbers = inputs[1]
        
        scale = float(inputs[1])
        geoms = ['Group']
        tokenized = svgutil._tokenize_path(svgdpath)
        command = None
        position = None
        
        points = [[0.0,0.0],[0.0,0.0],[0.0,0.0],[0.0,0.0]]
        initialposition = None
        #token = next(tokenized)
        for token in tokenized:
            if token in "mlhvcsqtaMLHVCSQTA":
                previouscommand = command
                command = token
                currenttoken = next(tokenized)
            else:
                currenttoken = token
            #output('token={}; currenttoken={}'.format(token,currenttoken))
            
            if token in 'zZ':
                if initialposition[0] != position[0] or initialposition[1] != position[1]:
                   
                    geoms.append(['Line',transform.transform(position),transform.transform(initialposition)])
                continue
            elif command == 'm':
                if geoms[-1] != 'Group':
                    geoms.append('Group')
                # "If a relative moveto (m) appears as the first element of the path, then it is treated as a pair of absolute coordinates. In this case, subsequent pairs of coordinates are treated as relative even though the initial moveto is interpreted as an absolute moveto."
                if position is None:
                    position = [0.0,0.0]
                position[0] += float(currenttoken)      * scale
                position[1] += float(next(tokenized))  * scale
                initialposition = list(position)
                command = 'l'
            elif command == 'M':
                if geoms[-1] != 'Group':
                    geoms.append('Group')
            # "M633 1437q0 83 78 83h290q86 0 86 -78q0 -72 -88 -72h-208v-72q216 0 366 -151q159 -160 159 -389t-204 -405q-137 -118 -321 -118v-134q0 -101 -91 -101h-282q-89 0 -89 73q0 76 90 76h214v86q-217 0 -373 156q-160 160 -160 361q0 228 120 355q184 195 413 195v135z M633 1147q-132 0 -245 -88q-134 -104 -134 -293q0 -171 128 -284q102 -90 251 -90v755zM792 1147v-755q164 0 263 108q110 120 110 277q0 164 -134 282q-100 88 -239 88z" 0.02 mm fromsvg newdrawing refresh
            # "M633 1437q0 83 78 83" 0.02 mm fromsvg newdrawing refresh
                if position is None:
                    position = [0.0,0.0]
                #output('currenttoken={}'.format(currenttoken))
                position[0] = float(currenttoken)       * scale
                position[1] = float(next(tokenized))   * scale
                initialposition = list(position)
                command = 'L'
            elif command == 'l':
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[0] += float(currenttoken)      * scale
                position[1] += float(next(tokenized))  * scale
                geoms.append(['Line',transform.transform(points[0]),transform.transform(position)])
            elif command == 'L':
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[0] = float(currenttoken)       * scale
                position[1] = float(next(tokenized))   * scale
                geoms.append(['Line',transform.transform(points[0]),transform.transform(position)])
            elif command == 'h':
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[0] += float(currenttoken)      * scale
                geoms.append(['Line',transform.transform(points[0]),transform.transform(position)])
            elif command == 'H':
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[0] = float(currenttoken)       * scale
                geoms.append(['Line',transform.transform(points[0]),transform.transform(position)])
            elif command == 'v':
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[1] += float(currenttoken)      * scale
                geoms.append(['Line',transform.transform(points[0]),transform.transform(position)])
            elif command == 'V':
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[1] = float(currenttoken)       * scale
                geoms.append(['Line',transform.transform(points[0]),transform.transform(position)])
            elif command == 'c':
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[1][0] = points[0][0]+float(currenttoken)       * scale 
                points[1][1] = points[0][1]+float(next(tokenized))   * scale
                points[2][0] = points[0][0]+float(next(tokenized))       * scale 
                points[2][1] = points[0][1]+float(next(tokenized))   * scale
                position[0] = points[0][0]+float(next(tokenized))    * scale
                position[1] = points[0][1]+float(next(tokenized))    * scale
                geoms.append(['Bezier',transform.transform(points[0]),transform.transform(points[1]),transform.transform(points[2]),transform.transform(position)])
            elif command == 'C':
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[1][0] = float(currenttoken)       * scale 
                points[1][1] = float(next(tokenized))   * scale
                points[2][0] = float(next(tokenized))       * scale 
                points[2][1] = float(next(tokenized))   * scale
                position[0] = float(next(tokenized))    * scale
                position[1] = float(next(tokenized))    * scale
                geoms.append(['Bezier',transform.transform(points[0]),transform.transform(points[1]),transform.transform(points[2]),transform.transform(position)])
            elif command == 's':
                # Draws a cubic Bezier curve from the current point to (x,y). The first control point is assumed to be the reflection of the second control point on the previous command relative to the current point. (If there is no previous command or if the previous command was not an C, c, S or s, assume the first control point is coincident with the current point.) (x2,y2) is the second control point (i.e., the control point at the end of the curve). S (uppercase) indicates that absolute coordinates will follow; s (lowercase) indicates that relative coordinates will follow. Multiple sets of coordinates may be specified to draw a polybezier. At the end of the command, the new current point becomes the final (x,y) coordinate pair used in the polybezier.
                if previouscommand in "cCsS":
                    points[1] = list(reflected_point(points[2],position))
                else:
                    points[1] = list(position)
                    # control point 
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[2][0] = points[0][0]+float(currenttoken)    * scale
                points[2][1] = points[0][1]+float(next(tokenized))    * scale                    
                position[0] = points[0][0]+float(next(tokenized))    * scale
                position[1] = points[0][1]+float(next(tokenized))    * scale                    
                geoms.append(['Bezier',transform.transform(points[0]),transform.transform(points[1]),transform.transform(points[2]),transform.transform(position)])
                
            elif command == 'S':
                if previouscommand in "cCsS":
                    points[1] = list(reflected_point(points[2],position))
                else:
                    points[1] = list(position)
                    # control point 
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[2][0] = float(currenttoken)    * scale
                points[2][1] = float(next(tokenized))    * scale                    
                position[0] = float(next(tokenized))    * scale
                position[1] = float(next(tokenized))    * scale                    
                geoms.append(['Bezier',transform.transform(points[0]),transform.transform(points[1]),transform.transform(points[2]),transform.transform(position)])
            elif command == 'q':
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[1][0] = points[0][0]+float(currenttoken)       * scale 
                points[1][1] = points[0][1]+float(next(tokenized))   * scale
                position[0] = points[0][0]+float(next(tokenized))    * scale
                position[1] = points[0][1]+float(next(tokenized))    * scale
                geoms.append(['Bezier',list(itertools.imap(transform.transform,svgutil.beziercubic(points[0],points[1],position)))])
            elif command == 'Q':
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[1][0] = float(currenttoken)       * scale 
                points[1][1] = float(next(tokenized))   * scale
                position[0] = float(next(tokenized))    * scale
                position[1] = float(next(tokenized))    * scale
                geoms.append(['Bezier',list(itertools.imap(transform.transform,svgutil.beziercubic(points[0],points[1],position)))])
            elif command == 't':
                # Draws a quadratic Bezier curve from the current point to (x,y). The control point is assumed to be the reflection of the control point on the previous command relative to the current point. (If there is no previous command or if the previous command was not a Q, q, T or t, assume the control point is coincident with the current point.) T (uppercase) indicates that absolute coordinates will follow; t (lowercase) indicates that relative coordinates will follow. At the end of the command, the new current point becomes the final (x,y) coordinate pair used in the polybezier.
                if previouscommand in "qQtT":
                    points[1] = list(reflected_point(points[1],position))
                else:
                    points[1] = list(position)
                    # control point 
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[0] = points[0][0]+float(currenttoken)    * scale
                position[1] = points[0][1]+float(next(tokenized))    * scale                    
                geoms.append(['Bezier',list(itertools.imap(transform.transform,svgutil.beziercubic(points[0],points[1],position)))])
            elif command == 'T':
                if previouscommand in "qQtT":
                    points[1] = list(reflected_point(points[1],position))
                else:
                    points[1] = list(position)
                    # control point 
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[0] = float(currenttoken)    * scale
                position[1] = float(next(tokenized))    * scale                    
                geoms.append(['Bezier',list(itertools.imap(transform.transform,svgutil.beziercubic(points[0],points[1],position)))])
            elif command == 'a':
                points[0][0] = position[0]
                points[0][1] = position[1]
                # float(currenttoken)        * scale # rx
                float(next(tokenized))      * scale # ry
                float(next(tokenized))              # x-axis rotation (degrees)
                bool(int(next(tokenized)))          # large-arc-flag (0 or 1)
                bool(int(next(tokenized)))          # sweep-flag     (0 or 1)
                position[0] = points[0][0]+float(next(tokenized))    * scale
                position[1] = points[0][1]+float(next(tokenized))    * scale                    
                output('Unsupported SVG path command: %s - elliptical arc (relative)'%command)
                # (rx ry x-axis-rotation large-arc-flag sweep-flag x y)+
            elif command == 'A':
                points[0][0] = position[0]
                points[0][1] = position[1]
                # float(currenttoken)        * scale # rx
                float(next(tokenized))      * scale # ry
                float(next(tokenized))              # x-axis rotation (degrees)
                bool(int(next(tokenized)))          # large-arc-flag (0 or 1)
                bool(int(next(tokenized)))          # sweep-flag     (0 or 1)
                position[0] = float(next(tokenized))    * scale
                position[1] = float(next(tokenized))    * scale                    
                output('Unsupported SVG path command: %s - elliptical arc (absolute)'%command)
            # if(geoms):
                # output(geoms[-1])
            # MoveTo: M, m (implicit L or l)
            # LineTo: L, l, H, h, V, v
            # Cubic Bezier Curve: C, c, S, s
            # Quadratic Bezier Curve: Q, q, T, t
            # Elliptical Arc Curve: A, a
            # ClosePath: Z, z
            
            # An upper-case command specifies absolute coordinates, while a lower-case command specifies coordinates relative to the current position.
            # It is always possible to specify a negative value as an argument to a command:
            # negative angles will be anti-clockwise;
            # absolute negative x and y values are interpreted as negative coordinates;
            # relative negative x values move to the left, and relative negative y values move upwards.
            
            
        # tokens = ['']
        # for char in path:
            # if char in '0123456789-+.':
                # tokens[-1] += char
                # continue
            # if tokens[-1]:
                # tokens.append('')
            # if char not in ' ,':
                # tokens[-1] += char
        # position = [0.0,0.0]
        # currenttoken = 0
        # listresult = []
        # #print(tokens)
        # scale = float(scale)
        # while currenttoken < len(tokens):
            # token = tokens[currenttoken]
            # try: 
                # x = float(token)*scale
                # currenttoken += 1
                # y = float(tokens[currenttoken])*scale
                # currenttoken += 1
                # position[0] += x
                # position[1] += y
                # listresult[-1].append((position[0],position[1]))
                # continue
            # except:
                # if token == 'm':
                    # currenttoken += 1
                    # position[0] = float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # position[1] = float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # listresult.append([(position[0],position[1])])
                    # continue
                # if token == 'l':
                    # currenttoken += 1
                    # position[0] += float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # position[1] += float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # #position = pcbnew.wxPoint(x,y)
                    # listresult[-1].append((position[0],position[1]))
                    # continue
                # if token == 'h':
                    # currenttoken += 1
                    # position[0] += float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # listresult[-1].append((position[0],position[1]))
                    # continue
                # if token == 'v':
                    # currenttoken += 1
                    # position[1] += float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # listresult[-1].append((position[0],position[1]))
                    # continue
                # if token == 'z':
                    # currenttoken += 1
                    # listresult[-1].append(listresult[-1][0])
                    # continue
                # output('Bad SVG token: %s'%token)
                # currenttoken += 1
        return geoms

    # def fromsvg_old(self,inputs):
        # """Geometry,Conversion [PATH_D_ATTRIBUTE SCALE] Converts SVG path element "d attribute"
            # to a list of coordinates suitable for drawelements. Applies SCALE
            # to all coordinates."""
        # #print(path)
        # path = inputs[0]
        # scale = inputs[1]
        # tokens = ['']
        # for char in path:
            # if char in '0123456789-+.':
                # tokens[-1] += char
                # continue
            # if tokens[-1]:
                # tokens.append('')
            # if char not in ' ,':
                # tokens[-1] += char
        # position = [0.0,0.0]
        # currenttoken = 0
        # listresult = []
        # #print(tokens)
        # scale = float(scale)
        # while currenttoken < len(tokens):
            # token = tokens[currenttoken]
            # try: 
                # x = float(token)*scale
                # currenttoken += 1
                # y = float(tokens[currenttoken])*scale
                # currenttoken += 1
                # position[0] += x
                # position[1] += y
                # listresult[-1].append((position[0],position[1]))
                # continue
            # except:
                # if token == 'm':
                    # currenttoken += 1
                    # position[0] = float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # position[1] = float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # listresult.append([(position[0],position[1])])
                    # continue
                # if token == 'l':
                    # currenttoken += 1
                    # position[0] += float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # position[1] += float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # #position = pcbnew.wxPoint(x,y)
                    # listresult[-1].append((position[0],position[1]))
                    # continue
                # if token == 'h':
                    # currenttoken += 1
                    # position[0] += float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # listresult[-1].append((position[0],position[1]))
                    # continue
                # if token == 'v':
                    # currenttoken += 1
                    # position[1] += float(tokens[currenttoken])*scale
                    # currenttoken += 1
                    # listresult[-1].append((position[0],position[1]))
                    # continue
                # if token == 'z':
                    # currenttoken += 1
                    # listresult[-1].append(listresult[-1][0])
                    # continue
                # output('Bad SVG token: %s'%token)
                # currenttoken += 1
        # return listresult
    
    def tocommand(self,elementlist,commandname):
        """Programming,Elements [ELEMENTLIST COMMANDNAME] Create a user command named COMMANDNAME that draws the drawsegments in ELEMENTLIST."""
        kicommand.kc(': %s "Draw Custom Drawing Command"'%commandname)
        for element in elementlist:
            s,e = element.GetStart(), element.GetEnd()
            kicommand.kc('%f,%f,%f,%f drawsegments'%(s[0],s[1],e[0],e[1]))
        kicommand.kc(';')
    
    def REJOIN(self,empty):
        'Action Using selected lines, move multiple connected lines to the isolated line.'
        # Moves the set of coniguous lines or tracks to match the single line already moved.
        kc('drawings copytop selected')
        # lines = _stack[-1]
        # if len(lines) <=2:
            # return
        # for line in lines:
            # output( "Selected:", line.GetStart(), line.GetEnd())
        # if isinstance(lines[0],pcbnew.TRACK):
            # kc('tracks')
        # elif isinstance(lines[0],pcbnew.DRAWSEGMENT):
            # kc('drawings drawsegment filtertype')
        # else:
            # return
            
        # kc('swap connected')
        
        #kc('copy copy GetStart call swap GetEnd call append')
        
        # Stack is now: CONNECTED StartAndEndPoints
        # recast the end points as tuples
        lines_by_vertex = defaultdict(set) #{}
        for line in _stack[-1]:
            # output( 'Connected: ',line)
            for p in (line.GetStart(),line.GetEnd()):
                lines_by_vertex[(p.x,p.y)].add(line)
                #lines_by_vertex.setdefault((p.x,p.y),set()).add(line)
                
        # for vertex,lines in lines_by_vertex.iteritems():
            # output( vertex,': ',lines)
            
        line_by_lonelyvertex = filter(lambda x: len(x[1])==1, lines_by_vertex.iteritems())
        
        # if both vertexes have only one line in lines_by_vertex, then it's the lonely line
        lonely_line = []
        connected_lines = []
        for line in _stack[-1]:
            if len(lines_by_vertex[(line.GetStart().x,line.GetStart().y)]) == 1 \
               and len(lines_by_vertex[(line.GetEnd().x,line.GetEnd().y)]) == 1:
                lonely_line.append(line)
            else:
                connected_lines.append(line)
        _stack.pop()
        # output( 'lonely',len(lonely_line),'; connected',len(connected_lines))
        if len(lonely_line) != 1:
            # output( 'no loney_line')
            return
            
        lonely_line = lonely_line[0]
        lonely_line_vertices = [(lonely_line.GetStart().x,lonely_line.GetStart().y),
                                (lonely_line.GetEnd().x,lonely_line.GetEnd().y)]
        lonely_vertices = [tup[0] for tup in line_by_lonelyvertex]
        lonely_vertices.remove(lonely_line_vertices[0])
        lonely_vertices.remove(lonely_line_vertices[1])
        #output( type(list(lines_by_vertex[lonely_vertices[0]])[0]))
        vector = lonely_line.GetStart() - list(lines_by_vertex[lonely_vertices[0]])[0].GetEnd()
        #output( "Moving by",vector)
        for line in connected_lines:
            #output( '\t',line.GetStart(),line.GetEnd())
            line.Move(vector)
            
        # match lonely_line vertices to each of the other vertices by orientation
        
        
        # find the vertices with only one line coincident.
        # One of these is the lonely line, the other two are the polygon opening.
        # Match topmost or left most coordinates of the lonely line to the opening.
        # Now we have the vector of the Move, so Move the remaining lines.
    
    def printf(self, *arglist):
        'Output [LISTOFLISTS FORMAT] Output each list within LISTOFLISTS formatted according to FORMAT in Pythons {} string format (https://www.python.org/dev/peps/pep-3101/).'
        print('Format:',arglist[0][1])
        
        
        for item in arglist[0][0]:
            #print ("item:",item)
            output(arglist[0][1].format(*item))
            
    def fprintf(self, *arglist):
        "Output [LISTOFLISTS FORMAT FILENAME] Output to FILENAME each list within LISTOFLISTS formatted according to FORMAT in Python's {} string format (https://www.python.org/dev/peps/pep-3101/)."
        arglist = arglist[0]
        #print('Format:',arglist[1])
        filename = os.path.join(os.getcwd(),arglist[2])
        with open(filename,'w') as f: 
            for item in arglist[0]:
                #print("item:",item)
                f.write(arglist[1].format(*item))

    def escaped(self,encoded_string):
        "Conversion [ESCAPED_STRING] Interpret escaped string according to Python escape rules."
        return decodestring(encoded_string[0])
    def pwd(self,empty):
        "Programming Return the present working directory."
        return os.getcwd()
        
    def cduser(self,empty):
        "Programming Change working directory to ~/kicad/kicommand."
        os.chdir(USERSAVEPATH)
        
    def cd(self,path):
        "Programming [PATH] Change working directory to PATH."
        os.chdir(path[0])
        
    def cdproject(self,empty):
        "Programming Return the project directory (location of .kicad_pcb file)."
        os.chdir(os.path.dirname(pcbnew.GetBoard().GetFileName()))
        
    def regex(self, *arglist):
        'Comparison [LIST REGEX] Create a LIST of True/False values corresponding to whether the values in LIST match the REGEX (for use prior to FILTER)'
        stringlist, regex_ = arglist[0]
        #print(stringlist, regex_)
    # Format of comment is: 'Category [ARGUMENT1 ARGUMENT2] Description'
        prog = re.compile(regex_)
        return map(lambda s: prog.match(s),stringlist)
#        '=': Command(2,lambda c: map(lambda x: x==c[1],c[0]),'Comparison',
    def call(self,*c):
        '''Python [OBJECT_OR_LIST FUNCTION_NAME_OR_LIST] Execute each python FUNCTION on 
        each member of OBJECTLIST. Each of the inputs can optionally be a single object. 
        Results are grouped by object (if both inputs are lists, then the results of calling 
        each function on the first object are in the first list in the result list of lists). 
        To change the grouping by function instead, use the ZIP command. To ungroup the results into 
        a single-dimension list, use the FLATLIST command. If only one of OBJECTLIST or FUNCTIONLIST 
        is in fact a list, then only a single-dimension list with all the results is returned. The list 
        of results are in the same order as the original OBJECTLIST. The commands LIST, ZIP, and ZIP2 
        will be helpful here. list,zip2,zip,flatlist,callarg'''
        DEBUG = False
        # Possible permulations
        # 000 OBJECT     FUNCTION    # execute FUNCTION on OBJECT
        # 100 OBJECTLIST FUNCTION    # execute FUNCTION on each OBJECT with ARG, return list of results
 
        # 011 OBJECT     FUNCTIONLIST # execute each FUNCTION on OBJECT, return as a list
        # 111 OBJECTLIST FUNCTIONLIST # execute FUNCTION on each corresponding OBJECT.

        if DEBUG:
            output('argvalue: {}'.format(str(c)))
        obj,func = c[0]
        if DEBUG:
            islist = (isiter(obj),isiter(func))
            output('{}'.format(str(c[0])))
            output('iter: {}'.format(islist))
        
        
        if isiter(obj):
            if isiter(func): # both are iter
                return [[getattr(o,f)() for f in func] for o in obj]
            else: # only obj is iter
                return [getattr(o,func)() for o in obj]
        else:
            if isiter(func): # only func is iter
                return [getattr(obj,f)() for f in func]
            else: # neither are iter
                return getattr(obj,func)()
        
        
        if not isiter(obj) and not isiter(func):
            if DEBUG:
                output('neither obj nor func are iter')
            return getattr(obj,func)()

        if DEBUG:
            output('neither obj nor func are iter')

        # 10 OBJECTLIST  FUNCTION    
        # 01 OBJECT      FUNCTIONLIST
        # 11 OBJECTLIST  FUNCTIONLIST
        
        
        if not isiter(obj):
            obj = [obj]
        if not isiter(func):
            func = [func]
        
        if DEBUG:
            islist = (isiter(obj),isiter(func))
            output('Final:')
            output('obj : {}'.format(str(obj)))
            output('func: {}'.format(str(func)))
            output('iter: {}'.format(islist))
        
        # now we have only case 11
        # cycle all elements to the longest element
        # if obj or func are iterators, then convert to list for 'len'
        # obj = list(obj)
        # func = list(func)
        # callcount = max(len(obj),len(func))
        # if DEBUG:
            # output("Callcount: {}".format(callcount))
            # cobj = cycle(obj)
            # cfunc = cycle(func)
            # output(
            # str(
            # [
            # str((x[0],x[1]))
            # for x in itertools.islice(itertools.izip(cobj,cfunc),callcount)
            # ]
            # ))
            
        #return map(lambda x: getattr(x[0],x[1])(),zip(cycle(obj),cycle(func),range(callcount)))
        #return [map(lambda x: getattr(x[0],f)(),obj) for f in func]
        return [[getattr(o,f)() for f in func] for o in obj]
        
    def callargs(self,*c):
        'Python [OBJECTLIST ARGLISTOFLISTS FUNCTION] Execute python FUNCTION on each member '
        'of OBJECTLIST with arguments in ARGLISTOFLISTS. ARGLISTOFLISTS can be '
        'a different length than OBJECTLIST, in which case ARGLISTOFLISTS '
        'elements will be repeated (or truncated) to match the length of '
        'OBJECTLIST. Returns the list of results in the same order as the '
        'original OBJECTLIST. The commands LIST and ZIP2 will be helpful '
        'here. ARGLISTOFLISTS can also be a single list or a single value, '
        'in which case the value will be converted to a list of lists. '
        'Returns single object if both obj and func are single items, otherwise '
        'will return a list of results. list,list.,zip2,zip,call'
        
        # Possible permulations
        # 010 OBJECT     ARGLIST FUNCTION    # execute FUNCTION once on OBJECT with single ARGLIST
        # 000 OBJECT     ARG     FUNCTION    # execute FUNCTION on OBJECT with single ARG
        # 100 OBJECTLIST ARG     FUNCTION    # execute FUNCTION on each OBJECT with ARG, return list of results
 
        #   ? OBJECT     ARGLOL FUNCTION     #? execute FUNCTION on OBJECT for each ARG list in LOL
        # 110 OBJECTLIST ARGLOL FUNCTION     # execute FUNCTION on OBJECT with corresponding ARG list in LOL, return list of results
        # 011 OBJECT     ARGLOL FUNCTIONLIST # execute each FUNCTION on OBJECT for each ARG list in LOL
        # 111 OBJECTLIST ARGLOL FUNCTIONLIST # execute FUNCTION on each OBJECT using each ARGLIST in turn.


        # Want to handle the following situations
        # Case 000 OBJECT ARG FUNCTION
        #    Return result of OBJECT.FUNCTION(ARG)
        # Case 010 OBJECT ARGLIST FUNCTION
        #    OBJECT.FUNCTION(ARG0,ARG1)
        #    [OBJECT.FUNCTION(ARG0), OBJECT.FUNCTION(ARG1)
        # Case 100 OBJECTLIST ARG FUNCTION
        #    [OBJECT0.FUNCTION(ARG), OBJECT1.FUNCTION(ARG)]
        #  
        # Case 110 OBJECTLIST ARGLOL FUNCTION
        #    [OBJECT0.FUNCTION(ARG00,ARG01), OBJECT1.FUNCTION(ARG10,ARG11)]
        # Case 111 OBJECTLIST ARGLOL FUNCTIONLIST
        #    [[OBJECT0.FUNCTION0(ARG00,ARG01), OBJECT0.FUNCTION1(ARG10,ARG11)],[OBJECT1.FUNCTION0(ARG00,ARG01), OBJECT1.FUNCTION1(ARG10,ARG11)]]
        # Case 011 OBJECT ARGLOL FUNCTIONLIST
        #    [OBJECT.FUNCTION0(ARG00,ARG01), OBJECT.FUNCTION1(ARG10,ARG11)]
        # There's no good way to differentiate a list from a list of lists.
        # It's probably a good idea to assume case 010 is an ARGLOL and not an ARGLIST.
        # Because if ARGLOL is assumed, then you can create it from ARGLIST by preceding with "list".
        # One difference is in the results. You'd have to also delist the results.
        # If ARGLIST was assumed, there's not a good way to create the situation where you want an ARGLOL.
        # Is there a situation where you'd repeated call the same function on the same object with different arguments?
        # Maybe in the case of a rotate or move command, where you are essentially concatenating commands.
        # But it is useful for getting a list of results like with FindNet from multiple netcodes (or names).
        
        # I think the basic rule is that any ARGLIST mirrors FUNCTION list, so that parallel arrays are used.
        # If it's a single FUNCTION, then it's a single ARGLIST. If it is a FUNCTIONLIST, then ARGLOL is assumed.
        # ARG0 (which could itself be a list) is paired with FUNCTION0
        # In case one list is smaller, the function list is cycled (or truncated) to match 
        # the number of arglists given within arglol.
        # This has the useful effect of calling the same function with multiple arguments.
        # Results for the following, for example, 
        # [[ARG00,ARG01],[ARG10,ARG11],[ARG20,ARG21]] [FUNCTION0,FUNCTION1]
        #    [OBJECT0.FUNCTION0(ARG00,ARG01), OBJECT0.FUNCTION1(ARG10,ARG11), OBJECT0.FUNCTION0(ARG20,ARG21)]
        #
        # FUNCTION2 is ignored because no matching argument in ARGLOL:
        # [[ARG00,ARG01],[ARG10,ARG11]] [FUNCTION0,FUNCTION1,FUNCTION2] 
        #    [OBJECT0.FUNCTION0(ARG00,ARG01), OBJECT0.FUNCTION1(ARG10,ARG11)]
        # 
        # Note that For any function in FUNCTIONLIST that take no arguments, 
        # an empty list in that position within the ARGLOL can be used.
        
        # Examples:
        # board 0 int FindNet callargs print
        
        # A single function assumes the argument is for one call. These are errors:
        # board 0,1 int FindNet callargs print 
        # board 0,1 int list. FindNet callargs print 
        
        # Here's the correct version:
        # board 0,1 int list. FindNet list callargs print 
        # function (FindNet) is repeated for each argumentlist in arglol.
        # list. creates a list from each member of the given list. [1,2] becomes [[1],[2]]
        # Useful for preparing arguments for single-argument functions called multiple times.
        
        #output('argvalue: {}'.format(str(c)))
        obj,arg,func = c[0]
        
        
        if isiter(obj):
            if isiter(func): # both are iter
                return [[getattr(o,f)(*a) for f,a in itertools.izip(itertools.cycle(func),arg)] for o in obj]
            else: # only obj is iter
                if not isiter(arg):
                    arg = [arg]
                return [getattr(o,func)(*arg) for o in obj]
        else:
            if isiter(func): # only func is iter
                return [getattr(obj,f)(*a) for f,a in itertools.izip(itertools.cycle(func),arg)]
            else: # neither are iter
                if not isiter(arg):
                    arg = [arg]
                return getattr(obj,func)(*arg)
                
                
                
        if DEBUG:
            islist = (isiter(obj),isiter(arg),isiter(func))
            output('{}'.format(str(c[0])))
            output('iter: {}'.format(islist))
        
        if not isiter(obj) and not isiter(func):
            if DEBUG:
                output('neither obj nor func are iter')
            if not isiter(arg):
                if DEBUG:
                    output('arg is not iter')
                arg = [arg]
            return getattr(obj,func)(*arg)

        if DEBUG:
            output('neither obj nor func are iter')
        if not isiter(arg):
            arg = [[arg]]

        # Now ARG is guaranteed to be LOL (possibly from case 100)
        # 110 OBJECTLIST ARGLOL FUNCTION    
        # 011 OBJECT     ARGLOL FUNCTIONLIST
        # 111 OBJECTLIST ARGLOL FUNCTIONLIST
        if not isiter(obj):
            obj = [obj]
        if not isiter(func):
            func = [func]
        
        if DEBUG:
            islist = (isiter(obj),isiter(arg),isiter(func))
            output('Final:')
            output('obj : {}'.format(str(obj)))
            output('arg : {}'.format(str(arg)))
            output('func: {}'.format(str(func)))
            output('iter: {}'.format(islist))
        
        # now we have only case 111
        # cycle all elements to the longest element
        callcount = max(len(obj),len(arg),len(func))
        if DEBUG:
            output(
            str(
            [
            (cycle(obj),cycle(func),cycle(arg))
            for x in range(callcount)
            ]
            ))
        return map(lambda x: getattr(x[0],x[1])(*x[2]),zip(cycle(obj),cycle(func),cycle(arg),range(callcount)))
                
    # OLD VERSIOM
    # def callargs(self,*c):
        # 'Python [OBJECTLIST ARGLISTOFLISTS FUNCTION] Execute python FUNCTION on each member '
        # 'of OBJECTLIST with arguments in ARGLISTOFLISTS. ARGLISTOFLISTS can be '
        # 'a different length than OBJECTLIST, in which case ARGLISTOFLISTS '
        # 'elements will be repeated (or truncated) to match the length of '
        # 'OBJECTLIST. Returns the list of results in the same order as the '
        # 'original OBJECTLIST. The commands LIST and ZIP2 will be helpful '
        # 'here. ARGLISTOFLISTS can also be a single list or a single value, '
        # 'in which case the value will be converted to a list of lists. list,zip2,zip'
        
        # if not isiter(c[0]) and not isiter(c[2]):
            # if not isiter(args):
                # args = [args]
        
        # if not isiter(args):
            # args = [[args]]
    
        # c = c[0]
        # #print(c)
        # args = c[1]
        
        # if isiter(args):
            # if not isiter(args[0]):
                # args = [args]
        # else:
            # args = [[args]]

        # if not hasattr(c,'__iter__') and not isinstance(c,basestring):
            # c = [c]
            
        # if len(c[0]) > args:
            # return map(lambda x: 
                # getattr(x[0],c[2])(*(x[1])), 
                # zip(c[0], cycle(args))
                # )
        # elif len(c[0]) < args:
            # return map(lambda x: 
                # getattr(x[0],c[2])(*(x[1])), 
                # zip(cycle(c[0]), args)
                # )
        # else:
            # return map(lambda x: 
                # getattr(x[0],c[2])(*(x[1])), 
                # zip(c[0], args)
                # )
                
    # def FINDNET(netname):
        # 'Draw [NETNAME] Returns the netcode of NETNAME.'
        # # board has: 'BuildListOfNets', 'CombineAllAreasInNet', 'FindNet'
        # board = getBoard()
        # # nets = board.GetNetsByName()
        # # netinfo = nets.find(netname).value()[1]
        
        # netinfo = board.FindNet(netname)
        # return netinfo.GetNet()

    def getpolypoints(self,*c):
        """Geometry [SEGMENTLIST] Extract a list of polygon points from SEGMENTLIST. Returns a list of lists."""

        dseglist = c[0][0]
        print(dseglist)
        # get the connected pairs. Use any one as a starting point.
        # Between each successive pair of segments, find the intersection point assuming 
        # the lines are infinite. Use the closest of the segments' points as the polygon point.
        # This ensures that the grid is maintained.
        ordered_and_split = order_segments(dseglist)
        polypointslist = []

        # order_segments() returns a list of lists. Each element of the first-level list is 
        # a set of SEGMENTS that are connected together, and expect to be a single polygon.
        for seglist in ordered_and_split:
            polypoints = []    
            a,b = itertools.tee(dseglist,2)
            segiter = itertools.chain(a,itertools.islice(b,1))
            points = []
            # take first two segments
            # find minimum distance 0s,1s; 0s,1e; 0e,1s; 0e,1e; 
            points.extend(get_ds_ends(segiter.next()))
            points.extend(get_ds_ends(segiter.next()))
            dists = (
                wxPointUtil.distance2(points[0],points[2]),
                wxPointUtil.distance2(points[0],points[3]),
                wxPointUtil.distance2(points[1],points[2]),
                wxPointUtil.distance2(points[1],points[3]))        
            minindex = min(enumerate(dists), key=operator.itemgetter(1))[0] 
            # make sure the closest points are indexes 1 and 2
            # index 0 is connected in the other direction
            # index 3 is connected to the next point we will process
            if minindex < 2:
               points[0],points[1] = points[1],points[0] 
               
            if minindex % 2:
               points[2],points[3] = points[3],points[2] 
            
            polypoints.append(points[1])
            points = points[-1:] # this will be a one-element list
            
            for nextseg in segiter:
                points.extend(get_ds_ends(nextseg))
                if wxPointUtil.distance2(points[0],points[2]) < wxPointUtil.distance2(points[0],points[1]):
                    points[1],points[2] = points[2],points[1]        
                polypoints.append(points[1])
                points = points[-1:]
            polypointslist.append(polypoints)
            
        return polypointslist

    def getgeom(self,*c):
        """Geometry [OBJECTLIST] Extract the OBJECTLIST geometries into list of strings, suitable for newdrawing, newtrack, or newzone. Some information is lost, such as thickness, corner smoothing, and layer. newdrawing,newtrack,newzone"""
        result = []
        # output('c={}'.format(c))
        # output('c[0]={}'.format(c[0]))
        for segment in c[0][0]:
            if isinstance(segment,pcbnew.DRAWSEGMENT):
                segmentshapenum = segment.GetShape()
                if segmentshapenum == pcbnew.S_SEGMENT:
                    outtype = 'Line'
                    result.append([outtype,segment.GetStart(),segment.GetEnd()])
                elif segmentshapenum == pcbnew.S_ARC:
                    outtype = 'ArcC'
                    result.append([outtype,segment.GetArcStart(),segment.GetCenter(),segment.GetAngle()/10.0])
                elif segmentshapenum == pcbnew.S_CIRCLE:
                    outtype = 'CircleP'
                    result.append([outtype,segment.GetCenter(),segment.GetStart()])
                elif segmentshapenum == pcbnew.S_POLYGON:
                    #outtype = 'Polygon'
                    result.append(parse_poly_set(segment.GetPolyShape()))
                elif segmentshapenum == pcbnew.S_CURVE:
                    outtype = 'Bezier'
                    result.append([outtype,
                    segment.GetStart(),
                    segment.GetBezControl1(),
                    segment.GetBezControl2(),
                    segment.GetEnd()])

                elif segmentshapenum == pcbnew.S_RECT:
                    outtype = 'Rect'
                    result.append([outtype,'Unsupported'])
            elif isinstance(segment,pcbnew.ZONE_CONTAINER):
                    # output('zone')
                    #outtype = 'Zone'
                    result.append(parse_poly_set(segment.GetFilledPolysList()))
            elif isinstance(segment,pcbnew.ZONE_CONTAINERS):
                    result.append([parse_poly_set(segment.GetFilledPolysList()) for zone in zone_containers])
                    #result.extend(itertools.imap([parse_poly_set(segment.GetFilledPolysList()) for zone in zone_containers])
            elif isinstance(segment,pcbnew.VIA):
                result.append([outtype,'VIA Unsupported'])
            # elif isinstance(segment,pcbnew.ARC):
                # outtype = 'ArcM'
                # result.append([outtype,segment.GetStart(),segment.GetEnd(),segment.GetMid()])
            elif isinstance(segment,pcbnew.TRACK):
                outtype = 'Line'
                result.append([outtype,segment.GetStart(),segment.GetEnd()])
        return result

# test string
# Point,0,0,Dot,mm,1,TTranslate,mm,0,10,Point,0,0,Dot,2,TTranslate,mm,0,10,Point,0,0,Dot,3 split newdrawing refresh

# help with array manipulation:
# seq = [1,2,1]
# reduce(lambda a,b: a[b],seq[:-1],g)[seq[-1]] = val
# Traceback (most recent call last):
  # File "<input>", line 1, in <module>
# NameError: name 'val' is not defined
# val = 3
# reduce(lambda a,b: a[b],c[1],c[0])
# 749
# val = 750
# reduce(lambda a,b: a[b],seq[:-1],g)[seq[-1]] = val

    def newdrawing(self,*c):
        """Draw [GEOMS] Define new DRAWSEGMENT shapes, sing layers and attributes from drawparams."""
    
        fracture = True
        pendingFracture = False
        c=c[0]
        layerID = getLayerID(_user_stacks['Params'][-1]['l'])
        thickness = max(1,int(_user_stacks['Params'][-1]['t']))
        board = getBoard()
        results = []
        previousPoint = None
        previousGeom = None
        previousSegment = None
        previousCornerRadius = None
        currentCornerRadius = None
        
        for geom in streamgeom().streamgeom(c):
            # output("GEOM = {}".format(str(geom)))

            if geom[0] in ('Hole', 'Polygon.'):
                pendingFracture = True
                previousSegment = None
                ds = results[-1]
                if ds.GetShape() != pcbnew.S_POLYGON:
                    raise TypeError("Hole must be preceded by Polygon")
                lc=pcbnew.SHAPE_LINE_CHAIN()
                map(lc.Append,itertools.starmap(pcbnew.VECTOR2I,geom[1:]))
                ps = ds.GetPolyShape()
                if geom[0][0] == 'H':
                    ps.AddHole(lc)
                else:
                    ps.AddOutline(lc)
                continue
            else:
                if pendingFracture and fracture:
                    pendingFracture = False
                    ds = results[-1]
                    ps = ds.GetPolyShape()
                    ps.Fracture(1) # now efficiently, this is called after polygon is complete
                # ds.GetPolyShape().AddHole(pcbnew.SHAPE_LINE_CHAIN(geom[1:]))
                
                # previousPoint = geom[-1]
                # previousGeom = geom[0]




            if geom[0] == 'Line':
                for argset in itertools.izip_longest(*(iter(geom[1:]),) * 2):
                    ds=pcbnew.DRAWSEGMENT(board)
                    board.Add(ds)
                    results.append(ds)
                    previousSegment = ds

                    ds.SetLayer(layerID)                
                    ds.SetShape(pcbnew.S_SEGMENT)
                    
                    ds.SetWidth(thickness)

                    ds.SetStart(argset[0])
                    ds.SetEnd(argset[1])
                    previousPoint = argset[1]
                previousGeom = geom[0]

                
            elif geom[0].startswith('Arc') and len(geom[0]) == 4:
                previousSegment = None

            # Autodesk: To create an arc, you can specify combinations of center, endpoint, start point, radius, angle, chord length, and direction values
            # Arc: A chord, a central angle or an inscribed angle may divide a circle into two arcs. The smaller of the two arcs is called the minor arc. The larger of the two arcs is called the major arc.
            
                if geom[0][-1] == 'C': # center start angle
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        ds=pcbnew.DRAWSEGMENT(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)                
                        ds.SetShape(pcbnew.S_ARC)

                        ds.SetWidth(thickness)
                        
                        # output('Created ArcC with C={}; S={}; A={}'.format(*argset))
                        ds.SetCenter(argset[0])
                        ds.SetArcStart(argset[1])
                        ds.SetAngle(int(argset[2]*10))
                elif geom[0][-1] == 'O': # start, mid, end
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        (start, mid, end) = argset
                        # (center, start, angle) = argset
                        ds=pcbnew.DRAWSEGMENT(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)                
                        ds.SetShape(pcbnew.S_ARC)

                        ds.SetWidth(thickness)
                        
                        # 'O' to 'C'
                        center = centerFromPoints(*argset)
                        # radius = wxpointutil.distance(argset[0],center)
                        # vector angle
                        # output('Start={}; Center={};'.format(start,center))
                        startvector = (start[0] - center[0],start[1] - center[1])
                        startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi

                        endvector = (end[0] - center[0],end[1] - center[1])
                        endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi
                        
                        angle = endangledeg - startangledeg
                        
                        midvector = (mid[0] - center[0],mid[1] - center[1])
                        midangledeg = math.atan2(float(midvector[1]),midvector[0])*180/math.pi
                        
                        #output("sme (angle) = {} > {} > {}".format(int(startangledeg),int(midangledeg),int(endangledeg)))

                        # start mid end newmid
                        # m0=m-s ; e0=e-s
                        # a0=a-s
                        # if not s<m<e:
                        # if not (s<m<a or s>m>a):
                        #     if a<=0:
                        #         a += 360
                        #     else:
                        #         a -= 360

                        # 1,0 1,1 0,1 -1,1 -1,0 -1,-1 0,-1 1,-1
                        
                        s=startangledeg % 360
                        m=midangledeg % 360
                        e=endangledeg % 360
                        
                        if s<m<e or m<e<s or e<s<m:
                            angle = angle%360
                        elif s<e<m or m<s<e or e<m<s:
                            angle = angle%360-360

                        #output('SME={} --> CSA={}'.format(str((start,mid,end)),str((center,start,angle))))
                        ds.SetArcStart(pcbnew.wxPoint(*start))
                        ds.SetCenter(pcbnew.wxPoint(*center))
                        ds.SetAngle(int(angle*10))
                        previousPoint = end
                elif geom[0][-1] == 'P': # center start end
   #?
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        ds=pcbnew.DRAWSEGMENT(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)                
                        ds.SetShape(pcbnew.S_ARC)

                        ds.SetWidth(thickness)

                        # output('Unsupported ArcP with C={}; S={}; E={}'.format(*argset))
                        center,start,end = argset
                        
                        startvector = (start[0] - center[0],start[1] - center[1])
                        startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi
                        
                        endvector = (end[0] - center[0],end[1] - center[1])
                        endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi

                        angle = endangledeg - startangledeg

                        ds.SetCenter(center)
                        ds.SetArcStart(start)
                        ds.SetAngle(int(angle*10))
                        previousPoint = end
                        
                elif geom[0][-1] == 'R': # start end radius
   #?
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        start,end,radius = argset
                        ds=pcbnew.DRAWSEGMENT(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)                
                        ds.SetShape(pcbnew.S_ARC)

                        ds.SetWidth(thickness)
                        
                        center = centerFromPointsAndRadius(start,end,radius)
                        startvector = (start[0] - center[0],start[1] - center[1])
                        startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi
                        
                        endvector = (end[0] - center[0],end[1] - center[1])
                        endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi

                        angle = endangledeg - startangledeg

                        #output('C={}; S={}; A={}'.format(center,start,angle))
                        ds.SetCenter(pcbnew.wxPoint(*center))
                        ds.SetArcStart(start)
                        ds.SetAngle(int(angle*10))
                previousGeom = geom[0]

            elif geom[0].startswith('Circle') and len(geom[0]) == 7:
                previousSegment = None
                if geom[0][-1] == 'C':
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 2):
                        center,radius = argset
                        end = pcbnew.wxPoint(center[0]+radius,center[1])

                        ds=pcbnew.DRAWSEGMENT(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)                
                        ds.SetShape(pcbnew.S_CIRCLE)

                        ds.SetWidth(thickness)
                        #output('C={}; S={}'.format(center,start))
                        ds.SetCenter(center)
                        ds.SetEnd(end)
                    
                elif geom[0][-1] == 'P':

                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 2):
                        center,end = argset
                        ds=pcbnew.DRAWSEGMENT(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)                
                        ds.SetShape(pcbnew.S_CIRCLE)

                        ds.SetWidth(thickness)
                        #output('C={}; S={}'.format(center,start))
                        ds.SetCenter(center)
                        ds.SetEnd(end)
                elif geom[0][-1] == 'R':
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        p1,p2,radius = argset
                        ds=pcbnew.DRAWSEGMENT(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)                
                        ds.SetShape(pcbnew.S_CIRCLE)

                        ds.SetWidth(thickness)
                        
                        center = centerFromPointsAndRadius(p1,p2,radius)
                        #output('C={}; S={}'.format(center,p1))
                        ds.SetCenter(pcbnew.wxPoint(*center))
                        ds.SetEnd(p1)
                        
                elif geom[0][-1] == 'O':
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        end,p2,p3 = argset
                        ds=pcbnew.DRAWSEGMENT(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)                
                        ds.SetShape(pcbnew.S_CIRCLE)

                        ds.SetWidth(thickness)
                        # output("three points: {} {} {}".format(*argset))
                        
                        center = centerFromPoints(*argset)
                        center = pcbnew.wxPoint(*center)
                        # output("center ({})={}".format(type(center),center))
                        # output("end ({})={}".format(type(end),end))
                        ds.SetCenter(center)
                        ds.SetEnd(end)
                previousGeom = geom[0]

            elif geom[0] == 'Polygon':
                previousSegment = None
                ds=pcbnew.DRAWSEGMENT(board)
                board.Add(ds)
                results.append(ds)
                ds.SetLayer(layerID)                
                ds.SetShape(pcbnew.S_POLYGON)

                ds.SetWidth(thickness)
                ds.SetPolyPoints(geom[1:])
                # ds.GetPolyShape().AddHole(pcbnew.SHAPE_LINE_CHAIN(geom[1:]))
                previousPoint = geom[-1]
                previousGeom = geom[0]
            elif geom[0] == 'PolylineRounded':
            # PolylineRounded,mm,2,20,20,25,25,20,25,30,30,35,35,40,35 split newdrawing refresh
            # PolylineRounded,mm,2,20,20,20,25,20,20,25,20,20 split newdrawing refresh
                firstsegment = None
                firstpoint = None
                cornerRadius = geom[1]
                #output('CornerR={}'.format(cornerRadius))
                startpoints = itertools.islice(geom,2,len(geom))
                endpoints = itertools.islice(geom,3,len(geom))
                for start,end in itertools.izip(startpoints,endpoints):
                    #output("s={} e={}".format(start,end))
                    ds=pcbnew.DRAWSEGMENT(board)
                    board.Add(ds)
                    ds.SetLayer(layerID)                
                    ds.SetShape(pcbnew.S_SEGMENT)
                    
                    ds.SetWidth(thickness)
                    ds.SetStart(start)
                    ds.SetEnd(end)
                    if firstsegment is None:
                        #output('setting firstsegment')
                        firstsegment = ds
                        firstpoint = start
                    else:
                        #output('drawing arc near {}: {}'.format(start,str((results[-1].GetStart(),results[-1].GetEnd(),ds.GetStart(),ds.GetEnd()))))
                        draw_arc_to_lines(cornerRadius,results[-1],ds)
                    results.append(ds)
                lastsegment = results[-1]
                if firstpoint[0] == end[0] and firstpoint[1] == end[1]:
                    #output('drawing arc at end near {}'.format(firstpoint))
                    draw_arc_to_lines(cornerRadius,firstsegment,lastsegment)
                
            
            elif geom[0] == 'Polyline':
                if previousGeom in ('Dot','Via','Corner'):
                    #output('Continuing polyline from {}'.format(previousPoint))
                 
                 
                
                    # output("previous Dot")
                    previousGeom = geom[0]
                    geom[0] = previousPoint
                    startpoints = iter(geom)
                    endpoints = iter(geom[1:])
                    # endpoints = itertools.islice(geom,1,len(geom)-1)
                else:
                    # output("previous not Dot")
                    previousGeom = geom[0]
                    startpoints = itertools.islice(geom,1,len(geom))
                    endpoints = itertools.islice(geom,2,len(geom))
                for start,end in itertools.izip(startpoints,endpoints):
                    # output("s={} e={}".format(start,end))
                    ds=pcbnew.DRAWSEGMENT(board)
                    board.Add(ds)
                    results.append(ds)
                    ds.SetLayer(layerID)                
                    ds.SetShape(pcbnew.S_SEGMENT)
                    
                    ds.SetWidth(thickness)
# Polyline,mm,20,20,25,25,20,25,Dot,mm,3,Polyline,mm,30,30,35,35 split newdrawing refresh
# Polyline,mm,20,20,25,25,20,25,Polyline,mm,30,30,35,35 split newdrawing refresh
# Polyline,mm,20,20,25,25,20,25,Via,mm,2,1,Polyline,mm,30,30,35,35 split newdrawing refresh
# Polyline,mm,20,20,25,25,20,25,Corner,mm,1,Polyline,mm,30,30,35,35,Via,mm,3,2,F.Cu,Polyline,mm,40,35 split newdrawing refresh
                    ds.SetStart(start)
                    ds.SetEnd(end)
                    if previousSegment and currentCornerRadius:
                    # make a corner between previousCornerSegment and ds.
                        #output("Corner radius {} ".format(currentCornerRadius))
                        draw_arc_to_lines(currentCornerRadius,ds,previousSegment)
                        previousSegment = None
                        currentCornerRadius = None
                    #output("s={} e={}".format(start,end))
                    previousSegment = ds
                    previousPoint = end
# a=[0,1,2,3,4,5,6,7,8]
# s=itertools.islice(a,1,len(a))


            elif geom[0].startswith('Bezier'):
                for argset in itertools.izip_longest(*(iter(geom[1:]),) * 4):
                    ds=pcbnew.DRAWSEGMENT(board)
                    board.Add(ds)
                    results.append(ds)
                    ds.SetLayer(layerID)                
                    ds.SetShape(pcbnew.S_CURVE)

                    ds.SetWidth(thickness)
                    
                    
                    ds.SetStart(argset[0])
                    ds.SetBezControl1(argset[1])
                    ds.SetBezControl2(argset[2])
                    ds.SetEnd(argset[3])
                    previousPoint = argset[3]
                    previousSegment = None # change this to ds when Corner after Bezier is supported
                previousGeom = geom[0]
            elif geom[0] == 'Via': # arguments are [Type] Width DrillValue [ToLayer] 
                previousSegment = None
                previousGeom = geom[0]
                ds=pcbnew.VIA(board)
                board.Add(ds)
                results.append(ds)
                ds.SetPosition(previousPoint)
                
                viatypes = {
                    'Blind':pcbnew.VIA_BLIND_BURIED,
                    'Buried':pcbnew.VIA_BLIND_BURIED,
                    'Through':pcbnew.VIA_THROUGH,
                    'Micro':pcbnew.VIA_MICROVIA
                    # pcbnew.VIA_NOT_DEFINED 
                }
                viatype = viatypes.get(geom[1],None)
                if viatype:
                    typeindex = 1
                else:
                    typeindex = 0
                    viatype = viatypes['Through']
                ds.SetViaType(viatype)
                w = int(pcbnew.IU_PER_MM*float(geom[typeindex+1]))
                d = int(pcbnew.IU_PER_MM*float(geom[typeindex+2]))
                ds.SetWidth(max(w,d))
                ds.SetDrill(min(w,d))
                
                fromLayerID = getLayerID(_user_stacks['Params'][-1]['l'])
                #output('geomlen={}; layerindex={}'.format(len(geom),typeindex+3))
                if len(geom) > (typeindex+3):
                    tolay = geom[typeindex+3]
                    toLayerID = getLayerID(tolay)
                    PARAM('l',tolay)
                    layerID = getLayerID(_user_stacks['Params'][-1]['l'])
                else:
                    toLayerID = fromLayerID
                ds.SetLayerPair(fromLayerID,toLayerID)
                
                # SetWidth(int)?
                #SetDrillDefault()
            elif geom[0] == 'Dot': # argument is Diameter
                previousSegment = None
                previousGeom = geom[0]
                radius = int(geom[1])
                centerpoint = previousPoint
                
                # for argset in itertools.izip_longest(*(iter(geom[2:]),) * 1):
                    # centerpoint = argset
                ds=pcbnew.DRAWSEGMENT(board)
                board.Add(ds)
                results.append(ds)
                ds.SetLayer(layerID)                
                ds.SetShape(pcbnew.S_CIRCLE)
                

                ds.SetWidth(radius)
                #output('C={}; S={}'.format(center,start))
                #output("Drawing dot at center {}, {}".format(*centerpoint))
                ds.SetCenter(centerpoint)
                ds.SetEnd(centerpoint)#pcbnew.wxPoint(centerpoint[0]+1,centerpoint[1]))
                #output("After Center={}; Position={}".format(ds.GetCenter(),ds.GetPosition()))
            elif geom[0] == 'Layer':
                PARAM('l',geom[-1])
                layerID = getLayerID(_user_stacks['Params'][-1]['l'])
                
            elif geom[0] == 'Thickness':
                PARAM('t',geom[-1])
                thickness = max(1,int(_user_stacks['Params'][-1]['t']))

            elif geom[0] == 'Text':
                # text,pos,size
                text = ' '.join(geom[2:])
                if '\\' in text:
                    text = decodestring(text)
                text = draw_text(text,geom[1],[_user_stacks['Params'][-1]['w'],_user_stacks['Params'][-1]['h']],layer=_user_stacks['Params'][-1]['l'],thickness=_user_stacks['Params'][-1]['t'])
                results.append(text)
            elif geom[0] == 'Point':
                previousSegment = None
                previousGeom = geom[0]
                previousPoint = geom[-1]
            elif geom[0] == 'Corner':
                previousGeom = geom[0]
                if len(geom) >= 2:
                    currentCornerRadius = geom[1]
                else:
                    currentCornerRadius = previousCornerRadius
        return results

    def newtrack(self,*c):
        """Draw [OBJECTS] Define new tracks using layers and attributes from drawparams."""
        results = []
        c=c[0]
        layerID = getLayerID(_user_stacks['Params'][-1]['l'])
        thickness = max(1,int(_user_stacks['Params'][-1]['t']))
        for geom in streamgeom().streamgeom(c):
            if geom[0] == 'Line':
                for argset in itertools.izip_longest(*(iter(geom[1:]),) * 2):
                    # makeline(*argset)
                    ds = draw_segmentwx(*argset,layer=_user_stacks['Params'][-1]['l'],thickness=_user_stacks['Params'][-1]['t'])
                    results.append(ds)

            elif geom[0].startswith('Arc') and len(geom[0] == 4):
                if geom[-1] == 'M':
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        board = getBoard()
                        ds=pcbnew.ARC(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)
                        ds.SetWidth(thickness)
                        
                        ds.SetStart(argset[0])
                        ds.SetMid(argset[1])
                        ds.SetEnd(argset[2])
                elif geom[-1] == 'C': # center start angle
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        (center, start, angle) = argset
                        board = getBoard()
                        ds=pcbnew.ARC(board)
                        board.Add(ds)
                        results.append(ds)
                        ds.SetLayer(layerID)
                        ds.SetWidth(thickness)
                        
                        # Angle from center to start
                        startvector = start - center
                        startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi
                        endangledeg = startangledeg + angle
                        endanglerad = endangledeg*math.pi/180
                        r=wxpointutil.distance(center,start)
                        endx=center[0]+r*math.cos(endanglerad)
                        endy=center[1]+r*math.sin(endanglerad)
                        # Add "angle" then find midangle by dividing by 2
                        midanglerad = ((startangledeg*math.pi/180)+endanglerad)/2
                        midx=center[0]+r*math.cos(midanglerad)
                        midy=center[1]+r*math.sin(midanglerad)
                        #output('CSA={} --> SME={}'.format(str((center,start,angle)),str((start[0],start[1],midx,midy,endx,endy))))
                        # ds.SetStart(argset[0])
                        # ds.SetMid(argset[1])
                        # ds.SetEnd(argset[2])
            elif geom[0].startswith('Circle') and len(geom[0] == 7):
                pass
            elif geom[0].startswith('Polygon'):
                pass
            elif geom[0].startswith('Polyline'):
                pass
            elif geom[0].startswith('Bezier'):
                pass
            elif geom[0].startswith('Via'): # arguments are [Type] DrillValue ToLayer 
            # VIATYPE_BLIND_BURIED
            # VIATYPE_MICROVIA
            # VIATYPE_NOT_DEFINED
            # VIATYPE_THROUGH
                pass
        return results
    
    def contourlisttopolygonpoints(self,contourlist,bsteps=None,arcerror=None,arcunits=None):
        """Geometry [GEOM_LIST] Convert geoms to line segments. getgeoms,"""
        if bsteps is None:
            bsteps = _user_stacks['Params'][-1].get('beziersteps',5)
        if arcerror is None:
            arcerror = _user_stacks['Params'][-1].get('arcerror',0.1)
        if arcunits is None:
            arcunits = _user_stacks['Params'][-1].get('arcunits',2500)
        # points = []
        points = []
        firstwinding = None
        c=contourlist
        #output('Geoms input to conourlist:\n{}'.format(pprint.pformat(c)))

        layerID = getLayerID(_user_stacks['Params'][-1]['l'])
        thickness = max(1,int(_user_stacks['Params'][-1]['t']))
        arcerror = _user_stacks['Params'][-1].get('arcerror',0.1)
        arcunits = _user_stacks['Params'][-1].get('arcunits',2500)
        
        board = getBoard()
        results = []
        previousPoint = None
        previousGeom = None
        previousSegment = None
        previousCornerRadius = None
        currentCornerRadius = None
        for contour in contourlist:
            points.append([])
            for geom in streamgeom().streamgeom(contour):
                # output("GEOM = {}".format(str(geom)))

                if geom[0] == 'Group':
                    if points and points[-1]:
                        currentpoints = points[-1][1:]
                        if len(currentpoints) > 0:
                            if firstwinding is None:
                                if currentpoints:
                                    firstwinding = IsWindingCW(currentpoints)
                                    # output('firstwinding is Clockwise? {}'.format(firstwinding))
                            elif firstwinding != IsWindingCW(currentpoints):
                                #points[-1][0] = 'Hole'
                                pass #output('polygon winding different than first: polygon Hole')
                            else:
                                pass #output('polygon winding matches first path (CW? {})'.format(firstwinding))
                    points.append(['Polygon'])
                if geom[0] == 'Line':
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 2):
                        if points[-1]:
                            points[-1].append(argset[1])
                        else:
                            points[-1].extend(argset)
                    previousGeom = geom[0]
                elif geom[0].startswith('Arc') and len(geom[0]) == 4:
                    previousSegment = None
                    
                # Autodesk: To create an arc, you can specify combinations of center, endpoint, start point, radius, angle, chord length, and direction values
                # Arc: A chord, a central angle or an inscribed angle may divide a circle into two arcs. The smaller of the two arcs is called the minor arc. The larger of the two arcs is called the major arc.
                
                    if geom[0][-1] == 'C': # center start angle
                        for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                            points[-1].extend(arctopoints(*argset,arcerror=arcerror,arcunits=arcunits)) # center,start,angle
                    elif geom[0][-1] == 'O': # start, mid, end
                        for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                            (start, mid, end) = argset
                            
                            # 'O' to 'C'
                            center = centerFromPoints(*argset)
                            startvector = (start[0] - center[0],start[1] - center[1])
                            startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi

                            endvector = (end[0] - center[0],end[1] - center[1])
                            endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi
                            
                            angle = endangledeg - startangledeg
                            
                            midvector = (mid[0] - center[0],mid[1] - center[1])
                            midangledeg = math.atan2(float(midvector[1]),midvector[0])*180/math.pi
                                                    
                            s=startangledeg % 360
                            m=midangledeg % 360
                            e=endangledeg % 360
                            
                            if s<m<e or m<e<s or e<s<m:
                                angle = angle%360
                            elif s<e<m or m<s<e or e<m<s:
                                angle = angle%360-360
                            points[-1].extend(arctopoints(center,start,angle,arcerror=arcerror,arcunits=arcunits)) # center,start,angle
                            previousPoint = end
                    elif geom[0][-1] == 'P': # center start end
                        for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):

                            # output('Unsupported ArcP with C={}; S={}; E={}'.format(*argset))
                            center,start,end = argset
                            
                            startvector = (start[0] - center[0],start[1] - center[1])
                            startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi
                            
                            endvector = (end[0] - center[0],end[1] - center[1])
                            endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi

                            angle = endangledeg - startangledeg

                            points[-1].extend(arctopoints(center,start,angle,arcerror=arcerror,arcunits=arcunits)) # center,start,angle
                            previousPoint = end
                    elif geom[0][-1] == 'R': # start end radius
                        for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                            start,end,radius = argset
                            
                            center = centerFromPointsAndRadius(start,end,radius)
                            startvector = (start[0] - center[0],start[1] - center[1])
                            startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi
                            
                            endvector = (end[0] - center[0],end[1] - center[1])
                            endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi

                            angle = endangledeg - startangledeg

                            points[-1].extend(arctopoints(center,start,angle,arcerror=arcerror,arcunits=arcunits)) # center,start,angle
                    previousGeom = geom[0]
                elif geom[0] == 'Polyline':
                    if previousGeom in ('Dot','Via','Corner'):
                        #output('Continuing polyline from {}'.format(previousPoint))
                     
                     
                    
                        # output("previous Dot")
                        previousGeom = geom[0]
                        geom[0] = previousPoint
                        startpoints = iter(geom)
                        endpoints = iter(geom[1:])
                        # endpoints = itertools.islice(geom,1,len(geom)-1)
                    else:
                        # output("previous not Dot")
                        previousGeom = geom[0]
                        startpoints = itertools.islice(geom,1,len(geom))
                        endpoints = itertools.islice(geom,2,len(geom))
                    for start,end in itertools.izip(startpoints,endpoints):
                        if previousSegment and currentCornerRadius:
                        # # make a corner between previousCornerSegment and ds.
                            # output("Corner radius {} ".format(currentCornerRadius))
                            # draw_arc_to_lines(currentCornerRadius,ds,previousSegment)
                            # previousSegment = None
                            # currentCornerRadius = None

                            pass
                        else:
                            points[-1].append(end) # This misses the first point
                        previousSegment = ds
                        previousPoint = end
    # a=[0,1,2,3,4,5,6,7,8]
    # s=itertools.islice(a,1,len(a))


                elif geom[0].startswith('Bezier'):
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 4):
                        previousPoint = argset[3]
                        if points[-1]:
                            points[-1].extend(beziertopoints(*argset,steps=bsteps)[1:])
                        else:
                            points[-1].extend(beziertopoints(*argset,steps=bsteps))
                        previousSegment = None # change this to ds when Corner after Bezier is supported
                    previousGeom = geom[0]
                elif geom[0] == 'Via': # arguments are [Type] Width DrillValue [ToLayer] 
                    previousSegment = None
                    previousGeom = geom[0]
                    viatypes = {
                        'Blind':pcbnew.VIA_BLIND_BURIED,
                        'Buried':pcbnew.VIA_BLIND_BURIED,
                        'Through':pcbnew.VIA_THROUGH,
                        'Micro':pcbnew.VIA_MICROVIA
                        # pcbnew.VIA_NOT_DEFINED 
                    }
                    viatype = viatypes.get(geom[1],None)
                    if viatype:
                        typeindex = 1
                    else:
                        typeindex = 0
                        viatype = viatypes['Through']
                    w = int(pcbnew.IU_PER_MM*float(geom[typeindex+1]))
                    d = int(pcbnew.IU_PER_MM*float(geom[typeindex+2]))
                    
                    fromLayerID = getLayerID(_user_stacks['Params'][-1]['l'])
                    #output('geomlen={}; layerindex={}'.format(len(geom),typeindex+3))
                    if len(geom) > (typeindex+3):
                        tolay = geom[typeindex+3]
                        toLayerID = getLayerID(tolay)
                        PARAM('l',tolay)
                        layerID = getLayerID(_user_stacks['Params'][-1]['l'])
                    else:
                        toLayerID = fromLayerID
                    ds.SetLayerPair(fromLayerID,toLayerID)
                    
                    # SetWidth(int)?
                    #SetDrillDefault()
                elif geom[0] == 'Dot': # argument is Diameter
                    previousSegment = None
                    previousGeom = geom[0]
                    radius = int(geom[1])
                    centerpoint = previousPoint
                    
                    # for argset in itertools.izip_longest(*(iter(geom[2:]),) * 1):
                        # centerpoint = argset
                    ds=pcbnew.DRAWSEGMENT(board)
                    board.Add(ds)
                    results.append(ds)
                    ds.SetLayer(layerID)                
                    ds.SetShape(pcbnew.S_CIRCLE)
                    

                    ds.SetWidth(radius)
                    #output('C={}; S={}'.format(center,start))
                    ds.SetCenter(centerpoint)
                    ds.SetEnd(centerpoint)#pcbnew.wxPoint(centerpoint[0]+1,centerpoint[1]))

                elif geom[0] == 'Layer':
                    PARAM('l',geom[-1])
                    layerID = getLayerID(_user_stacks['Params'][-1]['l'])
                    
                elif geom[0] == 'Thickness':
                    PARAM('t',geom[-1])
                    thickness = max(1,int(_user_stacks['Params'][-1]['t']))

                elif geom[0] == 'Text':
                    # text,pos,size
                    text = ' '.join(geom[2:])
                    if '\\' in text:
                        text = decodestring(text)
                    text = draw_text(text,geom[1],[_user_stacks['Params'][-1]['w'],_user_stacks['Params'][-1]['h']],layer=_user_stacks['Params'][-1]['l'],thickness=_user_stacks['Params'][-1]['t'])
                    results.append(text)
                elif geom[0] == 'Point':
                    previousSegment = None
                    previousGeom = geom[0]
                    previousPoint = geom[-1]
                elif geom[0] == 'Corner':
                    previousGeom = geom[0]
                    if len(geom) >= 2:
                        currentCornerRadius = geom[1]
                    else:
                        currentCornerRadius = previousCornerRadius
        
        
        # if points and points[-1]:
            # currentpoints = points[-1][1:]
            # if len(currentpoints) > 0:
                # if firstwinding is None:  # for ttf fonts, CW is contour, CCW is hole
                    # if currentpoints:
                        # firstwinding = IsWindingCW(currentpoints)
                        # output('firstwinding is {}'.format(firstwinding))
                # elif firstwinding != IsWindingCW(currentpoints):
                    # #output('polygon Hole')
                    # pass #points[-1][0] = 'Hole'
                    # #output('polygon winding different than first')
                # else:
                    # pass #output('polygon winding matches first')

        return points

    def geomtopolygon(self,geomlist):
        """Geometry [GEOM_LIST] Convert geoms to line segments. getgeoms,"""
        # points = []
        points = [['Polygon']]
        firstwinding = None
        c=geomlist
        layerID = getLayerID(_user_stacks['Params'][-1]['l'])
        thickness = max(1,int(_user_stacks['Params'][-1]['t']))
        board = getBoard()
        results = []
        previousPoint = None
        previousGeom = None
        previousSegment = None
        previousCornerRadius = None
        currentCornerRadius = None
        
        for geom in streamgeom().streamgeom(c):
            # output("GEOM = {}".format(str(geom)))

            if geom[0] == 'Group':
                if points and points[-1]:
                    currentpoints = points[-1][1:]
                    if len(currentpoints) > 0:
                        if firstwinding is None:
                            if currentpoints:
                                firstwinding = IsWindingCW(currentpoints)
                                # output('firstwinding is Clockwise? {}'.format(firstwinding))
                        elif firstwinding != IsWindingCW(currentpoints):
                            #points[-1][0] = 'Hole'
                            pass #output('polygon winding different than first: polygon Hole')
                        else:
                            pass #output('polygon winding matches first path (CW? {})'.format(firstwinding))
                points.append(['Polygon'])
            if geom[0] == 'Line':
                for argset in itertools.izip_longest(*(iter(geom[1:]),) * 2):
                    points[-1].extend(argset)
                previousGeom = geom[0]
            elif geom[0].startswith('Arc') and len(geom[0]) == 4:
                previousSegment = None

            # Autodesk: To create an arc, you can specify combinations of center, endpoint, start point, radius, angle, chord length, and direction values
            # Arc: A chord, a central angle or an inscribed angle may divide a circle into two arcs. The smaller of the two arcs is called the minor arc. The larger of the two arcs is called the major arc.
            
                if geom[0][-1] == 'C': # center start angle
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        points[-1].extend(arctopoints(*argset)) # center,start,angle
                elif geom[0][-1] == 'O': # start, mid, end
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        (start, mid, end) = argset
                        
                        # 'O' to 'C'
                        center = centerFromPoints(*argset)
                        startvector = (start[0] - center[0],start[1] - center[1])
                        startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi

                        endvector = (end[0] - center[0],end[1] - center[1])
                        endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi
                        
                        angle = endangledeg - startangledeg
                        
                        midvector = (mid[0] - center[0],mid[1] - center[1])
                        midangledeg = math.atan2(float(midvector[1]),midvector[0])*180/math.pi
                                                
                        s=startangledeg % 360
                        m=midangledeg % 360
                        e=endangledeg % 360
                        
                        if s<m<e or m<e<s or e<s<m:
                            angle = angle%360
                        elif s<e<m or m<s<e or e<m<s:
                            angle = angle%360-360
                        points[-1].extend(arctopoints(pcbnew.wxPoint(*center),pcbnew.wxPoint(*start),angle)) # center,start,angle
                        previousPoint = end
                elif geom[0][-1] == 'P': # center start end
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):

                        # output('Unsupported ArcP with C={}; S={}; E={}'.format(*argset))
                        center,start,end = argset
                        
                        startvector = (start[0] - center[0],start[1] - center[1])
                        startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi
                        
                        endvector = (end[0] - center[0],end[1] - center[1])
                        endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi

                        angle = endangledeg - startangledeg

                        points[-1].extend(arctopoints(center,start,angle)) # center,start,angle
                        previousPoint = end
                elif geom[0][-1] == 'R': # start end radius
                    for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        start,end,radius = argset
                        
                        center = centerFromPointsAndRadius(start,end,radius)
                        startvector = (start[0] - center[0],start[1] - center[1])
                        startangledeg = math.atan2(float(startvector[1]),startvector[0])*180/math.pi
                        
                        endvector = (end[0] - center[0],end[1] - center[1])
                        endangledeg = math.atan2(float(endvector[1]),endvector[0])*180/math.pi

                        angle = endangledeg - startangledeg

                        points[-1].extend(arctopoints(pcbnew.wxPoint(*center),start,angle)) # center,start,angle
                previousGeom = geom[0]

            # elif geom[0].startswith('Circle') and len(geom[0]) == 7:
                
                # previousSegment = None
                # if geom[0][-1] == 'C':
                    # for argset in itertools.izip_longest(*(iter(geom[1:]),) * 2):
                        # center,radius = argset
                        # end = pcbnew.wxPoint(center[0]+radius,center[1])

                        # ds=pcbnew.DRAWSEGMENT(board)
                        # board.Add(ds)
                        # results.append(ds)
                        # ds.SetLayer(layerID)                
                        # ds.SetShape(pcbnew.S_CIRCLE)

                        # ds.SetWidth(thickness)
                        # #output('C={}; S={}'.format(center,start))
                        # ds.SetCenter(center)
                        # ds.SetEnd(end)
                    
                # elif geom[0][-1] == 'P':

                    # for argset in itertools.izip_longest(*(iter(geom[1:]),) * 2):
                        # center,end = argset
                        # ds=pcbnew.DRAWSEGMENT(board)
                        # board.Add(ds)
                        # results.append(ds)
                        # ds.SetLayer(layerID)                
                        # ds.SetShape(pcbnew.S_CIRCLE)

                        # ds.SetWidth(thickness)
                        # #output('C={}; S={}'.format(center,start))
                        # ds.SetCenter(center)
                        # ds.SetEnd(end)
                # elif geom[0][-1] == 'R':
                    # for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        # p1,p2,radius = argset
                        # ds=pcbnew.DRAWSEGMENT(board)
                        # board.Add(ds)
                        # results.append(ds)
                        # ds.SetLayer(layerID)                
                        # ds.SetShape(pcbnew.S_CIRCLE)

                        # ds.SetWidth(thickness)
                        
                        # center = centerFromPointsAndRadius(p1,p2,radius)
                        # output('C={}; S={}'.format(center,p1))
                        # ds.SetCenter(pcbnew.wxPoint(*center))
                        # ds.SetEnd(p1)
                        
                # elif geom[0][-1] == 'O':
                    # for argset in itertools.izip_longest(*(iter(geom[1:]),) * 3):
                        # end,p2,p3 = argset
                        # ds=pcbnew.DRAWSEGMENT(board)
                        # board.Add(ds)
                        # results.append(ds)
                        # ds.SetLayer(layerID)                
                        # ds.SetShape(pcbnew.S_CIRCLE)

                        # ds.SetWidth(thickness)
                        # # output("three points: {} {} {}".format(*argset))
                        
                        # center = centerFromPoints(*argset)
                        # center = pcbnew.wxPoint(*center)
                        # # output("center ({})={}".format(type(center),center))
                        # # output("end ({})={}".format(type(end),end))
                        # ds.SetCenter(center)
                        # ds.SetEnd(end)
                # previousGeom = geom[0]

            # elif geom[0] == 'Polygon':
                # previousSegment = None
                # ds=pcbnew.DRAWSEGMENT(board)
                # board.Add(ds)
                # results.append(ds)
                # ds.SetLayer(layerID)                
                # ds.SetShape(pcbnew.S_POLYGON)

                # ds.SetWidth(thickness)
                # ds.SetPolyPoints(geom[1:])
                # previousPoint = geom[-1]
                # previousGeom = geom[0]
            # elif geom[0] == 'PolylineRounded':
            # # PolylineRounded,mm,2,20,20,25,25,20,25,30,30,35,35,40,35 split newdrawing refresh
            # # PolylineRounded,mm,2,20,20,20,25,20,20,25,20,20 split newdrawing refresh
                # firstsegment = None
                # firstpoint = None
                # cornerRadius = geom[1]
                # output('CornerR={}'.format(cornerRadius))
                # startpoints = itertools.islice(geom,2,len(geom))
                # endpoints = itertools.islice(geom,3,len(geom))
                # for start,end in itertools.izip(startpoints,endpoints):
                    # output("s={} e={}".format(start,end))
                    # ds=pcbnew.DRAWSEGMENT(board)
                    # board.Add(ds)
                    # ds.SetLayer(layerID)                
                    # ds.SetShape(pcbnew.S_SEGMENT)
                    
                    # ds.SetWidth(thickness)
                    # ds.SetStart(start)
                    # ds.SetEnd(end)
                    # if firstsegment is None:
                        # output('setting firstsegment')
                        # firstsegment = ds
                        # firstpoint = start
                    # else:
                        # output('drawing arc near {}: {}'.format(start,str((results[-1].GetStart(),results[-1].GetEnd(),ds.GetStart(),ds.GetEnd()))))
                        # draw_arc_to_lines(cornerRadius,results[-1],ds)
                    # results.append(ds)
                # lastsegment = results[-1]
                # if firstpoint[0] == end[0] and firstpoint[1] == end[1]:
                    # output('drawing arc at end near {}'.format(firstpoint))
                    # draw_arc_to_lines(cornerRadius,firstsegment,lastsegment)
                
            
            elif geom[0] == 'Polyline':
                if previousGeom in ('Dot','Via','Corner'):
                    output('Continuing polyline from {}'.format(previousPoint))
                 
                 
                
                    # output("previous Dot")
                    previousGeom = geom[0]
                    geom[0] = previousPoint
                    startpoints = iter(geom)
                    endpoints = iter(geom[1:])
                    # endpoints = itertools.islice(geom,1,len(geom)-1)
                else:
                    # output("previous not Dot")
                    previousGeom = geom[0]
                    startpoints = itertools.islice(geom,1,len(geom))
                    endpoints = itertools.islice(geom,2,len(geom))
                for start,end in itertools.izip(startpoints,endpoints):
                    if previousSegment and currentCornerRadius:
                    # # make a corner between previousCornerSegment and ds.
                        # output("Corner radius {} ".format(currentCornerRadius))
                        # draw_arc_to_lines(currentCornerRadius,ds,previousSegment)
                        # previousSegment = None
                        # currentCornerRadius = None

                        pass
                    else:
                        points[-1].append(start,end)
                    previousSegment = ds
                    previousPoint = end
# a=[0,1,2,3,4,5,6,7,8]
# s=itertools.islice(a,1,len(a))


            elif geom[0].startswith('Bezier'):
                for argset in itertools.izip_longest(*(iter(geom[1:]),) * 4):
                    previousPoint = argset[3]
                    points[-1].extend(beziertopoints(*argset))
                    previousSegment = None # change this to ds when Corner after Bezier is supported
                previousGeom = geom[0]
            elif geom[0] == 'Via': # arguments are [Type] Width DrillValue [ToLayer] 
                previousSegment = None
                previousGeom = geom[0]
                viatypes = {
                    'Blind':pcbnew.VIA_BLIND_BURIED,
                    'Buried':pcbnew.VIA_BLIND_BURIED,
                    'Through':pcbnew.VIA_THROUGH,
                    'Micro':pcbnew.VIA_MICROVIA
                    # pcbnew.VIA_NOT_DEFINED 
                }
                viatype = viatypes.get(geom[1],None)
                if viatype:
                    typeindex = 1
                else:
                    typeindex = 0
                    viatype = viatypes['Through']
                w = int(pcbnew.IU_PER_MM*float(geom[typeindex+1]))
                d = int(pcbnew.IU_PER_MM*float(geom[typeindex+2]))
                
                fromLayerID = getLayerID(_user_stacks['Params'][-1]['l'])
                #output('geomlen={}; layerindex={}'.format(len(geom),typeindex+3))
                if len(geom) > (typeindex+3):
                    tolay = geom[typeindex+3]
                    toLayerID = getLayerID(tolay)
                    PARAM('l',tolay)
                    layerID = getLayerID(_user_stacks['Params'][-1]['l'])
                else:
                    toLayerID = fromLayerID
                ds.SetLayerPair(fromLayerID,toLayerID)
                
                # SetWidth(int)?
                #SetDrillDefault()
            elif geom[0] == 'Dot': # argument is Diameter
                previousSegment = None
                previousGeom = geom[0]
                radius = int(geom[1])
                centerpoint = previousPoint
                
                # for argset in itertools.izip_longest(*(iter(geom[2:]),) * 1):
                    # centerpoint = argset
                ds=pcbnew.DRAWSEGMENT(board)
                board.Add(ds)
                results.append(ds)
                ds.SetLayer(layerID)                
                ds.SetShape(pcbnew.S_CIRCLE)
                

                ds.SetWidth(radius)
                #output('C={}; S={}'.format(center,start))
                ds.SetCenter(centerpoint)
                ds.SetEnd(centerpoint)#pcbnew.wxPoint(centerpoint[0]+1,centerpoint[1]))

            elif geom[0] == 'Layer':
                PARAM('l',geom[-1])
                layerID = getLayerID(_user_stacks['Params'][-1]['l'])
                
            elif geom[0] == 'Thickness':
                PARAM('t',geom[-1])
                thickness = max(1,int(_user_stacks['Params'][-1]['t']))

            elif geom[0] == 'Text':
                # text,pos,size
                text = ' '.join(geom[2:])
                if '\\' in text:
                    text = decodestring(text)
                text = draw_text(text,geom[1],[_user_stacks['Params'][-1]['w'],_user_stacks['Params'][-1]['h']],layer=_user_stacks['Params'][-1]['l'],thickness=_user_stacks['Params'][-1]['t'])
                results.append(text)
            elif geom[0] == 'Point':
                previousSegment = None
                previousGeom = geom[0]
                previousPoint = geom[-1]
            elif geom[0] == 'Corner':
                previousGeom = geom[0]
                if len(geom) >= 2:
                    currentCornerRadius = geom[1]
                else:
                    currentCornerRadius = previousCornerRadius
        if points and points[-1]:
            currentpoints = points[-1][1:]
            if len(currentpoints) > 0:
                if firstwinding is None:  # for ttf fonts, CW is contour, CCW is hole
                    if currentpoints:
                        firstwinding = IsWindingCW(currentpoints)
                        # output('firstwinding is {}'.format(firstwinding))
                elif firstwinding != IsWindingCW(currentpoints):
                    #output('polygon Hole')
                    pass #points[-1][0] = 'Hole'
                    #output('polygon winding different than first')
                else:
                    pass #output('polygon winding matches first')


        # Now, we have both the simplified list and the detailed points list.
        # each item in orderedlist is a list containing 'Polygon' or 'Hole' followed by polygon points.
        # We need to convert that to a fractured list of polygons.
        # 1) For each

        return points
        # coding=<encoding name>
        # 1\n2 stringtogeom Thickness,mm,0.1,TScale,0.04,0.04 split swap append newdrawing refresh
        # "KiCADは素晴\nらしいオープンソースプロジェクトです" stringtogeom newdrawing refresh
        # "Το KiCAD είναι ένα φοβερό\nέργο ανοιχτού κώδικα.\n\n KiCADは素晴\nらしいオープンソースプロジェクトです\n\n1234567890\n!@#$%^&*()\nABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz" stringtogeom TScale,0.01,0.01 split swap append newdrawing refresh
        # 1234567890\n!@#$%^&*()\nABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz stringtogeom geomtopolygons copy TScale,0.01,0.01 split swap append newdrawing refresh
        # ab\ncd stringtogeom geomtopolygon Thickness,1,TScale,0.01,0.01 split swap append newdrawing refresh
        # aa stringtogeom Thickness,1,TTranslate,0,15000000,TScale,0.05,0.05 split swap append newdrawing refresh
        # "Το KiCAD είναι ένα φοβερό\nέργο ανοιχτού κώδικα.\n\n KiCADは素晴\nらしいオープンソースプロジェクトです\n\n1234567890\n!@#$%^&*()\nABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz" stringtogeom Thickness,1,TTranslate,0,15000000,TScale,0.05,0.05 split swap append newdrawing refresh
        # : r "" int getunicoderange concat \n concat ; ' 0,100 r 100,100 r 200,100 r 300,100 r 400,100 r 500,100 r 600,100 r 700,100 r 800,100 r 900,100 r print stringtogeom Thickness,1,TScale,0.05,0.05 split swap append newdrawing refresh
        # : r "" int getunicoderange concat \n concat ; ' 0,3 r 100,3 r 200,3 r 300,3 r 400,3 r 500,3 r 600,3 r 700,3 r 800,3 r 900,3 r 1000,3 r print stringtogeom Thickness,1,TScale,0.05,0.05 split swap append newdrawing refresh
        # : r "" 1 pick list 1 pick append int getunicoderange concat \n concat ; ' 0 3 int copy pull 2 int + list swap append r 100,3 r 200,3 r 300,3 r 400,3 r 500,3 r 600,3 r 700,3 r 800,3 r 900,3 r 1000,3 r print stringtogeom Thickness,1,TScale,0.05,0.05 split swap append newdrawing refresh
        # : t "Start with two ints/floats on the stack, this will add together and make a list added and the second argument." swap 1 pick + int delist swap 1 pick list 1 pick append ; clear -3 int 3 int t
        # : rangeline "" 1 pick list 1 pick append int getunicoderange concat \n concat ; : nextrange "Start with two ints/floats on the stack, this will add together and make a list added and the second argument." swap 1 pick + int delist swap 1 pick list 1 pick append ; : r "Execute one unicode range into elements." rangeline nextrange ; clear -3 3 r r r r r r r r r r
        # startint stepint t r t r t r
        # : rangeline "" getunicoderange 3 pull swap concat \n concat ; : nextrange ""  1 pull 2 pull 1 pick + int delist swap 1 pick list 1 pick append stack ; : r "Execute one unicode range into elements." nextrange rangeline ; 
        #  100 int 10 int "" r r r r
        # clear 1 int 25 int "" r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r r print
        # clear -99 int 100 int "" r r r r r r r r r r r r r r r r r r r r r r r r r r r r r print
        # clear -149 int 150 int "" r r r r r r r r r r r r r r r r r r r r  print
        # stringtogeom Thickness,1,TTranslate,0,43000000,TScale,0.05,0.05 split swap append newdrawing refresh ◎ 9678 
        # 0x25CB	9675	WHITE CIRCLE in font table is 'circle'
        # 'AA\nAAA stringtogeom Thickness,1,TScale,10000,-10000 split swap append newdrawing refresh
        # For Noto Regular
        # 'AA\nAAA\nA stringtogeom Thickness,1,TScale,1000,-1000 split swap append newdrawing refresh
        # 'abc\ndef\nghi stringtogeom Thickness,1,TTranslate,0,53000,TScale,1000,1000 split swap append newdrawing refresh
        # clear 8 150 * 149 - 150 int "" r r r r  print
        # clear 0 150 * 149 - 150 int "" r r r r  r r r r  r r r r  r r r r  r r r r  r r r r  print
        # https://www.cambam.pixelmaker.eu/Cambam/Aide/Plugins/stickfonts.html
        
    def stringtogeom(self,*c):
        """Geometry [STRING] Convert string to geoms."""
        current_position=[0.0,0,0] # native units

        #scale = float(1) # 0.02*pcbnew.IU_PER_MM # for converting font glyph data into KiCAD units
        heightvector = [0.0,0.0]
        line_start = list(current_position)
        #output('string type {}'.format(type(c[0][0])))
        
        # to output the font at the actual size 
        # fscale = 72 * 1000 * pcbnew.IU_PER_MIL * FontSizeInPoints / unitsPerEm
        FontSizeInPoints = 10.0
        # output('font unitsPerEm = {}'.format(fonts.getfont()._overall['unitsPerEm']))
        fscale = 1000.0 * pcbnew.IU_PER_MILS * FontSizeInPoints / (fonts.getfont()._overall['unitsPerEm'] * 72.0)
        # start a new transform matrix. then scale so the font is actual size and
        # 10 point font = em bounding box is 10 / 72 inches (138 mils = 3.5 mm).
        geomlist = [['T+','Thickness',1,'S',fscale,'Sy',-1]] # make the preamble its own list
        stringforrender = c[0][0].encode('unicode_escape').decode('string_escape').decode('unicode_escape')
        for char in stringforrender:
            # Each glyph will be a single polygon, with (possibly) multiple polygon outer contours and holes.
            try:
                glyphdata = fonts.getfont().char(char)
            except:
                glyphdata = None
            overall = fonts.getfont()._overall
            # heightvector[0] = max(glyphdata['hv'][0],heightvector[0]) # need to handle negative values
            # heightvector[1] = max(glyphdata['hv'][1],heightvector[1])
            
            if glyphdata:
                #output('{} {}'.format(glyphdata['av'],glyphdata['svg']))
                #output(': {}'.format(str(geom)))
                contourgeoms = svgutil.fromsvgcontours(glyphdata['svg'])
                # comments here are old :-(
                # break each self intersecting contour into non-intersecting polygons. 
                # determine hierarchy of polygons, determine which are holes and which occur inside holes, etc.
                # 
                # output('simplified outlines: {}'.format(simplified_outlines))
                bsteps = _user_stacks['Params'][-1].get('beziersteps',5)
                polygonpoints = self.contourlisttopolygonpoints(contourgeoms,bsteps=bsteps)
                # orderedindexlist = getpolygonholes(simplified_outlines)
                orderedindexlist = getpolygonholes(polygonpoints)
                #for ptype,index in getpolygonholes(simplified_outlines):
                drawnpoints = polygonpoints
                #drawnpoints = svgutil.fromsvgcontours(glyphdata['svg'],simplified=1)

                # get detailed polygons from contourlisttopolygonpoints
                # Then we have both the detailed list and the ordered index list
                

                #output('Ordered Index List:\n{}'.format(pprint.pformat(orderedindexlist)))
                #output('Geoms for polygon:\n{}'.format(pprint.pformat(contourgeoms)))
                #polygonpoints = self.geomtopolygon(contourgeoms)
                 

                #output('polygons result: {}'.format(pprint.pformat(polygonpoints)))
                orderedlist = []
                for ptype,ipoly in orderedindexlist:
                    drawnpoints[ipoly].insert(0,ptype)
                    orderedlist.append(drawnpoints[ipoly])
                geomlist.extend(orderedlist)
                #current_position[0] += glyphdata['aw']*scale
                advance = list(glyphdata['av'])
            else:
                advance = [0.0,0.0]
            
            #output('ord {}'.format(ord(char)))
            if ord(char) == 10:
                advance[0] += -(current_position[0]-line_start[0])
                advance[1] = -overall['line'][1]
                #output('advancing line by {}; after scale {}'.format(advance,(advance[0]*scale,advance[1]*scale)))
            geomlist.append(('+T,{},{}'.format(advance[0],advance[1]).split(',')))
            current_position[0] += advance[0]
            current_position[1] += advance[1]
            # TTranslate,mm,0,150 split a\nd stringtogeom append print
            #output('FINAL GEOM LIST BEFORE POLYGON {}'.format(geomlist))
        geomlist.append('T-') # pop out of the character transform matrix

        return geomlist # self.geomtopolygon((geomlist))
    def stringtosvg(self,*c):
        """Geometry [STRING] Convert string to geoms."""
        current_position=[0.0,0,0] # native units
        geomlist = []
        scale = 1 #0.02*pcbnew.IU_PER_MM # for converting font glyph data into KiCAD units
        heightvector = [0.0,0.0]
        line_start = list(current_position)
        #output('string type {}'.format(type(c[0][0])))
        stringforrender = c[0][0].encode('unicode_escape').decode('string_escape').decode('unicode_escape')
        for char in stringforrender:
            try:
                glyphdata = fonts.getfont().char(char)
            except:
                glyphdata = None
            overall = fonts.getfont()._overall
            # heightvector[0] = max(glyphdata['hv'][0],heightvector[0]) # need to handle negative values
            # heightvector[1] = max(glyphdata['hv'][1],heightvector[1])
            
            if glyphdata:
                #output('{} {}'.format(glyphdata['av'],glyphdata['svg']))
                #output(': {}'.format(str(geom)))
                geomlist.append(svgutil.fromsvgcontours((glyphdata['svg'],scale))) # fromsvgcontours are the contour geoms
                #current_position[0] += glyphdata['aw']*scale
                advance = [glyphdata['av'][0],glyphdata['av'][1]]
            else:
                advance = [0.0,0.0]
            
            #output('ord {}'.format(ord(char)))
            if ord(char) == 10:
                advance[0] += - (current_position[0]-line_start[0])
                advance[1] += -overall['line'][1]
                #output('advancing line by {}; after scale {}'.format(advance,(advance[0]*scale,advance[1]*scale)))
            geomlist.append(('+T,{},{}'.format(advance[0],advance[1]).split(',')))
            current_position[0] += advance[0]
            current_position[1] += advance[1]
            # TTranslate,mm,0,150 split a\nd stringtogeom append print
            #output('FINAL GEOM LIST BEFORE POLYGON {}'.format(geomlist))
        return ' '.join(svglist)
    # def newsegment(self,*c):
        # """Draw [TYPE POINTS] Define a new segment using drawparameters, TYPE (string), and POINTS (list of floats)."""
        # c=c[0]
        # output("newsegment: {}".format(c))
        # _newsegment(*c)
        # # It's plausible that entries can come in any of the following.
        # # Single Line
        # # string,[number,number,number,number]
        # # string,[(number,number),(number,number)]
        # # string,[point,point]
        # # string,[point,(number,number)]
        # # string,[(number,number),point]
        # #?string,[(number,number),number,number]
        # #?string,[number,number,(number,number)]
        # #?string,[point,number,number]
        # #?string,[number,number,point]

        # for inlist in [
            # [1,2,3,4,5,6,7,8]
            # ,[[1,2],[3,4],[5,6],[7,8]]
            # ,[(1,2),(3,4),(5,6),(7,8)]
            # ,[pcbnew.wxpoint(1,2),pcbnew.wxpoint(3,4),pcbnew.wxpoint(4,6),pcbnew.wxpoint(7,8)]
            # ,[pcbnew.wxpoint(1,2),3,4,pcbnew.wxpoint(4,6),(7,8)]
            # ,[list("12345678")]
            # ]:
            # print(listtoargs("pp",inlist))
        # # first element is point,number, or iterable (2-element list or tuple)
        
        # # Possible algorithm for Line
        # listtoargs("pp",c[1])
    # def getfontlist(self,*c):
        # """Font Returns the list of available fonts."""
        # return fonts.getfontmanager().getfontlist()
    def getfontlist(self,*c):
        """Font Returns the list of available fonts with family and subfamily."""
        fontlist = []
        fontbyfamandsub = fonts.getfontmanager().getfontfamilies()
        for family,famdict in sorted(fontbyfamandsub.items()):
            for subfamily,subdict in sorted(famdict.items()):
                for fontname in sorted(subdict):
                    fontlist.append('{}: Family: {} Subfamily: {}'.format(fontname,family,subfamily))
        output('\n'.join(fontlist))
        
    def setfont(self,fontname):
        """Font [FONTNAME] Sets the current font to FONTNAME. getfontlist,"""
        global font
        font = fonts.getfont(fontname[0]) or font
    def fontinfo(self,*c):
        """Font Output current font's info"""
        f = fonts.getfont()
        retval = []
        for nId in f.getNameIndexes():
            retval.append(u'{}: {}\n'.format(f.getNameShortDescription(nId),f.getNameValue(nId)))
        output(u'{}:\n'.format(f._fontname))
        
        retval = ''.join(retval)
        retval = '\n'.join(['\n'.join(textwrap.wrap(line, 76,
                 break_long_words=False, replace_whitespace=False))
                 for line in retval.splitlines() if line.strip() != ''])

        # indent('\n'.join(textwrap.wrap(''.join(retval),76)), 4)
        retval = indent(retval,4)
        output(retval)
#               indent('\n'.join(textwrap.wrap(''.join(retval),6)), 4)

    symboltype2args = {
        'A': ('type','posx','posy','radius','start_angle','end_angle','unit','convert','thickness','fill','startx','starty','endx','endy')
        ,'C': ('type','posx','posy','radius','unit','convert','thickness','fill')
        ,'S': ('type','startx','starty','endx','endy','unit','convert','thickness','fill')
        ,'P': ('type','point_count','unit','convert','thickness') # (px py)* fill
        #,'X': ('type','name','num','posx','posy','length','direction','name_text_size','num_text_size','unit','convert','electrical_type') # [pin_type]
        }
        
# https://en.wikibooks.org/wiki/Kicad/file_formats
# 

# name = name displayed on the pin
# num = pin no. displayed on the pin
# posx = Position X same units as the length
# posy = Position Y same units as the length
# length = length of pin
# direction = R for Right, L for left, U for Up, D for Down
# name_text_size = Text size for the pin name
# num_text_size = Text size for the pin number
# unit_num = Unit number reference (see REF 'unit_count')
# convert = (0 if common to the representations, if not 1 or 2)
# electrical_type = Elec. Type of pin (I=Input, O=Output, B=Bidi, T=tristate,P=Passive, U=Unspecified, W=Power In, w=Power Out, C=Open Collector, E=Open Emitter, N=Not Connected)
# [pin_type] = Type of pin or "Graphic Style" (N=Not Visible, I=Invert (hollow circle), C=Clock, IC=Inverted Clock, L=Low In (IEEE), CL=Clock Low, V=Low Out (IEEE), F=Falling Edge, NX=Non Logic). Optional : when not specified uses "Line" graphic style.
    def importlib(self,filename):
        """Symbol,Schematic [LIB_FILE_NAME] import lib file as a dict with drawing elements, keyed by symbol name. getsymbolvar,symboltogeom"""
        filename = filename[0]
        libdict = {}
        output('reading file: {}'.format(filename))
        with codecs.open(filename, encoding='utf-8') as lib:
            fileiter = iter(lib)
            version = next(fileiter)
            # EESchema-LIBRARY Version 2.4
            if version != 'EESchema-LIBRARY Version 2.4\n':
                output('Warning: Expected EESchema-LIBRARY Version 2.4. Detected Version {}'.format(version.split()[-1]))
            for line in fileiter:
                if line.startswith('#'):
                    continue
                #output('Line: {}'.format(line))
                words = line.split()
                if words[0] == 'DEF':
                    key = words[1]
                    for line in fileiter:
                        # if line.startswith('#'):
                            # continue
                        words = line.split()
                        if words[0] == 'DRAW':
                            drawdef = []
                            parts = defaultdict(list)
                            for line in fileiter:
                                # if line.startswith('#'):
                                    # continue
                                if words[0] == 'ENDDRAW':
                                    break
                                words = line.split()
                                # Here we create dictionary keyed by convert + unit

                                keys = self.symboltype2args.get(words[0],None)
                                if keys is None:
                                    continue
                                pdict = {k:v for (k,v) in zip(keys, words)} 
                                if words[0] == 'P':
                                    pdict['points'] = words[len(keys):-1]
                                    pdict['fill'] = words[-1]
                                unitconvert = '00'
                                parts[pdict['convert']+pdict['unit']].append(line)

                                drawdef.append(parts)

                                # if words[0] in 'ACTS':
                                    # drawdef.append(line)
                            if words[0] == 'ENDDRAW':
                                break
                    
                    libdict[key] = parts # drawdef
        return libdict

    def getsymbolvar(self, c):
        """Symbol,Schematic [IMPORTLIBOUTPUT NAME_VAR_UNIT] from the output of importlib, retrieve the specified symbol, variation and unit. importlib,symboltogeom"""
        ssoutput, namevarunit = c
        
        if isinstance(namevarunit,basestring):
            namevarunit = namevarunit.split(',')
        name = namevarunit.pop(0)
        if namevarunit:
            var = str(namevarunit.pop(0))
        else:
            var = '1'
        if namevarunit:
            unit = str(namevarunit.pop(0))
        else:
            unit = '1'
        # except:            
            # raise TypeError('Name, Unit, and Variation must be specified as list or comma-separated string "INVERTER,1,1"')
        # cu also gets 0u and c0
        
        single = ssoutput[name]
        #output('single: {}'.format(str(single)))
        varunit=str(var)+str(unit)
        lineoutput = []
        for key in (varunit,varunit[0]+'0','0'+varunit[1:]):
            #output('key {}?'.format(key))
            if key in single:
                lineoutput.extend(single[key])
        return ''.join(lineoutput)
        
    # def splitsymbolvars(self, drawdef):
        # """Schematic [DRAW_DEFINITION] extract the units and variations from the DRAW_DEFINITION. ,importlib"""
        # parts = defaultdict(list)
        # for line in drawdef[0].splitlines():
            # words = line.split()
            # keys = self.symboltype2args.get(words[0],None)
            # if keys is None:
                # continue
            # pdict = {k:v for (k,v) in zip(keys, words)} 
            # if words[0] == 'P':
                # points = itertools.islice(words,len(keys),-1)
                # pdict['points'] = points
                # pdict['fill'] = words[-1]
            # #unitconvert = '00'
            
            # parts[pdict['convert']+pdict['unit']].append(line)
        # return parts
        
    # to get a symbol to geom, use importlib SYMBOLNAME,CONVERT,UNIT getsymbolvar symboltogeom
    # alternatively define this
    # : getsymbolgeom "Symbol [LIBFILE SYMBOLNAME_CONVERT_UNIT_LIST] Gets the indicated symbol variation and part number from LIBFILE. importlib,getsymbolvar,symboltogeom" pull 1 importlib swap getsymbolvar symboltogeom ;
    def symboltogeom(self, drawdef):
        """Schematic [DRAW_DEFINITION] the definition of the symbol, as returned by importlib and getsymbolvar. importlib,getsymbolvar"""
        # https://en.wikibooks.org/wiki/Kicad/file_formats#Schematic_Libraries_Files_Format
        geoms = []
        # #unit = int(drawdef[1])
        # # 'P' (polygon) is special because it has multiple vertices.
        # # 'T' (text) is special because text could(?) include spaces.
        # symboltype2args = {
            # 'A': ('type','posx','posy','radius','start_angle','end_angle','unit','convert','thickness','fill','startx','starty','endx','endy')
            # ,'C': ('type','posx','posy','radius','unit','convert','thickness','fill')
            # ,'S': ('type','startx','starty','endx','endy','unit','convert','thickness','fill')
            # ,'P': ('type','point_count','unit','convert','thickness') # (px py)* fill
            # }
        for line in drawdef[0].splitlines():
            words = line.split()
            if words[0] == 'A':

                # A posx posy radius start_angle end_angle unit convert thickness fill startx starty endx endy
                keys = ('type','posx','posy','radius','start_angle','end_angle','unit','convert','thickness','fill','startx','starty','endx','endy')
                pdict = { k:v for (k,v) in zip(keys, words)}
                # u = int(pdict['unit'])
                # if u != 0 and u != unit:
                    # continue
                pdict['angle'] = (float(pdict['end_angle']) - float(pdict['start_angle']))/10.0
                # posx, posy = centre of the circle part of which is the arc
                # radius = radius of the lost arc
                # start_angle = start angle of the arc in tenths of degrees
                # end_angle = end angle of the arc in tenths of degrees
                # startx, starty = coordiantes of the start of the arc
                # endx, endy = coordinates of the end of the arc

                # center,start,angle
                #output(str(pdict))
                geoms.append(
                'ArcC,{posx},{posy},{startx},{starty},{angle}'.
                    format(**pdict).split(',')
                    )

            elif words[0] == 'C':
                # C posx posy radius unit convert thickness fill
                keys = ('type','posx','posy','radius','unit','convert','thickness','fill')
                pdict = { k:v for (k,v) in zip(keys, words)}
                
                pdict['radius'] = float(pdict['radius'])/10.0
                # posx, posy = centre of the circle
                # radius = radius of the circle
                geoms.append(
                'CircleC,{posx},{posy},{radius}'.
                    format(**pdict).split(',')
                    )
            elif words[0] == 'T':
                pass
            elif words[0] == 'S':
                # S startx starty endx endy unit convert thickness fill
                keys = ('type','startx','starty','endx','endy','unit','convert','thickness','fill')
                pdict = { k:v for (k,v) in zip(keys, words)}
                
                # startx, starty = Starting corner of the rectangle
                # endx, endy = End corner of the rectangle
                geoms.append(
                'Polyline,{startx},{starty},{endx},{starty},{endx},{endy},{startx},{endy},{startx},{starty}'.
                    format(**pdict).split(',')
                    )
                    
        return geoms
        
################## END OF COMMANDS CLASS ###########################
            
    #modules copy GetReference call .*EF.* regex isnotnone filter Reference call false SetVisible callargs
    #modules *.EF.* regexref refobj clearvisible
    #'help': Command(0,lambda c: HELPMAIN(),'Help', "Shows general help"),
    
commands.classinstance = commands()

# Add commands from commands class
# added for python3: "not x.startswith('__') and "
for c in filter(lambda x: not x.startswith('__') and hasattr(getattr(commands,x), '__call__'),dir(commands)):
    f = getattr(commands.classinstance,c)
    if hasattr(f,'category'):
        _dictionary['command'][c.lower()] = Command(f.nargs,f,f.category,f.__doc__)
    else:
        # Format of comment is: 'Category [ARGUMENT1 ARGUMENT2] Description'
        # from beginning, Search for first letter, then first space
        # Extract and trim, then split on ',' for classes
        # from the space, find first non space.
        # If character is '[' then search for first ']'.
        # Extract for arguments, trim, then split on ' '
        # after ']' find first space then first nonspace.
        # The remainder of the line is description
        nargs = 0
        category, doc = f.__doc__.split(' ', 1)
        if doc[0] == '[':
            arg = doc[1:].split(']',1)[0].split()
            if arg:
                nargs = len(arg)
            # print(c,':',arg)
        # else:
            # print(c,':',numarg)
            
        doc = decodestring(inspect.cleandoc(' '.join(doc.split())))
        _dictionary['command'][c.lower()] = Command(nargs,f,category,doc)


def LESSTHAN(*c):
    if isiter(c[0]):
        if isiter(c[1]):
            return itertools.starmap(operator.lt,itertools.izip(c[0],c[1]))
        else:
            return map(lambda x: float(x)<float(c[1]),c[0])
    else:
        if isiter(c[1]):
            return map(lambda x: float(x)>float(c[0]),c[1])
        else:
            return float(c[1])>float(c[0])

def rotate_point(point,center,angle,ccw=True):
    # try:
        # center=center[0]
    # except:
        # pass
    # output( 'pca: ',point,center,angle)
    #return None
    if ccw:
        mult = -1
    else:
        mult = 1
    radians = mult*float(angle)*math.pi/180.0
    radians = mult*float(angle)*math.pi/180.0
    if not isinstance(point,pcbnew.wxPoint):
        point = pcbnew.wxPoint(point[0],point[1]) 
    if not isinstance(center,pcbnew.wxPoint):
        center = pcbnew.wxPoint(center[0],center[1])
    s = math.sin(radians)
    c = math.cos(radians)
    point = point - center
    # output( point)
    point =  pcbnew.wxPoint(point[0]*c - point[1]*s,point[0]*s + point[1]*c)
    point = point + center
    # output('rotated ',str(point))
    return point
    
def ROTATEPOINTS(points,center,angle):
    # output( 'c1: ',center, points)
    center = convert_to_points(center)[0]
    points = convert_to_points(points)
    if not hasattr(angle,'__iter__'):
        angle = [angle]
    # for ps,c in zip(points, cycle(center)):
        # newp = [rotate_point(p,c,float(angle)) for p in ps ]
    newps = []
    # output( 'cpsa: ',center,points, angle)
    for ps,c,a in zip(points, cycle(center),cycle(angle)):
        newps.append([rotate_point(p,c,float(a)) for p in ps])

    # output( 'c2:',center, points)
    return newps

def REMOVE(items):
    if not hasattr(items,'__iter__'):
        items = [items]
    b = getBoard()
    d=b.GetDrawings().Remove
    t=b.GetTracks().Remove
    m=b.GetModules().Remove
    access = ((pcbnew.TRACK,t),(pcbnew.MODULE,m),(object,d))    
    for item in items:
        for inst,remove in access:
            #output(str(inst),str(remove))
            if isinstance(item,inst):
                remove(item)
                break

    
def TOCOPPER(*c):
    objects,layer = c
    board = getBoard()
    layerID = getLayerID(layer)
        
    for object in objects:
        track = pcbnew.TRACK(board)
        track.SetStart(object.GetStart())
        track.SetEnd(object.GetEnd())
        track.SetWidth(object.GetWidth())
        track.SetLayer(layerID)

        board.Add(track)
    
def CORNERS(c):
    if (not hasattr(c,'__iter__')) and \
        ((hasattr(c,'GetSize') and hasattr(c,'GetCenter')) or \
         isinstance(c,pcbnew.EDA_RECT) or \
         isinstance(c[0],pcbnew.wxPoint)):
        rects = [c]
    else:
        rects = c

    
    aggregate = []
    for r in rects:
        if hasattr(r,'GetCenter') and hasattr(r,'GetSize'):
            ns = pcbnew.wxPoint(r.GetSize()[0]/2.0,r.GetSize()[1]/2.0)
            aggregate.append(pcbnew.EDA_RECT(r.GetCenter()-ns,r.GetSize()))
        elif hasattr(r,'GetBoundingBox'):
            aggregate.append(r.GetBoundingBox())
        else:
            aggregate.append(r)
    rects = aggregate
    #rects = [r.GetBoundingBox() if hasattr(r,'GetBoundingBox') else r for r in rects]

    # rect = [c[0]] \
    # if isinstance(c[0],pcbnew.EDA_RECT) else map(lambda x: x.GetBoundingBox(),c[0]) \
    # if hasattr(c[0],'__iter__') else [c[0].GetBoundingBox()]
    xyvals = []
    for poly in rects:
        if isinstance(poly,pcbnew.EDA_RECT):
            l,r,t,b = poly.GetLeft(),poly.GetRight(),poly.GetTop(),poly.GetBottom()
            xyvals.append((l,t,r,t,r,b,l,b,l,t))
        #elif isinstance(poly[0],pcbnew.wxPoint):
    return xyvals
def CORNERS_old(c):
    if (not hasattr(c,'__iter__')) and \
        (hasattr(c,'GetBoundingBox') or \
         isinstance(c,pcbnew.EDA_RECT) or \
         isinstance(c[0],pcbnew.wxPoint)):
        rects = [c]
    else:
        rects = c

    
    aggregate = []
    for r in rects:
        if hasattr(r,'GetBoundingBox'):
            aggregate.append(r.GetBoundingBox())
        else:
            aggregate.append(r)
    rects = aggregate
    #rects = [r.GetBoundingBox() if hasattr(r,'GetBoundingBox') else r for r in rects]

    # rect = [c[0]] \
    # if isinstance(c[0],pcbnew.EDA_RECT) else map(lambda x: x.GetBoundingBox(),c[0]) \
    # if hasattr(c[0],'__iter__') else [c[0].GetBoundingBox()]
    xyvals = []
    for poly in rects:
        if isinstance(poly,pcbnew.EDA_RECT):
            l,r,t,b = poly.GetLeft(),poly.GetRight(),poly.GetTop(),poly.GetBottom()
            xyvals.append((l,t,r,t,r,b,l,b,l,t))
        #elif isinstance(poly[0],pcbnew.wxPoint):
    return xyvals


def SAVE(name):
    dictname = 'user'
    if not os.path.exists(USERSAVEPATH):
        os.makedirs(USERSAVEPATH)
        output('created '%USERSAVEPATH)#~/kicad/kicommand')
    output("saving to %s"%name)
    new_path = os.path.join(USERSAVEPATH, name)
    with open(new_path,'w') as f:
        commands = _dictionary[dictname].iteritems()
        for command,definition in sorted(commands,key=lambda x:x[0]):
            f.write(str(_dictionary[dictname][command]))
            f.write('\n')

def EXPLAIN(commandstring,category=None):
    output('Explaining',commandstring)
    commands = commandstring.split(',')
    commands.reverse()
    printed = set()
    count = 0
    while commands:
        count += 1
        if count > 100:
            output('explain command has an output limit of 100 commands.')
            break
        command = commands.pop()
        if not command:
            continue
        if command in printed:
            output(('%s (see explanation above)'%(command)))
            continue
        else:
            found = None
            printed.add(command)
            for dictname in ['user','persist']:
                #output( '\n',dictname,'Dictionary')
                if command in _dictionary[dictname]:
                    found = _dictionary[dictname][command]
                    if isinstance(found,basestring):
                        found = found.split()
                        output( ': %s %s ;'%(command,' '.join(found)))
                        found.reverse()
                        commands.extend(found)
                    else:
                        print_command_detail(command)
                    break;
            if not found:
                if not print_command_detail(command):
                    output( '%s - A literal value (argument)'%command)
                # HELP(command,exact=True)
            else:
                printed.add(command)

def HELPALL():
    sorted = list(_dictionary['command'].keys())
    sorted.sort()
    for command in sorted:
        print_command_detail(command)
        
def print_command_detail(command):
    for dictname in ('user','persist','command'):
        v = _dictionary[dictname].get(command,None)
        if v:
            break
    if not v:
        return False
    # if isinstance(command,basestring):
        # return False
    output(('%s (Category: %s)'%(command,v.category)))
    helptext = v.helptext
    seealso = ''
    if helptext:
        seealso = v.helptext.split()[-1].split(',')
    if len(seealso) > 1:
        seealso = '\n\n\tSEE ALSO: {}'.format(', '.join([x for x in seealso if x]))
        helptext = helptext[0:helptext.rindex(' ')]
    else:
        seealso = ''
    helptext += seealso
    output(('\t%s'%'\n'.join(['\n\t'.join(wrap(block, width=60)) for block in helptext.splitlines()])))
    return True

#def getcommand(command):
def HELPMAIN():
    helptext = ' '.join("""
    KiCommand gives you quick access to objects in pcbnew for manipulation or information.
    Enter arguments (if any) prior to commands and use previous results for succeeding commands.
    Simple commands allow you to create useful command strings. For more information,
    use one of the following commands in the Help category:""".split())
    output(('\t%s'%'\n'.join(['\n\t'.join(wrap(block, width=60)) for block in helptext.splitlines()])))
    output( 'All helpcat - For a list of all commands by category.')
    output( "'COMMAND explain - For help on a specific COMMAND (be sure to include the single quote).")
    output("helpall - for detailed help on all commands.")
    output()
    
    commands = 'helpcat explain helpall'.split()
    # commands = filter(lambda c: c[1].category == 'Help', _dictionary['command'].iteritems())
    # commands = [command[0] for command in commands]
    # commands.sort()
    for command in commands:
        print_command_detail(command)

def HELPCAT(category):

    uniondict = {}
    commands = []
    
    for dictname in ('user','persist','command'):        
        uniondict.update(_dictionary[dictname])

    if category == 'Core':
        commands = _dictionary ['command'].iteritems()
    elif category == 'All':
        commands = uniondict.iteritems()
        
    if commands:
        cbyc = defaultdict(list)
        for command in commands:
            #print(command[1])
            try:
                catlist = command[1].category.split(',')
            except:
                catlist = command[1].category
            for cat in catlist:
                cbyc[cat].append(command[0])
        catlen = max(map(len,cbyc.keys()))
        #output( format('{'+str(catlen)+'} - {}','CATEGORY'))
        #output( 'CATEGORY   -   COMMANDS IN THIS CATEGORY')
        output( '{:<{width}} - {}'.format('CATEGORY','COMMANDS IN THIS CATEGORY', width=catlen))
        for cat in sorted(cbyc.keys()):
            output( '{:<{width}} - {}'.format(cat,' '.join(sorted(cbyc[cat])), width=catlen))
        return
    # list(set(list1).intersection(list2))    
    try:
        catset = set(category.split(','))
    except:
        catset = set(category)
        
    commands = filter(lambda c: hasattr(c[1],'category') and catset.intersection(c[1].category.split(',') if hasattr(c[1].category,'split') else c[1].category), uniondict.iteritems())
    commands = [command[0] for command in commands]
    commands.sort()
    for command in commands:
        print_command_detail(command)
            
def safe_float(value):
    try:
        return float(value)
    except:
        return value
def safe_round(value,n=0):
    try:
        return round(float(value),n) # convert to float to catch the case where input is string float value
    except:
        return value
def safe_int(value):
    try:
        return int(float(value)) # convert to float to catch the case where input is string float value
    except:
        return value
def multiplynoerror(value,multiplier):
    try:
        f = float(value)
    except:
        return value
    return f*multiplier
    
def HELP(textlist,category=None,exact=False):
    # if text contains a space, it is interpreted as 
    # a list of space-separated commands and arguments.
    # Each command in the space-separated string should
    # be listed in order, and unknown strings listed as
    # arguments prior to the next known command.
    
    # allow detail input to be a list of comma separated commands
    
    if isinstance(textlist,basestring):
        textlist = [textlist]
    for text in textlist:
        textspace = text.split()
        if len(textspace) > 1:
            # here, text is a space-separated command sequence
            # in textspace list
            # each command should look for exact match. If not found,
            # hold as argument.
            pass
        else:
            # here, textspace[0] is comma separated list of keywords
            # if there is only one item in the list, use find, otherwise exact.
            pass
        if text.find(' '):
            pass
        #text=text.lower()
        if category == 'All':
            foundkv = _dictionary ['command'].iteritems()
            command_by_category = defaultdict(list) #{}
            for command,val in _dictionary ['command'].iteritems():
                #command_by_category.setdefault(val.category,[]).append(command)
                command_by_category[val.category].append(command)
                
            for category,commands in sorted(command_by_category.iteritems(),key=lambda x:x[0]):
                output('%11s: %s\n'%(category,' '.join(commands))),
            return
            # foundkv = sorted(foundkv,key=lambda x: x[1].category)
            # foundkv = filter(lambda x: x[2].find(text)!=-1,_dictionary['command'].iteritems())
        
        if text:
            if exact:
                foundkv = text,_dictionary['command'].get(text,None)
            else:
                foundkv = filter(lambda x: x[0].find(text)!=-1,_dictionary['command'].iteritems())
        else:
            foundkv = _dictionary['command'].iteritems()
        #output( 'foundkv = ',foundkv)
        if not foundkv or not foundkv[1]:
            continue
        foundkv = sorted(foundkv,key=lambda x: x[0])
        for commandandvalue in foundkv:
            output( commandandvalue)
            #print_command_detail(k)
            # output('%s (Category: %s)'%(k,v.category))
            # output('\t%s'%'\n'.join(['\n\t'.join(wrap(block, width=60)) for block in v.helptext.splitlines()]))
        
        #'\n'.join(['\n'.join(wrap(block, width=50)) for block in text.splitlines()])


def isiter(object):
    return hasattr(object,'__iter__') and not isinstance(object,basestring)

def safe_multiply(a,b):
    try:
        return float(a)*float(b)
    except:
        return a
def safe_add(a,b):
    try:
        return float(a)+float(b)
    except:
        return a
def safe_subtract(a,b):
    try:
        return float(a)-float(b)
    except:
        return a
def safe_divide(a,b):
    try:
        return float(a)/float(b)
    except:
        return a

# params is extended to set other various parameters
# t - Thickness of a drawsegment or track, this is commonly referred to as "width"
# w - Width of text
# h - Height of text
# l - Layer for drawing
# zt - ZoneType, one of NO_HATCH, DIAGONAL_FULL, or DIAGONAL_EDGE
# zp - ZonePriority
# debug - an integer indicating the debug level, 0 - 5 where 0 is no debug
# arcerror - integer in native units of the minimum error when converting an arc into line segments
# arcerrorradius   - a float between 0.0 and 1.0 indicating, as a fraction of radius, the maximum error when turning an arc into segments 
# beziersteps   - the integer number of steps for turning a bezier curve into segments.

# params are held by the UserStack as a list (which can be considered a stack itself)
# that contains a dictionary keyed by parameter name.
    
# Add more command definitions
_dictionary['command'].update({
    # PCB Elements
    # ': board pcbnew GetBoard call ;'
    # ': modules board GetModules call ;'
    # ': pads board GetPads call ;'
    # ': tracks board GetTracks call ;'
    # ': drawings board GetDrawings call ;'
    # ': board GetDrawings call ;'
    
    # ': selected IsSelected callfilter ;'
    # ': notselected IsSelected callnotfilter ;'
    # ': setselected SetSelected call ;'
    # ': clearselected ClearSelected call ;'
    # ': getstart GetStart call ;'
    # ': getend GetEnd call ;'
    # ': copytop 0 pick ;'
    
    
    'pcbnew': Command(0,lambda c: pcbnew,'Python',
        'Get the python base object for PCBNEW'),
    'getboard': Command(0,lambda c: pcbnew.GetBoard(),'Elements',
        'Get the loaded Board object (execute pcbnew.GetBoard()).'),
    # boardpush can be done with "[BOARD Object] Board spush"
    # boardpop can be done with "Board spop"
    # 'boardpush': Command(1,lambda c: _user_stacks['Board'].append(c[0]),'Elements',
        # '[BOARD] Add board to Board stack. This is the new default Board object for many commands'),
    # 'boardpop': Command(0,lambda c: _user_stacks['Board'].pop(),'Elements',
        # 'Remove last board from Board stack and place on the stack. The previous default board becomes the new default Board object for many commands'),
    'board': Command(0,lambda c: getBoard(),'ElementsCore',
        'Get the default Board object for many commands'),
    'modules': Command(0,lambda c: getBoard().GetModules(),'ElementsCore',
        'Get all modules of the default board'),
    'tracks': Command(0,lambda c: getBoard().GetTracks(),'ElementsCore',
        'Get all tracks (including vias) of the default board'),
    'drawings': Command(0,lambda c: getBoard().GetDrawings(),'ElementsCore',
        'Get all top-level drawing objects (lines and text) of the default board'),
#    'toptext': Command(0,lambda c: filter(lambda x: isinstance(x,pcbnew.EDA_TEXT),getBoard().GetDrawings()),'Elements'),
# 'copy IsSelected call filter'
    # PCB Element Attributes
    'selected': Command(1,lambda c: filter(lambda x: x.IsSelected(), c[0]),'Filter',
        '[objects] Get selected objects '),
    'notselected': Command(1,lambda c: filter(lambda x: not x.IsSelected(), c[0]),'Filter',
        '[objects] Get unselected objects '),
    'attr': Command(2,lambda c: map(lambda x: getattr(x,c[1]), c[0]),'Python',
        '[OBJECTSLIST ATTRIBUTE] Get specified python attribute of the objects. attr.,' ),
    'attr.': Command(2,lambda c: map(lambda y: map(lambda x: getattr(x,c[1]),y), c[0]),'Python',
        '[OBJECTLISTOFLISTS ATTRIBUTE] Get specified python attribute of the objects with the LISTOFLISTS. attr,' ),
    # want this to work where c[1] is a value or list. If list, then member by member.
    #'index': Command(2,lambda c: map(lambda x: x[c[1]], c[0]),'Attributes',
    'sindex': Command(2,lambda c: c[0][c[1]] if isinstance(c[1], collections.Hashable) else map(lambda x: c[0][x],c[1]) ,'Python',
       '[DICTIONARYOBJECT STRINGINDEX] Select an item in the list of objects based on string INDEX. Also works with a STRINGINDEX_LIST, in which case a list is returned.'),

    'index.': Command(2, lambda c: map(lambda x: x[int(c[1])],c[0]), 'Conversion',
        '[LISTOFLISTS INDEX] return a list made up of the INDEX item of each list in LISTOFLISTS'),
    'indexx': Command(2, lambda c: reduce(lambda a,b: a[b],c[1],c[0]), 'Conversion',
        '[LISTOFLISTS INDEXLIST] takes each successive index in the index list and gets each index individually. index must be the proper type (integer for lists). For example, [5,6,7] will get the 7th element of the 6th element of the 5th element of the "top" list.'),
    'replace': Command(2, lambda c: operator.setitem(reduce(lambda a,b: a[b],c[0][:-1],_stack[-3]),c[0][-1],c[1]), 'Conversion',
        '[LISTOFLISTS INDEXLIST VALUE] takes the successive index in the index list and gets each index individually. index must be the proper type (integer for lists). For example, [5,6,7] will get the 7th element of the 6th element of the 5th element of the "top" list.'),
        # operator.setitem(array,index,value)
        # Noto-sans-cjk-jp-thin setfont \u00d8 stringtogeom pprint 3,0 int Hole replace
    
        # _stack[-1]
    'index': Command(2,
                       lambda c: c[0][int(c[1])] if isinstance(c[1],basestring) \
                       and c[1].find(',') == -1 else map(lambda x: x[0][int(x[1])],
                       zip(c[0], cycle(c[1].split(','))
                       if isinstance(c[1],basestring) else c[1]
                       )),
                       
                       #if hasattr(c[0],'__iter__') else [c[1]]),
                       
                       # lambda c: map(lambda x: x[0][x[1]],
                       # c[0].split(',')
                       # if isinstance(c[0],basestring) else c[0]
                       # if hasattr(c[0],'__iter__') else [c[0]]),
                       'Programming',
        '[LIST INDEX] Select an item in the list of objects based on numeric index. '
        'If INDEX is a list of integers or a comma separated list of numbers, then '
        'each number in INDEX will be applied to the corresponding item in the LIST of '
        'lists, where the INDEX list is repeated or truncated as necessary.'
        ),
        
    # PCB Actions
    'connect': Command(1,lambda c: CONNECT(*c),'Action',
        'Using selected lines, connect all vertices to each closest one.'),
    # Filter
    'length': Command(1, lambda c: LENGTH(*c),'Geometry',
        '[SEGMENTLIST] Get the length of each segment (works with '
        'segment and arc types'),
    'setlength': Command(2, lambda c: SETLENGTH(*c),'Geometry',
        '[SEGMENTLIST LENGTH] Set the length of each segment. Move connected segments accordingly.'),
    'ends': Command(1, lambda c: [get_ds_ends(seg) for seg in c[0]] if hasattr(c[0],'__iter__') else get_ds_ends(*c),'Geometry',
        'Get the end points of the drawsegment (works with segment and arc types'),
    'connected': Command(2,lambda c: CONNECTED(*c),'Filter',
        '[WHOLE INITIAL] From objects in WHOLE, return those that are connected to objects in INITIAL (recursevely)'),
    'matchreference': Command(2,lambda c: filter(lambda x: x.GetReference() in c[1].split(','), c[0]),'Filter',
        '[MODULES REFERENCE] Filter the MODULES and retain only those that match REFERENCE. Note that REFERENCE can be a comma-separated list of names. If there is an embedded comma in a name, use filterrefregex instead.'),
    
    'extend': Command(2,lambda c: c[0].extend(c[1]) or c[0],'Stack',
        '[LIST1 LIST2] Join LIST1 and LIST2. append,concat'),
        
    'filter': Command(2,lambda c: list(compress(c[0], c[1])),'Filter', # filter op1 by bool op2
        '[LIST1 TF_LIST] Retain objects in LIST1 where the corresponding value in TF_LIST is True, not None, not zero, and not zero length'),
    #'<': Command(2,lambda c: [c[0][i] for i,x in enumerate(c[1]) if x<float(c[2]))
    '<': Command(2,lambda c: LESSTHAN(*c),'Comparison',
        '[VALUES1 VALUES2] Returns boolean value of VALUES1 < VALUES2. If either is a list, the result is a list. If both are a list, the result is an element by element comparison. (for use prior to FILTER).'),

# cycletocount(c[0],max(len(c[0]),len(c[1])))
# cycletocount(c[1],max(len(c[0]),len(c[1])))
# def cycletocount(iterable,count):
    # return itertools.islice(itertools.cycle(iterable), 0, count, 1)
     
    'filtertype': Command(2,lambda c: filter(lambda x:isinstance(x,getattr(pcbnew,c[1])),c[0]),'Filter',
        '[LIST TYPE] Retains objects in LIST that are of TYPE' ),
    'istype': Command(2,lambda c: map(lambda x:isinstance(x,getattr(pcbnew,c[1])),c[0]),'Comparison',
        '[LIST TYPE] Create a LIST of True/False values corresponding to whether '
        'the values in LIST are of TYPE (for use prior to FILTER). '
        'TYPE must be an attribute of pcbnew.' ),
    '=': Command(2,lambda c: map(lambda x: x==c[1],c[0])if hasattr(c[0],'__iter__') and not isinstance(c[0],basestring) else c[1]==c[0],'Comparison',
    
        '[LIST VALUE] Create a LIST of True/False values corresponding to whether the values in LIST equal to VALUE (for use prior to FILTER)'),
    'isnone': Command(1,lambda c: map(lambda x: x is None,c[0]),'Comparison',
        '[LIST VALUE] Create a LIST of True/False values corresponding to whether the values in LIST equal to None (for use prior to FILTER)'),
    'isnotnone': Command(1,lambda c: map(lambda x: x is not None,c[0]),'Comparison',
        '[LIST VALUE] Create a LIST of True/False values corresponding to whether the values in LIST is not  None (for use prior to FILTER)'),
#x=lambda c: map(lambda x: float(x),c.split(',')) if isinstance(c,basestring) else map(lambda x: float(x),c)
    'undock': Command(0,lambda c: UNDOCK(*c),'System',
        'Undock the window.'),
    'spush': Command(2,lambda c: _user_stacks[c[1]].append(c[0]),'StackUser',
        '[STACK] [VALUE] Push VALUE onto the named STACK. spop,sdelete,scopy,scopyall'),
    'spop': Command(1,lambda c: _user_stacks[c[0]].pop() if len(_user_stacks[c[0]])>1 else _user_stacks[c[0]],'StackUser',
        '[STACK] Pop the top of the user STACK onto the main stack only if stack contains more than 1 item. spush,sdelete,scopy,scopyall'),
    'sdelete': Command(1,lambda c: _user_stacks.pop(c[0],None) and None,'StackUser',
        '[STACK] Delete the user stack. spush,spop,scopy,scopyall'),
    'scopy': Command(1,lambda c: _user_stacks[c[0]][-1],'StackUser',
        '[STACK] Copy the top of the user STACK onto the main stack. spush,spop,sdelete,scopyall'),
    'scopyall': Command(1,lambda c: _user_stacks[c[0]],'StackUser',
        '[STACK] Copy the entire user STACK as a list onto the main stack. spush,sdelete,scopy,spop'),
    'stack': Command(0,lambda c: STACK(*c),'Output',
        'Output the string representation of each object on the stack'),
    'print': Command(0,lambda c: PRINT(*c),'Output',
        'Output the string representation of the top object on the stack'),
    'pprint': Command(0,lambda c: PPRINT(*c),'Output',
        'Pretty print the string representation of the top object on the stack'),
    'builtins': Command(0,lambda c:  __builtins__,'Programming,Python',
        """Output the __builtins__ Python object, giving access to the built in Python functions.\n
        Example: builtins pow sindex list 2,3 float list fcallargs sindex,fcallargs"""),
    
    # 'getstart': Command(1,lambda c: [m.GetStart() for m in c[0]],'Python',
        # '[LIST] Get the start wxPoint from the LIST of DRAWSEGMENTS.'),
    # 'getend': Command(1,lambda c: [m.GetEnd() for m in c[0]],'Python',
        # '[LIST] Get the end wxPoint from the LIST of DRAWSEGMENTS.'),
    'calllist': Command(2,lambda c: CALLLIST(*c),'Python',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. '
        'The FUNCTION must return a list of items (this is suitable '
        'for module functions such as GraphicalItems and Pads. '
        'This is similar to call followed by flatlist. call,flatlist') ,
    'fcall': Command(1,lambda c: map(lambda x: x(), c[0]),'Python',
        '[FUNCTIONLIST] Execute each python function in the FUNCTIONLIST on each member of LIST. Return the list of results in the same order as the original LIST. '
        'fcall differs from call in that call assumes the function is a attribute of the object identified by the named function (string), '
        'whereas fcall assumes the function is a an actual Python function object. They also handle list arguments differently.'),
    'fcallargs': Command(2,
                lambda c: 
                map(lambda x: 
                        x[0](*(x[1])), 
                        #itertools.islice(zip(itertools.cycle(c[0]),itertools.cycle(c[1])),max(len(c[0]),len(c[1])))
                        itertools.islice(itertools.izip(itertools.cycle(c[0]),itertools.cycle(c[1])),max(len(c[0]),len(c[1])))
                        # zip(c[0], cycle(c[1]))
                   )
                ,'Python',
                # islice(seq,start,stop)
                # itertools.islice(zip(cycle(c[0]),cycle(c[1])),0,max(len(c[0],c[1])))
        '[FUNCTIONLIST ARGLISTOFLISTS] Execute each python function in the '
        'FUNCTIONLIST on each member of that list with arguments in ARGLISTOFLISTS. '
        'ARGLISTOFLISTS can be '
        'a different length than FUNCTIONLIST, in which case the short list of the two '
        'will be repeated to match the length of '
        'the longer. Returns the list of results in the same order as the '
        'original OBJECTLIST. The commands LIST and ZIP2 might be helpful '
        'here. '
        'fcallargs differs from callargs in that "call" assumes the function is a attribute of the object identified by the named function (string), '
        'whereas fcall assumes the function is a an actual Python function object. They also handle list arguments differently. list,zip,zip2,callargs'),
 
    
    'calld': Command(2,lambda c: map(lambda x: getattr(c[0],x)(), c[1]) if isiter(c[1]) else getattr(c[0],c[1])()
        ,'Python',
        '[OBJECT FUNCTION_OR_LIST] Call direct. Execute python FUNCTION on OBJECT. Do not interpret the object as an iterable. '
        'This is useful when OBJECT is an iterable and you want to call a function on the iterable itself '
        '(such as calling keys or values on a dictionary). '
        'Return either a single result or the list of results in the same order as '
        'the original FUNCTION list. call,callargs,split'),
    # 'call': Command(2,lambda c: map(lambda x: getattr(x,c[1])(), c[0]) if isiter(c[0]) else getattr(c[0],c[1])()
        # # if hasattr(c[0],'__getitem__') and hasattr(c[0][0],'__getitem__') else 
        # # map(lambda x: getattr(x,c[1])(), [c[0]])
        # # if hasattr(c[0],'__getitem__') else  
        # # map(lambda x: getattr(x,c[1])(), [[c[0]]])
        # ,'Python',
        # '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Return the list of results in the same order as the original LIST.'),
    'callfilter': Command(2,lambda c: filter(lambda x: getattr(x,c[1])(), c[0]),'Python',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Return results that return True.'),
    'callnotfilter': Command(2,lambda c: filter(lambda x: not getattr(x,c[1])(), c[0]),'Python',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Return results that return False.'),
    # 'callargs': Command(3,
                # lambda c: 
                # map(lambda x: 
                        # getattr(x[0],c[2])(*(x[1])), 
                        # zip(c[0], cycle(c[1]))
                   # )
                # ,'Python',
                # #        zip(c[0],c[1][0:len(c[0])])
                # # itertools.zip(c[0], itertools.cycle(c[1]))
                # #list(itertools.zip([1,2,3], itertools.cycle([4,5])))
        # '[OBJECTLIST ARGLISTOFLISTS FUNCTION] Execute python FUNCTION on each member '
        # 'of OBJECTLIST with arguments in ARGLISTOFLISTS. ARGLISTOFLISTS can be '
        # 'a different length than OBJECTLIST, in which case ARGLISTOFLISTS '
        # 'elements will be repeated (or truncated) to match the length of '
        # 'OBJECTLIST. Returns the list of results in the same order as the '
        # 'original OBJECTLIST. The commands LIST and ZIP2 will be helpful '
        # 'here.'),
    # Move all module's Value text to Dwgs.User layer
    # r('modules Value call Dwgs.User layernums list SetLayer callargs')
    # Move only selected module's Value text to Dwgs.User layer
    # r('modules selected Value call Dwgs.User layernums list SetLayer callargs')
    # Numeric
    
    # Outline all module text objects, including value and reference.
    # r('clear referencetextobj valuetextobj moduletextobj append append copy GetTextBox call corners swap copy GetCenter call swap copy GetParent call Cast call GetOrientationDegrees call swap GetTextAngleDegrees call +l rotatepoints drawsegments')
    # # Outline the pads. Might be a problem with "bounding box" being orthogonal when pad is rotated.
    # r('clear pads copy GetBoundingBox call corners swap copy GetCenter call swap GetOrientationDegrees call rotatepoints drawsegments')
    '+.': Command(2,lambda c:
            [safe_add(a,b) for a,b in zip(c[0], cycle(c[1]))],'Numeric',
        '[LIST1 LIST2] Return the the floating point LIST1 + LIST2 member by member.'),
    '*.': Command(2,lambda c:
            [safe_multiply(a,b) for a,b in zip(c[0], cycle(c[1]))],'Numeric',
        '[LIST1 LIST2] Return the the floating point LIST1 * LIST2 member by member.'),
        
    '+': Command(2,lambda c:
            safe_add(c[0],c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 + OPERAND2.'),
        # safe_float(c[0]) if str and not ','
    # 'a': Command(2,
                       # lambda c: safe_float(c[0]) if isinstance(c[0],basestring) \
                       # and c[0].find(',') == -1 else map(lambda x: safe_float(x),
                       # c[0].split(',')
                       # if isinstance(c[0],basestring) else c[0]
                       # if hasattr(c[0],'__iter__') else [c[0]]),
                       # 'Conversion',
        # '[OBJECT] Return OBJECT as a floating point value or list. OBJECT can '
        # 'be a string, a comma separated list of values, a list of strings, or '
        # 'list of numbers.', ),
    '-': Command(2,lambda c: safe_subtract(c[0],c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 - OPERAND2.'),
    '*': Command(2,lambda c: safe_multiply(c[0],c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 * OPERAND2.'),
    '/': Command(2,lambda c: safe_divide(c[0],c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 / OPERAND2.'),
    'sum': Command(1, lambda c: sum(*c), 'Numeric', 
        '[LIST] Return the sum of all members in LIST.'), 
    
    # 'sum': Command(1,
       # lambda c: safe_float(c[0]) if isinstance(c[0],basestring) \
       # and c[0].find(',') == -1 else sum(map(lambda x: safe_float(x),
       # c[0].split(','))
       # if isinstance(c[0],basestring) else sum(c[0])) 
       # if hasattr(c[0],'__iter__') else safe_float(c[0]),

    # 'Numeric',
        # '[LIST] Return the sum of all members in LIST.'),

    # Stack Manipulation
    'concat': Command(2,lambda c: c[0]+c[1],'Stack',
        '[LIST1 LIST2] Return LIST1 and LIST2 concatenated together. append,extend'),
    'append': Command(2,lambda c: c[0].append(c[1]) or c[0],'Stack',
        '[LIST ITEM] Add ITEM to the end of LIST. If ITEM is a list, then it is added as a list. Use concat or extend for other options. extend,concat'),
    #'copytop': Command(0,lambda c: list(_stack[-1])),
    # 'copytop': Command(0,lambda c: _stack[-1],'Stack',
        # 'Duplicate the top object on the stack.'),
    'clear': Command(0,lambda c: CLEAR(*c),'Stack',
        'Clear the stack.'),
    # Conversion
    #'float': Command(1,lambda c: float(c[0]),'Conversion'),
    # Handles string, comma sep string, float, list of anything convertable
    # old version of float:
    # 'float': Command(1,
                       # lambda c: map(lambda x: float(x),
                       # c[0].split(',')
                       # if isinstance(c[0],basestring) else c[0]
                       # if hasattr(c[0],'__iter__') else [c[0]]),
    'float': Command(1,
                       lambda c: safe_float(c[0]) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: safe_float(x),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list. OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.', ),
    'roundint': Command(1,
                       lambda c: safe_round(c[0]) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: safe_round(x),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a rounded floating point value or list. OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.', ),
    'roundn': Command(2,
                       lambda c: safe_round(c[0],n=int(c[1])) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: safe_round(x,n=int(c[1])),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT N] Return OBJECT as a floating point value or list each member rounded to N number of decimals. '
        'OBJECT can be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.', ),
    'bool': Command(1,
    # if basestring and has ','
                       lambda c: bool(c[0]) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: bool(x),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a boolean value or list. OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of values.', ),
    'int': Command(1,
    # if basestring and has ','
                       lambda c: safe_int(c[0]) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: safe_int(x),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list. OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.', ),
    'string': Command(1,lambda c: str(c[0]),'Conversion',
        '[OBJECT] Convert OBJECT to a string.'),
    'dict': Command(2,lambda c: dict(zip(*c)),'Conversion',
        '[KEYS VALUES] Create a dictionary from KEYS and VALUES lists.'),
    #'mm': Command(1,lambda c: float(c[0])*pcbnew.IU_PER_MM,'Conversion'),
    'mm': Command(1,
                       lambda c: multiplynoerror(c[0],pcbnew.IU_PER_MM) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: multiplynoerror(x,pcbnew.IU_PER_MM),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list converted '
        'from mm to native units (nm). OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.'),
    'mil': Command(1,
                       lambda c: multiplynoerror(c[0],pcbnew.IU_PER_MILS) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: multiplynoerror(x,pcbnew.IU_PER_MILS),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list converted '
        'from mils to native units (nm). OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.'),
    'mils': Command(1,
                       lambda c: multiplynoerror(c[0],pcbnew.IU_PER_MILS) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: multiplynoerror(x,pcbnew.IU_PER_MILS),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list converted '
        'from mils to native units (nm). OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.'),
    'split': Command(1,lambda c: c[0].split(','),'Conversion',
        '[STRING] Split STRING on commas into a list of strings'),
    #'list': Command(1,lambda c: map(lambda x: [x],c[0]),'Conversion'),
    'iset': Command(1,lambda c: set(c[0]),'Conversion',
        '[ITERABLE] Make a set from ITERABLE where each item is a member of ITERABLE.'),
    'isstring': Command(1,lambda c: isinstance(c[0],basestring),'Conversion,Test',
        '[OBJECT] Return True if OBJECT is a string.'),
    'isiter': Command(1,lambda c: hasattr(c[0],'__iter__') and not isinstance(c[0],basestring),'Conversion,Test',
        '[OBJECT] Return True if OBJECT is an iterable (and not string). A list is iterable, for example'),
    'isint': Command(1,lambda c: isinstance(c[0],int),'Conversion,Test',
        '[OBJECT] Return True if OBJECT is an int.'),
    'isfloat': Command(1,lambda c: isinstance(c[0],float),'Conversion,Test',
        '[OBJECT] Return True if OBJECT is float.'),
    'ilist': Command(1,lambda c: list(c[0]),'Conversion,Test',
        '[ITERABLE] Make list from ITERABLE where each item is a member of ITERABLE.'),
    'list': Command(1,lambda c: [c[0]],'Conversion',
        '[OBJECT] Make OBJECT into a list (with only OBJECT in it).'),
    'list.': Command(1,lambda c: map(lambda x: [x],c[0]),'Conversion',
        '[LIST] Make each member of LIST into a list (with only that member in it).'),
    'delist': Command(1,lambda c: c[0][0],'Conversion',
        '[LIST] Output index 0 of LIST.'),
    'flatlist': Command(1,lambda c: [item for sublist in c[0] for item in sublist],'Conversion',
        '[LISTOFLISTS] Flatten the list of lists into a single-dimension list.'),


    #'swap': Command(2,retNone(lambda c: _stack[-1],_stack[-2]=_stack[-2],_stack[-1])),
    # 'pick': Command(1,lambda c: _stack.insert(-int(_stack[-1])-1,_stack[-2]),'Stack',
    #works: 'pick': Command(1,lambda c: _stack.insert(-1,_stack[len(_stack)-int(c[0])-2]),'Stack',
    'pick': Command(1,lambda c: _stack.insert(-1,_stack[-int(c[0])-2]),'Stack',
        '[NUMBER] Copy the value that is NUMBER of objects deep in the stack to the top of the stack. '
        '\n\tExamples:\n\t0 pick - copies the top of the stack.\n'
        '\t1 pick - pushes a copy of the second item from the top of the stack onto the top of the stack.\n copy,pull'
        ),
    'pull': Command(1,lambda c: _stack.insert(-1,_stack.pop(-int(c[0])-2)),'Stack',
        '[NUMBER] Move the value that is NUMBER of objects deep in the stack to the top of the stack. '
        '\n\tExamples:\n\t0 pull - moves the top of the stack, essentially a null operation.\n'
        '\t1 pull - moves  the second item from the top of the stack onto the top of the stack.\n copy,pick'
        ),
    'swap': Command(0,lambda c: SWAP(*c),'Stack',
        'Switches the two top objects on the stack.'),
    'zip2': Command(2,lambda c: zip(*c),'Stack',
        '[LIST1 LIST2] Creates a list with parallel objects in LIST1 and '
        'LIST2 together at the same index. zip,'),
    'zip': Command(1,lambda c: zip(*c[0]),'Stack',
        '[LISTOFLISTS] Creates a list with parallel objects formed by each list '
        'in LISTOFLISTS ((1,2,3)(4,5,6)(7,8,9)) -> ((1,4,7)(2,5,8)(3,6,9)). Note that zip is its own inverse. ,zip2'
        ),
    ':': Command(0,lambda c: setcompilemode(True),'Programming',
        'Begin the definition of a new command. This is the only command in '
        'which arguments occur after the command. Command definition ends with '
        'the semicolon (;). Run command SEEALL for more examples. Special commands are '
        "Delete all commands ': ;'. Delete a command ': COMMAND ;"
        ),
    # this is here only to provide help text. The main execution of '?' happens during parsing of command strings
    '?': Command(0,lambda c: None,'Programming',
        "?command will pop the stack and execute 'command' if True. "
        'The top of the stack is interpreted as a boolean, (see bool). '
        'Essentially this is a single-command-skip if False. '
        'To conditionally execute a series of command, define a new user command using the : command. '
        ":,;,true,false,bool"
        ),
    ':persist': Command(0,lambda c: setcompilemode(True,'persist'),'Programming',
        'Begin the definition of a new command in the persist dictionary. '
        'This is the only type of command in '
        'which arguments occur after the command. Command definition ends with '
        'the semicolon (;). Run command SEEALL for more examples.'
        ),
    
    'rotatepoints': Command(3,lambda c: ROTATEPOINTS(*c),'Geometry',
        '[POINTS CENTER DEGREES] Rotate POINTS around CENTER. POINTS can be in '
        'multiple formats such as EDA_RECT or a list of one or more points.'),
    'rotate': Command(2,lambda c: ROTATE(*c),'Geometry',
        '[SEGMENTLIST DEGREES] Rotate segments by DEGREES around the calculated '
        'average center.'),
        
    'corners': Command(1,lambda c: CORNERS(*c),'Geometry',
        "[OBJECT] OBJECT is either a single object or a list of objects. "
        "Converts each OBJECT, either EDA_RECT or OBJECT's BoundingBox "
        "into vertices appropriate for drawsegments."
        ),
    
    'tocopper': Command(2,lambda c: TOCOPPER(*c),'Layer',
        "[DRAWSEGMENTLIST LAYER] put each DRAWSEGMENT on the copper LAYER."),
    
    'layernums': Command(1,lambda c: [getLayerID(x) for x in c[0].split(',')],'Layer',
        '[STRING] Get the layer numbers for each layer in comma separated STRING. '
        'STRING can also be one number, if desired.'),
    'onlayers':  Command(2,lambda c: filter(lambda x: set(x.GetLayerSet().Seq()).intersection(set(c[1])),c[0]),'Layer',
        '[LIST LAYERIDS] Retains the objects in LIST that exist on any of the integer LAYERIDS. ,layernums'),
    'setlayer': Command(2,lambda c: map(lambda x: x.SetLayer(getLayerID(c[1])),
                          c[0] if hasattr(c[0],'__iter__') else list(c[0])), 'Layer',
        '[OBJECTS LAYER] Moves all OBJECTS to LAYER.'),
    'pop': Command(1,lambda c: None,'Stack',
        'Removes the top item on the stack.'),
    'see': Command(1,lambda c: print_userdict(*c),'Help',
        '[COMMAND] Shows previously-defined COMMAND from the user dictionary. '
        'See the colon (:) command for more information.'),
    'seeall': Command(0,lambda c: print_userdict(*c),'Help',
        '[COMMAND] Shows all previously-defined COMMANDs from the user dictionary. '
        'See the colon (:) command for more information.'),
    'now': Command(0,lambda c: time.asctime(),'System',
        'Returns the current system time as a string. Suitable for timestamping a pcb when converted to a text object.'),
    # 'createtext': Command(2,lambda c: )
    #def draw_arc(x1,y1,x2,y2,radius,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):

    'makeangle': Command(2,lambda c:MAKEANGLE(*c),'Draw',
        '[SEGMENTLIST ANGLE] Make the selected segments form '
        'the specified angle. arc radius is maintained, though angle and '
        'position are modified, while line segments are moved '
        'and stretched to be +/- n*angle specified.'),
    'regular': Command(1,lambda c:REGULAR(*c),'Draw',
        '[SEGMENTLIST] Move/stretch the selected segments into a regular '
        'polygon (equal length sides, equal angles).'),
    'grid': Command(2,lambda c:GRID(*c),'Draw',
        '[ITEMLIST GRID] Move points of ITEMLIST to be a multiple of GRID. Start/End points of segments/tracks are moved, and position of BOARD_ITEMs are moved to grid.'),
    'scale': Command(2,lambda c:SCALE(*c),'Draw',
        '[SEGMENTLIST FACTOR] Scale each item in SEGMENTLIST by FACTOR, using '
        'the midpoint of all segments as the center.'),
    'cut': Command(0,lambda c: CUT(*c),'Draw',
        'Cut all segments with the selected segment at the intersection. Then remove the cutting (selected) segment.'),
    'round': Command(2,lambda c: draw_arc_to_segments(*c),'Draw',
        '[RADIUS SEGMENTLIST] Round the corners of connected line segments '
        'within SEGMENTLIST by adding ARCs of specified RADIUS.'),
    'angle': Command(1,lambda c: ANGLE(*c),'Geometry',
        '[SEGMENTLIST] Return the angle of each segment in SEGMENTLIST.'),
    'drawarctest':Command(1,lambda c: draw_arc(50*pcbnew.IU_PER_MM,50*pcbnew.IU_PER_MM,radius,angle,layer=_user_stacks['Params'][-1]['l'],thickness=_user_stacks['Params'][-1]['t']),'Draw',
        ""),
    'drawarc':Command(2,lambda c: draw_arc(c[0][0],c[0][1],c[0][2],c[0][3],c[1],layer=_user_stacks['Params'][-1]['l'],thickness=_user_stacks['Params'][-1]['t']),'Draw',
        "[STARTX,STARTY,CENTERX,CENTERY DEGREES] Draw an arc with the given parameters. Layer and Thickness are taken from the draw parameters (see params command)"),
    'remove':Command(1,lambda c: REMOVE(*c),'Layer',
        '[OBJECTORLIST] remove items from board. Works with any items in Modules, Tracks, or Drawings.'),
    'tosegments':Command(2,lambda c: tosegments(*c),'Layer',
        '[LIST LAYER] copy tracks or point pairs in LIST to drawsegments on LAYER. Copies width of each track.'),
    'drawsegments':Command(1,lambda c: draw_segmentlist(c[0],layer=_user_stacks['Params'][-1]['l'],thickness=_user_stacks['Params'][-1]['t']),'Draw',
        "[POINTSLIST] Points list is interpreted as pairs of X/Y values. Line segments are"
        "drawn between all successive pairs of points, creating a connected sequence of lines "
        "where each point is a vertex in a polygon "
        "as opposed to being just a list of line segments or point pairs. "
        "This command uses previously set drawparams and the points are in native units (nm) so using mm or mils commands is suggested."),
    'drawtext': Command(2,lambda c: draw_text(c[0],c[1],[_user_stacks['Params'][-1]['w'],_user_stacks['Params'][-1]['h']],layer=_user_stacks['Params'][-1]['l'],thickness=_user_stacks['Params'][-1]['t']),'Draw',
        '[TEXT POSITION] Draws the TEXT at POSITION using previously set drawparams. Position is in native units (nm) so using mm or mils commands is suggested.'),
    'drawparams': Command(2,lambda c: DRAWPARAMS(c),'Draw',
        '[THICKNESS,WIDTH,HEIGHT LAYER] Set drawing parameters for future draw commands.\n'
        'Example: 1,5,5 mm F.Fab drawparams'),
    'getparams': Command(0,lambda c: _user_stacks['Params'][-1],'Draw',
        'Return the draw parameters.'),
    #'findnet': Command(1,lambda c: FINDNET(*c),'Draw','[NETNAME] Returns the netcode of NETNAME.'),
    # findnet could be implemented as ':persist findnet "Draw [NETNAME] Returns the netcode of NETNAME." board swap FindNet call'

    'params': Command(2,lambda c: PARAM(*c),'Draw',
        '[VALUESLIST KEYLIST] Set drawing parameters. Each member of VALUELIST is assigned to the '
        'corresponding key in KEYLIST. Keys are "t,w,h,l,zt,zp" indicating Thickness, Width, Height, '
        'Layer, ZoneType, ZonePriority. ZoneType is one of NO_HATCH, DIAGONAL_FULL, or DIAGONAL_EDGE.\n'
        'Example: 1,5,5 mm t,w,h param'),
    'helpall': Command(0,lambda c: HELPALL(),'Help',
        "Shows detailed help on every command."),
    'help': Command(0,lambda c: HELPMAIN(),'Help',
        "Shows general help"),
    'explain': Command(1,lambda c: EXPLAIN(*c),'Help',
        "[COMMAND] Shows help for COMMAND. COMMAND can be a comma separated list of commands (use a comma after a single command to prevent KiCommand from interpreting the command). The keyword 'All' shows help for all commands. You can precede the COMMAND by single quote mark so that it does not execute, or use the comma trick."),
    # 'helpcom': Command(0,lambda c: HELP(None),'Help',
        # "[COMMAND] Shows help for COMMAND. The keyword 'All' shows help for all commands. Precede the COMMAND by single quote mark (') so that it doesn't execute."),
    'helpcat': Command(1,lambda c: HELPCAT(*c),'Help',
        "[CATEGORY] Shows commands in CATEGORY. CATEGORY value of 'All' shows all categories."),
    'pad2draw': Command(1,lambda c: pad_to_drawsegment(*c),'Draw',
        '[PADLIST] draws outlines around pad on DRAWPARAMS layer.'),
    'load': Command(1,lambda c: LOAD(*c),'Programming',
        '[FILENAME] executes commands from FILENAME. relative to '
        '~/kicad/kicommand then $KICOMMAND_MODULE_DIR/loadable. Note that this command is not '
        'totally symmetric with the save command.'),
    'save': Command(1,lambda c: SAVE(*c),'Programming',
        '[FILENAME] saves the user dictionary into FILENAME relative to '
        '~/kicad/kicommand. Note that this command is not '
        'totally symmetric with the load command.'),

        
    # 'vias': filter(lambda x:isinstance(x,pcbnew.VIA),_dictionary['command']['tracks']),
    # 'vias_class': filter(lambda x:pcbnew.VIA_Classof(x),_dictionary['command']['tracks']),
})

loadname = os.path.join(os.path.dirname(__file__),'kicommand_persist.commands')
#print ('Loading from %s'%os.path.normpath(loadname))
LOAD('kicommand_persist.commands',path=os.path.dirname(__file__))

#wx.MessageDialog(None,'KiCommand commands defined.').ShowModal()
    

def getBoard():
    if len(_user_stacks['Board']) == 0:
        _user_stacks['Board'].append(pcbnew.GetBoard())
    return _user_stacks['Board'][-1]
# _user_stacks = {'drawparams':
# {'t':0.3*pcbnew.IU_PER_MM, 'w':1*pcbnew.IU_PER_MM, 'h':1*pcbnew.IU_PER_MM,'l':pcbnew.Dwgs_User,
# 'zt':pcbnew.CPolyLine.NO_HATCH,'zp':0},
    # 'Board': [pcbnew.GetBoard()]
# }
# drawparams: thickness,width,height,layer

def print_userdict(command=None):
    for dictname in ['user','persist']:
        output( '\n',dictname,'Dictionary')
        if command:
            commands = filter (lambda x:x[0].startswith(command),_dictionary[dictname].iteritems())
        else:
            commands = _dictionary[dictname].iteritems()
            #output ('%d items in %s'%(99,dictname))
        for found,definition in sorted(commands,key=lambda x:x[0]):
            text = _dictionary[dictname][found]
            if hasattr(text,'helptext'):
                text = '"'+text.category+' '+text.helptext+'" '+' '.join(text.execute)
            output( ":",found,text,';')
            
# r('CLEAR MODULETEXTOBJ VALUETEXTOBJ APPEND REFERENCETEXTOBJ APPEND COPY GetTextBox CALL CORNERS SWAP COPY GetCenter CALL SWAP GetTextAngleDegrees CALL ROTATEPOINTS DRAWSEGMENTS')
#    'not': Command(0,lambda c: kc('0 FLOAT ='),'Comparison'),

#output( 'ops',str(_stack))
def printcategories():
    result=defaultdict(set)
    for key,val in _dictionary['command'].iteritems():
        result[val.category].add(key)
    
    for key,val in result.iteritems():
        output( key)
        output( '\t','\n\t'.join(val))
        
pshapesactual = filter(lambda x: x.startswith('PAD_SHAPE_'),dir(pcbnew))
# pshapes = ['PAD_SHAPE_CIRCLE','PAD_SHAPE_OVAL', 'PAD_SHAPE_RECT', 'PAD_SHAPE_ROUNDRECT', 'PAD_SHAPE_TRAPEZOID'] 5.1.5
pshapes = ['PAD_SHAPE_CIRCLE', 'PAD_SHAPE_CUSTOM', 'PAD_SHAPE_OVAL', 'PAD_SHAPE_RECT', 'PAD_SHAPE_ROUNDRECT', 'PAD_SHAPE_TRAPEZOID'] # 5.1.6
if Counter(pshapesactual) != Counter(pshapes):
    try:
        output( 'Warning! Expected Pad Shapes are different than KiCommand expects. KiCAD has been updated? Consider running unit tests (import kicommand.test)')
    except:
        pass

def _newsegment(type, points):
    #output("_newsegment: {} {}".format(type,points))
    
    board = getBoard()
    ds=pcbnew.DRAWSEGMENT(board)
    board.Add(ds)
    layer = _user_stacks['Params'][-1]['l']

    ds.SetLayer(getLayerID(layer)) # TODO: Set layer number from string
    ds.SetWidth(max(1,int(_user_stacks['Params'][-1]['t'])))
    
    # ds=pcbnew.DRAWSEGMENT()
    # types = {}
    # for shapenum in range(pcbnew.S_LAST):
        # ds.SetShape(shapenum)
        # types[ds.GetShapeStr()] = shapenum
        
    types = {
            'Arc':pcbnew.S_ARC,
            'Circle':pcbnew.S_CIRCLE,
            #'Bezier':pcbnew.S_CURVE,
            'Polygon':pcbnew.S_POLYGON,
            #'Rect':pcbnew.S_RECT,
            'Line':pcbnew.S_SEGMENT
        }
    typenum = types.get(type,-1)
    if type == -1:
        raise TypeError('Type must be one of {}'.format(', '.join(types.keys())))
    
    # GetShapeStr,GetPosition,GetCenter,GetArcStart,GetAngle,
    # what is the difference between Center and Position?
    # GetType always returns 0
    
    # newline
    # newpolygon 
    # newarc, newarca, newarcp, newarcr, 
    # newcircle, newcirclep, newcircler, newcirclec
    
    # line, polygon, arca, arcp, arcr, circlep, circler, circlec
    
    # newsegmenttype SegmentShape ArgX...,[Thickness],[Layer]
    # newsegment SegmentShape,ArgX...,[Thickness],[Layer]
    # getsegment[t,l,tl] SegmentShape,ArgX...,[Thickness],[Layer]
    # {'Line':'pp', 'Polygon':'p', 'ArcA':'ppn', 'ArcP':'ppp', 'ArcR':'ppn', 'CircleP':'pp', 'CircleR':'pn', 'CircleC':'ppn'}
    # ? Polyline where a string of points is connected by segments.
    # Line is where point pairs are given, one pair for each segment.
    ds.SetShape(typenum)
    if type == 'Line': # pcbnew.S_SEGMENT:
        # GetStart/SetStart
        # GetEnd/SetEnd
        s = pcbnew.wxPoint(points[0],points[1])
        e = pcbnew.wxPoint(points[2],points[3])
        ds.SetStart(s)
        ds.SetEnd(e)
    if type == 'Polygon': # typenum == pcbnew.S_POLYGON:
        pass
        # BuildPolyPointsList/SetPolyPoints
    if type == 'Arc': # if typenum == pcbnew.S_ARC:
        pass
        # ArcA StartPoint, CenterPoint, AngleDegrees (+/- indicates direction)
        # ArcP StartPoint, EndPoint, CenterPoint
        # ArcR StartPoint, EndPoint, RadiusNative (+/- indicates direction, CW/CCW or RW/LW, make sure this matches Angle direction)
        # GetArcStart/SetArcStart
        # GetCenter/SetCenter
        # GetAngle/SetAngle
        # ds.SetArcStart(pcbnew.wxPoint(x1,y1))
        # ds.SetAngle(float(angle)*10)
        # ds.SetCenter(pcbnew.wxPoint(x2,y2))
        
    if type == 'Circle': # if typenum == pcbnew.S_CIRCLE:
        pass
        # CircleP CenterPoint, StartPoint
        # CircleR CenterPoint, RadiusNative
        # CirlceC CirclePoint1, CirclePoint2, RadiusNative (+/- indicates direction, CW/CCW or RW/LW, make sure this matches Angle direction)
        # GetCenter/SetCenter
        # GetArcStart/SetArcStart = GetEnd/SetEnd, with point anywhere on circle (i.e. Center.x + radius)
        # ? GetArcAngle is 0.0
    # if typenum == pcbnew.S_CURVE: # Bezier?
        # GetBezierPoints/SetBezierPoints 
        # GetBezControl1/SetBezControl1
        # GetBezControl2/SetBezControl2
    # if typenum == pcbnew.S_RECT:
        
    
def pad_to_drawsegment(pad):
    #ds_shapes=['S_ARC', '', 'S_CURVE', 'S_LAST', 'S_POLYGON', '', 'S_SEGMENT']
    #p_shapes=['','', '', '', '']
    # 5.1.5-(3) ['S_ARC', 'S_CIRCLE', 'S_CURVE', 'S_LAST', 'S_POLYGON', 'S_RECT', 'S_SEGMENT']
    # ['PAD_SHAPE_CIRCLE', 'PAD_SHAPE_CUSTOM', 'PAD_SHAPE_OVAL', 'PAD_SHAPE_RECT', 'PAD_SHAPE_ROUNDRECT', 'PAD_SHAPE_TRAPEZOID']
    pshape2ds = {
        pcbnew.PAD_SHAPE_CIRCLE:pcbnew.S_CIRCLE,
        pcbnew.PAD_SHAPE_RECT:pcbnew.S_RECT,
        pcbnew.PAD_SHAPE_ROUNDRECT:pcbnew.S_RECT,
        pcbnew.PAD_SHAPE_OVAL:pcbnew.S_RECT,
        pcbnew.PAD_SHAPE_TRAPEZOID:pcbnew.S_RECT,
    }
    board = getBoard()
    ds=pcbnew.DRAWSEGMENT(board)
    board.Add(ds)
    layer = _user_stacks['Params'][-1]['l']

    ds.SetLayer(getLayerID(layer)) # TODO: Set layer number from string
    ds.SetWidth(max(1,int(_user_stacks['Params'][-1]['t'])))

    if pad.GetShape() in [pcbnew.PAD_SHAPE_RECT,
                          pcbnew.PAD_SHAPE_ROUNDRECT,
                          pcbnew.PAD_SHAPE_OVAL,
                          pcbnew.PAD_SHAPE_TRAPEZOID]:
        pad.GetBoundingBox()
    elif pad.GetShape==pcbnew.PAD_SHAPE_CIRCLE:
        ds.SetShape(S_CIRCLE)
        ds.SetRadius(pad.GetSize())
    ds.SetPosition(pad.GetPosition())
    ###ds.SetSize(pad.GetSize())
    # ds.SetStart(pcbnew.wxPoint(x1,y1))
    # ds.SetEnd(pcbnew.wxPoint(x2,y2))
    return ds

    # viasbb_selected = filter(lambda x:         isinstance(x,pcbnew.VIA_BLIND_BURIED),tracks_selected)
    # viasthrough_selected = filter(lambda x:    isinstance(x,pcbnew.VIA_THROUGH),tracks_selected)
    # viasmicrovia_selected = filter(lambda x:   isinstance(x,pcbnew.VIA_MICROVIA),tracks_selected)
    # viasnotdefined_selected = filter(lambda x: isinstance(x,pcbnew.VIA_NOT_DEFINED),tracks_selected)

    # toptext = filter(lambda x: isinstance(x,pcbnew.EDA_TEXT) and x.IsSelected(),getBoard().GetDrawings())
    # moduleitems=[]
    # for m in getBoard().GetModules():
        # moduleitems.extend(m.GraphicalItems())
    # moduletext = filter(lambda x: isinstance(x,pcbnew.EDA_TEXT),moduleitems)

    # viasnotdefined_selected = filter(lambda x: isinstance(x,pcbnew.VIA_NOT_DEFINED),tracks_selected)
    
    # Examples of more filters:
    
    # Get list of Selected items:
    # items_selected = filter(lambda x: x.IsSelected(), items_all)
    
    # Get list of items on a specific layer:
    # items_onlayer = filter(lambda x: x.IsOnLayer(pcbnew.F_Cu), items_all)
    
    # Get list of items on any one of several layers:
    # layerIdList = [pcbnew.F_Cu, pcbnew.F_SilkS]
    # items_onAnyLayer = filter(len(filter(labmda x: x.IsOnLayer(layer), layerIdList)),items_all)
    
    # Set items to "Selected"
    # for x in items_all:
    #     x.SetSelected()
    
    # Clear Select on list of items:
    # for x in items_all:
    #     x.ClearSelected()

    
# https://stackoverflow.com/questions/20389032/how-to-program-optional-multiple-inheritance-in-python
# I found inspiration in this great article:
# http://www.jeffknupp.com/blog/2013/12/28/improve-your-python-metaclasses-and-dynamic-classes-with-type/

# def jinjacms_get(self):         # member function for JinjaCMS class
    # ....

# if config.GDRIVE_HOOK:          #optional multiple inheritance
    # from jinjacms import drivecms
    # JinjaCMS = type(str('JinjaCMS'), (drivecms.CmsDrive, cmsbase.CmsHandler), {'get': jinjacms_get})
# else:
    # JinjaCMS = type(str('JinjaCMS'), (cmsbase.CmsHandler, ), {'get': jinjacms_get})
# in Python the class hierarchy is defined right to left

#import makeAP
# class MakeAP():
    # @staticmethod
    # MakeAP(mClass,name,category,description)
    
# try:
    # menu().register()
# except:
    # pass

def getallcommands():
    fulldict = {}
    for dictname in ('command','persist'): #,'user'):
        fulldict.update(_dictionary[dictname])

    dependencies = defaultdict(list)
    
    for cname,command in _dictionary['persist'].iteritems():
        for subcommand in command.execute:
            #print(str(subcommand))
            dependencies[cname].append(subcommand)
    for cname,executelist in dependencies.iteritems():
        dependencies[cname] = set([x for x in executelist if x in dependencies])
       
    # print("List of commands without dependencies")

    # for command,depends in dependencies.iteritems():
        # if not depends:
            # print('"{}"'.format(command))

    #print("List of commands with dependencies")
    for x in toposort2(dependencies):
        print(x)
    # for command,depends in toposort2(dependencies):
        # if depends:
            # print('"{}: {}"'.format(command,', '.join(depends)))
        
from functools import reduce

def toposort2(data):
    """Dependencies are expressed as a dictionary whose keys are items
and whose values are a set of dependent items. Output is a list of
sets in topological order. The first set consists of items with no
dependences, each subsequent set consists of items that depend upon
items in the preceeding sets.

>>> print '\\n'.join(repr(sorted(x)) for x in toposort2({
...     2: set([11]),
...     9: set([11,8]),
...     10: set([11,3]),
...     11: set([7,5]),
...     8: set([7,3]),
...     }) )
[3, 5, 7]
[8, 11]
[2, 9, 10]

"""

    # http://code.activestate.com/recipes/578272-topological-sort/
    # Ignore self dependencies.
    for k, v in data.items():
        v.discard(k)
    # Find all items that don't depend on anything.
    extra_items_in_deps = reduce(set.union, data.itervalues()) - set(data.iterkeys())
    # Add empty dependences where needed
    data.update({item:set() for item in extra_items_in_deps})
    while True:
        ordered = set(item for item, dep in data.iteritems() if not dep)
        if not ordered:
            break
        yield ordered
        data = {item: (dep - ordered)
                for item, dep in data.iteritems()
                    if item not in ordered}
    assert not data, "Cyclic dependencies exist among these items:\n%s" % '\n'.join(repr(x) for x in data.iteritems())

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def flatten(iterable):
    iterator, sentinel, stack = iter(iterable), object(), []
    while True:
        value = next(iterator, sentinel)
        if value is sentinel:
            if not stack:
                break
            iterator = stack.pop()
        elif isinstance(value, str):
            yield value
        else:
            try:
                new_iterator = iter(value)
            except TypeError:
                yield value
            else:
                stack.append(iterator)
                iterator = new_iterator
import random    
def font_test(origin=(0,0)):

    x,y = origin
    fm = fonts.getfontmanager()
    fontlist = fm.getfontlist()
    count = -1
    random.shuffle(fontlist)
    #print('Fontlist:',fontlist)
    for font in fontlist[:80]: # 90 fonts fails, 80 succeeds, 85 fails
        count += 1
        print(font)
        fm.getfont(font)
        #for glyphname,glyphdata in self._fontdata.items():
        #for codepoint,glyphname in self._fontdata._unicode_codepoint_lookup.items():
        ustr = u''.join([unichar(ord) for ord in sorted(fonts.getfont()._unicode_codepoint_lookup.keys())])
        ustr=ustr.replace(u'"',u"")
        #print(ustr)
        fontsize = 10.0
        r=kc(u'{} setfont {} stringtogeom Tmm,-1000,{} split swap append newdrawing'.format(font,font,-1000+count*30*fontsize/72.0))
        r=kc(u'{} setfont {} stringtogeom Tmm,-908,{} split swap append newdrawing'.format(font,ustr,-1000+count*30*fontsize/72.0))
        # ustr[:100]
        fm.removeFromTable(font)
    kc('refresh')
    # : windowzoom "Gui [x_y_w_h] input is a list of integers. Zoom to the box defined by x,y and w(idth), h(eight)." int pcbnew swap WindowZoom callargs ;
def visual_test(originpoint):

    x,y = originpoint
    
    # This should form a single "star" with lines from origin to each point.
    # Two lines for all angles and three for angle 0 (-360, 0, and 360)
    points = [wxPointUtil.toxy(1.0,theta*math.pi/180) for theta in range(-360,361,45)]
    preflat=[((x,y),(p[0]+x,p[1]+y)) for p in points]
    #flat=itertools.chain.from_iterable(itertools.chain.from_iterable(preflat))
    flat = flatten(preflat)
    ostr = "Line,{} split newdrawing refresh".format(','.join([str(int(k*1000000)) for k in flat]))
    
    r=kc(ostr)
    text=r'This should form a single star with lines from origin\nto each point. Lines should be uniform around the circle.  EndText'
    r=kc('Text,mm,{},{},{} split newdrawing justifyr refresh'.format(x-3,y,','.join(text.split(' '))))
    
    #return
    x = originpoint[0]
    y+=3*2

    text = r'This is testing the core rounded corner python function call. EndText'
    r=kc('Text,mm,{},{},{} split newdrawing justifyr'.format(x-3,y,','.join(text.split(' '))))


    inity=y
    points = [wxPointUtil.toxy(1.0,theta*math.pi/180) for theta in range(-360,361,60)]
    preflat = []
    columncount = 0
    # Text,mm,-20,-20,Hello\nLine2\nLine3\nLine4 split newdrawing justifyt justifyl refresh
    for s in points:
        for e in points:
            columncount += 1
            if not columncount % 3:
                x+=3
                y=inity
            # else:
                # y+=3*4
            if isclose(s[0],e[0],rel_tol=1e-10,abs_tol=1e-10) and isclose(s[1],e[1],rel_tol=1e-10,abs_tol=1e-10):
                continue
            for m in points:
                y+=3
                if (isclose(s[0],m[0],rel_tol=1e-10,abs_tol=1e-10) and isclose(s[1],m[1],rel_tol=1e-10,abs_tol=1e-10)) or (isclose(e[0],m[0],rel_tol=1e-10,abs_tol=1e-10) and isclose(e[1],m[1],rel_tol=1e-10,abs_tol=1e-10)):
                    continue
                # print 'ArcO,mm,{},{},{},{},{},{}'.format(s[0],s[1],m[0],m[1],e[0],e[1])
                # make a line from origin to each midpoint. The midpoint should be part of the arc in a visual check.
                p = ((x,y),(s[0]+x,s[1]+y),(m[0]+x,m[1]+y),(e[0]+x,e[1]+y))
                preflat.append((('PolylineRounded','mm',.2),p[1],p[2],p[3],p[1]))
                # y+=3
                # p = ((x,y),(s[0]+x,s[1]+y),(m[0]+x,m[1]+y),(e[0]+x,e[1]+y))
                # preflat.append((('PolylineRounded','mm',.2),p[3],p[2],p[1],p[3]))
                # y+=3
                # p = ((x,y),(s[0]+x,s[1]+y),(m[0]+x,m[1]+y),(e[0]+x,e[1]+y))
                # preflat.append((('PolylineRounded','mm',.2),p[1],p[3],p[2],p[1]))
                # y+=3
                # p = ((x,y),(s[0]+x,s[1]+y),(m[0]+x,m[1]+y),(e[0]+x,e[1]+y))
                # preflat.append((('PolylineRounded','mm',.2),p[2],p[1],p[3],p[2]))
                # y+=3
                # p = ((x,y),(s[0]+x,s[1]+y),(m[0]+x,m[1]+y),(e[0]+x,e[1]+y))
                # preflat.append((('PolylineRounded','mm',.2),p[2],p[3],p[1],p[2]))
                # y+=3
                # p = ((x,y),(s[0]+x,s[1]+y),(m[0]+x,m[1]+y),(e[0]+x,e[1]+y))
                # preflat.append((('PolylineRounded','mm',.2),p[3],p[1],p[2],p[3]))
                # y+=3
                # p = ((x,y),(s[0]+x,s[1]+y),(m[0]+x,m[1]+y),(e[0]+x,e[1]+y))
                # preflat.append((('PolylineRounded','mm',.2),p[3],p[2],p[1],p[3]))
    print('flattening')
    flat=flatten(preflat)
    print('flattened')
    ostr = "{} split newdrawing refresh".format(','.join([str(x) for x in flat]))
    print('string length={}'.format(len(ostr)))
    r=kc(ostr)

# End rounded test

    
    return

    x = originpoint[0]
    y+=3*2

    text = r'This verifies that the internal definition of toxy call matches the KiCAD definition of angle.\nEach line should point to the end point. EndText'
    r=kc('Text,mm,{},{},{} split newdrawing justifyr'.format(x-3,y,','.join(text.split(' '))))

    d=[]
    for theta in range(-360,361,15):
        # make two drawings, one a line from origin to "toxy" and one an arc with the same angle.
        p=wxPointUtil.toxy(1.0,theta*math.pi/180)
        d.append('Line,mm,{},{},{},{},ArcC,mm,{},{},{},{},{}'.format(0+x,0+y,p[0]+x,p[1]+y,0+x,0+y,1+x,0+y,theta))
        x+=3
    ostr = "{} split newdrawing refresh".format(','.join([str(k) for k in d]))
    r=kc(ostr)
    
    x = originpoint[0]
    y+=3*2

    text = r"This verifies many different point inputs to 'ArcO'.\nThe white lines point to the start/end points.\nThe pink line points to the mid point. EndText"
    r=kc('Text,mm,{},{},{} split newdrawing justifyr justifyt'.format(x-3,y,','.join(text.split(' '))))

    inity=y
    points = [wxPointUtil.toxy(1.0,theta*math.pi/180) for theta in range(-360,361,60)]
    groupsize = len(points)*2
    preflat = []
    columncount = 0
    # Text,mm,-20,-20,Hello\nLine2\nLine3\nLine4,EndText split newdrawing justifyt justifyl refresh
    for s in points:
        for e in points:
            columncount += 1
            if not columncount % 3:
                x+=3
                y=inity
            # else:
                # y+=3*4
            if isclose(s[0],e[0],rel_tol=1e-10,abs_tol=1e-10) and isclose(s[1],e[1],rel_tol=1e-10,abs_tol=1e-10):
                continue
            for m in points:
                y+=3
                if (isclose(s[0],m[0],rel_tol=1e-10,abs_tol=1e-10) and isclose(s[1],m[1],rel_tol=1e-10,abs_tol=1e-10)) or (isclose(e[0],m[0],rel_tol=1e-10,abs_tol=1e-10) and isclose(e[1],m[1],rel_tol=1e-10,abs_tol=1e-10)):
                    continue
                # print 'ArcO,mm,{},{},{},{},{},{}'.format(s[0],s[1],m[0],m[1],e[0],e[1])
                # make a line from origin to each midpoint. The midpoint should be part of the arc in a visual check.
                preflat.append((('Layer,Margin,Line','mm'),(x,y),(m[0]+x,m[1]+y),('Layer,Dwgs.User,Line','mm'),(x,y),(s[0]+x,s[1]+y),('Line','mm'),(x,y),(e[0]+x,e[1]+y),('ArcO','mm'),(s[0]+x,s[1]+y),(m[0]+x,m[1]+y),(e[0]+x,e[1]+y)))
    flat=itertools.chain.from_iterable(itertools.chain.from_iterable(preflat))
    ostr = "{} split newdrawing refresh".format(','.join([str(x) for x in flat]))
    r=kc(ostr)
    
    x = originpoint[0]
    y+=3*2

         
    # points = [wxPointUtil.toxy(1.0,theta*math.pi/180) for theta in range(0,360,45)]
    # perm = itertools.permutations(points,3)
    # postsort=sorted(perm, key=operator.itemgetter(1,0,2))
    # grp=itertools.izip_longest(*(iter(postsort),) * groupsize)
    # preflat = [[[(p[0]+dx*3,p[1]+dy*3) for p in e1] for dy,e1 in enumerate(eg)] for dx,eg in enumerate(grp)]
    # flat=itertools.chain.from_iterable(itertools.chain.from_iterable(itertools.chain.from_iterable(preflat)))
    # ostr = "ArcO,{} split newdrawing refresh".format(','.join([str(int(k*1000000)) for k in flat]))
    # r=kc(ostr)

    x = originpoint[0]
    y+=3*2


def __main__(self):
    KiCommandAction.getInstance().register()

#wx.MessageDialog(None,'KiCommand __name__: '+__name__).ShowModal()
