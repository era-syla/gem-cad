import cadquery as cq

# Define basic shape
shape = cq.Workplane("XY").polyline([
    (0, 0), (15, 0), (15, 10), (30, 10), 
    (30, 0), (45, 0), (45, 10), (60, 10), 
    (60, 0), (75, 0), (75, 20), (60, 20), 
    (60, 30), (45, 30), (45, 20), (30, 20), 
    (30, 30), (15, 30), (15, 20), (0, 20), 
    (0, 0)
]).close().extrude(5)

result = shape