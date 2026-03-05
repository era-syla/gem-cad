import cadquery as cq

# Parametric definitions for dimensions
plate_length = 200.0
plate_width = 40.0
plate_thickness = 3.0
hole_diameter = 6.0
num_holes = 5
hole_spacing = 30.0

# Create the base rectangular plate
# box() centers the geometry at the origin (0,0,0)
base = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the linear pattern of holes
# Select the top face (>Z), create a workplane, define a rectangular array (1D in this case), and cut holes
result = (
    base.faces(">Z")
    .workplane()
    .rarray(
        xSpacing=hole_spacing, 
        ySpacing=1,          # ySpacing is irrelevant for a single row
        xCount=num_holes, 
        yCount=1             # Single row of holes
    )
    .hole(hole_diameter)
)