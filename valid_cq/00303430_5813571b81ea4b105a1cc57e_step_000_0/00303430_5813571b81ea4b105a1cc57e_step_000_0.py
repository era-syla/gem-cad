import cadquery as cq

# -- Model Parameters --
plate_width = 100.0       # Overall width of the plate (X axis)
plate_length = 100.0      # Overall length of the plate (Y axis)
plate_thickness = 3.0     # Thickness of the plate
corner_cutout = 12.0      # Size of the square notches to remove from corners

# -- Geometry Construction --
# The shape is constructed by creating two rectangular prisms that form a cross.
# This approach is topologically equivalent to a square plate with the corners removed.

# 1. Create the horizontal section (Full width, reduced length)
# Dimensions: width x (length - 2*cutout) x thickness
horizontal_section = cq.Workplane("XY").box(
    plate_width, 
    plate_length - 2 * corner_cutout, 
    plate_thickness
)

# 2. Create the vertical section (Reduced width, full length)
# Dimensions: (width - 2*cutout) x length x thickness
vertical_section = cq.Workplane("XY").box(
    plate_width - 2 * corner_cutout, 
    plate_length, 
    plate_thickness
)

# 3. Union the two sections to form the final notched plate
result = horizontal_section.union(vertical_section)