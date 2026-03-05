import cadquery as cq

# Parametric dimensions
length = 80.0
width = 20.0
height = 30.0
wall_thickness = 5.0  # Thickness of the clevis ears

# Clevis (fork) dimensions
clevis_depth = 25.0
clevis_gap = 12.0
clevis_hole_diam = 8.0
clevis_outer_radius = height / 2.0

# Pin (bottom cylinder) dimensions
pin_diam = 12.0
pin_height = 10.0

# 1. Create the main rectangular body
# We start by drawing the side profile and extruding it
main_body = (
    cq.Workplane("XY")
    .box(length, width, height, centered=(False, True, True))
)

# 2. Create the Clevis (Fork) shape
# We need to cut out the gap and round the ends.
# Instead of cutting, it's often easier to build the distinct shape or cut a slot.
# Let's try cutting the slot first.

# Create the slot cutout
slot_cut = (
    cq.Workplane("XY")
    .workplane(offset=-length/2) # Start at the origin (left side)
    .transformed(offset=(0, 0, 0), rotate=(0, 90, 0)) # Rotate to look at the end face
    .rect(clevis_depth * 2, clevis_gap) # Deep enough to cut through
    .extrude(length) # Cut through entirely, we will intersect later or position carefully
)

# Actually, a better approach for the clevis end:
# 1. Round the end of the main block.
# 2. Cut the slot.
# 3. Drill the hole.

# Re-approach: Construct the profile from the top view (XZ plane in this orientation relative to camera, 
# but let's stick to standard XY for base). Let's define the long axis as X.

result = (
    cq.Workplane("XY")
    .box(length, width, height)
    # Align so left face is at x=0 for easier math
    .translate((length/2, 0, 0))
)

# Create the rounded clevis end
# We will add a cylinder at the end and then hull it or just overlap.
# Let's fillet the vertical edges at the x=0 end.
# Actually, the image shows a full semi-circle profile.
# A simple way is to extend the block and fillet, or construct a cylinder and fuse.

clevis_center_x = 0
clevis_cylinder = (
    cq.Workplane("XY")
    .cylinder(height=height, radius=width/2, direct=(0, 0, 1))
    .rotate((0,0,0), (1,0,0), 90) # Rotate to lie horizontal like the block
    .translate((0, 0, 0)) # Centered at origin
)

# Fuse the main body and the rounded end
# The main body needs to be shifted so it connects tangentially or overlaps
# The main block starts at X=0. The cylinder is at X=0. 
# We need to shift the main block slightly right or just rely on the overlap.
# Let's adjust the main block construction.

body = (
    cq.Workplane("XY")
    # Draw side profile on XZ plane
    .workplane(offset=width/2)
    .moveTo(0, height/2)
    .lineTo(length, height/2)
    .lineTo(length, -height/2)
    .lineTo(0, -height/2)
    .close()
    .extrude(-width) # Extrude along Y
)

# Add the rounded ear profile
ears = (
    cq.Workplane("XY")
    .workplane(offset=width/2)
    .moveTo(0, height/2)
    .threePointArc((-height/2, 0), (0, -height/2)) # Semi-circle
    .lineTo(0, height/2)
    .close()
    .extrude(-width)
)

result = body.union(ears)

# Cut the Clevis Slot
result = (
    result
    .faces("<X") # Select the rounded face
    .workplane()
    .rect(height*2, clevis_gap) # Make rectangle large enough to clear the arc
    .cutBlind(clevis_depth) # Cut into the body
)

# Drill the Pin Hole in the Clevis
result = (
    result
    .faces(">Y") # Select top face (width direction)
    .workplane()
    .moveTo(0, 0) # Center of the semi-circle
    .hole(clevis_hole_diam)
)

# Add the bottom Pin
# It is located at the far end of the arm (max X), on the bottom face (-Z)
result = (
    result
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    # We need to target near the end. 
    # The center of mass of the bottom face is roughly length/2.
    # Let's locate explicitly relative to the main length.
    .center(length/2 - width/2, 0) # Shift to near the end
    .circle(pin_diam/2)
    .extrude(pin_height)
)

# Refine fillets if necessary based on image interpretation
# The transition from the clevis ears to the body looks sharp in the render, 
# but there's a slight curve on the top/bottom edges of the arm.
# Let's add a small fillet to the long edges for realism.
result = result.edges("|X").fillet(0.5)

# Fillet the pin connection for strength/visual match
result = result.faces("<Z").edges(cq.selectors.RadiusNthSelector(0)).fillet(1.0)

# Optional: Fillet the vertical edge at the back
result = result.edges(">X and |Y").fillet(1.0)