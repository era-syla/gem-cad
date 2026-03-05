import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 160.0
width = 40.0
thickness = 5.0

# Structural dimensions
side_wall_thickness = 5.0      # Thickness of the long rails
end_wall_thickness = 10.0      # Thickness of the solid ends
center_block_width = 30.0      # Width of the solid central section

# Large cutout calculation
cutout_len = (length - center_block_width - (2 * end_wall_thickness)) / 2
cutout_wid = width - (2 * side_wall_thickness)
cutout_x_pos = (center_block_width / 2) + (cutout_len / 2)

# Feature dimensions
center_hole_diam = 6.0
small_hole_diam = 3.0
center_small_hole_spacing = 14.0  # Vertical distance between small central holes
notch_width = 4.0
notch_depth = 2.5

# Calculate end hole position (centered in the end wall)
end_hole_x_pos = (length / 2) - (end_wall_thickness / 2)

# --- Modeling ---
result = (
    cq.Workplane("XY")
    # 1. Create the base block
    .box(length, width, thickness)
    
    # 2. Cut the large rectangular windows
    .faces(">Z")
    .workplane()
    .pushPoints([(-cutout_x_pos, 0), (cutout_x_pos, 0)])
    .rect(cutout_len, cutout_wid)
    .cutThruAll()
    
    # 3. Cut the main central hole
    .faces(">Z")
    .workplane()
    .hole(center_hole_diam)
    
    # 4. Cut the two small holes flanking the center (vertical)
    .faces(">Z")
    .workplane()
    .pushPoints([(0, center_small_hole_spacing / 2), (0, -center_small_hole_spacing / 2)])
    .hole(small_hole_diam)
    
    # 5. Cut the holes at the far ends
    .faces(">Z")
    .workplane()
    .pushPoints([(-end_hole_x_pos, 0), (end_hole_x_pos, 0)])
    .hole(small_hole_diam)
    
    # 6. Cut the notches on top and bottom edges
    .faces(">Z")
    .workplane()
    .pushPoints([(0, width / 2), (0, -width / 2)])
    # We use a rectangle double the depth centered on the edge to ensure a clean cut inward
    .rect(notch_width, notch_depth * 2)
    .cutThruAll()
)