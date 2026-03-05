import cadquery as cq
import math

# --- Parameter Definitions ---
hex_diameter = 100.0  # Diameter across corners
plate_thickness = 15.0  # Height of the hexagonal prism

# Feature parameters
num_features = 5      # Number of circular features
feature_spacing = 13.0 # Spacing between centers
feature_radius_outer = 6.0
feature_depth = 5.0
wedge_angle = 60.0    # Degrees for the "Pacman" wedge left behind

# Calculations for centering the array
total_span = (num_features - 1) * feature_spacing
start_x = -total_span / 2

# --- Base Geometry ---
# Create the main hexagonal body
# polygon takes radius (which is diameter/2) or side length? 
# In CadQuery polygon usually takes number of sides and a diameter (circumscribed or inscribed) depending on implementation details of higher level funcs, 
# but specifically sketch.polygon uses side length or radius. 
# cq.Workplane.polygon uses radius (distance from center to vertex).
base = (
    cq.Workplane("XY")
    .polygon(nSides=6, diameter=hex_diameter)
    .extrude(plate_thickness)
)

# --- Feature Creation ---

def pacman_cutout(loc):
    """
    Creates a 'Pacman' style shape: a circular cut with a wedge removed.
    We actually want to cut the circle *except* for the wedge.
    It's easier to create the negative volume (the full cylinder) and subtract a wedge volume from it,
    then use that result to cut the main body.
    Alternatively, sketch the 2D profile (circle minus triangle) and revolve or extrude-cut.
    
    Let's try the extrusion cut approach with a custom sketch profile.
    """
    
    # Method: Create a solid cylinder for the hole, then create a wedge to intersection/mask it?
    # Simpler 2D geometry approach:
    # 1. Circle
    # 2. Triangle pointing to center
    # 3. Cut triangle from circle?
    # Looking at the image, the "wedge" is solid material *inside* the hole.
    # So we need to cut a shape that is a Circle MINUS a Wedge.
    
    # Calculate points for the wedge triangle
    # The wedge is aligned along the array axis (X-axis in the image logic)
    # The wedge points towards the "left" relative to the feature center in the image?
    # Let's align the wedge opening towards negative X for variety, or positive X.
    # Looking closely at image: The "mouth" is open towards the bottom-left. 
    # Let's assume standard orientation: wedge centered on -Y axis or similar.
    # Let's approximate the orientation: The flat face of the wedge seems perpendicular to the line of holes.
    
    # Re-evaluating image: The features are aligned on a diagonal. Let's align them on X for simplicity.
    # The wedge is pointing 'down' into the hole, but geometric wedge.
    # It looks like an annular ring cut, except the center is also cut, but a slice is missing.
    # Actually, it looks like a revolved profile or a simple extruded cut of a Pacman shape.
    # Let's assume extruded cut of a "C" shape (Pacman).
    
    # Define the 2D Pacman shape
    # Start with a full circle
    s = (
        cq.Sketch()
        .circle(feature_radius_outer)
    )
    
    # Create a wedge shape to SUBTRACT from the circle sketch
    # This wedge represents the material we want to KEEP in the final part, 
    # so we remove it from the cutting tool.
    
    # Triangle defining the wedge
    # Length needs to be enough to cover the radius
    r = feature_radius_outer * 1.5
    half_angle_rad = math.radians(wedge_angle / 2.0)
    y_offset = r * math.tan(half_angle_rad)
    
    # Triangle points: (0,0), (-r, y_offset), (-r, -y_offset)
    # This creates a wedge pointing to the right (positive X) if we subtract the left side.
    # Let's subtract a polygon on the left side (-X) to keep the material there?
    # No, we are defining the CUT shape. The CUT shape needs a gap.
    # If the material stays on the "bottom left" of the hole, the Cut shape needs a gap there.
    
    wedge_poly = [
        (0, 0),
        (-r, r), # Oversized arbitrary
        (-r, -r) # Oversized arbitrary
    ]
    
    # Let's refine the wedge logic using angles for cleaner code
    # We want a sector of a circle to be ignored during the cut.
    # Let's create the cut tool.
    
    # Workplane approach for the specific feature
    tool = (
        cq.Workplane("XY")
        .circle(feature_radius_outer)
        .extrude(feature_depth)
    )
    
    # Create the wedge that remains (solid material)
    # This wedge is what prevents the cut.
    # So we need to SUBTRACT this wedge from the cylindrical tool.
    keep_wedge = (
        cq.Workplane("XY")
        .moveTo(0,0)
        .lineTo(r * math.cos(math.radians(225 - wedge_angle/2)), r * math.sin(math.radians(225 - wedge_angle/2)))
        .lineTo(r * math.cos(math.radians(225 + wedge_angle/2)), r * math.sin(math.radians(225 + wedge_angle/2)))
        .close()
        .extrude(feature_depth)
    )
    
    # The orientation of the wedge in the image:
    # The linear array goes along a diagonal.
    # The wedge "point" is the center. The "flat back" of the wedge is towards the outside.
    # The opening of the pacman is roughly 90 degrees relative to the array line.
    
    # Let's construct the "Tool" directly as a Pacman prism.
    # 1. Make a circle wire.
    # 2. Make a V-shape wire going to center.
    # 3. Create a face.
    
    tool_sketch = (
        cq.Workplane("XY")
        .moveTo(0,0)
        .lineTo(feature_radius_outer, 0) # Start on X axis
        .revolve(360 - wedge_angle, (0,0,0), (0,0,1)) # Create the sector solid
    )
    # Revolve creates a solid sector. This is exactly the shape of the hole.
    # We just need to orient it correctly.
    # The default revolve starts at X and goes CCW.
    # We want to rotate this tool so the wedge gap is in the desired spot.
    
    tool_sketch = tool_sketch.rotate((0,0,0), (0,0,1), 90 + wedge_angle/2)
    
    # Position the tool at the location
    return tool_sketch.val().located(loc)

# Create the array of cutting tools
cut_tools = cq.Workplane("XY")

# Generate positions
positions = []
# Rotate the line of features to match the isometric-like view (approx 30 deg or aligned with hex faces)
# In the image, the hex has a point facing "down". The line is horizontal relative to the hex symmetry?
# No, the hex has flat top/bottom. The line is horizontal.
# Let's stick to X-axis alignment for the array.
for i in range(num_features):
    x_pos = start_x + (i * feature_spacing)
    positions.append(cq.Location(cq.Vector(x_pos, 0, plate_thickness)))

# Create the combined cutting solid
tools = []
for loc in positions:
    # We generate a sector solid (the air)
    # Revolve logic: 
    # Create a face on XZ plane (rectangle for radius/depth)
    # Revolve it around Z axis for (360-wedge) degrees.
    
    # Correct approach for boolean subtraction tool:
    # Create the "positive" shape of the hole (the Pacman cylinder)
    t = (
        cq.Workplane("XY")
        .rect(feature_radius_outer, feature_depth) # Draw rect on XY?? No.
    )
    
    # Let's use the explicit modeling of the "air" shape
    # Profile on XZ plane: rectangle from x=0 to x=radius, y=0 to y=-depth
    t = (
        cq.Workplane("XZ")
        .moveTo(0,0)
        .lineTo(feature_radius_outer, 0)
        .lineTo(feature_radius_outer, -feature_depth)
        .lineTo(0, -feature_depth)
        .close()
        .revolve(360 - wedge_angle, (0,0,0), (0,1,0)) # Revolve around Z (which is Y in this local plane logic? No.)
    )
    # Revolve syntax: angle, axisStart, axisEnd.
    # Workplane XZ: X is local X, Z is local Y. Normal is local Z (global Y).
    # We want to revolve around the vertical axis (Global Z).
    # In XZ plane, the "Vertical" axis is the Z-axis of the global system, which maps to local Y.
    # So axis is (0,0,0) to (0,1,0) in local coords.
    
    # Rotation to align the wedge opening
    # The "Sector" created starts at local X and goes CCW.
    # We want the solid part to be aligned with the X-axis of the array, and the gap to be perpendicular?
    # In the image, the little triangles (the material LEFT) point towards the viewer-left.
    # The gap in the hole is roughly at 225 degrees.
    t = t.rotate((0,0,0), (0,1,0), -90 - wedge_angle/2) # Rotate around vertical Z
    
    # Move to top of plate and position
    # The revolve was created at origin. We need to move it to the specific array location.
    # location is (x_pos, 0, plate_thickness)
    t = t.val().located(loc)
    tools.append(t)

# --- Boolean Operation ---

# Combine all tools into one compound for efficient cutting
cutting_compound = cq.Compound.makeCompound(tools)

# Cut the holes from the base
result = base.cut(cutting_compound)

# Export (optional, for verification if running locally)
# cq.exporters.export(result, "hex_plate.step")