import cadquery as cq

def create_frame():
    # Define points for the frame
    points = [
        (0, 0), (1, 0), (1, 1), (0, 1),
        (0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)
    ]
    
    # Create base frame
    frame = cq.Workplane("XY").polyline(points[:4]).close().extrude(1)
    
    # Add tubes at specified locations
    tubes = cq.Workplane("XY")
    for x, y, z in points[4:]:
        tubes = tubes.union(cq.Workplane("XY").workplane(offset=z).circle(0.05).extrude(1).translate((x, y, 0)))
    
    return frame.union(tubes)

result = create_frame()