import cadquery as cq

# Parameters
outer_diameter = 50.0
height = 200.0
wall_thickness = 2.0
hole_diameter = 15.0
hole_height_from_top = 40.0

# Calculated values
inner_diameter = outer_diameter - (2 * wall_thickness)
hole_center_z = height - hole_height_from_top
radius = outer_diameter / 2.0

# Create the main cylinder
# We create a solid cylinder first
main_body = cq.Workplane("XY").circle(radius).extrude(height)

# Create the hollow inside
# We subtract a smaller cylinder to create the tube
hollow_cutout = cq.Workplane("XY").circle(inner_diameter / 2.0).extrude(height)
tube = main_body.cut(hollow_cutout)

# Create the side hole
# We define a workplane on the side of the cylinder (XZ plane, offset by radius)
# Or easier: Create a cylinder perpendicular to the Z axis and cut it.
# Let's use a workplane centered on the axis, rotated, and extruded.

# Method: Create a cylinder for the hole cutter oriented along Y axis
# Move it up to the correct Z height
hole_cutter = (
    cq.Workplane("XZ")
    .center(0, hole_center_z)
    .circle(hole_diameter / 2.0)
    .extrude(outer_diameter + 10) # Extrude enough to pass through, centered on XZ plane implies Y direction
    .translate((0, -(outer_diameter/2 + 5), 0)) # Move it so it cuts through
)

# Alternatively, a cleaner CadQuery way using workplanes relative to faces:
# But since it's a cylinder, selecting a face is tricky. 
# Let's stick to simple boolean operations which are robust.
# Let's refine the cutter position.
hole_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=0) # Center of the tube
    .center(0, hole_center_z)
    .circle(hole_diameter / 2.0)
    .extrude(outer_diameter * 2, both=True) # Extrude in X direction both ways to ensure cut
)

# Apply the cut
result = tube.cut(hole_cutter)

# Export or visualize (not strictly required by prompt but good practice if running locally)
# show_object(result)