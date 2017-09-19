import collections
from collections import defaultdict, Counter
from itertools import compress,izip, cycle
import pcbnew
import time
import os
import math
from textwrap import wrap
import wx
from wxpointutil import wxPointUtil
import kicommand_gui


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

# Clearly there are two types of statements that test values.
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
Command = collections.namedtuple('Command','numoperands execute category helptext')

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
            self.combolist.insert(0,commandstring)
            self.entrybox.SetItems(self.combolist)
            #self.entrybox.Append(commandstring)
            self.entrybox.SetFocus()
            #output(str(self.combolist))
            self.entrybox.Update()
        except Exception as e:
            wx.MessageDialog(self.GetParent(),"Error 1: %s"%str(e)).ShowModal()
            

class aplugin(pcbnew.ActionPlugin):
    """implements ActionPlugin"""
    g = None
    def defaults(self):
        self.name = "KiCommand"
        self.category = "Command"
        self.description = "Select, modify and interrogate pcbnew objects with a simple command script."
    def Run(self):
        parent =      \
            filter(lambda w: w.GetTitle().startswith('Pcbnew'), 
                   wx.GetTopLevelWindows()
            )[0]
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
        run('help')

def run(commandstring):

# Items beginning with single quote are entered onto the stack as a string (without the quote)
# Items beginning with double quote swallow up elements until a word ends in a double quote,
# and enters the entire item on the stack as a string (without the quotes)
# Commands beginning with ? are conditional. The top of the stack is popped,
# and if it was True, then the command is executed.

    global _operand_stack
    global _compile_mode
    global _command_definition
    global _user_dictionary
    global _dictionary
    #output( _command_dictionary.keys())
    #output( str(_operand_stack))
    
    commandlines = commandstring.splitlines()
    
    for commandstring in commandlines:
        commands = []
        qend = 0
        while True:
            qindex = commandstring.find('"',qend)
            if qindex != -1:
                # wx.MessageDialog(None,'PRE '+commandstring[qend:qindex-1]).ShowModal()
                commands.extend(commandstring[qend:qindex].split())
                qend = commandstring.find('"',qindex+1)
                if qend == -1:
                    raise SyntaxError('A line must contain an even number of double quotes.')
                commands.append(commandstring[qindex+1:qend])
                # wx.MessageDialog(None,'Q {'+commandstring[qindex+1:qend]+'}').ShowModal()
                qend += 1
            else:
                break
            
        # wx.MessageDialog(None,'END {'+commandstring[qend:]+'}').ShowModal()
        commands.extend(commandstring[qend:].split())
    # wx.MessageDialog(None,'{'+'}{'.join(commands)+'}').ShowModal()
    for command in commands:
        
        if command == ';':
            _compile_mode = False
            comm = _command_definition[:1]
            cdef = _command_definition[1:]
            output( "COMMAND %s DEFINITION %s"%(comm,cdef))
            if not comm: # delete all commands in the user dictionary: ': ;'
                _user_dictionary = {}
                continue
            comm = comm[0]
            if cdef: # delete a command in the user dictionary: ': COMMAND ;'
                _dictionary[_newcommanddictionary][comm] = ' '.join(cdef)
            else:
                del(_user_dictionary[_command_definition[0]])
            _command_definition = []
            continue

        if _compile_mode:
            _command_definition.append(command)
            continue
        
        if command.startswith("'"):
            _operand_stack.append(command[1:])
            continue
            
        found = False
        for dictname in ['user','persist']:
            if command in _dictionary[dictname]:
                run(_dictionary[dictname][command])
                found = True
                continue
        if found:
            continue
        if command not in _command_dictionary:
            _operand_stack.append(command)
            continue

        numop = _command_dictionary[command].numoperands
        result = _command_dictionary[command].execute(_operand_stack[-numop:])
        #output( '1: ',str(_operand_stack))
        if numop != 0:
            _operand_stack = _operand_stack[:-numop]
        #output( '2: ',str(_operand_stack))
        
        if result is None:
            #output( command,'result is None')
            continue
        #output( command,_command_dictionary[command].numoperands,'result is not None',str(_operand_stack), str(result))
        _operand_stack.append(result)
    #output( 'after command: ',str(_operand_stack))
    if len(_operand_stack):
        output( len(_operand_stack), 'operands left on the stack.' )
        
    pcbnew.UpdateUserInterface()
    return _operand_stack

def retNone(function,args):
    function(args)

def UNDOCK():
    aplugin.g.Float() #mgr.GetPane(text1).Float()
def STACK():
    for obj in _operand_stack:
        output(obj)
def PRINT():
    """print the top of the stack"""
    output(_operand_stack[-1])
        
def CLEAR():
    global _operand_stack
    _operand_stack = []
    return None
    
def SWAP():
    global _operand_stack
    _operand_stack[-1],_operand_stack[-2]=_operand_stack[-2],_operand_stack[-1]

def output(*args):

    for arg in args:
        aplugin.g.outputbox.AppendText(str(arg)+' ')
    aplugin.g.outputbox.AppendText('\n')
    return
    # Here's the simple 'print' definition of output
    for arg in args:
        print arg,
    print
    
def draw_segmentlist(input,layer=pcbnew.Eco2_User,thickness=0.015*pcbnew.IU_PER_MM):
    """Draws the vector (wxPoint_vector of polygon vertices) on the given
       layer and with the given thickness.
       close indicates whether the polygon needs to be closed
       (close=False means the last point is equal to the first point).
       The drawing will use this input to draw a closed polygon."""
    # input is either: string (of comma seperated points)
    # list of strings of comma separated points
    # list of wxPoint
    # list of lists of wxPoint

    if isinstance(input,basestring):
        input = input.split(',')
    # Now, input is an actual list
    # convert a list of strings (possibly comma separated) into a list of floats
    if isinstance(input[0],basestring):
        temp = []
        input = map(lambda y: float(y),map(lambda x: temp.extend(x),[i.split(',') for i in input]))
    # Now, input is a list of
    # 1) individual floats, 2) wxPoints, or 3) wxPoint lists
    if isinstance(input[0],float):
        a = iter(input)
        input = [[pcbnew.wxPoint(x,y) for x,y in izip(a, a)]]

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
    allsegments = []
    segments = []
    for shape in input:
        #for segment in shape:
        if isinstance(shape[0],(float,int)):
            a = iter(shape)
            shape = [pcbnew.wxPoint(int(x),int(y)) for x,y in izip(a, a)]
        for i in range(len(shape)-1):
            segments.append(draw_segment(
                shape[i][0],
                shape[i][1],
                shape[i+1][0],
                shape[i+1][1],
                layer=layer,
                thickness=thickness))
        allsegments.append(segments)
        segments = []
    return allsegments
# r('0 FLOAT LIST 0 FLOAT LIST 100 MM LIST 100 MM LIST APPEND APPEND APPEND DRAWSEGMENTS')
# r('0,0,100,100 MM DRAWSEGMENTS')
def REGULAR(dseglist):
    """create a regular polygon from the set of connected and closed segments"""
    ordered = order_segments(dseglist)
    
    for seg in dseglist:
        output( "s,e=",seg.GetStart(),seg.GetEnd())
    for seg in ordered:
        output( "ordered s,e=",seg.GetStart(),seg.GetEnd())

    sidelength = 0
    for seg in dseglist:
        sidelength += wxPointUtil.distance(seg.GetStart(),seg.GetEnd())

    # positive polarity is this end is common to the next seg.
    polarity = []
    e = ordered[0].GetEnd()
    for i in range(len(ordered)-1):
        sn = ordered[(i+1)%len(ordered)].GetStart()
        en = ordered[(i+1)%len(ordered)].GetEnd()        
        polarity.append((e[0] == sn[0] and e[1] == sn[1]) or (e[0] == en[0] and e[1] == en[1]))
        e = en
    polarity.append(polarity[0])
    numsides = len(dseglist)
    output( 'sides = ',numsides)
    sidelength = sidelength / numsides
    angle = 2*math.pi / numsides
    
    # get angle of first segment, use this as the starting angle
    # if positive polarity, end is the anchor
    

    
    angleincrement = 2*math.pi/numsides
    for i in range(len(ordered)-1):
        if polarity[i]:
            anchor = ordered[i].GetStart()
            free = ordered[i].GetEnd()
        else:
            anchor = ordered[i].GetEnd()
            free = ordered[i].GetStart()

         
        
        if i == 0:
            firstanchor = anchor
            vector = free - anchor
            startangle = -math.atan2(vector[1],vector[0]) # - is kicad angle polarity CCW
            #wxPointUtil.scale(vector*sidelength/mag(vector))

        angle = startangle+2*math.pi*i/numsides
        output( 'anchor,free,angle=',anchor,free,angle*180/math.pi)
        vector = wxPointUtil.towxPoint(sidelength,angle)

        endpoint = anchor+vector

        if polarity[i]:
            ordered[i].SetEnd(endpoint)  
            if i==0:
                output( 'setend')
        else:
            ordered[i].SetStart(endpoint)
            if i==0:
                output( 'setstart')
        if polarity[i+1]:
            ordered[i+1].SetStart(endpoint) 
            output( 'setstart')
        else:
            ordered[i+1].SetEnd(endpoint)
            output( 'setend')

        # ordered[i].SetEnd(endpoint) if polarity[i] else ordered[i].SetStart(endpoint)
        # ordered[i+1].SetStart(endpoint) if polarity[i+1] else ordered[i+1].SetEnd(endpoint)
#    ordered[-1].SetEnd(firstanchor) if polarity[-1] else ordered[-1].SetStart(firstanchor)
    
def CONNECT(dseglist):
    """given a list of almost-connected DRAWSEGMENTs, move their endpoints such that they are coincident. It is assumed
    that each segment connects to two others, except perhaps the 'end' segments."""

    #output( dseglist)
    points = defaultdict(set)
    #dsegse = defaultdict(set)
    for dseg in dseglist:
        s=dseg.GetStart()
        e=dseg.GetEnd()
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
    for i,p in enumerate(unconnected):
        distances2[p] = \
        [(unconnected[j],wxPointUtil.distance2(unconnected[i],unconnected[j])) for j in range(0,len(unconnected)) if i!=j] # 0 should be i+1

    # for dseg in dseglist:
        # s=dseg.GetStart()
        # e=dseg.GetEnd()
        # (s[0],s[1])
        # (e[0],e[1])
    
      
    for distanceslist in distances2.values():
        distanceslist.sort(key=lambda dist:dist[1])

    # for i in unconnected:
        # output( '\n',i,':')
    for p,d in distances2.iteritems():
        output( '\n',p)
        output( '\t',d)
        
    output( "distances2 = ",distances2.keys())
    pointset = set(points.keys())
    
    for point in unconnected:
    #for point in points.keys():
        output( "point = ",point)
        if point not in pointset:
            continue
        # If the two points are each others closest points, then connect them.
        
        point2 = distances2[point][0][0]
        output( 'p  : ',point,)
        output( 'p2 : ',point2,)
        output( 'dp : ',distances2[point][0][0],)
        output( 'dp2: ',distances2[point2][0][0])
        
        if point == distances2[point2][0][0]:
            newpoint = point
            for pchange in point,point2:
                #seg = points[pchange][0] # should be only one segment in the list for this point.
                (seg,) = points[pchange] # get the one element in the set
                segpoint = seg.GetStart()
                segstart = seg.GetStart()
                segend = seg.GetEnd()
                if segstart[0] == pchange[0] and segstart[1] == pchange[1]:
                    seg.SetStart(pcbnew.wxPoint(newpoint[0],newpoint[1]))
                elif segend[0] == pchange[0] and segend[1] == pchange[1]:
                    seg.SetEnd(pcbnew.wxPoint(newpoint[0],newpoint[1]))
                else:
                    output( "Warning, bug in code.: ",pchange, segstart, segend)
                pointset.remove(pchange)
                
    # for i in range(len(unconnected)):
        # output( '\n',unconnected[i],':')
        # for d in distances2[i]:
            # output( '\t',d)
    
def order_segments(dseglist):
    segs_by_point = defaultdict(set)
    points_by_seg = {}
    for seg in dseglist:
        output( "segment: ",seg.GetStart(), seg.GetEnd())
    #output( "dseglist = ",list(dseglist))
    
    for seg in dseglist:
        s=seg.GetStart()
        st=(s[0],s[1])
        e=seg.GetEnd()
        et=(e[0],e[1])
        points_by_seg[seg] = {st:et,et:st}

        #output( seg)
        for p in seg.GetStart(),seg.GetEnd():
            segs_by_point[(p[0],p[1])].add(seg)

    if not len(points_by_seg):
        return

    for p,segs in segs_by_point.iteritems():
        for seg in segs:
            output( "s_by_p point ",p,"seg ",seg.GetStart(),seg.GetEnd())
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
    
def draw_arc_to_segments(radius,dseglist):
    ordered = order_segments(dseglist)
    for i in range(len(ordered)-1):
        draw_arc_to_lines(radius[0],ordered[i],ordered[i+1])
        
def lines_intersect(p,q,w,v):
    # get intersection
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    r=w-p
    s=v-q
    
    # intersection = (p+tr = q+us)
    # dot vx wy - vy wx
    drs = wxPointUtil.dot_other(r,s)
    output( "drs,r,s=",drs, r, s)
    qmp = q-p
    t = wxPointUtil.dot_other(qmp,s)/ float(drs)
    u = wxPointUtil.dot_other(qmp,r)/ float(drs)
    output( "p,q,r,s,drs,qmp,t,u ",p,q,r,s,drs,qmp,t,u)
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

    xi = (x2112*(x4-x3) - x4334*(x2-x1))/divisor
    yi = (x2112*(y4-y3) - x4334*(y2-y1)) / divisor


    return pcbnew.wxPoint(xi,yi)


def draw_arc_to_lines(radius,pqseg,wvseg):
    p=pqseg.GetStart()
    q=pqseg.GetEnd()
    w=wvseg.GetStart()
    v=wvseg.GetEnd()
    
    # w = p+r; v=q+s
    output( radius,p,q,w,v)
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
    output( "intersection,p,q,w,v = ",intersection, p,q,w,v)
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

    output( 'pq,wv=', pq,wv)
    # draw_segment(wv[1].x,wv[1].y,intersection.x,intersection.y)
    # draw_segment(pq[1].x,pq[1].y,intersection.x,intersection.y)
    # angle between lines, radians
    output( 'vi ',wv[1]-intersection, '; qi ',pq[1]-intersection)
    output( 'dot ',wxPointUtil.dot_other(wv[1]-intersection,pq[1]-intersection))
    # tangentpoints
    # scale(wxPointUtil.unit(wv[1]-intersection)
    output( 'i3=',intersection)
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
    output( 'awv,apq = ',awv*180/math.pi,apq*180/math.pi)
    #theta = (awv + apq) % 2*math.pi

    output( 'theta= ',theta)
    #  CB/PB=tan(theta/2) => dist(intersection,tangent_line) = radius/tan(theta/2.0)
    distance_intersection_to_tangent = abs(radius/math.tan(theta/2.0))
    output( 'dist int to tan',distance_intersection_to_tangent)
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
    output( thickness, pqseg.GetWidth(), wvseg.GetWidth())
    
    
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
    output( 'centerlinepoint, intersection = ',centerlinepoint,intersection)
    centervector = centerlinepoint - intersection
    cangle = -math.atan2(centervector[1],centervector[0])
    #draw_segment(centerlinepoint[0],centerlinepoint[1],intersection[0],intersection[1],layer=pcbnew.Dwgs_User)
    
    output( 'anglebase,cangle,a/2 = ',anglebase*180/math.pi,cangle*180/math.pi,(awv+apq)*90/math.pi,"   awv,apq = ",awv*180/math.pi,apq*180/math.pi )
    arcstart = tangentfirst[1]
    # angle = ((awv-apq)*180/math.pi)

    output( 'i4=',intersection)

    output( 'wvtpoint,pqtpoint ',wvtpoint,pqtpoint)
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

    output( 'i5=',intersection)
    # unit = scale(w,1/dist(w))
    wvtpi = wvtpoint-intersection
    pqtpi = pqtpoint-intersection
    
    lefttpi = arcstart-intersection
    output( 'center calc info: ',wvtpi,)
    # center = pqtpoint+wxPointUtil.scale(pcbnew.wxPoint(pqtpi[1],-pqtpi[0]),radius/
                                        # math.sqrt(pqtpi[0]*pqtpi[0]+pqtpi[1]*pqtpi[1]))

    center = arcstart+wxPointUtil.scale(pcbnew.wxPoint(lefttpi[1],-lefttpi[0]),sign*radius/
                                        math.sqrt(lefttpi[0]*lefttpi[0]+lefttpi[1]*lefttpi[1]))
    # center = arcstart+wxPointUtil.scale(pcbnew.wxPoint(-lefttpi[1],lefttpi[0]),sign*radius/
                                        # math.sqrt(lefttpi[0]*lefttpi[0]+lefttpi[1]*lefttpi[1]))

                                        
    center2 = wvtpoint+wxPointUtil.scale(pcbnew.wxPoint(-wvtpi[1],wvtpi[0]),radius/
                                        math.sqrt(wvtpi[0]*wvtpi[0]+wvtpi[1]*wvtpi[1]))

    #draw_segment(center[0],center[1],intersection[0],intersection[1],layer=pcbnew.Dwgs_User)
    output( 'i6=',intersection)
    ci = center - intersection
    acenter = -math.atan2(ci[1],ci[0])
    output( 'awv,center,apq = ',awv,acenter,apq)
    output( 'pqtpoint, intersection = ',pqtpoint,intersection)
    pqtpi = pqtpoint-intersection
    output( 'pqtpi = ',pqtpi)
    center3 = pqtpoint+wxPointUtil.scale(wxPointUtil.normal(pqtpi),radius/
                                        math.sqrt(pqtpi[0]*pqtpi[0]+pqtpi[1]*pqtpi[1]))

                                        
    center4 = pqtpoint+wxPointUtil.scale(pcbnew.wxPoint(pqtpi[1],-pqtpi[0]),radius/
                                        math.sqrt(pqtpi[0]*pqtpi[0]+pqtpi[1]*pqtpi[1]))

    #draw_segment(center3[0],center3[1],center4[0],center4[1],layer=pcbnew.Dwgs_User)

    # wvtpoint-intersection+normal()
    
    #intersect_to_pqtpoint is adjacent
    output( "angle,s,c=",angle, arcstart,center)
    # draw_segment(arcstart[0],arcstart[1],center[0],center[1])
    # draw_segment(wvtpoint[0],wvtpoint[1],center[0],center[1],layer=pcbnew.Eco1_User)
    # draw_segment(pqtpoint[0],pqtpoint[1],center[0],center[1],layer=pcbnew.Eco1_User)
    # draw_segment(pqtpoint[0],pqtpoint[1],wvtpoint[0],wvtpoint[1],layer=pcbnew.Eco1_User)

    thickness = int((pqseg.GetWidth()+wvseg.GetWidth())/2.0)
    output( thickness, pqseg.GetWidth(), wvseg.GetWidth())
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
    board = pcbnew.GetBoard()
    ds=pcbnew.DRAWSEGMENT(board)
    ds.SetShape(pcbnew.S_ARC)
    ds.SetLayer(layer)
    ds.SetWidth(max(1,int(thickness)))
    
    # # Line Segment:
    # ds.SetStart(pcbnew.wxPoint(x1,y1))
    # ds.SetEnd(pcbnew.wxPoint(x2,y2))
    
    # Arc
    output( angle,pcbnew.wxPoint(x1,y1),pcbnew.wxPoint(x2,y2), "thickness=",thickness)
    ds.SetArcStart(pcbnew.wxPoint(x1,y1))
    ds.SetAngle(angle*10)
    ds.SetCenter(pcbnew.wxPoint(x2,y2))
    
    board.Add(ds)
    return ds
    # Need two algorithms:
    # Given two lines and a corner radius,
    #    what is the SetStart() and SetCenter() values?
    

def draw_segment(x1,y1,x2,y2,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):
    """Draws the line segment indicated by the x,y values
    on the given layer and with the given thickness."""
    board = pcbnew.GetBoard()
    ds=pcbnew.DRAWSEGMENT(board)
    board.Add(ds)
    ds.SetStart(pcbnew.wxPoint(x1,y1))
    ds.SetEnd(pcbnew.wxPoint(x2,y2))
    ds.SetLayer(layer)
    ds.SetWidth(max(1,int(thickness)))
    return ds

def layer(layer):
    try:
        return int(layer)
    except:
        return pcbnew.GetBoard().GetLayerID(layer)
    
def draw_text(text,pos,size,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):
    """Draws the line segment indicated by the x,y values
    on the given layer and with the given thickness."""
    
# 'Hello 100,100 MM 10,10 MM 1 MM F.SilkS DRAWTEXT'
# '0,0,100,100 MM DRAWSEGMENTS'
    
    size = pcbnew.wxSize(size[0],size[1])
    pos = pcbnew.wxPoint(pos[0],pos[1])
    board = pcbnew.GetBoard()
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

def REJOIN():
    # Moves the set of coniguous lines or tracks to match the single line already moved.
    run('drawings copytop selected')
    # lines = _operand_stack[-1]
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
    for line in _operand_stack[-1]:
        output( 'Connected: ',line)
        for p in (line.GetStart(),line.GetEnd()):
            lines_by_vertex[(p.x,p.y)].add(line)
            #lines_by_vertex.setdefault((p.x,p.y),set()).add(line)
            
    for vertex,lines in lines_by_vertex.iteritems():
        output( vertex,': ',lines)
        
    line_by_lonelyvertex = filter(lambda x: len(x[1])==1, lines_by_vertex.iteritems())
    
    # if both vertexes have only one line in lines_by_vertex, then it's the lonely line
    lonely_line = []
    connected_lines = []
    for line in _operand_stack[-1]:
        if len(lines_by_vertex[(line.GetStart().x,line.GetStart().y)]) == 1 \
           and len(lines_by_vertex[(line.GetEnd().x,line.GetEnd().y)]) == 1:
            lonely_line.append(line)
        else:
            connected_lines.append(line)
    _operand_stack.pop()
    output( 'lonely',len(lonely_line),'; connected',len(connected_lines))
    if len(lonely_line) != 1:
        output( 'no loney_line')
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
    
def CONNECTED(wholelist, initlist):
    s = map(lambda x: (x.GetStart().x,x.GetStart().y),wholelist)
    e = map(lambda x: (x.GetEnd().x,x.GetEnd().y),wholelist)
    d = defaultdict(list)
    for i,item in enumerate(wholelist):
        d[s[i]].append(item)
        d[e[i]].append(item)
    # Now we have items by coordinates for fast lookup
    i = 0
    retValue = list(initlist)
    while i < len(retValue):
        key=(retValue[i].GetStart().x,retValue[i].GetStart().y)
        try: d[key].remove(retValue[i]) 
        except: pass
        retValue.extend(d[key])
        key=(retValue[i].GetEnd().x,retValue[i].GetEnd().y)
        try: d[key].remove(retValue[i]) 
        except: pass
        retValue.extend(d[key])
        i += 1
    return list(set(retValue))
    
def DRAWPARAMS(c):
    t,w,h,l = c[0].split(',') \
    if isinstance(c[0],basestring) else c[0] \
    if hasattr(c[0],'__iter__') else [c[0]]
    _user_stacks['DRAWPARAMS'] = [t,w,h,l]

def list_to_paired_list(input):
    a = iter(input)
    input = [pcbnew.wxPoint(int(x),int(y)) for x,y in izip(a, a)]
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
    
def rotate_point(point,center,angle,ccw=True):
    # try:
        # center=center[0]
    # except:
        # pass
    output( 'pca: ',point,center,angle)
    #return None
    if ccw:
        mult = -1
    else:
        mult = 1
    radians = mult*float(angle)*math.pi/180.0
    if not isinstance(point,pcbnew.wxPoint):
        point = pcbnew.wxPoint(point[0],point[1]) 
    if not isinstance(center,pcbnew.wxPoint):
        center = pcbnew.wxPoint(center[0],center[1])
    s = math.sin(radians)
    c = math.cos(radians)
    point = point - center
    output( point)
    point =  pcbnew.wxPoint(point[0]*c - point[1]*s,point[0]*s + point[1]*c)
    point = point + center
    return point
    
def ROTATEPOINTS(points,center,angle):
    output( 'c1: ',center, points)
    center = convert_to_points(center)[0]
    points = convert_to_points(points)
    if not hasattr(angle,'__iter__'):
        angle = [angle]
    # for ps,c in izip(points, cycle(center)):
        # newp = [rotate_point(p,c,float(angle)) for p in ps ]
    newps = []
    output( 'cpsa: ',center,points, angle)
    for ps,c,a in izip(points, cycle(center),cycle(angle)):
        newps.append([rotate_point(p,c,float(a)) for p in ps])

    output( 'c2:',center, points)
    return newps

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

savepath = os.path.join(os.path.expanduser('~'),'kicad','kicommand')

def LOAD(name):
    new_path = os.path.join(savepath, name)
    with open(new_path,'r') as f: run(f.read())

def SAVE(name):
    dictname = 'user'
    if not os.path.exists(savepath):
        os.makedirs(savepath)
        output('created ~/kicad/kicommand')
    output("saving to %s"%name)
    new_path = os.path.join(savepath, name)
    with open(new_path,'w') as f:
        commands = _dictionary[dictname].iteritems()
        for command,definition in sorted(commands,key=lambda x:x[0]):
            f.write( ": %s %s ;\n"%(command,_dictionary[dictname][command]))

def EXPLAIN(commandstring,category=None):
    commands = commandstring.split(',')
    commands.reverse()
    printed = set()
    count = 0
    while commands:
        count += 1
        if count > 100:
            output('explain command has limit of 100 command output.')
            break
        command = commands.pop()
        if not command:
            continue
        if command in printed:
            output(('%s'%(command)))
            continue
        else:
            found = None
            for dictname in ['user','persist']:
                #output( '\n',dictname,'Dictionary')
                if command in _dictionary[dictname]:
                    found = _dictionary[dictname][command].split()
                    output( ': %s %s ;'%(command,' '.join(found)))
                    found.reverse()
                    commands.extend(found)
                    break;
            if not found:
                if not print_command_detail(command):
                    output( '%s - A literal value (argument)'%command)
                # HELP(command,exact=True)
                # printed.add(command)

def print_command_detail(command):
        k,v = command,_command_dictionary.get(command,None)
        if not v:
            return False
        output(('%s (Category: %s)'%(k,v.category)))
        output(('\t%s'%'\n'.join(['\n\t'.join(wrap(block, width=60)) for block in v.helptext.splitlines()])))
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
    output( 'COMMAND explain - For help on a specific COMMAND.')
    output()
    
    commands = 'helpcat explain'.split()
    # commands = filter(lambda c: c[1].category == 'Help', _command_dictionary.iteritems())
    # commands = [command[0] for command in commands]
    # commands.sort()
    for command in commands:
        print_command_detail(command)

def HELPCAT(category):
    if category == 'All':
        commands = _command_dictionary.iteritems()
        cbyc = defaultdict(list)
        for command in commands:
            cbyc[command[1].category].append(command[0])
        catlen = max(map(len,cbyc.keys()))
        #output( format('{'+str(catlen)+'} - {}','CATEGORY'))
        #output( 'CATEGORY   -   COMMANDS IN THIS CATEGORY')
        output( '{:<{width}} - {}'.format('CATEGORY','COMMANDS IN THIS CATEGORY', width=catlen))
        for category in sorted(cbyc.keys()):
            output( '{:<{width}} - {}'.format(category,' '.join(cbyc[category]), width=catlen))
        return

    commands = filter(lambda c: c[1].category == category, _command_dictionary.iteritems())
    commands = [command[0] for command in commands]
    commands.sort()
    for command in commands:
        print_command_detail(command)
            
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



_dictionary = {'user':{}, 'persist':{}, 'command':{}}
# collections.OrderedDict
_command_dictionary = _dictionary ['command']
_operand_stack = []
_command_dictionary = {
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
        'Get the base object for PCBNEW'),
    'board': Command(0,lambda c: pcbnew.GetBoard(),'Elements',
        'Get the Board object'),
    'modules': Command(0,lambda c: pcbnew.GetBoard().GetModules(),'Elements',
        'Get all modules'),
    'pads': Command(0,lambda c: pcbnew.GetBoard().GetPads(),'Elements',
        'Get all pads'),
    'tracks': Command(0,lambda c: pcbnew.GetBoard().GetTracks(),'Elements',
        'Get all tracks (including vias)'),
    'drawings': Command(0,lambda c: pcbnew.GetBoard().GetDrawings(),'Elements',
        'Get all top-level drawing objects (lines and text)'),
#    'toptext': Command(0,lambda c: filter(lambda x: isinstance(x,pcbnew.EDA_TEXT),pcbnew.GetBoard().GetDrawings()),'Elements'),
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

    'index': Command(2,
                       lambda c: c[0][int(c[1])] if isinstance(c[1],basestring) \
                       and c[1].find(',') == -1 else map(lambda x: x[0][int(x[1])],
                       izip(c[0], cycle(c[1].split(','))
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
    'setselect': Command(1,lambda c: filter(lambda x: x.SetSelected(), c[0]),'Action',
        '[objects] Select the objects'),
    'clearselect': Command(1,lambda c: filter(lambda x: x.ClearSelected(), c[0]),'Action',
        '[objects] Deselect the objects'),
    'rejoin': Command(0,lambda c: REJOIN(),'Action',
        'Using selected lines, move multiple connected lines to the isolated line.'),
    'connect': Command(1,lambda c: CONNECT(c[0]),'Action',
        'Using selected lines, connect all vertices to each closest one.'),
    # Filter
    'connected': Command(2,lambda c: CONNECTED(c[0],c[1]),'Filter',
        '[WHOLE INITIAL] From objects in WHOLE, select those that are connected to objects in INITIAL (recursevely)'),
    'matchreference': Command(2,lambda c: filter(lambda x: x.GetReference() in c[1].split(','), c[0]),'Filter',
        '[MODULES REFERENCE] Filter the MODULES and retain only those that match REFERENCE'),
    
    'extend': Command(2,lambda c: c[0].extend(c[1]),'Stack',
        '[LIST1 LIST2] Join LIST1 and LIST2'),
        
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
#x=lambda c: map(lambda x: float(x),c.split(',')) if isinstance(c,basestring) else map(lambda x: float(x),c)
    'stack': Command(0,lambda c: STACK(),'Programming',
        'Output the string representation of the objects on the stack'),
    'print': Command(0,lambda c: PRINT(),'Programming',
        'Output the string representation of the top object on the stack'),
    'builtins': Command(0,lambda c:  __builtins__,'Programming',
        'Output the __builtins__ Python object, giving access to the built in Python functions.'),
    
    # 'getstart': Command(1,lambda c: [m.GetStart() for m in c[0]],'Call',
        # '[LIST] Get the start wxPoint from the LIST of DRAWSEGMENTS.'),
    # 'getend': Command(1,lambda c: [m.GetEnd() for m in c[0]],'Call',
        # '[LIST] Get the end wxPoint from the LIST of DRAWSEGMENTS.'),
    'calllist': Command(2,lambda c: CALLLIST(c[0],c[1]),'Call',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST.'
        'The FUNCTION must return a list of items (this is suitable'
        'for module functions such as GraphicalItems and Pads.'),
    'fcall': Command(1,lambda c: map(lambda x: x(), c[0]),'Call',
        '[FUNCTIONLIST] Execute each python function in the FUNCTIONLIST on each member of LIST. Return the list of results in the same order as the original LIST.'),
    'fcallargs': Command(2,
                lambda c: 
                map(lambda x: 
                        x[0](*(x[1])), 
                        izip(c[0], cycle(c[1]))
                   )
                ,'Call',
        '[FUNCTIONLIST ARGLISTOFLISTS] Execute each python function in the'
        'FUNCTIONLIST on each member of that list with arguments in ARGLISTOFLISTS.' 'ARGLISTOFLISTS can be '
        'a different length than OBJECTLIST, in which case ARGLISTOFLISTS '
        'elements will be repeated (or truncated) to match the length of '
        'OBJECTLIST. Returns the list of results in the same order as the '
        'original OBJECTLIST. The commands LIST and ZIP2 will be helpful '
        'here.'),

    
    'call': Command(2,lambda c: map(lambda x: getattr(x,c[1])(), c[0]),'Call',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Return the list of results in the same order as the original LIST.'),
    'callfilter': Command(2,lambda c: filter(lambda x: getattr(x,c[1])(), c[0]),'Call',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Filter results that return False.'),
    'callnotfilter': Command(2,lambda c: filter(lambda x: not getattr(x,c[1])(), c[0]),'Call',
        '[LIST FUNCTION] Execute python FUNCTION on each member of LIST. Filter results that return True.'),
    'callargs': Command(3,
                lambda c: 
                map(lambda x: 
                        getattr(x[0],c[2])(*(x[1])), 
                        izip(c[0], cycle(c[1]))
                   )
                ,'Call',
                #        zip(c[0],c[1][0:len(c[0])])
                # itertools.izip(c[0], itertools.cycle(c[1]))
                #list(itertools.izip([1,2,3], itertools.cycle([4,5])))
        '[OBJECTLIST ARGLISTOFLISTS FUNCTION] Execute python FUNCTION on each member '
        'of OBJECTLIST with arguments in ARGLISTOFLISTS. ARGLISTOFLISTS can be '
        'a different length than OBJECTLIST, in which case ARGLISTOFLISTS '
        'elements will be repeated (or truncated) to match the length of '
        'OBJECTLIST. Returns the list of results in the same order as the '
        'original OBJECTLIST. The commands LIST and ZIP2 will be helpful '
        'here.'),
    # Move all module's Value text to Dwgs.User layer
    # r('modules Value call Dwgs.User layernums list SetLayer callargs')
    # Move only selected module's Value text to Dwgs.User layer
    # r('modules selected Value call Dwgs.User layernums list SetLayer callargs')
    # Numeric
    
    # Outline all module text objects, including value and reference.
    # r('clear referencetextobj valuetextobj moduletextobj append append copy GetTextBox call corners swap copy GetCenter call swap copy GetParent call Cast call GetOrientationDegrees call swap GetTextAngleDegrees call +l rotatepoints drawsegments')
    # # Outline the pads. Might be a problem with "bounding box" being orthogonal when pad is rotated.
    # r('clear pads copy GetBoundingBox call corners swap copy GetCenter call swap GetOrientationDegrees call rotatepoints drawsegments')
    '+l': Command(2,lambda c:
            [float(a)+float(b) for a,b in izip(c[0], cycle(c[1]))],'Numeric',
        '[LIST1 LIST2] Return the the floating point LIST1 + LIST2 member by member.'),
    '+f': Command(2,lambda c:
            float(c[0])+float(c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 + OPERAND2.'),
    '-f': Command(2,lambda c: float(c[0])-float(c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 - OPERAND2.'),
    '*f': Command(2,lambda c: float(c[0])*float(c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 * OPERAND2.'),
    '/f': Command(2,lambda c: float(c[0])/float(c[1]),'Numeric',
        '[OPERAND1 OPERAND2] Return the the floating point OPERAND1 / OPERAND2.'),
    'sum': Command(1,lambda c: sum(c[0]),'Numeric',
        '[LIST] Return the sum of all members in LIST.'),

    # Stack Manipulation
    'append': Command(2,lambda c: c[0]+c[1],'Stack',
        '[OPERAND1 OPERAND2] Return LIST1 and LIST2 concatenated together.'),
    #'copytop': Command(0,lambda c: list(_operand_stack[-1])),
    # 'copytop': Command(0,lambda c: _operand_stack[-1],'Stack',
        # 'Duplicate the top object on the stack.'),
    'clear': Command(0,lambda c: CLEAR(),'Stack',
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
                       lambda c: float(c[0]) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: float(x),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list. OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.', ),
    'int': Command(1,
    # if basestring and has ','
                       lambda c: int(c[0]) if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: int(x),
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list. OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.', ),
    'string': Command(1,lambda c: str(c[0]),'Conversion',
        '[OBJECT] Convert OBJECT to a string.'),
    'dict': Command(2,lambda c: dict(zip(c[0], c[1])),'Conversion',
        '[KEYS VALUES] Create a dictionary from KEYS and VALUES lists.'),
    #'mm': Command(1,lambda c: float(c[0])*pcbnew.IU_PER_MM,'Conversion'),
    'mm': Command(1,
                       lambda c: float(c[0])*pcbnew.IU_PER_MM if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: float(x)*pcbnew.IU_PER_MM,
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list converted '
        'from mm to native units (nm). OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.'),
    'mil': Command(1,
                       lambda c: float(c[0])*pcbnew.IU_PER_MILS if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: float(x)*pcbnew.IU_PER_MILS,
                       c[0].split(',')
                       if isinstance(c[0],basestring) else c[0]
                       if hasattr(c[0],'__iter__') else [c[0]]),
                       'Conversion',
        '[OBJECT] Return OBJECT as a floating point value or list converted '
        'from mils to native units (nm). OBJECT can '
        'be a string, a comma separated list of values, a list of strings, or '
        'list of numbers.'),
    'mils': Command(1,
                       lambda c: float(c[0])*pcbnew.IU_PER_MILS if isinstance(c[0],basestring) \
                       and c[0].find(',') == -1 else map(lambda x: float(x)*pcbnew.IU_PER_MILS,
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
    'list': Command(1,lambda c: [c[0]],'Conversion',
        '[OBJECT] Make OBJECT into a list (with only OBJECT in it).'),
    'delist': Command(1,lambda c: c[0][0],'Conversion',
        '[LIST] Output index 0 of LIST.'),
    

    #'swap': Command(2,retNone(lambda c: _operand_stack[-1],_operand_stack[-2]=_operand_stack[-2],_operand_stack[-1])),
    # 'pick': Command(1,lambda c: _operand_stack.insert(-int(_operand_stack[-1])-1,_operand_stack[-2]),'Stack',
    #works: 'pick': Command(1,lambda c: _operand_stack.insert(-1,_operand_stack[len(_operand_stack)-int(c[0])-2]),'Stack',
    'pick': Command(1,lambda c: _operand_stack.insert(-1,_operand_stack[-int(c[0])-2]),'Stack',
        '[NUMBER] Copy the value that is NUMBER of objects deep in the stack to the top of the stack. '
        '\n\tExamples:\n\t0 pick - copies the top of the stack.\n'
        '\t1 pick - pushes a copy of the second item from the top of the stack onto the top of the stack.\n'
        ),
    'swap': Command(0,lambda c: SWAP(),'Stack',
        'Switches the two top objects on the stack.'),
    'zip2': Command(2,lambda c: zip(c[0],c[1]),'Stack',
        '[LIST1 LIST2] Creates a list with parallel objects in LIST1 and '
        'LIST2 together at the same index.'),
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
    
    'rotatepoints': Command(3,lambda c: ROTATEPOINTS(c[0],c[1],c[2]),'Geometry',
        '[POINTS CENTER DEGREES] Rotate POINTS around CENTER. POINTS can be in '
        'multiple formats such as EDA_RECT or a list of one or more points.'),
        
    'corners': Command(1,lambda c: CORNERS(c[0]),'Geometry',
        "[OBJECT] OBJECT is either a single object or a list of objects. "
        "Converts each OBJECT, either EDA_RECT or OBJECT's BoundingBox "
        "into vertices appropriate for drawsegments."
        ),
    
    'layernums': Command(1,lambda c: [pcbnew.GetBoard().GetLayerID(x) for x in c[0].split(',')],'Layer',
        '[STRING] Get the layer numbers for each layer in comma separated STRING. '
        'STRING can also be one number, if desired.'),
    'onlayers':  Command(2,lambda c: filter(lambda x: set(x.GetLayerSet().Seq()).intersection(set(c[1])),c[0]),'Layer',
        '[LIST LAYERS] Retains the objects in LIST that exist on any of the LAYERS.'),
    'setlayer': Command(2,lambda c: map(lambda x: x.SetLayer(layer(c[1])),
                          c[0] if hasattr(c[0],'__iter__') else list(c[0])), 'Layer',
        '[OBJECTS LAYER] Moves all OBJECTS to LAYER.'),
    'pop': Command(1,lambda c: None,'Stack',
        'Removes the top item on the stack.'),
    'see': Command(1,lambda c: print_userdict(c[0]),'Help',
        '[COMMAND] Shows previously-defined COMMAND from the user dictionary. '
        'See the colon (:) command for more information.'),
    'seeall': Command(0,lambda c: print_userdict(None),'Help',
        '[COMMAND] Shows all previously-defined COMMANDs from the user dictionary. '
        'See the colon (:) command for more information.'),
    'time': Command(0,lambda c: time.asctime(),'System',
        'Returns the current system time as a string.'),
    # 'createtext': Command(2,lambda c: )
    #def draw_arc(x1,y1,x2,y2,radius,layer=pcbnew.Dwgs_User,thickness=0.15*pcbnew.IU_PER_MM):

    'regular': Command(1,lambda c:REGULAR(c[0]),'Draw',""),
    'round': Command(2,lambda c: draw_arc_to_segments(c[0],c[1]),'Draw',""),
    'drawarc':Command(1,lambda c: draw_arc(50*pcbnew.IU_PER_MM,50*pcbnew.IU_PER_MM,radius,angle,layer=_user_stacks['drawparams'][3],thickness=_user_stacks['drawparams'][0]),'Draw',
        ""),
    'drawsegments':Command(1,lambda c: draw_segmentlist(c[0],layer=_user_stacks['drawparams'][3],thickness=_user_stacks['drawparams'][0]),'Draw',
        "[POINTSLIST] Points list is interpreted as pairs of X/Y values. Line segments are"
        "drawn between all successive pairs of points, creating a connected sequence of lines."
        "This command uses previously set drawparams and the points are in native units (nm) so using mm or mils commands is suggested."),
    'drawtext': Command(2,lambda c: draw_text(c[0],c[1],_user_stacks['drawparams'][1:3],layer=_user_stacks['drawparams'][3],thickness=_user_stacks['drawparams'][0]),'Draw',
        '[TEXT POSITION] Draws the TEXT at POSITION using previously set drawparams. Position is in native units (nm) so using mm or mils commands is suggested.'),
    'drawparams': Command(4,lambda c: DRAWPARAMS(c),'Draw',
        '[THICKNESS WIDTH HEIGHT LAYER] Set drawing parameters for future draw commands.\n'
        'Example: 1,5,5 MM F.Fab LAYERNUMS append drawparams'),
    'help': Command(0,lambda c: HELPMAIN(),'Help',
        "Shows general help"),
    'explain': Command(1,lambda c: EXPLAIN(c[0]),'Help',
        "[COMMAND] Shows help for COMMAND. COMMAND can be a comma separated list of commands (use a comma after a single command to prevent KiCommand from interpreting the command). The keyword 'All' shows help for all commands. You can precede the COMMAND by single quote mark so that it does not execute, or use the comma trick."),
    # 'helpcom': Command(0,lambda c: HELP(None),'Help',
        # "[COMMAND] Shows help for COMMAND. The keyword 'All' shows help for all commands. Precede the COMMAND by single quote mark (') so that it doesn't execute."),
    'helpcat': Command(1,lambda c: HELPCAT(c[0]),'Help',
        "[CATEGORY] Shows commands in CATEGORY. CATEGORY value of 'All' shows all categories."),
    'pad2draw': Command(1,lambda c: pad_to_drawsegment(c[0]),'Draw',
        '[PADLIST] draws outlines around pad on DRAWPARAMS layer.'),
    'load': Command(1,lambda c: LOAD(c[0]),'Programming',
        '[FILENAME] executes commands from FILENAME. relative to '
        '~/kicad/kicommand. Note that this command is not '
        'totally symmetric with the save command.'),
    'save': Command(1,lambda c: SAVE(c[0]),'Programming',
        '[FILENAME] saves the user dictionary into FILENAME relative to '
        '~/kicad/kicommand. Note that this command is not '
        'totally symmetric with the load command.'),

        
    # 'vias': filter(lambda x:isinstance(x,pcbnew.VIA),_command_dictionary['tracks']),
    # 'vias_class': filter(lambda x:pcbnew.VIA_Classof(x),_command_dictionary['tracks']),
}

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
_user_stacks = {'drawparams':[0.3*pcbnew.IU_PER_MM,1*pcbnew.IU_PER_MM,1*pcbnew.IU_PER_MM,pcbnew.Dwgs_User]}
# drawparams: thickness,width,height,layer

def print_userdict(command):
    for dictname in ['user','persist']:
        output( '\n',dictname,'Dictionary')
        if command:
            commands = filter (lambda x:x[0].startswith(command),_dictionary[dictname].iteritems())
        else:
            commands = _dictionary[dictname].iteritems()
            #output ('%d items in %s'%(99,dictname))
        for command,definition in sorted(commands,key=lambda x:x[0]):
            output( ":",command,_dictionary[dictname][command],';')
# r('CLEAR MODULETEXTOBJ VALUETEXTOBJ APPEND REFERENCETEXTOBJ APPEND COPY GetTextBox CALL CORNERS SWAP COPY GetCenter CALL SWAP GetTextAngleDegrees CALL ROTATEPOINTS DRAWSEGMENTS')
# _persistdefault = """
# :  ; 
# """
# for line in _persistdefault.splitlines():
    # run(line)
_dictionary['persist']['wxpoint'] = 'pcbnew list swap list wxPoint callargs'
_dictionary['persist']['toptextobj'] = 'drawings EDA_TEXT filtertype'
_dictionary['persist']['valuetextobj']= 'modules Value call'
_dictionary['persist']['referencetextobj']= 'modules Reference call'
_dictionary['persist']['moduletextobj']= 'modules GraphicalItems calllist EDA_TEXT filtertype'
_dictionary['persist']['textfromobj']= 'GetShownText call' 

#_dictionary['persist']['valuetext'] = 'modules GetValue call'
#_dictionary['persist']['referencetext'] = 'modules GetReference call'

_dictionary['persist']['not'] = "' ="
_dictionary['persist']['copy'] = "0 pick"
_dictionary['persist']['setselect'] = 'SetSelected call'
_dictionary['persist']['clearselect'] = 'ClearSelected call'
_dictionary['persist']['clearallselected'] = """
        modules copy GetReference call clearselect
        copy GetValue call clearselect
        copy GraphicalItems calllist clearselect
        clearselect
        pads clearselect
        tracks clearselect
        drawings clearselect 
        """
_dictionary['persist']['outlinepads'] = """
        pads copy corners swap copy GetCenter call swap 
        GetOrientationDegrees call rotatepoints drawsegments
        """
_dictionary['persist']['outlinetext'] = """
        valuetextobj
        referencetextobj append 
        moduletextobj append 
        copy GetTextBox call corners swap copy GetCenter call swap 
        copy GetTextAngleDegrees call swap GetParent call Cast call GetOrientationDegrees call
        +l rotatepoints drawsegments
        """ 
        
_dictionary['persist']['outlinetoptext'] = """
        toptextobj
        copy GetTextBox call corners swap copy GetCenter call swap
        GetTextAngleDegrees call rotatepoints drawsegments ;
        """
        #         toptextobj append 

#    'not': Command(0,lambda c: run('0 FLOAT ='),'Comparison'),

#output( 'ops',str(_operand_stack))
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
    output( 'Warning! Expected Pad Shapes are different that command stack expects.')


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
    board = pcbnew.GetBoard()
    ds=pcbnew.DRAWSEGMENT(board)
    board.Add(ds)
    ds.SetLayer(_user_stacks['drawparams'][3])
    ds.SetWidth(max(1,int(_user_stacks['drawparams'][3])))

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

    # toptext = filter(lambda x: isinstance(x,pcbnew.EDA_TEXT) and x.IsSelected(),pcbnew.GetBoard().GetDrawings())
    # moduleitems=[]
    # for m in pcbnew.GetBoard().GetModules():
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
    
aplugin.register(aplugin())