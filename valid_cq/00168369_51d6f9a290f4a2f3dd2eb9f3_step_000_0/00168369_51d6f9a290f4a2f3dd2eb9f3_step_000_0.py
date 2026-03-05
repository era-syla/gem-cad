import cadquery as cq

# Parametric dimensions
total_length = 120.0    # Total length of the object along X
height = 30.0           # Height of the object along Z
spine_width = 15.0      # Width of the central beam along Y
rib_width = 45.0        # Total width of the transverse ribs along Y
rib_thickness = 15.0    # Thickness of the ribs along X

# Create the central spine (the long connecting beam)
# Centered at the origin
spine = cq.Workplane("XY").box(total_length, spine_width, height)

# Calculate the positions for the ribs
# We need one in the center, and one at each end (flush with the spine ends)
end_offset = (total_length / 2.0) - (rib_thickness / 2.0)
rib_locations = [(-end_offset, 0), (0, 0), (end_offset, 0)]

# Create the ribs
# pushPoints places a workplane context at each specified location
# box creates a solid at each of those locations
ribs = (
    cq.Workplane("XY")
    .pushPoints(rib_locations)
    .box(rib_thickness, rib_width, height)
)

# Combine the spine and the ribs into the final part
result = spine.union(ribs)