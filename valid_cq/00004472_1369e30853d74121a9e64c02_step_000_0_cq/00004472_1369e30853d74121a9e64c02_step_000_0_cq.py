import cadquery as cq

# --- Parameter Definitions ---
# Overall plate dimensions
plate_width = 100.0   # Total width from tip to tip
plate_height_center = 35.0 # Approximate height at the deepest part
plate_thickness = 5.0 # Thickness of the main flat profile

# Side tip dimensions
tip_height = 12.0     # Height of the vertical edge at the ends

# Central Hub/Boss dimensions
hub_diameter = 20.0
hub_height = 8.0      # Height protruding from the back face

# Hole dimensions
hole_diameter = 4.0
hole_spacing = 14.0   # Distance between the two small holes
hole_height_from_top = 22.0 # Distance from the top edge to the hole centers

# --- Geometry Construction ---

# 1. Create the main profile shape
# We will draw this on the XY plane.
# The shape is symmetric roughly, but let's define it by coordinates.
# Top edge is straight. Bottom is a curve.
# Let's assume the origin is at the center of the top edge.

x_limit = plate_width / 2.0
y_top = 0.0
y_tip_bottom = -tip_height
y_bottom_center = -plate_height_center

# Create the sketch for the plate
# Using a 3-point arc for the bottom curve is a reasonable approximation.
# Point 1: (-x_limit, -tip_height)
# Point 2: (0, -plate_height_center)
# Point 3: (x_limit, -tip_height)

plate_profile = (
    cq.Workplane("XY")
    .moveTo(-x_limit, y_top)
    .lineTo(x_limit, y_top)           # Top straight edge
    .lineTo(x_limit, y_tip_bottom)    # Right vertical edge
    .threePointArc((0, y_bottom_center), (-x_limit, y_tip_bottom)) # Bottom curve
    .close()
)

# Extrude the plate
plate = plate_profile.extrude(plate_thickness)

# 2. Create the central hub on the back
# We extrude a circle from the back face (-plate_thickness) downwards (negative Z relative to front)
# Or simply extrude from the "bottom" face in CadQuery terms if we consider XY as front.
# Let's orient it so the plate is front.
# The image shows a boss protruding from the back side.

hub = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at z=0 (back face, assuming extrude was positive Z)
    # Actually, let's look at the extrude direction. 
    # If we extrude(plate_thickness), the solid is between Z=0 and Z=5.
    # The image shows the boss on the "back" relative to the view.
    # Let's put the boss on the negative Z side.
    .center(0, y_bottom_center * 0.4) # Position hub somewhat centrally vertically, biased down
    # Adjust hub position based on image: looks concentric with the curve bottom roughly
    # Let's refine hub position: somewhat below the holes.
    .moveTo(0, -plate_height_center + hub_diameter/2 + 2) 
    .circle(hub_diameter / 2)
    .extrude(-hub_height) # Extrude backwards
)

# Let's refine the hub position to better match the "rocker" look. 
# It often pivots near the bottom center.
hub_center_y = -plate_height_center + 10.0 # Tuning this visually

# Re-create hub with better positioning logic
hub = (
    cq.Workplane("XY")
    .workplane(offset=0) # Back face (Z=0)
    .moveTo(0, hub_center_y)
    .circle(hub_diameter / 2)
    .extrude(-hub_height)
)

# Union the plate and the hub
base_solid = plate.union(hub)

# 3. Create the two holes
# The image shows two small holes near the bottom center.
# They go through the plate.

hole_y = -plate_height_center + 12.0 # Similar height to hub center, maybe slightly different
hole_x_offset = hole_spacing / 2.0

result = (
    base_solid
    .faces(">Z") # Select front face
    .workplane()
    .pushPoints([(-hole_x_offset, hole_y), (hole_x_offset, hole_y)])
    .hole(hole_diameter)
)

# Optional: Add fillets to smooth edges if desired, though the image looks fairly sharp on the profile
# The image shows a slight radius on the hub transition, but it's subtle. We'll leave it sharp for robustness.