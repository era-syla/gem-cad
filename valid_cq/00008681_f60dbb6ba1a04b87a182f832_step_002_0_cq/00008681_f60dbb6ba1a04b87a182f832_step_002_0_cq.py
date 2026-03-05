import cadquery as cq

# --- Parametric Dimensions ---
# These can be adjusted to change the size of the part
total_height = 30.0       # Total length of the fastener
head_diameter = 20.0      # Outer diameter of the flange/head
head_thickness = 4.0      # Thickness of the flange/head
body_diameter = 12.0      # Diameter of the cylindrical shaft
hole_diameter = 6.0       # Diameter of the through-hole
chamfer_size = 0.5        # Size of the chamfer on the hole entrance

# --- Modeling ---

# 1. Create the main cylindrical shaft (the body)
# We start by drawing a circle on the XY plane and extruding it
shaft = (
    cq.Workplane("XY")
    .circle(body_diameter / 2.0)
    .extrude(total_height)
)

# 2. Create the head (flange) on top of the shaft
# We select the top face of the shaft and draw a larger circle
# Note: Since the shaft was extruded upwards, the top face is at Z = total_height
# We want the head to be part of the total height, but usually in CAD, a head sits on top.
# Looking at the image, the head has thickness. Let's assume total_height includes the head.
# Alternatively, we can build it from bottom up. Let's restart the strategy for clarity.

# Revised Strategy:
# 1. Sketch the profile to revolve? Or stack cylinders.
# Stacking cylinders is simpler and very robust in CadQuery.

# Let's define the shaft length based on head thickness
shaft_length = total_height - head_thickness

# Create the shaft
part = (
    cq.Workplane("XY")
    .circle(body_diameter / 2.0)
    .extrude(shaft_length)
)

# Create the head on top of the shaft
# Select the top face of the current shaft
part = (
    part.faces(">Z")
    .workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_thickness)
)

# 3. Create the through-hole
# Select the top face of the new head and cut a hole all the way through
part = (
    part.faces(">Z")
    .workplane()
    .hole(hole_diameter)
)

# 4. Add the chamfer
# The image shows a chamfer around the top edge of the hole.
# We select the edge at the top of the hole.
# The selector logic: Find the top face (>Z), get its inner wire or select edges near the hole radius.
# A robust way is to select the edge that is at the top Z height and has the hole radius.
part = (
    part.edges(cq.selectors.RadiusNthSelector(0)) # Selects the smallest radius edges (the hole)
    .edges(">Z")                                  # Filters for the one at the top
    .chamfer(chamfer_size)
)

# Assign to result variable as requested
result = part