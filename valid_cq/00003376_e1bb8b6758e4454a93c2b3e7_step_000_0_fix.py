import cadquery as cq

# Main plate dimensions
plate_width = 40
plate_height = 70
plate_thickness = 4

# Create the main rectangular plate with rounded corners
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
)

# Add rounded corners via fillet
result = result.edges("|Z").fillet(4)

# Create slot dimensions
slot_width = 24
slot_height = 6
slot_radius = 3

# Top slot - centered horizontally, near top of plate
top_slot_y = plate_height / 2 - 10

result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, top_slot_y - plate_height/2 + plate_height - 10)
)

# Cut top slot
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(plate_thickness)
    .edges("|Z").fillet(4)
)

# Cut slots using slot shape (rounded rectangle)
def make_slot(wp, x_pos, y_pos, s_width, s_height):
    return (
        wp.faces(">Z")
        .workplane()
        .center(x_pos, y_pos)
        .slot2D(s_width, s_height, 0)
        .cutThruAll()
    )

# Top slot position
top_y = plate_height / 2 - 10
# Bottom slot position  
bottom_y = -(plate_height / 2 - 10)

result = make_slot(result, 0, top_y, slot_width, slot_height)
result = make_slot(result, 0, bottom_y, slot_width, slot_height)

# Add center hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(3)
    .cutThruAll()
)

# Add small circular bump/boss on the left side
bump_x = -(plate_width / 2)
bump_y = 0
bump_radius = 5
bump_height = 3

bump = (
    cq.Workplane("YZ")
    .center(bump_y, plate_thickness / 2)
    .circle(bump_radius)
    .extrude(bump_radius)
)

# Position bump on left side
bump = bump.translate((-plate_width / 2 - bump_radius + bump_radius, 0, 0))

# Create the bump on the left face
result = (
    result
    .faces("<X")
    .workplane(origin=(0, 0, 0))
    .center(0, plate_thickness / 2)
    .circle(bump_radius)
    .extrude(bump_radius)
)