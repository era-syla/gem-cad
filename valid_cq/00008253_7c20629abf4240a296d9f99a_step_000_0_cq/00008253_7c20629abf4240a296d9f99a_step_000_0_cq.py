import cadquery as cq

# --- Parameters ---
# Main body dimensions
body_width = 28.0
body_depth = 28.0
body_height = 28.0
fillet_radius = 5.0
edge_fillet_radius = 0.5  # For the sharp edges

# USB Cutout dimensions
usb_width = 13.0
usb_height = 5.0
usb_depth = 12.0

# Prong dimensions (US Plug NEMA 1-15)
prong_width = 1.5
prong_depth = 6.3
prong_length = 16.0
prong_spacing = 12.7  # Center to center distance
hole_dia = 3.0
hole_z_offset = -12.0 # Distance from base

# --- Modeling ---

# 1. Create the Main Body
# Start with a simple box
main_body = (
    cq.Workplane("XY")
    .box(body_width, body_depth, body_height)
    # Fillet the vertical edges to get the rounded square shape
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Add slight chamfer/fillet to top and bottom edges for realism
main_body = (
    main_body
    .edges("#Z")  # Select edges perpendicular to Z (top and bottom loops)
    .fillet(edge_fillet_radius)
)

# 3. Create the USB Cutout on the Top Face
# We select the top face, work on it, sketch a rectangle, and cut blind
usb_cutout = (
    main_body.faces(">Z")
    .workplane()
    .rect(usb_width, usb_height)
    .cutBlind(-usb_depth)
)

# 4. Create the Prongs
# Helper function to create a single prong shape
def create_prong():
    p = (
        cq.Workplane("XZ")
        .box(prong_width, prong_length, prong_depth)
        # Add the hole
        .faces(">Y")
        .workplane()
        .pushPoints([(0, prong_length/2 - 4.0)]) # Rough position of hole relative to center
        .hole(hole_dia)
    )
    
    # Optional: Taper the tip for easier insertion
    # Create a cutting tool to chamfer the tip
    tip_cutter = (
        cq.Workplane("XY")
        .workplane(offset=prong_length/2)
        .rect(prong_width*2, prong_depth*2)
        .extrude(2)
        .rotate((0,0,0), (1,0,0), 45) # Just a placeholder logic, usually specific chamfers
    )
    
    # For simplicity in this generated code, we will apply a chamfer to the bottom edges of the prong
    # Note: Because the prong was created in XZ, "bottom" in the prong's local Y is -Y
    p = p.edges("<Y").fillet(0.5) # Soften tip
    
    # Rotate to align vertically (Z-axis) pointing down
    p = p.rotate((0,0,0), (1,0,0), 90)
    return p

# Instantiate prongs
left_prong = (
    cq.Workplane("XY")
    .box(prong_width, prong_depth, prong_length)
    .translate((-prong_spacing/2, 0, -body_height/2 - prong_length/2))
)

# Add the hole to the left prong
left_prong = (
    left_prong
    .faces("<X")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(0, -prong_length/2 + 3.0, 0)) # Position near tip
    .hole(hole_dia)
)

# Add chamfer to tip of left prong for insertion
left_prong = (
    left_prong.edges("<Z").fillet(0.5)
)


right_prong = (
    cq.Workplane("XY")
    .box(prong_width, prong_depth, prong_length)
    .translate((prong_spacing/2, 0, -body_height/2 - prong_length/2))
)

# Add the hole to the right prong
right_prong = (
    right_prong
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(0, -prong_length/2 + 3.0, 0))
    .hole(hole_dia)
)

# Add chamfer to tip of right prong
right_prong = (
    right_prong.edges("<Z").fillet(0.5)
)

# 5. Combine everything
result = usb_cutout.union(left_prong).union(right_prong)

# Export or Display (if running in an environment that supports it)
# cq.exporters.export(result, "charger.step")