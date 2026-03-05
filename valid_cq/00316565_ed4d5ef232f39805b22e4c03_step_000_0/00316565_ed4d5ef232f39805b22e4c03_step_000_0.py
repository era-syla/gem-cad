import cadquery as cq
import math

# --- Parameters ---
num_clips = 5
spacing = 25.0         # Distance between clips
inner_radius = 6.0
thickness = 2.0
outer_radius = inner_radius + thickness
length = 12.0          # Length of the clip (extrusion depth)
opening_angle = 90.0   # Size of the opening gap in degrees

# --- Geometry Calculation ---
# We orient the C-clip in the XZ plane with the opening facing Up (+Z).
# The extrusion will be along the Y axis.
# The array of clips will be arranged along the X axis.

# Calculate angles for the profile (Counter-Clockwise)
# Gap is centered at 90 degrees (Up).
# Solid starts at 90 + half_gap and ends at 90 - half_gap (wrapping around).
half_gap = opening_angle / 2.0
start_deg = 90.0 + half_gap
end_deg = 90.0 - half_gap + 360.0  # Add 360 to handle wrap-around for calculation
mid_deg = 270.0  # The point opposite the opening

def polar(r, deg):
    rad = math.radians(deg)
    return (r * math.cos(rad), r * math.sin(rad))

# Define profile points
p_out_start = polar(outer_radius, start_deg)
p_out_mid   = polar(outer_radius, mid_deg)
p_out_end   = polar(outer_radius, end_deg)

p_in_end    = polar(inner_radius, end_deg)
p_in_mid    = polar(inner_radius, mid_deg)
p_in_start  = polar(inner_radius, start_deg)

# --- Model Construction ---

# 1. Create the base profile sketch and extrude
# We use XZ plane so "Up" is Z. Extrusion is Y.
base_clip = (
    cq.Workplane("XZ")
    .moveTo(*p_out_start)
    .threePointArc(p_out_mid, p_out_end)
    .lineTo(*p_in_end)
    .threePointArc(p_in_mid, p_in_start)
    .close()
    .extrude(length)
)

# 2. Create the linear array
# We translate copies of the base clip along the X axis
clips = []
for i in range(num_clips):
    # Calculate position: i * spacing
    # We center the extrusion on Y by translating -length/2 if desired, 
    # but here we just space them along X.
    pos = (i * spacing, 0, 0)
    clips.append(base_clip.translate(pos))

# 3. Combine into final result
result = clips[0]
for clip in clips[1:]:
    result = result.union(clip)

# Center the whole assembly roughly at origin for better viewing
total_width = (num_clips - 1) * spacing
result = result.translate((-total_width / 2.0, -length / 2.0, 0))