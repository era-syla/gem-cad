import cadquery as cq

# Parameters for the plate dimensions
length = 160.0
width = 40.0
thickness = 4.0

# Parameters for the center pattern
center_hole_dia = 12.0
center_bolt_circle_dia = 26.0
center_bolt_count = 8
center_bolt_hole_dia = 3.5

# Parameters for the end patterns
end_pattern_offset = 60.0  # Distance from center to the center of the end pattern
end_square_side = 22.0     # Side length of the square pattern at ends
end_mount_hole_dia = 4.5   # Diameter of the 4 corner holes
end_pin_spacing = 12.0     # Distance between the two inner pin holes
end_pin_hole_dia = 3.0     # Diameter of the inner pin holes

# Create the base plate
result = cq.Workplane("XY").box(length, width, thickness)

# 1. Create the large center hole
result = result.faces(">Z").workplane().hole(center_hole_dia)

# 2. Create the circular pattern of small holes in the center
result = (result.faces(">Z").workplane()
          .polarArray(center_bolt_circle_dia/2, 0, 360, center_bolt_count)
          .hole(center_bolt_hole_dia))

# 3. Create the end patterns (Symmetric on both ends)
# We define offsets for one side and mirror/apply to both
for direction in [1, -1]:
    center_x = direction * end_pattern_offset
    
    # Create the 4 corner mounting holes (Square pattern)
    # Using pushPoints to locate the square relative to the specific end center
    result = (result.faces(">Z").workplane()
              .pushPoints([(center_x, 0)])
              .rect(end_square_side, end_square_side, forConstruction=True)
              .vertices()
              .hole(end_mount_hole_dia))
    
    # Create the 2 inner alignment/pin holes (Aligned along X-axis)
    # These are at offsets relative to the end center
    pin_locs = [
        (center_x - end_pin_spacing/2, 0),
        (center_x + end_pin_spacing/2, 0)
    ]
    result = (result.faces(">Z").workplane()
              .pushPoints(pin_locs)
              .hole(end_pin_hole_dia))

# The variable 'result' now contains the final model