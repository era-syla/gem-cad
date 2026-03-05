import cadquery as cq

# Parameters used for defining dimensions
base_width = 40.0
base_length = 80.0
base_height = 5.0

# Main body (Nave)
nave_width = 32.0
nave_length = 50.0
nave_height_walls = 35.0
nave_roof_height = 15.0  # Height of the triangular part of the roof

# Apse (semi-circular part at the back)
apse_radius = nave_width / 2.0
apse_height = nave_height_walls

# Tower (Steeple)
tower_base_width = 25.0
tower_base_length = 25.0
tower_base_height = 60.0
spire_height = 50.0
spire_base_width = tower_base_width + 4.0 # Slight overhang/flare at the transition

# --- Construction ---

# 1. Base Plate
# The base roughly follows the contour of the building but is slightly larger.
# We'll build it as a rectangle + semi-circle, then union.
base_rect = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height)
    .translate((base_length/2 - 10, 0, base_height/2)) # Shift to align roughly
)

base_circle = (
    cq.Workplane("XY")
    .cylinder(base_height, base_width/2)
    .translate((-10, 0, base_height/2)) # Shift to the back
)

base_tower = (
    cq.Workplane("XY")
    .box(tower_base_length + 4, tower_base_width + 4, base_height)
    .translate((base_length - 10, 0, base_height/2))
)

base = base_rect.union(base_circle).union(base_tower)


# 2. The Nave (Main Hall)
# Rectangular body with a pitched roof.
# Create the profile on the YZ plane and extrude along X.
pts_nave = [
    (nave_width/2, 0),
    (nave_width/2, nave_height_walls),
    (0, nave_height_walls + nave_roof_height),
    (-nave_width/2, nave_height_walls),
    (-nave_width/2, 0)
]

nave = (
    cq.Workplane("YZ")
    .polyline(pts_nave)
    .close()
    .extrude(nave_length)
    .translate((0, 0, base_height)) # Sit on top of base
)


# 3. The Apse (Rear semi-circle)
# A cylinder merged into the back of the nave.
# It usually has a conical or domed roof, but in the image, the roof looks 
# like a continuation of the nave roof but rounded, or a half-cone.
# Let's approximate the image: simple cylinder for walls, half-cone for roof.

apse_cylinder = (
    cq.Workplane("XY")
    .cylinder(nave_height_walls, apse_radius)
    .translate((-10, 0, base_height + nave_height_walls/2)) # -10 seems to be the visual offset
)

# For the apse roof, we can revolve a profile or use a loft.
# A simple way is a revolution of the roof slope.
apse_roof_profile = [
    (0, nave_height_walls + nave_roof_height),
    (apse_radius, nave_height_walls),
    (0, nave_height_walls) # Closing the triangle
]

apse_roof = (
    cq.Workplane("YZ")
    .polyline(apse_roof_profile)
    .close()
    .revolve(180, (0,0,0), (0,1,0)) # Revolve around Z axis (which is Y in this plane sketch)
    .rotate((0,0,0), (1,0,0), -90) # Rotate to upright
    .rotate((0,0,0), (0,0,1), 90) # Rotate to face back
    .translate((-10, 0, base_height))
)

apse = apse_cylinder.union(apse_roof)


# 4. The Tower
# Square base
tower_x_pos = nave_length - 5 # Position at the front of the nave

tower_body = (
    cq.Workplane("XY")
    .box(tower_base_length, tower_base_width, tower_base_height)
    .translate((tower_x_pos, 0, base_height + tower_base_height/2))
)

# 5. The Spire
# The image shows a transition (chamfered block) then an octagonal or faceted spire.
# Let's create a transition block that tapers slightly out, then the tall spire.

transition_height = 8.0
transition_width = tower_base_width + 4.0

# Create a loft for the transition from square tower to the base of the spire
# Actually, looking closely, it looks like a small pyramid section that flares out slightly.
transition = (
    cq.Workplane("XY")
    .rect(tower_base_length, tower_base_width)
    .workplane(offset=transition_height)
    .rect(transition_width, transition_width)
    .loft(combine=True)
    .translate((tower_x_pos, 0, base_height + tower_base_height))
)

# The sharp spire. It looks like an 8-sided (octagonal) pyramid.
spire_start_height = base_height + tower_base_height + transition_height

spire = (
    cq.Workplane("XY")
    .workplane(offset=spire_start_height)
    .polygon(8, transition_width) # Base of spire
    .workplane(offset=spire_height)
    .polygon(8, 0.1) # Tip of spire (almost 0 size)
    .loft()
    .translate((tower_x_pos, 0, 0))
)


# Combine all parts
result = base.union(nave).union(apse).union(tower_body).union(transition).union(spire)

# Export to STEP (optional, for verification)
# cq.exporters.export(result, "church.step")