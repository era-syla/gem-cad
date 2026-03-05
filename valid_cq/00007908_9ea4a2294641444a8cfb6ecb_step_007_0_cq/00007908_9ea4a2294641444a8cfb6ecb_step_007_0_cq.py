import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions
speaker_diameter = 200.0  # Overall outer diameter
total_depth = 120.0       # Front face to back magnet

# Mounting Flange
flange_thickness = 8.0
flange_rim_width = 15.0   # Width of the outer ring
mounting_hole_count = 4
mounting_hole_dia = 5.0
mounting_bc_dia = 185.0   # Bolt circle diameter

# Basket/Cone (The main curved part)
cone_start_dia = 170.0    # Inner diameter of the flange
cone_end_dia = 80.0       # Diameter where it meets the magnet structure
cone_depth = 80.0         # Depth of the curved section
wall_thickness = 4.0      # Thickness of the basket/cone material

# Magnet/Motor Structure (Back cylinders)
neck_dia = 90.0           # Connection between cone and magnet
neck_length = 15.0
magnet_dia = 110.0
magnet_thickness = 30.0

# --- Geometry Construction ---

# 1. The Mounting Flange (Outer Rim)
# We create the main disk first
flange = (
    cq.Workplane("XY")
    .circle(speaker_diameter / 2.0)
    .extrude(flange_thickness)
)

# 2. Creating the "Bowl" or Cone shape
# We'll do this by revolving a profile. This gives the smooth organic curve seen in the image.
# We need to calculate points for a spline or arc.
# Let's use a loft or a revolution of a cross-section.
# A revolution is cleaner for this rotational symmetry.

# Define the profile for the cone wall
def create_cone_profile(workplane):
    # Calculate radius points
    r_outer = cone_start_dia / 2.0
    r_inner = cone_end_dia / 2.0
    
    # Z-coordinates relative to the back of the flange (z=0 for simplicity in profile)
    z_start = 0
    z_end = -cone_depth
    
    return (
        workplane
        .moveTo(r_outer, z_start)
        # Outer curve (convex/concave shape) - classic speaker curve
        .spline([(r_outer * 0.8 + r_inner * 0.2, z_start - cone_depth * 0.4), 
                 (r_inner, z_end)], includeCurrent=True)
        # Bottom thickness
        .lineTo(r_inner - wall_thickness, z_end)
        # Inner curve (parallel to outer)
        .spline([(r_outer * 0.8 + r_inner * 0.2 - wall_thickness, z_start - cone_depth * 0.4), 
                 (r_outer - wall_thickness, z_start)], includeCurrent=True)
        .close()
    )

# Create the cone basket by revolving the profile
cone_basket = (
    cq.Workplane("XY")
    .workplane(offset=0) # Start at the back face of flange (which is at z=0 if flange extruded up)
    # Actually, let's adjust flange position. Let flange be from Z=0 to Z=flange_thickness
    # So the cone goes down from Z=0
)

# Re-doing logic slightly for assembly cleanliness:
# Let's build the revolve profile on the XZ plane
cone_profile = (
    cq.Workplane("XZ")
    .moveTo(cone_start_dia/2.0, 0)
    .spline([(cone_start_dia/2.0 * 0.7 + cone_end_dia/2.0 * 0.3, -cone_depth * 0.5), 
             (cone_end_dia/2.0, -cone_depth)], includeCurrent=True)
    .lineTo((cone_end_dia/2.0) - wall_thickness, -cone_depth)
    .spline([((cone_start_dia/2.0 * 0.7 + cone_end_dia/2.0 * 0.3) - wall_thickness, -cone_depth * 0.5), 
             ((cone_start_dia/2.0) - wall_thickness, 0)], includeCurrent=True)
    .close()
    .revolve()
)

# 3. Cut the center out of the flange to merge with the cone
flange_ring = (
    flange.faces(">Z").workplane()
    .circle(cone_start_dia / 2.0 - wall_thickness) # Cut inner diameter
    .cutThruAll()
)

# 4. Magnet Assembly
# The transition neck
neck_z_start = -cone_depth
neck = (
    cq.Workplane("XY")
    .workplane(offset=neck_z_start)
    .circle(neck_dia / 2.0)
    .extrude(-neck_length)
)

# The main magnet cylinder
magnet_z_start = neck_z_start - neck_length
magnet = (
    cq.Workplane("XY")
    .workplane(offset=magnet_z_start)
    .circle(magnet_dia / 2.0)
    .extrude(-magnet_thickness)
)

# The back plate/chamfer detail on magnet (optional but looks nice)
magnet_chamfer = magnet.faces("<Z").edges().chamfer(2.0)

# 5. Mounting Holes
# We add these to the flange_ring
mounting_holes = (
    flange_ring.faces(">Z").workplane()
    .polarArray(mounting_bc_dia/2.0, 0, 360, mounting_hole_count)
    .circle(mounting_hole_dia / 2.0)
    .cutThruAll()
)

# 6. Recess/Chamfer on the front of the flange (visual detail)
# The image shows a slight step or rim detail inside the flange
flange_recess = (
    mounting_holes.faces(">Z").workplane()
    .circle(cone_start_dia/2.0)
    .circle(cone_start_dia/2.0 - 2.0) # Small rim
    .extrude(-1.0) # Shallow cut
)

# 7. Combine Everything
# Note: flange_recess is the latest version of the flange stack
result = flange_recess.union(cone_profile).union(neck).union(magnet)

# Optional: Add fillets to smooth transitions like in the image
result = result.edges(cq.selectors.RadiusNthSelector(0)).fillet(1.0) # General cleanup
try:
    # Fillet the neck-magnet junction
    result = result.edges(cq.NearestToPointSelector((0, neck_dia/2.0, neck_z_start - neck_length))).fillet(3.0)
except:
    pass

try:
    # Fillet the cone-flange junction
    result = result.edges(cq.NearestToPointSelector((0, cone_start_dia/2.0, 0))).fillet(2.0)
except:
    pass

# Export or Render
if 'show_object' in globals():
    show_object(result)