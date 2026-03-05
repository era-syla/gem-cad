import cadquery as cq

# Define the parametric dimensions
total_length = 130.0
tower_height = 45.0
tower_start = 15.0
tower_end = 65.0
width = 25.0
wall_thickness = 3.0

# Define the points for the side profile (XZ plane)
# This captures the silhouette: front nose, high tower, tapered tail, and curved bottom.
profile_pts = [
    (0, 0),                      # Bottom-front
    (0, 25),                     # Front face top
    (tower_start, 25),           # Step inward
    (tower_start, tower_height), # Tower front vertical
    (tower_end, tower_height),   # Tower roof
    (tower_end, 28),             # Tower back drop
    (total_length, 18),          # Tail top slope
    (total_length + 5, 12),      # Tail tip
    (total_length, 10),          # Tail bottom
    (70, 5),                     # Bottom curve inflection
    (30, 0),                     # Bottom return
    (0, 0)                       # Close loop
]

# 1. Create the main solid body
# Extrude along Y to create the depth of the part
main_body = cq.Workplane("XZ").polyline(profile_pts).close().extrude(width)

# 2. Create the internal cavity (Hollow out)
# We select the face at Y=0 (front relative to screen) and cut inwards 
# to create the "section cut" appearance showing the interior walls.
# offset2D is used to create a uniform wall thickness profile.
cavity = (
    main_body.faces("<Y")
    .workplane()
    .polyline(profile_pts)
    .close()
    .offset2D(-wall_thickness)
    .extrude(width - wall_thickness, combine="cut")
)

# 3. Add the front protruding detail (Nose Boss)
# A blocky feature extending from the front face (-X)
nose_boss = (
    cq.Workplane("YZ")
    .workplane(offset=0)  # Plane at X=0
    .center(width / 2, 12.5)   # Center relative to the face
    .rect(width * 0.6, 15)     # Dimensions of the boss
    .extrude(-8)               # Extrude outwards (negative X)
)

# Combine the boss with the main hollow body
result = cavity.union(nose_boss)

# 4. Add subtle detailing
# Chamfer the top edge of the tower for a machined look
result = result.edges(">Z").chamfer(1.0)

# Optional: Add side ribs/gussets at the bottom-rear transition
rib_shape = [
    (0, 0), (10, 0), (0, 10)
]
rib = (
    cq.Workplane("YZ")
    .workplane(offset=tower_end) # Position at the back of the tower
    .polyline(rib_shape).close()
    .extrude(5)
    .translate((0, width - 5, 5)) # Position on the far side
)

result = result.union(rib)

# Return the final geometry
# result is the variable containing the CadQuery solid