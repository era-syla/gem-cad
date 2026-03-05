import cadquery as cq

# Parametric dimensions
length = 100.0   # Total length of the plate
width = 60.0     # Total width of the plate
thickness = 10.0 # Thickness of the plate
hole_dist = 50.0 # Distance between the centers of the two holes
hole_diam = 10.0 # Diameter of the through holes
cb_diam = 18.0   # Diameter of the counterbore (implied by visual appearance)
cb_depth = 4.0   # Depth of the counterbore

# Create the base plate
# We center it on the XY plane for easier hole placement
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_dist/2, 0), (hole_dist/2, 0)])
    .cboreHole(hole_diam, cb_diam, cb_depth)
)

# If the holes are simple through-holes instead of counterbored:
# result = (
#     cq.Workplane("XY")
#     .box(length, width, thickness)
#     .faces(">Z")
#     .workplane()
#     .pushPoints([(-hole_dist/2, 0), (hole_dist/2, 0)])
#     .hole(hole_diam)
# )

# The image shows what looks like a counterbore or countersink due to the internal shadow/rim.
# The code above uses cboreHole which matches the visual feature best.