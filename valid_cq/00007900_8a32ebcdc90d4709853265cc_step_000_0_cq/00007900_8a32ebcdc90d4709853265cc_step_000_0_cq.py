import cadquery as cq

# --- Parameter Definitions ---
# Main Enclosure Dimensions
box_length = 50.0
box_width = 50.0
box_total_height = 12.0
wall_thickness = 2.0
base_thickness = 2.0

# Inner Corner Posts
post_size = 4.0  # Size of the square post
post_offset = 1.0 # Offset from the inner wall corner (often flush, but let's make it distinct)

# Cylinder (Cap/Button) Dimensions
cyl_flange_diameter = 25.0
cyl_flange_thickness = 2.0
cyl_body_diameter = 18.0
cyl_body_height = 10.0
cyl_offset_x = 15.0 # Distance to move the cylinder away from the box
cyl_offset_y = 15.0 

# --- Modeling Steps ---

# 1. Create the Main Box
# Start with a solid block
main_box = cq.Workplane("XY").box(box_length, box_width, box_total_height)

# Create the internal cavity (shelling effect)
# We want the top to be open.
# The simplest way is to cut a pocket from the top face.
cavity_length = box_length - 2 * wall_thickness
cavity_width = box_width - 2 * wall_thickness
cavity_depth = box_total_height - base_thickness

# Select top face and cut the pocket
main_box = (main_box.faces(">Z")
            .workplane()
            .rect(cavity_length, cavity_width)
            .cutBlind(-cavity_depth))

# 2. Add Corner Posts
# Calculate positions for the 4 corner posts inside the box
# They sit in the corners of the cavity.
# Position relative to center: (L/2 - wall - post_size/2, W/2 - wall - post_size/2)
dx = (cavity_length / 2) - (post_size / 2)
dy = (cavity_width / 2) - (post_size / 2)

posts = (main_box.faces(">Z").workplane(offset=-cavity_depth)
         .rect(post_size, post_size, forConstruction=True) # Construction rect for positioning
         .vertices() # Select vertices of construction rect? No, that's just one rect.
         # Let's use pushPoints for explicit coordinates
         .pushPoints([(dx, dy), (dx, -dy), (-dx, dy), (-dx, -dy)])
         .rect(post_size, post_size)
         .extrude(cavity_depth)
        )
# Union the posts with the main box
part1 = posts # Because the extrusion joined with 'main_box' implicitly due to workplane chain

# 3. Create the Cylinder Object (The cap/button next to the box)
# Create the flange (base disk)
flange = cq.Workplane("XY").circle(cyl_flange_diameter / 2).extrude(cyl_flange_thickness)

# Create the main body on top of the flange
body = (flange.faces(">Z").workplane()
        .circle(cyl_body_diameter / 2)
        .extrude(cyl_body_height))

# Move the cylinder assembly to the side
# The image shows it near the corner. Let's position it relative to the box corner.
# Box corner is at (L/2, W/2). Let's put it at (L/2 + offset, -W/2 - offset) roughly based on perspective
cyl_pos_x = (box_length / 2) + cyl_body_diameter/2 + 5
cyl_pos_y = -(box_width / 2) - cyl_body_diameter/2 

part2 = body.translate((cyl_pos_x, cyl_pos_y, 0))

# 4. Combine into final result
result = part1.union(part2)