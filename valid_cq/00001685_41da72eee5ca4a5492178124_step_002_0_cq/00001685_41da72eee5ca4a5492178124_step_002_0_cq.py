import cadquery as cq

# Parametric dimensions
slat_width = 30.0    # Width of individual slats
slat_thickness = 4.0 # Thickness of the slats
gap_width = 2.0      # Gap between slats
length = 150.0       # Total length of the assembly
lip_height = 8.0     # Height of the front lip (L-shape)
lip_thickness = 4.0  # Thickness of the front lip
num_slats = 3        # Number of slats

# Derived dimensions
total_width = (slat_width * num_slats) + (gap_width * (num_slats - 1))

# Create the first slat (the one with the lip)
# We sketch the profile of the first slat which has an L-shape
slat1_profile = (
    cq.Workplane("YZ")
    .moveTo(0, 0)
    .lineTo(slat_width, 0)
    .lineTo(slat_width, -lip_height)
    .lineTo(slat_width - lip_thickness, -lip_height)
    .lineTo(slat_width - lip_thickness, -slat_thickness)
    .lineTo(0, -slat_thickness)
    .close()
)

# Extrude the first slat
slat1 = slat1_profile.extrude(length)

# Create the subsequent flat slats
# Profile for a standard flat slat
flat_slat_profile = (
    cq.Workplane("YZ")
    .rect(slat_width, slat_thickness, centered=False)
    .translate((0, -slat_thickness, 0)) # Align top surface with Z=0
)

flat_slat = flat_slat_profile.extrude(length)

# Assemble the parts
# Start with the L-shaped slat
result = slat1

# Add remaining flat slats
for i in range(1, num_slats):
    # Calculate offset: negative Y direction because of how sketch was drawn/oriented
    # The L-slat extends from Y=0 to Y=slat_width.
    # We want to add slats "behind" it (negative Y relative to the start, or positive depending on view)
    # Looking at the image, the lip is at the front. Let's assume the L-profile was drawn 
    # starting at origin.
    # Let's adjust the logic to build strictly by offsets.
    
    offset_distance = -1 * i * (slat_width + gap_width)
    
    # We need to move the flat slat to the correct position
    # The flat slat was created at (0, -thickness) to (width, 0).
    # We need to shift it in Y.
    shifted_slat = flat_slat.translate((0, offset_distance, 0))
    
    result = result.union(shifted_slat)

# Center the whole assembly for better presentation (optional but good practice)
center_y = -(total_width - slat_width) / 2
result = result.translate((-length/2, -center_y, 0))

# If the orientation needs to match the image exactly (Lip at bottom right),
# The current "YZ" sketch extrusion goes along X. 
# Let's rotate it to align better with a typical isometric view if needed, 
# but usually, standard X-axis extrusion is fine. 
# The code above produces the geometry correctly.