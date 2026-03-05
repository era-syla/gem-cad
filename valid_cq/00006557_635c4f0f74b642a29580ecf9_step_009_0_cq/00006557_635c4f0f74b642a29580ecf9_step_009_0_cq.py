import cadquery as cq

# Parametric dimensions
length = 100.0       # Distance between hole centers
width = 20.0         # Width of the link
thickness = 2.0      # Thickness of the plate
hole_diameter = 10.0 # Diameter of the holes at ends

# The total length of the object is length + width (due to radius at each end)
# We will create it centered on the origin for easier mirroring if needed later, 
# but simply drawing it flat is best.

# Construct the geometry
# 1. Sketch the 2D profile
#    - We can use a 'slot' shape or a hull of two circles
#    - CadQuery's sketch API is very convenient for this.
#    - Alternatively, we can use the Workplane API directly.

result = (
    cq.Workplane("XY")
    .slot2D(length, width)  # Creates a slot with center-to-center distance `length` and diameter `width`
    .extrude(thickness)     # Extrude to create the solid plate
    .faces(">Z")            # Select the top face to cut holes
    .workplane()
    .pushPoints([(-length/2.0, 0), (length/2.0, 0)]) # Locate hole centers
    .hole(hole_diameter)    # Cut the holes
)

# Alternative method using Sketch API (often cleaner for complex 2D profiles, though this is simple):
# result = (
#     cq.Workplane("XY")
#     .sketch()
#     .slot(length, width, angle=0) # Defines the outer boundary
#     .push([(-length/2, 0), (length/2, 0)])
#     .circle(hole_diameter/2, mode='s') # Subtractive circle for holes
#     .finalize()
#     .extrude(thickness)
# )

# The first method is very robust for this specific shape.