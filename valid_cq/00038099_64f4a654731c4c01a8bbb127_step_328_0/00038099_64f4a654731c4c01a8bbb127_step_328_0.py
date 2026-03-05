import cadquery as cq

# ==========================================
# Parameters for the 5-Hole Technic Beam
# ==========================================
num_holes = 5
pitch = 8.0             # Distance between hole centers
beam_width = 7.4        # Width of the beam (diameter of rounded ends)
thickness = 7.8         # Thickness of the beam
hole_diam = 4.8         # Diameter of the through-holes
cb_diam = 6.2           # Diameter of the counterbore
cb_depth = 0.85         # Depth of the counterbore

# ==========================================
# Geometry Generation
# ==========================================

# Calculate the length between the centers of the first and last holes
length_centers = (num_holes - 1) * pitch

# 1. Create the base shape (Stadium/Slot profile)
# Constructed by unioning a central rectangular section with cylinders at the ends
center_section = cq.Workplane("XY").box(length_centers, beam_width, thickness)

end_caps = (
    cq.Workplane("XY")
    .pushPoints([(-length_centers / 2, 0), (length_centers / 2, 0)])
    .cylinder(thickness, beam_width / 2)
)

# Combine into the main solid body
beam_body = center_section.union(end_caps)

# 2. Define the locations for the holes
# Points are calculated relative to the center of the beam (0,0)
hole_locations = [
    (-length_centers / 2 + i * pitch, 0) 
    for i in range(num_holes)
]

# 3. Create the counterbored holes
# Select the top face, move to hole locations, and cut counterbored holes
result = (
    beam_body
    .faces(">Z")
    .workplane()
    .pushPoints(hole_locations)
    .cboreHole(hole_diam, cb_diam, cb_depth)
)