import cadquery as cq

# Parameters
total_length = 100.0   # Overall length of the handle
total_height = 30.0    # Overall height from top to bottom
depth = 20.0           # Depth of the profile
thickness = 5.0        # Thickness of the material
leg_width = 25.0       # Width of the mounting legs on the ends

# Create the profile sketch
# We will draw the side profile on the XZ plane and extrude it in Y (depth)
# The shape is essentially a "U" or staple shape, but flattened.

# Define the points for the path
# Point 0: Bottom left corner of left leg
# Point 1: Top left corner of left leg
# Point 2: Top right corner of right leg
# Point 3: Bottom right corner of right leg
# And the inner corresponding points to give it thickness

pts = [
    (0, 0),                       # Bottom left outer
    (0, total_height),            # Top left outer
    (total_length, total_height), # Top right outer
    (total_length, 0),            # Bottom right outer
    (total_length - thickness, 0),# Bottom right inner
    (total_length - thickness, total_height - thickness), # Top right inner corner
    (thickness, total_height - thickness),      # Top left inner corner
    (thickness, 0),               # Bottom left inner
]

# We will create the main bridge shape first
profile = (
    cq.Workplane("XY")
    .rect(total_length, depth)
    .extrude(thickness)
)

# Create the left leg
left_leg = (
    cq.Workplane("XY")
    .rect(thickness, depth)
    .extrude(-total_height + thickness) # Extrude downwards
    .translate((-total_length/2 + thickness/2, 0, 0))
)

# Create the right leg
right_leg = (
    cq.Workplane("XY")
    .rect(thickness, depth)
    .extrude(-total_height + thickness) # Extrude downwards
    .translate((total_length/2 - thickness/2, 0, 0))
)

# The image shows wider pads at the bottom/ends, let's look closer.
# Actually, the image shows a "U" shape handle but laid flat or viewed isometrically.
# Let's re-evaluate the geometry.
# It looks like a flat bar that bends down at 90 degrees at both ends.
# The "legs" seem to be wider than the thickness of the bar itself? 
# No, looking at the corners, the thickness is uniform.
# It looks like a standard drawer handle.
# However, the "legs" (the vertical parts) are actually rectangular blocks in the image,
# while the bridge is a thinner section connecting them? 
# Let's look really closely at the connections.
# The top surface is continuous.
# The vertical faces are perpendicular.
# It looks like a simple bent metal strip or a milled bracket.
# Let's assume a uniform cross-section for simplicity, or slightly modify based on visual cues.
# The left "leg" looks like a square plate. The right "leg" looks like a square plate.
# The bridge connects the top edges.

# Let's refine the approach to match the specific "blocky" look of the ends.
# It looks like two rectangular blocks connected by a bridge.

leg_height = 40.0
leg_width = 30.0    # Along the main axis
leg_depth = 20.0    # Transverse axis
bridge_thickness = 5.0 

# Strategy: Construct a shape that looks exactly like the image.
# It appears to be a single continuous top surface.
# Underneath, there is material at the ends but a gap in the middle.

# Base shape: A large rectangle for the top surface
# Plus two blocks extending downwards at the ends.

# Revised Parameters
length = 120.0
width = 40.0       # The depth dimension in the image
height = 30.0      # Total Z height
top_thickness = 5.0 # Thickness of the horizontal bar
leg_len = 25.0      # Length of the solid sections at the ends along the main axis

# Create the top plate
top_plate = cq.Workplane("XY").box(length, width, top_thickness)

# Create the legs
# Left Leg
leg_l = (
    cq.Workplane("XY")
    .workplane(offset=-top_thickness/2) # Start from bottom of top plate
    .center(-length/2 + leg_len/2, 0)
    .box(leg_len, width, height - top_thickness, centered=(True, True, False)) # Extrude downwards (using centered False for Z)
    .mirror("XY") # Flip Z direction to go down
)

# Right Leg
leg_r = (
    cq.Workplane("XY")
    .workplane(offset=-top_thickness/2)
    .center(length/2 - leg_len/2, 0)
    .box(leg_len, width, height - top_thickness, centered=(True, True, False))
    .mirror("XY")
)

# Combine them
result = top_plate.union(leg_l).union(leg_r)

# Optional: Add small fillets to the edges to make it look realistic like the render
# The render has sharp edges, but a tiny fillet usually helps rendering.
# Based on the sharp appearance, I will stick to a very small fillet or chamfer if visible,
# but the image looks quite sharp. I will leave it sharp to be safe, or add a tiny fillet.
# Let's maintain the sharp geometry as primary.

# To strictly match the orientation in the image:
# The image shows the object "lying down" or with the legs pointing away/down.
# Let's ensure the orientation in the viewer matches the isometric view.
# The current code creates it centered on XY plane, legs pointing -Z.
# This is a standard orientation for such a part.