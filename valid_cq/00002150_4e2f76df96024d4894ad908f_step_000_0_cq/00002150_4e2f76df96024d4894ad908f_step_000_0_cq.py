import cadquery as cq

# Parameters
width = 16.0    # Approximate width of a dual-stack RJ45
depth = 21.0    # Depth of the housing
height = 14.0   # Height of the housing
wall_thickness = 0.3 # Thickness of the sheet metal

# Spring Finger Parameters
finger_width = 1.5
finger_length = 6.0
finger_bend_height = 0.8
finger_offset_top = 4.0  # From back edge
finger_spacing_top = 4.0 # Distance between top fingers
finger_offset_side = 3.0 # From top edge
finger_spacing_side = 4.0

# Pin Parameters
pin_width = 0.8
pin_length = 3.5

# Step 1: Create the Main Box Shell
# We start with a solid block and shell it out to create the sheet metal enclosure feel.
main_box = (
    cq.Workplane("XY")
    .box(width, depth, height)
    # Remove the front face (assumed to be the opening) and the bottom (for mounting)
    .faces("-Y").shell(-wall_thickness) 
)

# Step 2: Create the Top Spring Fingers
# These are the curved contacts on the top surface.
# We'll create a single finger profile and sweep/extrude it.

def make_spring_finger(length, width, bend_height):
    # Profile for the finger (side view)
    pts = [
        (0, 0),
        (length * 0.2, bend_height),
        (length * 0.8, bend_height),
        (length, 0),
        (length, -wall_thickness), # Close shape
        (length * 0.8, bend_height - wall_thickness),
        (length * 0.2, bend_height - wall_thickness),
        (0, -wall_thickness)
    ]
    
    finger = (
        cq.Workplane("XZ")
        .polyline(pts)
        .close()
        .extrude(width)
    )
    # Center the finger on width
    finger = finger.translate((0, -width/2, 0))
    return finger

# Create cutouts for the fingers
def make_finger_cutout(length, width):
    cutout = (
        cq.Workplane("XY")
        .rect(width + 0.5, length + 1.0)
        .extrude(wall_thickness * 3)
    )
    return cutout

# Generate the top fingers
finger_shape = make_spring_finger(finger_length, finger_width, finger_bend_height)

# Position Top Finger 1 (Left)
top_finger_1 = (
    finger_shape
    .rotate((0,0,0), (1,0,0), 90) # Orient correctly
    .rotate((0,0,0), (0,0,1), 90)
    .translate((-finger_spacing_top/2, depth/2 - finger_offset_top, height/2 + wall_thickness))
)

# Position Top Finger 2 (Right)
top_finger_2 = (
    finger_shape
    .rotate((0,0,0), (1,0,0), 90) 
    .rotate((0,0,0), (0,0,1), 90)
    .translate((finger_spacing_top/2, depth/2 - finger_offset_top, height/2 + wall_thickness))
)

# Create recesses/depressions for the fingers to sit in (visual detail)
top_recess_1 = (
    cq.Workplane("XY")
    .rect(finger_width + 2.0, finger_length + 2.0)
    .extrude(wall_thickness) # Just a cutout or depression
    .translate((-finger_spacing_top/2, depth/2 - finger_offset_top - finger_length/2 + 1.5, height/2))
)

top_recess_2 = (
    cq.Workplane("XY")
    .rect(finger_width + 2.0, finger_length + 2.0)
    .extrude(wall_thickness)
    .translate((finger_spacing_top/2, depth/2 - finger_offset_top - finger_length/2 + 1.5, height/2))
)


# Step 3: Create the Side Spring Fingers
# Similar to top fingers but on the side face (+X)

side_finger_1 = (
    finger_shape
    .rotate((0,0,0), (0,0,1), 90) # Align with Y axis
    .rotate((0,0,0), (0,1,0), -90) # Rotate to side
    .translate((width/2 + wall_thickness, depth/2 - finger_offset_top, height/2 - finger_offset_side))
)

side_finger_2 = (
    finger_shape
    .rotate((0,0,0), (0,0,1), 90) 
    .rotate((0,0,0), (0,1,0), -90) 
    .translate((width/2 + wall_thickness, depth/2 - finger_offset_top, height/2 - finger_offset_side - finger_spacing_side))
)

# Create recesses for side fingers
side_recess_1 = (
    cq.Workplane("YZ")
    .rect(finger_length + 2.0, finger_width + 2.0)
    .extrude(wall_thickness)
    .translate((width/2, depth/2 - finger_offset_top - finger_length/2 + 1.5, height/2 - finger_offset_side))
)

side_recess_2 = (
    cq.Workplane("YZ")
    .rect(finger_length + 2.0, finger_width + 2.0)
    .extrude(wall_thickness)
    .translate((width/2, depth/2 - finger_offset_top - finger_length/2 + 1.5, height/2 - finger_offset_side - finger_spacing_side))
)


# Step 4: Add Mounting Pins/Legs at the bottom
pin_shape = (
    cq.Workplane("XY")
    .rect(pin_width, pin_width)
    .extrude(-pin_length)
    .edges("|Z").fillet(pin_width/2.1) # Round them off a bit
)

pin_left = pin_shape.translate((-width/2 + 1.0, 0, -height/2))
pin_right = pin_shape.translate((width/2 - 1.0, 0, -height/2))
pin_back_l = pin_shape.translate((-width/2 + 1.0, depth/2 - 2.0, -height/2))
pin_back_r = pin_shape.translate((width/2 - 1.0, depth/2 - 2.0, -height/2))

# Step 5: Side Flap Detail
# The image shows a slight angled flap on the side near the top.
flap_pts = [
    (0, 0),
    (depth * 0.4, 0),
    (depth * 0.5, -2.0),
    (0, -2.0)
]

side_flap = (
    cq.Workplane("YZ")
    .polyline(flap_pts).close()
    .extrude(0.5) # Thin sheet
    .translate((width/2 + wall_thickness, depth/2 - depth*0.5, height/2))
)

# Step 6: Combine geometry
# Start with main box
result = main_box

# Cut recesses first
result = result.cut(top_recess_1).cut(top_recess_2).cut(side_recess_1).cut(side_recess_2)

# Add fingers
result = result.union(top_finger_1).union(top_finger_2)
result = result.union(side_finger_1).union(side_finger_2)

# Add side flap detail
result = result.union(side_flap)

# Add pins
result = result.union(pin_left).union(pin_right).union(pin_back_l).union(pin_back_r)

# Step 7: Refine the front folded edge (Lip)
lip = (
    cq.Workplane("XY")
    .rect(width + wall_thickness*2, wall_thickness)
    .extrude(0.5)
    .translate((0, -depth/2 - wall_thickness/2, height/2 + 0.25))
)
result = result.union(lip)

# Add the grounding tab at the bottom
ground_tab = (
    cq.Workplane("YZ")
    .rect(2.0, 5.0)
    .extrude(wall_thickness)
    .translate((width/2, 0, -height/2 - 2.5))
)
result = result.union(ground_tab)

# Final Rotation to match image perspective roughly (optional, but helps visualization)
# result = result.rotate((0,0,0), (1,0,0), -90)