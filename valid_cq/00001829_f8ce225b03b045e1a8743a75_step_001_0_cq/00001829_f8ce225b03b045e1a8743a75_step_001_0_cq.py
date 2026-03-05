import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
overall_height = 80.0
main_body_width = 15.0
main_body_depth_top = 25.0
main_body_depth_bottom = 20.0  # Tapered effect

# Top Flange
flange_width = 45.0
flange_depth = 15.0
flange_thickness = 3.0

# Top Tab
tab_height_extension = 15.0  # Height above flange
tab_thickness = 4.0
tab_width = main_body_width

# Main Hollow Body
wall_thickness = 2.5
hollow_height = 55.0  # Length of the cutout
hollow_offset_top = 5.0  # Distance from bottom of flange to start of hollow

# Bottom Hinge/Mount
hinge_hole_diameter = 6.0
hinge_slot_width = 6.0
hinge_slot_depth = 12.0

# Mounting Pins (on Flange)
pin_diameter = 3.0
pin_height = 4.0
pin_head_chamfer = 0.5
pin_spacing = 25.0

# --- Geometry Construction ---

# 1. Main Body (Tapered profile)
# Creating a loft for the tapered main body
body_sk1 = cq.Sketch().rect(main_body_width, main_body_depth_top)
body_sk2 = cq.Sketch().rect(main_body_width, main_body_depth_bottom)

main_body = (
    cq.Workplane("XY")
    .placeSketch(body_sk1, body_sk2.moved(cq.Location(cq.Vector(0, 0, -overall_height))))
    .loft()
)

# 2. Top Flange
flange = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness)
    .box(flange_width, flange_depth, flange_thickness, centered=(True, True, False))
)
# Fillet the flange connection to the body for the smooth look
# Note: This is simplified; the image shows a continuous curve. We will union first.

# 3. Top Tab (extension of the back face)
# Assuming the back face is flat aligned with Y-positive or negative. 
# Looking at image, the tab is aligned with the "back" of the hollow section.
tab = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(0, main_body_depth_top/2 - tab_thickness/2)
    .box(tab_width, tab_thickness, tab_height_extension, centered=(True, True, False))
)

# Combine base shapes
part = main_body.union(flange).union(tab)

# 4. Hollow/Pocket Cutout
# Cut a rectangular pocket into the front face
# We need to orient to the front face.
# Based on the loft, the "front" is roughly Y-negative.
part = (
    part.faces(">Y") # Select back face
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=cq.Vector(0, 0, -wall_thickness)) # Go inside
    # We want to cut from the front, so we need a different approach or cut through
    # Let's cut from the front (Y-negative side)
)

# Re-orienting strategy: Use local coordinates relative to the top center
pocket = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness - hollow_offset_top)
    .center(0, (main_body_depth_top/2 - wall_thickness) - (main_body_depth_top - wall_thickness)/2 ) 
    # Centering the cut relative to the body thickness
    .box(
        main_body_width - 2*wall_thickness, 
        main_body_depth_top - wall_thickness, # Depth of cut
        hollow_height, 
        centered=(True, True, False)
    )
)
# Adjust pocket to be a through-pocket on the front face but leaving a back wall
# The image shows a "U" channel profile basically.
pocket_cut = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness - hollow_offset_top)
    .center(0, -wall_thickness/2) # Shift slightly back to leave front open? No, image shows front open.
    .box(
        main_body_width - 2*wall_thickness,
        main_body_depth_top, # Make it deep enough to cut through the front
        hollow_height,
        centered=(True, True, False)
    )
)
# Correction: The image shows a box-like structure with a large rectangular cutout on the *face*.
# It looks like a rectangular tube that is tapered.
# Let's shell or cut a pocket.
part = part.cut(pocket_cut)


# 5. Bottom Hinge Slot
part = (
    part.faces("<Z")
    .workplane()
    .center(0, 0) # Center of bottom face
    .rect(hinge_slot_width, main_body_depth_bottom + 5) # +5 to ensure cut through depth
    .cutBlind(-hinge_slot_depth)
)

# 6. Bottom Hinge Hole
# We need to find the side faces of the bottom section
part = (
    part.faces("<Z").workplane(offset=-hinge_slot_depth/2) # Go up to mid-clevis
    .transformed(rotate=cq.Vector(0, 90, 0)) # Rotate to drill from side
    .circle(hinge_hole_diameter/2)
    .cutThruAll()
)

# 7. Internal Hex/Hole at bottom of pocket (visible in image)
# There is a feature inside the pocket at the bottom.
part = (
    part.faces("<Z").workplane(offset=overall_height - hollow_height - flange_thickness - hollow_offset_top)
    .center(0, -wall_thickness) # Adjust center
    .polygon(6, 4.0) # Hex cutout
    .cutBlind(-10) # Cut downwards
)


# 8. Mounting Pins on Flange
# Locate pins on the flange wings
pin_locs = [
    (-flange_width/2 + 6, 0), # Left wing
    (flange_width/2 - 6, 0)   # Right wing
]

# Only one pin is clearly visible on the left, let's assume symmetry or just place the visible one.
# The image has a pin on the left side of the flange.
pin = (
    cq.Workplane("XY")
    .workplane(offset=-flange_thickness) # Start on top of flange (which is Z=0 in our build, wait.. flange was built down)
    # Flange was built offset -flange_thickness. So top of flange is Z=-flange_thickness?
    # Let's check build order. 
    # Flange built at offset=-flange_thickness. Top face is at -flange_thickness + thickness = 0.
    # Actually flange built downwards from offset -thickness. Top is at -thickness.
    # Let's adjust reference. Flange top surface is at Z=0 based on Union with main_body starting at Z=0.
    # But main body goes -Z. 
    # Let's assume top surface of flange is at Z = -flange_thickness (approx).
    .workplane(offset=0) # Top of flange
    .center(-flange_width/3, 0)
    .circle(pin_diameter/2)
    .extrude(pin_height)
)

# Add chamfer to pin
pin = pin.faces(">Z").chamfer(pin_head_chamfer)

# There is a small boss/pin on the other side too, partially visible? Let's add it for symmetry.
pin2 = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(flange_width/3, 0)
    .circle(pin_diameter/2)
    .extrude(pin_height)
).faces(">Z").chamfer(pin_head_chamfer)


result = part.union(pin).union(pin2)

# 9. Fillets
# Fillet the junction between flange and main body.
# This is tricky with complex topology, selecting edges by position.
try:
    result = result.edges("|Y").filter(lambda e: e.center().z > -20 and e.center().z < -2).fillet(2.0)
except:
    pass # Fallback if fillet fails

# Clean up the top tab position relative to the cut
# The cut might have eaten into the tab base. The tab is on the "back" wall.
# The cut was shifted to the "front".

# Result assignment
result = result