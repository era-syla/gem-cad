import cadquery as cq

# Parameters for the model dimensions
length = 100.0
outer_radius = 30.0
inner_radius = 20.0
wall_thickness = outer_radius - inner_radius
# Fillet radius set slightly less than half thickness to ensure geometric validity
end_fillet_radius = (wall_thickness / 2.0) - 0.1 

boss_size = 10.0      # Size of the square protrusion
boss_height = 6.0     # How far it sticks out from the cylinder surface
boss_position = 15.0  # Distance from the flat end
boss_hole_diam = 4.0  # Diameter of the hole in the boss

# 1. Create the main hollow cylinder (Tube)
# Aligned along the X-axis
result = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(length)
)

# 2. Create the rounded end
# Select the face at the far end (max X) and fillet both its inner and outer edges
result = (
    result
    .faces(">X")
    .edges()
    .fillet(end_fillet_radius)
)

# 3. Create the Side Boss
# We create a workplane parallel to XZ, offset to the surface of the cylinder.
# To ensure a clean boolean union without gaps, we start the sketch slightly 
# inside the cylinder wall (overlap).
overlap = 2.0
plane_offset = -(outer_radius - overlap) # Negative Y direction (Front side)

boss_geo = (
    cq.Workplane("XZ")
    .workplane(offset=plane_offset)
    .center(boss_position, 0)  # Position along X (length) and Z (vertical)
    .rect(boss_size, boss_size)
    .extrude(-(boss_height + overlap)) # Extrude outwards (negative Y)
)

# 4. Create the hole in the boss
# Select the outermost face of the boss geometry (lowest Y value)
boss_geo = (
    boss_geo
    .faces("<Y")
    .workplane()
    .circle(boss_hole_diam / 2.0)
    .cutBlind(boss_height + overlap) # Cut back through the boss
)

# 5. Combine the main body and the boss
result = result.union(boss_geo)