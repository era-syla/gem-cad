import cadquery as cq
import math

# --- Parameters ---
# Overall Dimensions
hub_length = 135.0
axle_bore_dia = 12.0
axle_cap_od = 19.0
axle_cap_len = 10.0

# Flanges
flange_od = 58.0
flange_width = 3.5
left_flange_x = 32.0
right_flange_x = 85.0
spoke_hole_dia = 2.6
spoke_holes_count = 16  # Per flange

# Center Shell
waist_dia = 26.0
waist_x = (left_flange_x + right_flange_x) / 2

# Disc Brake Mount (ISO 6-bolt)
disc_bcd = 44.0
disc_hole_dia = 5.0  # M5
disc_mount_od = 52.0 # The "star" shape peaks
disc_mount_x_start = 12.0
disc_mount_thickness = 10.0

# Freehub (Shimano HG Style)
freehub_od = 35.0
freehub_len = 38.0
spline_depth = 1.5
num_splines = 9

# --- Construction ---

# 1. Main Revolved Body Profile
# We define points for half the cross-section (X, Y)
pts = [
    (0, axle_cap_od/2),
    (axle_cap_len, axle_cap_od/2),
    (axle_cap_len, 18.0), # Step up to disc mount area
    (left_flange_x, 18.0), # Disc mount area cylinder
    (left_flange_x, flange_od/2), # Left Flange Start
    (left_flange_x + flange_width, flange_od/2), # Left Flange End
]

# Create the curve for the shell body (Hourglass shape)
# We use a spline for the waist section
shell_curve_pts = [
    (left_flange_x + flange_width, 19.0), # Drop down from flange
    (waist_x, waist_dia/2),             # Waist
    (right_flange_x, 19.0)              # Rise to right flange
]

pts_right = [
    (right_flange_x, flange_od/2), # Right Flange Start
    (right_flange_x + flange_width, flange_od/2), # Right Flange End
    (right_flange_x + flange_width, freehub_od/2), # Drop to freehub
    (hub_length - 2, freehub_od/2), # End of freehub body
    (hub_length - 2, axle_cap_od/2), # Step down to end cap
    (hub_length, axle_cap_od/2), # End cap
    (hub_length, axle_bore_dia/2), # To Bore
    (0, axle_bore_dia/2) # Close loop
]

# Build profile with moveTo/lineTo/spline
all_pts = pts + shell_curve_pts + pts_right

profile = cq.Workplane("XY").moveTo(*all_pts[0])
for p in all_pts[1:6]:  # Left side lines up to flange end
    profile = profile.lineTo(*p)
# Spline through shell curve to right flange
profile = profile.spline([shell_curve_pts[0], shell_curve_pts[1], shell_curve_pts[2], pts_right[0]], includeCurrent=True)
# Right side lines
for p in pts_right[1:]:
    profile = profile.lineTo(*p)
profile = profile.close()

main_body = profile.revolve(360, (0, 0, 0), (1, 0, 0))

# 2. Disc Brake Mount (ISO 6-bolt)
# Create the mounting bosses
disc_boss = (
    cq.Workplane("YZ")
    .workplane(offset=disc_mount_x_start)
    .polarArray(disc_bcd/2, 0, 360, 6)
    .circle(4.5) # Boss radius
    .extrude(disc_mount_thickness)
)

# Create the holes
disc_holes = (
    cq.Workplane("YZ")
    .workplane(offset=disc_mount_x_start - 1)
    .polarArray(disc_bcd/2, 0, 360, 6)
    .circle(disc_hole_dia/2)
    .extrude(disc_mount_thickness + 5, combine=False)
)

# Unite bosses then cut holes
result = main_body.union(disc_boss).cut(disc_holes)


# 3. Spoke Holes
# Left Flange
left_holes = (
    cq.Workplane("YZ")
    .workplane(offset=left_flange_x + flange_width/2)
    .polarArray(flange_od/2 - 4, 0, 360, spoke_holes_count)
    .circle(spoke_hole_dia/2)
    .extrude(10) # Cut through
)

# Right Flange
# Offset rotation by half pitch for visual realism
right_holes = (
    cq.Workplane("YZ")
    .workplane(offset=right_flange_x + flange_width/2)
    .polarArray(flange_od/2 - 4, 360/spoke_holes_count/2, 360, spoke_holes_count)
    .circle(spoke_hole_dia/2)
    .extrude(10)
)

result = result.cut(left_holes).cut(right_holes)


# 5. Freehub Splines
# Create one spline tooth and array it
spline_width = 3.5

spline_tooth = (
    cq.Workplane("YZ")
    .workplane(offset=right_flange_x + flange_width)
    .transformed(rotate=cq.Vector(0, 0, 0))
    .center(0, freehub_od/2) # Move to surface
    .rect(spline_width, spline_depth * 2) # Rectangle centered on circumference
    .extrude(freehub_len - 4) # Extrude along freehub
)

# Array the splines
all_splines = (
    cq.Workplane("YZ")
    .workplane(offset=right_flange_x + flange_width)
    .polarArray(freehub_od/2, 0, 360, num_splines)
    .rect(spline_width, spline_depth*2)
    .extrude(freehub_len - 4)
)

result = result.union(all_splines)

# 6. Final Clean up
# Chamfer the axle bore entrance for realism
result = result.faces("<X").chamfer(0.5)
result = result.faces(">X").chamfer(0.5)

# Fillet the junction between flanges and shell for smoothness
try:
    # Select edges at the base of the flanges on the shell side
    # This selector is approximate based on X coordinates
    result = result.edges(f"(>X[{left_flange_x}] and <X[{left_flange_x+10}]) and <Z[{flange_od/2}]").fillet(2.0)
    result = result.edges(f"(<X[{right_flange_x}] and >X[{right_flange_x-10}]) and <Z[{flange_od/2}]").fillet(2.0)
except:
    pass # Skip if selection is too complex for robust execution

# Add chamfers to the disc mount bosses
try:
    result = result.edges(cq.selectors.NearestToPointSelector((disc_mount_x_start+disc_mount_thickness, disc_bcd/2 + 4.5, 0))).chamfer(0.5)
except:
    pass
