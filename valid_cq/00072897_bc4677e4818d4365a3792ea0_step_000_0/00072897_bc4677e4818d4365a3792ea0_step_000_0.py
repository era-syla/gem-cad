import cadquery as cq

# Dimensions
plate_length = 100.0
plate_width = 24.0
plate_thickness = 3.0
boss_diameter = 12.0
boss_height = 6.0
hole_diameter = 5.5
cbore_diameter = 10.0
cbore_depth = 2.0
fillet_rad = 1.0

# Calculate spacing for the bosses (centered on the radius of the slot ends)
# For a slot, the center-to-center distance is length - width
c2c_distance = plate_length - plate_width
boss_locations = [
    (0, 0),                       # Center
    (c2c_distance / 2.0, 0),      # Top
    (-c2c_distance / 2.0, 0)      # Bottom
]

# 1. Create the base plate (Stadium/Slot shape)
# We start on the XY plane and extrude upwards
result = (
    cq.Workplane("XY")
    .slot2D(plate_length, plate_width)
    .extrude(plate_thickness)
)

# 2. Create the bosses on the back face
# We select the bottom face (<Z) and extrude cylinders downwards
# Note: In CadQuery, extruding from a face adds material in the normal direction.
# If we workplane on <Z, the normal is -Z.
result = (
    result.faces("<Z")
    .workplane()
    .pushPoints(boss_locations)
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
)

# 3. Create the central counterbored hole
# This feature is on the front face (>Z) and goes through the plate
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(0, 0)])
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)

# 4. Apply Fillets
# Fillet the main outer edge of the front face
result = result.faces(">Z").edges().fillet(fillet_rad)

# Fillet the tips of the bosses on the back side
result = result.faces("<Z").edges().fillet(fillet_rad * 0.5)