import cadquery as cq

# Dimensions (approximate)
plate_length = 80
plate_width = 18
plate_thickness = 3
hole_radius = 4
slot_width = 8
slot_length = 50

# Tab/handle dimensions
tab_width = 14
tab_height = 18
tab_depth_bottom = 8
tab_depth_top = 14
tab_thickness = 3

# Create the flat plate (rounded rectangle)
plate = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .rect(plate_width, plate_length)
    .extrude(plate_thickness)
)

# Round the ends of the plate
plate = (
    cq.Workplane("XY")
    .workplane()
    .center(0, plate_length/2 - plate_width/2)
    .circle(plate_width/2)
    .extrude(plate_thickness)
    .union(
        cq.Workplane("XY")
        .center(0, -(plate_length/2 - plate_width/2))
        .circle(plate_width/2)
        .extrude(plate_thickness)
    )
    .union(
        cq.Workplane("XY")
        .rect(plate_width, plate_length - plate_width)
        .extrude(plate_thickness)
    )
)

# Cut mounting holes at top and bottom
plate = (
    plate
    .cut(
        cq.Workplane("XY")
        .center(0, plate_length/2 - plate_width/2)
        .circle(hole_radius/2 * 1.2)
        .extrude(plate_thickness)
    )
    .cut(
        cq.Workplane("XY")
        .center(0, -(plate_length/2 - plate_width/2))
        .circle(hole_radius/2 * 1.2)
        .extrude(plate_thickness)
    )
)

# Cut the center slot
slot_offset = 5
plate = plate.cut(
    cq.Workplane("XY")
    .center(0, slot_offset)
    .rect(slot_width, slot_length)
    .extrude(plate_thickness)
)

# Round the slot ends
plate = plate.cut(
    cq.Workplane("XY")
    .center(0, slot_offset + slot_length/2)
    .circle(slot_width/2)
    .extrude(plate_thickness)
).cut(
    cq.Workplane("XY")
    .center(0, slot_offset - slot_length/2)
    .circle(slot_width/2)
    .extrude(plate_thickness)
)

# Create the trapezoidal tab/handle on top
# The tab sits at the top of the plate
tab_y_pos = plate_length/2 - plate_width/2  # top center of plate

# Trapezoidal prism for the tab
# Bottom face is smaller, top face is larger (or tapered)
tab_bottom_width = tab_width
tab_top_width = tab_width + 6
tab_x_offset = 0
tab_z_base = plate_thickness

tab = (
    cq.Workplane("XY")
    .workplane(offset=tab_z_base)
    .center(tab_x_offset, tab_y_pos)
    .rect(tab_bottom_width, tab_depth_bottom)
    .workplane(offset=tab_height)
    .transformed(offset=cq.Vector(tab_x_offset, tab_y_pos, 0))
    .rect(tab_top_width, tab_depth_top)
)

# Build tab as loft
tab_bottom = (
    cq.Workplane("XY")
    .workplane(offset=tab_z_base)
    .center(tab_x_offset, tab_y_pos)
    .rect(tab_bottom_width, tab_depth_bottom)
)

tab_top = (
    cq.Workplane("XY")
    .workplane(offset=tab_z_base + tab_height)
    .center(tab_x_offset, tab_y_pos)
    .rect(tab_top_width, tab_depth_top)
)

# Build tab using shell approach
tab_solid = (
    cq.Workplane("XY")
    .workplane(offset=tab_z_base)
    .center(0, tab_y_pos)
    .rect(tab_bottom_width, tab_depth_bottom)
    .extrude(tab_height)
)

# Combine plate and tab
result = plate.union(tab_solid)

# Add small fillets to soften edges
result = result.edges("|Z").fillet(1.5)