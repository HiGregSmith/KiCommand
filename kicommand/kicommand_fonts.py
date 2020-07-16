# -*- coding: utf-8 -*-
from __future__ import print_function

try:
    import fontTools
    import fontTools.ttLib
except:
    pass
    
import copy 
import pickle
import os
import inspect
import itertools
import svgutil
from wxpointutil import wxPointUtil

try:
    try: 
        _file = __file__
    except NameError:
        _file = inspect.getfile(inspect.currentframe())        
except:
    pass
if not os.path.exists(_file):
    _basedir = os.getcwd()
else:
    _basedir = os.path.dirname(os.path.abspath(_file))
    
_fontdata_directory = os.path.join(_basedir,'fontdata')

def _save_obj(obj, filefullname):
    with open(filefullname, 'wb') as f:
        pickle.dump(obj, f, 2)#pickle.HIGHEST_PROTOCOL)

def _load_obj(filefullname):
    with open(filefullname, 'rb') as f:
        return pickle.load(f)

# import imp

# ttf_filename = os.path.join('..','osifont-lgpl3fe.ttf')
# kifonts = imp.load_source('kicommand_fonts', 'C:\Program Files\KiCad\kicad-5.1-jenkins-619\share\kicad\scripting\plugins\kicommand\kicommand_fonts.py')
## kifonts = imp.reload(kifonts)
# kifonts._fontdata_directory = os.path.join(os.getcwd(),'fontdata')
# ttf_file = os.path.abspath(os.path.join(kifonts._fontdata_directory,ttf_filename))
# ft = kifonts.fonttable()
# ft.load_ttf(ttf_file)
# ft.save_fontdata('osi')
class fontmanager(object):
    def __init__(self):
        self._fonts = {}
        self._fontIndex = {}
    def _getfontindex(self):
        indexfilefull = os.path.join(_fontdata_directory,'fontindex.txt')
        if not os.path.exists(indexfilefull):
            return # self.updatefontindex()
        with open(indexfilefull, 'rb') as f:
            for line in f:
                words = line.split(',')
            self._fontIndex[words[0]] = words[1:]
        return self._fontIndex
            # expected filename,family,sub family
    def _getfonttable(self,filename):
        return _load_obj(os.path.join(_fontdata_directory,filename))
    def _loadfont(self,fontname):
        fontpath = os.path.join(_fontdata_directory,fontname)
        self._fonts[fontname] = _load_obj(fontpath)
        self._fonts[fontname]._fontname = fontname
        self._fonts[fontname]._fontfile = fontpath
    # def __getitem__(self,fontname):
        # font = self._fonts.get(fontname,None)
        # if font is None:
            # _loadfont(fontname)
        # return self._fonts.get(fontname,None)
    def updatefontindex(self):
        #output('updating index')
        indexfilefull = os.path.join(_fontdata_directory,'fontindex.txt')
        retindex = self._getfontindex()
        if retindex is not None:
            return
        for fontname in self.getfontlist():
            if fontname not in self._fontIndex:
                with open(indexfilefull, 'ab') as f:
                    self._loadfont(fontname)
                    family = self._fonts[fontname].getNameValue(1)
                    subfamily = self._fonts[fontname].getNameValue(2)
                    f.write('{},{},{}'.format(fontname,family,subfamily))
                    self._fontIndex[fontname] = [family,subfamily]
                    self.removeFromTable(fontname)
    def getfontlist(self):
        return [f for f in os.listdir(_fontdata_directory) if os.path.isfile(os.path.join(_fontdata_directory, f))]
    def getfontfamilies(self): # this should get and create the font index.
        #output('getting families')
        i=self._getfontindex()
        if not self._fontIndex:
            self.updatefontindex()
        fontbyfamandsub = {}
        for fontname,famandsub in self._fontIndex.items():
            fam = famandsub[0]
            sub = famandsub[1]
            famdict = fontbyfamandsub.get(fam,None)
            if famdict is None:
                fontbyfamandsub[fam] = {}
            subdict = fontbyfamandsub.get(famandsub[0]).get(famandsub[1],None)
            if subdict is None:
                fontbyfamandsub.get(famandsub[0])[famandsub[1]] = []
            fontbyfamandsub.get(famandsub[0])[famandsub[1]].append(fontname)
        return fontbyfamandsub
        
    def getfont(self,fontname):
        font = self._fonts.get(fontname,None)
        if font is None:
            self._loadfont(fontname)
        return self._fonts.get(fontname,None)
    def removeFromTable(self,fontname):
        #self._fonts.pop(fontname,None)
        self._fonts.pop(fontname,None)

class fonttable(object):
    # Name Id	Meaning
    _nameIdDescription = [
          ("Copyright","Copyright notice" )
        , ("Family","Font Family name." )
        , ("Subfamily",'Font Subfamily name. Font style (italic, oblique) and weight (light, bold, black, etc.). A font with no particular differences in weight or style (e.g. medium weight, not italic) should have the string "Regular" stored in this position.')
        , ("UID","Unique font identifier. Usually similar to 4 but with enough additional information to be globally unique. Often includes information from Id 8 and Id 0.")
        , ("Full Name",'Full font name. This should be a combination of strings 1 and 2. Exception: if the font is "Regular" as indicated in string 2, then use only the family name contained in string 1. This is the font name that Windows will expose to users.')
        , ("Version","Version string. Must begin with the syntax ‘Version n.nn ‘ (upper case, lower case, or mixed, with a space following the number).")
        , ("PS Name","Postscript name for the font.")
        , ("Trademark","Trademark. Used to save any trademark notice/information for this font. Such information should be based on legal advice. This is distinctly separate from the copyright.")
        , ("Manufacturer","Manufacturer Name.")
        , ("Designer","Designer. Name of the designer of the typeface.")
        , ("Description","Description. Description of the typeface. Can contain revision information, usage recommendations, history, features, etc.")
        , ("Vendor URL","URL Vendor. URL of font vendor (with protocol, e.g., http://, ftp://). If a unique serial number is embedded in the URL, it can be used to register the font.")
        , ("Designer URL","URL Designer. URL of typeface designer (with protocol, e.g., http://, ftp://).")
        , ("License","License description. Description of how the font may be legally used, or different example scenarios for licensed use. This field should be written in plain language, not legalese.")
        , ("License URL","License information URL. Where additional licensing information can be found.")
        , ("Reserved","Reserved; Set to zero.")
        , ("Preferred Family","Preferred Family (Windows only). In Windows, the Family name is displayed in the font menu. The Subfamily name is presented as the Style name. For historical reasons, font families have contained a maximum of four styles, but font designers may group more than four fonts to a single family. The Preferred Family and Preferred Subfamily IDs allow font designers to include the preferred family/subfamily groupings. These IDs are only present if they are different from IDs 1 and 2.")
        , ("Preferred Subfamily","Preferred Subfamily (Windows only). See above.")
        , ("Compatible Full","Compatible Full (Mac OS only). On the Mac OS, the menu name is constructed using the FOND resource. This usually matches the Full Name. If you want the name of the font to appear differently than the Full Name, you can insert the Compatible Full Name here.")
        , ("Sample Text","Sample text. This can be the font name, or any other text that the designer thinks is the best sample text to show what the font looks like.")
        , ("PS CID","PostScript CID findfont name.")
        , ("Reserved Future","Reserved for future expansion.") # (21-255)
        , ("Font-specific","Font-specific names.")           # (256-32767)
    ]

    def __init__(self):
        self._current_position = [0.0,0,0]
        self._fontdata = None
        self._unicode_codepoint_lookup = {}
        self._glyph_index = []
        self._overall = {}
        self._nameData = {}
        self._kernTable = None
#    def __init__(self,filename):
    def save_fontdata(self,filename):
        _save_obj(self,os.path.join(_fontdata_directory,filename))

    def __getitem__(self,name):
        return self._fontdata[name]
    def svg(self,glyph,template=None,properties={}):
        # return full svg of given glyph. glyph variable input allows any method to retrieve it
        if template is None:
            template = """<svg xmlns="http://www.w3.org/2000/svg"  viewBox="{xmin} {ymin} {width} {height}" transform="scale(1,-1)" version="1.1">
  <path d="{d}" fill="#path"></path>
</svg>"""
# stroke="#path" stroke-width="1" 
# width="200" height="200"
        return template.format(d=glyph['svg'],xmin=glyph['min'][0],xmax=glyph['max'][0],ymin=glyph['min'][1],ymax=glyph['max'][1],width=glyph['max'][0]-glyph['min'][0],height=glyph['max'][1]-glyph['min'][1],)
        
    def u(self,unicode_codepoint):
        return self._fontdata[self._unicode_codepoint_lookup[unicode_codepoint][0]]
    def char(self,character):
        return self.u(ord(character))

    def load_ttf(self,name,ttf,userelative=True):
        _fontname = name
        _fontfile = None
        self._fontdata = {}
        self._unicode_codepoint_lookup = {} # defaultdict(list)
        
        fontdict = self._fontdata
        #ttf = fontTools.ttLib.TTFont(filename)
        #r'C:\Users\gmsmith\Documents\Personal\kicad\KiCommand\fonts\NotoSansMono-Regular.ttf'
        print('   font --> {}'.format(name),end=' ')
        nan = float('NaN')
        for t in ttf['cmap'].tables:
            for code,value in t.cmap.items(): # cmap is a dictionary
                elementarray = self._unicode_codepoint_lookup.get(code,None)
                if elementarray:
                    if value not in elementarray:
                        self._unicode_codepoint_lookup[copy.deepcopy(code)].append(copy.deepcopy(value))
                else:
                    self._unicode_codepoint_lookup[copy.deepcopy(code)] = [copy.deepcopy(value)]

        # for codeandvalueslist in itertools.chain.from_iterable([y + (fontTools.unicode[y[0]],) for y in x.cmap.items()] for x in ttf["cmap"].tables):
            # self._unicode_codepoint_lookup[codeandvalueslist[0]]=codeandvalueslist[1:]
        
        cfftable = ttf.get('CFF ',None)
        if cfftable:
            cfftable.desubroutinize()
            cfftable.remove_hints()
        glyphNames = ttf.getGlyphNames()
        print ('({} glyphs)'.format(len(glyphNames)))
        for gn in glyphNames:# [0:2]: # ['colon']:
            currentsvg = []
                # # the last oncurve point, whether actual or implied, is in curve[2] which has been moved to curvep[0]
                # # last oncurve point is in curve[0]
                # # last offcurve point is in curve[1] (i.e. if not laston)
                # # Now we check to see the first point vs the last point.
                # # bool(firstoffcurveinsegment) == first point is on curve
                # # if lastpoint is off curve and first point is off curve, connect with bezier lastonpoint, calcimplied, firstoncurveinsegment
                # # if lastpoint is on curve and first point is off curve, connect with bezier lastpoint,firstoffcurveinsegment,firstoncurveinsegment
                # # if lastpoint is on curve and first point is on curve, connect with line
                # # if lastpoint is off curve and first point is on curve, connect with bezier lastonpoint, lastoffpoint, firstoncurveinsegment


            glyftable = ttf.get('glyf',None)
            if glyftable:
                coordTables = glyftable[gn].getCoordinates(glyftable) 
                currentsvg = self.svgfromttf(coordTables,userelative=userelative)
            else:
                charstring = cfftable.cff[0].CharStrings[gn]
                currentsvg = self.svgfromcff(charstring)
                
                
            # current svg holds the final svg for the glyph. 
            # We want to use simplified points and determine if 
            # any segments in the glyph contours cross. If they do, 
            # then generating polygons from the contours is more complicated. We can use:
            # wxPointUtil.check_polygons_intersecting(poly_a, poly_b,closed=True):
            
            # right now, we'll just say there's no overlap :-)
            # if there is overlap, this array will contain tuples of polygon indexes that overlap
            # hopefully indexes will be consistent across each of the point generation functions.
            #fontdict[gn]['overlap'] = []
            overlaplist = []
            # get simplified polygons (for now)
            # simplified polygons can be obtained from
            # "fromsvgcontours(svg,simplified=1)", but that's in kicommand.py class "commands")
            #print('svg: {}'.format(' '.join(currentsvg)))
            polygonlist = svgutil.fromsvgcontours(' '.join(currentsvg),simplified=1)
            
            for i in range(len(polygonlist)):
                for j in range(i+1,len(polygonlist)):
                    ilines = wxPointUtil.doPolygonsIntersect(polygonlist[i], polygonlist[j])
                    if ilines:
                        #print('Lines intersect: {}'.format(','.join(map(str,itertools.chain.from_iterable(itertools.chain.from_iterable(ilines))))))
                        overlaplist.append((i,j))
            
            #print(gn)
            fontdict[gn] = {
            'overlap':overlaplist
            ,'svg':' '.join(currentsvg)
            ,'av':(ttf['hmtx'][gn][0],0)  # Advance Vector (advance width,advance_height)
            #,'lv':[] # line vector for using in line height calculations, for left-to-right fonts with lines down the page, this should be [0,-linewidth]
            ,'kv':{} # kerning vector table, not sure how av.h should be affected, complicates "forward-only" processing)
            ,'lsb':ttf['hmtx'][gn][1]
            # ,'ah':ttf['hmtx'][gn][0]*1.5
            }
            # ,('xMin','xMax','yMin','yMax')))
            lvY = max(ttf['hhea'].lineGap, ttf['hhea'].ascent- ttf['hhea'].descent) # , max(ttf['hhea'].yMaxExtent)
            self._overall['line']=[0,lvY] # positive number is down
            for a in ('unitsPerEm',):#,'sTypoAscender','sTypoDescender'):
                self._overall[a] = getattr(ttf['head'],a)
            # https://stackoverflow.com/a/38271649
            # unitsPerEm value from the head table. Usually, for OTF its 1000 UPM, for TTF - 1024 or 2048 UPM. 
            # Absolute values of sTypoAscender and sTypoDescender should add up to unitsPerEm value. And then its just a matter of ratio.       

            # https://docs.microsoft.com/en-us/typography/opentype/spec/hmtx
            # aw,lsb = ttf['hmtx']['uni1EDB']
            # lsb = xmin
            # aw = 
            # rsb = aw - (lsb + xMax - xMin)

            if glyftable:
                fontdict[gn]['min'] = tuple(map(
                lambda n: int(hasattr(ttf['glyf'][gn],n)) and ttf['glyf'][gn].__getattribute__(n)
                ,('xMin','yMin')))
                fontdict[gn]['max'] = tuple(map(
                lambda n: int(hasattr(ttf['glyf'][gn],n)) and ttf['glyf'][gn].__getattribute__(n)
                ,('xMax','yMax')))
                fontdict[gn]['rsb'] = fontdict[gn]['av'][0] - (fontdict[gn]['lsb'] + fontdict[gn]['max'][0] - fontdict[gn]['min'][0])
                # if fontdict[gn]['lsb'] != fontdict[gn]['min'][0]:
                    # print('Warning on {}, font lsb ({}) != xmin ({})'.format(gn,fontdict[gn]['lsb'],fontdict[gn]['min'][0]))


            for name in ttf['name'].names:
                self._nameData[name.nameID] = name.toUnicode()
                # ttf['name'].names[index].toUnicode()

            kt = ttf.get('kern',None)
            if kt:
                self._kernTable = ttf['kern'].kernTables[0].kernTable.copy()
            
    def getNameIndexes(self):
        return sorted(self._nameData.keys())
    def getNameFullDescription(self,index):
        if index <= 20:
            return _nameIdDescription[index][1]
        if 21 <= index <= 255:
            return "{desc} #{index}".format(desc=_nameIdDescription[21][1],index=index)
        if 256 <= index <= 32767:
            return "{desc} #{index}".format(desc=_nameIdDescription[22][1],index=index)
    def getNameShortDescription(self,index):
        if index <= 20:
            return self._nameIdDescription[index][0]
        if 21 <= index <= 255:
            return "{desc} #{index}".format(desc=_nameIdDescription[21][0],index=index)
        if 256 <= index <= 32767:
            return "{desc} #{index}".format(desc=_nameIdDescription[22][0],index=index)

    def getNameValue(self,index):
        return self._nameData.get(index,None)

    # returns a sequence of point generators, one for each contour
    def glyph_contours_generator(self,coordTables):
        #print(coordTables)
        # coords = glyph.getCoordinates(glyphtable) # glyph,glyphtable # ttf['glyf'][gn]
        istart = 0
        for iend_inclusive in coordTables[1]: # coordTables[1] is a list of point counts, the index range for points is istart, iend_inclusive
            iend_exclusive = iend_inclusive+1 # iend_exclusive is need for "range" functions, which don't include the "end" index
            yield self.glyph_contour_generator(coordTables,istart,iend_inclusive)
            istart = iend_exclusive # extra calculation at the end, but no biggie

    def calculate_implied(self,point1,point2):
        """given two off-curve points, calculate the implied on-curve point"""
        return (point1[0]+point2[0])/2.0,(point1[1]+point2[1])/2.0
        
    # returns a point generator one contour. begin and end points are guaranteed to be on curve.
    def glyph_contour_generator(self,coordTables,istart,iend_inclusive):
        # this is very specific to the ttf format table layout and fontTools access to ttf
        # coordTables is a list of lists in order
        # [ points list, segment end index list, on curve flag list ]
        # get the point array
        coords = coordTables # ttf['glyf'][gn].getCoordinates(ttf['glyf'])
        # here we decode 
        # 1) whether the first or last point are off curve
        # 2) if neither are off curve, yield the range as is
        # 3) if only one is off curve, include it the on curve point before (if start is off curve) or after (if end is off curve) the stated range
        # 4) if both are off curve, calculate midway as the oncurve point and include it both before and after the stated range
        firstoncurvepoint = None
        lastoncurvepoint = None
        #print('len coords = {}, istart = {}'.format(len(coords[2]),istart))
        #print('first/last oncurve {}/{}'.format(coords[2][istart],coords[2][iend_inclusive]))
        if coords[2][istart]: # first point is on curve
            if coords[2][iend_inclusive]: # first and last point are on curve
                lastoncurvepoint = coords[0][istart]
                # # do nothing. No extra points, use range as is
            else: # first point is on, last point is off
                lastoncurvepoint = coords[0][istart]
        else: # first point is off
            if coords[2][iend_inclusive]: # last point is on curve
                firstoncurvepoint = coords[0][iend_inclusive]
            else: # first point is off, last point is off
                # calculate on curve point (that will be used for both first and last points
                firstoncurvepoint = self.calculate_implied(coords[0][istart],coords[0][iend_inclusive])
                # ((coords[0][istart][0]+coords[0][iend_inclusive][0])/2.0,(coords[0][istart][1]+coords[0][iend_inclusive][1])/2.0)
                lastoncurvepoint = firstoncurvepoint

        if firstoncurvepoint:
            yield (firstoncurvepoint,1)
        
        for ipoint in range(istart,iend_inclusive+1):
            yield (coords[0][ipoint],coords[2][ipoint])
            
        if lastoncurvepoint:
            yield (lastoncurvepoint,1)

    def delta(self,point,base_point):
        return (point[0]-base_point[0],point[1]-base_point[1])

    def svgfromcff(self,charstring,userelative=True):
        # use charstring: t['CFF '].cff[0].CharStrings[charname]
        # MoveTo: M, m
        # LineTo: L, l, H, h, V, v
        # Cubic Bézier Curve: C, c, S, s
        # Quadratic Bézier Curve: Q, q, T, t
        # Elliptical Arc Curve: A, a
        # ClosePath: Z, z
        currentsvg = []
        base_point = [0.0,0.0]
        pstack = [] # holding program parameters prior to command that uses them
        # currentsvg.append()
        # print('program: {}'.format(' '.join(map(str,charstring.program))))
        for programstep in charstring.program:
            
            if not isinstance(programstep,str):
                pstack.append(programstep)
                continue
            # print('{} {}'.format(programstep,' '.join(map(str,pstack))))
            #tokens[programstep].add(len(pstack))
            if programstep.endswith('to'):
                if programstep.endswith('moveto'):
                    if programstep == 'hmoveto': # |- dx1 hmoveto (22) |-
                        topoint = [ pstack[-1] , 0 ]
                    elif programstep == 'vmoveto': # |- dy1 vmoveto (4) |-
                        topoint = [ 0 , pstack[-1] ]
                    elif programstep == 'rmoveto': # |- dx1 dy1 rmoveto (21) |-
                        topoint = [ pstack[-2], pstack[-1] ]
                    else:
                        raise TypeError('Unrecognized program token {}'.format(programstep))
                    currentsvg.append('m {} {}'.format(*topoint))
                    base_point[0] += topoint[0]
                    base_point[1] += topoint[1]
                    # if userelative:
                        # currentsvg.append('m {} {}'.format(*self.delta(point,base_point)))
                    # else:
                        # currentsvg.append('M {} {}'.format(*point))

                elif programstep.endswith('lineto'): # vlineto and hlineto for CFF alternate h/v while SVG h and v path commands don't
                    if programstep == 'rlineto': # |- {dxa dya}+ rlineto (5) |-
                        # here we have params in sets of two each interpreted as rlineto, just like SVG 'l'
                        #print('pstack: {}'.format(pstack))
                        for argset in zip(*(iter(pstack),) * 2):
                            currentsvg.append('l {} {}'.format(*argset))
                            base_point[0] += argset[0]
                            base_point[1] += argset[1]

                            # do we reset base_point here?
                    elif programstep == 'hlineto': # |- dx1 {dya dxb}* hlineto (6) |-
                                                # or |- {dxa dyb}+ hlineto (6) |-
                        argsiter = iter(pstack)
                        if len(pstack) % 2: # if odd number of arguments, read the first one
                            dx = argsiter.__next__()
                            currentsvg.append('h {}'.format(dx))
                            base_point[0] += dx

                            for argset in zip(*(argsiter,) * 2):
                                currentsvg.append('v {} h {}'.format(*argset))
                                base_point[0] += argset[1]
                                base_point[1] += argset[0]
                        else:
                            for argset in zip(*(argsiter,) * 2):
                                currentsvg.append('h {} v {}'.format(*argset))
                                base_point[0] += argset[0]
                                base_point[1] += argset[1]

                    elif programstep == 'vlineto': # |- dy1 {dxa dyb}* vlineto (7) |-
                                                   # |- {dya dxb}+ vlineto (7) |-
                        argsiter = iter(pstack)
                        if len(pstack) % 2: # if odd number of arguments, read the first one
                            dy = argsiter.__next__()
                            currentsvg.append('v {}'.format(dy))
                            base_point[1] += dy
                            for argset in zip(*(argsiter,) * 2):
                                currentsvg.append('h {} v {}'.format(*argset))
                                base_point[0] += argset[0]
                                base_point[1] += argset[1]
                        else:
                            for argset in zip(*(argsiter,) * 2):
                                currentsvg.append('v {} h {}'.format(*argset))
                                base_point[0] += argset[1]
                                base_point[1] += argset[0]
                    else:
                        raise TypeError('Unrecognized program token {}'.format(programstep))
                elif programstep.endswith('curveto'):
                    # be careful here. SVG defines relative curves as relative to the starting point of the curve
                    # CCF defines relative curves as relative to each previous point within the curve.
                    if programstep == 'rrcurveto': # |- {dxa dya dxb dyb dxc dyc}+ rrcurveto (8) |-
                        # TESTED
                        bpoints = [0,0,0,0,0,0]
                        for argset in zip(*(iter(pstack),) * 6):
                            bpoints[0] = argset[0]
                            bpoints[1] = argset[1]
                            bpoints[2] = argset[2]+bpoints[0]
                            bpoints[3] = argset[3]+bpoints[1]
                            bpoints[4] = argset[4]+bpoints[2]
                            bpoints[5] = argset[5]+bpoints[3]
                            currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                    elif programstep == 'vvcurveto': # |- dx1? {dya dxb dyb dyc}+ vvcurveto (26) |-
                        bpoints = [0,0,0,0,0,0]
                        argsiter = iter(pstack)
                        if len(pstack) % 4: # if not zero, then dx1 is there
                            dx1 = argsiter.__next__()
                            bpoints[0] = dx1
                        else:
                            bpoints[0] = 0
                            
                        for argset in zip(*(argsiter,) * 4):
                            #bpoints[0] +=         # bpoints[4] # dxa
                            bpoints[1] = argset[0]#+bpoints[5] # dya
                            bpoints[2] = argset[1]+bpoints[0] # dxb
                            bpoints[3] = argset[2]+bpoints[1] # dyb
                            bpoints[4] =          +bpoints[2] # dxc
                            bpoints[5] = argset[3]+bpoints[3] # dyc
                            base_point[0], base_point[1] = bpoints[4], bpoints[5]
                            currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                            bpoints[0] = 0
                        
                    elif programstep == 'hhcurveto': # |- dy1? {dxa dxb dyb dxc}+ hhcurveto (27) |-
                        bpoints = [0,0,0,0,0,0]
                        argsiter = iter(pstack)
                        if len(pstack) % 4: # if not zero, then dy1 is there
                            dy1 = argsiter.__next__()
                            bpoints[1] = dy1
                        else:
                            bpoints[1] = 0
                            
                        for argset in zip(*(argsiter,) * 4):
                            bpoints[0] = argset[0]#+bpoints[4] # dxa
                            #bpoints[1] +=         # bpoints[5] # dya
                            bpoints[2] = argset[1]+bpoints[0] # dxb
                            bpoints[3] = argset[2]+bpoints[1] # dyb
                            bpoints[4] = argset[3]+bpoints[2] # dxc
                            bpoints[5] =          +bpoints[3] # dyc
                            base_point[0], base_point[1] = bpoints[4], bpoints[5]
                            currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                            bpoints[1] = 0
                    elif programstep == 'hvcurveto': 
                        # |- dx1 dx2 dy2 dy3 {dya dxb dyb dxc dxd dxe dye dyf}* dxf? hvcurveto (31) |-
                        # |- {dxa dxb dyb dyc dyd dxe dye dxf}+ dyf? hvcurveto (31) |-
                        # appends one or more Bézier curves to the current point. The
                        # tangent for the first Bézier must be horizontal, and the second
                        # must be vertical (except as noted below).
                        # If there is a multiple of four arguments, the curve starts
                        # horizontal and ends vertical. Note that the curves alternate
                        # between start horizontal, end vertical, and start vertical, and
                        # end horizontal. The last curve (the odd argument case) need not
                        # end horizontal/vertical.
                        
                        # to decode, note that the first four are always x x y y 
                        # and the second set of four are y x y x
                        # we rely on that pattern, but we shift writing out by one
                        # set, so we can save the last to check for even/odd
                        # using dxc = None as the check for the first
                        dxc = None
                        bpoints = [0,0,0,0,0,0]
                        count = 0
                        for points in zip(*(iter(pstack),) * 4):
                            count+=1
                            # dxc is None first time through, 
                            # print after loop and save the last curve to print after we check even/odd
                            if dxc is not None:
                                currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                            if count % 2: # case 1
                                dxa,dxb,dyb,dyc = points
                                dya,dxc = 0,0
                            else:
                                dya,dxb,dyb,dxc = points
                                dxa,dyc = 0,0

                            bpoints[0],bpoints[1] =  dxa, dya
                            bpoints[2],bpoints[3] = bpoints[0]+dxb,bpoints[1]+dyb
                            bpoints[4],bpoints[5] = bpoints[2]+dxc,bpoints[3]+dyc

                        if len(pstack) % 2: # is odd
                            if count % 2: # case 1
                                bpoints[4] += pstack[-1]
                            else: # case 2
                                bpoints[5] += pstack[-1]
                                
                        currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                        base_point[0],base_point[1] = bpoints[4],bpoints[5]
                    elif programstep == 'vhcurveto': 
                        # |- dy1 dx2 dy2 dx3 {dxa dxb dyb dyc dyd dxe dye dxf}* dyf? vhcurveto (30) |-
                        # |- {dya dxb dyb dxc dxd dxe dye dyf}+ dxf? vhcurveto (30) |- 
                        # pattern is y1x2y2x3 then x1x2y2y3
                        dxc = None
                        bpoints = [0,0,0,0,0,0]
                        count = 0
                        for points in zip(*(iter(pstack),) * 4):
                            count+=1
                            # dxc is None first time through, 
                            # print after loop and save the last curve to print after we check even/odd
                            if dxc is not None:
                                currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                            if not count % 2: # case 2
                                dxa,dxb,dyb,dyc = points
                                dya,dxc = 0,0
                            else:
                                dya,dxb,dyb,dxc = points
                                dxa,dyc = 0,0

                            bpoints[0],bpoints[1] =  dxa, dya
                            bpoints[2],bpoints[3] = bpoints[0]+dxb,bpoints[1]+dyb
                            bpoints[4],bpoints[5] = bpoints[2]+dxc,bpoints[3]+dyc

                        if len(pstack) % 2: # is odd
                            if not count % 2: # case 2 # this is opposite to the hvcurveto end
                                bpoints[4] += pstack[-1]
                            else: # case 2
                                bpoints[5] += pstack[-1]
                                
                        currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                        base_point[0],base_point[1] = bpoints[4],bpoints[5]
                    else:
                        raise TypeError('Unrecognized program token {}'.format(programstep))
            elif programstep == 'rlinecurve': # |- {dxa dya}+ dxb dyb dxc dyc dxd dyd rlinecurve (25) |-
                # TESTED
                # pstack = [25,25,-591,592,76,-11,106,-4,88,12]
                bpoints = [0,0,0,0,0,0]
                #print('rlinecurve')
                for argset in zip(*(iter(pstack[:-6]),) * 2):
                    currentsvg.append('l {} {}'.format(*argset))
                    base_point[0] += argset[0]
                    base_point[1] += argset[1]
                bpoints[0], bpoints[1] =            pstack[-6]           , pstack[-5]
                bpoints[2], bpoints[3] = bpoints[0]+pstack[-4], bpoints[1]+pstack[-3]
                bpoints[4], bpoints[5] = bpoints[2]+pstack[-2], bpoints[3]+pstack[-1]
                currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                base_point[0], base_point[1] = bpoints[4], bpoints[5]
            elif programstep == 'rcurveline': # - {dxa dya dxb dyb dxc dyc}+ dxd dyd rcurveline (24) |-
                # TESTED
                bpoints = [0,0,0,0,0,0]
                for argset in zip(*(iter(pstack),) * 6):
                    bpoints[0], bpoints[1] =            argset[0]           , argset[1]
                    bpoints[2], bpoints[3] = bpoints[0]+argset[2], bpoints[1]+argset[3]
                    bpoints[4], bpoints[5] = bpoints[2]+argset[4], bpoints[3]+argset[5]
                    currentsvg.append('c {} {} {} {} {} {}'.format(*bpoints))
                    base_point[0], base_point[1] = bpoints[4], bpoints[5]
                currentsvg.append('l {} {}'.format(*pstack[-2:]))
                base_point[0] += pstack[-2]
                base_point[1] += pstack[-1]
            elif programstep == 'endchar':
                pass
            else:
                raise TypeError('Unrecognized program token {}'.format(programstep))
            pstack.clear()
                
                # remove_hints() removes (and resolves?)
                # 'cntrmask'
                # 'hintmask'
                # 'hstem'
                # 'vstem'
                # 'hstemhm'
                # 'vstemhm'
                # desubroutinize() resolves and removes callgsubr and callsubr
                # 'callgsubr'
                # # where are the charstrings for subroutines and global subroutines?
                
                # 'callsubr'
                
                
                # if programstep == '':
                # elif programstep == '':
                # elif programstep == '':
                # elif programstep == '':
                # elif programstep == '':
                # elif programstep == '':
                # else:
                    # raise TypeError("unexpected program code {}".format(programstep))
        return currentsvg
        
    def svgfromttf(self,coordTables,userelative=True):
        currentsvg = []
        for contour in self.glyph_contours_generator(coordTables):
            # generator returns a tuple of (point,oncurve_flag), the first one will always be oncurve
            point,onflag = contour.__next__() # python3: __next__; python2: next
            base_point=[0.0,0.0]

            # previousoncurvepoint will hold the last oncurve point, in prep for a line or bezier
            # this holds the last on curve point used for line or bezier, depending on if current point is on or off curve
            previousoncurvepoint = point 
            previousoffcurvepoint = False # this holds a point if the last point was off curve, otherwise is False
            # to know if the immediately previous point is on curve: previousoffcurve = bool(previousoffcurvepoint)
            if userelative:
                currentsvg.append('m {} {}'.format(*self.delta(point,base_point)))
            else:
                currentsvg.append('M {} {}'.format(*point))
            
            for point,onflag in contour:


                #if previousoffcurvepoint: 
                    # if onflag: # we know this is after the first point
                        # # onflag and not previousonflag

                        # # previousoncurvepoint = point
                        # # bezier to (previousoffcurvepoint, previousoncurvepoint)
                        # # previousoffcurvepoint = None

                    # else:
                        # # not onflag and not previousonflag
                        # # calculate implied point, and output previous bezier, saving current point as offpoint for future bezier

                        # # previousoncurvepoint = calculate_implied(previousoffcurvepoint,point)
                        # # bezier to (previousoffcurvepoint, previousoncurvepoint)
                        # # previousoffcurvepoint = point

                    
     
                # break this up into four conditions
                #if previousoff and onflag, bezier(previousoff,point); previouson = point; previousoff=None
                #if previousoff and not onflag, bezier(previousoff,implied); previouson = implied; ; previousoff=point
                #if not previousoff and onflag, line(point); previouson = point; previousoff=None
                #if not previousoff and not onflag, save point to previousoff
                if previousoffcurvepoint: 
                    # optimize in code space by having one location to define bezier at the expense of an extra onflag check.
                    if onflag:
                        previousoncurvepoint = point                                
                    else:
                        previousoncurvepoint = self.calculate_implied(previousoffcurvepoint,point)
                    # bezier to (previousoffcurvepoint, previousoncurvepoint)
                    if userelative:
                        currentsvg.append('q {} {} {} {}'.format(*self.delta(previousoffcurvepoint,base_point)+self.delta(previousoncurvepoint,base_point)))
                    else:
                        currentsvg.append('Q {} {} {} {}'.format(*previousoffcurvepoint+previousoncurvepoint))
                    previousoffcurvepoint = not onflag and point # if onflag, False; else point; repeats onflag check (performance hit)
                else:
                    if onflag: # onflag and previousonflag. This repeats code slightly, but only executes one assign in each location.
                        previousoncurvepoint = point                                
                        if userelative:
                            currentsvg.append('l {} {}'.format(*self.delta(previousoncurvepoint,base_point)))
                        else:
                            currentsvg.append('L {} {}'.format(*previousoncurvepoint))                    
                    else: # not onflag and previousonflag, save point for future bezier
                        previousoffcurvepoint = point
        return currentsvg

# ttf['kern'].kernTables[0].kernTable
#
# {('uni044E', 'uni0434'): -104, ('uni044E', 'uni0436'): -51, ('uni044E', 'uni043B'): -51, 
# ('uni044E', 'uni043C'): -27, ('uni044E', 'uni0442'): -27, ('uni044E', 'uni0444'): -12, 
# ('uni044E', 'uni0445'): -80, ('uni044E', 'uni0447'): -78, ('uni045E', 'comma'): -205, 
# ('uni045E', 'period'): -205, ('uni045E', 'guillemotright'): 25, ('uni0490', 'comma'): -203, 
# ('uni0490', 'period'): -203, ('uni0490', 'colon'): -51, ('uni0490', 'semicolon'): -51, 
# ('uni0490', 'guillemotleft'): -180, ('uni0490', 'guillemotright'): -78, ('uni0490', 'emdash'): -51}
