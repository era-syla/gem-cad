import cadquery as cq
import math

# Parameter definitions
length = 50.0       # Length of the clip
outer_radius = 15.0 # Outer radius of the cylinder
thickness = 3.0     # Wall thickness
opening_angle = 60.0 # Angle of the cutout opening in degrees

# Derived parameters
inner_radius = outer_radius - thickness
height = outer_radius * 2

# Create the base profile: two concentric circles with a cutout
# We sketch on the YZ plane to extrude along X
result = (
    cq.Workplane("YZ")
    .sketch()
    # Draw the outer circle
    .circle(outer_radius)
    # Draw the inner circle to form the ring
    .circle(inner_radius, mode="s")
    # Cut out a sector to create the 'C' shape
    # We create a large rectangle and position it based on trigonometry or use a polygon
    # A cleaner way in sketch API is to use arc logic, but boolean subtraction of a wedge is robust.
    # Let's finish the sketch first as a full ring, then cut.
    # Actually, constructing the C-shape directly in the sketch is cleaner.
    .reset() # Start over for a cleaner arc-based approach
    .arc((inner_radius, 0), (0, inner_radius), (-inner_radius, 0)) # Inner arc top half
    .arc((-inner_radius, 0), (0, -inner_radius), (inner_radius, 0)) # Inner arc bottom half
    .assemble(tag="inner_circle") # This is just a circle, but let's do arcs to be explicit or just circle
    
    # Let's try a different approach: Tube then cutout. It's often simpler to read.
)

# Approach 2: Solid modeling (Constructive Solid Geometry)
# 1. Create a tube.
# 2. Cut a slot out of it.

# Create the main tube
tube = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)

# Calculate dimensions for the cutting box
# The box needs to be wide enough to cut the opening defined by the angle
# Width calculation: 2 * outer_radius * sin(opening_angle/2) roughly covers chord
# But a simple large box positioned correctly works best.
# We want the opening at the top (positive Y direction relative to the circle profile)
cutout_width = 2 * outer_radius * math.sin(math.radians(opening_angle / 2))
# To ensure clean cut through thickness, we cut from the center outwards
# A wedge shape is most accurate for an angular opening.

# Create a wedge shape to subtract
# The wedge will be extruded along the length of the tube
wedge_profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius * 1.5 * math.cos(math.radians(90 + opening_angle/2)), 
            outer_radius * 1.5 * math.sin(math.radians(90 + opening_angle/2)))
    .lineTo(outer_radius * 1.5 * math.cos(math.radians(90 - opening_angle/2)), 
            outer_radius * 1.5 * math.sin(math.radians(90 - opening_angle/2)))
    .close()
    .extrude(length)
)

# Subtract the wedge from the tube
result = tube.cut(wedge_profile)

# To match the specific orientation in the image (laying on its side):
# The current model is extruded along Z (default). The image shows it extruded along an axis roughly X or Y.
# Let's rotate it to match the visual better, though strictly not required for geometry validity.
# The image shows the opening facing "up/left".
result = result.rotate((0,0,0), (1,0,0), 90).rotate((0,0,0), (0,1,0), -90)