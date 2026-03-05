import cadquery as cq
import math

# --- Parameters ---
# Main T shape parameters
t_height = 100
t_width_top = 80
t_thickness = 10
pointy_tip_offset = 20  # How far the center tip extends down

# Curved top bar parameters
bar_radius = 80  # Radius of the arc for the top bar
bar_thickness = 8
bar_width = 10
bar_gap = 2 # Gap between main T and top bar

# Text parameters
text_string = "TESLA"
text_size = 12
text_depth = 2
text_radius_offset = 5 # Offset from the bar for text path

# --- Helper Functions ---

def make_tesla_t(height, top_width, thickness):
    """
    Creates the main body of the Tesla 'T' logo.
    Approximated using points and splines/lines.
    """
    # Define key points for half of the T (symmetric)
    # Origin is roughly the center of the arc at the top
    
    # Points for the right half outline
    # P1: Bottom tip
    p1 = (0, -height) 
    # P2: The sharp inner corner
    p2 = (15, -height + 40)
    # P3: The outer wing tip
    p3 = (top_width/2, -15)
    # P4: The inner curve start on top
    p4 = (10, -5)
    # P5: The center top notch
    p5 = (0, -15)

    # Create the profile
    path = (
        cq.Workplane("XY")
        .moveTo(p1[0], p1[1])
        .lineTo(p2[0], p2[1]) # Line up the stem
        # Curve out to the wing tip. 
        # Using a 3-point arc approximation or spline
        .spline([p3], tangents=[(0.5, 1), (1, 0.2)], includeCurrent=True)
        # Curve back to the center top
        .spline([p4, p5], includeCurrent=True)
        .mirrorY() # Mirror to create the full shape
    )
    
    # Extrude
    solid = path.extrude(thickness)
    
    # The shape in the image is slightly curved/arched along the top face.
    # For simplicity, we'll keep it flat but refine the profile if needed.
    # A simple extrusion is usually sufficient for logo approximations.
    
    return solid

def make_top_bar(radius, width, thickness, angle_sweep):
    """
    Creates the curved bar above the T.
    """
    # Create an arc profile
    inner_r = radius
    outer_r = radius + width
    
    # Using a 2D sketch approach
    bar = (
        cq.Workplane("XY")
        .moveTo(inner_r, 0)
        .lineTo(outer_r, 0)
        .revolve(angle_sweep, (0,0,0), (0,0,1)) # Revolve creates a segment
        .translate((-angle_sweep/2, 0, 0)) # This rotation logic is tricky with revolve, let's use extrude
    )
    
    # Alternative: Extrude a sketch of concentric arcs
    # We need an arc centered at origin, pointing upwards (Y+) relative to the T
    # The T points down in Y.
    
    # Let's rebuild the coordinate system concept.
    # Let (0,0) be the center of the arc.
    # The T points downwards (negative Y).
    
    outer_r = radius + width
    inner_r = radius
    
    # Calculate start/end points for the arc based on width/angle
    # We'll just approximate geometric width
    half_angle = 35 # degrees
    
    # Define points for the arc shape
    # P1: inner right
    p1_x = inner_r * math.sin(math.radians(half_angle))
    p1_y = inner_r * math.cos(math.radians(half_angle))
    
    # P2: outer right
    p2_x = outer_r * math.sin(math.radians(half_angle))
    p2_y = outer_r * math.cos(math.radians(half_angle))
    
    # P3: outer top (center)
    p3_x = 0
    p3_y = outer_r
    
    # P4: inner top (center)
    p4_x = 0
    p4_y = inner_r
    
    sketch = (
        cq.Workplane("XY")
        .moveTo(p1_x, p1_y)
        .lineTo(p2_x, p2_y)
        .radiusArc((0, outer_r), -outer_r) # Arc to center top
        .radiusArc((-p2_x, p2_y), -outer_r) # Arc to left
        .lineTo(-p1_x, p1_y) # Close left side
        .radiusArc((0, inner_r), inner_r) # Inner arc back to center
        .radiusArc((p1_x, p1_y), inner_r) # Inner arc back to start
        .close()
    )
    
    return sketch.extrude(thickness)


# --- Construction ---

# 1. Create the Main T
# We use a custom sketch approach to get the specific Tesla curvature
pts = [
    (0, -90),        # Bottom tip
    (6, -80),        # Slight width at bottom
    (20, -30),       # Mid stem
    (55, 5),         # Wing tip
    (45, 12),        # Top corner of wing
    (15, 0),         # Inner curve dip
    (0, -10)         # Center notch
]

# We need to be careful with spline tangents to get the sharp look
t_sketch = (
    cq.Workplane("XY")
    .moveTo(0, -90)
    .spline([(12, -40), (55, 5)], includeCurrent=True) # Right outer edge
    .lineTo(45, 12) # Top edge tip
    .spline([(15, 2), (0, -10)], includeCurrent=True) # Top inner curve
    .mirrorY() # Mirror the whole operation
)

main_t = t_sketch.extrude(t_thickness)


# 2. Create the Top Curved Bar
# The bar sits above the T.
# Let's center the arc slightly above the T wings.
bar_inner_radius = 60
bar_width = 12
bar_thickness = 10
bar_angle_half = 40

# Calculate arc points
bir = bar_inner_radius
bor = bar_inner_radius + bar_width

# Arc calculation helper
def get_xy(r, angle_deg):
    rad = math.radians(90 - angle_deg) # 0 is straight up (Y+)
    return (r * math.cos(rad), r * math.sin(rad))

p_in_start = get_xy(bir, -bar_angle_half)
p_out_start = get_xy(bor, -bar_angle_half)
p_out_mid = (0, bor)
p_out_end = get_xy(bor, bar_angle_half)
p_in_end = get_xy(bir, bar_angle_half)
p_in_mid = (0, bir)

bar_sketch = (
    cq.Workplane("XY")
    .moveTo(*p_in_start)
    .lineTo(*p_out_start)
    .threePointArc(p_out_mid, p_out_end)
    .lineTo(*p_in_end)
    .threePointArc(p_in_mid, p_in_start)
    .close()
)

# Position the bar. The T wing tips are around Y=12. 
# We want the bar to hover slightly above.
# The bar center (0,0) of the arc generation creates an arc centered at 0,0.
# We need to shift it down so the arc fits over the T.
top_bar = bar_sketch.extrude(bar_thickness).translate((0, -45, 0)) # Shift down manually to fit visual

# 3. Create the Text "TESLA"
# The text is embossed on the face of the Top Bar.
# CadQuery's textOnPath or simple projection can work.
# Given the image, the text follows the curve of the top bar.

text_path_radius = 66 # Middle of the bar roughly
text_angle_start = 140 # Degrees in polar coordinates for start
text_angle_end = 40   # Degrees in polar coordinates for end (span)

# We will create individual letters and rotate/place them
# Simple placement logic:
letters = ["T", "E", "S", "L", "A"]
spacing_angle = 12 # Degrees between letters
start_angle = (len(letters) - 1) * spacing_angle / 2

text_objs = cq.Assembly()

for i, letter in enumerate(letters):
    angle = start_angle - (i * spacing_angle)
    
    # Create letter geometry
    l = (
        cq.Workplane("XY")
        .text(letter, fontsize=10, distance=text_depth + 1, font="Arial", kind='bold')
    )
    
    # Rotate and translate to position on the arc
    # The arc center is roughly at (0, -45) based on previous translation
    r = 66 # Radius from the virtual center of the arc
    
    # Convert polar to cartesian
    # 0 degrees is "East", 90 is "North". We are working around 90 (Top)
    rad_angle = math.radians(90 + angle)
    x = r * math.cos(rad_angle)
    y = r * math.sin(rad_angle) - 45 # Apply the offset of the bar center
    
    # Rotate the letter to face outward
    l = l.rotate((0,0,0), (0,0,1), angle)
    l = l.translate((x, y, bar_thickness - text_depth))
    
    text_objs.add(l)

# 4. Combine Everything

# Union the T and the Bar
base_model = main_t.union(top_bar)

# Cut the text from the bar (embossed) or union (raised)?
# The image shows raised text sitting on a ledge, or possibly cut into the top edge.
# Looking closely at the prompt image, the text "TESLA" sits ON the step or is part of the bar structure.
# It actually looks like the text is placed on a shelf cut out of the bar, or simply raised on the bar.
# Let's assume Raised Text on the bar face.

final_assembly = base_model
for i, letter in enumerate(letters):
    # Recalculating positions for boolean union
    angle = start_angle - (i * spacing_angle)
    l = (
        cq.Workplane("XY")
        .text(letter, fontsize=8, distance=2, font="Arial", kind='bold')
    )
    
    # Position logic repeated for the solid objects
    r = 66 
    rad_angle = math.radians(90 + angle)
    x = r * math.cos(rad_angle)
    y = r * math.sin(rad_angle) - 45
    
    l = l.rotate((0,0,0), (0,0,1), angle)
    l = l.translate((x, y, bar_thickness)) # On top of the bar
    
    final_assembly = final_assembly.union(l)

result = final_assembly