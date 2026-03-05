import cadquery as cq

# --- Parameter Definitions ---
height = 100.0       # Total height of the bracket
width = 25.0         # Width of the flanges (leg length)
thickness = 4.0      # Thickness of the material
hole_diameter = 8.0  # Diameter of the mounting hole

# --- Derived Parameters ---
# The top is a full round fillet, so radius is half the width
top_radius = width / 2.0
# Height of the straight vertical section before the arc starts
straight_run = height - top_radius

# --- Geometry Construction ---

# 1. Create Leg 1 (Aligned along the Y-axis)
# We sketch the profile on the YZ plane and extrude along X.
# The profile starts at the origin (0,0) which will be the corner of the L.
leg1 = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(width, 0)                  # Bottom width
    .lineTo(width, straight_run)       # Vertical side up to arc start
    .threePointArc(
        (width / 2.0, height),         # Arc peak point
        (0, straight_run)              # Arc end point
    )
    .lineTo(0, 0)                      # Return to origin
    .close()
    .extrude(thickness)                # Extrude to create the plate thickness
)

# 2. Create Leg 2 (Aligned along the X-axis)
# We sketch the profile on the XZ plane and extrude along Y.
# Note: CadQuery's XZ plane normal is -Y. To extrude into the +Y space 
# (to overlap with leg1 at the corner), we extrude by negative thickness.
leg2 = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(width, 0)                  # Bottom width
    .lineTo(width, straight_run)       # Vertical side up to arc start
    .threePointArc(
        (width / 2.0, height),         # Arc peak point
        (0, straight_run)              # Arc end point
    )
    .lineTo(0, 0)                      # Return to origin
    .close()
    .extrude(-thickness)               # Extrude in +Y direction
)

# 3. Add the Hole to Leg 2
# We select the face at the extreme +Y coordinate (the front face of the flange).
# We use ProjectedOrigin to maintain global coordinate references easily.
leg2 = (
    leg2
    .faces(">Y")
    .workplane(centerOption="ProjectedOrigin")
    .moveTo(width / 2.0, height - top_radius)  # Center the hole in the rounded top
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 4. Union the two legs to form the final L-bracket
result = leg1.union(leg2)