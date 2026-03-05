import cadquery as cq
import math

# --- Parameters ---
length = 100.0   # Length of the panel
width = 80.0     # Width of the panel
thickness = 2.0  # Thickness of the solid panel
curvature_height = 15.0 # Height of the arch in the middle

# --- Helper function for creating an arc ---
def create_arced_face(l, w, h):
    # Calculate radius of the arc based on width and height
    # Using the chord theorem: R^2 = (W/2)^2 + (R-H)^2
    # R^2 = W^2/4 + R^2 - 2RH + H^2
    # 2RH = W^2/4 + H^2
    # R = (W^2/4 + H^2) / (2H)
    radius = (w**2 / 4 + h**2) / (2 * h)
    
    # Create the profile path (an arc)
    # We draw it on the XZ plane
    path = (
        cq.Workplane("XZ")
        .moveTo(-w / 2, 0)
        .radiusArc((w / 2, 0), radius)
    )
    
    # Extrude the profile along the Y axis to create the surface/solid base
    # Since we can't easily extrude a wire into a curved surface directly and then thicken perfectly 
    # without potential issues in simple extrusions, we will extrude a shape.
    
    # Alternative approach: Create a solid block with the top face curved
    # But a simple shell extrusion is cleaner for this visual.
    # Let's extrude the wire to create a surface, then thicken it.
    
    # Create the wire for the arc
    arc_wire = path.wire()
    
    # Extrude the wire to make a surface
    surface = arc_wire.toPending().extrude(l)
    
    return surface

# --- Construction ---

# 1. Create the base curved surface by extruding an arc
# Calculate radius for the arc
R = (width**2 / 4 + curvature_height**2) / (2 * curvature_height)

# Create a sketch on the front plane (XZ)
# We make a closed profile that looks like the cross-section of the panel
# This allows for a simple extrusion
profile = (
    cq.Workplane("XZ")
    .moveTo(-width/2, 0)
    .radiusArc((width/2, 0), -R) # Negative radius for concave down, or adjust points
    .lineTo(width/2, -thickness)
    .radiusArc((-width/2, -thickness), R) # Inner arc
    .close()
)

# Extrude the profile to create the main body
# We extrude along Y
panel = profile.extrude(length)

# 2. Apply the "cutout" or feature seen on the right edge
# The image shows a notch on one corner.
# Let's creating a cutting object.
cut_size = 15.0
cut_depth = 20.0

# Define a cutting box or cylinder at the corner
# The corner seems to be at roughly (width/2, length, ...) or similar.
# Let's orient the panel so we can cut easily.
# Currently panel is centered on X, starts at Y=0 and goes to Y=length.
# The notch looks like it's on the right side (positive X) at the far end (positive Y).

# Create a cutter to remove the corner material
cutter = (
    cq.Workplane("XY")
    .workplane(offset=-10) # Start below
    .moveTo(width/2, length)
    .rect(cut_size*2, cut_depth*2, centered=True)
    .extrude(curvature_height + 20)
)

# The image actually shows a more subtle "bite" or stepped edge on the right side.
# Let's refine the cut to look more like the "step" in the image.
# It looks like a rectangular cutout on the side edge.

cutout_width = 10.0
cutout_length = 30.0
cutout_x_pos = width/2
cutout_y_pos = length * 0.7 # Position along the length

cutter2 = (
    cq.Workplane("XY")
    .moveTo(cutout_x_pos, cutout_y_pos)
    .rect(cutout_width*2, cutout_length, centered=True) # Overlap edge
    .extrude(50) # Go high enough
)

# The image has a specific irregular cut on the right. 
# It looks like an inward curve or a notch. 
# Let's make a specific shape to subtract.
notch_radius = 15.0
notch = (
    cq.Workplane("XY")
    .moveTo(width/2, length - 20)
    .circle(notch_radius)
    .extrude(50)
)

# Looking closely at the image, there is a seam line running across the middle.
# This suggests it might be an assembly of two sheets or a single sheet with a split line.
# However, for a single solid model, the geometry is continuous. 
# The "features" in the middle (triangles) look like mesh artifacts or surface imperfections in the render, 
# but could be small triangular cutouts. I will assume they are visual artifacts or minor details 
# and focus on the main shape: a curved panel with a corner cutout.

# Let's refine the specific cutout shape on the right edge (positive X).
# It looks like a rectangular notch near the corner.
corner_notch = (
    cq.Workplane("XY")
    .workplane(offset=-5)
    .moveTo(width/2, length) # Top right corner
    .rect(20, 20, centered=True) # 10x10 cut into the corner roughly
    .extrude(50)
)

# Apply the cut
result = panel.cut(corner_notch)

# Rotate to match the isometric-like view in the image roughly
# The image shows the top surface, curved, with the "far" edge having the cutout.
result = result.rotate((0,0,0), (1,0,0), -90) # Orient Z-up roughly for standard viewing if needed
# But keeping it in the construction orientation is fine.

# Final Result
result = result