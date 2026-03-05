import cadquery as cq
import math

# --- Parameters ---
plate_diameter = 90.0
plate_thickness = 15.0

lug_diameter = 26.0
lug_radial_dist = 50.0  # Distance from center to lug center
lug_hole_diameter = 12.0

face_hole_diameter = 7.0
face_hole_spacing = 14.0 # Distance between holes in a pair
face_hole_offset = 22.0  # Distance from center to the midpoint of the pair

fillet_radius = 4.0

# --- Derived Values ---
# Lugs are arranged at 45 degree angles (corners of a square)
lug_axis_offset = lug_radial_dist * math.cos(math.radians(45))

lug_locations = [
    (lug_axis_offset, lug_axis_offset),
    (-lug_axis_offset, lug_axis_offset),
    (-lug_axis_offset, -lug_axis_offset),
    (lug_axis_offset, -lug_axis_offset)
]

# Face holes are located on the diagonal (quadrants 1 and 3)
diag_unit_vector = math.sqrt(2) / 2
d_inner = face_hole_offset - (face_hole_spacing / 2)
d_outer = face_hole_offset + (face_hole_spacing / 2)

face_hole_locations = [
    # Top-Right Pair
    (d_inner * diag_unit_vector, d_inner * diag_unit_vector),
    (d_outer * diag_unit_vector, d_outer * diag_unit_vector),
    # Bottom-Left Pair
    (-d_inner * diag_unit_vector, -d_inner * diag_unit_vector),
    (-d_outer * diag_unit_vector, -d_outer * diag_unit_vector)
]

# --- Modeling ---

# 1. Base Geometry: Main Disc
main_disc = cq.Workplane("XY").circle(plate_diameter / 2).extrude(plate_thickness)

# 2. Base Geometry: Lugs
lugs = (
    cq.Workplane("XY")
    .pushPoints(lug_locations)
    .circle(lug_diameter / 2)
    .extrude(plate_thickness)
)

# 3. Combine to create the solid body
result = main_disc.union(lugs)

# 4. Apply Fillet to the top outer perimeter
# We select the top face and then its edges. 
# Since holes haven't been cut yet, this selects the outer boundary.
result = result.faces(">Z").edges().fillet(fillet_radius)

# 5. Cut Lug Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(lug_locations)
    .hole(lug_hole_diameter)
)

# 6. Cut Face Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(face_hole_locations)
    .hole(face_hole_diameter)
)