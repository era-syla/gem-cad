import cadquery as cq

# --- Parametric Dimensions ---
# Base Cover
cover_width_top = 400.0  # Width of the top flat section
cover_depth = 500.0      # Length of the cover
side_height = 150.0      # Vertical height of the sides
side_angle = 15.0        # Angle of sides (0 would be vertical)
thickness = 5.0          # Thickness of the sheet metal

# Support Frame (Angle Irons)
angle_iron_w = 40.0      # Width of L-profile leg
angle_iron_h = 40.0      # Height of L-profile leg
angle_iron_thk = 5.0     # Thickness of L-profile
cross_bar_pos = 150.0    # Position of the cross bar from the front edge
strut_height = 120.0     # Height of the angled struts
strut_angle = 60.0       # Angle of struts relative to horizontal

# --- Geometry Construction ---

# 1. Main Cover (Bent Sheet Metal)
# Define the profile as a wire
# Center the top flat part
half_top = cover_width_top / 2.0
# Calculate bottom width based on angle
# tan(angle) = x / height -> x = height * tan(angle)
import math
flare = side_height * math.tan(math.radians(side_angle))
bottom_x = half_top + flare

# Create the profile points for the outer shell
pts = [
    (-bottom_x, -side_height),
    (-half_top, 0),
    (half_top, 0),
    (bottom_x, -side_height)
]

# Create the cover
cover_profile = (
    cq.Workplane("front")
    .polyline(pts)
    .offset2D(thickness, kind='intersection') # Offset inwards/outwards to give thickness
)

# Extrude the cover
cover = cover_profile.extrude(cover_depth)

# 2. Side Rails (L-Angle Irons along the top edges)
def make_angle_iron(length):
    return (
        cq.Workplane("front")
        .moveTo(0,0)
        .lineTo(angle_iron_w, 0)
        .lineTo(angle_iron_w, angle_iron_thk)
        .lineTo(angle_iron_thk, angle_iron_thk)
        .lineTo(angle_iron_thk, angle_iron_h)
        .lineTo(0, angle_iron_h)
        .close()
        .extrude(length)
    )

rail_left = make_angle_iron(cover_depth)
rail_right = make_angle_iron(cover_depth)

# Position Left Rail
rail_left = (
    rail_left
    .rotate((0,0,0), (0,1,0), 90) # Orient along Y
    .rotate((0,0,0), (0,0,1), 180) # Flip to face inward/downward correctly
    .translate((-half_top, 0, 0)) # Move to left edge
    .translate((angle_iron_thk, 0, angle_iron_thk)) # Adjust for L-shape alignment
)

# Position Right Rail (Mirrored setup)
rail_right = (
    rail_right
    .rotate((0,0,0), (0,1,0), 90)
    .rotate((0,0,0), (0,0,1), 90) # Flip to face inward
    .translate((half_top, 0, 0))
    .translate((-angle_iron_thk, 0, angle_iron_thk))
)

# 3. Cross Bar
cross_bar_len = cover_width_top - (2 * angle_iron_thk) # Fit between rails
cross_bar = make_angle_iron(cross_bar_len)

cross_bar = (
    cross_bar
    .rotate((0,0,0), (0,0,1), -90) # Orient across X
    .rotate((0,0,0), (1,0,0), 180) # L shape facing up/back
    .translate((0, cross_bar_pos, angle_iron_thk)) # Lift up
    .translate((-cross_bar_len/2, 0, 0)) # Center
)

# 4. Angled Struts
# We create one strut and mirror/copy it
# Profile is a rectangular tube or channel, looks like C-channel or tube in image
# Assuming rectangular tube for simplicity based on visual
strut_w = 40.0
strut_d = 20.0
strut_wall = 3.0

def make_strut(h, angle):
    # Calculate length based on height and angle
    # sin(angle) = h / L -> L = h / sin(angle)
    L = h / math.sin(math.radians(angle))
    
    s = (
        cq.Workplane("front")
        .rect(strut_w, strut_d)
        .rect(strut_w - 2*strut_wall, strut_d - 2*strut_wall)
        .extrude(L)
    )
    
    # Rotate to angle
    s = s.rotate((0,0,0), (1,0,0), 90 - angle)
    
    # Cut the bottom flush with Z=0 plane (conceptually)
    # And cut top vertical
    # Actually simpler to just model a block and cut it
    return s

# Simpler approach for struts: Loft or specific extrusion vector
# Let's use a sketch on the side plane and extrude
strut_side_pts = [
    (0,0),
    (strut_d, 0),
    (strut_d + strut_height/math.tan(math.radians(strut_angle)), strut_height),
    (strut_height/math.tan(math.radians(strut_angle)), strut_height)
]

strut_geo_base = (
    cq.Workplane("YZ")
    .polyline(strut_side_pts).close()
    .extrude(strut_w) # Extrude along X
)

# Position Struts
strut_left = (
    strut_geo_base
    .translate((-half_top + angle_iron_w, cross_bar_pos, 0)) # Initial position
    .translate((-strut_w - angle_iron_thk, 0, angle_iron_thk)) # Fine adjustment
)

strut_right = (
    strut_geo_base
    .translate((half_top - angle_iron_w, cross_bar_pos, 0))
    .translate((angle_iron_thk, 0, angle_iron_thk))
)

# Add holes to the rails (mounting points)
hole_dia = 10.0
rail_left = (
    rail_left.faces(">Z").workplane()
    .pushPoints([(0, 50), (0, cover_depth - 50)])
    .hole(hole_dia)
)
rail_right = (
    rail_right.faces(">Z").workplane()
    .pushPoints([(0, 50), (0, cover_depth - 50)])
    .hole(hole_dia)
)

# Combine everything
result = (
    cover
    .union(rail_left)
    .union(rail_right)
    .union(cross_bar)
    .union(strut_left)
    .union(strut_right)
)