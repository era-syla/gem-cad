import cadquery as cq
import math

# --- Parameters ---
base_radius = 50.0       # Radius of the enclosing circle of the base hexagon
top_radius = 10.0        # Radius of the enclosing circle of the top hexagon
height = 50.0            # Total height of the truncated pyramid
arch_height = 25.0       # Height of the cutout arches from the base
hole_diameter = 8.0      # Diameter of the through-hole in the center
num_sides = 6            # It's a hexagon

# --- Geometry Construction ---

# 1. Create the base profile (hexagon)
# We use a polygon centered at origin
base_pts = []
for i in range(num_sides):
    angle = math.radians(i * (360 / num_sides))
    x = base_radius * math.cos(angle)
    y = base_radius * math.sin(angle)
    base_pts.append((x, y))

# 2. Create the top profile (hexagon)
top_pts = []
for i in range(num_sides):
    angle = math.radians(i * (360 / num_sides))
    x = top_radius * math.cos(angle)
    y = top_radius * math.sin(angle)
    top_pts.append((x, y))

# 3. Create the Truncated Pyramid (Loft)
# We place sketches on the bottom and top planes and loft between them
pyramid = (
    cq.Workplane("XY")
    .polyline(base_pts).close()
    .workplane(offset=height)
    .polyline(top_pts).close()
    .loft(combine=True)
)

# 4. Create the Arches (Subtractive features)
# The arches appear to be cutouts on the side faces. 
# A hexagonal pyramid has 6 faces. We need to cut an arch into each face.
# A simple way to do this is to create a cylinder or sphere and subtract it,
# but looking at the geometry, it looks like cylindrical cutouts directed 
# towards the center, or perhaps perpendicular to the faces.
# 
# Let's try cylindrical cutouts positioned at the midpoint of the base edges.
# The axis of the cylinder should be tangent to the base polygon edge.

# Calculate the distance from center to the midpoint of a base edge (apothem)
apothem = base_radius * math.cos(math.radians(180 / num_sides))

# Create a cutting tool (a cylinder rotated 90 degrees)
# The radius of this cutter determines the steepness of the arch.
# Let's estimate the cutter radius based on the arch height.
cutter_radius = 25.0 

# We will iterate through each side and perform a cut.
result = pyramid
for i in range(num_sides):
    angle_deg = i * (360 / num_sides)
    angle_rad = math.radians(angle_deg)
    
    # Calculate position for the cutout cylinder.
    # We want the cylinder axis to lie roughly along the edge chord.
    # But actually, looking at the image, the cutout is centered on the FACE,
    # not the edge. Wait, looking closer:
    # The "legs" touch the ground at the vertices of the hexagon.
    # The arches are between the vertices. 
    # So the cutout is indeed centered on the midpoint of the base edges.
    
    # Position of the midpoint of the edge
    mid_angle_deg = angle_deg + (180/num_sides) 
    mid_angle_rad = math.radians(mid_angle_deg)
    
    mid_x = apothem * math.cos(mid_angle_rad)
    mid_y = apothem * math.sin(mid_angle_rad)
    
    # We need a cylinder oriented perpendicular to the radial line to the midpoint.
    # Axis of cylinder is perpendicular to the vector (mid_x, mid_y).
    
    # Let's create a cutter object.
    # We position a cylinder such that it intersects the solid.
    # The center of the cylinder needs to be offset upwards or downwards to achieve the arch height.
    # If the cylinder is at z=0, the cut is a semi-circle on the ground.
    # The image shows the cut going up to 'arch_height'.
    
    # Let's try a cylinder moving radially inward.
    # Center of cylinder at (mid_x, mid_y, 0).
    # Radius = arch_height roughly? If it's a circular cut.
    # Let's assume the cutout is a cylinder oriented perpendicular to the face normal projected on XY.
    
    cutter = (
        cq.Workplane("XY")
        .workplane(offset=-10) # Start slightly below
        .transformed(rotate=(0, 90, mid_angle_deg)) # Rotate to align with face normal direction
        .circle(arch_height) # This defines the arch shape/size
        .extrude(base_radius * 2) # Cut through enough material
    )
    
    # Now we need to move this cutter to the right location.
    # The workplane transformation rotates around the origin.
    # The extrusion goes along the new Z.
    # With rotate=(0, 90, mid_angle_deg), the local Z axis points radially outward.
    # The circle is in the plane perpendicular to the radius.
    # We need to shift it so it cuts the bottom edge.
    
    # Actually, a simpler way is to use a large cylinder centered far away
    # or just a cylinder lying on the ground plane, rotated to match the side.
    
    # Let's refine:
    # We want a cylindrical cut. The axis of the cylinder connects two adjacent vertices?
    # No, that would just shave the bottom flat.
    # The axis of the cutting cylinder is perpendicular to the side face?
    # Looking at the sharp points on the ground, the cut is circular in profile when viewed from the side.
    
    # Let's try placing a cylinder centered at the midpoint of the edge, with axis parallel to the ground.
    # Axis vector: Tangent to the circle at that angle.
    
    # Vector to midpoint: (cos(mid_angle), sin(mid_angle))
    # Tangent vector: (-sin(mid_angle), cos(mid_angle))
    
    # Let's build the cutter explicitly using geometric transformations logic provided by CQ
    c = cq.Workplane("YZ").circle(arch_height).extrude(100, both=True)
    c = c.rotate((0,0,0), (0,0,1), mid_angle_deg)
    c = c.translate((mid_x, mid_y, 0))
    
    result = result.cut(c)

# 5. Create the center hole
# It goes from top to bottom (or at least through the top part).
# Image shows it going deep. Assume through-hole.
result = result.faces(">Z").workplane().circle(hole_diameter/2).cutBlind(-height)

# 6. Optional: Chamfers or Fillets
# The top edge looks faceted/chamfered in the image, but the main geometry is the loft.
# The image top edge looks like it might have a small chamfer.
try:
    result = result.edges(">Z").chamfer(0.5)
except:
    pass # If geometry is complex, skip chamfer

# Final validation
if result.val().Volume() < 0:
    raise ValueError("Resulting volume is invalid")