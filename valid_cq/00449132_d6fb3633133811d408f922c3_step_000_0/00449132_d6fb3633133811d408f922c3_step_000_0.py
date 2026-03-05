import cadquery as cq

# -- Parametric Dimensions --
strip_width = 12.7      # Width of the metal strip (approx 0.5 inch)
strip_thickness = 1.0   # Thickness of the strip
hole_diameter = 4.2     # Diameter of the holes (clearance for M4)
pitch = 12.7            # Distance between hole centers (standard 0.5 inch)
vertical_gap = 20.0     # Spacing between strips in the layout

def create_strip(num_holes):
    """
    Creates a single perforated mechanical strip.
    
    Args:
        num_holes (int): Total number of holes in the strip.
        
    Returns:
        cq.Workplane: The 3D object of the strip.
    """
    # Calculate the length between the centers of the two end holes (and arcs)
    length_cc = (num_holes - 1) * pitch
    
    # Create the base 'lozenge' or slot shape
    # slot2D creates a profile defined by center-to-center length and diameter (width)
    base = (
        cq.Workplane("XY")
        .slot2D(length_cc, strip_width)
        .extrude(strip_thickness)
    )
    
    # Calculate hole positions relative to the center (0,0)
    # The slot is centered at the origin, extending length_cc/2 in both -x and +x directions
    start_x = -length_cc / 2.0
    hole_positions = [(start_x + i * pitch, 0) for i in range(num_holes)]
    
    # Cut the holes through the strip
    final_strip = (
        base.faces(">Z")
        .workplane()
        .pushPoints(hole_positions)
        .circle(hole_diameter / 2.0)
        .cutThruAll()
    )
    
    return final_strip

# -- Scene Construction --

parts = []

# Define the configuration of strips based on the image
# Group 1 (Left): Increasing by 2 (3, 5, 7, 9, 11)
left_counts = [3, 5, 7, 9, 11]
# Group 2 (Right): Mixed increments (3, 4, 5, 6, 7, 9)
right_counts = [3, 4, 5, 6, 7, 9]
# Group 3 (Bottom): Single long strip
long_strip_count = 25

# Generate and position Left Group
current_y = 100
x_pos_left = -80

for count in left_counts:
    part = create_strip(count)
    part = part.translate((x_pos_left, current_y, 0))
    parts.append(part)
    current_y -= vertical_gap

# Generate and position Right Group
current_y = 100 # Reset Y height
x_pos_right = 80

for count in right_counts:
    part = create_strip(count)
    part = part.translate((x_pos_right, current_y, 0))
    parts.append(part)
    current_y -= vertical_gap

# Generate and position Bottom Long Strip
# Place it below the lowest point of the previous groups
min_y = current_y - vertical_gap
part_long = create_strip(long_strip_count)
# Center it horizontally between the groups roughly
part_long = part_long.translate((0, min_y, 0))
parts.append(part_long)

# Combine all parts into a single result object
result = parts[0]
for p in parts[1:]:
    result = result.union(p)