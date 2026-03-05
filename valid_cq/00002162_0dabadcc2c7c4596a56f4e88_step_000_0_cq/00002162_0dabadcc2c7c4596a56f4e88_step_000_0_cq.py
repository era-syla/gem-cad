import cadquery as cq

# --- Parameters ---

# Main Base Block (The trapezoidal part)
base_width = 30.0  # Total width of the base
base_length = 25.0 # Depth of the part
base_height_side = 5.0 # Height of the side flanges
base_height_center = 10.0 # Total height at the center
center_width = 12.0 # Width of the raised center section
center_hole_diam = 4.5 # Diameter of the screw hole

# The Dovetail / Sloped sides
slope_angle = 60.0 # Approximate angle of the sides

# The slot/groove on the top face
slot_width = 2.0
slot_depth = 1.0

# The rectangular extension (visible on the larger assembly on the right)
# Looking at the image, there's a standalone piece (left), a small piece (center-front),
# and an assembly (right). I will model the primary component (the one on the left)
# as it appears to be the core reusable part, but based on the complexity, 
# I will model the assembly on the right as it contains the most geometric features.
# Let's target the right-most assembly which combines a base plate and the clamp.

# Plate parameters (the flat part with rounded corners)
plate_length = 40.0
plate_width = 30.0
plate_thickness = 4.0
plate_hole_diam = 6.5
fillet_radius = 5.0

# Clamp parameters (the trapezoidal block attached to the plate)
clamp_width = 30.0
clamp_length = 20.0 
clamp_height = 8.0 # From bottom of clamp to top
clamp_lip_height = 3.0 # The lower side height
clamp_top_width = 12.0
clamp_hole_diam = 4.0

# Positioning
offset_distance = 5.0 # Overlap between plate and clamp

# --- Geometry Construction ---

# 1. Create the Flat Plate
plate = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .hole(plate_hole_diam)
)

# 2. Create the Clamp Body (Trapezoidal profile)
# We will draw the profile on the XZ plane and extrude it along Y

# Calculate coordinates for the trapezoid
# Center is at X=0
# Bottom width is clamp_width
# Top width is clamp_top_width (plus slopes)
# Actually, looking closely, it's a standard rail clamp profile.
# Let's sketch it.

x_outer = clamp_width / 2.0
x_inner = clamp_top_width / 2.0
y_base = 0.0
y_lip = clamp_lip_height
y_top = clamp_height

# Points for the right half of the profile (counter-clockwise)
# Starting from bottom center
pts = [
    (0, 0),
    (x_outer, 0),             # Bottom right corner
    (x_outer, y_lip),         # Top of lip
    (x_inner, y_top),         # Top corner
    (0, y_top)                # Top center
]

clamp_profile = (
    cq.Workplane("XZ")
    .polyline(pts)
    .mirrorY() # Mirror across Y axis (which is Z in the sketch plane) to get full shape
    .extrude(clamp_length)
)

# Rotate and move clamp to align with the plate
# The plate is centered at (0,0,0). Length is along Y.
# We want the clamp to be attached to the end of the plate.

# Move clamp so its bottom face is flush with the plate bottom (or aligned as per image)
# In the image, the clamp sits *next* to the plate, connected. 
# It looks like the plate is an extension.
# Let's align the bottom of the clamp with the bottom of the plate for a flush assembly
# or potentially the clamp is thicker.
# Assuming flush bottoms for simplicity, Z= -plate_thickness/2. 

# Re-centering the clamp extrusion
clamp = clamp_profile.translate((0, -clamp_length/2.0, -plate_thickness/2.0))

# Now shift the plate and clamp relative to each other
# Plate center Y=0. Clamp needs to be offset in Y.
clamp_y_pos = (plate_length / 2.0) + (clamp_length / 2.0) - offset_distance # Adjust for overlap/connection
# Actually, looking at the image, they seem to be a single machined part or welded.
# Let's overlap them to fuse them.
clamp = clamp.translate((0, plate_length/2.0 + clamp_length/2.0 - 0.1, 0)) 
# Just abutting them for now, but usually they are one solid.
# Let's recreate the "Assembly" on the right as a single solid object.

# Let's refine the approach: Build the clamp relative to global coordinates
# and the plate relative to it.

# Profile for the Clamp
# We draw on YZ plane this time to extrude along X (Width)? No, sticking to Extrude along Y is better for the profile.
# Let's draw on XZ plane.

# Define the clamp shape more precisely based on the "center-front" small piece style
# It has a "V" notch on the bottom? The image shows a small notch on the bottom of the floating piece.
# The main assembly clamp looks flat on bottom.

def create_clamp(length):
    pts = [
        (0, 0),
        (x_outer, 0),
        (x_outer, y_lip),
        (x_inner, y_top),
        (0, y_top)
    ]
    
    c = (
        cq.Workplane("XZ")
        .polyline(pts)
        .mirrorY()
        .extrude(length)
    )
    
    # Add the center hole
    c = (
        c.faces(">Y")
        .workplane()
        .center(0, y_top/2.0) # Approximate center vertically relative to the face? No.
        # The hole is on the top face going down.
        .transformed(rotate=(90, 0, 0)) # Rotate workplane to look at Top
        .center(0, 0) # Center of the top face
        .hole(clamp_hole_diam, depth=y_top)
    )
    
    # Add the small vertical slit/marker on the side if visible (optional detail)
    # The image shows a small vertical groove on the slanted face. 
    # Skipping for simplicity as it's a minor detail.
    
    return c

# Create the specific assembly shown on the right
# 1. The Plate
plate_part = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
    .faces(">Z")
    .workplane()
    .hole(plate_hole_diam)
)

# 2. The Clamp Section
# The clamp seems to be thicker than the plate.
# Let's position the clamp so its bottom is flush with the plate's bottom.
clamp_part = create_clamp(clamp_length)

# Rotate clamp to align with Y axis extrusion
# The create_clamp extrudes along normal (Y). 
# We need to position it.
# Current clamp center is (0, length/2, 0) roughly relative to sketch plane.
# Sketch plane was XZ.
# We need to move it to the end of the plate.

# Align bottoms:
# Plate bottom is at Z = -plate_thickness/2
# Clamp bottom (from sketch) is at Z = 0 (relative to its local coords)
# We need clamp bottom at global Z = -plate_thickness/2
clamp_part = clamp_part.translate((0, -clamp_length/2, -plate_thickness/2))

# Align Y Position:
# Plate ends at Y = plate_length/2
# Clamp should start there.
# Clamp currently spans Y = -clamp_length/2 to clamp_length/2 (locally) after the create_clamp extrusion?
# No, CadQuery extrude usually goes positive normal.
# Let's adjust translation.
# Clamp is centered on X.
# We move clamp in Y to attach to plate.
clamp_part = clamp_part.translate((0, plate_length/2 + clamp_length/2, 0))

# Union them
result = plate_part.union(clamp_part)

# If the request implies generating *all* parts in the image, I should probably 
# just generate the most complex one (the assembly) as "result". 
# The prompt says "create this 3D CAD model", singular, usually implying the main subject.
# However, to be safe and impressive, I will create the assembly on the right.

# Refinement on the connection:
# The image shows the plate overlaps the clamp slightly or is milled from one block.
# The clamp section is taller.
# The connection area looks like a step.
# The current union does exactly that.

# Optional: Adding the slot on top of the clamp
# Select top face of the clamp section
# The clamp top face is the highest planar face.
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, clamp_length/2 + plate_length/2) # Shift workplane center to clamp center
    # Create the slot
    .rect(slot_width, clamp_length)
    .cutBlind(-slot_depth)
)

# Re-drill the hole in the clamp (because union might have messed with context or order)
# Finding the center of the clamp section relative to global 0,0,0
clamp_center_y = (plate_length / 2) + (clamp_length / 2)
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(0, clamp_center_y)
    .hole(clamp_hole_diam, depth=clamp_height)
)

# Final check of the geometry
# Plate at Z centered around 0? box() centers at 0,0,0.
# So Plate bottom is -2. Top is +2.
# Clamp bottom is -2. Clamp Height is 8. Top is 6.
# Looks correct.