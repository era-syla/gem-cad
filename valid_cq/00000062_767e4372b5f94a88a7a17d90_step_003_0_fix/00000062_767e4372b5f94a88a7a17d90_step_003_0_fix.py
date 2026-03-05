import cadquery as cq
import math

# Create a decorative bracket/corbel with S-scroll design
# This is a flat plate with decorative scrollwork cut out

thickness = 3

# Create the outer L-shaped bracket profile
# The bracket appears to be roughly triangular/corner bracket shape
# with decorative S-scroll cutouts

# Build the outer profile as a 2D shape
# The bracket is like a right-angle corner bracket with scrollwork

# Outer dimensions
width = 120
height = 60

# Create base plate - triangular corner bracket
pts_outer = [
    (0, 0),
    (width, 0),
    (width, 8),
    (8, 8),
    (8, height),
    (0, height),
    (0, 0),
]

# Create the main plate shape using a polygon outline
plate = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(width, 0)
    .lineTo(width, 8)
    .lineTo(8, 8)
    .lineTo(8, height)
    .lineTo(0, height)
    .close()
    .extrude(thickness)
)

# Add a diagonal brace from corner to corner (the main body)
# The scrollwork sits on a diagonal bar
# Create diagonal bar
import cadquery as cq

def make_bracket():
    # Main L-frame
    frame = (
        cq.Workplane("XY")
        .moveTo(0, 0)
        .lineTo(115, 0)
        .lineTo(115, 7)
        .lineTo(7, 7)
        .lineTo(7, 55)
        .lineTo(0, 55)
        .close()
        .extrude(thickness)
    )
    
    # Diagonal bar connecting the two ends of the L
    # from approx (7, 7) to (115, 0) area - the scrollwork panel
    # Create a parallelogram/strip for the diagonal decorative panel
    
    # The diagonal strip
    diag = (
        cq.Workplane("XY")
        .moveTo(7, 7)
        .lineTo(115, 7)
        .lineTo(7, 55)
        .close()
        .extrude(thickness)
    )
    
    combined = frame.union(diag)
    
    # Now cut scroll shapes
    # Large left scroll (S-shape) - approximate with circles
    # Left scroll circle - outer
    scroll1_x, scroll1_y = 30, 25
    r1_out = 16
    r1_in = 10
    
    scroll1_outer = (
        cq.Workplane("XY")
        .circle(r1_out)
        .extrude(thickness + 2)
        .translate((scroll1_x, scroll1_y, -1))
    )
    scroll1_inner = (
        cq.Workplane("XY")
        .circle(r1_in)
        .extrude(thickness + 2)
        .translate((scroll1_x, scroll1_y, -1))
    )
    
    # Right scroll
    scroll2_x, scroll2_y = 75, 20
    r2_out = 18
    r2_in = 12
    
    scroll2_outer = (
        cq.Workplane("XY")
        .circle(r2_out)
        .extrude(thickness + 2)
        .translate((scroll2_x, scroll2_y, -1))
    )
    scroll2_inner = (
        cq.Workplane("XY")
        .circle(r2_in)
        .extrude(thickness + 2)
        .translate((scroll2_x, scroll2_y, -1))
    )
    
    # Small top right scroll
    scroll3_x, scroll3_y = 93, 30
    r3_out = 10
    r3_in = 6
    
    scroll3_outer = (
        cq.Workplane("XY")
        .circle(r3_out)
        .extrude(thickness + 2)
        .translate((scroll3_x, scroll3_y, -1))
    )
    scroll3_inner = (
        cq.Workplane("XY")
        .circle(r3_in)
        .extrude(thickness + 2)
        .translate((scroll3_x, scroll3_y, -1))
    )
    
    # Cut the scroll rings (cut outer, keep inner as solid, then cut inner)
    result = combined
    result = result.cut(scroll1_outer).union(scroll1_inner)
    result = result.cut(scroll2_outer).union(scroll2_inner)
    result = result.cut(scroll3_outer).union(scroll3_inner)
    
    return result

result = make_bracket()