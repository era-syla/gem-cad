import cadquery as cq

# Parameters for the cylinder
cylinder_radius = 15.0
cylinder_height = 20.0
cylinder_x_offset = 20.0  # Move slightly to the right to match perspective
cylinder_z_offset = 30.0  # Height above the origin

# Parameters for the folded plate (tent shape)
plate_length = 40.0
plate_width = 30.0
plate_thickness = 1.0  # Thin sheet
bend_angle = 120.0     # Angle between the two planes
plate_z_offset = -10.0 # Position relative to origin

# Create the Cylinder
# We create a workplane, offset it, and extrude a circle
cyl = (
    cq.Workplane("XY")
    .center(cylinder_x_offset, cylinder_x_offset) # Position based on visual arrangement
    .workplane(offset=cylinder_z_offset)
    .circle(cylinder_radius)
    .extrude(cylinder_height)
)

# Create the Folded Plate
# Method: Create a wedge/prism or just two thin boxes rotated
# A simpler way to get the exact look is to sketch a 'V' profile and extrude it
# Or sketch a rectangle and a line, but extruding a V-shape profile is robust.

# Let's define the V-shape profile points
# Assuming the bend is along the Y-axis
half_width = plate_width / 2.0
height_drop = 15.0 # How far down the wings go

# Points for a V-profile (cross-section)
# Center point at (0,0), then wings going out
p1 = (-half_width, -height_drop)
p2 = (0, 0) # Peak of the tent
p3 = (half_width, -height_drop)

# To make it a solid with thickness, we offset these lines
# Or easier: just make two thin boxes and rotate them.
# Let's try the two-box method for clarity and control.

# Left wing
wing_left = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, plate_thickness)
    .rotate((0,0,0), (0,1,0), -30) # Tilt it
    .translate((-plate_width/2 * 0.8, 0, 0)) # Move it roughly into position
)

# Right wing
wing_right = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, plate_thickness)
    .rotate((0,0,0), (0,1,0), 30) # Tilt opposite way
    .translate((plate_width/2 * 0.8, 0, 0))
)

# Alternative, cleaner approach for the folded plate:
# Sketch the profile on the XZ plane and extrude along Y.
# Let's define a path that looks like "^"
# We need an inner and outer wire to form a closed profile with thickness.

plate_h_span = 20.0 # Horizontal distance from center to edge
plate_v_drop = 15.0 # Vertical drop
thickness_vert = 1.0 # Approximate vertical thickness for simplicity

points = [
    (-plate_h_span, -plate_v_drop),
    (0, 0),
    (plate_h_span, -plate_v_drop),
    (plate_h_span, -plate_v_drop - thickness_vert),
    (0, -thickness_vert),
    (-plate_h_span, -plate_v_drop - thickness_vert)
]

folded_plate = (
    cq.Workplane("XZ")
    .polyline(points)
    .close()
    .extrude(plate_length)
    # Center the extrusion on Y
    .translate((0, -plate_length/2, 0)) 
    # Move the whole assembly to match the image relative to cylinder
    .translate((-10, -10, 0)) 
)

# Combine the objects
result = cyl.union(folded_plate)
