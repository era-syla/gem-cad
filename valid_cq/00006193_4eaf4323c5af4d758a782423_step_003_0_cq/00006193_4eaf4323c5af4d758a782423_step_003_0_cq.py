import cadquery as cq

# Parameters for the model
plate_width = 100.0   # Width of the base plate (x-direction)
plate_length = 100.0  # Length of the base plate (y-direction)
plate_thickness = 5.0 # Thickness of the base plate
num_pyramids_x = 5    # Number of pyramids in x-direction
num_pyramids_y = 5    # Number of pyramids in y-direction
pyramid_height = 10.0 # Height of the pyramids

# Calculations derived from parameters
pyr_base_w = plate_width / num_pyramids_x
pyr_base_l = plate_length / num_pyramids_y

# 1. Create the base plate
base_plate = cq.Workplane("XY").box(plate_width, plate_length, plate_thickness)

# 2. Define a single pyramid shape
# We create a pyramid by lofting a rectangle to a point or using a tapered extrusion.
# Here, we will use a loft from the base rectangle to a center point.
def create_pyramid(loc):
    return (
        cq.Workplane("XY")
        .rect(pyr_base_w, pyr_base_l)
        .workplane(offset=pyramid_height)
        .rect(0.001, 0.001) # Theoretically a point, but small rect avoids kernel issues
        .loft(combine=False)
        .val()
        .locate(loc)
    )

# 3. Create the grid of points where pyramids will be placed
# The points need to be on the top surface of the plate
pyramid_centers = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness/2) # Move to top of plate
    .rarray(
        xSpacing=pyr_base_w, 
        ySpacing=pyr_base_l, 
        xCount=num_pyramids_x, 
        yCount=num_pyramids_y, 
        center=True
    )
)

# 4. Generate the pyramids using `eachpoint`
# Note: creating individual solids and unioning them is one way,
# but using `eachpoint` with a callback is cleaner for patterns.
# However, `eachpoint` with custom solids can be tricky. 
# A more robust CadQuery method for this specific shape is to iterate and union.
# Alternatively, we can use the `rarray` created above to place copies.

pyramids = (
    pyramid_centers
    .eachpoint(create_pyramid)
)

# 5. Combine everything
# We union the base plate with the generated pyramids
result = base_plate.union(pyramids)