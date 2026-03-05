import cadquery as cq

# ==========================================
# Parameters
# ==========================================
width = 25.0           # Width of the strip
thickness = 2.5        # Thickness of the material
leg_long_len = 150.0   # Length of the long vertical leg (from outer corner)
leg_short_len = 45.0   # Length of the short horizontal leg (from outer corner)
bend_radius = 4.0      # Outer bend radius
hole_diameter = 5.5    # Diameter of the mounting holes
hole_count = 7         # Number of holes on the long leg
hole_spacing = 18.0    # Center-to-center spacing of holes
slot_width = 6.5       # Width of the slot on the short leg
slot_length = 12.0     # Center-to-center length of the slot

# ==========================================
# 3D Modeling
# ==========================================

# 1. Create the base bent profile
# Sketch L-shape on YZ plane and extrude along X
# Origin (0,0,0) is at the outer corner of the bend
pts = [
    (0, leg_long_len),             # Top of long leg (outer)
    (0, 0),                        # Corner (outer)
    (leg_short_len, 0),            # End of short leg (outer)
    (leg_short_len, thickness),    # End of short leg (inner)
    (thickness, thickness),        # Corner (inner)
    (thickness, leg_long_len)      # Top of long leg (inner)
]

# Create the base extrusion, centered on X axis for symmetry
base = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(width, both=True)
)

# 2. Apply Fillets
# Fillet the bend corners
# Outer corner is at (0,0,0), Inner corner is at (thickness, thickness, 0) projected along X
# We select edges parallel to X nearest to these points
result = base.edges(cq.selectors.NearestToPointSelector((0, 0, 0))).fillet(bend_radius)
result = result.edges(cq.selectors.NearestToPointSelector((0, thickness, thickness))).fillet(max(0.1, bend_radius - thickness))

# Round the ends of the legs (Full round fillets)
# Long leg tip: Edges at Z = max, running along Y (thickness direction)
result = result.edges(">Z and |Y").fillet(width / 2.0 - 0.01)

# Short leg tip: Edges at Y = max, running along Z (thickness direction)
result = result.edges(">Y and |Z").fillet(width / 2.0 - 0.01)

# 3. Cut Holes in Long Leg
# Calculate hole positions
# Start from the top (rounded end), centered relative to the width
# First hole is concentric with the rounded tip (distance W/2 from top edge)
start_z = leg_long_len - (width / 2.0)
hole_points = [(0, start_z - i * hole_spacing) for i in range(hole_count)]

result = (
    result.faces("<Y")  # Select the outer vertical face (at Y=0)
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints(hole_points)
    .circle(hole_diameter / 2.0)
    .cutThruAll()
)

# 4. Cut Slot in Short Leg
# Position slot concentric with the rounded end of the short leg
slot_center_y = leg_short_len - (width / 2.0)

result = (
    result.faces("<Z")  # Select the bottom face (at Z=0)
    .workplane(centerOption="ProjectedOrigin")
    .pushPoints([(0, slot_center_y)])
    .slot2D(slot_length, slot_width, angle=90) # Angle 90 aligns slot with Y axis
    .cutThruAll()
)

# Final Result
if 'show_object' in globals():
    show_object(result)