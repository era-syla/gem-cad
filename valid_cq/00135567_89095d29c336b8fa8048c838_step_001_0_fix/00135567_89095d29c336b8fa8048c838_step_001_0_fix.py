import cadquery as cq

base_height = 30
base_radius = 10
plate_length = 80
plate_width = 20
plate_thickness = 5
slot_radius = 6
central_diameter = 12

# Base cylinder
base = cq.Workplane("XY").cylinder(base_height, base_radius)

# Plate on top of base
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness).translate((0, 0, base_height + plate_thickness/2))

# Slot cutouts at ends of plate (semi‐circular ends + rectangular channel)
slot1 = cq.Workplane("XZ").cylinder(plate_width + 2, slot_radius).translate((-(plate_length/2 - slot_radius), 0, base_height + plate_thickness/2))
slot2 = cq.Workplane("XZ").cylinder(plate_width + 2, slot_radius).translate(( (plate_length/2 - slot_radius), 0, base_height + plate_thickness/2))
rect_cut = cq.Workplane("XY").box(plate_length - 2*slot_radius, plate_width + 2, plate_thickness + 2).translate((0, 0, base_height + plate_thickness/2))

# Central hole through plate
central_cut = cq.Workplane("XY", origin=(0, 0, base_height)).cylinder(plate_thickness + 1, central_diameter/2)

# Apply cuts to plate
plate_cut = plate.cut(slot1).cut(slot2).cut(rect_cut).cut(central_cut)

# Combine base and plate
result = base.union(plate_cut)