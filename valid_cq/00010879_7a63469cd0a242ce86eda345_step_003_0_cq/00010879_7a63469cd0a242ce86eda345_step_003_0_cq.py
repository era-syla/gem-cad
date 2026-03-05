import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
width = 200.0
height = 100.0
thickness = 5.0

# Frame and beam dimensions
frame_width = 10.0
vertical_bar_width = 10.0
diagonal_bar_width = 10.0

# Hole dimensions
hole_diameter = 6.0
hole_margin = frame_width / 2.0  # Center holes on the frame

# --- Modeling ---

# 1. Create the base plate (outer rectangle)
base_plate = cq.Workplane("XY").box(width, height, thickness)

# 2. Define the cutout regions
# We will create pockets to remove material, leaving the frame and beams.
# The structure consists of:
# - An outer frame
# - A central vertical bar
# - Two diagonal bars radiating from the bottom-center

# Calculate inner dimensions for the pockets
inner_w = width - 2 * frame_width
inner_h = height - 2 * frame_width

# The central vertical bar splits the inner area into left and right halves
left_half_center_x = -(width / 4.0)
right_half_center_x = (width / 4.0)

# Create the main cutout shape (a large rectangle representing the inner area)
# We will use this as a reference or cut it entirely and then add bars back? 
# Actually, sketching the negative spaces (triangles) is often easier for trusses.

# Let's sketch the cutouts directly on the face.
sketch = (
    cq.Workplane("XY")
    .workplane(offset=thickness/2)
    .sketch()
)

# Coordinates helper
# Top Left Inner Corner: (-w/2 + fw, h/2 - fw)
# Top Right Inner Corner: (w/2 - fw, h/2 - fw)
# Bottom Left Inner Corner: (-w/2 + fw, -h/2 + fw)
# Bottom Right Inner Corner: (w/2 - fw, -h/2 + fw)
# Bottom Center Inner: (0, -h/2 + fw)
# Top Center Inner: (0, h/2 - fw)

x_min = -width/2 + frame_width
x_max = width/2 - frame_width
y_min = -height/2 + frame_width
y_max = height/2 - frame_width

# Left Vertical strut logic:
# We have a vertical bar at x=0. So the left cutout area ends at x = -vertical_bar_width/2
# The right cutout area starts at x = vertical_bar_width/2

x_mid_left = -vertical_bar_width / 2
x_mid_right = vertical_bar_width / 2

# Left side diagonal:
# Goes from bottom-center to top-left corner region.
# Let's define the points for the "Left Triangle" (which is actually a trapezoid split by a diagonal)
# Actually, looking at the image:
# The left side has a diagonal going from the bottom-center up to the top-left corner.
# This splits the left rectangle into two triangles.

# Right side diagonal:
# Goes from bottom-center to top-right (but wait, looking closely at the image...)
# Image analysis:
# - There is a central vertical post.
# - Left side: Diagonal goes from bottom-center strut connection to top-left corner.
# - Right side: Diagonal goes from bottom-center strut connection to middle-right frame? 
#   Looking at the right side, the triangle is flatter. The diagonal goes from bottom-center to... 
#   Wait, looking closer at the crop.
#   Left side: Diagonal from Bottom-Center to Top-Left.
#   Right side: Diagonal from Bottom-Center to... slightly below top-right? No, it looks like it hits the right vertical frame at about mid-height or slightly higher.
#   Let's assume for symmetry or standard design it hits a specific point or just creates a triangle.
#   Actually, looking at the right side triangle, the top edge is horizontal. The diagonal goes from the bottom-center to the Right Frame.
#   This creates a triangle on the bottom and a trapezoid on top.

# Let's re-evaluate the geometry strategy. Instead of complex subtraction, let's build the positive shape (union).
# It's often robust for trusses.

# 1. Outer Frame
outer_frame = (
    cq.Workplane("XY")
    .rect(width, height)
    .rect(width - 2*frame_width, height - 2*frame_width)
    .extrude(thickness)
)

# 2. Vertical Bar (Center)
vertical_bar = (
    cq.Workplane("XY")
    .rect(vertical_bar_width, height - 2*frame_width)
    .extrude(thickness)
)

# 3. Left Diagonal (Bottom Center to Top Left)
# Angle calculation or point-to-point. 
# Start point (approx): (0, -height/2 + frame_width) -> actually intersection of beams
# End point (approx): (-width/2 + frame_width, height/2 - frame_width)

# Let's use a path extrude or a hull of circles/rectangles, or simply a rotated rectangle.
# Point-to-point is easiest with a custom sketch or simple rect rotation.

# Center point of the truss convergence at bottom: (0, -height/2 + frame_width/2)
p_convergence = (0, -height/2 + frame_width/2)

# Target Left: Top Left inner corner area.
p_top_left = (-width/2 + frame_width/2, height/2 - frame_width/2)

# Target Right: Mid-Right frame area.
# Based on the image, the right diagonal hits the right-side vertical frame.
# It seems to hit it slightly above the middle. Let's assume it hits at Y=0 or slightly up. 
# Or maybe it simply connects the bottom center to the right frame.
# Let's look really closely at the right side. The triangle formed has vertices: (Bottom-Center), (Bottom-Right), (Right-Frame-Something).
# It looks like the diagonal goes from Bottom-Center to (Width/2, SomeY).
# Let's assume for the right side, it's a diagonal to a point on the right edge, perhaps aligning with the top of the left diagonal? No, it looks distinct.
# Let's assume the right diagonal goes to the middle of the right vertical leg (y=0).

p_right_mid = (width/2 - frame_width/2, 0)

# Constructing the diagonals as thin rectangles rotated and positioned is tricky to get perfect joins.
# A more robust way in CadQuery 2D sketches is constructing the wires of the beams.

def create_truss_plate():
    # Outer rectangle
    r_outer = cq.Workplane("XY").rect(width, height)
    
    # Inner Cutouts
    # We define the negative spaces (the holes)
    
    # Common margins
    l = -width/2 + frame_width
    r = width/2 - frame_width
    b = -height/2 + frame_width
    t = height/2 - frame_width
    
    c_left = -vertical_bar_width/2
    c_right = vertical_bar_width/2
    
    # Left Side Cutouts
    # Diagonal splits the left area (l to c_left, b to t)
    # The diagonal goes from (0, b) to (l, t).
    # Since the diagonal has width, we offset the cutouts.
    
    # Vector for left diagonal
    # The logic is simpler: Draw the full rectangle, then draw the beams on top of it, then intersect? 
    # No, Union is better.
    
    # Let's build the "Skeleton" of the beams and extrude.
    
    # 1. Frame
    part = cq.Workplane("XY").rect(width, height).rect(width - 2*frame_width, height - 2*frame_width).extrude(thickness)
    
    # 2. Vertical Post
    v_post = cq.Workplane("XY").rect(vertical_bar_width, height - 2*frame_width).extrude(thickness)
    part = part.union(v_post)
    
    # 3. Diagonals
    # We will define a sketch with lines representing the centerlines of the diagonals, 
    # then offset them to create the bars.
    
    # Left Diagonal Centerline: (0, -height/2 + frame_width/2) to (-width/2 + frame_width/2, height/2 - frame_width/2)
    # Right Diagonal Centerline: (0, -height/2 + frame_width/2) to (width/2 - frame_width/2, 0) -> Estimate Y=0 based on image
    
    # Using a helper function to create a bar between two points
    def make_bar(p1, p2, w, th):
        length = ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5
        angle = cq.Workplane("XY").plane.toLocalCoords(cq.Vector(p2[0], p2[1], 0) - cq.Vector(p1[0], p1[1], 0)).getAngle(cq.Vector(1, 0, 0))
        # angle is in radians, convert to degrees
        import math
        deg = math.degrees(angle)
        
        center = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
        
        return (
            cq.Workplane("XY")
            .center(*center)
            .rect(length, w)
            .rotate((0,0,1), (0,0,0), deg)
            .extrude(th)
        )

    # Coordinates for connections (center of beams)
    # Bottom Center
    p_bc = (0, -height/2 + frame_width/2)
    # Top Left Corner
    p_tl = (-width/2 + frame_width/2, height/2 - frame_width/2)
    # Right Side Mid-ish point. Looking at the image, the triangle apex is on the right frame.
    # The triangle looks like an Isosceles triangle with base on the bottom frame?
    # No, it's a right triangle. The diagonal connects Bottom-Center to the Right-Edge.
    # The height of the connection on the right edge looks to be about 1/3 to 1/2 up.
    # Let's assume it hits the corner of the inner cutout for a cleaner look if possible, but the image shows it distinct.
    # Let's set the target on the right frame at Y=0 (middle).
    p_rm = (width/2 - frame_width/2, 0)
    
    # However, looking extremely closely at the provided image:
    # Left Side: There are two cutouts. One triangle, one trapezoid/triangle.
    # The diagonal goes from the "hub" at the bottom center, up to the top left corner.
    
    # Right Side: There is one triangular cutout and one trapezoid (or rectangle?).
    # Wait, the right side in the image shows a diagonal going from the bottom-center hub...
    # to the RIGHT FRAME.
    # And there is a horizontal-ish top edge. 
    # Actually, looking at the right side cutouts:
    # There is a triangle on the bottom right.
    # There is a shape above it. 
    # The diagonal goes from (Center-Bottom) to (Right-Frame-Mid).
    
    bar_left = make_bar(p_bc, p_tl, diagonal_bar_width, thickness)
    bar_right = make_bar(p_bc, p_rm, diagonal_bar_width, thickness)
    
    part = part.union(bar_left).union(bar_right)
    
    # Cleanup: The union of rotated rectangles leaves messy corners on the outside if they protrude, 
    # but since we defined points inside the frame, they are contained or buried.
    # However, to be safe, we can intersect with the bounding box or just rely on the design.
    # The 'frame' logic earlier puts the frame *around* the center area.
    # If the bars overlap the hole of the frame but not the outer edge, it's fine.
    
    return part

# Generate the main geometry
result = create_truss_plate()

# 4. Add Holes
# Holes are in the four corners of the frame.
corner_offset = hole_margin
hx = width/2 - corner_offset
hy = height/2 - corner_offset

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-hx, hy),  # Top Left
        (hx, hy),   # Top Right
        (-hx, -hy), # Bottom Left
        (hx, -hy)   # Bottom Right
    ])
    .hole(hole_diameter)
)