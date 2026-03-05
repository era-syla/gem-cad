import cadquery as cq

# Parametric dimensions
disk_radius = 10.0
disk_thickness = 4.0
spacing_x = 35.0  # Center-to-center distance in X
spacing_y = 45.0  # Center-to-center distance in Y (appears larger in the image)
rows = 2
cols = 2

# Create the 2x2 array of cylindrical disks
result = (
    cq.Workplane("XY")
    .rarray(
        xSpacing=spacing_x, 
        ySpacing=spacing_y, 
        xCount=cols, 
        yCount=rows, 
        center=True
    )
    .circle(disk_radius)
    .extrude(disk_thickness)
)