import cadquery as cq

# --- Parameters ---
length = 300.0           # Center-to-center distance
beam_width = 35.0        # Width of the central connecting bar
head_diameter = 60.0     # Diameter of the rounded ends
head_radius = head_diameter / 2.0
thickness = 5.0          # Plate thickness
fillet_radius = 30.0     # Radius for the transition from beam to head

# Hole Dimensions
center_hole_dia = 12.0
mount_hole_dia = 4.2     # M4 clearance
bolt_circle_dia = 36.0   # Diameter of the mounting hole pattern
bolt_circle_radius = bolt_circle_dia / 2.0
detail_hole_dia = 3.0    # Small holes on the beam

# --- Modeling ---

# 1. Base Geometry
# Create the central rectangular beam
beam = cq.Workplane("XY").rect(length, beam_width).extrude(thickness)

# Create the two circular heads at the ends
head_left = (
    cq.Workplane("XY")
    .center(-length / 2, 0)
    .circle(head_radius)
    .extrude(thickness)
)

head_right = (
    cq.Workplane("XY")
    .center(length / 2, 0)
    .circle(head_radius)
    .extrude(thickness)
)

# Union the shapes into a single solid
result = beam.union(head_left).union(head_right)

# 2. Fillets
# Smooth the transition between the beam and the heads.
# We select vertical edges (|Z) that are "internal" (x coordinate < length/2).
result = result.edges("|Z").filter(
    lambda e: abs(e.Center().x) < length / 2 and abs(e.Center().y) < head_radius
).fillet(fillet_radius)

# 3. Hole Patterns
# We chain operations on the top face
result = (
    result.faces(">Z").workplane()
    
    # -- Left End --
    .center(-length / 2, 0)           # Move origin to left end
    .hole(center_hole_dia)            # Cut center hole
    .polarArray(bolt_circle_radius, 0, 360, 4) # Create 4-bolt pattern
    .hole(mount_hole_dia)             # Cut mounting holes
    
    # -- Right End --
    .center(length, 0)                # Move origin relative to previous (move to right end)
    .hole(center_hole_dia)            # Cut center hole
    .polarArray(bolt_circle_radius, 0, 360, 4)
    .hole(mount_hole_dia)             # Cut mounting holes
)

# 4. Detail Holes
# Add the small holes on the beam near the shoulders
detail_x_offset = length / 2 - head_radius - 15.0
detail_y_offset = beam_width / 2 - 6.0

result = (
    result.faces(">Z").workplane()
    .pushPoints([
        (detail_x_offset, detail_y_offset),
        (detail_x_offset, -detail_y_offset),
        (-detail_x_offset, detail_y_offset),
        (-detail_x_offset, -detail_y_offset)
    ])
    .hole(detail_hole_dia)
)