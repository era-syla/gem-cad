import cadquery as cq

# Parametric dimensions for the frame
frame_height = 100.0
frame_width = 60.0
frame_depth = 30.0
tube_thickness = 5.0

# Create the main outer block
outer_box = cq.Workplane("XY").box(frame_width, frame_depth, frame_height)

# Create cutting tools to hollow out the center and faces
# We subtract boxes that are slightly smaller than the outer dims 
# in two axes, and larger in the cutting axis.

# 1. Cut along the X-axis (removes side walls)
# Dimensions: Over-sized X, reduced Y, reduced Z
cut_x = cq.Workplane("XY").box(
    frame_width * 2, 
    frame_depth - 2 * tube_thickness, 
    frame_height - 2 * tube_thickness
)

# 2. Cut along the Y-axis (removes front and back walls)
# Dimensions: reduced X, Over-sized Y, reduced Z
cut_y = cq.Workplane("XY").box(
    frame_width - 2 * tube_thickness, 
    frame_depth * 2, 
    frame_height - 2 * tube_thickness
)

# 3. Cut along the Z-axis (removes top and bottom walls)
# Dimensions: reduced X, reduced Y, Over-sized Z
cut_z = cq.Workplane("XY").box(
    frame_width - 2 * tube_thickness, 
    frame_depth - 2 * tube_thickness, 
    frame_height * 2
)

# Perform boolean subtractions to create the frame structure
result = outer_box.cut(cut_x).cut(cut_y).cut(cut_z)