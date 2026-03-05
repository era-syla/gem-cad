import cadquery as cq
import math

# --- Parameters ---
# Hex Base dimensions
hex_flat_width = 6.0    # Width across flats (wrench size)
hex_height = 4.5        # Height of the hex base

# Vertical Post dimensions
post_diameter = 1.8     # Diameter of the thin vertical shaft
post_length = 35.0      # Length of the shaft

# Top Cap dimensions
cap_diameter = 3.2      # Diameter of the top fitting
cap_height = 7.0        # Height of the top fitting
cap_dome_radius = 1.5   # Radius for filleting the top (must be < cap_diameter/2)

# Horizontal Antenna Wire dimensions
wire_diameter = 0.8     # Thickness of the horizontal wire
wire_length = 160.0     # Total length of the wire

# --- Geometry Generation ---

# 1. Create the Hexagonal Base
# Calculate circumdiameter based on flat-to-flat width
circum_diameter = hex_flat_width / math.cos(math.radians(30))

base = (
    cq.Workplane("XY")
    .polygon(6, circum_diameter)
    .extrude(hex_height)
)

# 2. Create the Vertical Post
# Extrude from the top face of the base
post = (
    base.faces(">Z")
    .workplane()
    .circle(post_diameter / 2.0)
    .extrude(post_length)
)

# 3. Create the Top Cap
# Extrude from the top face of the post
cap = (
    post.faces(">Z")
    .workplane()
    .circle(cap_diameter / 2.0)
    .extrude(cap_height)
)

# 4. Round the top of the Cap
# Apply a fillet to the top edge to create a domed appearance
structure = cap.faces(">Z").edges().fillet(cap_dome_radius)

# 5. Create the Horizontal Wire
# Calculate Z position to place wire within the cap (approx 70% up the cap)
wire_z = hex_height + post_length + (cap_height * 0.7)

wire = (
    cq.Workplane("YZ")
    .center(0, wire_z)
    .circle(wire_diameter / 2.0)
    .extrude(wire_length / 2.0, both=True)  # Extrude symmetrically
)

# 6. Combine into final result
result = structure.union(wire)