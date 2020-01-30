from __future__ import print_function
import collections
from collections import defaultdict, Counter
from itertools import compress,cycle

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

try:
    from wxpointutil import wxPointUtil
    import kicommand_gui
except:
    from .wxpointutil import wxPointUtil
    from . import kicommand_gui

# added for Python 3 compatibility, 
# define basestring so all the "isinstance(x,basestring)" functions will work.
try:
    basestring
except NameError:
    basestring = str
  
_dictionary = {'user':{}, 'persist':{}, 'command':{}}
# collections.OrderedDict
_command_dictionary = _dictionary ['command']
stack = []

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
# r('clear moduletext valuetext append referencetext append toptext append copy GetTextBox call corners swap copy GetCenter call swap GetTextAngle call rotatepoints drawpoly')
# copy copy Value call swap Reference call append swap GraphicalItems calllist append toptext append         copy GetTextBox call corners swap copy GetCenter call swap GetTextAngleDegrees call rotatepoints drawpoly

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

        # command_stack.run(command_string)
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
        # run()
        

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
UserCommand = collections.namedtuple('UserCommand','execute category helptext')
#DrawParams = collections.namedtuple('DrawParams','thickness width height layer cpolyline zonepriority')
DrawParams = collections.namedtuple('DrawParams','t w h l zt zp')
# param Usage:
# 0.3,1,1 mm F.Cu,NO_HATCH,0 split append t,w,h,l,zt,zp param
# 0.3,1,1 mm t,w,h param
# F.Cu,NO_HATCH,0 l,zt,zp param

# : drawparams list append t,w,h,l param ;
# : drawparams 'l param t,w,h param ;
# clear toptextobj selected topoints pairwise Dwgs.User tosegments
# clear toptextobj selected copy GetThickness call swap topoints pairwise Dwgs.User tosegments

#uc.execute(uc.string)
def SHOWPARAM(values,keys):
    return _user_stacks['drawparams']
    
def PARAM(values,keys):
    if isinstance(values,basestring):
        values = values.split(',')
    keys = keys.split(',')
    
    if not hasattr(values,'__iter__'):
        values = [values]
    for k,v in zip(keys,values):
        _user_stacks['drawparams'][k] = v

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
            run(commandstring)
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
            wx.MessageDialog(self.GetParent(),"Error 1 on line %s: %s\n%s"%
               (exc_tb.tb_lineno, str(e), traceback.format_exc())).ShowModal()
            
class aplugin(pcbnew.ActionPlugin):
    """implements ActionPlugin"""
    g = None
    def defaults(self):
        self.name = "KiCommand"
        self.category = "Command"
        self.description = "Select, modify and interrogate pcbnew objects with a simple command script."
    def Run(self):
        # parent =      \
            # filter(lambda w: w.GetTitle().startswith('Pcbnew'), 
                # wx.GetTopLevelWindows()
            # )[0]
        # better for Python3
        parent = [x for x in wx.GetTopLevelWindows() if x.GetTitle().startswith('Pcbnew')][0]
        aplugin.g=gui(parent)
        pane = wx.aui.AuiPaneInfo()                       \
         .Caption( u"KiCommand" )                   \
         .Center()                                \
         .Float()                                 \
         .FloatingPosition( wx.Point( 346,268 ) ) \
         .Resizable()                             \
         .FloatingSize( wx.Size( int(610),int(652) ) )       \
         .Layer( 0 )                                 

        manager = wx.aui.AuiManager.GetManager(parent)
        manager.AddPane( self.__class__.g, pane )
        manager.Update()
        loadname = os.path.join(os.path.dirname(__file__),'kicommand_persist.commands')
        #print ('Loading from %s'%os.path.normpath(loadname))
        LOAD('kicommand_persist.commands',path=os.path.dirname(__file__))

        run('help')


def run(commandstring,returnval=0):
    """returnval -1 return entire stack, 0 return top, >0 return that number of elements from top of list as a list."""
# Items beginning with single quote are entered onto the stack as a string (without the quote)
# Items beginning with double quote swallow up elements until a word ends in a double quote,
# and enters the entire item on the stack as a string (without the quotes)
# Commands beginning with ? are conditional. The top of the stack is popped,
# and if it was True, then the command is executed.
    try:
        global stack
        global _compile_mode
        global _command_definition
        global _user_dictionary
        global _dictionary
        #output( _command_dictionary.keys())
        #output( str(stack))
        
        #print(type(commandstring))
        commandlines = commandstring.splitlines()
        commands = []
        for commandstring in commandlines:
            #print('processing {%s}'%commandstring)
            #commands = []
            qend = 0
            while True:
                qindex = commandstring.find('"',qend)
                if qindex == -1:
                    break;
                # wx.MessageDialog(None,'PRE '+commandstring[qend:qindex-1]).ShowModal()
                commands.extend(commandstring[qend:qindex].split())
                qend = commandstring.find('"',qindex+1)
                if qend == -1:
                    raise SyntaxError('A line must contain an even number of double quotes.')
                commands.append(commandstring[qindex+1:qend])
                # wx.MessageDialog(None,'Q {'+commandstring[qindex+1:qend]+'}').ShowModal()
                qend += 1
                
            # wx.MessageDialog(None,'END {'+commandstring[qend:]+'}').ShowModal()
            commands.extend(commandstring[qend:].split())
        # wx.MessageDialog(None,'{'+'}{'.join(commands)+'}').ShowModal()
        #print('{','}{'.join(commands),'}')
        for command in commands:
            
            if command == ';':
                _compile_mode = False
                comm = _command_definition[:1]
                if not comm: # delete all commands in the user dictionary: ': ;'
                    _user_dictionary = {}
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
                        _dictionary[_newcommanddictionary][comm] = UserCommand(cdef,cat,help)
                    #output( "COMMAND %s DEFINITION %s\nCategory: {%s} Help: {%s}"%(comm,cdef,cat,help))
                    else:
                        _dictionary[_newcommanddictionary][comm] = UserCommand(cdef,'','')
                        #_dictionary[_newcommanddictionary][comm] = ' '.join(cdef)
                else: # delete a command in the user dictionary: ': COMMAND ;'
                    del(_user_dictionary[_command_definition[0]])
                _command_definition = []
                continue

            if _compile_mode:
                _command_definition.append(command)
                continue
            
            if command.startswith("'"):
                stack.append(command[1:])
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
                    if len(stack) < numop:
                        raise TypeError('%s expects %d arguments on the stack.'%(command,numop))
                    if numop:
                        result = commandToExecute.execute(stack[-numop:])
                        stack = stack[:-numop]
                    else:
                        result = commandToExecute.execute([]) # TODO should this be [] ?
                        
                    if result != None:
                        stack.append(result)
                elif isinstance(commandToExecute,UserCommand):
                    #output('%s is UserCommand'%command)
                    run(' '.join(commandToExecute.execute))
                elif isinstance(commandToExecute,basestring):
                    #output('%s is commandstring'%command)
                    run(commandToExecute)
                found = True
                break
            if not found:
                stack.append(command)
            
            
        if len(stack):
            output( len(stack), 'operands left on the stack.' )
        try:
            pcbnew.UpdateUserInterface()
        except:
            pass
        #print('User dictionary',_dictionary['user'])
        if returnval == 0:
            if stack:
                return stack[-1]
            else:
                return None
        elif returnval == -1:
            return stack
        elif returnval > 0:
            #returnval = -1 - returnval
            return stack[-returnval:]
    except Exception as e:
        # print(traceback.format_exc())
        #e = sys.exc_info()[0]
        #print("Error: %s" % e)
        raise
        
def retNone(function,*args):
    function(*args)

def UNDOCK():
    wx.aui.AuiManager.GetManager(aplugin.g).GetPane(aplugin.g).Float()
    # wx.aplugin.g.Float() #mgr.GetPane(text1).Float()
    # self.mgr.GetPane(text1).Float()
    # wx.aui.AuiManager.GetPane(wx.aplugin.g, item)
def STACK():
    for obj in stack:
        output(obj)
def PRINT():
    """print the top of the stack"""
    output(stack[-1])
        
def CLEAR():
    global stack
    stack = []
    return None
    
def SWAP():
    global stack
    stack[-1],stack[-2]=stack[-2],stack[-1]
# clear modules selected Reference call 0 bool list list SetVisible stack
def output(*args):

    for arg in args:
        aplugin.g.outputbox.AppendText(str(arg)+' ')
    aplugin.g.outputbox.AppendText('\n')
    return
    # Here's the simple 'print' definition of output
    for arg in args:
        print(arg,end=' ')
    print()

def tosegments(*c):
    tracklist,layer = c
    #print('tracklist: ',tracklist)
    try:
        layerID = int(layer)
    except:
        layerID = _user_stacks['Board'][-1].GetLayerID(str(layer))
        
    segments = []
    for tlist in tracklist:
        for t in tlist:
            # s=t.GetStart()
            # e=t.GetEnd()
            s,e = get_ds_ends(t)
            
            try:
                width = t.GetWidth()
            except:
                width = _user_stacks['drawparams']['t']
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
    
    try:
        layer = int(layer)
    except:
        layer = _user_stacks['Board'][-1].GetLayerID(str(layer))

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
        input = map(lambda y: floatnoerror(y),map(lambda x: temp.extend(x),[i.split(',') for i in input]))
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
            output('string2')
            #numbers = map(lambda x: float(x),shape.split(','))
            numbers = [float(x) for x in shape.split(',')]
			
        if not hasattr(numbers[0],'__getitem__'):
            #print('zip triggered')
            a=iter(numbers)
            numbers = [(intnoerror(x),intnoerror(y)) for x,y in zip(a, a)]
        for i in range(len(numbers)-1):
            s = numbers[i]
            e = numbers[i+1]

            if not isinstance(numbers[i],pcbnew.wxPoint) or not isinstance(numbers[i],pcbnew.wxPoint):
                try:
                    s = pcbnew.wxPoint(numbers[i][0],numbers[i][1])
                    e = pcbnew.wxPoint(numbers[i+1][0],numbers[i+1][1])
                except:
                    continue
            segments.append(draw_segmentwx(s,e,layer=layer,thickness=thickness))
# test commands:
# Test single list of numbers:
# 0,0,1,1 mm drawpoly
# Test single list of list of numbers:
# 0,0,1,1 mm list drawpoly
# Test single list of numbers:
# 0,0,1,1,2,2,3,3 mm list drawpoly
# Test two lists of numbers:
# 0,0,1,1 mm list 2,2,3,3 mm list append drawpoly
# 0,0,1000000,1000000 ,2000000,2000000,3000000,3000000 append drawpoly
# 0,0,1000000,1000000,2000000,2000000,3000000,3000000 drawpoly
# 0,0,1000000,1000000 list 2000000,2000000,3000000,3000000 list append drawpoly
# 0,0 mm wxpoint 1,1 mm wxpoint append 2,2 mm wxpoint append 3,3 mm wxpoint append drawpoly
# 0,0 mm wxpoint 1,1 mm wxpoint append list 2,2 mm wxpoint 3,3 mm wxpoint append list append drawpoly
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
            for gp,sp in ((seg.GetStart,seg.SetStart),(seg.GetEnd,seg.SetEnd)):
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
    
    output('Center: %s'%(center))
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

def order_segments(dseglist):
    # fixed with gridboxes
    segs_by_box = defaultdict(set)
    boxes_by_seg = {}

    for seg in dseglist:
        s,e = get_ds_ends(seg)
        gbs = gridboxes(s)
        gbe = gridboxes(e)
        # any of the boxes points to the opposite end of the segment
        sdict={}
        for b in gbs:
            sdict[b] = e
            # output(str(b))
            segs_by_box[b].add(seg)
        edict={}
        for b in gbe:
            # output(str(b))
            edict[b] = s
            segs_by_box[b].add(seg)
            
        boxes_by_seg[seg] = {s:sdict,e:edict}
        """bbs is a structure that you can look up all the boxes the 
        opposing point of the segment exists in."""
    # output ('sbb keys:')
    for box,segs in segs_by_box.iteritems():
        seglist=list(segs)
        # output(str(box),len(segs))
        # for seg in seglist:
            # output('\t',get_ds_ends(seg))
    # now create a structure where a segment points to all connected segments
    # output('sbb %s'%str(segs_by_box))
    # output('bbs %s'%str(boxes_by_seg))
    connected = defaultdict(set)
    for b,seglist in segs_by_box.iteritems():
        for seg1 in seglist:
            for seg2 in seglist:
                if seg1 != seg2:
                    # output('adding')
                    connected[seg1].add(seg2)
                    connected[seg2].add(seg1)
    # output('connected:')
    # for seg,seglist in connected.iteritems():
        # output('%s'%str(get_ds_ends(seg)))
        # for cseg in seglist:
            # output('\t%s'%str(get_ds_ends(cseg)))
    # now a sanity check
    for seg,seglist in connected.iteritems():
        if len(seglist) > 2:
            # doesn't capture three segments at one box/point
            output('Error: segment connected to more than 2 other segments: %s'%
                str(get_ds_ends(seg)))
            return dseglist
    
    segset = set()
    ordered_and_split = [[]]
    for seg in dseglist:
        currentseg = seg
        lastseg = seg
        while currentseg is not None and currentseg not in segset:
            segset.add(currentseg)
            csegs = list(connected.get(currentseg,None))
            # csegs should be one or two segments
            if lastseg in csegs:
                csegs.remove(lastseg)
            # output('added to oas')
            ordered_and_split[-1].append(currentseg)
            lc = len(csegs)            
            if lc == 0:
                ordered_and_split.append([])
                currentseg = None
            elif lc == 1:
                lastseg = currentseg
                currentseg = csegs[0]
            else: # lc = > 1
                output('Error: segment connected to more than 2 other segments: %s'%
                    str(get_ds_ends(currentseg)))
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
        output( "currentpoint = ",currentpoint)
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
    
def draw_arc_to_segments(radius,dseglist):
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
        allpoints.extend(get_ds_ends(seg))
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
        if shape == pcbnew.S_ARC:
            seg.SetCenter(pcbnew.wxPoint(*rotate_point(seg.GetCenter(),center,angle,ccw=True)))
        if shape == pcbnew.S_CIRCLE:
            seg.SetCenter(pcbnew.wxPoint(*rotate_point(seg.GetCenter(),center,angle,ccw=True)))
        
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
    board = _user_stacks['Board'][-1]
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
    board = _user_stacks['Board'][-1]
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
    board = _user_stacks['Board'][-1]
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

def layer(layer):
    try:
        return int(layer)
    except:
        return _user_stacks['Board'][-1].GetLayerID(layer)
    
def draw_text(text,pos,size,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):
    """Draws the line segment indicated by the x,y values
    on the given layer and with the given thickness."""
    
# 'Hello 100,100 MM 10,10 MM 1 MM F.SilkS DRAWTEXT'
# '0,0,100,100 MM DRAWSEGMENTS'
    
    size = pcbnew.wxSize(size[0],size[1])
    pos = pcbnew.wxPoint(pos[0],pos[1])
    board = _user_stacks['Board'][-1]
    thickness = int(thickness)
    try:
        layer = int(layer)
    except:
        layer = board.GetLayerID(layer)
    
    #ds=pcbnew.DRAWSEGMENT(board)
    ds=pcbnew.TEXTE_PCB(board)
    board.Add(ds)
    # ds.SetStart(pcbnew.wxPoint(x1,y1))
    # ds.SetEnd(pcbnew.wxPoint(x2,y2))
    #ds.SetLayer(layer)
    #ds.SetWidth(max(1,int(thickness)))
    
    ds.SetPosition(pos) # wxPoint
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
    allitems = list(_user_stacks['Board'][-1].GetDrawings())
    for m in _user_stacks['Board'][-1].GetModules():
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
    
def CUT():

    cutees = filter(
        lambda x: isinstance(x,pcbnew.DRAWSEGMENT) and x.GetShape() == pcbnew.S_SEGMENT,
        _user_stacks['Board'][-1].GetDrawings())

    cutter = filter(lambda x:x.IsSelected(),cutees)[0]
    scutter,ecutter = get_ds_ends(cutter)
    #output(str(cutter),len(cutees))
    bb = cutter.GetBoundingBox()
    cutl,cutr,cutt,cutb = bb.GetLeft(),bb.GetRight(),bb.GetTop(),bb.GetBottom()
    within = []
    for cutee in cutees:
        if cutee == cutter:
            # output('=')
            continue
        if not isinstance(cutee,pcbnew.DRAWSEGMENT):
            continue
        if cutee.GetShape() != pcbnew.S_SEGMENT:
            continue
        #output(get_ds_ends(cutee))
        bb = cutee.GetBoundingBox()
        segl,segr,segt,segb = bb.GetLeft(),bb.GetRight(),bb.GetTop(),bb.GetBottom()
        if segr < cutl or segl > cutr or segb < cutt or segt > cutb:
            continue
        #output('!')

        # Get intersection point
        s,e = get_ds_ends(cutee)
        intersect = lines_intersect(s,e,scutter,ecutter)
        #output('intersect',intersect,'s',s,'e',e,'scut',scutter,'ecut',ecutter)
        if intersect is None:
            output('intersect returned None')
            continue
        
        if ((s[0] < intersect[0] < e[0]) or (e[0] < intersect[0] < s[0])) and \
        ((s[1] < intersect[1] < e[1]) or (e[1] < intersect[1] < s[1])) and \
        ((scutter[0] < intersect[0] < ecutter[0]) or (ecutter[0] < intersect[0] < scutter[0])) and \
        ((scutter[1] < intersect[1] < ecutter[1]) or (ecutter[1] < intersect[1] < scutter[1])):

        # see if intersection point is within s and e
        #if (s[0] < intersect[0] < e[0]) and (s[1] < intersect[1] < e[1]) and \
           #(scutter[0] < intersect[0] < ecutter[0]) and (scutter[1] < intersect[1] < ecutter[1]):
            newe = tuple(e)
            cutee.SetEnd(intersect)
            draw_segment(intersect[0],intersect[1],newe[0],newe[1],layer=cutee.GetLayer(),thickness=cutee.GetWidth())
            #output('new segment',intersect, e)
            #output('cut',s,e,'at',intersect)        
        # within.append(cutee) 
    #pcbnew.UpdateUserInterface()
    #cutter.UnLink()
    _user_stacks['Board'][-1].GetDrawings().Remove(cutter)
    #cutter.DeleteStructure()
    return None
def DRAWPARAMS(dims,layer):
    t,w,h = dims.split(',') if isinstance(dims,basestring) else dims \
    if hasattr(dims,'__iter__') else [dims]

    try:
        layerID = int(layer)
    except:
        layerID = _user_stacks['Board'][-1].GetLayerID(str(layer))

    _user_stacks['drawparams'] = [t,w,h,layerID]

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
def FINDNET(netname):
    # board has: 'BuildListOfNets', 'CombineAllAreasInNet', 'FindNet'
    board = _user_stacks['Board'][-1]
    # nets = board.GetNetsByName()
    # netinfo = nets.find(netname).value()[1]
    
    netinfo = board.FindNet(netname)
    return netinfo.GetNet()


class commands:
    classinstance = None
    def NEWNET(self,netname):
        """Create a new net with name netname."""

        board = _user_stacks['Board'][-1] 

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
    NEWNET.nargs = 1
    NEWNET.category = 'Draw'
    
    def getpads(self,items):
        """[MODULES] Get pads of each module in MODULES."""
        items = items[0]
        p = []
        for i in items:
            p.extend(list(i.Pads()))
        return p            
    getpads.nargs = 1
    getpads.category = 'Elements'
    
    def select(self,items):
        '[objects] Select the objects'
        filter(lambda x: x.SetSelected(), items[0])
    select.nargs = 1
    select.category = 'Action'
    
    def deselect(self,items):
        '[objects] Deselect the objects'
        filter(lambda x: x.ClearSelected(), items[0])
    deselect.nargs = 1
    deselect.category = 'Action'
    
    def pads(self,empty):
        """Get all pads"""
        p=[]
        for m in _user_stacks['Board'][-1].GetModules():
            p.extend(list(m.Pads()))
        return p
    pads.nargs = 0
    pads.category = 'Elements'
    
    def AREAS(self,empty):
        """Return all Areas of the board (includes Zones and Keepouts)."""
        b = _user_stacks['Board'][-1]
        return [b.GetArea(i) for i in range(b.GetAreaCount())]
        
    AREAS.nargs = 0
    AREAS.category = 'Elements,Area'

    def ZONES(self,ignore):
        """Return all Zones of the board."""
        b = _user_stacks['Board'][-1]
        return filter(lambda c: not c.IsKeepout(),[b.GetArea(i) for i in range(b.GetAreaCount())])
    ZONES.nargs = 0
    ZONES.category = 'Elements,Area'
    # Example: clear toptextobj selected copy GetThickness call list swap topoints pairwise F.SilkS tosegments copy 2 pick SetWidth callargs pop F.Cu tocopper
    # : texttosegments "Draw [TEXTOBJLIST LAYER] Copies text objects in TEXTOBJLIST to LAYER." swap copy GetThickness call list swap topoints pairwise swap tosegments copy 2 pick SetWidth callargs pop ;
    
    
    # : texttosegments "Draw [TEXTOBJLIST LAYER] Copies text objects in TEXTOBJLIST to LAYER." swap copy GetThickness call list swap topoints pairwise 2 pick tosegments copy 2 pick SetWidth callargs pop swap pop swap pop ;
    
    # Usage: clear toptextobj selected Dwgs.User texttosegments F.Cu tocopper
    def TOPOINTS(self,itemlist):
        """[EDA_TEXTLIST] a list of EDA_TEXT items, which are converted to point pairs suitable for TODRAWSEGMENTS"""
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
    TOPOINTS.nargs = 1
    TOPOINTS.category = 'Draw,Geometry'
    
    def pairwise(self,iterable):
        "s -> (s0, s1), (s2, s3), (s4, s5), ..."
        valuelist = []
        #print('iterable: ',iterable)
        for item in iterable[0]:
            a = iter(item)
            valuelist.append(list(zip(a, a)))
        return valuelist
    pairwise.nargs = 1
    pairwise.category = 'Conversion'
    
    def KEEPOUTS(self,empty):
        """Return all Keepouts of the board."""
        b = _user_stacks['Board'][-1]
        return filter(lambda c: c.IsKeepout(),[b.GetArea(i) for i in range(b.GetAreaCount())])
    KEEPOUTS.nargs = 0
    KEEPOUTS.category = 'Elements,Area'
    
    def AREACORNERS(self,arealist):
        """Area Corners."""
        b=_user_stacks['Board'][-1]
        areacorners = [[a.GetCornerPosition(i) 
            for i in range(a.GetNumCorners())] 
                for a in arealist[0]]
        return areacorners
    AREACORNERS.nargs = 1
    AREACORNERS.category = 'Geometry,Area'
    # Test:
    # "m 81.38357,74.230848 5.612659,1.870887 5.211757,3.474503 2.138156,2.138157 10.958048,-6.1472 0.53454,5.078121 -1.06908,4.009044 -2.80633,4.276312 -2.539056,1.603616 1.202716,4.276312 9.48806,-2.939963 13.36348,8.686253 -8.95353,-0.4009 -2.13815,5.34539 -5.21176,-2.67269 -4.67722,4.54358 -2.40542,-3.0736 -4.009046,6.94901 -3.741775,4.27631 -4.142676,2.53906 1.870887,3.34087 v 3.34087 l -4.409948,2.53906 h -2.806329 l -2.80633,-0.53454 -0.267271,-2.00452 1.469982,-1.60362 0.668176,-0.4009 -0.53454,-1.73726 -4.142676,0.53454 -4.677217,-0.93544 -3.34087,-0.66817 -1.336347,-0.13364 -2.405428,3.87541 -1.469982,1.33635 -1.603616,0.66817 -5.479026,-0.66817 -2.405425,-2.80633 -0.133636,-1.60362 3.207235,-3.34087 1.870887,-2.53906 -2.80633,-2.93996 -2.672696,-4.40995 -0.668174,-2.40543 -4.409945,5.47903 -3.207234,-5.34539 -5.078121,2.13815 -3.474506,-6.14719 -8.285356,0.26726 13.229844,-8.418985 10.022607,4.81085 0.400905,-5.34539 -3.741775,-2.138156 -2.405425,-3.474503 -0.668173,-3.073601 v -7.884451 l 13.363474,5.078121 3.608139,-2.939965 5.211757,-2.271789 3.875408,-1.33635 2.138156,0.133636 3.207234,-3.474503 4.677217,-2.939965 2.405425,-0.668174 z" 1 mm fromsvg drawpoly
    # https://www.w3.org/TR/SVG11/paths.html#PathDataGeneralInformation

    def fromsvg(self,inputs):
        """[PATH_D_ATTRIBUTE SCALE] Converts SVG path element d attribute
            to a list of coordinates suitable for drawelements. Applies SCALE
            to all coordinates."""
        #print(path)
        path = inputs[0]
        scale = inputs[1]
        tokens = ['']
        for char in path:
            if char in '0123456789-+.':
                tokens[-1] += char
                continue
            if tokens[-1]:
                tokens.append('')
            if char not in ' ,':
                tokens[-1] += char
        position = [0.0,0.0]
        currenttoken = 0
        listresult = []
        #print(tokens)
        scale = float(scale)
        while currenttoken < len(tokens):
            token = tokens[currenttoken]
            try: 
                x = float(token)*scale
                currenttoken += 1
                y = float(tokens[currenttoken])*scale
                currenttoken += 1
                position[0] += x
                position[1] += y
                listresult[-1].append((position[0],position[1]))
                continue
            except:
                if token == 'm':
                    currenttoken += 1
                    position[0] = float(tokens[currenttoken])*scale
                    currenttoken += 1
                    position[1] = float(tokens[currenttoken])*scale
                    currenttoken += 1
                    listresult.append([(position[0],position[1])])
                    continue
                if token == 'l':
                    currenttoken += 1
                    position[0] += float(tokens[currenttoken])*scale
                    currenttoken += 1
                    position[1] += float(tokens[currenttoken])*scale
                    currenttoken += 1
                    #position = pcbnew.wxPoint(x,y)
                    listresult[-1].append((position[0],position[1]))
                    continue
                if token == 'h':
                    currenttoken += 1
                    position[0] += float(tokens[currenttoken])*scale
                    currenttoken += 1
                    listresult[-1].append((position[0],position[1]))
                    continue
                if token == 'v':
                    currenttoken += 1
                    position[1] += float(tokens[currenttoken])*scale
                    currenttoken += 1
                    listresult[-1].append((position[0],position[1]))
                    continue
                if token == 'z':
                    currenttoken += 1
                    listresult[-1].append(listresult[-1][0])
                    continue
                output('Bad SVG token: %s'%token)
        return listresult
    fromsvg.nargs = 2
    fromsvg.category = 'Geometry,Conversion'
    
    def tocommand(self,elementlist,commandname):
        """[ELEMENTLIST COMMANDNAME] Generate a command named COMMANDNAME that 
           draws the elements in ELEMENTLIST."""
        kicommand.run(': %s "Draw Custom Drawing Command"'%commandname)
        for element in elementlist:
            s,e = element.GetStart(), element.GetEnd()
            kicommand.run('%f,%f,%f,%f drawpoly'%(s[0],s[1],e[0],e[1]))
        kicommand.run(';')
    tocommand.nargs = 2
    tocommand.category = 'Programming,Elements'
    
    def REJOIN(self,empty):
        'Using selected lines, move multiple connected lines to the isolated line.'
        # Moves the set of coniguous lines or tracks to match the single line already moved.
        run('drawings copytop selected')
        # lines = stack[-1]
        # if len(lines) <=2:
            # return
        # for line in lines:
            # output( "Selected:", line.GetStart(), line.GetEnd())
        # if isinstance(lines[0],pcbnew.TRACK):
            # run('tracks')
        # elif isinstance(lines[0],pcbnew.DRAWSEGMENT):
            # run('drawings drawsegment filtertype')
        # else:
            # return
            
        # run('swap connected')
        
        #run('copy copy GetStart call swap GetEnd call append')
        
        # Stack is now: CONNECTED StartAndEndPoints
        # recast the end points as tuples
        lines_by_vertex = defaultdict(set) #{}
        for line in stack[-1]:
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
        for line in stack[-1]:
            if len(lines_by_vertex[(line.GetStart().x,line.GetStart().y)]) == 1 \
               and len(lines_by_vertex[(line.GetEnd().x,line.GetEnd().y)]) == 1:
                lonely_line.append(line)
            else:
                connected_lines.append(line)
        stack.pop()
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
        output( type(list(lines_by_vertex[lonely_vertices[0]])[0]))
        vector = lonely_line.GetStart() - list(lines_by_vertex[lonely_vertices[0]])[0].GetEnd()
        output( "Moving by",vector)
        for line in connected_lines:
            output( '\t',line.GetStart(),line.GetEnd())
            line.Move(vector)
            
        # match lonely_line vertices to each of the other vertices by orientation
        
        
        # find the vertices with only one line coincident.
        # One of these is the lonely line, the other two are the polygon opening.
        # Match topmost or left most coordinates of the lonely line to the opening.
        # Now we have the vector of the Move, so Move the remaining lines.
    REJOIN.nargs = 0
    REJOIN.category = 'Action',

    
    def printf(self, *arglist):
        'Output [LISTOFLISTS FORMAT] Output each list within LISTOFLISTS formatted according to FORMAT in Pythons {} string format (https://www.python.org/dev/peps/pep-3101/).'
        print('Format:',arglist[0][1])
        
        
        for item in arglist[0][0]:
            print ("item:",item)
            output(arglist[0][1].format(*item))
            
    def fprintf(self, *arglist):
        'Output [LISTOFLISTS FORMAT FILENAME] Output to FILENAME each list within LISTOFLISTS formatted according to FORMAT in Pythons {} string format (https://www.python.org/dev/peps/pep-3101/).'
        arglist = arglist[0]
        #print('Format:',arglist[1])
        filename = os.path.join(os.getcwd(),arglist[2])
        with open(filename,'w') as f: 
            for item in arglist[0]:
                #print("item:",item)
                f.write(arglist[1].format(*item))
        
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
        os.chdir(PROJECTPATH)
        
    def regex(self, *arglist):
        'Comparison [LIST REGEX] Create a LIST of True/False values corresponding to whether the values in LIST match the REGEX (for use prior to FILTER)'
        stringlist, regex_ = arglist[0]
        #print(stringlist, regex_)
    # Format of comment is: 'Category [ARGUMENT1 ARGUMENT2] Description'
        prog = re.compile(regex_)
        return map(lambda s: prog.match(s),stringlist)
#        '=': Command(2,lambda c: map(lambda x: x==c[1],c[0]),'Comparison',
    def callargs(self,*c):
        'Call [OBJECTLIST ARGLISTOFLISTS FUNCTION] Execute python FUNCTION on each member '
        'of OBJECTLIST with arguments in ARGLISTOFLISTS. ARGLISTOFLISTS can be '
        'a different length than OBJECTLIST, in which case ARGLISTOFLISTS '
        'elements will be repeated (or truncated) to match the length of '
        'OBJECTLIST. Returns the list of results in the same order as the '
        'original OBJECTLIST. The commands LIST and ZIP2 will be helpful '
        'here. ARGLISTOFLISTS can also be a single list or a single value, '
        'in which case the value will be converted to a list of lists.'
        c = c[0]
        #print(c)
        args = c[1]
        
        if hasattr(args,'__getitem__'):
            if not hasattr(args[0],'__getitem__'):
                args = [args]
        else:
            args = [[args]]
            
        return map(lambda x: 
            getattr(x[0],c[2])(*(x[1])), 
            zip(c[0], cycle(args))
            )

################## END OF COMMANDS CLASS ###########################
            
    #modules copy GetReference call .*EF.* regex isnotnone filter Reference call false SetVisible callargs
    #modules *.EF.* regexref refobj clearvisible
    #'help': Command(0,lambda c: HELPMAIN(),'Help', "Shows general help"),
    
commands.classinstance = commands()
# added for python3: "not x.startswith('__') and "
for c in filter(lambda x: not x.startswith('__') and hasattr(getattr(commands,x), '__call__'),dir(commands)):
    f = getattr(commands.classinstance,c)
    if hasattr(f,'category'):
        _dictionary ['command'][c.lower()] = Command(f.nargs,f,f.category,f.__doc__)
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
        _dictionary ['command'][c.lower()] = Command(nargs,f,category,doc)


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
    b = _user_stacks['Board'][-1]
    d=b.GetDrawings().Remove
    t=b.GetTracks().Remove
    m=b.GetModules().Remove
    access = ((pcbnew.TRACK,t),(pcbnew.MODULE,m),(object,d))    
    for item in items:
        for inst,remove in access:
            output(str(inst),str(remove))
            if isinstance(item,inst):
                remove(item)
                continue

    
def TOCOPPER(*c):
    objects,layer = c
    board = _user_stacks['Board'][-1]
    try:
        layerID = int(layer)
    except:
        layerID = board.GetLayerID(str(layer))
        
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

import inspect
USERSAVEPATH = os.path.join(os.path.expanduser('~'),'kicad','kicommand')
os.chdir(USERSAVEPATH)

KICOMMAND_MODULE_DIR = os.path.dirname(inspect.stack()[0][1])
LOADABLE_DIR = os.path.join(KICOMMAND_MODULE_DIR,'loadable')
USERLOADPATH = USERSAVEPATH+':'+LOADABLE_DIR
PROJECTPATH = os.path.dirname(pcbnew.GetBoard().GetFileName())
# for i in range(len(inspect.stack())):
    # print(i,inspect.stack()[i][1])
    
def LOAD(name,path=USERLOADPATH):
    for p in path.split(':'):
        new_path = os.path.join(p, name)
        if not os.path.isfile(new_path):
            continue
        with open(new_path,'r') as f: run(f.read())

def SAVE(name):
    dictname = 'user'
    if not os.path.exists(USERSAVEPATH):
        os.makedirs(USERSAVEPATH)
        output('created ~/kicad/kicommand')
    output("saving to %s"%name)
    new_path = os.path.join(USERSAVEPATH, name)
    with open(new_path,'w') as f:
        commands = _dictionary[dictname].iteritems()
        for command,definition in sorted(commands,key=lambda x:x[0]):
            f.write( ": %s %s ;\n"%(command,_dictionary[dictname][command]))

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
    sorted = list(_command_dictionary.keys())
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
    seealso = v.helptext.split()[-1].split(',')
    if len(seealso) > 1:
        seealso = '\n\n\tSEE ALSO: {}'.format(', '.join(seealso))
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
    # commands = filter(lambda c: c[1].category == 'Help', _command_dictionary.iteritems())
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
        commands = _command_dictionary.iteritems()
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
            output( '{:<{width}} - {}'.format(cat,' '.join(cbyc[cat]), width=catlen))
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
            
def floatnoerror(value):
    try:
        return float(value)
    except:
        return value
def intnoerror(value):
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
            foundkv = _command_dictionary.iteritems()
            command_by_category = defaultdict(list) #{}
            for command,val in _command_dictionary.iteritems():
                #command_by_category.setdefault(val.category,[]).append(command)
                command_by_category[val.category].append(command)
                
            for category,commands in sorted(command_by_category.iteritems(),key=lambda x:x[0]):
                output('%11s: %s\n'%(category,' '.join(commands))),
            return
            # foundkv = sorted(foundkv,key=lambda x: x[1].category)
            # foundkv = filter(lambda x: x[2].find(text)!=-1,_command_dictionary.iteritems())
        
        if text:
            if exact:
                foundkv = text,_command_dictionary.get(text,None)
            else:
                foundkv = filter(lambda x: x[0].find(text)!=-1,_command_dictionary.iteritems())
        else:
            foundkv = _command_dictionary.iteritems()
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



_command_dictionary.update({
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
    
    
    'pcbnew': Command(0,lambda c: pcbnew,'Elements',
        'Get the python base object for PCBNEW'),
    'getboard': Command(0,lambda c: pcbnew.GetBoard(),'Elements',
        'Get the loaded Board object'),
    # boardpush can be done with "[BOARD Object] Board spush"
    # boardpop can be done with "Board spop"
    # 'boardpush': Command(1,lambda c: _user_stacks['Board'].append(c[0]),'Elements',
        # '[BOARD] Add board to Board stack. This is the new default Board object for many commands'),
    # 'boardpop': Command(0,lambda c: _user_stacks['Board'].pop(),'Elements',
        # 'Remove last board from Board stack and place on the stack. The previous default board becomes the new default Board object for many commands'),
    'board': Command(0,lambda c: _user_stacks['Board'][-1],'Elements',
        'Get the default Board object for many commands'),
    'modules': Command(0,lambda c: _user_stacks['Board'][-1].GetModules(),'Elements',
        'Get all modules of the default board'),
    'tracks': Command(0,lambda c: _user_stacks['Board'][-1].GetTracks(),'Elements',
        'Get all tracks (including vias) of the default board'),
    'drawings': Command(0,lambda c: _user_stacks['Board'][-1].GetDrawings(),'Elements',
        'Get all top-level drawing objects (lines and text) of the default board'),
#    'toptext': Command(0,lambda c: filter(lambda x: isinstance(x,pcbnew.EDA_TEXT),_user_stacks['Board'][-1].GetDrawings()),'Elements'),
# 'copy IsSelected call filter'
    # PCB Element Attributes
    'selected': Command(1,lambda c: filter(lambda x: x.IsSelected(), c[0]),'Attributes',
        '[objects] Get selected objects '),
    'notselected': Command(1,lambda c: filter(lambda x: not x.IsSelected(), c[0]),'Attributes',
        '[objects] Get unselected objects '),
    'attr': Command(2,lambda c: map(lambda x: getattr(x,c[1]), c[0]),'Attributes',
        '[objects attribute] Get specified python attribute of the objects' ),
    # want this to work where c[1] is a value or list. If list, then member by member.
    #'index': Command(2,lambda c: map(lambda x: x[c[1]], c[0]),'Attributes',
    'sindex': Command(2,lambda c: c[0][c[1]],'Attributes',
       '[DICTIONARYOBJECT STRINGINDEX] Select an item in the list of objects based on string INDEX'),

    'index.': Command(2, lambda c: map(lambda x: x[int(c[1])],c[0]), 'Conversion',
        '[LISTOFLISTS INDEX] return a list made up of the INDEX item of each list in LISTOFLISTS'),
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
    'ends': Command(1, lambda c: get_ds_ends(*c),'Geometry',
        'Get the end points of the drawsegment (works with segment and arc types'),
    'connected': Command(2,lambda c: CONNECTED(*c),'Filter',
        '[WHOLE INITIAL] From objects in WHOLE, return those that are connected to objects in INITIAL (recursevely)'),
    'matchreference': Command(2,lambda c: filter(lambda x: x.GetReference() in c[1].split(','), c[0]),'Filter',
        '[MODULES REFERENCE] Filter the MODULES and retain only those that match REFERENCE'),
    
    'extend': Command(2,lambda c: c[0].extend(c[1]) or c[0],'Stack',
        '[LIST1 LIST2] Join LIST1 and LIST2. append,concat'),
        
    'filter': Command(2,lambda c: list(compress(c[0], c[1])),'Filter', # filter op1 by bool op2
        '[LIST1 TF_LIST] Retain objects in LIST1 where the corresponding value in TF_LIST is True, not None, not zero, and not zero length'),
    #'<': Command(2,lambda c: [c[0][i] for i,x in enumerate(c[1]) if x<float(c[2]))
    '<': Command(2,lambda c: map(lambda x: float(x)<float(c[1]),c[0]),'Comparison',
        '[LIST VALUE] Create a LIST of True/False values corresponding to whether the values in LIST are less than VALUE (for use prior to FILTER)'),
    'filtertype': Command(2,lambda c: filter(lambda x:isinstance(x,getattr(pcbnew,c[1])),c[0]),'Comparison',
        '[LIST TYPE] Retains objects in LIST that are of TYPE' ),
    'istype': Command(2,lambda c: filter(lambda x:isinstance(x,getattr(pcbnew,c[1])),c[0]),'Comparison',
        '[LIST TYPE] Create a LIST of True/False values corresponding to whether '
        'the values in LIST are of TYPE (for use prior to FILTER). '
        'TYPE must be an attribute of pcbnew.' ),
    '=': Command(2,lambda c: map(lambda x: x==c[1],c[0]),'Comparison',
        '[LIST VALUE] Create a LIST of True/False values corresponding to whether the values in LIST equal to VALUE (for use prior to FILTER)'),
    'isnone': Command(1,lambda c: map(lambda x: x is None,c[0]),'Comparison',
        '[LIST VALUE] Create a LIST of True/False values corresponding to whether the values in LIST equal to None (for use prior to FILTER)'),
    'isnotnone': Command(1,lambda c: map(lambda x: x is not None,c[0]),'Comparison',
        '[LIST VALUE] Create a LIST of True/False values corresponding to whether the values in LIST is not  None (for use prior to FILTER)'),
#x=lambda c: map(lambda x: float(x),c.split(',')) if isinstance(c,basestring) else map(lambda x: float(x),c)
    'undock': Command(0,lambda c: UNDOCK(*c),'Interface',
        'Undock the window.'),
    'spush': Command(2,lambda c: _user_stacks[c[1]].append(c[0]),'Programming',
        '[STACK] [VALUE] Push VALUE onto the named STACK.'),
    'spop': Command(1,lambda c: _user_stacks[c[0]].pop(),'Programming',
        '[STACK] Pop the top of the user STACK onto the main stack.'),
    'scopy': Command(1,lambda c: _user_stacks[c[0]][-1],'Programming',
        '[STACK] Copy the top of the user STACK onto the main stack.'),
    'stack': Command(0,lambda c: STACK(*c),'Programming',
        'Output the string representation of the objects on the stack'),
    'print': Command(0,lambda c: PRINT(*c),'Programming',
        'Output the string representation of the top object on the stack'),
    'builtins': Command(0,lambda c:  __builtins__,'Programming',
        'Output the __builtins__ Python object, giving access to the built in Python functions.'),
    
    # 'getstart': Command(1,lambda c: [m.GetStart() for m in c[0]],'Call',
        # '[LIST] Get the start wxPoint from the LIST of DRAWSEGMENTS.'),
    # 'getend': Command(1,lambda c: [m.GetEnd() for m in c[0]],'Call',
        # '[LIST] Get the end wxPoint from the LIST of DRAWSEGMENTS.'),
    'calllist': Command(2,lambda c: CALLLIST(*c),'Call',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST.'
        'The FUNCTION must return a list of items (this is suitable'
        'for module functions such as GraphicalItems and Pads.'),
    'fcall': Command(1,lambda c: map(lambda x: x(), c[0]),'Call',
        '[FUNCTIONLIST] Execute each python function in the FUNCTIONLIST on each member of LIST. Return the list of results in the same order as the original LIST.'),
    'fcallargs': Command(2,
                lambda c: 
                map(lambda x: 
                        x[0](*(x[1])), 
                        zip(c[0], cycle(c[1]))
                   )
                ,'Call',
        '[FUNCTIONLIST ARGLISTOFLISTS] Execute each python function in the'
        'FUNCTIONLIST on each member of that list with arguments in ARGLISTOFLISTS.' 'ARGLISTOFLISTS can be '
        'a different length than OBJECTLIST, in which case ARGLISTOFLISTS '
        'elements will be repeated (or truncated) to match the length of '
        'OBJECTLIST. Returns the list of results in the same order as the '
        'original OBJECTLIST. The commands LIST and ZIP2 will be helpful '
        'here.'),
 
    
    'call': Command(2,lambda c: map(lambda x: getattr(x,c[1])(), c[0]) 
        # if hasattr(c[0],'__getitem__') and hasattr(c[0][0],'__getitem__') else 
        # map(lambda x: getattr(x,c[1])(), [c[0]])
        # if hasattr(c[0],'__getitem__') else  
        # map(lambda x: getattr(x,c[1])(), [[c[0]]])
        ,'Call',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Return the list of results in the same order as the original LIST.'),
    'callfilter': Command(2,lambda c: filter(lambda x: getattr(x,c[1])(), c[0]),'Call',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Return results that return True.'),
    'callnotfilter': Command(2,lambda c: filter(lambda x: not getattr(x,c[1])(), c[0]),'Call',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Return results that return False.'),
    # 'callargs': Command(3,
                # lambda c: 
                # map(lambda x: 
                        # getattr(x[0],c[2])(*(x[1])), 
                        # zip(c[0], cycle(c[1]))
                   # )
                # ,'Call',
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
    # r('clear referencetextobj valuetextobj moduletextobj append append copy GetTextBox call corners swap copy GetCenter call swap copy GetParent call Cast call GetOrientationDegrees call swap GetTextAngleDegrees call +l rotatepoints drawpoly')
    # # Outline the pads. Might be a problem with "bounding box" being orthogonal when pad is rotated.
    # r('clear pads copy GetBoundingBox call corners swap copy GetCenter call swap GetOrientationDegrees call rotatepoints drawpoly')
    '+.': Command(2,lambda c:
            [float(a)+float(b) for a,b in zip(c[0], cycle(c[1]))],'Numeric',
        '[LIST1 LIST2] Return the the floating point LIST1 + LIST2 member by member.'),
    '*.': Command(2,lambda c:
            [float(a)*float(b) for a,b in zip(c[0], cycle(c[1]))],'Numeric',
        '[LIST1 LIST2] Return the the floating point LIST1 * LIST2 member by member.'),
    '+': Command(2,lambda c:
            float(c[0])+float(c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 + OPERAND2.'),
    '-': Command(2,lambda c: float(c[0])-float(c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 - OPERAND2.'),
    '*': Command(2,lambda c: float(c[0])*float(c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 * OPERAND2.'),
    '/': Command(2,lambda c: float(c[0])/float(c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 / OPERAND2.'),
    'sum': Command(1, lambda c: sum(*c), 'Numeric', 
        '[LIST] Return the sum of all members in LIST.'), 
    
    # 'sum': Command(1,
       # lambda c: floatnoerror(c[0]) if isinstance(c[0],basestring) \
       # and c[0].find(',') == -1 else sum(map(lambda x: floatnoerror(x),
       # c[0].split(','))
       # if isinstance(c[0],basestring) else sum(c[0])) 
       # if hasattr(c[0],'__iter__') else floatnoerror(c[0]),

    # 'Numeric',
        # '[LIST] Return the sum of all members in LIST.'),

    # Stack Manipulation
    'concat': Command(2,lambda c: c[0]+c[1],'Stack',
        '[LIST1 LIST2] Return LIST1 and LIST2 concatenated together. append,extend'),
    'append': Command(2,lambda c: c[0].append(c[1]) or c[0],'Stack',
        '[LIST ITEM] Add ITEM to the end of LIST. If ITEM is a list, then it is added as a list. Use concat or extend for other options. extend,concat'),
    #'copytop': Command(0,lambda c: list(stack[-1])),
    # 'copytop': Command(0,lambda c: stack[-1],'Stack',
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
                       lambda c: floatnoerror(c[0]) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: floatnoerror(x),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list. OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
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
                       lambda c: intnoerror(c[0]) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: intnoerror(x),
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
    'ilist': Command(1,lambda c: list(c[0]),'Conversion',
        '[ITERABLE] Make list from ITERABLE where each item is a member of ITERABLE.'),
    'list': Command(1,lambda c: [c[0]],'Conversion',
        '[OBJECT] Make OBJECT into a list (with only OBJECT in it).'),
    'delist': Command(1,lambda c: c[0][0],'Conversion',
        '[LIST] Output index 0 of LIST.'),

    #'swap': Command(2,retNone(lambda c: stack[-1],stack[-2]=stack[-2],stack[-1])),
    # 'pick': Command(1,lambda c: stack.insert(-int(stack[-1])-1,stack[-2]),'Stack',
    #works: 'pick': Command(1,lambda c: stack.insert(-1,stack[len(stack)-int(c[0])-2]),'Stack',
    'pick': Command(1,lambda c: stack.insert(-1,stack[-int(c[0])-2]),'Stack',
        '[NUMBER] Copy the value that is NUMBER of objects deep in the stack to the top of the stack. '
        '\n\tExamples:\n\t0 pick - copies the top of the stack.\n'
        '\t1 pick - pushes a copy of the second item from the top of the stack onto the top of the stack.\n'
        ),
    'swap': Command(0,lambda c: SWAP(*c),'Stack',
        'Switches the two top objects on the stack.'),
    'zip2': Command(2,lambda c: zip(*c),'Stack',
        '[LIST1 LIST2] Creates a list with parallel objects in LIST1 and '
        'LIST2 together at the same index. ,zip'),
    'zip': Command(1,lambda c: zip(*c[0]),'Stack',
        '[LISTOFLISTS] Creates a list with parallel objects formed by each list '
        'in LISTOFLISTS ((1,2,3)(4,5,6)(7,8,9)) -> ((1,4,7)(2,5,8)(3,6,9)). ,zip2'
        ),
    ':': Command(0,lambda c: setcompilemode(True),'Programming',
        'Begin the definition of a new command. This is the only command in '
        'which arguments occur after the command. Command definition ends with '
        'the semicolon (;). Run command SEEALL for more examples. Special commands are'
        "Delete all commands ': ;'. Delete a command ': COMMAND ;"
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
        '[SEGMENTLIST DEGREES] Rotate segments by DEGREES around calculated '
        'average center.'),
        
    'corners': Command(1,lambda c: CORNERS(*c),'Geometry',
        "[OBJECT] OBJECT is either a single object or a list of objects. "
        "Converts each OBJECT, either EDA_RECT or OBJECT's BoundingBox "
        "into vertices appropriate for drawpoly."
        ),
    
    'tocopper': Command(2,lambda c: TOCOPPER(*c),'Layer',
        "[DRAWSEGMENTLIST LAYER] put each DRAWSEGMENT on the copper LAYER."),
    
    'layernums': Command(1,lambda c: [_user_stacks['Board'][-1].GetLayerID(x) for x in c[0].split(',')],'Layer',
        '[STRING] Get the layer numbers for each layer in comma separated STRING. '
        'STRING can also be one number, if desired.'),
    'onlayers':  Command(2,lambda c: filter(lambda x: set(x.GetLayerSet().Seq()).intersection(set(c[1])),c[0]),'Layer',
        '[LIST LAYERS] Retains the objects in LIST that exist on any of the LAYERS.'),
    'setlayer': Command(2,lambda c: map(lambda x: x.SetLayer(layer(c[1])),
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
        'Returns the current system time as a string.'),
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
        '[SEGMENTLIST GRID] Move points of SEGMENTLIST to be a multiple of GRID.'),
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
    'drawarctest':Command(1,lambda c: draw_arc(50*pcbnew.IU_PER_MM,50*pcbnew.IU_PER_MM,radius,angle,layer=_user_stacks['drawparams']['l'],thickness=_user_stacks['drawparams']['t']),'Draw',
        ""),
    'drawarc':Command(2,lambda c: draw_arc(c[0][0],c[0][1],c[0][2],c[0][3],c[1],layer=_user_stacks['drawparams']['l'],thickness=_user_stacks['drawparams']['t']),'Draw',
        "[STARTX,STARTY,CENTERX,CENTERY DEGREES] Draw an arc with the given parameters. Layer and Thickness are taken from the draw parameters (see params command)"),
    'remove':Command(1,lambda c: REMOVE(*c),'Layer',
        '[OBJECTORLIST] remove items from board. Works with any items in Modules, Tracks, or Drawings.'),
    'tosegments':Command(2,lambda c: tosegments(*c),'Layer',
        '[LIST LAYER] copy tracks or point pairs in LIST to drawpoly on LAYER. Copies width of each track.'),
    'drawpoly':Command(1,lambda c: draw_segmentlist(c[0],layer=_user_stacks['drawparams']['l'],thickness=_user_stacks['drawparams']['t']),'Draw',
        "[POINTSLIST] Points list is interpreted as pairs of X/Y values. Line segments are"
        "drawn between all successive pairs of points, creating a connected sequence of lines "
        "where each point is a vertex in a polygon "
        "as opposed to being just a list of line segments or point pairs. "
        "This command uses previously set drawparams and the points are in native units (nm) so using mm or mils commands is suggested."),
    'drawtext': Command(2,lambda c: draw_text(c[0],c[1],[_user_stacks['drawparams']['w'],_user_stacks['drawparams']['h']],layer=_user_stacks['drawparams']['l'],thickness=_user_stacks['drawparams']['t']),'Draw',
        '[TEXT POSITION] Draws the TEXT at POSITION using previously set drawparams. Position is in native units (nm) so using mm or mils commands is suggested.'),
    'drawparams': Command(2,lambda c: DRAWPARAMS(c),'Draw',
        '[THICKNESS,WIDTH,HEIGHT LAYER] Set drawing parameters for future draw commands.\n'
        'Example: 1,5,5 mm F.Fab drawparams'),
    'showparam': Command(0,lambda c: _user_stacks['drawparams'],'Draw',
        'Return the draw parameters.'),
    'findnet': Command(1,lambda c: FINDNET(*c),'Draw','[NETNAME] Returns the netcode of NETNAME.'),
    'param': Command(2,lambda c: PARAM(*c),'Draw',
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

        
    # 'vias': filter(lambda x:isinstance(x,pcbnew.VIA),_command_dictionary['tracks']),
    # 'vias_class': filter(lambda x:pcbnew.VIA_Classof(x),_command_dictionary['tracks']),
})

_newcommanddictionary = None
_compile_mode = False
def setcompilemode(val=True, dictionary='user'):
    global _compile_mode
    global _newcommanddictionary
    _newcommanddictionary = dictionary
    _compile_mode=val
    
"""Tracks whether compile mode is on, allowing new command definitions.
   This is affected by the commands : and ;"""
_command_definition = []
_user_dictionary = _dictionary['user']

_user_stacks = defaultdict(list)

_user_stacks['drawparams'] = { 
                                't':0.3*pcbnew.IU_PER_MM,
                                'w':1*pcbnew.IU_PER_MM,
                                'h':1*pcbnew.IU_PER_MM,
                                'l':pcbnew.Dwgs_User, 
                                'zt':pcbnew.ZONE_CONTAINER.NO_HATCH,
                                'zp':0
                             }
                             
_user_stacks['Board'].append(pcbnew.GetBoard())

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
#    'not': Command(0,lambda c: run('0 FLOAT ='),'Comparison'),

#output( 'ops',str(stack))
def printcategories():
    result=defaultdict(set)
    for key,val in _command_dictionary.iteritems():
        result[val.category].add(key)
    
    for key,val in result.iteritems():
        output( key)
        output( '\t','\n\t'.join(val))
        
pshapesactual = filter(lambda x: x.startswith('PAD_SHAPE_'),dir(pcbnew))
pshapes = ['PAD_SHAPE_CIRCLE','PAD_SHAPE_OVAL', 'PAD_SHAPE_RECT', 'PAD_SHAPE_ROUNDRECT', 'PAD_SHAPE_TRAPEZOID']

if Counter(pshapesactual) != Counter(pshapes):
    try:
        output( 'Warning! Expected Pad Shapes are different than KiCommand expects.')
    except:
        pass


def pad_to_drawsegment(pad):
    #ds_shapes=['S_ARC', '', 'S_CURVE', 'S_LAST', 'S_POLYGON', '', 'S_SEGMENT']
    #p_shapes=['','', '', '', '']

    pshape2ds = {
        pcbnew.PAD_SHAPE_CIRCLE:pcbnew.S_CIRCLE,
        pcbnew.PAD_SHAPE_RECT:pcbnew.S_RECT,
        pcbnew.PAD_SHAPE_ROUNDRECT:pcbnew.S_RECT,
        pcbnew.PAD_SHAPE_OVAL:pcbnew.S_RECT,
        pcbnew.PAD_SHAPE_TRAPEZOID:pcbnew.S_RECT,
    }
    board = _user_stacks['Board'][-1]
    ds=pcbnew.DRAWSEGMENT(board)
    board.Add(ds)
    layer = _user_stacks['drawparams']['l']
    try:
        layerID = int(layer)
    except:
        layerID = _user_stacks['Board'][-1].GetLayerID(str(layer))

    ds.SetLayer(layerID) # TODO: Set layer number from string
    ds.SetWidth(max(1,int(_user_stacks['drawparams']['t'])))

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

    # viasbb_selected = filter(lambda x: isinstance(x,pcbnew.VIA_BLIND_BURIED),tracks_selected)
    # viasthrough_selected = filter(lambda x: isinstance(x,pcbnew.VIA_THROUGH),tracks_selected)
    # viasmicrovia_selected = filter(lambda x: isinstance(x,pcbnew.VIA_MICROVIA),tracks_selected)
    # viasnotdefined_selected = filter(lambda x: isinstance(x,pcbnew.VIA_NOT_DEFINED),tracks_selected)

    # toptext = filter(lambda x: isinstance(x,pcbnew.EDA_TEXT) and x.IsSelected(),_user_stacks['Board'][-1].GetDrawings())
    # moduleitems=[]
    # for m in _user_stacks['Board'][-1].GetModules():
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

    
# plugin = aplugin()
# aplugin.register(plugin)
# plugin.Run()

