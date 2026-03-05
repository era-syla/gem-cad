import cadquery as cq

# --- Parameters ---
# Base dimensions
base_diameter = 100.0
base_thickness = 5.0

# Vertical Plate dimensions
plate_width = 70.0  # Width of the rectangular plate
plate_height = 60.0
plate_thickness = 8.0
plate_offset = 35.0 # Distance from center to inner face of the plate

# Hole parameters
large_hole_diameter = 12.0
small_hole_diameter = 8.0

# --- Modeling ---

# 1. Create the circular base
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_thickness)

# 2. Create one vertical plate
# We'll create it centered first, then move it into position
plate_sketch = (
    cq.Workplane("XZ")
    .box(plate_width, plate_height, plate_thickness, centered=(True, False, True))
)

# 3. Add holes to the plate
# Based on the image, there's a triangular pattern: two small holes up top, one large hole below.
# Coordinates relative to the center of the plate face
hole_vertical_spacing = 15.0 # Vertical distance from center of plate
hole_horizontal_spacing = 20.0 # Horizontal distance for top holes

plate_with_holes = (
    plate_sketch
    # Top two small holes
    .faces(">Y").workplane()
    .pushPoints([(-hole_horizontal_spacing, plate_height - 15), 
                 (hole_horizontal_spacing, plate_height - 15)])
    .hole(small_hole_diameter)
    # Bottom large hole
    .faces(">Y").workplane()
    .pushPoints([(0, 15)]) # Near the bottom
    .hole(large_hole_diameter)
)

# 4. Position and combine the plates
# Move the plate to the "left"
left_plate = plate_with_holes.translate((0, -plate_offset - plate_thickness/2, base_thickness))

# Move the plate to the "right" (or mirror it)
# We need to mirror it across the XZ plane to maintain symmetry
right_plate = left_plate.mirror("XZ")

# 5. Combine everything
result = base.union(left_plate).union(right_plate)

# Export or display the result (standard practice for CadQuery scripts)
if 'show_object' in globals():
    show_object(result)