import cadquery as cq

# Parametric dimensions
back_plate_radius = 40.0
back_plate_thickness = 2.0

inner_ring_radius = 25.0
inner_ring_thickness = 4.0
inner_ring_offset = 2.0  # Slightly protrudes from the back plate

large_cylinder_radius = 20.0
large_cylinder_length = 30.0
# The large cylinder is offset from the center
large_cylinder_y_offset = -12.0 

medium_cylinder_radius = 6.0
medium_cylinder_length = 25.0
# The medium cylinder sits "on top" of the large cylinder, roughly centered on Y=0 or slightly above
medium_cylinder_y_offset = 15.0

small_pin_radius = 2.0
small_pin_length = 10.0 # Stick out length from medium cylinder

# Create the Back Plate (Main Disk)
# We'll orient the Z-axis as the axis of revolution/extrusion
back_plate = cq.Workplane("XY").circle(back_plate_radius).extrude(back_plate_thickness)

# Create the Inner Ring/Step
# This sits on top of the back plate
inner_ring = (
    cq.Workplane("XY")
    .workplane(offset=back_plate_thickness)
    .circle(inner_ring_radius)
    .extrude(inner_ring_thickness)
)

# Create the Large Lower Cylinder
# This is offset in the Y direction and extruded further out
large_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=back_plate_thickness) # Starts at the face of the back plate
    .center(0, large_cylinder_y_offset)
    .circle(large_cylinder_radius)
    .extrude(large_cylinder_length)
)

# Create the Medium Upper Cylinder
# This is offset in the positive Y direction
medium_cylinder = (
    cq.Workplane("XY")
    .workplane(offset=back_plate_thickness) # Starts at the face of the back plate
    .center(0, medium_cylinder_y_offset)
    .circle(medium_cylinder_radius)
    .extrude(medium_cylinder_length)
)

# Create the Small Pin
# Extends from the end of the medium cylinder
small_pin = (
    cq.Workplane("XY")
    .workplane(offset=back_plate_thickness + medium_cylinder_length)
    .center(0, medium_cylinder_y_offset)
    .circle(small_pin_radius)
    .extrude(small_pin_length)
)

# Combine all parts into a single object
result = back_plate.union(inner_ring).union(large_cylinder).union(medium_cylinder).union(small_pin)

# Optional: Fillet the connection between large/medium cylinders and the back structures 
# for a more realistic molded look (though not strictly visible in the low-poly reference)
# result = result.faces("|Z").edges().fillet(1.0) 