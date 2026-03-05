import cadquery as cq

# Parameters
thickness = 5.0
width = 150.0  # Total width of the back edge
depth = 80.0   # Distance from back edge to the furthest front point
corner_cut_x = 20.0 # Horizontal distance of the corner chamfer
corner_cut_y = 30.0 # Vertical distance of the corner chamfer
arc_radius = 50.0 # Radius of the front circular cutout
hole_diameter = 6.0
hole_spacing = 50.0 # Spacing between holes
hole_offset_y = 15.0 # Distance from the back edge to hole centers

# Create the base shape
# We'll start with a rectangle and then modify it
# Or better, draw the profile directly
pts = [
    (-width/2, 0),  # Top left corner (back edge is at y=0)
    (width/2, 0),   # Top right corner
    (width/2, -corner_cut_y), # Right angled corner start
    (width/2 - corner_cut_x, -depth), # Bottom right point
    (-width/2 + corner_cut_x, -depth), # Bottom left point
    (-width/2, -corner_cut_y), # Left angled corner end
]

# Create the main plate
plate = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(thickness)
)

# Create the circular cutout
# The cutout is centered horizontally, located towards the front
cutout_center_y = -depth - 10 # Center of circle slightly below the front edge
cutout_r = arc_radius

# We need to subtract a cylinder or circle
plate_with_cutout = (
    plate.faces("<Z") # Select bottom face to draw on
    .workplane()
    .moveTo(0, -depth) # Move to the front edge center
    .circle(arc_radius) # Draw the circle
    .cutThruAll() # Cut through the plate
)

# Add the mounting holes
# Three holes: one center, two offset
holes = (
    plate_with_cutout.faces(">Z")
    .workplane()
    .moveTo(0, -hole_offset_y)
    .circle(hole_diameter/2)
    .moveTo(-hole_spacing, -hole_offset_y)
    .circle(hole_diameter/2)
    .moveTo(hole_spacing, -hole_offset_y)
    .circle(hole_diameter/2)
    .cutThruAll()
)

result = holes