import cadquery as cq

# Parametric dimensions
height = 30.0           # Total height of the object
outer_diam_main = 40.0  # Outer diameter of the central cylinder section
wall_thickness = 4.0    # Thickness of the wall
flare_diam = 60.0       # Outer diameter of the top and bottom flares
flare_height = 8.0      # Height of the flared sections
internal_feature_height = 5.0 # Height of internal rings/features
internal_chamfer = 2.0  # Size of internal chamfers

# Calculated dimensions
radius_main = outer_diam_main / 2.0
radius_flare = flare_diam / 2.0
radius_inner = radius_main - wall_thickness

# Create the main profile for revolution
# We will draw half the cross-section and revolve it.
# The profile is essentially a "C" shape or an "I" beam shape rotated.

# Let's define points for a cross-section on the XZ plane (Z is up)
# We'll start from the bottom inner corner and go counter-clockwise

# Coordinate helpers
z_bottom = 0
z_flare_bottom_end = flare_height
z_flare_top_start = height - flare_height
z_top = height

# Draw the cross section
# We'll create the outer shell first
pts = [
    (radius_flare, z_bottom),                    # Bottom outer rim
    (radius_main, z_flare_bottom_end),           # Bottom flare transition
    (radius_main, z_flare_top_start),            # Top flare transition
    (radius_flare, z_top),                       # Top outer rim
    (radius_inner, z_top),                       # Top inner rim
    (radius_inner, z_bottom),                    # Bottom inner rim
]

# Create the base revolution
result = (
    cq.Workplane("XZ")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0)) # Revolve around Z axis
)

# Refine the shape based on the image visual details
# The image shows curved transitions (fillets) on the outside
# and stepped or grooved features on the inside.

# 1. External Fillets (the flares look curved, not straight conical chamfers)
# We select the edges at the waist (where the flare meets the cylinder)
# and the outer rim edges aren't sharp, but the transition is the key.
# Actually, looking closer, the profile might be better modeled with a spline or large fillets.
# Let's apply fillets to the "waist" edges.
result = result.edges(cq.selectors.RadiusNthSelector(1)).fillet(flare_height * 0.8)


# 2. Internal Features
# The image shows the inside isn't smooth. It has steps or grooves.
# There looks to be a central thicker band or recessed rings.
# Let's cut a central groove or add internal rings. 
# It looks like the top and bottom internal diameters are larger, narrowing in the middle.

# Let's cut a subtle counterbore/chamfer at the top and bottom internal edges
result = result.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(internal_chamfer)
result = result.faces("<Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(internal_chamfer)

# There appears to be a central internal ring or ridge.
# Let's add a small internal protrusion (ring) in the middle.
# Alternatively, it could be machined out. Let's model it as a slight thickening in the center.

# We create a cylinder in the center and intersect it or union it?
# Actually, looking at the shadows, there are two distinct internal grooves.
# Let's cut two internal grooves.

groove_width = 3.0
groove_depth = 1.0
groove_z_pos1 = height / 2.0 - 4.0
groove_z_pos2 = height / 2.0 + 4.0

# Create a tool to cut the grooves
groove_cutter = (
    cq.Workplane("XY")
    .circle(radius_inner + groove_depth) # Make it bigger than hole to cut into wall
    .extrude(height) # Initial large cylinder
    .faces(">Z").workplane()
    .hole(radius_inner * 2) # Make it a tube
)

# Actually, easier way to make internal grooves is simply revolving a rectangle removal
groove_profile = (
    cq.Workplane("XZ")
    .rect(radius_inner * 0.1, groove_width) # Small rectangle
    .translate((radius_inner, height/2.0 - groove_width, 0)) # Move to wall
)
# Cut Groove 1
result = result.cut(
    cq.Workplane("XZ")
    .moveTo(radius_inner, height/2.0 - 3.0)
    .rect(groove_depth * 2, 2.0, centered=False) # Cutting rectangle sticking into the wall
    .revolve(360, (0,0,0), (0,1,0))
)

# Cut Groove 2
result = result.cut(
    cq.Workplane("XZ")
    .moveTo(radius_inner, height/2.0 + 1.0)
    .rect(groove_depth * 2, 2.0, centered=False)
    .revolve(360, (0,0,0), (0,1,0))
)

# Final smoothing/filleting to match the rendering style
# The top and bottom faces look flat, but the edges are soft.
try:
    # Outer rims
    result = result.edges(cq.selectors.RadiusNthSelector(2)).fillet(0.5)
except:
    pass 

# Ensure result is valid
if not result.val().isValid():
    raise ValueError("Generated geometry is invalid")