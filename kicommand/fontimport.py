
try:
    import fontTools
    import fontTools.ttLib
except:
    pass
    
#import pickle
import os
from os import walk
import inspect
import itertools

import sys
import warnings
#print('The "imp" package is deprecated for this version of Python.\nHowever, the use of imp in kicommand_fonts.py needs to be compatible with Python 2.7\n')
warnings.filterwarnings("ignore", category=DeprecationWarning)# with action as "ignore"
import imp


try:
    pyfile = __file__
except:
    pyfile = sys.argv[0]
    
pyfile = os.path.abspath(pyfile)
pydir = os.path.dirname(pyfile)

print("Executing file: {}".format(pyfile))

kifonts = imp.load_source('kicommand_fonts', 'C:\Program Files\KiCad\KiCad-5.1.6\share\kicad\scripting\plugins\kicommand\kicommand_fonts.py')


font_pathcomponent_list = [('osifont-lgpl3fe.ttf',),('Noto','NotoSans-hinted','NotoSans-Regular.ttf')]
font_source_base = ['..','KiCad','KiCommand','fonts']
font_source_dirs = [r'.',r'Noto']

def list_files(directory, extension):
    for (dirpath, dirnames, filenames) in os.walk(directory):
        return [os.path.join(dirpath,f) for f in filenames if f.endswith('.' + extension)]
        
def getone(file):
    "Specify the full path to a ttf font file, and this will use fontTools to assign the variable 'ttf'"
    global ttf
    ttf_filefull = os.path.abspath(os.path.join(*font_source_base+[file]))
    ttf=fontTools.ttLib.TTFont(ttf_filefull)
    
# from https://stackoverflow.com/a/295466 (and Django)
# The slugify function has been moved to django/utils/text.py, and that file also contains a get_valid_filename function.
# http://github.com/django/django/blob/master/django/utils/text.py
# S,1000000,Thickness,100000,Line,323.0,635.0,323.0,0.0,635.0,403.0,305.0,403.0 split newdrawing refresh
def slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    #print ( type(value))
    import unicodedata
    import re
    unicode = str
    #value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    value = unicode(re.sub('[-\s]+', '-', value))
    # ...
    return value
    # \u00d8 stringtogeom Tmm,300,-5 split swap append newdrawing refresh

# makeone(r'C:\Users\gmsmith\Documents\Personal\kicad\KiCommand\fonts\Noto\NotoSans-Regular.ttf')
def makeone(file):
#makeone(r'C:\Users\gmsmith\Documents\Personal\kicad\KiCommand\fonts\Noto\NotoMono-Regular.ttf')
#makeone(r'C:\Users\gmsmith\Documents\Personal\kicad\KiCommand\fonts\OTC\NotoSansCJK.ttc\NotoSansCJK.ttc')

    "This creates a KiCommand-compatible file for the specified ttf font"
    ttf_filefull = os.path.abspath(os.path.join(r'C:\Users\gmsmith\Documents\Personal\kicad\KiCommand\fonts',file))

    kifonts._fontdata_directory = os.path.join(os.getcwd(),'fontdata')
    print('ttf file: {}'.format(ttf_filefull))

    try:
        tc=fontTools.ttLib.ttCollection.TTCollection(file=ttf_filefull, shareTables=False)
        ttflist = tc.fonts
    except:
        ttflist=[fontTools.ttLib.TTFont(ttf_filefull)]


    for ttf in ttflist:

        try:
            name = ttf['name'].names[4].toStr()
        except:
            name = os.path.splitext(os.path.basename(ttf_filefull))[0]
        name = slugify(name).capitalize()    

        ft = kifonts.fonttable()
        ft.load_ttf(name,ttf,userelative=False)
        ft.save_fontdata(os.path.join(pydir,name)) # os.getcwd()
        with open('tables.txt','a') as f:
            f.write('{}: {}\n\n'.format(name,ttf.keys()))
        
def makeall(dir=None,output=None,recursive=False,noexec=False):
    "Create a KiCommand-compatible file for all font files found (ttf, otf, ttc, otc)." 

    if dir is None:
        dir = os.path.join(pydir,'fonts')
    if output is None:
        output = os.path.join(pydir,'fontdata')
    print('input directory: {}'.format(dir))
    if not os.path.isdir(dir):
        print("(Doesn't exist)")
    print('output directory: {}'.format(output))# os.getcwd())
    if not os.path.isdir(output):
        print("(Doesn't exist)")
    for dirName, subdirList, fileList in os.walk(dir):
        for filename in fileList:
            fname, file_extension = os.path.splitext(filename)
            if file_extension not in ('.ttf','.otf','.otc','.ttc'):
                continue
            filefull = os.path.abspath(os.path.join(dirName,filename))
                        
            kifonts._fontdata_directory = output
            try:
                tc=fontTools.ttLib.ttCollection.TTCollection(file=filefull, shareTables=False)
                ttflist = tc.fonts
            except:
                ttflist=[fontTools.ttLib.TTFont(filefull)]
        
            print('font input file: {}'.format(os.path.relpath(filefull,dir)))
            for ttf in ttflist:

                name = None
                try:
                    name = ttf['name'].names[4].toStr()
                except:
                    pass
                #print('name starts with Version-? {}'.format(name.startswith(u'Version')))
                if (name is None) or name.startswith(u'Version'):
                    #print('changing name')
                    name = os.path.splitext(os.path.basename(filefull))[0]
                name = slugify(name).capitalize()

                if noexec:
                    print('    output font: {} ({} glyphs)'.format(os.path.relpath(os.path.join(pydir,name),pydir),len(ttf.getGlyphNames())))
                    if not recursive:
                        break
                    continue

                ft = kifonts.fonttable()
                ft.load_ttf(name,ttf,userelative=False)
                ft.save_fontdata(os.path.join(pydir,name)) # os.getcwd()
         
            # ttf=fontTools.ttLib.TTFont(filefull)
            # with open('tables.txt','a') as f:
                # f.write('{}: {}\n\n'.format(name,ttf.keys()))
        if not recursive:
            break
helptext = """
    Usage: fontimport -a directory
    
fontimport translates ttf files to a format readable to KiCommand. 

The directory specified should already exist and have a subdirectory named "ttf" which contains the ttf files that will be translated.
The results are placed in a directory named "fontdata" within the specified directory. 
If fontdata does not exist already, it will be created.
"""

    
    #ftnew=kifonts.fontmanager().getfonttable(r'..\osi')
    #print(ftnew._unicode_codepoint_lookup)
    
    # SVG Viewer  https://www.freecodeformat.com/svg-editor.php
    # unicode lookup - https://www.compart.com/en/unicode/U+2564
    # categorized unicode tables: https://www.ssec.wisc.edu/~tomw/java/unicode.html#x25A0

    # With KiCAD 5.1.6-release,

    # - "Within" in the following context means the polygon/hole exists in the same SHAPE_POLY_SET using AddOutline() or AddHole().    
    # - Multiple polygons within one DRAWSEGMENT can be created, and are moved together, yet only the first one can be selected (the others are selected simultaneously)
    # - multiple polygons within one DRAWSEGMENT are not saved
    # - Holes within polygons are displayed, but do not move together
    # - Holes within polygons are not displayed


    # SHAPE_POLY_SET has several methods that might be useful. There are also boolean operations using the Clipper library (the library I would have chosen as well)
    # Fracture (and Unfracture)
    # Simplify
    # The basic SHAPE_POLY_SET structure seems to support multiple outlines (filled contour) and multiple holes within an each outline.
    # However, this basic structure is not saved in full when saving the board.
        
from collections import defaultdict
from pprint import pprint
from fontTools import subset

def otf():
    ft = kifonts.fonttable()
    svgfromcff = ft.svgfromcff
    # t=fontTools.ttLib.ttFont.TTFont(r'C:\Users\gmsmith\Documents\Personal\kicad\KiCommand\fonts\OTC\NotoSansCJK.ttc\NotoSansCJK.ttc',fontNumber=0)
    
    # If shareTables is True, then different fonts in the collection might point to the same table object if the data for the table was the same in the font file. Note, however, that this might result in suprises and incorrect behavior if the different fonts involved have different GlyphOrder. 
    tc=fontTools.ttLib.ttCollection.TTCollection(file=filename, shareTables=False)

    currentpoint = [0.0,0.0]
    lastmoveto = [0.0,0.0]
    pstack = []
    tokens = defaultdict(set)
    # following https://docs.microsoft.com/en-us/typography/opentype/spec/cff2charstr
    # t['CFF '].cff[0].decompileAllCharStrings()
    count = 0
    # {'hmoveto', 'vmoveto', 'cntrmask', 'vvcurveto', 'hvcurveto', 'rlineto', 'hlineto', 'rmoveto', 'hintmask', 'rlinecurve', 'vhcurveto', 'vlineto', 'hstemhm', 'vstem', 'hhcurveto', 'hstem', 'rcurveline', 'callsubr', 'endchar', 'vstemhm', 'rrcurveto', 'callgsubr'}
    # following https://programtalk.com/python-examples/fontTools.ttLib.TTFont/?ipage=3
    # options = subset.Options(**kwargs)
    # options.desubroutinize = True
    # subsetter = subset.Subsetter(options=options)
    # subsetter.populate(glyphs=tmpfont.getGlyphOrder())
    # subsetter.subset(tmpfont)
    # char 'a' = codpoint 97 = 'cid00066'
    ft = kifonts.fonttable()
    svgfromcff = ft.svgfromcff
    for i,t in enumerate(tc.fonts):
        if i > 1:
            break
        fontname = t['CFF '].cff.fontNames
        print('\nFont #{}/{}: {}'.format(i,len(tc.fonts),fontname))
        print('desubroutinize')
        t['CFF '].desubroutinize()
        print('remove hints')
        t['CFF '].remove_hints()
        print('done remove hints')
        # options = subset.Options()
        # options.desubroutinize = True
        # subsetter = subset.Subsetter(options=options)
        # subsetter.populate(glyphs=t.getGlyphOrder())
        # subsetter.subset(t)
        #t['CFF '].cff[0].decompileAllCharStrings()
        
        for charname in ('cid00094',): # ('cid00066',):#t['CFF '].cff.otFont.getGlyphNames(): # ('cid00090',): # # ('cid00792',):#
            count += 1
            if not count % 1000:
                print('.',end='')
            charstring = t['CFF '].cff[0].CharStrings[charname]
            print('{}: {}'.format(charname,' '.join(svgfromcff(charstring))))
            
            # #print('char: {}'.format(charname))
            program = t['CFF '].cff[0].CharStrings[charname].program
            if not program:
                print('Warning: program zero length {}, {}'.format(fontname,charname))
            for programstep in program:
                #print('step: {} ({})'.format(programstep,type(programstep)))
                if isinstance(programstep,str):
                    tokens[programstep].add(len(pstack))
                    print('{} ({})'.format(programstep,','.join(map(str,pstack))))
                    pstack.clear()
                else:
                    pstack.append(programstep)
            pprint(tokens)
                    
                    # # remove_hints() removes (and resolves?)
                    # # 'cntrmask'
                    # # 'hintmask'
                    # # 'hstem'
                    # # 'vstem'
                    # # 'hstemhm'
                    # # 'vstemhm'
                    # # desubroutinize() resolves and removes callgsubr and callsubr
                    # # 'callgsubr'
                    # # # where are the charstrings for subroutines and global subroutines?
                    
                    # # 'callsubr'
                    

        
        # https://www.freecodeformat.com/svg-editor.php
        # <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200" viewbox="-1000 -1000 2000 2000" version="1.1">
  # <path  stroke="#000" stroke-width="20px" d="m 553 604 c 41 -59 64 -140 64 -239 c 0 -208 -102 -343 -255 -343 c -72 0 -134 30 -178 84 m -19 26 c -38 59 -60 138 -60 233 c 0 208 104 339 257 339 c 69 0 127 -26 171 -74 m 114 100 l -26 19 l -66 -90 c -51 52 -117 80 -193 80 c -173 0 -296 -145 -296 -374 c 0 -109 28 -199 75 -265 l -77 -104 l 25 -18 l 72 98 c 52 -57 121 -89 201 -89 c 171 0 295 149 295 378 c 0 113 -30 205 -81 270"></path>
  # https://rsms.me/fonttools-docs/ttLib/ttCollection.html
    # </svg>

import argparse

def create(args):
    print('input: {}\noutput: {}\nrecursive: {}\n'.format(args.input,args.output,args.recursive))

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()
#parser.add_argument('foo', nargs='+')

# parser = argparse.ArgumentParser()
parser.add_argument('--version', action='version', version='1.0.0')
#subparsers = parser.add_subparsers()

create_parser = parser # subparsers.add_parser('create')
create_parser.add_argument('--output', default=os.path.join(pydir,'fontdata'),help='output directory')
create_parser.add_argument('--input', default=os.path.join(pydir,'fonts'),help='input directory or file')
create_parser.add_argument('--recursive', action='store_true',help='search find files recursively when --input is a directory')
create_parser.add_argument('--exec', action='store_true',help='without this option, just list environment and files, but do not write to the output. Actually writing to the output requires this option.')
create_parser.set_defaults(func=create)

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)
    
if __name__ == '__main__':
    args = parser.parse_args()
    if hasattr(args,'func'):
        args.func(args)
    #print('calling makeall')
    makeall(dir=args.input,output=args.output,recursive=args.recursive,noexec=(not args.exec))
