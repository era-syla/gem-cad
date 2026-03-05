import cadquery as cq

# --- Parameter Definitions ---

# Main base plate dimensions
plate_length = 150.0
plate_width = 40.0
plate_thickness = 3.0
plate_hole_dist = 80.0
plate_hole_dia = 5.0

# Circular disk dimensions
disk_radius = 20.0
disk_thickness = 5.0
disk_center_hole_dia = 4.0
disk_small_hole_dia = 3.0
disk_small_hole_offset = 12.0  # Distance from center for the smaller hole
disk_pin_dia = 4.0
disk_pin_length = 8.0 # Total length including the part inside the disk

# Small bar dimensions
small_bar_length = 15.0
small_bar_width = 5.0
small_bar_thickness = 3.0
small_bar_hole_dist = 10.0 # Approximate
small_bar_hole_dia = 2.0

# Medium bar dimensions
med_bar_length = 40.0
med_bar_width = 5.0
med_bar_thickness = 3.0
med_bar_hole_dist = 30.0 # Approximate
med_bar_hole_dia = 2.0

# --- Geometry Creation ---

# 1. Create the large rectangular plate
# Rectangle centered at origin, extruded, with two holes along X axis
plate = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-plate_hole_dist/2, 0), (plate_hole_dist/2, 0)])
    .hole(plate_hole_dia)
)

# 2. Create the circular disk assembly
# Create the disk
disk = (
    cq.Workplane("XY")
    .circle(disk_radius)
    .extrude(disk_thickness)
)

# Add the center hole
disk = (
    disk.faces(">Z")
    .workplane()
    .hole(disk_center_hole_dia)
)

# Add the offset smaller hole
disk = (
    disk.faces(">Z")
    .workplane()
    .pushPoints([(disk_small_hole_offset, 0)]) # Offset along X relative to disk center
    .hole(disk_small_hole_dia)
)

# Add the pin protruding from the bottom
pin = (
    cq.Workplane("XY")
    .workplane(offset=-disk_pin_length + disk_thickness) # Start below
    .circle(disk_pin_dia/2)
    .extrude(disk_pin_length) # Extrude up into the disk
    .translate((0, -disk_small_hole_offset, 0)) # Position pin opposite the small hole roughly
)
# Combine disk and pin
disk_assembly = disk.union(pin)

# 3. Create the small bar
small_bar = (
    cq.Workplane("XY")
    .box(small_bar_length, small_bar_width, small_bar_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-small_bar_hole_dist/2, 0), (small_bar_hole_dist/2, 0)])
    .hole(small_bar_hole_dia)
)

# 4. Create the medium bar
med_bar = (
    cq.Workplane("XY")
    .box(med_bar_length, med_bar_width, med_bar_thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-med_bar_hole_dist/2, 0), (med_bar_hole_dist/2, 0)])
    .hole(med_bar_hole_dia)
)

# --- Assembly / Positioning ---

# To match the image layout, we translate the parts relative to the main plate.
# The plate stays at (0,0,0).

# Move disk to the right and slightly down
disk_assembly_positioned = disk_assembly.translate((plate_length/2 + 30, -10, 0))

# Move small bar below the disk
small_bar_positioned = small_bar.translate((plate_length/2 + 10, -40, 0))

# Move medium bar below the disk, next to small bar
med_bar_positioned = med_bar.translate((plate_length/2 + 45, -40, 0))

# Combine all into one result object
result = (
    plate
    .union(disk_assembly_positioned)
    .union(small_bar_positioned)
    .union(med_bar_positioned)
)