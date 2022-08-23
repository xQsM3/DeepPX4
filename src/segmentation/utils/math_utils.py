import math
import numpy as np
class Point:  # class-object for point coordinates (X,Y)
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Polyline:  # main class
    def __init__(self, pol):  # constructor
        self.polyline_points = []
        for dot in pol:
            self.polyline_points.append(Point(dot[0], dot[1]))  # insert points coordinates in list of "Point" objects
        return

    def Add(self, x, y):
        self.polyline_points.append(Point(x, y))
        return

    def PrintPoints(self, file=None):  # output points
        print("X  Y", file = file)
        for dot in self.polyline_points:
            print(str(dot.x) + "  " + str(dot.y), file = file)
        return

    def Segments(self):
        segments = []  # get all segments of polyline
        a = self.polyline_points[0]
        for i in range(1, len(self.polyline_points)):
            b = self.polyline_points[i]
            segments.append((a, b))
            a = b
        return segments

    def Perimeter(self):  # get perimeter of polyline
        length = 0.0
        segments = self.Segments()
        for seg in segments:
            distance = math.hypot(seg[1].x - seg[0].x, seg[1].y - seg[0].y)  # distance of segments
            length += distance  # add distances
        return length

    def SelfIntersections(self):
        epsilon = 1e-13
        def LineIntersects(p1, p2, q1, q2):  # check if intersection present for segment

            def Clockwise(p0, p1, p2):  # check for intersection of all point combinations
                dx1 = p1.x - p0.x
                dy1 = p1.y - p0.y
                dx2 = p2.x - p0.x
                dy2 = p2.y - p0.y
                d = dx1 * dy2 - dy1 * dx2  # distance
                if d > epsilon: return 1
                if d < epsilon: return -1
                if dx1 * dx2 < -epsilon or dy1 * dy2 < -epsilon: return -1
                if dx1 * dx1 + dy1 * dy1 < (dx2 * dx2 + dy2 * dy2) + epsilon: return 1
                return 0

            return (Clockwise(p1, p2, q1) * Clockwise(p1, p2, q2) <= 0) and (
                0 >= Clockwise(q1, q2, p1) * Clockwise(q1, q2, p2))

        def line(p1, p2):  # find A,B,C coefficients for line
            A = (p1.y - p2.y)
            B = (p2.x - p1.x)
            C = (p1.x * p2.y - p2.x * p1.y)
            return A, B, -C

        def IntersectionPoint(L1, L2):  # find intersection point for two lines
            D = L1[0] * L2[1] - L1[1] * L2[0]
            Dx = L1[2] * L2[1] - L1[1] * L2[2]
            Dy = L1[0] * L2[2] - L1[2] * L2[0]
            if D != 0:
                x = Dx / D
                y = Dy / D
                return x, y
            else:
                return False

        segments = self.Segments()
        present = []
        for seg1 in segments:  # for all combinations of segments
            for seg2 in segments:
                if (seg1[0] != seg2[1] and seg1[1] != seg2[0]) and \
                        (seg1[1] != seg2[1] and seg1[0] != seg2[0]):  # exclude points of segments connection
                    if LineIntersects(seg1[0], seg1[1], seg2[0], seg2[1]) == True:  # check if current segment intersect
                        L1 = line(seg1[0], seg1[1])  # find line coefficients (A, B, C) for segment parts
                        L2 = line(seg2[0], seg2[1])
                        P = IntersectionPoint(L1, L2)  # get point coordinate of intersection
                        present.append(P)  # add points to list
        answer = sorted(set(present))  # clean list from duplicate points
        return answer  # return list of points

    def SelfApproaches(self,epsilon=1):
        # checks if polyline approaches itselfs (not intersect) under a given threshold
        segments = self.Segments()
        present = []
        for i,seg1 in enumerate(segments):  # for all combinations of segments
            for j,seg2 in enumerate(segments):
                if (seg1[0] != seg2[1] and seg1[1] != seg2[0]) and \
                        (seg1[1] != seg2[1] and seg1[0] != seg2[0]):  # exclude points of segments connection
                    closeness = self.check_if_too_close(seg1[0], seg1[1], seg2[0], seg2[1])

                    if closeness[2] < epsilon:  # check if current segment approaches under epsilon thresh distance
                        if closeness[0] is not None \
                                and closeness[1] is not None \
                                and closeness[2] is not None: # if not None

                            p1 = tuple(closeness[0].tolist())
                            p2 = tuple(closeness[1].tolist())
                            distance = closeness[2]
                            present.append((p1,p2,distance))# add points to list
        answer = sorted(set(present))  # clean list from duplicate points
        return answer  # return list of points

    def CheckIfPointInside(self, x, y):  # check if point (x, y) is on polyline
        epsilon = 1e-13

        def isBetween(a, b, c):  # check if point c between points a and b
            cross_product = (c.y - a.y) * (b.x - a.x) - (c.x - a.x) * (b.y - a.y)  # cross production
            if abs(cross_product) > epsilon: return False

            dot_product = (c.x - a.x) * (b.x - a.x) + (c.y - a.y) * (b.y - a.y)  # dot production
            if dot_product < 0: return False

            squared_length = (b.x - a.x) * (b.x - a.x) + (b.y - a.y) * (b.y - a.y)  # squared length
            if dot_product > squared_length: return False

            return True

        p = Point(x, y)
        isInside = False
        segments = self.Segments()
        for seg in segments:
            isInside = isBetween(seg[0], seg[1], p)  # check each segment if point inside of it
            if isInside == True:
                break
        return isInside

    def check_if_too_close(self,a0, a1, b0, b1, twoD=True, clampAll=True, clampA0=True, clampA1=True, clampB0=True,
                                    clampB1=True):

        ''' Given two lines defined by numpy.array pairs (a0,a1,b0,b1)
            Return the closest points on each segment and their distance
        '''

        # If clampAll=True, set all clamps to True
        if clampAll:
            clampA0 = True
            clampA1 = True
            clampB0 = True
            clampB1 = True

        if twoD:
            a0 = np.array([a0.x, a0.y,0])
            a1 = np.array([a1.x, a1.y,0])
            b0 = np.array([b0.x, b0.y,0])
            b1 = np.array([b1.x, b1.y,0])
        else:
            a0 = np.array([a0.x, a0.y,a0.z])
            a1 = np.array([a1.x, a1.y,a1.z])
            b0 = np.array([b0.x, b0.y,b0.z])
            b1 = np.array([b1.x, b1.y,b1.z])
        # Calculate denomitator
        A = a1 - a0
        B = b1 - b0
        magA = np.linalg.norm(A)
        magB = np.linalg.norm(B)

        _A = A / magA
        _B = B / magB

        cross = np.cross(_A, _B);
        denom = np.linalg.norm(cross) ** 2

        # If lines are parallel (denom=0) test if lines overlap.
        # If they don't overlap then there is a closest point solution.
        # If they do overlap, there are infinite closest positions, but there is a closest distance
        if not denom:
            d0 = np.dot(_A, (b0 - a0))

            # Overlap only possible with clamping
            if clampA0 or clampA1 or clampB0 or clampB1:
                d1 = np.dot(_A, (b1 - a0))

                # Is segment B before A?
                if d0 <= 0 >= d1:
                    if clampA0 and clampB1:
                        if twoD:
                            a0 = a0[:2]  # remove Z dummies
                            b0 = b0[:2]
                            b1 = b1[:2]
                        if np.absolute(d0) < np.absolute(d1):
                            return a0, b0, np.linalg.norm(a0 - b0)
                        return a0, b1, np.linalg.norm(a0 - b1)

                # Is segment B after A?
                elif d0 >= magA <= d1:
                    if clampA1 and clampB0:
                        if twoD:
                            a1 = a1[:2]  # remove Z dummies
                            b0 = b0[:2]
                            b1 = b1[:2]
                        if np.absolute(d0) < np.absolute(d1):
                            return a1, b0, np.linalg.norm(a1 - b0)
                        return a1, b1, np.linalg.norm(a1 - b1)

            # Segments overlap, return distance between parallel segments
            return None, None, np.linalg.norm(((d0 * _A) + a0) - b0)

        # Lines criss-cross: Calculate the projected closest points
        t = (b0 - a0);
        detA = np.linalg.det([t, _B, cross])
        detB = np.linalg.det([t, _A, cross])

        t0 = detA / denom;
        t1 = detB / denom;

        pA = a0 + (_A * t0)  # Projected closest point on segment A
        pB = b0 + (_B * t1)  # Projected closest point on segment B

        # Clamp projections
        if clampA0 or clampA1 or clampB0 or clampB1:
            if clampA0 and t0 < 0:
                pA = a0
            elif clampA1 and t0 > magA:
                pA = a1

            if clampB0 and t1 < 0:
                pB = b0
            elif clampB1 and t1 > magB:
                pB = b1

            # Clamp projection A
            if (clampA0 and t0 < 0) or (clampA1 and t0 > magA):
                dot = np.dot(_B, (pA - b0))
                if clampB0 and dot < 0:
                    dot = 0
                elif clampB1 and dot > magB:
                    dot = magB
                pB = b0 + (_B * dot)

            # Clamp projection B
            if (clampB0 and t1 < 0) or (clampB1 and t1 > magB):
                dot = np.dot(_A, (pB - a0))
                if clampA0 and dot < 0:
                    dot = 0
                elif clampA1 and dot > magA:
                    dot = magA
                pA = a0 + (_A * dot)

        if twoD:
            pA = pA[:2] # remove Z dummies
            pB = pB[:2]
        return pA, pB, np.linalg.norm(pA - pB)