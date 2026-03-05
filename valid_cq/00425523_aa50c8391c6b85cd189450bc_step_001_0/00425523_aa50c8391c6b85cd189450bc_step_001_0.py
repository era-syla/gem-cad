import cadquery as cq
import math

# Parameters defining the geometry
width = 220.0        # Total width of the part (chord length approx)
depth_left = 85.0    # Depth from chord to top edge on the left side
depth_right = 60.0   # Depth from chord to top edge on the right side
step_x = 25.0        # X position where the step transition occurs
thickness = 6.0      # Thickness of the plate
arc_radius = 250.0   # Radius of the large curved edge

# Hole parameters
hole_y_pos = 35.0    # Y distance from the chord to the line of holes
inner_hole_spacing = 50.0  # Spacing between the two inner circular holes
outer_hole_spacing = 150.0 # Spacing between the two outer slots
hole_diameter = 6.0  # Diameter of the circular holes
slot_length = 18.0   # Total length of the slots
slot_width = 6.0     # Width of the slots

# Calculate the sagitta to find the midpoint of the arc
# The arc connects (-width/2, 0) and (width/2, 0)
sagitta = arc_radius - math.sqrt(arc_radius**2 - (width/2)**2)
# Since the arc is convex relative to the main body (bulges outwards/downwards),
# the midpoint y is negative relative to the chord at y=0.
arc_midpoint = (0, -sagitta)

# Define the points of the perimeter (Counter-Clockwise)
p_bottom_right = (width/2, 0)
p_top_right = (width/2, depth_right)
p_step_corner_1 = (step_x, depth_right)
p_step_corner_2 = (step_x, depth_left)
p_top_left = (-width/2, depth_left)
p_bottom_left = (-width/2, 0)

# Generate the base solid
result = (
    cq.Workplane("XY")
    .moveTo(*p_bottom_right)
    .lineTo(*p_top_right)
    .lineTo(*p_step_corner_1)
    .lineTo(*p_step_corner_2)
    .lineTo(*p_top_left)
    .lineTo(*p_bottom_left)
    # Create the curved bottom edge
    .threePointArc(arc_midpoint, p_bottom_right)
    .close()
    .extrude(thickness)
)

# Create the inner circular holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-inner_hole_spacing/2, hole_y_pos), 
        (inner_hole_spacing/2, hole_y_pos)
    ])
    .hole(hole_diameter)
)

# Create the outer slots
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-outer_hole_spacing/2, hole_y_pos), 
        (outer_hole_spacing/2, hole_y_pos)
    ])
    .slot2D(slot_length, slot_width, angle=0)
    .cutThruAll()
)