import cadquery as cq

# --- Parameters ---
height = 200.0          # Total height of the post
tube_od = 50.0          # Outer diameter of the main tube
tube_id = 42.0          # Inner diameter (wall thickness 4mm)
flange_od = 72.0        # Diameter of the top flange
flange_height = 14.0    # Height of the top flange
scoop_len = 45.0        # Length of the bottom horizontal extension
hole_dia = 3.5          # Diameter of the mounting holes

# Derived dimensions
tube_rad = tube_od / 2.0
inner_rad = tube_id / 2.0
scoop_axis_z = tube_rad # Center axis of horizontal scoop is one radius up

# --- 1. Main Vertical Body ---
# Create the main vertical cylinder
main_tube = cq.Workplane("XY").circle(tube_rad).extrude(height)

# --- 2. Bottom Horizontal Feature (Scoop) ---
# Create a cylinder oriented along the X-axis
# We extrude it and then cut it in half to form the "U" shape channel
# Positioned so it intersects the main tube at the bottom
scoop_full = (cq.Workplane("YZ", origin=(0, 0, scoop_axis_z))
              .circle(tube_rad)
              .extrude(-(tube_rad + scoop_len)) # Extrude along -X
              )

# Cut the top half of the horizontal cylinder
# We remove everything above the centerline (Z > scoop_axis_z)
cutter_box = (cq.Workplane("XY", origin=(0, 0, scoop_axis_z))
              .rect(500, 500)
              .extrude(200)
              )
scoop_half = scoop_full.cut(cutter_box)

# Union the scoop with the main tube
body = main_tube.union(scoop_half)

# --- 3. Top Flange ---
# Create the flared top section
# We create a ring and fillet the edges to simulate the rounded profile
flange = (cq.Workplane("XY", origin=(0, 0, height - flange_height))
          .circle(flange_od / 2.0)
          .extrude(flange_height)
          )

# Apply fillets for smooth look
flange = flange.edges(">Z").fillet(flange_height * 0.4) # Round top heavily
flange = flange.edges("<Z").fillet(2.0)                 # Blend to tube

# Union the flange to the body
body = body.union(flange)

# --- 4. Hollow Out (Shelling) ---
# Create a negative volume representing the inner space
# Inner vertical cylinder
core_vertical = cq.Workplane("XY").circle(inner_rad).extrude(height + 10)

# Inner horizontal scoop
core_scoop_full = (cq.Workplane("YZ", origin=(0, 0, scoop_axis_z))
                   .circle(inner_rad)
                   .extrude(-(tube_rad + scoop_len))
                   )
core_scoop_half = core_scoop_full.cut(cutter_box)

# Union the cores
core = core_vertical.union(core_scoop_half)

# Cut the core from the main body
result = body.cut(core)

# --- 5. Details: Holes ---
# Helper function to create radial holes perpendicular to the tube surface
def add_radial_hole(part, z_pos, angle_deg, diameter):
    # Create a cutting cylinder oriented correctly
    # Rotate workplane to correct angle around Z, move to surface, point inward
    hole_cutter = (cq.Workplane("XY", origin=(0, 0, z_pos))
                   .rotate((0, 0, 0), (0, 0, 1), angle_deg)
                   .workplane(offset=tube_od) # Move well outside
                   .rotate((0, 0, 0), (1, 0, 0), -90) # Point towards center
                   .circle(diameter / 2.0)
                   .extrude(tube_od * 1.5) # Cut through
                   )
    return part.cut(hole_cutter)

# Add holes based on image (Scoop is along -X)
# Holes appear on the side faces (approx -Y axis direction in image)
# Upper hole
result = add_radial_hole(result, height * 0.65, -90, hole_dia)

# Lower holes (two holes near the bottom)
result = add_radial_hole(result, height * 0.15, -70, hole_dia)
result = add_radial_hole(result, height * 0.15, -110, hole_dia)

# --- 6. Details: Notch ---
# Add a small notch at the tip of the scoop
notch_width = 6.0
notch_depth = 5.0
tip_x = -(tube_rad + scoop_len)

notch_cutter = (cq.Workplane("XY", origin=(tip_x + notch_depth/2, 0, 0))
                .rect(notch_depth, notch_width)
                .extrude(tube_od)
                )

result = result.cut(notch_cutter)

# Export or Render
if 'show_object' in globals():
    show_object(result)