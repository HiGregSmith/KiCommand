import math
import itertools
#import pcbnew
    
class wxPointUtil:
    """A variety of utilities and geometric calculations for
       operating on wxPoint objects. Will work on other objects with
       x,y attributes"""
       
    atts=('x','y','z')
    d=[]
    # 
    # Possible functions to implement for point class: 
    # __add__(), __radd__(), __iadd__(), __mul__(), __rmul__() and __imul__()
    # 
        
    @staticmethod
    def dot_other(v,w):
        return v[0]*w[1] - v[1]*w[0]	
    @staticmethod
    def dot(v,w):
        """return the dot product of point and w"""
        return v[0]*w[0] - v[1]*w[1]	
    @staticmethod
    def distance2(v,w):
        """return the distance squared between point and w"""
        #sub=w-v
        wvx = w[0] - v[0]
        wvy = w[1] - v[1]
        return wvx*wvx+wvy*wvy #abs(wxPointUtil.dot(sub,sub))
    @staticmethod
    def distance(v,w):
        """return the distance between point and w"""
        p = v - w
        return (p[0]*p[0]+p[1]*p[1])**(1/2.0)
        
    # Vector functions
    @staticmethod
    def scale(w,factor):
        """ scale (multiply) the point x and y by a specific factor"""
        # self[0] *= factor
        # self[1] *= factor
        return w.__class__(float(w[0])*factor,float(w[1])*factor)
    
    @staticmethod
    def mag(w):
        return math.sqrt(w[0]*w[0]+w[1]*w[1])
        
    # @staticmethod
    # def unit(w):
        # """return unit vector in same angle as w"""
        # return wxPointUtil.scale(w,1/wxPointUtil.mag(w))
        
    @staticmethod
    def rotatexy(w,radians):
        """rotates an x,y vector by a radians"""
        s=math.sin(radians)
        c=math.cos(radians)
        return w.__class__(w[0]*c - w[1]*s, w[0]*s + w[1]*c)
        
    @staticmethod
    def topolar(w):
        """returns polar coordinates in radians"""
        return sqrt(math.pow(w[0],2),math.pow(w[1],2)), math.atan(w[1]/w[0])
        
    @staticmethod
    def toxy(r,theta):
        return r*math.cos(theta),r*math.sin(theta)

    # @staticmethod
    # def towxPoint(r,theta):
        # return pcbnew.wxPoint(r*math.cos(theta),r*math.sin(theta))
    
    @staticmethod
    def projection_axis(v, axis):
        """Project the point onto axis specified by w.
           w must be a vector on the unit circle (for example: (1,0) or (0,1)
           to project on the x axis or y axis, respectively)"""
           
        # Consider the line extending the segment,
        # parameterized as v + t (w - v).
        # We find projection of point p onto the line. 
        # It falls where t = [(p-v) . (w-v)] / |w-v|^2
        t = wxPointUtil.dot(v,axis);
        return t
        
    # v,w are points defining the line segment
    @staticmethod
    def projection_line(p, v, w):
        """project point onto the line segment v,w"""
        # Return minimum distance between line segment vw and point p
        # Consider the line extending the segment,
        # parameterized as v + t (w - v).
        # We find projection of point p onto the line. 
        # It falls where t = [(p-v) . (w-v)] / |w-v|^2
        # We clamp t from [0,1] to handle points outside the segment vw.
        # if w[0] == v[0] and w[1] == v[1]:
            # return self.distance(w);   # v == w case

        #print "divisor=",w.distance(v)
        wv=w-v
        wvx = w[0] - v[0]
        wvy = w[1] - v[1]
        pvx = p[0] - v[0]
        pvy = p[1] - v[1]
        #t=0.5
        t = max(0, min(1, abs(pvx*wvx+pvy*wvy) / float(wvx*wvx+wvy*wvy)));
        #t = max(0, min(1, wxPointUtil.dot(p - v,wv) / float(wxPointUtil.distance2(w,v))));
        projection = v + wxPointUtil.scale(wv,t);  # Projection falls on the segment
        return projection
    
    @staticmethod
    def ccw(A,B,C):
        return (C.y-A.y) * (B.x-A.x) > (B.y-A.y) * (C.x-A.x)

    # Return true if line segments AB and CD intersect
    @staticmethod
    def intersect(A,B,C,D):
        return wxPointUtil.ccw(A,C,D) != wxPointUtil.ccw(B,C,D) and wxPointUtil.ccw(A,B,C) != wxPointUtil.ccw(A,B,D)
    
    
    # from https://www.geeksforgeeks.org/check-if-two-given-line-segments-intersect/
    # Given three colinear points p, q, r, the function checks if  
    # point q lies on line segment 'pr'  
    @staticmethod
    def onSegment(p, q, r): 
        if ( (q[0] <= max(p[0], r[0])) and (q[0] >= min(p[0], r[0])) and 
               (q[1] <= max(p[1], r[1])) and (q[1] >= min(p[1], r[1]))): 
            return True
        return False
    @staticmethod  
    def orientation(p, q, r): 
        # to find the orientation of an ordered triplet (p,q,r) 
        # function returns the following values: 
        # 0 : Colinear points 
        # 1 : Clockwise points 
        # 2 : Counterclockwise 
          
        # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/  
        # for details of below formula.  
          
        val = (float(q[1] - p[1]) * (r[0] - q[0])) - (float(q[0] - p[0]) * (r[1] - q[1])) 
        if (val > 0): 
              
            # Clockwise orientation 
            return 1
        elif (val < 0): 
              
            # Counterclockwise orientation 
            return 2
        else: 
              
            # Colinear orientation 
            return 0
      
    # The main function that returns true if  
    # the line segment 'p1q1' and 'p2q2' intersect. 
    @staticmethod
    def doLinesIntersect(p1,q1,p2,q2): 
          
        # Find the 4 orientations required for  
        # the general and special cases 
        o1 = wxPointUtil.orientation(p1, q1, p2) 
        o2 = wxPointUtil.orientation(p1, q1, q2) 
        o3 = wxPointUtil.orientation(p2, q2, p1) 
        o4 = wxPointUtil.orientation(p2, q2, q1) 
      
        # General case 
        if ((o1 != o2) and (o3 != o4)): 
            return True
      
        # Special Cases 
      
        # p1 , q1 and p2 are colinear and p2 lies on segment p1q1 
        if ((o1 == 0) and wxPointUtil.onSegment(p1, p2, q1)): 
            return True
      
        # p1 , q1 and q2 are colinear and q2 lies on segment p1q1 
        if ((o2 == 0) and wxPointUtil.onSegment(p1, q2, q1)): 
            return True
      
        # p2 , q2 and p1 are colinear and p1 lies on segment p2q2 
        if ((o3 == 0) and wxPointUtil.onSegment(p2, p1, q2)): 
            return True
      
        # p2 , q2 and q1 are colinear and q1 lies on segment p2q2 
        if ((o4 == 0) and wxPointUtil.onSegment(p2, q1, q2)): 
            return True
      
        # If none of the cases 
        return False
    
    
    @staticmethod
    def doPolygonsIntersect(a,b):
        for aline in zip(a,a[1:]):
            for bline in zip(b,b[1:]):
                if wxPointUtil.doLinesIntersect(aline[0],aline[1],bline[0],bline[1]):
                    return (aline,bline)
        return False
    @staticmethod
    def normal(w):
        return w.__class__(-w[1],w[0])
        # or (w[1],-w[0])
    def normal_old(v, w):
        """NOT FINISHED
           get normals of line formed with point w 
           This is the left normal if w is clockwise of self 
           This is the right normal if w is counter-clockwise of self"""
        w[0] - v[0], 
        w[1] - v[1]
    
    # var normals:Vector.<Vector2d> = new Vector.<Vector2d>
    # for (var i:int = 1; i < dots.length-1; i++) 
    # {
        # var currentNormal:Vector2d = new Vector2d(
            # dots[i + 1][0] - dots[i][0], 
            # dots[i + 1][1] - dots[i][1]
        # ).normL //left normals
        # normals.push(currentNormal);
    # }
    # normals.push(
        # new Vector2d(
            # dots[1][0] - dots[dots.length-1][0], 
            # dots[1][1] - dots[dots.length-1][1]
        # ).normL
    # )
    # return normals;

    @staticmethod
    def mindistance2(u, v, w):
        """Return minimum distance squared between point and line segment v,w.
           Perhaps obviously, this is faster than mindistance because sqrt()
           is not called."""
        #L2 = wxPointUtil.distance2(v,w)
        if w[0] == v[0] and w[1] == v[1]:
        #if L2 == 0.0:
            return wxPointUtil.distance2(u,w);   # v == w case
        return wxPointUtil.distance2(u,wxPointUtil.projection_line(u,v,w))        
        
    @staticmethod
    def mindistance(u, v, w):
        """return minimum distance squared between point and line segment v,w"""
        L2 = wxPointUtil.distance2(w,v)
        #if w[0] == v[0] and w[1] == v[1]:
        if L2 == 0.0:
            return wxPointUtil.distance(u,w);   # v == w case
        return wxPointUtil.distance(u,wxPointUtil.projection_line(u,v,w))
        
        # L2 = v.distance2(w);  # i.e. |w-v|^2 -  avoid a sqrt
        # if (L2 == 0.0):
            # return p.distance(w);   # v == w case
        # return p.distance(self.projection_line(v,w));
        
        # p = self
        # # Return minimum distance between line segment vw and point p
        # L2 = self.distance2(v, w);  # i.e. |w-v|^2 -  avoid a sqrt
        # if (L2 == 0.0):
            # return p.distance(v);   # v == w case
        # # Consider the line extending the segment,
        # # parameterized as v + t (w - v).
        # # We find projection of point p onto the line. 
        # # It falls where t = [(p-v) . (w-v)] / |w-v|^2
        # # We clamp t from [0,1] to handle points outside the segment vw.
        # t = max(0, min(1, (p - v).dot(w - v) / float(L2)));
        # # SavePrint = "L2 %d; t %.3f"%(L2,t)
        
        # #t = max(0, min(1, (v - p).dot(v - w) / float(L2)));
        # projection = v + (w-v).scale(t);  # Projection falls on the segment
        # return p.distance(projection);
                
    #https://stackoverflow.com/questions/2272179/a-simple-algorithm-for-polygon-intersection
    # NB: The algorithm only works for convex polygons, specified in either clockwise, or counterclockwise order.

    # 1)For each edge in both polygons, check if it can be used as a separating line. If so, you are done: No intersection.
    # 2) If no separation line was found, you have an intersection

    @staticmethod
    def check_polygons_intersecting(poly_a, poly_b,closed=True):
        """Returns boolean indicating whether the indicated polygons are intersecting.
           closed=True indicates the last point is equal to the first point.
           if closed=False, the first and last point are checked as if they represent
           the last polygon edge."""
        for polygon in (poly_a, poly_b):
            #print "\nPolygon",

            # This loop is assuming last point is not the repeated first point:
            # for i1 in range(len(polygon)):
                # i2 = (i1 + 1) % len(polygon)
                
            # This loop assumes the last point is the repeated first point to form closed polygon:
            # for i1 in range(len(polygon)-1):
                # i2 = (i1 + 1)
                
            # This loop combines both loops above:
            for i1 in range(len(polygon)-1*closed):
                i2 = (i1 + 1) % len(polygon)
                
                #print("i1={} i2={}".format(polygon[i1], i2))
                p1 = polygon[i1]
                p2 = polygon[i2]

                normal_old = (p2[1] - p1[1], p1[0] - p2[0]) # pcbnew.wxPoint(p2[1] - p1[1], p1[0] - p2[0])

                minA, maxA, minB, maxB = (None,) * 4

                for p in poly_a:
                    projected = normal_old[0] * p[0] + normal_old[1] * p[1]

                    if not minA or projected < minA:
                        minA = projected
                    if not maxA or projected > maxA:
                        maxA = projected

                for p in poly_b:
                    projected = normal_old[0] * p[0] + normal_old[1] * p[1]

                    if not minB or projected < minB:
                        minB = projected
                    if not maxB or projected > maxB:
                        maxB = projected

                #print("maxA={} minB={} -- maxB={} minA={}".format(maxA, minB, maxB, minA))
                if maxA < minB or maxB < minA:
                    return False
                #print(" Nope\n")

        return True
        
    # To find orientation of ordered triplet (p, q, r).
    # The function returns following values
    # 0 --> p, q and r are colinear
    # 1 --> Clockwise
    # 2 --> Counterclockwise
    # sign = lambda x: x and (1, -1)[x < 0]
    
    # Get leftmost point
    # i, value = min(enumerate(vector), key=attrgetter('x'))
    # nextpoint = vector[(i+1)%len(vector)]
    # @staticmethod
    # def orientation(p, q, r)
    # {
        # int val = (q[1] - p[1]) * (r[0] - q[0]) -
                  # (q[0] - p[0]) * (r[1] - q[1]);
     
        # if (val == 0) return 0;  // colinear
        # return (val > 0)? 1: 2; // clock or counterclock wise
    # }
    
    @staticmethod
    def convex_hull(self,line,vector):
        """NOT IMPLEMENTED.
           Currently returns bounding box, best used on orthogonal.
           Return the convex hull of point list vector
           A fast algorithm using Jarvis's Algorithm (aka Wrapping)."""
        minx = vector[0][0]
        miny = vector[0][1]
        maxx = minx
        maxy = miny
        for v in vector:
            minx = min(minx,v[0])
            maxx = max(minx,v[0])
            miny = min(miny,v[1])
            maxy = max(miny,v[1])           
        return (
            (minx,maxy), # upper left
            (maxx,maxy), # upper right
            (maxx,miny), # lower right
            (minx,miny)) # lower left
