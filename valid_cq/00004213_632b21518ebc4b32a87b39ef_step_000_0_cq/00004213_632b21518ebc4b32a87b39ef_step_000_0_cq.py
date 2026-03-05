import cadquery as cq

# Parameters for the main L-bracket shape
width = 60.0          # Overall width of the bracket
depth = 40.0          # Depth of the horizontal part
height = 40.0         # Height of the vertical part
thickness = 5.0       # Wall thickness

# Parameters for the gusset (triangular supports)
gusset_thick = 5.0

# Parameters for the cylinder
cyl_diam = 15.0
cyl_height = 40.0     # Height extending downwards

# Parameters for the holes
hole_diam = 4.0       # Through hole diameter
c_bore_diam = 8.0     # Counterbore diameter
c_bore_depth = 2.0    # Counterbore depth

# 1. Create the main L-bracket profile
# We will draw the L-shape on the YZ plane and extrude it along X (width)
# Profile points: (0,0) -> (depth, 0) -> (depth, thickness) -> (thickness, thickness) -> (thickness, height) -> (0, height) -> close
L_profile = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (depth, 0),
        (depth, thickness),
        (thickness, thickness),
        (thickness, height),
        (0, height),
        (0, 0)
    ])
    .close()
    .extrude(width)
)

# Center the L-bracket so the cylindrical post aligns well
# Moving it so the center of the bottom face is roughly at X=0, Y=depth/2
# But extruding along X by 'width' puts it from 0 to width. Let's center it.
L_bracket = L_profile.translate((-width/2, 0, 0))


# 2. Add the triangular gussets (side walls)
# We can create a wedge shape or sketch triangles on the side faces.
# Let's sketch on the inner side face and extrude inwards.

# Left Gusset
gusset_l = (
    cq.Workplane("YZ")
    .moveTo(thickness, thickness)
    .lineTo(depth, thickness)
    .lineTo(thickness, height)
    .close()
    .extrude(gusset_thick)
    .translate((-width/2, 0, 0)) # Position at left edge
)

# Right Gusset
gusset_r = (
    cq.Workplane("YZ")
    .moveTo(thickness, thickness)
    .lineTo(depth, thickness)
    .lineTo(thickness, height)
    .close()
    .extrude(-gusset_thick) # Extrude in negative X direction
    .translate((width/2, 0, 0)) # Position at right edge
)

# Combine bracket and gussets
body = L_bracket.union(gusset_l).union(gusset_r)

# 3. Add the cylindrical post extending downwards
# We place it at the center of the horizontal section.
# The horizontal section spans Y from 0 to depth. Center is depth/2.
# The Z level is 0 (bottom face).
post = (
    cq.Workplane("XY")
    .center(0, depth/2)
    .circle(cyl_diam / 2)
    .extrude(-cyl_height)
)

# Add fillet to the transition between post and plate
# To do this robustly, we union first, then fillet.
body = body.union(post)

# Find the edge at the intersection of the cylinder and the bottom plane
# This is tricky to select automatically, so we'll look for edges at Z=0 
# that are circular.
try:
    body = body.edges("(>Z[-cyl_height] and <Z[0.1]) and %Circle").fillet(3.0)
except:
    # Fallback if specific selection fails (sometimes complex unions break edge tags)
    pass 

# 4. Add Holes with Counterbores

# Vertical hole (through cylinder and bracket)
# Located at (0, depth/2)
body = (
    body.faces(">Z")
    .workplane()
    .center(0, depth/2)
    .cboreHole(hole_diam, c_bore_diam, c_bore_depth)
)

# Horizontal holes (on the vertical back plate)
# The back plate is at Y=0. We want to drill into it.
# Holes need to be spaced out.
hole_spacing = 30.0 # Distance between holes
hole_height_z = (height + thickness) / 2 # Roughly centered vertically on the back plate

body = (
    body.faces("<Y") # Select the back face
    .workplane(centerOption="CenterOfBoundBox")
    # Shift workplane center to align with where we want holes
    .center(0, (height/2) - (thickness/2)) 
    .pushPoints([(-hole_spacing/2, 0), (hole_spacing/2, 0)])
    .cboreHole(hole_diam, c_bore_diam, c_bore_depth)
)

result = body