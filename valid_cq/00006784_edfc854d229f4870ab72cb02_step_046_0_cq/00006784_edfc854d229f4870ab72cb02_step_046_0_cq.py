import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions estimation
total_length = 50.0
outer_diameter = 16.0
wall_thickness = 1.5
inner_diameter = outer_diameter - (2 * wall_thickness)

# Smooth end section (Right side) parameters
smooth_end_length = 12.0

# Bellows parameters
# There appear to be two distinct sections of bellows/ribs separated by a small gap
# Section 1 (Middle-Right): Longer, more ribs
# Section 2 (Left): Shorter, fewer ribs
bellow_rib_radius = 1.5  # Radius of the semi-circular rib
bellow_pitch = 3.5      # Distance between rib centers
mid_gap_length = 3.0    # Gap between the two bellow sections
mid_gap_diameter = 6.0  # Narrow neck diameter in the gap

# Calculate number of ribs based on visual estimation
num_ribs_long_section = 7
num_ribs_short_section = 4

# --- Geometry Construction ---

# 1. Base Cylinder (Inner Bore)
# We will create the main shape and then shell it or hollow it out.
# Or better, construct the profile and revolve it. Revolve is usually cleaner for this.

def create_bellows_profile():
    # Start at the centerline (X-axis)
    
    # 1. Smooth End (Right Side)
    # Start at (0, 0) -> right end face center
    
    # Let's define the path along the outer profile from Right to Left
    
    # Setup workplane on XZ plane
    pts = []
    
    # Inner bore starts at X=0, Y=ID/2
    # But let's build the solid outer shape first and then cut the hole.
    
    # Let's define the axis along X.
    # X=0 is the rightmost face.
    
    current_x = 0.0
    
    # -- Smooth Cylindrical End --
    # From X=0 to X=-smooth_end_length
    pts.append((current_x, outer_diameter / 2.0))
    current_x -= smooth_end_length
    pts.append((current_x, outer_diameter / 2.0))
    
    # -- Long Bellows Section --
    # Each bellow is a hump. We can model them as sine waves or circular arcs.
    # Looking at the image, they look like rounded protrusions.
    # Let's use a custom profile for the ribs.
    
    for i in range(num_ribs_long_section):
        # A rib consists of a valley and a peak
        # Let's assume the outer diameter is the peak
        # Valley diameter
        valley_dia = outer_diameter - (2 * bellow_rib_radius)
        
        # We are currently at outer_diameter/2
        # Go down to valley
        pts.append((current_x, valley_dia / 2.0))
        
        # Arc for the rib
        # Center of arc
        center_x = current_x - (bellow_pitch / 2.0)
        center_y = valley_dia / 2.0
        
        # CadQuery polyline points for approximation or use specific spline/arc logic
        # For simplicity in a single profile list, straight lines are easier, 
        # but Spline is better for organic shapes.
        # Let's try to construct specific points for a Spline or just use simple geometry unions.
        
        current_x -= bellow_pitch

    # -- Gap Section --
    # The image shows a significant narrowing between the two rib sections.
    # It looks like a simple cylinder of smaller diameter.
    
    # Transition to gap
    gap_start_x = current_x
    pts.append((gap_start_x, mid_gap_diameter / 2.0))
    
    current_x -= mid_gap_length
    pts.append((current_x, mid_gap_diameter / 2.0))
    
    # -- Short Bellows Section --
    # Transition up from gap
    # Similar loop to previous
    
    # We need to get back to the start of the rib pattern
    # The logic above was a bit simplified for a single polyline. 
    # Let's change strategy: Build primitive shapes and union them. It's more robust in CQ.

    return None

# --- Revised Strategy: Constructive Solid Geometry (CSG) ---

# 1. The Smooth End Cylinder
smooth_end = cq.Workplane("YZ").circle(outer_diameter / 2).extrude(smooth_end_length)

# 2. The Long Bellows Section
# We create one rib and repeat it
def make_rib(od, id_val, width):
    # A toroidal shape or a disc with rounded edges
    # Let's use a revolved circle offset from center
    # Radius of the geometric circle forming the torus
    torus_r = (od - id_val) / 4.0 
    # Center distance from axis
    major_r = id_val / 2.0 + torus_r
    
    # Create the torus
    r = cq.Workplane("XZ").center(major_r, 0).circle(torus_r).revolve()
    
    # Often bellows are not perfect tori, but this is a good approximation.
    # Alternatively, just discs with fillets. 
    # Looking at the image, they look like stacked donuts.
    return r

# Let's use a simple revolve of a profile for the bellows to control the shape better.
# Profile: A series of bumps.

# Total length of long bellows section
len_long_bellows = num_ribs_long_section * bellow_pitch

# Path for the profile
path_pts = []
x_cursor = 0

# Start at valley radius
valley_rad = (outer_diameter / 2.0) - bellow_rib_radius

# Generate points for the long section (Right to Left in profile view)
path_pts.append((x_cursor, valley_rad))

for i in range(num_ribs_long_section):
    # Go up, over, down
    # We'll use a 3-point arc for the top of the rib
    p1 = (x_cursor, valley_rad)
    p2 = (x_cursor + bellow_pitch/2.0, outer_diameter/2.0) # Peak
    p3 = (x_cursor + bellow_pitch, valley_rad)
    
    # We store these to build the wires later
    x_cursor += bellow_pitch

# This approach with Splines is tricky to get water-tight.
# Let's go back to CSG with primitives, it's safer for this specific shape.

# --- Implementation ---

# 1. Smooth End
part = cq.Workplane("XY").circle(outer_diameter/2).extrude(smooth_end_length)

# 2. Long Bellows Stack
# We will construct a "rib" object and stack them.
# Rib geometry: A cylinder for the core, plus a torus or rounded disc for the outer part.
# Image analysis: The ribs look flattened, not perfectly circular cross-section.
# Let's use a cylinder with large fillets.

rib_thickness = bellow_pitch * 0.8
rib_gap = bellow_pitch * 0.2
core_dia = outer_diameter * 0.65

# Create a single rib
rib = (cq.Workplane("XY")
       .circle(outer_diameter/2)
       .extrude(rib_thickness)
       .edges().fillet(rib_thickness/2.1) # Round it off completely
      )

# Stack Long Section
current_z = smooth_end_length
for i in range(num_ribs_long_section):
    # Add a small connector cylinder (the valley)
    connector = (cq.Workplane("XY")
                 .workplane(offset=current_z)
                 .circle(core_dia/2)
                 .extrude(bellow_pitch)
                )
    part = part.union(connector)
    
    # Add the rib centered in the pitch
    # Offset slightly to center the rib on the connector
    rib_offset = current_z + (bellow_pitch - rib_thickness)/2.0
    placed_rib = rib.translate((0, 0, rib_offset))
    part = part.union(placed_rib)
    
    current_z += bellow_pitch

# 3. Middle Gap (The neck)
# Image shows a thin neck.
part = part.union(
    cq.Workplane("XY")
    .workplane(offset=current_z)
    .circle(mid_gap_diameter/2)
    .extrude(mid_gap_length)
)
current_z += mid_gap_length

# 4. Short Bellows Stack
for i in range(num_ribs_short_section):
    # Connector
    connector = (cq.Workplane("XY")
                 .workplane(offset=current_z)
                 .circle(core_dia/2)
                 .extrude(bellow_pitch)
                )
    part = part.union(connector)
    
    # Rib
    rib_offset = current_z + (bellow_pitch - rib_thickness)/2.0
    placed_rib = rib.translate((0, 0, rib_offset))
    part = part.union(placed_rib)
    
    current_z += bellow_pitch

# 5. Final End Cap / termination
# The image shows the last rib is the end. We might need a small flat face?
# The loop finishes with a rib, which is correct based on the left side of the image.

# 6. Hollow out the entire object
# Create a cylinder representing the hole and cut it.
# The hole goes all the way through.
hole = (cq.Workplane("XY")
        .circle(inner_diameter/2)
        .extrude(current_z + 10) # Oversize length
       )

result = part.cut(hole)

# Rotate to match image orientation (approximately isometric view with long axis on X or Y)
# The default view in many CAD viewers puts XY as ground. The image shows the cylinder lying down.
result = result.rotate((0,0,0), (1,0,0), -90)

if __name__ == "__main__":
    # If running in CQ-editor, this will render
    try:
        show_object(result)
    except NameError:
        pass