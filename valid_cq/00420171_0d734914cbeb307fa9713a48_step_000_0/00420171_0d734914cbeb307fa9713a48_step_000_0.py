import cadquery as cq

# Define parametric dimensions
plate_width = 50.0
plate_height = 50.0
thickness = 2.0

# Calculate the offset for a corner overlap
# Assuming the overlap is exactly one quadrant (1/4th) of the plate
offset_x = plate_width / 2.0
offset_y = plate_height / 2.0

# Create the first plate centered at the origin
plate1 = cq.Workplane("XY").box(plate_width, plate_height, thickness)

# Create the second plate, offset diagonally
# We create a new workplane, shift its center, and create the box there
plate2 = (
    cq.Workplane("XY")
    .center(offset_x, offset_y)
    .box(plate_width, plate_height, thickness)
)

# Create the final geometry by unioning the two plates
# This handles the overlapping volume (the dark square in the reference) correctly
result = plate1.union(plate2)