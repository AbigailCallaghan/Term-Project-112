

class Line:
    def __init__(self, m, b):
        self.m = m
        self.b = b
    
    def __repr__(self):
        return f'y={self.m}x+{self.b}'
    
    def evalAt(self, value):
        return value * self.m + self.b
    def __eq__(self, other):
        return isinstance(other, Line) and self.m == other.m and self.b == other.b
    def __hash__(self):
        return hash(str(self))
    def getPerpendicularLineAt(self, x):
        newSlope = -1 / self.m
        yIntersection = self.evalAt(x)
        print(yIntersection)
        newB = yIntersection - (newSlope*x)
        return Line(newSlope, newB)




line1 = Line(2, 3)
assert(line1.m == 2)
assert(line1.b == 3)
assert(str(line1) == 'y=2x+3')
assert(str([line1]) == '[y=2x+3]')
assert(line1.evalAt(10) == 23) # evaluate y=2x+3 at x=10
assert(line1 == Line(2, 3))
assert(line1 != Line(3, 2))
assert(line1 != 'do not crash here')
s = set()
assert(Line(2, 3) not in s)
s.add(Line(2, 3))
assert(Line(2, 3) in s)
# line1.getPerpendicularLineAt(x) returns a new line that is
# perpendicular to line1 and intersects line1 at x.
# The perpendicular line has a slope of -1/m.
# You can assume that m != 0.
# Thus, line1.getPerpendicularLineAt(2) has a slope of -1/2.
# Since line1 goes through (2, 7), then
# line2 must also go through (2, 7).
# We use this to find b for line2.
# So line2 is y = -0.5x + 8.
line2 = line1.getPerpendicularLineAt(2)
print(line2.m)
print(line2.b)
print(line2.evalAt(2))
#ssert(almostEqual(line2.b, 8))
#assert(almostEqual(line2.evalAt(2), 7))