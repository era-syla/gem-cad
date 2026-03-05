import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
bench_width = 1500  # Total length of the bench
bench_depth = 600   # Approximate depth at the legs
seat_height = 450   # Standard seat height
back_height = 900   # Total height including backrest

# Timber dimensions (approximated based on image visual weight)
leg_width = 80
leg_thickness = 40

seat_slat_width = 90
seat_slat_thickness = 35
seat_slat_gap = 15
num_seat_slats = 3

back_slat_width = 70
back_slat_thickness = 25
back_slat_gap = 25
num_back_slats = 3

armrest_width = 80
armrest_thickness = 30
armrest_length = 500

# Construction angles
leg_angle = 15  # Angle of the A-frame legs
back_angle = 12 # Angle of the backrest relative to vertical

# Helper calculation for spacing
leg_spacing = bench_width - 250  # Distance between the two leg assemblies

# --- Helper Functions ---

def create_slat(length, width, thickness):
    return cq.Workplane("XY").box(length, width, thickness)

# --- Assembly Construction ---

# 1. Create one side assembly (A-frame legs + armrest support)

# Front Leg
front_leg_height = seat_height + armrest_thickness # Goes up to armrest
front_leg = (
    cq.Workplane("XY")
    .box(leg_width, leg_thickness, 800) # Initial oversized length
    .rotate((0,0,0), (0,1,0), leg_angle)
    # Cut top flat for armrest
    .cut(cq.Workplane("XY").workplane(offset=front_leg_height).box(1000, 1000, 500, centered=(True, True, False)))
    # Cut bottom flat for ground
    .cut(cq.Workplane("XY").box(1000, 1000, 500, centered=(True, True, False)).mirror("XY"))
)

# Back Leg (extends up to support backrest)
back_leg_length = 1000 # Enough to reach top of backrest
back_leg = (
    cq.Workplane("XY")
    .box(leg_width, leg_thickness, back_leg_length)
    .rotate((0,0,0), (0,1,0), -leg_angle) # Slants opposite way initially for A-frame
    # Adjust position to meet front leg at top
    .translate((-250, 0, 0)) # Initial guess
)

# Refine Back Leg Position and Angle
# The back leg in the image seems to have two parts: 
# 1. The ground-to-seat part (part of the 'A')
# 2. The seat-to-top part (backrest support), which is angled differently or is a continuous piece.
# Looking closely, it looks like a continuous piece for the back leg that tilts backward.
# Let's model the A-frame side structure more simply: An inverted V.

# Let's redefine the leg strategy based on coordinates for better control.
# Side Profile 2D sketch extruded
side_profile_pts = [
    (0, 0),         # Bottom front
    (150, seat_height), # Intersection area
    (100, back_height) # Top back
]
# This is hard to parametize perfectly with simple rotations. Let's stick to placing beam geometry.

# Re-attempting Legs with explicit placement
# Front leg: Slants back /
f_leg = (
    cq.Workplane("XZ")
    .box(leg_width, 900, leg_thickness) # Length along hypotenuse approx
    .rotate((0,0,0), (0,1,0), -leg_angle)
    .translate((0, 0, 350)) # Move up
)
# Cut floor
f_leg = f_leg.cut(cq.Workplane("XY").box(2000, 2000, 1000, centered=(True,True,False)).mirror("XY"))
# Cut Armrest height
f_leg = f_leg.cut(cq.Workplane("XY").workplane(offset=seat_height + 180).box(2000, 2000, 1000, centered=(True,True,False)))

# Back leg / Backrest support: Slants forward \ then up
b_leg = (
    cq.Workplane("XZ")
    .box(leg_width, 1100, leg_thickness)
    .rotate((0,0,0), (0,1,0), back_angle)
    .translate((450, 0, 450)) # Position relative to front leg
)
# Cut floor
b_leg = b_leg.cut(cq.Workplane("XY").box(2000, 2000, 1000, centered=(True,True,False)).mirror("XY"))


# Horizontal Stretcher (Seat Support between legs)
seat_support = (
    cq.Workplane("XY")
    .box(550, leg_thickness, leg_width)
    .translate((250, 0, seat_height - leg_width/2))
)

# Lower Stretcher (between front and back leg)
lower_stretcher = (
    cq.Workplane("XY")
    .box(450, leg_thickness, leg_width*0.8)
    .translate((250, 0, 150))
)

# Armrest
armrest = (
    cq.Workplane("XY")
    .box(armrest_length, armrest_width, armrest_thickness)
    .translate((150, 0, seat_height + 180 + armrest_thickness/2))
)

# Combine one side assembly
side_assembly = f_leg.union(b_leg).union(seat_support).union(lower_stretcher).union(armrest)

# Create Left and Right Sides
left_side = side_assembly.translate((0, -leg_spacing/2, 0))
right_side = side_assembly.mirror("XZ").translate((0, leg_spacing/2, 0)) # Mirror geometry, then move positive

# --- Slats ---

# Seat Slats
seat_slats = cq.Workplane("XY")
total_seat_depth = num_seat_slats * seat_slat_width + (num_seat_slats - 1) * seat_slat_gap
start_y_seat = 80 # Offset from front

for i in range(num_seat_slats):
    x_pos = start_y_seat + i * (seat_slat_width + seat_slat_gap)
    slat = (
        cq.Workplane("YZ")
        .box(seat_slat_width, seat_slat_thickness, bench_width + 2*armrest_width) # Make slats extend past legs slightly
        .translate((x_pos, seat_height + seat_slat_thickness/2, 0))
    )
    seat_slats = seat_slats.union(slat)

# Back Rest Slats
back_slats = cq.Workplane("XY")
# Calculation to align slats with the angled back leg
# We need to find the plane of the back leg surface
# Back leg was rotated by `back_angle` around Y (in the local context of the leg creation)
# It's roughly at x=450 (base)
back_slat_start_height = seat_height + 100

for i in range(num_back_slats):
    # Height up the backrest
    h_offset = i * (back_slat_width + back_slat_gap)
    
    # Calculate position based on angle
    # x = x_base + height * tan(angle)
    # z = z_base + height
    
    # Simple placement and rotation
    slat = (
        cq.Workplane("YZ")
        .box(back_slat_width, back_slat_thickness, bench_width)
        .rotate((0,0,0), (0,0,1), -back_angle) # Rotate in YZ plane to match back incline
        .translate((430 + h_offset*0.25, back_slat_start_height + h_offset, 0)) # Manual tweak for visual alignment with back leg
    )
    back_slats = back_slats.union(slat)

# --- Final Assembly ---

# Center Support (Connecting the two lower stretchers)
center_tie = (
    cq.Workplane("XY")
    .box(leg_thickness, bench_width - leg_thickness*2, leg_width*0.7)
    .translate((250, 0, 150))
)


result = (
    left_side
    .union(right_side)
    .union(seat_slats)
    .union(back_slats)
    .union(center_tie)
)