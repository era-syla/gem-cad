import cadquery as cq

# Define parameters for the components
# Coin/Battery-like shape dimensions
coin_diameter = 20.0
coin_thickness = 3.0
rim_width = 2.0
rim_height = 1.0  # Extra height for the rim
recess_depth = 1.0

# Small pin dimensions
pin_diameter = 2.0
pin_length = 10.0

# Positions based on visual estimation from the origin (0,0,0)
# Group on the left
pos_bottom_left = (0, -20, 0)
pos_mid_left = (5, 0, 0)
pos_back_left = (15, 5, -5) # Slightly behind
pos_top_left = (12, 10, 5)  # Slightly elevated and overlapping

# The lonely pin
pos_pin = (40, 0, 0)

# The far right coin
pos_far_right = (80, 10, 0)

def create_coin(diameter, thickness, rim_w, rim_h):
    """
    Creates a coin-like object with a raised rim.
    Basically a cylinder with a smaller cylinder cut out of the top face,
    or a base cylinder plus a ring on top.
    """
    # Base cylinder
    base = cq.Workplane("XY").cylinder(thickness, diameter/2.0)
    
    # Create the rim
    # We can do this by cutting a pocket or adding a ring. 
    # Let's add a ring on the top face for the rim.
    rim_outer_r = diameter / 2.0
    rim_inner_r = (diameter / 2.0) - rim_w
    
    # We need to orient the workplane on the top face of the base
    # Since the base cylinder is centered at Z=0 (half up, half down), the top is at +thickness/2
    rim = (cq.Workplane("XY")
           .workplane(offset=thickness/2.0)
           .circle(rim_outer_r)
           .circle(rim_inner_r)
           .extrude(rim_h))
           
    return base.union(rim)

def create_pin(diameter, length):
    return cq.Workplane("XY").cylinder(length, diameter/2.0)

# Create the base components
# Looking closely at the image, some look like simple discs, some look like they have rims (like button batteries or shallow caps)
# The ones at pos_bottom_left and pos_top_left definitely show a rim/recess.
# The one at pos_far_right also shows a rim.
# The one at pos_mid_left looks flat, maybe the back side.
# The one at pos_back_left is partially obscured but looks like a disc.

# Let's standardize on a "cap" shape for most.

# 1. Bottom Left Coin (Facing viewer)
coin1 = create_coin(coin_diameter, coin_thickness, rim_width, recess_depth)
coin1 = coin1.rotate((0,0,0), (0,1,0), 90).translate(pos_bottom_left)

# 2. Middle Left Coin (Back facing viewer, or just a flat disc)
coin2 = cq.Workplane("XY").cylinder(coin_thickness, coin_diameter/2.0)
coin2 = coin2.rotate((0,0,0), (0,1,0), 90).translate(pos_mid_left)

# 3. Top Left Coin (Facing viewer, overlapping coin 2)
coin3 = create_coin(coin_diameter, coin_thickness, rim_width, recess_depth)
coin3 = coin3.rotate((0,0,0), (0,1,0), 90).translate(pos_top_left)

# 4. Back Left Coin (Behind coin 2/3)
coin4 = cq.Workplane("XY").cylinder(coin_thickness, coin_diameter/2.0)
coin4 = coin4.rotate((0,0,0), (0,1,0), 90).translate(pos_back_left)

# 5. The Pin
pin = create_pin(pin_diameter, pin_length)
# The pin in the image is vertical
pin = pin.translate(pos_pin)

# 6. The Far Right Coin (Facing viewer)
coin5 = create_coin(coin_diameter, coin_thickness, rim_width, recess_depth)
coin5 = coin5.rotate((0,0,0), (0,1,0), 90).translate(pos_far_right)

# Combine all objects into a single result
result = coin1.union(coin2).union(coin3).union(coin4).union(pin).union(coin5)