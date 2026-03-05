import cadquery as cq

# Parametric dimensions based on standard LEGO plate specifications
# The image shows a 2x16 plate
studs_x = 16
studs_y = 2
pitch = 8.0              # Distance between stud centers (mm)
stud_diameter = 4.8      # Diameter of the studs (mm)
stud_height = 1.7        # Height of the studs (mm)
plate_height = 3.2       # Height of the base plate (mm)

# Calculate overall dimensions for the base
# Nominal dimensions (count * pitch) used for the base block
length = studs_x * pitch
width = studs_y * pitch

# 1. Create the base rectangular plate
# We center the box at the origin to simplify the array positioning later
result = cq.Workplane("XY").box(length, width, plate_height)

# 2. Add the grid of studs on the top face
result = (
    result
    .faces(">Z")                # Select the top face
    .workplane()                # Initialize a new workplane on that face
    .rarray(                    # Create a rectangular array of points
        xSpacing=pitch,
        ySpacing=pitch,
        xCount=studs_x,
        yCount=studs_y,
        center=True             # Center the grid on the workplane origin
    )
    .circle(stud_diameter / 2)  # Draw circles at every array point
    .extrude(stud_height)       # Extrude the circles to create the studs
)