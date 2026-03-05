import cadquery as cq

# --- Model Parameters ---
total_length = 200.0      # Total length of the beam
beam_width = 20.0         # Width of the square arm profile
beam_height = 20.0        # Height of the square arm profile
hub_diameter = 32.0       # Diameter of the central hub
wall_thickness = 2.5      # Wall thickness for the hollow arms
rib_thickness = 3.0       # Thickness of the dividers between pockets
end_cap_thickness = 3.0   # Thickness of the solid end of the arm

# Hole Dimensions
center_bore = 10.0        # Main central hole diameter
mount_hole_dia = 3.5      # Hub mounting screw hole diameter
mount_hole_bcd = 22.0     # Bolt Circle Diameter for mounting holes
side_hole_dia = 5.0       # Diameter of holes on the side of the arms
end_hole_dia = 5.0        # Diameter of holes on the end caps

# --- Calculation of Internal Features ---
# Calculate arm length extending from the hub
arm_len_from_center = total_length / 2.0
# Calculate the space available for pockets (from hub edge to end cap)
available_pocket_len = (arm_len_from_center - (hub_diameter / 2.0)) - end_cap_thickness

# Determine pocket geometry (assume 3 pockets per side for this aspect ratio)
num_pockets = 3
# Calculate length of a single rectangular pocket based on available space and rib thickness
pocket_length = (available_pocket_len - (num_pockets - 1) * rib_thickness) / num_pockets
pocket_width = beam_width - (2 * wall_thickness)

# Calculate centers for the pockets along the X-axis
pocket_x_centers = []
start_offset = (hub_diameter / 2.0) + (pocket_length / 2.0)
for i in range(num_pockets):
    x_pos = start_offset + i * (pocket_length + rib_thickness)
    pocket_x_centers.append(x_pos)   # Right side
    pocket_x_centers.append(-x_pos)  # Left side

# --- Geometry Construction ---

# 1. Create the base solid: Central Hub + Rectangular Beam
hub = cq.Workplane("XY").circle(hub_diameter / 2.0).extrude(beam_height)
beam = cq.Workplane("XY").rect(total_length, beam_width).extrude(beam_height)
body = hub.union(beam)

# 2. Cut Rectangular Pockets (Top to Bottom)
# We create a sketch on the top face and cut through to the bottom
# effectively creating the "ladder" structure with side walls.
pockets = (
    cq.Workplane("XY")
    .workplane(offset=beam_height)
    .pushPoints([(x, 0) for x in pocket_x_centers])
    .rect(pocket_length, pocket_width)
    .extrude(-beam_height - 1.0) # Cut entirely through
)
body = body.cut(pockets)

# 3. Drill Side Holes
# These holes go through the side walls, aligned with the center of each pocket.
side_holes = (
    cq.Workplane("XZ") # Side plane
    .workplane(offset=beam_width / 2.0 + 1.0) # Offset to start cut from outside
    .pushPoints([(x, beam_height / 2.0) for x in pocket_x_centers]) # Centered vertically
    .circle(side_hole_dia / 2.0)
    .extrude(-beam_width - 2.0) # Cut through both walls
)
body = body.cut(side_holes)

# 4. Drill End Holes
# Holes on the longitudinal ends of the beam
end_holes_right = (
    cq.Workplane("YZ")
    .workplane(offset=total_length / 2.0 + 1.0)
    .pushPoints([(0, beam_height / 2.0)])
    .circle(end_hole_dia / 2.0)
    .extrude(-end_cap_thickness * 3) # Cut into the last pocket
)
end_holes_left = (
    cq.Workplane("YZ")
    .workplane(offset=-total_length / 2.0 - 1.0)
    .pushPoints([(0, beam_height / 2.0)])
    .circle(end_hole_dia / 2.0)
    .extrude(end_cap_thickness * 3)
)
body = body.cut(end_holes_right).cut(end_holes_left)

# 5. Machine Hub Features
# Central Bore
body = body.faces(">Z").workplane().circle(center_bore / 2.0).cutThruAll()

# Mounting Holes (4 holes on a bolt circle)
body = (
    body.faces(">Z").workplane()
    .polarArray(mount_hole_bcd / 2.0, 0, 360, 4)
    .circle(mount_hole_dia / 2.0)
    .cutThruAll()
)

# Assign final object to result variable
result = body