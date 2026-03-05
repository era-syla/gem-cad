import cadquery as cq

# Define parameters
length = 100.0
width = 20.0
thickness = 3.0
hole_diameter_large = 4.0
hole_diameter_small = 2.0
large_holes_count = 5
small_holes_count = 6

# Create main body
plate = cq.Workplane("XY").rect(length, width).extrude(thickness)

# Add rounded ends
plate = plate.faces(">Z").workplane().center(-(length/2 - width/2), 0).circle(width/2).cutThruAll()
plate = plate.faces(">Z").workplane().center((length/2 - width/2), 0).circle(width/2).cutThruAll()

# Add large holes
for i in range(large_holes_count):
    x_offset = -length/2 + width/2 + (length - width)/(large_holes_count - 1) * i
    plate = plate.faces(">Z").workplane().center(x_offset, 0).circle(hole_diameter_large/2).cutThruAll()

# Add small holes arranged in a circular pattern around each large hole
for i in range(large_holes_count):
    x_offset = -length/2 + width/2 + (length - width)/(large_holes_count - 1) * i
    plate = plate.faces(">Z").workplane().center(x_offset, 0).polarArray(5, 0, 360, small_holes_count).circle(hole_diameter_small/2).cutThruAll()

result = plate