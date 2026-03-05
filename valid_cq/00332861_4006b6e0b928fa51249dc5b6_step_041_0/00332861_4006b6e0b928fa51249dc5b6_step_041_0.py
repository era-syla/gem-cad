import cadquery as cq

# --- Parameters ---
length = 600.0        # Total length of the rail
width = 25.0          # Total width of the rail
base_thickness = 5.0  # Thickness of the base plate
rib_height = 5.0      # Additional height of the rib
rib_width = 8.0       # Width of the raised rib
total_height = base_thickness + rib_height

# Feature parameters
num_notches = 5
notch_length = 60.0
hole_diameter = 4.5
chamfer_distance = 25.0 # Length of the miter cut at the end

# Calculated spacing for notches
# Distribute notches evenly along the length with padding at ends
padding = 40.0
available_len = length - 2 * padding
notch_pitch = available_len / (num_notches - 1) if num_notches > 1 else 0

# --- Geometry Generation ---

# 1. Create the main L-profile extrusion
# Profile drawn on YZ plane: (0,0) is bottom-left-rear corner
# Extruded along X axis
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),
        (width, 0),
        (width, base_thickness),
        (rib_width, base_thickness),
        (rib_width, total_height),
        (0, total_height),
        (0, 0)
    ])
    .close()
    .extrude(length)
)

# 2. Cut notches into the rib
# We create a workplane on top of the base (where the rib starts)
# and cut rectangular sections out of the rib.
notch_cutter = cq.Workplane("XY").workplane(offset=base_thickness)

for i in range(num_notches):
    # Calculate position
    x_pos = padding + i * notch_pitch
    
    # Cut the notch (remove rib material)
    # Centered on the rib width (rib_width/2)
    result = result.cut(
        notch_cutter
        .moveTo(x_pos, rib_width / 2)
        .rect(notch_length, rib_width * 2) # Make width oversize to ensure clean cut
        .extrude(rib_height)
    )
    
    # 3. Drill mounting holes
    # Holes are placed in the center of the notches, through the base
    result = result.cut(
        cq.Workplane("XY")
        .moveTo(x_pos, width / 2) # Centered on the rail width, or rib?
        # Image suggests holes are centered on the rib/notch axis
        .moveTo(x_pos, rib_width / 2) 
        .circle(hole_diameter / 2)
        .extrude(total_height)
    )

# 4. Create the angled miter cut at the right end
# We remove a triangular prism from the end to create the angle.
# Cut reduces the width from full length (at rib) to shorter length (at edge).
result = result.cut(
    cq.Workplane("XY")
    .moveTo(length, 0)
    .lineTo(length, width)
    .lineTo(length - chamfer_distance, width)
    .close()
    .extrude(total_height)
)

# Optional: Add small fillets to the sharp edges if desired, 
# but keeping it sharp to match the schematic look of the prompt.
# result = result.edges("|X").fillet(0.5)