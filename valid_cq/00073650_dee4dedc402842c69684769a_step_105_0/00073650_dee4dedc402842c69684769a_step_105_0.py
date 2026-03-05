import cadquery as cq

# Geometric Parameters
length = 600.0          # Total length of the bar
width = 15.0            # Width of the square profile
height = 15.0           # Height of the square profile
side_hole_dia = 6.0     # Diameter of the holes on the side face
end_hole_dia = 5.0      # Diameter of the holes on the ends
end_hole_depth = 20.0   # Depth of the blind holes on the ends
side_hole_offset = 25.0 # Distance from the end to the first side hole center

# 1. Create the base solid: A long rectangular bar aligned along the X-axis
result = cq.Workplane("XY").box(length, width, height)

# 2. Add Transverse Holes (through the side face)
# The image shows a hole near the left end and a hole in the center.
# Coordinates are relative to the face center.
side_hole_locations = [
    (-length / 2 + side_hole_offset, 0),  # Hole near the left end
    (0, 0)                                # Hole in the middle
]

result = (
    result
    .faces(">Z")           # Select the top face
    .workplane()
    .pushPoints(side_hole_locations)
    .hole(side_hole_dia)   # Cut through-holes
)

# 3. Add Longitudinal Holes (into the end faces)
# These appear to be blind holes (e.g., tapped holes) on the ends of the bar.
result = (
    result
    .faces(">X")           # Select the right end face
    .workplane()
    .hole(end_hole_dia, end_hole_depth)
    .faces("<X")           # Select the left end face
    .workplane()
    .hole(end_hole_dia, end_hole_depth)
)