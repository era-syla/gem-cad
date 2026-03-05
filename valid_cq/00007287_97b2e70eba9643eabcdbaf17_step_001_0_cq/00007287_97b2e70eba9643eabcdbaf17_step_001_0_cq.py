import cadquery as cq

# --- Parametric Dimensions ---
# Standard bearing dimensions (e.g., 608 bearing often used in skates/3D printers)
# Dimensions: 8mm ID x 22mm OD x 7mm Width
id_diam = 8.0          # Inner Diameter
od_diam = 22.0         # Outer Diameter
width = 7.0            # Width of the bearing
seal_recess = 0.5      # Depth of the seal from the face
seal_gap = 0.5         # Gap between inner/outer race for the seal area

# Derived dimensions
id_rad = id_diam / 2.0
od_rad = od_diam / 2.0
w_half = width / 2.0

# Race Thickness estimations
outer_race_thickness = (od_rad - id_rad) * 0.25
inner_race_thickness = (od_rad - id_rad) * 0.25

outer_race_id = od_rad - outer_race_thickness
inner_race_od = id_rad + inner_race_thickness

# Ball parameters
ball_diam = (outer_race_id - inner_race_od) * 0.9  # Balls fit in the gap
ball_rad = ball_diam / 2.0
pitch_radius = (outer_race_id + inner_race_od) / 2.0
num_balls = 7

# --- Modeling ---

# 1. Outer Race
# Profile: Rectangle with a groove for balls and small chamfers/fillets
outer_race_prof = (
    cq.Workplane("XZ")
    .moveTo(od_rad, w_half)
    .lineTo(outer_race_id, w_half)
    .lineTo(outer_race_id, -w_half)
    .lineTo(od_rad, -w_half)
    .close()
)

# Add groove to outer race (cut)
groove_outer = (
    cq.Workplane("XZ")
    .moveTo(pitch_radius, 0)
    .circle(ball_rad * 1.05) # Slight clearance
)

outer_race = outer_race_prof.revolve().cut(groove_outer.revolve())

# Add slight chamfers to outer edges of outer race
outer_race = outer_race.edges(
    cq.selectors.SumSelector(
        cq.selectors.RadiusNthSelector(0), # Inner edges
        cq.selectors.RadiusNthSelector(1)  # Outer edges
    )
).fillet(0.2)


# 2. Inner Race
inner_race_prof = (
    cq.Workplane("XZ")
    .moveTo(inner_race_od, w_half)
    .lineTo(id_rad, w_half)
    .lineTo(id_rad, -w_half)
    .lineTo(inner_race_od, -w_half)
    .close()
)

# Add groove to inner race
groove_inner = (
    cq.Workplane("XZ")
    .moveTo(pitch_radius, 0)
    .circle(ball_rad * 1.05)
)

inner_race = inner_race_prof.revolve().cut(groove_inner.revolve())

# Add slight chamfers to edges of inner race
inner_race = inner_race.edges(
    cq.selectors.SumSelector(
        cq.selectors.RadiusNthSelector(0), 
        cq.selectors.RadiusNthSelector(1)
    )
).fillet(0.2)


# 3. Balls
single_ball = cq.Workplane("XY").moveTo(pitch_radius, 0).sphere(ball_rad)
balls = single_ball
for i in range(1, num_balls):
    angle = 360.0 / num_balls * i
    balls = balls.union(
        single_ball.rotate((0,0,0), (0,0,1), angle)
    )

# 4. Seals (The flat rings visible in the image between races)
# The image shows a seal that is recessed slightly.
seal_outer_rad = outer_race_id - 0.2 # Small clearance from outer race
seal_inner_rad = inner_race_od + 0.2 # Small clearance from inner race
seal_thickness = 0.5 

seal_profile = (
    cq.Workplane("XY")
    .circle(seal_outer_rad)
    .circle(seal_inner_rad)
    .extrude(seal_thickness)
)

# Position seals on top and bottom, recessed
top_seal = seal_profile.translate((0, 0, w_half - seal_thickness - 0.2))
bottom_seal = seal_profile.translate((0, 0, -(w_half - 0.2)))

# --- Assembly ---
result = outer_race.union(inner_race).union(balls).union(top_seal).union(bottom_seal)

# Optional: Add small fillets to the seal edges for realism as seen in the render
# This can be computationally expensive, so it's kept simple here.