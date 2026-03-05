import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
total_length = 15.0  # (3 units * 5mm pitch approx)
total_width = 8.5    # Depth of the connector
total_height = 10.0  # Height of the connector body

# Pitches
pitch = 5.0          # Standard pitch for terminal blocks
num_positions = 3    # Number of terminals seen in image

# Top features (Screw holes)
top_hole_dia = 3.0   # Diameter of the screw entry hole
top_hole_depth = 4.0 # How deep the conical/cylindrical part goes

# Front features (Wire entry)
wire_entry_width = 3.5
wire_entry_height = 4.0
wire_entry_offset_y = 1.0 # Height from bottom

# Side profile parameters
front_face_height = 6.0   # Height of the vertical front face before slanting
back_face_height = 8.0    # Height of the vertical back face
top_flat_width = 4.0      # Width of the flat top surface

# Internal/Details
wall_thickness = 0.8
pin_dia = 1.0
pin_length = 3.5
side_groove_width = 1.0
side_groove_depth = 0.5

# --- Geometry Construction ---

# 1. Create the Main Extrusion Profile (Side View)
# We sketch the cross-section on the YZ plane (Right view usually, but lets do XY and extrude Z for length)
# Let's orient: X = length (pitch direction), Y = width (depth), Z = height
# But for a profile sketch, it's easier to sketch on YZ plane and extrude along X.

# Defining the profile points (YZ plane)
# (0,0) is bottom-front corner
pts = [
    (0, 0),                       # Bottom-front
    (total_width, 0),             # Bottom-back
    (total_width, back_face_height), # Back vertical
    (total_width - (total_width - top_flat_width)/2, total_height), # Back slant top
    ((total_width - top_flat_width)/2, total_height),   # Front slant top
    (0, front_face_height)        # Front vertical
]

# Create the base block
base_profile = cq.Workplane("YZ").polyline(pts).close()
base = base_profile.extrude(total_length)

# 2. Create the Wire Entry Cavities (Front)
# We need to cut rectangular holes into the front face.
# These repeat along the X axis.

# Define a single cavity
cavity = (
    cq.Workplane("XY")
    .rect(wire_entry_width, total_width) # Rect is centered, we'll position it
    .extrude(wire_entry_height)
)

# Position and cut cavities
# Center of first cavity in X: -total_length/2 + pitch/2 (if centered at origin)
# Let's re-center the base first to make math easier.
# Currently base starts at X=0 and goes to X=total_length.
# Let's move base so X=0 is the center.
base = base.translate((-total_length/2, 0, 0))

cavities = cq.Workplane("XY")
for i in range(num_positions):
    # Calculate X position: start from left + half pitch + (index * pitch)
    x_pos = -total_length/2 + (pitch/2) + (i * pitch)
    
    # We want to cut from the front (Y=0) inwards.
    # The rect profile needs to be on the XZ plane.
    
    # Let's create the solid for the cut
    cut_solid = (
        cq.Workplane("XZ")
        .workplane(offset=0) # Front face
        .moveTo(x_pos, wire_entry_offset_y + wire_entry_height/2)
        .rect(wire_entry_width, wire_entry_height)
        .extrude(total_width - wall_thickness) # Don't cut all the way through back
    )
    base = base.cut(cut_solid)
    
    # There is also a small slot at the very bottom front for the clamping mechanism cage
    cage_slot = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .moveTo(x_pos, wire_entry_offset_y/2)
        .rect(wire_entry_width - 0.5, wire_entry_offset_y)
        .extrude(total_width * 0.6)
    )
    base = base.cut(cage_slot)


# 3. Create the Top Screw Holes
# These are vertical holes (Z-axis) descending from the top face.
# Since the top is slanted/complex, usually these are counterbored or simple holes.
# Image shows a conical entry (chamfered) leading to a cylindrical hole.

top_holes = cq.Workplane("XY")
for i in range(num_positions):
    x_pos = -total_length/2 + (pitch/2) + (i * pitch)
    
    # Create the cutter
    # Position: X=center of pitch, Y=center of top flat part
    # Top flat Y center approx: total_width/2
    y_pos = total_width / 2
    
    # Cut cylinder
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=total_height)
        .moveTo(x_pos, y_pos)
        .circle(top_hole_dia / 2)
        .extrude(-total_height + 2.0) # Leave some material at bottom
    )
    
    # Add Chamfer/Cone at top
    cone = (
        cq.Workplane("XY")
        .workplane(offset=total_height)
        .moveTo(x_pos, y_pos)
        .circle(top_hole_dia / 2 + 0.5) # Wider at top
        .workplane(offset=-1.0) # Go down 1mm
        .circle(top_hole_dia / 2) # Narrower
        .loft(combine=True)
    )
    
    base = base.cut(cutter).cut(cone)

# 4. Side Slots/Interlocking features
# The image shows a vertical rectangular groove on the right side (positive X).
# It likely has a corresponding tongue on the left, but we only see the groove clearly.

# Right side groove
groove = (
    cq.Workplane("YZ")
    .workplane(offset=total_length/2) # Right face
    .moveTo(total_width/2, total_height/2)
    .rect(total_width * 0.4, total_height * 0.6) # Approximate size
    .extrude(-side_groove_depth)
)
# Often these are specific shapes, let's make a simple vertical rectangular slot based on image
groove_cut = (
    cq.Workplane("YZ")
    .workplane(offset=total_length/2) # Right face
    .moveTo(total_width * 0.8, total_height/2) # Towards the back
    .rect(side_groove_width, total_height - 2.0)
    .extrude(-side_groove_depth)
)
base = base.cut(groove_cut)


# 5. Pins (Solder legs)
# Located at the bottom. Usually aligned with the wire entry or slightly offset.
pins = cq.Workplane("XY")
for i in range(num_positions):
    x_pos = -total_length/2 + (pitch/2) + (i * pitch)
    y_pos = total_width / 2 # Usually centered in depth or back-biased
    
    # In this specific style of terminal block, pins are often offset towards the wire entry
    y_pos_pin = total_width * 0.3
    
    pin = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .moveTo(x_pos, y_pos_pin)
        .circle(pin_dia / 2)
        .extrude(-pin_length)
    )
    base = base.union(pin)

result = base