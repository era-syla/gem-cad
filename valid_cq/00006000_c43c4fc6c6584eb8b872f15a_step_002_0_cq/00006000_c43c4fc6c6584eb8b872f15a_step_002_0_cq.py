import cadquery as cq
import math

# --- Parameters ---
# Main body dimensions
body_height = 80.0
body_radius = 45.0  # Max radius of the egg shape
base_flat_radius = 20.0 # Flatten the bottom slightly so it stands

# Neck dimensions
neck_radius = 8.0
neck_height = 10.0

# Cutout pattern (leaf/tear-drop shape) parameters
cutout_count = 3  # Number of cutouts around the circumference
cutout_depth = 2.0  # Depth of the embossing/cutout
cutout_height_center = 40.0 # Z-height of the cutout center
cutout_width = 25.0
cutout_height = 45.0

# --- Helper Functions ---

def create_egg_profile(height, radius):
    """
    Creates a spline profile for an egg-like revolution.
    The profile is defined on the XZ plane.
    """
    # Define control points for the egg curve
    # Points: (radius, height)
    # Start at bottom center (0,0), move out to max radius, curve back to top center (0, height)
    
    p0 = (0, 0)
    p1 = (radius * 0.7, 0)       # Bottom curvature control
    p2 = (radius, height * 0.35) # Widest point
    p3 = (radius * 0.8, height * 0.65) # Tapering up
    p4 = (neck_radius, height)  # Top point meeting the neck
    p5 = (0, height)            # Close on axis

    # Create the wire
    pts = [p0, p1, p2, p3, p4, p5]
    
    # We use a spline for smooth curvature, then close it with a line segment to the axis
    path = (
        cq.Workplane("XZ")
        .moveTo(*p0)
        .spline([p1, p2, p3, p4], includeCurrent=True)
        .lineTo(*p5)
        .close()
    )
    return path

def create_teardrop_sketch(width, height):
    """
    Creates a teardrop/leaf shape sketch on the XY plane.
    """
    w_half = width / 2.0
    h_half = height / 2.0
    
    # Points for a leaf shape:
    # Top tip, right curve, bottom curve, left curve
    p_top = (0, h_half)
    p_right = (w_half, -h_half * 0.2)
    p_bottom = (0, -h_half)
    p_left = (-w_half, -h_half * 0.2)
    
    sketch = (
        cq.Workplane("XY")
        .moveTo(*p_top)
        .spline([p_right, p_bottom], includeCurrent=True) # Right side curve
        .spline([p_left, p_top], includeCurrent=True)    # Left side curve
        .close()
    )
    return sketch

# --- Modeling ---

# 1. Create the main egg body
egg_profile = create_egg_profile(body_height, body_radius)
main_body = egg_profile.revolve(360, (0,0,0), (0,1,0)) # Revolve around Z (which is Y in the 2D profile logic, but standard revolve axis)

# Correcting the revolve axis: CadQuery's revolve on a Workplane("XZ") usually revolves around Z by default if unspecified or uses the Y axis of the local plane. 
# Let's be explicit. The profile was drawn in XZ. Z is vertical.
main_body = (
    cq.Workplane("XZ")
    .moveTo(0,0)
    .spline([(body_radius, body_height*0.35), (neck_radius, body_height)], includeCurrent=True)
    .lineTo(0, body_height)
    .close()
    .revolve(360, (0,0,0), (0,0,1))
)

# 2. Flatten the bottom
# Create a large box or cylinder to cut the bottom, or just plane cut
main_body = main_body.cut(
    cq.Workplane("XY").rect(body_radius*3, body_radius*3).extrude(-5) # Just cut below Z=0
)
# Re-align so it sits on Z=0 if we cut off the curved bottom
# However, simpler is to just let the spline start flat or use an intersection
# Let's use an intersection with a chamfered cylinder base logic, or simply accept the spline shape.
# Based on image, the bottom is rounded but stable. Let's apply a small fillet to the bottom edge if it was a cylinder, 
# but since it's a revolved spline, it's already round. Let's just create a flat spot.
flat_spot_cut = cq.Workplane("XY").workplane(offset=1.5).rect(100, 100).extrude(-10) # Cut bottom 1.5mm
main_body = main_body.cut(flat_spot_cut)


# 3. Add the Neck
neck = (
    cq.Workplane("XY")
    .workplane(offset=body_height)
    .circle(neck_radius)
    .extrude(neck_height)
)
body_with_neck = main_body.union(neck)


# 4. Create the embossed cutouts
# We will create a solid of the teardrop shape, move it to the surface, and cut
cutout_tool_sketch = create_teardrop_sketch(cutout_width, cutout_height)

# We need to project or position these around the egg.
# A robust way is to position the tool radially and subtract.
cutout_tools = cq.Workplane("XY")

for i in range(cutout_count):
    angle = i * (360.0 / cutout_count)
    
    # Define a workplane rotated to the correct angle
    # We position the sketch out at a radius slightly larger than the body
    # Then extrude inwards
    
    # Calculate radial position roughly at the height of the cutout center
    # Approximate radius at cutout_height_center using linear interpolation or just guess based on body_radius
    r_at_height = body_radius * 0.95 
    
    # Position the tool
    # 1. Rotate to angle
    # 2. Translate out to radius
    # 3. Translate up to height
    # 4. Rotate so sketch faces the origin
    
    wp = (
        cq.Workplane("XY")
        .transformed(rotate=cq.Vector(0, 0, angle))
        .transformed(offset=cq.Vector(r_at_height, 0, cutout_height_center))
        .transformed(rotate=cq.Vector(0, 90, 0)) # Rotate so Z points towards origin (local X points in)
    )
    
    # Create the teardrop on this plane
    # Note: sketch coords are local. 
    tool = (
        wp.spline(
            [(0, cutout_height/2), (cutout_width/2, -cutout_height*0.1), (0, -cutout_height/2), (-cutout_width/2, -cutout_height*0.1)],
            includeCurrent=True
        )
        .close()
        .extrude(cutout_depth * 4) # Extrude deep enough to penetrate
    )
    
    # To mimic the image, the cut isn't a straight extrusion, it follows the surface curvature (offset).
    # However, a simple boolean subtract with a positioned solid is standard for this visual approximation.
    # To get the "rim" effect, we can intersect the tool with a shell, or simply subtract.
    # The image shows an embossment.
    
    # Refined approach for surface emboss:
    # Create a tool that represents the inner volume to keep, or the outer volume to remove?
    # The image shows a recessed area.
    
    # Move the tool slightly "into" the egg
    tool = tool.translate(tool.plane.zDir.multiply(-cutout_depth))
    
    cutout_tools = cutout_tools.union(tool)

# 5. Apply the cuts
# Since the surface is curved and the extrusion is planar, the depth will vary.
# To make it look like the image (uniform depth inset), usually requires offsetting the surface.
# In pure CSG/Brep without complex surface offsets, we can subtract the tool.
# To make it look nice, we will fillet the edges of the cut later if possible, 
# or use a slightly tapered extrusion for the tool.

# Let's use a loft for the tool to simulate a draft angle
# (Simplified: just subtraction)

result = body_with_neck.cut(cutout_tools)

# 6. Detail: Fillets
# The neck transition looks sharp in image, maybe a tiny chamfer
try:
    result = result.edges(cq.selectors.NearestToPointSelector((0,0,body_height))).chamfer(0.5)
except:
    pass

# The base of the neck
try:
    result = result.edges(cq.selectors.NearestToPointSelector((0, neck_radius, body_height))).fillet(1.0)
except:
    pass

# Export or display
# show_object(result)