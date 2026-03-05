import cadquery as cq

# --- Parameter Definitions ---
# Main body dimensions
clevis_width = 20.0       # Outer width of the U-shape
clevis_length = 40.0      # Length from base of U to the center of the pin
clevis_thickness = 20.0   # Height/thickness of the U-shape prongs
prong_thickness = 5.0     # Thickness of the side walls

# Shaft/Stem dimensions
stem_diameter = 16.0
stem_length = 30.0

# Pin/Axle dimensions
pin_hole_diameter = 10.0
pin_head_diameter = 14.0
pin_head_thickness = 2.0
pin_body_length = clevis_width + 2 * pin_head_thickness + 2.0 # Extra length for locking clip hole

# Derived parameters
inner_gap = clevis_width - 2 * prong_thickness
total_length = stem_length + clevis_length + (clevis_thickness / 2.0)

# --- Geometry Construction ---

# 1. Create the Clevis (U-shaped body)
# We'll start with a solid block and cut out the center
clevis_body = (
    cq.Workplane("XY")
    .box(clevis_length + (clevis_thickness/2), clevis_width, clevis_thickness)
    .edges("|Z").fillet(clevis_thickness / 2.0 - 0.01) # Round the end. Small epsilon to avoid kernel issues
)

# Create the cutout for the U-shape
cutout = (
    cq.Workplane("XY")
    .box(clevis_length, inner_gap, clevis_thickness)
    .translate((-clevis_thickness/4, 0, 0)) # Shift slightly to ensure it cuts through the open end
)

# 2. Create the Stem (Cylinder at the back)
stem = (
    cq.Workplane("YZ")
    .circle(stem_diameter / 2.0)
    .extrude(stem_length)
    .translate((-stem_length - (clevis_length/2), 0, 0)) # Position at the back of the clevis body
)

# Combine body and stem, then cut the U-shape
main_part = clevis_body.union(stem).cut(cutout)

# 3. Create the Pin Holes
# Position hole center relative to the rounded end
hole_center_x = (clevis_length / 2) 

main_part = (
    main_part
    .faces(">Z")
    .workplane()
    .moveTo(hole_center_x, 0)
    .hole(pin_hole_diameter)
)

# 4. Create the Pin (Clevis Pin)
# Create the pin separately and place it
pin = (
    cq.Workplane("XZ")
    .circle(pin_hole_diameter / 2.0 - 0.1) # Tolerance clearance
    .extrude(clevis_width + 4.0) # Length of the main pin shaft
    .translate((hole_center_x, 0, -(clevis_width + 4.0)/2))
)

# Add Pin Head
pin_head = (
    cq.Workplane("XZ")
    .circle(pin_head_diameter / 2.0)
    .extrude(pin_head_thickness)
    .translate((hole_center_x, 0, (clevis_width + 4.0)/2))
)

# Add Cotter Pin Hole (Small hole at the end of the pin)
pin_end_hole = (
    cq.Workplane("XY")
    .circle(1.5) # Small hole for a clip
    .extrude(10)
    .translate((hole_center_x, 0, -(clevis_width/2 + 3.0))) # Position at the bottom end
)

# Add a washer at the bottom (implied by typical assembly) or just the pin sticking out
# Let's model the pin geometry as shown: head on top, shaft through, small hole at bottom.
pin_assembly = pin.union(pin_head).cut(pin_end_hole)

# 5. Create the Internal Thread/Bore in the Stem (Optional but realistic)
# The image shows a hole looking into the stem from the U-gap
stem_bore = (
    cq.Workplane("YZ")
    .circle(stem_diameter / 2.0 - 4.0) # Wall thickness
    .extrude(stem_length * 0.8)
    .translate((-stem_length - (clevis_length/2), 0, 0))
)

# Final Boolean Operations
result = main_part.cut(stem_bore).union(pin_assembly)

# Rotate for better view matching the image (Isometric-ish)
result = result.rotate((0,0,0), (0,0,1), 45).rotate((0,0,0), (1,0,0), 30)