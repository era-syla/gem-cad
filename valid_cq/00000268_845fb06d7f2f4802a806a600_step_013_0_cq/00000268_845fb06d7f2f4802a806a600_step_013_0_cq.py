import cadquery as cq

# Parameters
box_length = 80.0
box_width = 50.0
box_height = 30.0

# Wall thickness for the hollow inside (implied, though not fully visible, good practice for enclosures)
wall_thickness = 2.0

# Front features
knob_diameter = 12.0
knob_protrusion = 5.0
knob_x_offset = 10.0  # Offset from center
knob_y_offset = -5.0 # Offset from center vertically

rect_hole_width = 15.0
rect_hole_height = 8.0
rect_hole_depth = 5.0 # Or through, but let's make it an indent/connector slot
rect_hole_x_offset = -12.0
rect_hole_y_offset = 0.0

# Rear features
rear_cyl_diameter = 25.0
rear_cyl_length = 10.0

# Top mounting holes
hole_diameter = 3.0
hole_depth = 5.0
# Distance from edges
hole_inset_x = 5.0
hole_inset_y = 5.0

# Construct the main body
main_body = cq.Workplane("XY").box(box_length, box_width, box_height)

# Create the knob on the front face (min X face)
# Note: box is centered at origin. 
# Front face is at x = -box_length/2
# Rear face is at x = box_length/2
# Left face is at y = -box_width/2
# Right face is at y = box_width/2
# Top face is at z = box_height/2

# Let's orient based on the isometric view:
# Let the large flat face with holes be Top (Z+)
# Let the face with the knob be Front (Y-)
# Let the long dimension run along X.

# Re-evaluating orientation for easier coding to match standard views:
# Box dimensions: Length (X), Width (Y), Height (Z)
# View shows Length is likely X, Width is Y, Height is Z.
# Let's assume:
# - Length (long axis): X
# - Width (short axis on top): Y
# - Height (vertical axis): Z

# Actually, looking at the image:
# The face with the knob and rectangle is one of the smaller end faces.
# The large face with 4 holes is the top.
# Let's define:
# - Length along the long axis (Top face long edge)
# - Width along the short axis (Top face short edge)
# - Height (Thickness of the box)

length = 80.0 # Long axis
width = 40.0  # Short axis
height = 30.0 # Vertical

# Base block
result = cq.Workplane("XY").box(length, width, height)

# 1. Front Face Features (Face at -X)
# We need to select the face at -X
front_face = result.faces("<X").workplane()

# Add the knob (cylinder protrusion)
# Positioning: It looks to be in the lower right quadrant of the front face (relative to viewing it head-on)
knob_y_pos = -width/4 + 2 # Shifted towards right side of face in image (which is -Y in global if X is long axis? No, let's stick to local coordinates)
# Local coords on <X face: X is global Y, Y is global Z.
# Center of face is (0,0).
# Image: Knob is bottom-right.
knob_local_x = -width/4  # Global Y direction
knob_local_y = -height/4 # Global Z direction

result = (result.faces("<X").workplane()
          .center(width/4, -height/4) # Shift to bottom right of that face
          .circle(knob_diameter/2)
          .extrude(knob_protrusion)
          )

# Add the rectangular cutout
# Image: Rectangle is mid-left.
rect_local_x = -width/4
rect_local_y = 0

result = (result.faces("<X").workplane()
          .center(-width/4, 0) # Shift to left
          .rect(rect_hole_width, rect_hole_height)
          .cutBlind(-rect_hole_depth)
          )

# 2. Rear Face Feature (Face at +X)
# Large cylinder sticking out
result = (result.faces(">X").workplane()
          .circle(rear_cyl_diameter/2)
          .extrude(rear_cyl_length)
          )

# 3. Top Face Holes (Face at +Z)
# 4 screw holes near the corners
x_dist = length/2 - hole_inset_x
y_dist = width/2 - hole_inset_y

result = (result.faces(">Z").workplane()
          .rect(x_dist*2, y_dist*2, forConstruction=True) # Construction rectangle for corners
          .vertices()
          .hole(hole_diameter, hole_depth)
          )

# Optional: Add fillets to vertical edges for realism (looks sharp in image, but slight fillet is good)
# result = result.edges("|Z").fillet(0.5)

# Final Result
# The variable 'result' contains the geometry