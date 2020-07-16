import re

# converted from https://stackoverflow.com/a/3162732
def beziercubic(qp0,qp1,qp2):

    cp0 = qp0[0],qp0[1]
    cp3 = qp2[0],qp2[1]

    # The two control points for the cubic are:

    cp1 = qp0[0] + 2.0/3 *(qp1[0]-qp0[0]),qp0[1] + 2.0/3 *(qp1[1]-qp0[1])
    cp2 = qp2[0] + 2.0/3 *(qp1[0]-qp2[0]),qp2[1] + 2.0/3 *(qp1[1]-qp2[1])
    # cp0 = qp0
    # cp3 = qp2

    # # The two control points for the cubic are:

    # cp1 = qp0 + 2.0/3 *(qp1-qp0)
    # cp2 = qp2 + 2.0/3 *(qp1-qp2)

    return cp0,cp1,cp2,cp3
    
# converted from https://mortoray.com/2017/02/16/rendering-an-svg-elliptical-arc-as-bezier-curves/
def bezierfromellipticalarc():
    # /**
        # Perform the endpoint to center arc parameter conversion as detailed in the SVG 1.1 spec.
        # F.6.5 Conversion from endpoint to center parameterization

        # @param r must be a ref in case it needs to be scaled up, as per the SVG spec
    # */
    # internal static void EndpointToCenterArcParams( float2 p1, float2 p2, ref float2 r_, float xAngle, 
        # bool flagA, bool flagS, out float2 c, out float2 angles )
    # {
        # double rX = Math.Abs(r_.X);
        # double rY = Math.Abs(r_.Y);

        # //(F.6.5.1)
        # double dx2 = (p1.X - p2.X) / 2.0;
        # double dy2 = (p1.Y - p2.Y) / 2.0;
        # double x1p = Math.Cos(xAngle)*dx2 + Math.Sin(xAngle)*dy2;
        # double y1p = -Math.Sin(xAngle)*dx2 + Math.Cos(xAngle)*dy2;

        # //(F.6.5.2)
        # double rxs = rX * rX;
        # double rys = rY * rY;
        # double x1ps = x1p * x1p;
        # double y1ps = y1p * y1p;
        # // check if the radius is too small `pq < 0`, when `dq > rxs * rys` (see below)
        # // cr is the ratio (dq : rxs * rys) 
        # double cr = x1ps/rxs + y1ps/rys;
        # if (cr > 1) {
            # //scale up rX,rY equally so cr == 1
            # var s = Math.Sqrt(cr);
            # rX = s * rX;
            # rY = s * rY;
            # rxs = rX * rX;
            # rys = rY * rY;
        # }
        # double dq = (rxs * y1ps + rys * x1ps);
        # double pq = (rxs*rys - dq) / dq;
        # double q = Math.Sqrt( Math.Max(0,pq) ); //use Max to account for float precision
        # if (flagA == flagS)
            # q = -q;
        # double cxp = q * rX * y1p / rY;
        # double cyp = - q * rY * x1p / rX;

        # //(F.6.5.3)
        # double cx = Math.Cos(xAngle)*cxp - Math.Sin(xAngle)*cyp + (p1.X + p2.X)/2;
        # double cy = Math.Sin(xAngle)*cxp + Math.Cos(xAngle)*cyp + (p1.Y + p2.Y)/2;

        # //(F.6.5.5)
        # double theta = svgAngle( 1,0, (x1p-cxp) / rX, (y1p - cyp)/rY );
        # //(F.6.5.6)
        # double delta = svgAngle(
            # (x1p - cxp)/rX, (y1p - cyp)/rY,
            # (-x1p - cxp)/rX, (-y1p-cyp)/rY);
        # delta = Math.Mod(delta, Math.PIf * 2 );
        # if (!flagS)
            # delta -= 2 * Math.PIf;

        # r_ = float2((float)rX,(float)rY);
        # c = float2((float)cx,(float)cy);
        # angles = float2((float)theta, (float)delta);
    # }

    # static float svgAngle( double ux, double uy, double vx, double vy )
    # {
        # var u = float2((float)ux, (float)uy);
        # var v = float2((float)vx, (float)vy);
        # //(F.6.5.4)
        # var dot = Vector.Dot(u,v);
        # var len = Vector.Length(u) * Vector.Length(v);
        # var ang = Math.Acos( Math.Clamp(dot / len,-1,1) ); //floating point precision, slightly over values appear
        # if ( (u.X*v.Y - u.Y*v.X) < 0)
            # ang = -ang;
        # return ang;
    # }
    pass


# from https://codereview.stackexchange.com/a/28565
COMMANDS = set('MmZzLlHhVvCcSsQqTtAa')
COMMAND_RE = re.compile("([MmZzLlHhVvCcSsQqTtAa])")
FLOAT_RE = re.compile("[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?")

def _tokenize_path(pathdef):
    for x in COMMAND_RE.split(pathdef):
        if x in COMMANDS:
            yield x
        for token in FLOAT_RE.findall(x):
            yield token

#_tokenize_path.next = _tokenize_path.__next__
def fromsvgcontours(svgdpath,debug=False,simplified=0):
    """Geometry,Conversion [PATH_D_ATTRIBUTE] Converts SVG path element "d attribute"
        derived from TTF contours to a list geoms suitable for the newdrawing command. 
        We only have to consider M, L, and Q. newdrawing,"""
    geomformat = not bool(simplified)
    # if not geomformat: output a listoflists of points, 
    # each sublist is its own set of line segments
    # if accuracy == 0, then output simplified.
    
    # accomodate identifying holes in contours.
    # essentially we will treat the entire svg as a set of polygons.
    # we'll consider the commands M, L, and Q as only those are in 
    # TTF, where we need the hole determination.

    #print(path)
    #transform = matrixTransform2d()
    #transform.scale((float(inputs[1]),float(inputs[1])))
    # svgdpath = inputs
    #output('dpath={}'.format(svgdpath))
    # if isinstance(inputs[1],basestring):
        # inputnumbers = split(inputs[1])
    # else:
        # inputnumbers = inputs[1]
    
    #scale = float(inputs[1])
    geometry_output = []
    geoms = []
    simplified_outlines = [] # an array to hold geom arrays, where Qq is held as line segments from start, through control point, to end. This will be used for calculating whether the contour is a polygon or a hole.
    tokenized = _tokenize_path(svgdpath)
    
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
            if initialposition is not None and (initialposition[0] != position[0] or initialposition[1] != position[1]):
                if geomformat:
                    geometry_output[-1].extend(['Line',list(position),list(initialposition)])
                else:
                    geometry_output[-1].append(tuple(initialposition))
            # continue
        elif command == 'm':
            #simplified_outlines.append([])
            geometry_output.append([])
            #if geoms[-1] != 'Group':
            #    geoms.append('Group')
            # "If a relative moveto (m) appears as the first element of the path, then it is treated as a pair of absolute coordinates. In this case, subsequent pairs of coordinates are treated as relative even though the initial moveto is interpreted as an absolute moveto."
            if position is None:
                position = [0.0,0.0]
            position[0] += float(currenttoken)      
            position[1] += float(next(tokenized))  
            initialposition = list(position)
            command = 'l'
        elif command == 'M':
            #simplified_outlines.append([])
            geometry_output.append([])
            #if geoms[-1] != 'Group':
            #    geoms.append('Group')
        # "M633 1437q0 83 78 83h290q86 0 86 -78q0 -72 -88 -72h-208v-72q216 0 366 -151q159 -160 159 -389t-204 -405q-137 -118 -321 -118v-134q0 -101 -91 -101h-282q-89 0 -89 73q0 76 90 76h214v86q-217 0 -373 156q-160 160 -160 361q0 228 120 355q184 195 413 195v135z M633 1147q-132 0 -245 -88q-134 -104 -134 -293q0 -171 128 -284q102 -90 251 -90v755zM792 1147v-755q164 0 263 108q110 120 110 277q0 164 -134 282q-100 88 -239 88z" 0.02 mm fromsvg newdrawing refresh
        # "M633 1437q0 83 78 83" 0.02 mm fromsvg newdrawing refresh
            if position is None:
                position = [0.0,0.0]
            #output('currenttoken={}'.format(currenttoken))
            position[0] = float(currenttoken)       
            position[1] = float(next(tokenized))   
            initialposition = list(position)
            if not geomformat:
                geometry_output[-1].append(tuple(initialposition))
            command = 'L'
        elif command == 'l':
            points[0][0] = position[0]
            points[0][1] = position[1]
            position[0] += float(currenttoken)    
            position[1] += float(next(tokenized))
            if geomformat:
                geometry_output[-1].extend(['Line',list(points[0]),list(position)])
            else:
                geometry_output[-1].append(tuple(position))
        elif command == 'L':
            points[0][0] = position[0]
            points[0][1] = position[1]
            position[0] = float(currenttoken)       
            position[1] = float(next(tokenized))   
            if geomformat:
                geometry_output[-1].extend(['Line',list(points[0]),list(position)])
            else:
                geometry_output[-1].append(tuple(position))
        elif command == 'h':
            points[0][0] = position[0]
            points[0][1] = position[1]
            position[0] += float(currenttoken)      
            if geomformat:
                geometry_output[-1].extend(['Line',list(points[0]),list(position)])
            else:
                geometry_output[-1].append(tuple(position))
        elif command == 'H':
            points[0][0] = position[0]
            points[0][1] = position[1]
            position[0] = float(currenttoken)       
            if geomformat:
                geometry_output[-1].extend(['Line',list(points[0]),list(position)])
            else:
                geometry_output[-1].append(tuple(position))
        elif command == 'v':
            points[0][0] = position[0]
            points[0][1] = position[1]
            position[1] += float(currenttoken)      
            if geomformat:
                geometry_output[-1].extend(['Line',list(points[0]),list(position)])
            else:
                geometry_output[-1].append(tuple(position))
        elif command == 'V':
            points[0][0] = position[0]
            points[0][1] = position[1]
            position[1] = float(currenttoken)       
            if geomformat:
                geometry_output[-1].extend(['Line',list(points[0]),list(position)])
            else:
                geometry_output[-1].append(tuple(position))
        elif command in 'cCsS': # cubic bezier
            if command == 'c':
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[1][0] = points[0][0]+float(currenttoken)      
                points[1][1] = points[0][1]+float(next(tokenized))  
                points[2][0] = points[0][0]+float(next(tokenized))   
                points[2][1] = points[0][1]+float(next(tokenized))  
                position[0] = points[0][0]+float(next(tokenized))   
                position[1] = points[0][1]+float(next(tokenized))   
            elif command == 'C':
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[1][0] = float(currenttoken)      
                points[1][1] = float(next(tokenized))  
                points[2][0] = float(next(tokenized))  
                points[2][1] = float(next(tokenized)) 
                position[0] = float(next(tokenized))   
                position[1] = float(next(tokenized))   
            elif command == 's':
                # Draws a cubic Bezier curve from the current point to (x,y). The first control point is assumed to be the reflection of the second control point on the previous command relative to the current point. (If there is no previous command or if the previous command was not an C, c, S or s, assume the first control point is coincident with the current point.) (x2,y2) is the second control point (i.e., the control point at the end of the curve). S (uppercase) indicates that absolute coordinates will follow; s (lowercase) indicates that relative coordinates will follow. Multiple sets of coordinates may be specified to draw a polybezier. At the end of the command, the new current point becomes the final (x,y) coordinate pair used in the polybezier.
                if previouscommand in "cCsS":
                    points[1] = list(reflected_point(points[2],position))
                else:
                    points[1] = list(position)
                    # control point 
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[2][0] = points[0][0]+float(currenttoken)    
                points[2][1] = points[0][1]+float(next(tokenized))                  
                position[0] = points[0][0]+float(next(tokenized)) 
                position[1] = points[0][1]+float(next(tokenized))                  
            elif command == 'S':
                if previouscommand in "cCsS":
                    points[1] = list(reflected_point(points[2],position))
                else:
                    points[1] = list(position)
                    # control point 
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[2][0] = float(currenttoken)    
                points[2][1] = float(next(tokenized))                    
                position[0] = float(next(tokenized)) 
                position[1] = float(next(tokenized)) 
            bezier_points = (tuple(points[0]),tuple(points[1]),tuple(points[2]),tuple(position))

            if geomformat:
                geometry_output[-1].extend(tuple('Bezier')+bezier_points)
            else:
                geometry_output[-1].extend(bezier_points[1:])
        elif command in 'qQtT':
            if command == 'q':
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[1][0] = points[0][0]+float(currenttoken)       
                points[1][1] = points[0][1]+float(next(tokenized))   
                position[0] = points[0][0]+float(next(tokenized))    
                position[1] = points[0][1]+float(next(tokenized))    
            elif command == 'Q':
                points[0][0] = position[0]
                points[0][1] = position[1]
                points[1][0] = float(currenttoken)        
                points[1][1] = float(next(tokenized))   
                position[0] = float(next(tokenized))    
                position[1] = float(next(tokenized))    


            elif command == 't':
                # Draws a quadratic Bezier curve from the current point to (x,y). The control point is assumed to be the reflection of the control point on the previous command relative to the current point. (If there is no previous command or if the previous command was not a Q, q, T or t, assume the control point is coincident with the current point.) T (uppercase) indicates that absolute coordinates will follow; t (lowercase) indicates that relative coordinates will follow. At the end of the command, the new current point becomes the final (x,y) coordinate pair used in the polybezier.
                if previouscommand in "qQtT":
                    points[1] = list(reflected_point(points[1],position))
                else:
                    points[1] = list(position)
                    # control point 
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[0] = points[0][0]+float(currenttoken)    
                position[1] = points[0][1]+float(next(tokenized))                     
            elif command == 'T':
                if previouscommand in "qQtT":
                    points[1] = list(reflected_point(points[1],position))
                else:
                    points[1] = list(position)
                    # control point 
                points[0][0] = position[0]
                points[0][1] = position[1]
                position[0] = float(currenttoken)    
                position[1] = float(next(tokenized))                  
            bezier_points = beziercubic(points[0],points[1],position)
            if geomformat:
                geometry_output[-1].extend(['Bezier',bezier_points])
            else:
                geometry_output[-1].extend(bezier_points[1:])
        elif command == 'a':
            points[0][0] = position[0]
            points[0][1] = position[1]
            # float(currenttoken)                # rx
            float(next(tokenized))              # ry
            float(next(tokenized))              # x-axis rotation (degrees)
            bool(int(next(tokenized)))          # large-arc-flag (0 or 1)
            bool(int(next(tokenized)))          # sweep-flag     (0 or 1)
            position[0] = points[0][0]+float(next(tokenized))
            position[1] = points[0][1]+float(next(tokenized))                  
            output('Unsupported SVG path command: %s - elliptical arc (relative)'%command)
            # (rx ry x-axis-rotation large-arc-flag sweep-flag x y)+
        elif command == 'A':
            points[0][0] = position[0]
            points[0][1] = position[1]
            # float(currenttoken)                # rx
            float(next(tokenized))              # ry
            float(next(tokenized))              # x-axis rotation (degrees)
            bool(int(next(tokenized)))          # large-arc-flag (0 or 1)
            bool(int(next(tokenized)))          # sweep-flag     (0 or 1)
            position[0] = float(next(tokenized))
            position[1] = float(next(tokenized))                  
            output('Unsupported SVG path command: %s - elliptical arc (absolute)'%command)
            
    
    # geoms returned are the contour geoms
    return geometry_output