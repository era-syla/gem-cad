import cadquery as cq

# --- Parameters ---
flange_diameter = 56.0
flange_thickness = 3.5
housing_depth = 24.0
housing_radius = 24.0
flat_face_offset = 14.0  # Distance from center to the flat front face
wall_thickness = 2.5
floor_thickness = 3.0
latch_width = 11.0
latch_height = 15.0
latch_protrusion = 12.0

# --- 1. Main Body (Flange + Housing) ---

# Create the top circular flange
flange = (cq.Workplane("XY")
          .circle(flange_diameter / 2.0)
          .extrude(flange_thickness)
          .edges(">Z").fillet(1.5)  # Soften top edge
          )

# Create the main housing body (Cylinder with a flat face)
# Start with a cylinder extending downwards
housing_cyl = (cq.Workplane("XY")
               .workplane(offset=-housing_depth)
               .circle(housing_radius)
               .extrude(housing_depth)
               )

# Create a cutter box to flatten one side of the cylinder
cutter_box = (cq.Workplane("XY")
              .workplane(offset=-housing_depth)
              .center(flat_face_offset, 0)
              .box(housing_radius * 2, housing_radius * 3, housing_depth * 2, 
                   centered=(False, True, True))
              )

# Cut the housing and fillet the transition edges
housing = housing_cyl.cut(cutter_box)
housing = housing.edges("|Z").fillet(3.0)

# Union flange and housing
body = flange.union(housing)

# --- 2. Internal Recess (The "Cup") ---

# Calculate pocket dimensions
pocket_radius = housing_radius - wall_thickness
pocket_total_depth = housing_depth + flange_thickness - floor_thickness
pocket_flat_wall_x = flat_face_offset - wall_thickness

# Create the basic cylindrical pocket shape
pocket_cyl = (cq.Workplane("XY")
              .workplane(offset=flange_thickness)
              .circle(pocket_radius)
              .extrude(-pocket_total_depth)
              )

# Trim the pocket to match the D-shape of the housing (preserving wall thickness)
pocket_trimmer = (cq.Workplane("XY")
                  .workplane(offset=-housing_depth)
                  .center(pocket_flat_wall_x, 0)
                  .box(50, 60, 50, centered=(False, True, True))
                  )
pocket_shape = pocket_cyl.cut(pocket_trimmer)

# Cut the pocket from the main body
body = body.cut(pocket_shape)

# --- 3. Latch Mechanism Opening ---

latch_z_pos = -housing_depth / 2.0 + 2.0

# Cut the rectangular hole for the latch bolt
latch_hole = (cq.Workplane("YZ")
              .workplane(offset=flat_face_offset)
              .center(0, latch_z_pos)
              .rect(latch_width, latch_height)
              .extrude(-10)  # Cut inwards into the housing
              )
body = body.cut(latch_hole)

# --- 4. The Handle / Paddle ---

handle_top_z = flange_thickness - 2.5
handle_thick = 5.0
handle_gap = 0.5

# Create the paddle shape
paddle = (cq.Workplane("XY")
          .workplane(offset=handle_top_z - handle_thick)
          .circle(pocket_radius - handle_gap)
          .extrude(handle_thick)
          )

# Trim paddle to D-shape
paddle = paddle.cut(pocket_trimmer.translate((handle_gap, 0, 0)))

# Create the finger scoop (recess)
scoop = (cq.Workplane("XY")
         .workplane(offset=handle_top_z + 12)  # Position sphere center high up
         .center(-8, 0)  # Offset towards the back
         .sphere(18)
         )
paddle = paddle.cut(scoop)

# Create a center post to connect paddle to the floor (simulating the mechanism axis)
pivot_post = (cq.Workplane("XY")
              .workplane(offset=handle_top_z - handle_thick)
              .center(-2, 0)
              .rect(8, 20)
              .extrude(-(pocket_total_depth - (flange_thickness - handle_top_z)))
              )

# Combine handle parts and add to body
paddle_assembly = paddle.union(pivot_post)
body = body.union(paddle_assembly)

# --- 5. Latch Bolt ---

# Create the bolt body protruding from the flat face
bolt = (cq.Workplane("YZ")
        .workplane(offset=flat_face_offset)
        .center(0, latch_z_pos)
        .rect(latch_width - 0.5, latch_height - 0.5)
        .extrude(latch_protrusion)
        )

# Create the ramp/wedge shape on the bolt tip
# Chamfer the bottom-outer edge
bolt = bolt.faces(">X").edges("<Z").chamfer(latch_protrusion * 0.7, latch_protrusion * 0.5)

# Add bolt to the main assembly
body = body.union(bolt)

# --- 6. Mounting Bosses ---

# Add screw bosses on the bottom
boss_locations = [(-12, 14), (-12, -14)]
for x, y in boss_locations:
    boss = (cq.Workplane("XY")
            .workplane(offset=-housing_depth)
            .center(x, y)
            .circle(3.5)
            .extrude(6.0)
            )
    body = body.union(boss)

# Final Result
result = body