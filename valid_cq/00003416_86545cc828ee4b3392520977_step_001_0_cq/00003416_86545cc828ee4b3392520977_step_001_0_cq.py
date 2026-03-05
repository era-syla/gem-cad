import cadquery as cq

# Parameters for the main dimensions
width = 60.0    # Overall width
depth = 50.0    # Overall depth (front to back)
height = 60.0   # Overall height
thickness = 3.0 # Main wall thickness

# Vertical back frame dimensions
back_frame_width = 40.0
back_frame_height = 50.0
back_frame_window_w = 20.0
back_frame_window_h = 25.0

# Bottom rail dimensions
rail_height = 12.0
rail_length = depth - thickness

# Top extension dimensions
top_ext_height = 25.0
top_ext_width = 15.0

# Create the main back plate/frame
# We start with a centered rectangle and cut the window
back_plate = (
    cq.Workplane("XY")
    .box(back_frame_width, thickness, back_frame_height)
    .faces(">Y")
    .workplane()
    .center(0, -5) # Adjust center for window
    .rect(back_frame_window_w, back_frame_window_h)
    .cutThruAll()
)

# Add the bottom side rails (the U-shape base)
# Left rail
left_rail = (
    cq.Workplane("XY")
    .workplane(offset=-back_frame_height/2 + rail_height/2) # Position at bottom
    .center(-back_frame_width/2 + thickness/2, thickness/2 + rail_length/2)
    .box(thickness, rail_length, rail_height)
)

# Right rail
right_rail = (
    cq.Workplane("XY")
    .workplane(offset=-back_frame_height/2 + rail_height/2)
    .center(back_frame_width/2 - thickness/2, thickness/2 + rail_length/2)
    .box(thickness, rail_length, rail_height)
)

# Add the horizontal L-brackets/arms extending from the middle
arm_elevation = 0.0 # Vertical center of the back plate
arm_length = 30.0
arm_width = 4.0

# Left arm structure
left_arm_base = (
    cq.Workplane("XY")
    .workplane(offset=arm_elevation)
    .center(-back_frame_width/2 - thickness/2, thickness/2 + arm_length/2 - 5)
    .box(thickness, arm_length, arm_width)
)

# Add detail to left arm (the L-shape hook at the end)
left_arm_hook = (
    cq.Workplane("XY")
    .workplane(offset=arm_elevation)
    .center(-back_frame_width/2 - thickness/2 + 3, thickness/2 + arm_length - 5 - thickness/2)
    .box(6, thickness, arm_width)
)

# Right arm structure
right_arm_base = (
    cq.Workplane("XY")
    .workplane(offset=arm_elevation)
    .center(back_frame_width/2 + thickness/2, thickness/2 + arm_length/2 - 5)
    .box(thickness, arm_length, arm_width)
)

# Add detail to right arm (the L-shape hook at the end)
right_arm_hook = (
    cq.Workplane("XY")
    .workplane(offset=arm_elevation)
    .center(back_frame_width/2 + thickness/2 - 3, thickness/2 + arm_length - 5 - thickness/2)
    .box(6, thickness, arm_width)
)

# The complex top extension (tower)
top_tower = (
    cq.Workplane("XY")
    .workplane(offset=back_frame_height/2 + top_ext_height/2 - thickness)
    .center(0, 0)
    .box(top_ext_width, thickness, top_ext_height)
)

# Window in the top tower
top_tower = (
    top_tower.faces(">Y")
    .workplane()
    .rect(8, 8)
    .cutThruAll()
)

# The horizontal bar at the very top of the tower
top_bar = (
    cq.Workplane("XY")
    .workplane(offset=back_frame_height/2 + top_ext_height - thickness*1.5)
    .center(5, thickness) # Offset slightly to the right
    .box(top_ext_width + 10, thickness, thickness)
)

# The hook/return on the top bar
top_bar_return = (
    cq.Workplane("XY")
    .workplane(offset=back_frame_height/2 + top_ext_height - thickness*1.5)
    .center(5 + (top_ext_width + 10)/2 - thickness/2, thickness + 5)
    .box(thickness, 10, thickness)
)


# Side reinforcements (wings) near the middle arms
left_wing = (
    cq.Workplane("XY")
    .workplane(offset=arm_elevation + 10)
    .center(-back_frame_width/2 + thickness/2, thickness/2 + 5)
    .box(thickness, 10, 15)
    # Add a hole
    .faces(">X").workplane().center(0, 3).circle(2).cutThruAll()
)

right_wing = (
    cq.Workplane("XY")
    .workplane(offset=arm_elevation + 10)
    .center(back_frame_width/2 - thickness/2, thickness/2 + 5)
    .box(thickness, 10, 15)
    # Add a hole
    .faces("<X").workplane().center(0, 3).circle(2).cutThruAll()
)

# Front supports on the bottom rails
left_front_support = (
    cq.Workplane("XY")
    .workplane(offset=-back_frame_height/2 + rail_height + 2)
    .center(-back_frame_width/2 + thickness/2, depth - 5)
    .box(thickness, 10, 4)
)

right_front_support = (
    cq.Workplane("XY")
    .workplane(offset=-back_frame_height/2 + rail_height + 2)
    .center(back_frame_width/2 - thickness/2, depth - 5)
    .box(thickness, 10, 4)
)

# Small shelf/tab protruding inwards on the right wing
right_inner_tab = (
    cq.Workplane("XY")
    .workplane(offset=arm_elevation - 5)
    .center(back_frame_width/2 - thickness - 3, thickness/2 + 5)
    .box(6, 6, thickness)
)

# Connect everything
result = (
    back_plate
    .union(left_rail)
    .union(right_rail)
    .union(left_arm_base)
    .union(left_arm_hook)
    .union(right_arm_base)
    .union(right_arm_hook)
    .union(top_tower)
    .union(top_bar)
    .union(top_bar_return)
    .union(left_wing)
    .union(right_wing)
    .union(left_front_support)
    .union(right_front_support)
    .union(right_inner_tab)
)

# Apply some fillets to simulate the molded/smooth look in corners where structurally relevant
# or easy to select.
try:
    result = result.edges("|Z and (not <Z) and (not >Z)").fillet(0.5)
except:
    pass # Skip filleting if topology is too complex for simple selection logic