import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
total_height = 20.0
hex_height = 8.0     # Height of the hexagonal head part
cylinder_height = total_height - hex_height

# Head dimensions
hex_flat_to_flat = 20.0  # Width across flats
# Calculate flat-to-flat radius (apothem)
hex_r_inner = hex_flat_to_flat / 2.0
# Calculate point-to-point radius (circumradius)
hex_r_outer = hex_r_inner / 0.86602540378 

# The top of the hex is circular. The image shows the hex shape transitioning 
# into a circular top face, likely via a chamfer or a revolution cut. 
# A common way to model this fastener style is a hex extrusion intersected with a cone or chamfer.
chamfer_angle = 30.0 # Standard chamfer angle for bolt heads

# Cylinder (Shank) dimensions
shank_diameter = 12.0
shank_radius = shank_diameter / 2.0

# Through-hole dimensions
hole_diameter = 6.0
hole_radius = hole_diameter / 2.0
countersink_angle = 90.0 # Angle for the top chamfer of the hole
countersink_depth = 1.0

# Neck/Undercut dimensions (visual estimation from image)
# There is a small groove or relief where the head meets the shank
neck_height = 2.0
neck_radius = shank_radius * 0.85

# --- Modeling Process ---

# 1. Create the cylindrical shank (bottom part)
shank = cq.Workplane("XY").circle(shank_radius).extrude(cylinder_height)

# 2. Create the hexagonal head base
# We start at the top of the shank
head_base = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height)
    .polygon(nSides=6, diameter=hex_r_outer * 2) # polygon uses outer diameter (point-to-point)
    .extrude(hex_height)
)

# 3. Create the Chamfered Top on the Hex Head
# This is the signature look of a hex bolt. We effect this by creating a 
# revolving cut to shave off the corners.
# We need a profile that starts at the top edge of the inscribed circle and cuts downwards/outwards.
chamfer_cut_profile = (
    cq.Workplane("XZ")
    .workplane(offset=cylinder_height + hex_height) # Start at top of head
    .moveTo(hex_r_inner, 0) # Start at the flat-to-flat radius
    .lineTo(hex_r_outer * 1.5, 0) # Go out past the points
    .lineTo(hex_r_outer * 1.5, -hex_height) # Go down
    # Calculate the intersection point based on angle, or just visually approximate the "cut depth"
    # Looking at the image, the curve starts exactly at the tangent of the flat faces.
    .lineTo(hex_r_inner, -(hex_r_outer - hex_r_inner)) # Just a rough angle approximation
    .close()
)

# A cleaner way to get that specific "arced" look on the faces is a revolution cut 
# of a triangle.
# Define a cutting tool that spins around the Z axis to chamfer the hex corners.
head_chamfer_tool = (
    cq.Workplane("XZ", origin=(0, 0, cylinder_height + hex_height))
    .moveTo(hex_r_inner, 0)
    .lineTo(hex_r_outer + 5, 0) # Extend well beyond
    .lineTo(hex_r_outer + 5, -hex_height) # Go down
    .lineTo(hex_r_inner, - (hex_r_outer - hex_r_inner) * 1.5 ) # Slope back up to the start X
    .close()
    .revolve(360, (0,0,0), (0,0,1))
)

# Apply the cut to the head
head = head_base.cut(head_chamfer_tool)

# 4. Combine Shank and Head
part_body = shank.union(head)

# 5. Create the Undercut/Neck
# The image shows a smooth transition or a groove between shank and head.
# Let's create a small groove.
groove_profile = (
    cq.Workplane("XZ", origin=(0, 0, cylinder_height))
    .moveTo(shank_radius, 0)
    .lineTo(shank_radius, neck_height)
    .lineTo(shank_radius + 2, neck_height) # Go outwards into the head material
    .lineTo(shank_radius + 2, -1) # Go down into shank material slightly
    .close()
)
# Actually, looking closer, it looks like a fillet or a tapered neck. 
# Let's just fillet the junction if possible, or add a simple neck cylinder.
# The image shows a "waist".
neck_cut = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height - neck_height/2)
    .circle(shank_radius + 5) # Outer boundary
    .circle(neck_radius)      # Inner boundary (the waist size)
    .extrude(neck_height)
)
# Instead of a complex cut, let's just fillet the intersection line later 
# or assume the shank is the shank.
# Let's look at the image again: There is a distinct "ring" below the hex.
# Let's add a small fillet at the transition.
part_body = part_body.faces(cq.NearestToPointSelector((0,0,cylinder_height))).fillet(0.5)


# 6. Create the central hole
# Simple through hole
part_body = part_body.faces(">Z").hole(hole_diameter)

# 7. Add the chamfer/countersink to the hole
# We can do this by selecting the top circular edge of the hole.
part_body = part_body.edges(cq.NearestToPointSelector((0, 0, total_height))).chamfer(0.5)

result = part_body