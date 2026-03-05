import cadquery as cq
import math

# Build a bicycle helmet shape using basic CadQuery primitives
# The helmet is essentially an ellipsoidal dome with vents cut out

# Main helmet shell dimensions
helmet_width = 220  # mm side to side
helmet_length = 260  # mm front to back
helmet_height = 160  # mm tall

# Create the main dome shape using a sphere scaled to ellipsoid proportions
# We'll build it by revolving a profile

# Create base ellipsoid-like shape for the helmet
# Use a 2D profile revolved around Z axis, then stretched

def make_helmet():
    # Create main dome - start with a sphere-like shape
    # Profile for revolution: quarter ellipse from top to equator
    
    r_x = helmet_width / 2   # 110
    r_y = helmet_length / 2  # 130
    r_z = helmet_height       # 160
    
    # Create the outer shell as a stretched sphere approximation
    # Build using loft through cross sections at different heights
    
    heights = [0, 20, 50, 90, 130, 160]
    # Radii at each height level (ellipsoidal profile)
    # At h=0 (bottom): largest opening
    # At h=160 (top): point/small
    
    def ellipse_radius(h, h_max, r_base):
        # Parametric ellipse: r = r_base * sqrt(1 - (h/h_max)^2)
        ratio = h / h_max
        return r_base * math.sqrt(max(0.001, 1 - ratio**2))
    
    # Build helmet dome using a revolved profile
    # Create 2D profile in XZ plane
    pts = []
    n = 20
    for i in range(n + 1):
        angle = math.pi / 2 * i / n  # 0 to 90 degrees
        x = r_x * math.cos(angle)
        z = r_z * math.sin(angle)
        pts.append((x, z))
    
    # Create the profile as a wire and revolve
    profile_pts = [(0, 0)] + pts + [(0, r_z)]
    
    # Use a simpler approach: create ellipsoid via scaling a sphere
    # CadQuery doesn't have scale on workplane, so use BRep transforms
    
    import cadquery as cq
    from cadquery import Vector
    
    # Create sphere and transform using cq.Shape methods
    # Build the dome shape manually with a revolved ellipse
    
    # 2D profile for the dome (in XZ plane, revolved around Z)
    profile = (
        cq.Workplane("XZ")
        .moveTo(0, 0)
        .lineTo(r_x, 0)
        .spline(
            [(r_x * 0.95, r_z * 0.3),
             (r_x * 0.7, r_z * 0.7),
             (r_x * 0.2, r_z * 0.97)],
        )
        .lineTo(0, r_z)
        .close()
    )
    
    dome = profile.revolve(360, (0, 0, 0), (0, 0, 1))
    
    # Cut the bottom portion to create the helmet opening
    cut_box = (
        cq.Workplane("XY")
        .box(helmet_width * 2, helmet_length * 2, 80)
        .translate((0, 0, -40))
    )
    
    helmet_solid = dome.cut(cut_box)
    
    # Add some thickness - the dome is solid, hollow it out
    # Create inner dome slightly smaller
    scale_factor = 0.88
    inner_r_x = r_x * scale_factor
    inner_r_z = r_z * scale_factor
    
    inner_profile = (
        cq.Workplane("XZ")
        .moveTo(0, 8)
        .lineTo(inner_r_x, 8)
        .spline(
            [(inner_r_x * 0.95, 8 + inner_r_z * 0.3),
             (inner_r_x * 0.7, 8 + inner_r_z * 0.7),
             (inner_r_x * 0.2, 8 + inner_r_z * 0.97)],
        )
        .lineTo(0, 8 + inner_r_z)
        .close()
    )
    
    inner_dome = inner_profile.revolve(360, (0, 0, 0), (0, 0, 1))
    
    helmet_shell = helmet_solid.cut(inner_dome)
    
    # Add ventilation slots - elongated holes on the sides
    # Front vents
    vent_cutter = (
        cq.Workplane("XY")
        .workplane(offset=30)
        .center(0, 70)
        .ellipse(35, 12)
        .extrude(80)
    )
    
    helmet_shell = helmet_shell.cut(vent_cutter)
    
    # Side vents left
    vent_left = (
        cq.Workplane("YZ")
        .workplane(offset=-60)
        .center(40, 60)
        .ellipse(30, 10)
        .extrude(80)
    )
    helmet_shell = helmet_shell.cut(vent_left)
    
    # Side vents right
    vent_right = (
        cq.Workplane("YZ")
        .workplane(offset=60)
        .center(40, 60)
        .ellipse(30, 10)
        .extrude(80)
    )
    helmet_shell = helmet_shell.cut(vent_right)
    
    # Front top vent
    vent_top_front = (
        cq.Workplane("XY")
        .workplane(offset=80)
        .center(0, 50)
        .ellipse(15, 8)
        .extrude(80)
    )
    helmet_shell = helmet_shell.cut(vent_top_front)
    
    return helmet_shell

result = make_helmet()