import cadquery as cq

# Main dimensions
width = 120
height = 90
depth = 100
thickness = 6

# Build the main frame structure
# Top plate
top_plate = (
    cq.Workplane("XY")
    .box(width, depth, thickness)
    .translate((0, 0, height - thickness/2))
)

# Left side panel (with X-brace cutout style)
left_panel = (
    cq.Workplane("YZ")
    .workplane(offset=-width/2)
    .box(depth, height, thickness)
    .translate((-width/2 + thickness/2, 0, height/2))
)

# Right side panel (solid with holes)
right_panel = (
    cq.Workplane("YZ")
    .workplane(offset=width/2)
    .box(depth, height, thickness)
    .translate((width/2 - thickness/2, 0, height/2))
)

# Back panel
back_panel = (
    cq.Workplane("XZ")
    .workplane(offset=-depth/2)
    .box(width, height, thickness)
    .translate((0, -depth/2 + thickness/2, height/2))
)

# Combine main frame
frame = top_plate.union(left_panel).union(right_panel).union(back_panel)

# Add bottom foot/base extensions
left_foot = (
    cq.Workplane("XY")
    .box(thickness, depth + 20, 20)
    .translate((-width/2 + thickness/2, 0, -10))
)

right_foot = (
    cq.Workplane("XY")
    .box(thickness, depth + 20, 20)
    .translate((width/2 - thickness/2, 0, -10))
)

frame = frame.union(left_foot).union(right_foot)

# Add diagonal brace elements on left side (X pattern)
brace1 = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .transformed(offset=(-width/2 + thickness + 2, 0, height/2))
    .box(thickness/2, depth - thickness*2, height - thickness*2)
)

# Create the X-brace on left side using rotated boxes
import math

brace_len = math.sqrt((depth-thickness*2)**2 + (height-thickness*2)**2)

# Diagonal brace 1
brace_diag1 = (
    cq.Workplane("YZ")
    .workplane(offset=-width/2 + thickness)
    .rect(thickness/1.5, brace_len)
    .extrude(thickness/1.5)
    .translate((-width/2 + thickness*1.5, 0, height/2))
    .rotate((-width/2+thickness, 0, 0), (-width/2+thickness, 1, 0), 
            math.degrees(math.atan2(height-thickness*2, depth-thickness*2)))
)

frame = frame.union(brace_diag1)

# Add mounting holes to right panel
frame = (
    frame
    .faces(">X")
    .workplane()
    .rarray(25, 22, 4, 3)
    .hole(5)
)

# Add holes to back panel
frame = (
    frame
    .faces("<Y")
    .workplane()
    .rarray(25, 22, 4, 3)
    .hole(5)
)

# Add holes to top plate
frame = (
    frame
    .faces(">Z")
    .workplane()
    .rarray(30, 25, 3, 2)
    .hole(5)
)

# Add small mounting bracket on top
bracket = (
    cq.Workplane("XY")
    .workplane(offset=height - thickness)
    .box(30, 20, thickness * 1.5)
    .translate((10, 10, height - thickness/2 + thickness*0.75))
)

# Add holes to bracket
bracket = (
    bracket
    .faces(">Z")
    .workplane()
    .pushPoints([(0, -3), (-8, -3), (8, -3), (0, 5)])
    .hole(4)
)

frame = frame.union(bracket)

# Final result
result = frame