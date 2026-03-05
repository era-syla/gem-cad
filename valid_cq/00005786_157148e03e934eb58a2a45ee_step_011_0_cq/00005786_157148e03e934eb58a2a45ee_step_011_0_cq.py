import cadquery as cq

# --- Parameter Definitions ---
# Rack Gear Parameters
rack_length = 150.0
rack_width = 10.0
rack_height = 15.0
tooth_pitch = 3.0
tooth_depth = 2.5
tooth_angle = 20.0  # Pressure angle approximation for the profile

# Mounting Bracket Parameters
bracket_base_length = 25.0
bracket_width = 10.0 # Same as rack width usually
bracket_height = 10.0
mount_hole_dia = 4.0

# Crank Handle Parameters
handle_rod_dia = 4.0
handle_segment1 = 40.0 # The shaft part
handle_segment2 = 25.0 # The offset arm
handle_segment3 = 30.0 # The grip part
bend_radius = 4.0 # For the corners of the handle

# --- Rack Gear Modeling ---

# 1. Create the base rectangular bar for the rack
rack_base = cq.Workplane("XY").box(rack_length, rack_width, rack_height)

# 2. Create the cutter profile for the teeth
# We will create a single tooth cutter and pattern it
tooth_bottom_width = tooth_pitch / 3.0 # Rough approximation
tooth_top_width = tooth_pitch * 0.7

# Create a sketch for the space between teeth to cut away
# This is a trapezoidal shape
cutter_profile = (
    cq.Workplane("XZ", origin=(0, -rack_width/2, rack_height/2))
    .lineTo(tooth_pitch/2, 0)
    .lineTo(tooth_pitch/2 - (tooth_depth * 0.3), -tooth_depth)
    .lineTo(-tooth_pitch/2 + (tooth_depth * 0.3), -tooth_depth)
    .lineTo(-tooth_pitch/2, 0)
    .close()
)
# Extrude the cutter
cutter = cutter_profile.extrude(rack_width)

# Cut the teeth along the length of the rack
# We start slightly offset from the edge
num_teeth = int(rack_length / tooth_pitch) - 1
rack_with_teeth = rack_base
for i in range(num_teeth):
    # Calculate position: start from left end (-rack_length/2) + margin + index*pitch
    x_pos = -rack_length/2 + tooth_pitch + (i * tooth_pitch)
    # Translate the cutter and subtract
    current_cut = cutter.translate((x_pos, 0, 0))
    rack_with_teeth = rack_with_teeth.cut(current_cut)

# 3. Create the triangular mounting bracket
# It's attached to the right end of the rack
bracket_pts = [
    (0, 0),
    (bracket_base_length, 0),
    (0, -bracket_height)
]

bracket = (
    cq.Workplane("XY")
    .workplane(offset=-rack_height/2) # Start at bottom of rack
    .center(rack_length/2 - bracket_base_length, 0) # Position near the end
    .polyline(bracket_pts)
    .close()
    .extrude(rack_width)
)

# Move bracket to align correctly (extrusion is centered by default in Y, but we need to check Z)
# The default extrude goes +Z from the workplane. We want it effectively "hanging" or extending the shape.
# Let's adjust: The sketch was on the bottom face.
# We need to rotate/move it to look like the image (a gusset under the rack).
# Actually, simpler method: Draw on the side face of the rack.

bracket_side = (
    cq.Workplane("XZ")
    .center(rack_length/2 - bracket_base_length/2, -rack_height/2)
    .polyline([
        (bracket_base_length/2, 0), # Top right corner of triangle (relative to center)
        (bracket_base_length/2, -bracket_height), # Bottom tip
        (-bracket_base_length/2, 0) # Top left
    ])
    .close()
    .extrude(rack_width/2) # Extrude one way
    .union(
        cq.Workplane("XZ")
        .center(rack_length/2 - bracket_base_length/2, -rack_height/2)
        .polyline([
            (bracket_base_length/2, 0),
            (bracket_base_length/2, -bracket_height),
            (-bracket_base_length/2, 0)
        ])
        .close()
        .extrude(-rack_width/2) # Extrude the other way
    )
)

# Combine Rack and Bracket
rack_assembly = rack_with_teeth.union(bracket_side)

# Add the hole in the bracket
rack_assembly = (
    rack_assembly.faces("<Y").workplane()
    .center(rack_length/2 - bracket_base_length*0.3, -rack_height/2 - bracket_height*0.3)
    .circle(mount_hole_dia/2)
    .cutThruAll()
)

# --- Crank Handle Modeling ---

# We use a sweep path for the bent rod
path = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(handle_segment1, 0) 
    .lineTo(handle_segment1, handle_segment2) 
    .lineTo(handle_segment1 - handle_segment3, handle_segment2)
)

# Create the circular profile and sweep along the path
handle = (
    cq.Workplane("YZ")
    .circle(handle_rod_dia / 2)
    .sweep(path, transition="round") # transition="round" creates the fillets automatically
)

# Position the handle away from the rack for the assembly view
handle = handle.rotate((0,0,0), (1,0,0), 90).translate((-rack_length/2 - 20, -30, -20))

# --- Final Result ---

result = rack_assembly.union(handle)