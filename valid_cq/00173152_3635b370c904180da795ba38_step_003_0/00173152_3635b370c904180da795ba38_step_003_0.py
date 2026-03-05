import cadquery as cq

# --- Parameters ---
blade_length = 45.0      # Distance from center to tip
blade_width = 16.0       # Width of the blade
blade_thickness = 3.0    # Thickness of the blade plate
tip_chamfer = 5.0        # Size of the chamfer at the blade tip
offset_dist = 3.5        # Offset from center to create the "swirl" overlap
hub_diameter = 14.0      # Outer diameter of the top central ring
hub_height = 0.5         # Height of the ring above the blades
shaft_diameter = 10.0    # Diameter of the bottom cylinder
shaft_length = 20.0      # Length of the bottom cylinder
hole_diameter = 5.0      # Central bore diameter

# --- Geometry Construction ---

# 1. Define the 2D profile of a single blade
# We start the sketch behind the center (negative X) to ensure the roots overlap at the hub
# The shape is a rectangle with chamfered corners at the far end
root_extension = 15.0  # Extend backwards past center
L = blade_length
W = blade_width
C = tip_chamfer

# Points for the blade profile (counter-clockwise)
blade_pts = [
    (-root_extension, -W/2.0),
    (L - C, -W/2.0),
    (L, -W/2.0 + C),
    (L, W/2.0 - C),
    (L - C, W/2.0),
    (-root_extension, W/2.0)
]

# Create the solid blade
# Translate in Y to create the tangential/swirl offset
blade = (
    cq.Workplane("XY")
    .polyline(blade_pts)
    .close()
    .extrude(blade_thickness)
    .translate((0, offset_dist, 0))
)

# 2. Create the pattern of 4 blades
# Rotate and union the base blade
impeller = blade
for i in range(1, 4):
    impeller = impeller.union(blade.rotate((0, 0, 0), (0, 0, 1), i * 90))

# 3. Create the central components
# Top Hub Ring (Washer shape on top)
top_hub = (
    cq.Workplane("XY")
    .workplane(offset=blade_thickness)
    .circle(hub_diameter / 2.0)
    .extrude(hub_height)
)

# Bottom Shaft
bottom_shaft = (
    cq.Workplane("XY")
    .circle(shaft_diameter / 2.0)
    .extrude(-shaft_length)
)

# 4. Combine all parts and cut the central hole
result = (
    impeller
    .union(top_hub)
    .union(bottom_shaft)
    .faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)