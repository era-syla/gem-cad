import cadquery as cq

# Parametric dimensions
plate_size = 100.0        # Outer width/length of the base plate
plate_thickness = 10.0    # Thickness of the base plate
hole_diameter = 6.0       # Diameter of the mounting holes
hole_inset = 10.0         # Distance from edge to hole center
inner_opening = 60.0      # Size of the central square hole
rim_width = 5.0           # Thickness of the raised rim wall
rim_height = 5.0          # Height of the rim above the plate

# Derived dimensions
hole_spacing = plate_size - (2 * hole_inset)
rim_outer_size = inner_opening + (2 * rim_width)

# 1. Create the base plate
base = cq.Workplane("XY").box(plate_size, plate_size, plate_thickness)

# 2. Create the raised rim
# We create a sketch or a smaller box on top of the base
rim = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness / 2) # Start on top of the base
    .box(rim_outer_size, rim_outer_size, rim_height, centered=(True, True, False))
)

# Combine base and rim
part = base.union(rim)

# 3. Cut the central square opening
# We cut through the entire object (plate + rim)
result = (
    part.faces(">Z")
    .workplane()
    .rect(inner_opening, inner_opening)
    .cutThruAll()
)

# 4. Add the mounting holes
# There are 8 holes visible: 4 corners + 4 midpoints
# We can define their positions relative to the center

# Corner positions
corners = [
    (hole_spacing/2, hole_spacing/2),
    (hole_spacing/2, -hole_spacing/2),
    (-hole_spacing/2, hole_spacing/2),
    (-hole_spacing/2, -hole_spacing/2),
]

# Midpoint positions
midpoints = [
    (0, hole_spacing/2),
    (0, -hole_spacing/2),
    (hole_spacing/2, 0),
    (-hole_spacing/2, 0),
]

all_hole_positions = corners + midpoints

result = (
    result.faces(">Z") # Select top face of the rim (or plate, z-position matters less for cutThruAll)
    .workplane()
    .pushPoints(all_hole_positions)
    .hole(hole_diameter)
)

# Optional: Fillet the transition between the rim and the plate for better realism
# Selecting the edge at the base of the rim
# This step requires careful edge selection. Let's find edges on the plate top face 
# that belong to the rim base.
try:
    result = result.faces(cq.NearestToPointSelector((0, 0, plate_thickness/2))).edges().fillet(2.0)
except:
    # If selection fails, return the unfilleted result (robustness)
    pass