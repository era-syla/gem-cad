import cadquery as cq

# --- Parameters ---
outer_radius = 50.0
inner_radius = 25.0
total_height = 40.0
wall_thickness = 2.0
vane_count = 16

# Top Cover Parameters
cover_height = 15.0
slot_width = 15.0  # Width of the cutout in the top cover

# Base/Vane Parameters
base_height = total_height - cover_height
central_hub_radius = inner_radius - 0.5 # Slightly smaller to fit inside top hole if needed, or same size
hub_thickness = 3.0
hub_hole_dia = 3.0

# --- Geometry Construction ---

# 1. Create the Base (Bottom Part with Vanes)

# Start with the outer shell cylinder
base_outer = cq.Workplane("XY").circle(outer_radius).extrude(base_height)
base_inner_cut = cq.Workplane("XY").circle(outer_radius - wall_thickness).extrude(base_height)
base_shell = base_outer.cut(base_inner_cut)

# Create the inner hub shell
hub_outer = cq.Workplane("XY").circle(inner_radius + wall_thickness).extrude(base_height)
hub_inner_cut = cq.Workplane("XY").circle(inner_radius).extrude(base_height)
hub_shell = hub_outer.cut(hub_inner_cut)

# Combine shells to form the annular container
base_container = base_shell.union(hub_shell)

# Create the Vanes
# A single vane is a thin box positioned radially
vane_length = (outer_radius - wall_thickness) - (inner_radius + wall_thickness)
single_vane = (
    cq.Workplane("XY")
    .box(vane_length, wall_thickness, base_height, centered=(True, True, False))
    .translate(((inner_radius + wall_thickness + vane_length/2), 0, 0))
)

# Rotate and duplicate the vanes
vanes = single_vane
for i in range(1, vane_count):
    angle = 360.0 / vane_count * i
    vanes = vanes.union(single_vane.rotate((0, 0, 0), (0, 0, 1), angle))

# Create the central disc (the floor for the inner mechanism or mount)
central_hub = (
    cq.Workplane("XY")
    .workplane(offset=base_height - hub_thickness) # Positioned near top of base
    .circle(inner_radius + wall_thickness) # Slightly overlapping inner wall
    .extrude(hub_thickness)
)

# Add small mounting holes to the central hub
mounting_holes = (
    central_hub.faces(">Z")
    .workplane()
    .pushPoints([(5, 0), (-5, 0)]) # Arbitrary position based on image
    .hole(hub_hole_dia)
)

# Combine all base components
base_assembly = base_container.union(vanes).union(mounting_holes)


# 2. Create the Top Cover

# Main body of the cover
cover_outer = cq.Workplane("XY").workplane(offset=base_height + 5).circle(outer_radius).extrude(cover_height)
cover_inner_cut = cq.Workplane("XY").workplane(offset=base_height + 5).circle(outer_radius - wall_thickness).extrude(cover_height - wall_thickness)
cover_center_hole = cq.Workplane("XY").workplane(offset=base_height + 5).circle(inner_radius).extrude(cover_height)

cover_body = cover_outer.cut(cover_inner_cut).cut(cover_center_hole)

# Create the rectangular cutout slot on the top surface
# We create a shape to cut through the top face
cutout_shape = (
    cq.Workplane("XY")
    .workplane(offset=base_height + 5 + cover_height - wall_thickness * 1.5) # Position near top face
    .rect(outer_radius * 2, slot_width) # Long rectangle
    .extrude(wall_thickness * 3) # Cut through top thickness
    .rotate((0,0,0), (0,0,1), 25) # Angle slightly to match image perspective
)

# To limit the cut to just one section, we can intersect or use logic, 
# but a simpler way for the image match is a pie slice or restricted box.
# Let's use a sector cut approach for a cleaner "window".
# Alternatively, based on the image, it looks like a simple rectangular hole 
# extending radially.

# Let's refine the cutout to be a radial slot
slot_cut = (
     cq.Workplane("XY")
    .workplane(offset=base_height + 5 + cover_height - 5) # Start above
    .moveTo((inner_radius + outer_radius)/2, 0)
    .rect((outer_radius - inner_radius), 15) # Width of slot
    .extrude(-10) # Cut downwards
    .rotate((0,0,0), (0,0,1), 45) # Rotate to a specific angle
)

cover_final = cover_body.cut(slot_cut)

# --- Final Assembly ---

# Union everything into one result for visualization (exploded view kept by offset)
result = base_assembly.union(cover_final)