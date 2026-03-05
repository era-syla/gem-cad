import cadquery as cq
import math

# --- Parameters ---
thickness = 8.0
hub_id = 60.0       # Inner diameter of the main pivot hole
hub_od = 80.0       # Outer diameter of the hub ring
pitch_radius = 130.0 # Approximate radius of the gear pitch circle
rim_width = 10.0    # Thickness of the outer rim
spoke_width = 10.0  # Width of the radial spokes
sector_angle = 110.0 # Total angle of the gear sector
num_teeth_full = 100 # Estimated tooth count for a full circle
module = (2 * pitch_radius) / num_teeth_full
tooth_height = 2.25 * module

# --- Helper Functions ---

def create_trapezoidal_tooth(m, thickness):
    """Creates a simplified gear tooth profile."""
    bottom_width = math.pi * m / 2.0
    top_width = bottom_width * 0.4
    height = 2.25 * m
    
    # Define profile centered at origin, pointing +Y
    pts = [
        (-bottom_width/2, 0),
        (-top_width/2, height),
        (top_width/2, height),
        (bottom_width/2, 0)
    ]
    return cq.Workplane("XY").polyline(pts).close().extrude(thickness)

def make_sector_arc(r_inner, r_outer, start_angle, end_angle, thickness):
    """Creates a solid arc segment."""
    # Calculate points for the arc shape
    def get_pt(r, angle):
        rad = math.radians(angle)
        return (r * math.cos(rad), r * math.sin(rad))
    
    p1_in = get_pt(r_inner, start_angle)
    p1_out = get_pt(r_outer, start_angle)
    p2_in = get_pt(r_inner, end_angle)
    p2_out = get_pt(r_outer, end_angle)
    
    mid_angle = (start_angle + end_angle) / 2
    pm_out = get_pt(r_outer, mid_angle)
    pm_in = get_pt(r_inner, mid_angle)
    
    return (cq.Workplane("XY")
            .moveTo(*p1_in)
            .lineTo(*p1_out)
            .threePointArc(pm_out, p2_out)
            .lineTo(*p2_in)
            .threePointArc(pm_in, p1_in)
            .close()
            .extrude(thickness))

# --- Main Geometry Construction ---

# 1. Base Hub Ring
hub = cq.Workplane("XY").circle(hub_od/2).extrude(thickness)

# 2. Outer Rim Arc
start_deg = 270 - sector_angle/2
end_deg = 270 + sector_angle/2
rim_id = pitch_radius - rim_width
rim_od = pitch_radius
rim = make_sector_arc(rim_id, rim_od, start_deg, end_deg, thickness)

# 3. Spokes
# Central Spoke (Vertical Down at 270)
spoke_len = rim_id - hub_od/2
spoke_shape = (cq.Workplane("XY")
               .rect(spoke_width, spoke_len + 5) # Extra length for overlap
               .extrude(thickness)
               .translate((0, -(hub_od/2 + spoke_len/2), 0)))

# Create Radial Spokes
spokes = spoke_shape # Center
spokes = spokes.union(spoke_shape.rotate((0,0,0),(0,0,1), 35))  # Left
spokes = spokes.union(spoke_shape.rotate((0,0,0),(0,0,1), -35)) # Right

# 4. Wing Extensions (Mounting points at ends of arc)
def create_wing(angle, is_right_side):
    """Creates the mounting wing at the sector limit."""
    rad = math.radians(angle)
    # Anchor point on the rim
    anchor_x = rim_od * math.cos(rad)
    anchor_y = rim_od * math.sin(rad)
    
    # Create a generic mounting tab shape
    # We construct it local to origin then rotate/translate
    w = 30
    h = 25
    wing = (cq.Workplane("XY")
            .moveTo(0,0)
            .lineTo(w, 0)
            .lineTo(w, h)
            .lineTo(0, h-5) # Taper
            .close()
            .extrude(thickness))
    
    # Align
    rotation = angle - 90 if is_right_side else angle + 90 + 180
    offset_x = 10 if is_right_side else -10 # Overlap
    
    wing = wing.translate((-w/2, 0, 0)).rotate((0,0,0),(0,0,1), rotation).translate((anchor_x, anchor_y, 0))
    return wing

wing_l = create_wing(start_deg, False)
wing_r = create_wing(end_deg, True)

# Assemble Frame
frame = hub.union(rim).union(spokes).union(wing_l).union(wing_r)

# 5. Gear Teeth
# Create a single tooth pointing -Y (270 deg)
tooth = create_trapezoidal_tooth(module, thickness)
tooth = tooth.rotate((0,0,0),(0,0,1), 180) # Point down
tooth = tooth.translate((0, -pitch_radius, 0)) # Move to radius

# Polar Array the teeth
step_angle = 360.0 / num_teeth_full
num_sector_teeth = int(sector_angle / step_angle) + 2
# Center the teeth on the arc
start_tooth_angle = 270 - (num_sector_teeth * step_angle)/2

all_teeth = cq.Workplane("XY")
for i in range(num_sector_teeth + 1):
    ang = start_tooth_angle + i * step_angle
    # Rotate the base tooth (which is at 270) to the target angle
    # Rotation diff = target - 270
    t = tooth.rotate((0,0,0), (0,0,1), ang - 270)
    frame = frame.union(t)

# 6. Cuts and Holes
# Main Pivot Hole
final_part = frame.cut(cq.Workplane("XY").circle(hub_id/2).extrude(thickness))

# Small Mounting Holes on Hub Ring (5 holes)
hole_radius = 2.5
hole_pcd = (hub_od + hub_id) / 2.0 / 2.0 # Radius of hole centers
for i in [-2, -1, 0, 1, 2]:
    ang = 270 + i * 20 # 20 degree separation
    hx = hole_pcd * math.cos(math.radians(ang))
    hy = hole_pcd * math.sin(math.radians(ang))
    final_part = final_part.cut(cq.Workplane("XY").moveTo(hx, hy).circle(hole_radius).extrude(thickness))

# Wing Notches (Simulated)
# Left
final_part = final_part.cut(
    cq.Workplane("XY").rect(8, 15).extrude(thickness)
    .translate((-5, 10, 0)) # Local adjustment
    .rotate((0,0,0),(0,0,1), start_deg + 90)
    .translate((rim_od * math.cos(math.radians(start_deg)), rim_od * math.sin(math.radians(start_deg)), 0))
)
# Right
final_part = final_part.cut(
    cq.Workplane("XY").rect(8, 15).extrude(thickness)
    .translate((5, 10, 0)) # Local adjustment
    .rotate((0,0,0),(0,0,1), end_deg - 90)
    .translate((rim_od * math.cos(math.radians(end_deg)), rim_od * math.sin(math.radians(end_deg)), 0))
)

# Apply fillets to internal web intersections for realism
try:
    # Select edges that are parallel to Z axis
    final_part = final_part.edges("|Z").fillet(2.0)
except:
    # Fallback if topology is too complex for auto-fillet
    pass

result = final_part