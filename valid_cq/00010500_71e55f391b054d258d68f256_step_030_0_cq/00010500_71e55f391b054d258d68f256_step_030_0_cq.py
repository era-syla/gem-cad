import cadquery as cq
import math

# --- Parameters ---
# Main body parameters
body_width = 80.0  # Width of the octagonal profile
body_length = 50.0 # Extrusion depth of the main housing
chamfer_size = 3.0 # Chamfer on the front/back edges

# Mounting flange (front face) parameters
flange_thickness = 4.0
flange_hole_dia = 3.5
flange_bolt_pattern_radius = 35.0

# Central Hub/Cone parameters
cone_base_dia = 30.0
cone_top_dia = 15.0
cone_height = 30.0
cone_tip_hole_dia = 4.0
cone_tip_chamfer = 1.0

# Internal Structure (Spokes/Grill)
grill_thickness = 3.0
grill_inset = 5.0 # How deep the grill is inside the housing

# Pattern on the side
pattern_groove_depth = 0.5
pattern_groove_width = 1.0

# Mounting Ears/Lugs
ear_cylinder_dia = 12.0
ear_cylinder_len = 30.0
ear_standoff_height = 12.0 # Height from body surface to center of cylinder
ear_thickness = 5.0 # Thickness of the connecting rib

# --- Helper Functions ---

def create_octagon(size):
    """Creates an octagon points list based on width flat-to-flat"""
    # Half width
    h = size / 2.0
    # Side length for a regular octagon from apothem (h) is 2 * h * tan(22.5 deg)
    s_half = h * math.tan(math.radians(22.5))
    
    pts = [
        (h, s_half), (h, -s_half),
        (s_half, -h), (-s_half, -h),
        (-h, -s_half), (-h, s_half),
        (-s_half, h), (s_half, h)
    ]
    return pts

# --- Main Modeling ---

# 1. Main Octagonal Housing Body
pts = create_octagon(body_width)
main_body = (
    cq.Workplane("XY")
    .polyline(pts).close()
    .extrude(body_length)
    .edges("|Z").fillet(2.0) # Smooth the vertical edges slightly
)

# Chamfer front and back edges
main_body = main_body.edges(">Z or <Z").chamfer(chamfer_size)

# Hollow out the inside to make it a housing
wall_thickness = 4.0
internal_cut = (
    cq.Workplane("XY")
    .polyline(create_octagon(body_width - 2*wall_thickness)).close()
    .extrude(body_length)
)

# We want the front face to have the mounting flange look
# Let's create the flange rim separately and union it, or just cut properly.
# The image shows a black rim. Let's model the rim.
rim_face = (
    cq.Workplane("XY").workplane(offset=body_length)
    .polyline(pts).close()
    .extrude(flange_thickness)
)

# Combine body and rim
housing = main_body.union(rim_face)

# Cut the main internal bore, leaving a back wall if needed, but let's assume through or deep pocket
# Based on image, it looks hollow with a grill inside.
housing = housing.cut(internal_cut.translate((0,0,-2))) # Leave some back wall or just cut through? 
# Let's cut mostly through but keep the structure. Actually, let's just shell it effectively.
housing = (
    cq.Workplane("XY")
    .polyline(pts).close()
    .extrude(body_length + flange_thickness)
    .faces(">Z").shell(-wall_thickness)
)


# 2. Mounting Flange Holes (Hexagonal pattern typically, or Octagonal)
# The image shows 6 bolts on the black rim.
housing = (
    housing.faces(">Z").workplane()
    .polarArray(flange_bolt_pattern_radius, 0, 360, 6)
    .circle(flange_hole_dia / 2.0)
    .cutThruAll()
)

# 3. Central Cone and Grill Structure
# Create the central cone
cone = (
    cq.Workplane("XY").workplane(offset=body_length - grill_inset) # Start inside
    .circle(cone_base_dia/2)
    .workplane(offset=cone_height)
    .circle(cone_top_dia/2)
    .loft()
)

# Add chamfer/detail to cone tip
cone = cone.faces(">Z").chamfer(cone_tip_chamfer)
cone = cone.faces(">Z").hole(cone_tip_hole_dia, depth=5)

# Create the grill/spokes
# The image shows an intricate overlapping circular pattern. 
# We'll approximate this with a geometric pattern of spokes/rings for robustness.
grill_plate = (
    cq.Workplane("XY").workplane(offset=body_length - grill_inset)
    .circle(body_width/2 - wall_thickness).extrude(grill_thickness)
)

# Create a cutter for the grill pattern
grill_pattern_cutter = cq.Workplane("XY").workplane(offset=body_length - grill_inset - 1)

# Central hole for airflow around cone base
grill_pattern_cutter = grill_pattern_cutter.circle(cone_base_dia/2 - 0.1).extrude(grill_thickness + 2)

# Pattern of holes (simulating the complex mesh)
for angle in range(0, 360, 60):
    # Outer petal cuts
    grill_pattern_cutter = grill_pattern_cutter.union(
        cq.Workplane("XY").workplane(offset=body_length - grill_inset - 1)
        .center(0, 0)
        .polarArray(20, angle, 360, 1) # Position
        .circle(8) # Size of cutout
        .extrude(grill_thickness + 2)
    )
    # Inner petal cuts
    grill_pattern_cutter = grill_pattern_cutter.union(
        cq.Workplane("XY").workplane(offset=body_length - grill_inset - 1)
        .center(0, 0)
        .polarArray(12, angle + 30, 360, 1) # Position
        .circle(4) # Size of cutout
        .extrude(grill_thickness + 2)
    )

grill = grill_plate.cut(grill_pattern_cutter)

# Union internal parts
result = housing.union(cone).union(grill)


# 4. Mounting Ears (Top and Bottom)
def create_lug(angle_pos):
    # Define local workplane on the side of the octagon
    # Octagon apothem is body_width/2
    apothem = body_width / 2.0
    
    # Create the cylindrical pivot
    lug_cyl = (
        cq.Workplane("XZ")
        .workplane(offset=apothem + ear_standoff_height)
        .circle(ear_cylinder_dia / 2.0)
        .extrude(ear_cylinder_len)
        .translate((0, 0, -ear_cylinder_len/2)) # Center lengthwise
    )
    
    # Create the connecting rib/stand
    # Profile in YZ plane (relative to global, but we need to orient correctly)
    
    # We construct a shape that lofts from the body to the cylinder
    lug_rib = (
        cq.Workplane("YZ")
        .workplane(offset=0) # Center of body
        .moveTo(apothem - 2, -ear_cylinder_len/2 + 5)
        .lineTo(apothem + ear_standoff_height, -ear_cylinder_len/2 + 5)
        .lineTo(apothem + ear_standoff_height, ear_cylinder_len/2 - 5)
        .lineTo(apothem - 2, ear_cylinder_len/2 - 5)
        .close()
        .extrude(ear_thickness)
        .translate((-ear_thickness/2, 0, 0)) # Center thickness
        .rotate((0,0,0), (0,1,0), -90) # Rotate to align with Z axis extrusion of body
    )
    
    # Refine rib shape (fillets)
    lug_rib = lug_rib.edges("|X").fillet(2.0)

    # Combine
    lug = lug_cyl.union(lug_rib)
    
    # Position the lug along the Z axis (length of body)
    lug = lug.translate((0, 0, body_length/2))
    
    # Rotate around Z axis to position on top or bottom
    lug = lug.rotate((0,0,0), (0,0,1), angle_pos)
    
    return lug

# Add Top Lug (90 degrees roughly, dependent on octagon orientation)
# Our octagon has flat top. Top face normal is (0,1,0).
# The create_lug function assumes building on XZ plane translated up Y.
top_lug = create_lug(90)
bottom_lug = create_lug(-90)

result = result.union(top_lug).union(bottom_lug)


# 5. Side Pattern (Diamond/Zig-zag grooves)
# This is complex to wrap, so we will project cut onto the side faces.
# We will do this for one side face and array/mirror if needed, but the image shows it on the left.

def create_side_pattern():
    # Work on a face. Let's pick the -X face.
    # Dimensions of side face: Width = side_len_octagon, Height = body_length
    s_len = (body_width/2) * math.tan(math.radians(22.5)) * 2
    
    # Create a sketch for the zig-zag
    pattern_sketch = (
        cq.Workplane("YZ")
        .workplane(offset=body_width/2) # Move to surface
        .center(0, body_length/2) # Center on face
        # Create diamond shapes
        .rect(s_len * 0.7, body_length * 0.3, centered=True)
        .rect(s_len * 0.4, body_length * 0.15, centered=True)
    )
    
    # We need to subtract this.
    # Since we are wrapping around an octagon, simple projection is easiest per face.
    
    # Let's apply to the left-most face (-X direction)
    # Rotate workplane to face left
    pts_pattern = [
        (-s_len/2 + 5, 10), (0, 20), (s_len/2 - 5, 10), (0,0), (-s_len/2 + 5, 10)
    ]
    
    # Generating the cut solid
    cut_shape = (
        cq.Workplane("YZ")
        .workplane(offset=body_width/2 - pattern_groove_depth)
        .moveTo(-s_len/2 + 5, 10)
        .polyline(pts_pattern).close()
        .extrude(pattern_groove_depth * 2)
        .translate((-body_width/2 - pattern_groove_depth, 0, body_length/4)) # Rough positioning
    )
    
    # Create a few stacked diamonds
    cut_shape2 = cut_shape.translate((0, 0, 15))
    cut_shape3 = cut_shape.translate((0, 0, -15))
    
    return cut_shape.union(cut_shape2).union(cut_shape3)

# Apply pattern cut to the side (Rotate -90 to get to -X side)
# This is a simplification. Real pattern mapping requires advanced surface logic.
# We will skip the complex texture to ensure code robustness and focus on macro geometry.
# Instead, let's add the distinct horizontal groove line seen in the middle of the side.

side_groove = (
    cq.Workplane("XY")
    .polyline(create_octagon(body_width + 1.0)).close() # Slightly larger
    .extrude(1.0) # Width of groove
    .translate((0, 0, body_length / 2.0))
)

side_groove_inner = (
    cq.Workplane("XY")
    .polyline(create_octagon(body_width - 0.5)).close() # Slightly smaller (cut depth)
    .extrude(1.0)
    .translate((0, 0, body_length / 2.0))
)

groove_cutter = side_groove.cut(side_groove_inner)
result = result.cut(groove_cutter)

# Clean up overlaps
result = result.clean()

# Final output
result = result