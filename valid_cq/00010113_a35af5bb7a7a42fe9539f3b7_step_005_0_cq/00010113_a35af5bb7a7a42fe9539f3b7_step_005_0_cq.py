import cadquery as cq

# --- Parameters ---
outer_diameter = 50.0
height = 20.0
inner_hole_diameter = 20.0  # Diameter at the base of the teeth
spline_outer_diameter = 28.0 # Diameter at the tip of the teeth
num_splines = 8
spline_width = 5.0 # Approximate width of the tooth

# --- Construction ---

# 1. Create the main outer cylinder
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height)

# 2. Create the internal spline profile
# We will create one tooth and then polar array it
def create_spline_profile(loc):
    # Calculate angular width for the tooth based on width and radius
    # For simplicity in this visual approximation, we'll draw a rectangle and cut it
    return (
        cq.Workplane()
        .rect(spline_width, spline_outer_diameter) # Create a rectangle representing the tooth slot
        .val()
    )

# Instead of complex sketches, let's cut the central hole first
result = result.faces(">Z").workplane().hole(inner_hole_diameter)

# Now, let's cut the spline teeth.
# The image shows internal rectangular-ish teeth.
# We can think of this as removing material to form the gaps, or adding material to form the teeth.
# Given the "hole" operation above, the easiest way to match the image (teeth protruding inward) 
# is to cut a larger hole and then add the teeth back, or cut the negative of the teeth.
# Let's try cutting the slots.

# Strategy: 
# 1. Create outer cylinder.
# 2. Create a "cutter" profile for the central void. 
#    This profile is a circle (inner diameter) combined with rectangular teeth.

# Let's rebuild the logic for a cleaner single-sketch extrusion if possible, or boolean operations.
# Boolean approach is often easier to read.

# Base cylinder
base = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height)

# Create the cutting tool for the splined hole
# Start with the minor diameter circle
cutter_sk = cq.Workplane("XY").circle(inner_hole_diameter / 2.0)

# Create a single tooth rectangle
# The tooth sits on the perimeter. 
# In the image, the "teeth" protrude inwards from a larger diameter.
# So the "void" is a star-like shape.
# Let's define the void shape.
# Center circle is the empty space passing through everything.
# The slots are the spaces between the teeth.

# Let's reverse the thinking: The image shows solid teeth protruding into a hole.
# So we have a hole of `spline_outer_diameter` and we keep material for the teeth.
# Actually, looking at the image:
# There is a central bore. 
# There are rectangular protrusions extending INWARDS from the wall of a larger bore.
# Let's assume the larger bore is `spline_outer_diameter`.
# The teeth extend inwards to `inner_hole_diameter`.

tooth_height = (spline_outer_diameter - inner_hole_diameter) / 2.0

# Method:
# 1. Create solid cylinder.
# 2. Cut the large hole (the root of the splines).
# 3. Add the teeth back in.

# 1. Solid Cylinder
result = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height)

# 2. Cut the major diameter hole
result = result.faces(">Z").workplane().hole(spline_outer_diameter)

# 3. Create a tooth to add back
# A tooth is a rectangle centered on the radius
tooth_thickness = spline_width
tooth_depth = (spline_outer_diameter - inner_hole_diameter) / 2.0

# We need to position the tooth correctly.
# The tooth needs to bridge the gap from inner_radius to outer_radius
inner_rad = inner_hole_diameter / 2.0
outer_rad = spline_outer_diameter / 2.0
tooth_center_rad = (inner_rad + outer_rad) / 2.0

tooth = (
    cq.Workplane("XY")
    .rect(tooth_thickness, tooth_depth + 1.0) # slightly longer to ensure overlap
    .extrude(height)
    .translate((0, tooth_center_rad, 0)) # Move to radius
)

# 4. Polar array the tooth and union them
for i in range(num_splines):
    angle = 360.0 / num_splines * i
    rotated_tooth = tooth.rotate((0,0,0), (0,0,1), angle)
    result = result.union(rotated_tooth)

# Ensure the final result is in the 'result' variable