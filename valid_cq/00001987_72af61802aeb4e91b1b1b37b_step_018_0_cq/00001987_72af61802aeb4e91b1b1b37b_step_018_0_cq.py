import cadquery as cq

# Parameters
disk_diameter = 100.0
disk_thickness = 5.0
center_hole_diameter = 4.0

# Inner Pattern Parameters
inner_slot_count = 12
inner_slot_start_radius = 8.0
inner_slot_end_radius = 22.0
inner_slot_width = 3.0

# Outer Pattern Parameters
outer_slot_count = 12
outer_slot_start_radius = 26.0
outer_slot_end_radius = 42.0
outer_slot_width = 5.0

def create_radial_slot(start_r, end_r, width):
    """
    Creates a single rounded slot shape centered on the X-axis.
    """
    # Calculate length between circle centers
    center_dist = end_r - start_r
    
    # Create the slot profile
    slot = (
        cq.Workplane("XY")
        .center(start_r + center_dist / 2, 0)
        .slot2D(center_dist, width)
    )
    return slot

# Create the main disk
result = cq.Workplane("XY").circle(disk_diameter / 2).extrude(disk_thickness)

# Create the center hole
result = result.faces(">Z").workplane().circle(center_hole_diameter / 2).cutThruAll()

# Create the inner ring of slots
for i in range(inner_slot_count):
    angle = i * (360.0 / inner_slot_count)
    
    # Generate the slot shape rotated into position
    inner_slot = (
        create_radial_slot(inner_slot_start_radius, inner_slot_end_radius, inner_slot_width)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    
    # Cut the slot from the main body
    result = result.cut(inner_slot.extrude(disk_thickness))

# Create the outer ring of slots
for i in range(outer_slot_count):
    angle = i * (360.0 / outer_slot_count)
    
    # Generate the slot shape rotated into position
    outer_slot = (
        create_radial_slot(outer_slot_start_radius, outer_slot_end_radius, outer_slot_width)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    
    # Cut the slot from the main body
    result = result.cut(outer_slot.extrude(disk_thickness))