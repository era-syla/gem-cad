import cadquery as cq

# --- Parametric Variables ---
base_diameter = 40.0
base_height = 20.0
top_taper_height = 15.0
top_diameter = 30.0  # Diameter at the very top of the frustum
scoop_radius = 12.0   # Radius of the sphere used for the side cutouts
scoop_offset_z = 30.0 # Vertical position of the scoop center (relative to bottom)
scoop_offset_r = 15.0 # Radial offset for the scoop cut

center_hole_dia = 5.0
side_hole_dia = 3.0
side_hole_pattern_radius = 8.0

pin_diameter = 3.0
pin_length = 60.0
pin_offset_x = 40.0 # Distance to place the pin away from the main body

# --- Main Body Construction ---

# 1. Base Cylinder
# Start with the bottom cylindrical section
main_body = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_height)

# 2. Tapered Top Section (Frustum)
# Create a workplane on top of the base and loft to a smaller circle
# Note: CadQuery's extrude with taper can be tricky, so lofting is often safer for frustums
# or simply adding a cone. Let's use a cone approach relative to the top face.
tapered_section = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(base_diameter / 2.0)
    .workplane(offset=top_taper_height)
    .circle(top_diameter / 2.0)
    .loft(combine=True)
)

# Combine base and taper
# Since I started a new chain for the loft, let's just make the cone directly 
# and union it to the base to be cleaner.
cone = cq.Solid.makeCone(
    base_diameter / 2.0, 
    top_diameter / 2.0, 
    top_taper_height
).translate((0, 0, base_height))

main_body = main_body.union(cone)

# 3. Scoop Cutouts
# We need 4 spherical cuts around the perimeter.
# We create a sphere and rotate/cut it 4 times.
scoop_tool = cq.Workplane("XZ").sphere(scoop_radius)

for i in range(4):
    # Calculate position for the scoop
    angle = 90 * i
    
    # We position the sphere. It needs to cut into the tapered edge.
    # It sits high up (near the top face) and outwards.
    cutter = (
        scoop_tool
        .translate((scoop_offset_r, 0, scoop_offset_z))
        .rotate((0,0,0), (0,0,1), angle)
    )
    main_body = main_body.cut(cutter)

# 4. Holes
# Center Hole (goes all the way through or deep enough)
main_body = (
    main_body.faces(">Z")
    .workplane()
    .hole(center_hole_dia, depth=base_height + top_taper_height) # Through hole
)

# 4 small holes in a pattern
main_body = (
    main_body.faces(">Z")
    .workplane()
    .polarArray(side_hole_pattern_radius, 0, 360, 4)
    .hole(side_hole_dia, depth=10.0) # Assume blind holes
)

# 5. Bottom Nub (small protrusion visible at the very bottom center in the image)
bottom_nub = (
    main_body.faces("<Z")
    .workplane()
    .circle(5.0)
    .extrude(2.0)
)
main_body = main_body.union(bottom_nub)


# --- Pin Construction ---
pin = (
    cq.Workplane("XY")
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
    .translate((pin_offset_x, 0, 0))
)

# --- Final Assembly ---
result = main_body.union(pin)