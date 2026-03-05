import cadquery as cq

# Parametric dimensions
base_width = 20.0  # Overall width (X direction)
base_depth = 12.0  # Overall depth (Y direction)
base_height = 25.0 # Height of the main box (Z direction)
wall_thickness = 2.0

# Lever dimensions
lever_width = 6.0
lever_height = 25.0 # Height above the base
lever_depth_bottom = 10.0
lever_depth_top = 2.0
lever_angle_offset = 5.0 # Shift back/forward

# Pivot/Hinge dimensions
pivot_radius = 2.5
pivot_y_offset = -3.0 # Relative to center
pivot_z_offset = 5.0  # Relative to bottom or specific feature

# Create the main housing shell
# Start with a solid block and shell it out
main_body = (
    cq.Workplane("XY")
    .box(base_width, base_depth, base_height)
    .edges("|Z")
    .fillet(2.0) # Rounded corners on the vertical edges
)

# Shelling the box from the top
# Create a cutting tool for the inside
cavity = (
    cq.Workplane("XY")
    .box(base_width - 2*wall_thickness, base_depth - 2*wall_thickness, base_height)
    .edges("|Z")
    .fillet(1.0)
    .translate((0, 0, wall_thickness)) # Move up to leave floor thickness
)

housing = main_body.cut(cavity)

# Create the cutouts on the top sides for the mechanism
side_cut_depth = 5.0
side_cut_width = base_width  # Cut all the way through X
side_cut_length = 6.0 # Y direction cut
side_cut_z = base_height / 2.0 - side_cut_depth / 2.0

# Not strictly a simple box cut, it has steps. Let's model the top opening detail.
# Cut out the front-top area
front_cutout = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2.0)
    .center(0, -base_depth/4.0)
    .box(base_width - 2*wall_thickness, base_depth/2.0, 5.0, combine=False)
)
housing = housing.cut(front_cutout)

# Create the "Hinge" features on the sides
hinge_cyl = (
    cq.Workplane("YZ")
    .workplane(offset=base_width/2.0) # Move to right face
    .center(base_depth/2.0, -base_height/4.0) # Position near back-mid
    .circle(pivot_radius)
    .extrude(2.0) # Stick out
)
hinge_cyl_mirror = (
    cq.Workplane("YZ")
    .workplane(offset=-base_width/2.0 - 2.0) # Move to left face
    .center(base_depth/2.0, -base_height/4.0)
    .circle(pivot_radius)
    .extrude(2.0)
)

housing = housing.union(hinge_cyl).union(hinge_cyl_mirror)

# Create the central triangular lever
# Define points for the side profile of the lever
pts = [
    (0, 0),
    (lever_depth_bottom, 0),
    (lever_depth_bottom, 3.0), # Small vertical step
    (lever_depth_top, lever_height),
    (0, lever_height)
]

lever_profile = (
    cq.Workplane("YZ")
    .center(0, base_height/2.0 - 2.0) # Position somewhat correctly in Z
    .polyline(pts)
    .close()
    .extrude(lever_width)
)

# Center the lever
lever = lever_profile.translate((-lever_width/2.0, -2.0, 0))

# Add the internal mechanism block (the part the lever sits on/in)
inner_block = (
    cq.Workplane("XY")
    .box(base_width - 2*wall_thickness - 0.5, base_depth - 2*wall_thickness - 0.5, 6.0)
    .translate((0, 0, base_height/2.0 - 5.0))
)

# Detail on the internal block (looks like a flexible tab or catch)
tab_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2.0 - 2.0)
    .center(0, 2.0)
    .rect(lever_width + 2.0, 5.0)
    .extrude(-2.0, combine=False)
)
inner_block = inner_block.cut(tab_cut)
inner_block = inner_block.edges("|Z").fillet(0.5)

# Side holes on the main body
side_hole = (
    cq.Workplane("YZ")
    .center(0, 0) # Center of the side face
    .circle(1.5)
    .extrude(base_width + 5.0) # Cut through everything
    .translate((-base_width/2.0 - 2.5, 0, 0))
)

# Assemble
result = housing.union(inner_block).union(lever).cut(side_hole)

# Apply fillet to the back edge of the lever to match image style
try:
    result = result.edges(cq.selectors.BoxSelector(
        (-lever_width, 0, base_height), 
        (lever_width, 10, base_height + lever_height + 1)
    )).fillet(0.5)
except:
    pass # Fallback if selector misses

# Refine the top edge of the housing
try:
   result = result.edges(">Z").fillet(0.5)
except:
   pass 

# Final result
result = result