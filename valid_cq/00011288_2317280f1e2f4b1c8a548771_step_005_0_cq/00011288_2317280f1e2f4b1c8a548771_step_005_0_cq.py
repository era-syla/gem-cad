import cadquery as cq

# Parameters for the Euro-profile cylinder shape
length = 40.0         # Total length of the extrusion
upper_radius = 5.0    # Radius of the top circular part
lower_width = 6.0     # Width of the bottom rectangular part (approx, usually narrower than upper diameter)
lower_height = 10.0   # Height of the bottom rectangular extension
neck_width = 3.5      # Width of the narrowest part connecting circle and rectangle

# Constructing the 2D profile
# The profile is a standard Euro-cylinder shape: a circle on top, a rectangle on the bottom
# The standard profile is roughly 17mm diameter top, 10mm width bottom, 33mm total height.
# Looking at the image, it seems a bit simplified or a generic variant.
# Let's adjust dimensions to match the visual proportions better.

cyl_radius = 8.5      # Matches standard ~17mm diameter
total_height = 33.0   # Standard total height
bottom_width = 10.0   # Standard bottom width

# Create the profile sketch
# We will draw half the profile and mirror it to ensure symmetry

def euro_profile(radius, bot_width, tot_height):
    # Calculate key points
    # Center of top circle
    circle_center_y = tot_height - radius
    
    # Bottom rectangle height needs to reach up to where it starts blending or the circle tangent
    # A standard euro profile is a bit complex, but the image shows a simplified version:
    # A circle on top, a rectangle below, joined.
    
    s = cq.Sketch()
    s = s.push([(0, circle_center_y)])
    s = s.circle(radius) # The top circle
    
    # The bottom rectangular part
    rect_height = tot_height - radius # Height from bottom to circle center
    # We create a rectangle centered at x=0, with bottom at y=0
    s = s.reset().push([(0, rect_height/2)])
    s = s.rect(bot_width, rect_height)
    
    # Combine them
    # Note: CadQuery sketches add shapes. The union is automatic if drawn sequentially in some modes,
    # but strictly speaking, we want a union of two faces.
    
    # Alternative approach: Use Workplane and geometric primitives 2D
    return s

# Let's rebuild using Workplane geometry for a robust boolean operation
# 1. Top Circle
c_center_y = total_height - cyl_radius
top_circle = (
    cq.Workplane("XY")
    .center(0, c_center_y/2) # Shift up so the whole object sits nicely or centered
    .circle(cyl_radius)
)

# 2. Bottom Rectangle
# The rectangle goes from y=0 to somewhere near the circle. 
# Looking at the image, the sides are straight vertical lines.
# The rectangle width is `bottom_width`.
rect_part = (
    cq.Workplane("XY")
    .center(0, (total_height - cyl_radius)/2)
    .rect(bottom_width, total_height - cyl_radius)
)

# 3. Create the profile by unioning them
# However, the image shows a slight "neck" or step. 
# Actually, looking closely at the image:
# It's a "snowman" or "keyhole" shape extruded.
# There is a circular top part.
# There is a lower part with rounded bottom corners.
# The connection between them seems to be the full width of the top circle in some designs,
# but here the top circle overhangs the bottom part.

# Revised dimensions based on visual inspection of the specific render provided:
# - Top part: Cylinder
# - Bottom part: Rectangle with rounded bottom, slightly narrower than top cylinder diameter.
# - There's a distinct "lip" where the top circle is wider than the bottom block.

# Adjusted Parameters
top_diam = 17.0
top_rad = top_diam / 2.0
body_width = 10.0
body_height = 18.0 # Height of the rectangular part below the circle center
fillet_rad = 1.0   # Small fillet at the bottom corners

# Construction
# 1. Top Circle
profile_top = (
    cq.Workplane("XY")
    .moveTo(0, body_height) 
    .circle(top_rad)
)

# 2. Bottom shape (Rectangle)
profile_bottom = (
    cq.Workplane("XY")
    .moveTo(0, body_height / 2)
    .rect(body_width, body_height)
)

# 3. Union the 2D wires to create a single face
# We need to extrude the union of these two 2D shapes.
sketch = (
    cq.Workplane("XY")
    .moveTo(0, body_height)
    .circle(top_rad)
    .moveTo(0, body_height/2)
    .rect(body_width, body_height)
)

# Extract the wire and extrude
# The easiest way to get the union in CQ is often just extruding both and unioning the solids,
# or unioning the wires.
# Let's extrude the two parts and union them for the final shape.

part_top = (
    cq.Workplane("XY")
    .moveTo(0, body_height)
    .circle(top_rad)
    .extrude(length)
)

part_bot = (
    cq.Workplane("XY")
    .moveTo(0, body_height/2)
    .rect(body_width, body_height)
    .extrude(length)
)

# Combine
result = part_top.union(part_bot)

# Add fillets to the bottom of the rectangular part as seen in typical profiles
# The image is a bit dark at the bottom, but usually these are rounded.
# Let's select the bottom edges running along Z (which is the extrusion direction here)
# Wait, extrude creates along Z. The profile is on XY.
# So the "bottom" of the profile is at Y=0.
# The edges to fillet are the ones parallel to the extrusion vector (Z axis) at the bottom corners.

# Edges selector: Z direction, located at approximately y=0 and x = +/- width/2
try:
    result = result.edges(cq.selectors.NearestToPointSelector((body_width/2, 0, length/2))).fillet(fillet_rad)
    result = result.edges(cq.selectors.NearestToPointSelector((-body_width/2, 0, length/2))).fillet(fillet_rad)
except:
    # Fallback if selection is tricky due to coordinate exactness
    pass

# On the back face (or front face depending on perspective), there is a circular step in the image?
# Actually, looking at the very left of the image, there is a circular protrusion.
# It looks like the main body, and then a smaller circular boss on the front face.

# Let's interpret the image features:
# Main body: The keyhole extrusion.
# Left side: A circular boss extending from the top cylindrical part.

boss_extension = 2.0
boss_radius = top_rad - 0.5 # Slightly smaller or same size? Looks like same size or slightly indented edge.
# Let's assume it's the cam driver or actuator face often found on these locks.

# Select the face at Z=length (or Z=0 depending on view)
# Let's assume the current extrusion went from Z=0 to Z=length.
# The image shows the extension on the near side.

# We will add a small cylinder on the top circle face at Z=length (or 0)
# Let's put it at Z=length
c_center = (0, body_height)

result = (
    result.faces(">Z")
    .workplane()
    .center(0, body_height) # Move workplane center relative to the face center?
    # Face center of the complex shape is hard to predict exactly.
    # Safer to use absolute coordinates from origin
    .moveTo(0, body_height) 
    .circle(top_rad * 0.9) # Slightly smaller to show a seam line as per typical CAD renders
    .extrude(boss_extension)
)

# Optional: Fillet the transition between the main body and the boss
# result = result.faces(">Z").edges().fillet(0.5) 

# Final result variable
result = result