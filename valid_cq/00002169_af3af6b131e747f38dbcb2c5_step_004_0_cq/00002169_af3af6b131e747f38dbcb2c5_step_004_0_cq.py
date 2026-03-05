import cadquery as cq

# Define parametric dimensions
base_diameter = 50.0
base_height = 10.0

neck_diameter = 30.0
neck_height = 15.0

bulb_diameter = 70.0
bulb_straight_height = 20.0  # The cylindrical part in the middle of the bulb
bulb_transition_height = 20.0 # Height of the conical/curved sections

top_flange_diameter = 55.0
top_flange_height = 8.0

hole_diameter = 25.0

# Calculate derived points for the profile
# We will define half the profile in the XZ plane and revolve it around Z

# Points for the outer profile (starting from bottom center, moving clockwise)
p0 = (0, 0) # Bottom center
p1 = (base_diameter / 2.0, 0) # Bottom outer edge
p2 = (base_diameter / 2.0, base_height) # Top of base flange

# Neck region (concave curve approximation using a straight line for simplicity, 
# then we can use a fillet later, or define specific points)
# Looking at the image, it goes from base to the bulb. 
# There seems to be a small vertical neck or transition.
p3 = (neck_diameter / 2.0, base_height) 
p4 = (neck_diameter / 2.0, base_height + neck_height)

# Bulb region
# It expands out to the bulb diameter
current_height = base_height + neck_height
p5 = (bulb_diameter / 2.0, current_height + bulb_transition_height)
p6 = (bulb_diameter / 2.0, current_height + bulb_transition_height + bulb_straight_height)

# Transition to top flange
current_height = current_height + bulb_transition_height + bulb_straight_height
p7 = (neck_diameter / 2.0, current_height + bulb_transition_height) # Narrowing back down

# Top Flange
current_height = current_height + bulb_transition_height
p8 = (top_flange_diameter / 2.0, current_height) # Underside of top flange
p9 = (top_flange_diameter / 2.0, current_height + top_flange_height) # Top outer edge
p10 = (0, current_height + top_flange_height) # Top center

# Create the main revolution
# We construct the points. The image shows curved transitions.
# A spline or arc approach creates the smoother "bulb" look better than straight lines.
# However, the image has distinct sharp edges on the middle section, 
# implying it's a cylinder with chamfered/conical transitions, not a perfect sphere.

result = (
    cq.Workplane("XY")
    .tag("base_plane")
    # 1. Base Flange
    .circle(base_diameter / 2.0).extrude(base_height)
    
    # 2. Lower Neck (Cylinder)
    .faces(">Z").workplane()
    .circle(neck_diameter / 2.0).extrude(neck_height)
    
    # 3. Bulb Lower Transition (Cone)
    .faces(">Z").workplane()
    .circle(neck_diameter / 2.0).workplane(offset=bulb_transition_height)
    .circle(bulb_diameter / 2.0).loft(combine=True)
    
    # 4. Bulb Middle Section (Cylinder)
    .faces(">Z").workplane()
    .circle(bulb_diameter / 2.0).extrude(bulb_straight_height)
    
    # 5. Bulb Upper Transition (Cone)
    .faces(">Z").workplane()
    .circle(bulb_diameter / 2.0).workplane(offset=bulb_transition_height)
    .circle(neck_diameter / 2.0).loft(combine=True)
    
    # 6. Upper Neck/gap (Cylinder - small height before flange)
    .faces(">Z").workplane()
    .circle(neck_diameter / 2.0).extrude(5.0) # Small standoff
    
    # 7. Top Flange
    .faces(">Z").workplane()
    .circle(top_flange_diameter / 2.0).extrude(top_flange_height)
    
    # 8. Drill the central hole through the entire stack
    .faces(">Z").workplane()
    .hole(hole_diameter)
)

# Apply Fillets to smooth out the specific transitions as seen in the image
# The transition from the lower neck to the bulb cone is curved
# The transition from the upper neck to the bulb cone is curved
# The transition from the base to the neck is sharp in the code, but looks slightly filleted in image.

# Let's select edges based on Z height to apply fillets specifically where the 'curve' is
# The image shows the bulb part is very smooth, suggesting the cones might actually be a revolve spline
# or heavily filleted. Let's fillet the edges of the "bulb" section.

try:
    # Fillet the lower neck-to-cone transition
    result = result.edges(cq.selectors.NearestToPointSelector((neck_diameter/2, 0, base_height + neck_height))).fillet(5.0)
    
    # Fillet the "equator" of the bulb (top and bottom of the straight cylinder section)
    # The image actually shows a sharp line at the equator belt, so we KEEP those sharp.
    # Wait, looking closely at the image, the middle section is a cylinder, and there are visible seam lines.
    # It looks like: Base -> Neck -> Conical expansion -> Cylinder -> Conical contraction -> Neck -> Flange.
    
    # The image shows a fillet at the top neck junction
    # Fillet the junction under the top flange
    z_under_flange = base_height + neck_height + bulb_transition_height + bulb_straight_height + bulb_transition_height + 5.0
    result = result.edges(cq.selectors.NearestToPointSelector((neck_diameter/2, 0, z_under_flange))).fillet(2.0)

except Exception:
    # Fallback if edge selection is tricky due to parametric changes
    pass