import cadquery as cq

# Parametric Dimensions
base_diameter = 150.0   # Diameter of the circular base
base_thickness = 5.0    # Thickness of the base plate
rod_diameter = 2.0      # Diameter of the vertical rod
rod_height = 200.0      # Height of the rod
rod_offset = 60.0       # Distance from center to rod (approximate based on image)

# Hole pattern parameters
hole_diameter = 3.0     # Diameter of the small mounting holes
hole_circle_dia = 140.0 # Diameter of the circle on which holes are placed
# Angle positions for the hole pairs (visual estimation)
hole_angles = [15, 30, 195, 210, 345] 

# Create the Base
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_thickness)

# Create the Rod
# The rod is positioned offset from the center
rod = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness) # Start on top of the base
    .center(0, rod_offset)            # Move to the rod position
    .circle(rod_diameter / 2)
    .extrude(rod_height)
)

# Create the Holes
# Using a polar array logic or manual placement based on angles
holes = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .polarArray(hole_circle_dia / 2, 0, 360, 1) # Dummy start for individual pushes
)

# Creating a list of locations for the holes based on polar coordinates
hole_locs = []
import math
for angle in hole_angles:
    rad = math.radians(angle)
    x = (hole_circle_dia / 2) * math.cos(rad)
    y = (hole_circle_dia / 2) * math.sin(rad)
    hole_locs.append((x, y))

# Cut the holes through the base
base_with_holes = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_locs)
    .hole(hole_diameter)
)

# Combine the base and the rod
result = base_with_holes.union(rod)