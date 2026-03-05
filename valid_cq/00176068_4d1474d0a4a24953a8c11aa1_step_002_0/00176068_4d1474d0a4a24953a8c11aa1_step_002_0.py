import cadquery as cq
import math

# ------------------------------------------------------------------------------
# Parametric Dimensions
# ------------------------------------------------------------------------------
outer_diameter = 200.0       # Circumscribed diameter of the outer hexagon
ring_width = 35.0            # Width of the solid band
thickness = 8.0              # Thickness of the plate
corner_fillet = 12.0         # Fillet radius for corners
hole_dia_large = 10.0        # Diameter of holes at the vertices
hole_dia_small = 5.0         # Diameter of holes at the flats

# ------------------------------------------------------------------------------
# Calculations
# ------------------------------------------------------------------------------
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - ring_width
inner_diameter = inner_radius * 2.0

# Calculate radial distance for large holes (at vertices)
# Centered on the ring width at the corners
r_large = (outer_radius + inner_radius) / 2.0

# Calculate radial distance for small holes (at flats)
# Centered on the ring width at the flats (apothem)
# Apothem = Radius * cos(30 deg)
apo_outer = outer_radius * math.cos(math.radians(30))
apo_inner = inner_radius * math.cos(math.radians(30))
r_small = (apo_outer + apo_inner) / 2.0

# Generate coordinates for large holes (angles: 0, 60, 120...)
large_hole_pts = []
for i in range(6):
    angle = math.radians(i * 60)
    x = r_large * math.cos(angle)
    y = r_large * math.sin(angle)
    large_hole_pts.append((x, y))

# Generate coordinates for small holes (angles: 30, 90, 150...)
small_hole_pts = []
for i in range(6):
    angle = math.radians(i * 60 + 30)
    x = r_small * math.cos(angle)
    y = r_small * math.sin(angle)
    small_hole_pts.append((x, y))

# ------------------------------------------------------------------------------
# Solid Modeling
# ------------------------------------------------------------------------------

# 1. Create base hexagonal ring
result = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=outer_diameter)
    .polygon(nSides=6, diameter=inner_diameter)
    .extrude(thickness)
)

# 2. Apply fillets to all vertical corners (inner and outer)
result = result.edges("|Z").fillet(corner_fillet)

# 3. Cut the holes
result = (
    result.faces(">Z").workplane()
    .pushPoints(large_hole_pts)
    .hole(hole_dia_large)
    .pushPoints(small_hole_pts)
    .hole(hole_dia_small)
)