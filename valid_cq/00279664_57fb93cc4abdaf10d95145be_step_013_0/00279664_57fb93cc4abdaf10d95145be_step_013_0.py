import cadquery as cq

# --- Parameters ---
thickness = 10.0
arm_length = 85.0
arm_width = 30.0
arm_angle = 45.0  # Degrees
separation = 14.0  # Distance from center plane to arm root

# Gusset parameters
gusset_height = 25.0
gusset_length = 45.0
gusset_thickness = 10.0
gusset_offset = 20.0  # Start position from the root of the arm

# Hole sizes
hole_dia_small = 4.5
hole_dia_large = 8.0
hole_dia_side = 6.0
cbore_dia_small = 9.0
cbore_depth_small = 4.0
cbore_dia_large = 14.0
cbore_depth_large = 5.0

def create_arm():
    """
    Creates a single arm (wing) aligned along the X-axis.
    Includes the top plate and the under-hanging gusset.
    """
    # 1. Top Plate
    # Create box starting from X=0
    arm = (
        cq.Workplane("XY")
        .box(arm_length, arm_width, thickness, centered=(False, True, False))
    )
    
    # Chamfer the outer tip corners
    arm = (
        arm.faces(">X")
        .edges("|Z")
        .chamfer(8.0)
    )
    
    # 2. Top Holes
    # Two small holes at the tip
    arm = (
        arm.faces(">Z").workplane()
        .pushPoints([(arm_length - 10, 8), (arm_length - 10, -8)])
        .cboreHole(hole_dia_small, cbore_dia_small, cbore_depth_small)
    )
    
    # One large hole in the middle
    arm = (
        arm.faces(">Z").workplane()
        .pushPoints([(arm_length / 2 + 10, 0)])
        .cboreHole(hole_dia_large, cbore_dia_large, cbore_depth_large)
    )
    
    # One small hole near the root
    arm = (
        arm.faces(">Z").workplane()
        .pushPoints([(20, 8)])
        .cboreHole(hole_dia_small, cbore_dia_small, cbore_depth_small)
    )
    
    # 3. Gusset (Vertical triangular support)
    # Sketch on XZ plane (Front view relative to arm)
    # Profile: Trapezoidal shape hanging down
    pts = [
        (gusset_offset, 0),
        (gusset_offset, -gusset_height),
        (gusset_offset + 10, -gusset_height), # Bottom flat section
        (gusset_offset + gusset_length, 0)
    ]
    
    gusset = (
        cq.Workplane("XZ")
        .polyline(pts).close()
        .extrude(gusset_thickness / 2.0, both=True)
    )
    
    # Hole through the gusset (Y-axis relative to arm)
    gusset = (
        gusset.faces(">Y").workplane()
        .pushPoints([(gusset_offset + 15, -gusset_height / 2)])
        .hole(hole_dia_side)
    )
    
    # Notch at the bottom of the gusset
    # U-shaped cutout at the bottom flat face
    gusset = (
        gusset.faces("<Z").workplane(centerOption="CenterOfBoundBox")
        .rect(6.0, gusset_thickness + 2).cutThruAll()
    )
    
    return arm.union(gusset)

# --- Assembly ---

# Create one arm
right_arm_raw = create_arm()

# Rotate and position the right arm
# We rotate -45 degrees around Z and translate along X to create the central gap
right_arm = (
    right_arm_raw
    .rotate((0, 0, 0), (0, 0, 1), -arm_angle)
    .translate((separation, 0, 0))
)

# Mirror to create the left arm
left_arm = right_arm.mirror("YZ")

# Combine arms
result = right_arm.union(left_arm)

# --- Central Bridge & Features ---

# Create a central block to fill the gap between the angled arms
# This ensures a solid connection at the apex
bridge_block = (
    cq.Workplane("XY")
    .box(separation * 2.5, 30, thickness, centered=(True, True, False))
    .translate((0, 10, 0)) # Shift slightly back
)

# Intersect/Union to clean up the joint
result = result.union(bridge_block)

# --- Final Cutouts ---

# 1. Front Notch (The "Keyhole" at the V-apex)
# Positioned at the front convergence point
result = (
    result.faces(">Z").workplane()
    .moveTo(0, -5) # Adjust based on visual fit
    .hole(12.0)
)

# 2. Central Bridge Hole
# A large hole on the solid bridge part
result = (
    result.faces(">Z").workplane()
    .moveTo(0, 15)
    .cboreHole(hole_dia_large, cbore_dia_large, cbore_depth_large)
)

# 3. Clean up the back edge (Optional, gives it the chamfered look)
# Cut a V-shape or chamfer at the back if needed, but the union usually handles it well.
# We will chamfer the back corners of the bridge area for aesthetics
try:
    result = (
        result.faces(">Y").edges("|Z")
        .chamfer(5.0)
    )
except:
    pass # In case geometry selection is ambiguous

# Export or Render
# cq.exporters.export(result, "bracket.step")