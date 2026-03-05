import cadquery as cq

# --- Parameters ---
# Dimensions approximated from standard XT60 connector specifications
body_width = 15.5
body_depth = 8.1
body_height = 16.0
chamfer_size = 2.5
wall_thickness = 1.2
pin_spacing = 7.2
pin_diameter = 3.5
recess_depth = 0.5
text_string = "XT60"

# --- Helper Functions ---

def xt60_profile(w, d, c):
    """
    Generates the points for the chamfered rectangular profile.
    Flat face is at -Y, Chamfered face is at +Y.
    """
    return [
        (-w/2, -d/2),      # Front Left
        ( w/2, -d/2),      # Front Right
        ( w/2,  d/2 - c),  # Back Right Chamfer Start
        ( w/2 - c, d/2),   # Back Right Chamfer End
        (-w/2 + c, d/2),   # Back Left Chamfer End
        (-w/2,  d/2 - c)   # Back Left Chamfer Start
    ]

def create_pin():
    """
    Creates a detailed male bullet connector pin.
    Includes the split spring head and the solder cup tail.
    """
    shaft_len = body_height - 2.0
    # Main Shaft
    shaft = cq.Workplane("XY").circle(pin_diameter/2).extrude(shaft_len)
    
    # Bulbous Head (Spring part)
    head = (
        cq.Workplane("XY")
        .workplane(offset=shaft_len)
        .sphere(pin_diameter/2 * 1.05)
    )
    
    # Cross Slits (Spring detail)
    slit_w = 0.3
    slit_d = 4.5
    slits = (
        cq.Workplane("XY")
        .workplane(offset=shaft_len + pin_diameter/2)
        .rect(slit_w, pin_diameter * 2)
        .extrude(-slit_d)
        .union(
            cq.Workplane("XY")
            .workplane(offset=shaft_len + pin_diameter/2)
            .rect(pin_diameter * 2, slit_w)
            .extrude(-slit_d)
        )
    )
    
    # Solder Cup (Bottom)
    cup_len = 4.5
    cup_base = cq.Workplane("XY").circle(pin_diameter/2).extrude(-cup_len)
    
    # Cut half the cup to form the solder landing
    cup_cut = (
        cq.Workplane("XY")
        .workplane(offset=-cup_len/2)
        .center(0, -pin_diameter/2) # Cut front half
        .rect(pin_diameter * 2, pin_diameter)
        .extrude(cup_len * 2)
    )
    
    return shaft.union(head).cut(slits).union(cup_base.cut(cup_cut))

# --- Main Geometry Construction ---

# 1. Housing Body
points = xt60_profile(body_width, body_depth, chamfer_size)
housing = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(body_height)
)

# 2. Hollow out the housing
# Using shell to create walls and a floor
housing = housing.faces(">Z").shell(-wall_thickness)

# 3. Cut Pin Holes in Floor
housing = (
    housing.faces("<Z").workplane()
    .pushPoints([(-pin_spacing/2, 0), (pin_spacing/2, 0)])
    .circle(pin_diameter/2)
    .cutThruAll()
)

# 4. Side Detail: Recess, Text, and Ribs
# Locate the front flat face (-Y)
front_face_wp = housing.faces("<Y").workplane(centerOption="CenterOfBoundBox")

# Cut Recess
rec_w = 12.0
rec_h = 6.0
housing = (
    front_face_wp
    .rect(rec_w, rec_h)
    .cutBlind(-recess_depth)
)

# Create Text and Ribs inside the recess
# Reference the bottom of the recess
detail_wp = housing.faces("<Y").workplane(centerOption="CenterOfBoundBox").workplane(offset=-recess_depth)

# Text
text_geo = (
    detail_wp
    .text(text_string, fontsize=4.0, distance=recess_depth, font="Arial", kind="bold")
)

# Ribs (Top and Bottom)
rib_geo = (
    detail_wp
    .center(0, 2.3)
    .rect(rec_w, 0.4).extrude(recess_depth)
    .center(0, -4.6) # Move relative to previous center
    .rect(rec_w, 0.4).extrude(recess_depth)
)

housing = housing.union(text_geo).union(rib_geo)

# 5. Bottom Shield/Shroud
# Extension on the bottom right pin (common on some XT60 variants)
shield_len = 4.0
shield = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(pin_spacing/2, 0)
    .circle(pin_diameter/2 + 0.8)
    .extrude(-shield_len)
)
# Cut shield to be a half-cylinder facing back
shield_cut = (
    cq.Workplane("XY")
    .workplane(offset=-shield_len/2)
    .center(pin_spacing/2, -1.5)
    .rect(6, 4)
    .extrude(shield_len * 2)
)
shield = shield.cut(shield_cut)
housing = housing.union(shield)

# 6. Pins
pin_obj = create_pin()
left_pin = pin_obj.translate((-pin_spacing/2, 0, 0))
right_pin = pin_obj.translate((pin_spacing/2, 0, 0))

# 7. Final Assembly
result = housing.union(left_pin).union(right_pin)