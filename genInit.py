__author__  = ""
__date__    = "10 March 2023"
__version__ = "$Revision: 1.0.0 $"
__credits__ = """ 정운철이가 만듬 """

import os, sys, time, math

class Gen:
    def __init__(self) :
        self.prefix = "@%#%@"

        # Genesis 2000 환경 변수 Check
        if "GENESIS_DIR" not in os.environ:
            self.error("GENESIS_DIR not set", 1)
        self.gendir = os.environ["GENESIS_DIR"]
        if "GENESIS_EDIR" not in os.environ:
            self.error("GENESIS_EDIR not set", 1)
        self.edir = os.environ["GENESIS_EDIR"]
        if not os.path.isdir(self.edir):
            self.edir = os.path.join(self.gendir, self.edir)
        if not os.path.isdir(self.edir):
            self.error("Cannot normalize GENESIS_EDIR", 1)

        # 유일한 임시파일 생성 조건
        # Genesis 임시 폴더에 적용

        self.pid = os.getpid()
        tmp = "gen_"+repr(self.pid)+"."+repr(time.time())
        if "GENESIS_TMP" in os.environ:
            self.tmpfile = os.path.join(os.environ["GENESIS_TMP"], tmp)
            self.tmpdir = os.environ["GENESIS_TMP"]
        else:
            self.tmpfile = os.path.join("/genesis/tmp", tmp)
            self.tmpdir = "/genesis/tmp"
        
        self.blank()

    def error(self, msg, severity=0):
        sys.stderr.write(msg+'\n')
        if severity:
            sys.exit(severity)

    def blank(self):
        # Genesis stdio 입출력 command Return 저장 변수
        
        self.__STATUS   = 0
        self.__READANS  = ""
        self.__COMANS   = ""
        self.__PAUSANS  = ""
        self.__MOUSEANS = ""

    def __sendCmd(self, cmd, args=""):       
        self.blank()
        wsp = " "*(len(args)>0)
        cmd = self.prefix + cmd + wsp + args + "\n"
        sys.stdout.write(cmd)
        sys.stdout.flush()
        return 0

    def COM(self,args) :
        self.__sendCmd("COM", args)
        self.__STATUS = str(input())
        self.__READANS = input()
        self.__COMANS = self.__READANS[:]
        return self.__STATUS

    def MOUSE(self,mode,msg) :
        self.__sendCmd("MOUSE " + mode, msg)
        self.__STATUS = str(input())
        self.__READANS = input()
        self.__MOUSEANS = input()
        return self.__STATUS

    def PAUSE(self,msg) :
        self.__sendCmd("PAUSE", msg)
        self.__STATUS = str(input())
        self.__READANS = input()
        self.__PAUSANS = input()
        return self.__STATUS

    def VOF(self) :
        return self.__sendCmd("VOF")

    def VON(self) :
        return self.__sendCmd("VON")

    def AUX(self,args) :
        self.__sendCmd('AUX', args)
        self.__STATUS = str(input())
        self.__READANS = input()
        self.__COMANS = self.READANS[:]
        return self.__STATUS

    def SU_ON(self) :
        return self.__sendCmd("SU_ON")

    def SU_OFF(self) :
        return self.__sendCmd("SU_OFF")
        
    def DO_INFO(self, args):
        self.COM("info,out_file= %s,write_mode=replace,args= %s" % (self.tmpfile,args))
        lineList = open(self.tmpfile, 'r').readlines()
        Info_Dict = {}
        Info_List = []
        for VAL in lineList:
            ss = VAL.split("=")
            if len(ss) == 2:
                
                value = ss[1].strip()
                key = ss[0].strip("set").strip()
                if '(' in value:
                    valList = []
                    value = value.strip("\(").strip("\)").strip()
                    for chk in list(filter(None,value.split(" "))):
                        valList.append(chk.replace("'",""))
                    Info_Dict[key] = valList
                else:                    
                    Info_Dict[key] = value
            if VAL.find("#") != -1 :
                Info_List.append(VAL)

        os.unlink(self.tmpfile)

        if len(Info_Dict) < len(Info_List):
            return Info_List

        return Info_Dict
    
class GeoMetry:
    def __init__(self) :
        self.pi = 4 * math.atan(1)

    def FindLineInterSection(self, L1X1,L1Y1,L1X2,L1Y2,L2X1,L2Y1,L2X2,L2Y2):
        # References:
        # http://wiki.tcl.tk/12070 (Kevin Kenny)
        # http://local.wasp.uwa.edu.au/~pbourke/geometry/lineline2d/

        #set d [expr {($l2y2 - $l2y1) * ($l1x2 - $l1x1) - ($l2x2 - $l2x1) * ($l1y2 - $l1y1)}]
        d = (L2Y2 - L2Y1) * (L1X2 - L1X1) - (L2X2 - L2X1) * (L1Y2 - L1Y1)
        #set na [expr {($l2x2 - $l2x1) * ($l1y1 - $l2y1) - ($l2y2 - $l2y1) * ($l1x1 - $l2x1)}]
        na = (L2X2 - L2X1) * (L1Y1 - L2Y1) - (L2Y2 - L2Y1) * (L1X1 - L2X1)

        # http://local.wasp.uwa.edu.au/~pbourke/geometry/lineline2d/
        if d == 0 :
            if na == 0 :
                return "coincident"
            else :
                return "none"

        #set r [list [expr {$l1x1 + $na * ($l1x2 - $l1x1) / $d}] [expr {$l1y1 + $na * ($l1y2 - $l1y1) / $d}]]
        return [L1X1 + na * (L1X2 - L1X1) / d,L1Y1 + na * (L1Y2 - L1Y1) / d]
    
    def CCW(self,AX,AY,BX,BY,CX,CY) :

        dx1 = BX - AX
        dy1 = BY - AY
        dx2 = CX - AX
        dy2 = CY - AY
        
        if  dx1 * dy2 > dy1 * dx2:
            return 1
        if dx1 * dy2 < dy1 * dx2 :
            return -1
        if (dx1 * dx2 < 0) or (dy1 * dy2 < 0) :
            return -1
        if (dx1 * dx1 + dy1 * dy1) < (dx2 * dx2+ dy2* dy2) :
            return 1
        
        return 0
    
    def angle(self,X1,Y1,X2,Y2) :

        # - handle vertical lines
        if X1 == X2 :
            if Y1 < Y2 :
                return 90
            else :
                return 270
                       
        # - handle other lines
        # a is between 0 and pi/2
        a = math.atan(abs((1.0 * Y1 - Y2) / (1.0 * X1- X2)))

        if Y1 <= Y2 :
	        # line is going upwards
            if X1 < X2 :
                b = a
            else :
                b = self.pi - a
        else :
	        # line is going downwards
            if X1 < X2 :
                b = 2 * self.pi - a
            else :
                b = self.pi + a

        return b / self.pi * 180

    def movePointInDirection(self, X, Y, direction, dist) :
        xt = X + dist * math.cos( direction * self.pi) / 180
        yt = Y + dist * math.sin( direction * self.pi) / 180

        return xt,yt

    def ClosedPolygon(self, polygon) :
        if polygon[0] != polygon[-2] or polygon[1] != polygon[-1] :
            polygon.append(polygon[0])
            polygon.append(polygon[1])

        return polygon

    def bbox(PolyLine) :
        minX = PolyLine[0]
        maxX = minX
        minY = PolyLine[1]
        maxY = minY
        for i in range(int(len(PolyLine)/2)) :
            x = PolyLine[(i * 2)]
            y = PolyLine[(i * 2) + 1]
            if x < minX :
                minX = x
            if x > maxX :
                maxX = x
            if y < minY :
                minY = y
            if y > maxY :
                maxY = y

        return [minX, minY, maxX, maxY]

    def lineSegmentsIntersect(self, LineSegment1, LineSegment2) :
    # Algorithm based on SedgeWick.
        L1X1 = LineSegment1[0]
        L1Y1 = LineSegment1[1]
        L1X2 = LineSegment1[2]
        L1Y2 = LineSegment1[3]
        L2X1 = LineSegment2[0]
        L2Y1 = LineSegment2[1]
        L2X2 = LineSegment2[2]
        L2Y2 = LineSegment2[3]

        #
        # First check the distance between the endpoints
        #
        margin = 1.0e-7
        if self.calculateDistanceToLineSegment(LineSegment1[0:1], LineSegment2) < margin :
            return 1
        
        if self.calculateDistanceToLineSegment(LineSegment1[2:3], LineSegment2) < margin :
            return 1
        
        if self.calculateDistanceToLineSegment(LineSegment2[0:1], LineSegment2) < margin :
            return 1
        
        if self.calculateDistanceToLineSegment(LineSegment2[2:3], LineSegment2) < margin :
            return 1
        

        return self.ccw(L1X1, L1Y1, L1X2, L1Y2, L2X1, L2Y1) * self.ccw(L1X1, L1Y1, L1X2, L1Y2, L2X2, L2Y2) <= 0 \
	        and self.ccw(L2X1, L2Y1, L2X2, L2Y2, L1X1, L1Y1) * self.ccw(L2X1, L2Y1, L2X2, L2Y2, L1X2, L1Y2) <= 0
	        

    def pointInsidePolygon (self, P, polygon) :
        # check if P is on one of the polygon's sides (if so, P is not
        # inside the polygon)

        closedPolygon = self.ClosedPolygon(polygon)
        
        x1 = closedPolygon[0]
        y1 = closedPolygon[1]

        for i in range(1,int(len(closedPolygon)/2-1)) :
            x2 = closedPolygon[(i * 2)]
            y2 = closedPolygon[(i * 2) + 1]

            if self.calculateDistanceToLineSegment(P,[x1,y1,x2,y2]) < 0.0000001 :
                return 0
            
            x1 = x2
            y1 = y2

        # Algorithm
        #
        # Consider a straight line going from P to a point far away from both
        # P and the polygon (in particular outside the polygon).
        #   - If the line intersects with 0 of the polygon's sides, then
        #     P must be outside the polygon.
        #   - If the line intersects with 1 of the polygon's sides, then
        #     P must be inside the polygon (since the other end of the line
        #     is outside the polygon).
        #   - If the line intersects with 2 of the polygon's sides, then
        #     the line must pass into one polygon area and out of it again,
        #     and hence P is outside the polygon.
        #   - In general: if the line intersects with the polygon's sides an odd
        #     number of times, then P is inside the polygon. Note: we also have
        #     to check whether the line crosses one of the polygon's
        #     bend points for the same reason.

        # get point far away and define the line
        polygonBbox = self.bbox(polygon)
        pointFarAway = [polygonBbox[0] - polygonBbox[2], polygonBbox [1]- 0.1 * polygonBbox[3]]
        infinityLine = pointFarAway + P

        # calculate number of intersections
        noOfIntersections = 0
        #   1. count intersections between the line and the polygon's sides
        x1 = closedPolygon[0]
        y1 = closedPolygon[1]

        for i in range(1,int(len(closedPolygon)/2-1)) :
            if self.lineSegmentsIntersect(infinityLine,[x1, y1, x2 ,y2]) :
                noOfIntersections += 1
            x1 = x2
            y1 = y2

        #   2. count intersections between the line and the polygon's points
        for i in range(len(closedPolygon)/2) :
            x1 = closedPolygon[(i * 2)]
            y1 = closedPolygon[(i * 2) + 1]

            if self.calculateDistanceToLineSegment(infinityLine,[x1, y1]) < 0.0000001 :
                noOfIntersections += 1

        return noOfIntersections % 2

    def calculateDistanceToLineSegment(self, P, LineSegment):

        result = self.calculateDistanceToLineSegmentImpl(P, LineSegment)
        distToLine = result[0]
        r = result[1]

        if r < 0 :
            return self.lengthOfPolyLine(P + LineSegment[0:1])
        elif r > 1 :
            return self.lengthOfPolyLine(P + LineSegment[2:3])
        else :
            return distToLine
    
    def calculateDistanceToLineSegmentImpl(self, P, LineSegment) :

        # solution based on FAQ 1.02 on comp.graphics.algorithms
        # L = hypot( Bx-Ax , By-Ay )
        #     (Ay-Cy)(Bx-Ax)-(Ax-Cx)(By-Ay)
        # s = -----------------------------
        #                 L^2
        #      (Cx-Ax)(Bx-Ax) + (Cy-Ay)(By-Ay)
        # r = -------------------------------
        #                   L^2
        # dist = |s|*L
        #
        # =>
        #
        #        | (Ay-Cy)(Bx-Ax)-(Ax-Cx)(By-Ay) |
        # dist = ---------------------------------
        #                       L

        Ax = LineSegment[0]
        Ay = LineSegment[1]
        Bx = LineSegment[2]
        By = LineSegment[3]
        Cx = P[0]
        Cy = P[1]

        if Ax == Bx and Ay == By :
            return [self.lengthOfPolyLine(P + LineSegment[0:1]), 0]
        else :
            L = math.hypot(Bx - Ax,By - Ay)
            r = ((Cx - Ax) * (Bx - Ax) + (Cy - Ay) * (By - Ay)) / pow(L,2)
            return [abs((Ay - Cy) * (Bx - Ax) - (Ax - Cx) * (By - Ay)) / L, r]


    def lengthOfPolyLine(self,PolyLine) :
        length = 0

        x1 = PolyLine[0]
        y1 = PolyLine[1]

        for i in range(1,int(len(PolyLine)/2-1)):
            x2 = PolyLine[(i * 2)]
            y2 = PolyLine[(i * 2) + 1]

            length = length + math.hypot(x1-x2,y1-y2)
            x1 = x2
            y1 = y2

        return length

    def InSideAngle(self, L1, L2) :
        L1_ANG = self.angle(L1[0],L1[1],L1[2],L1[3])
        L2_ANG = self.angle(L2[0],L2[1],L2[2],L2[3])

        CHK_ANG = round(abs(L1_ANG - L2_ANG))
        
        if CHK_ANG == 180 or CHK_ANG == 0 :
            return -1
        else :
            return CHK_ANG < 180 if 180 - (L1_ANG  - L2_ANG) else (L1_ANG  - L2_ANG) - 180
        
    def CircleToCenterDist(self, DEG, R) :
        return R / math.sin(DEG * self.pi / 180)

    def CornerHolePoint(self, L1, L2, R_SIZE) :
        InSection = self.FindLineInterSection(L1[0],L1[1],L1[2],L1[3],L2[0],L2[1],L2[2],L2[3])
        if InSection == "none" or InSection == "coincident" :
            return
        
        ANGLE = self.InSideAngle(L1, L2)
        HALF_ANGLE = ANGLE / 2
        L1_ANGLE = self.angle(L1[0],L1[1],L1[2],L1[3])
        L2_ANGLE = self.angle(L2[0],L2[1],L2[2],L2[3])
        #CCW_LINE = self.ccw(L1[2],L1[3],L2[0],L2[1],L2[2],L2[3])

        if L2_ANGLE <= 180 :
            if L2_ANGLE < L1_ANGLE and L2_ANGLE + 180 > L1_ANGLE :
                CEN_ANGLE = L2_ANGLE - HALF_ANGLE
            else :
                CEN_ANGLE = L2_ANGLE + HALF_ANGLE
        else :
            if L2_ANGLE > L1_ANGLE and L2_ANGLE - 180 < L1_ANGLE :
                CEN_ANGLE = L2_ANGLE + HALF_ANGLE
            else :
                CEN_ANGLE = L2_ANGLE - HALF_ANGLE

        DIST = self.CircleToCenterDist(HALF_ANGLE, R_SIZE)
        HALF_POS = self.movePointInDirection(InSection,CEN_ANGLE,DIST)
        
        return HALF_POS
