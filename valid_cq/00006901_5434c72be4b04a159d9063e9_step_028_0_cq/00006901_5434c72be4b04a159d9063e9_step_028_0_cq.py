import cadquery as cq

# --- Parameters ---
length = 150.0       # Total length of the plate
width_top = 60.0     # Width of the top flat surface
thickness = 15.0     # Thickness of the plate
chamfer_width = 10.0 # Horizontal distance of the side slope
hole_diameter = 4.0  # Diameter of the mounting holes
side_hole_dia = 3.0  # Diameter of the hole on the slanted face

# Calculate bottom width based on chamfer
width_bottom = width_top + (2 * chamfer_width)

# Mounting hole positions (relative to center)
hole_spacing_x = length * 0.7  # Spacing along the length
hole_spacing_y = width_top * 0.6 # Spacing along the width

# --- Geometry Construction ---

# 1. Create the base profile (Trapezoidal cross-section extruded)
# We draw the profile on the front plane (XZ) and extrude along Y (length) to make orienting side holes easier
points = [
    (-width_bottom / 2, 0),
    (width_bottom / 2, 0),
    (width_top / 2, thickness),
    (-width_top / 2, thickness)
]

base = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(length)
)

# 2. Add the four top mounting holes
# We select the top face (largest Z face)
result = (
    base.faces(">Z")
    .workplane()
    .rect(width_top - 15, length - 40, forConstruction=True) # Construction rectangle for positioning
    .vertices()
    .hole(hole_diameter)
)

# 3. Add the hole on the slanted face
# The image shows a hole on the slanted face at the "front" (min Y usually, or max Y depending on view).
# Let's target the slanted face.
# A robust way is to select the face by normal vector or position.
# The slanted face has a normal with a component in X and Z.

# Let's find the slanted face on the negative X side.
# Normal vector will point roughly (-1, 0, 1).
slanted_face_selector = cq.DirectionMinMaxSelector(cq.Vector(-1, 0, 1), directionMax=True)

# Alternatively, select faces based on X coordinate range and Z coordinate range.
# Let's try selecting the face directly.
result = (
    result.faces("<X") # Select faces on the negative X side
    .faces("not |Z")   # Exclude vertical faces (if any side walls existed)
    .faces("not |Y")   # Exclude the end caps
    .workplane(centerOption="CenterOfMass")
    .hole(side_hole_dia, depth=20) # Drill through or deep enough
)

# If the image implies a hole on the end cap (the trapezoidal face), let's look closer.
# Looking at the image, there is a small hole on the *trapezoidal end face* (the cross-section face).
# And there are 4 holes on the top flat face.
# Wait, looking at the crop, the hole is on the *slanted side* face? 
# Actually, looking at the very specific shading, the hole at the bottom left is on the TRAPEZOIDAL END face.
# The previous step assumed a side slope hole. Let's correct that.

# Correction: The single hole is clearly on the visible end face (the one defined by the sketch profile).
# The profile was extruded along Z in standard CQ, or Y in my previous logic.
# My extrusion was: sketch on XY, extrude Z.
# Let's restart the mental model for standard orientation:
# Plate lies flat on XY plane. Long axis along X.
# Cross section is visible on the YZ plane (or XZ plane depending on rotation).

# Let's rebuild for clearer orientation matching the isometric view:
# Length along Y axis. Width along X axis. Vertical is Z.

# Re-defining base creation for better alignment
base_sketch = (
    cq.Workplane("XZ")
    .polyline([
        (-width_bottom / 2, 0),
        (width_bottom / 2, 0),
        (width_top / 2, thickness),
        (-width_top / 2, thickness)
    ])
    .close()
    .extrude(length) # Extrudes along Y
)

# Now the object is aligned with Y axis.
# Top face is +Z.
# End faces are -Y and +Y.
# Slanted sides are towards +/- X.

# Top holes
plate_with_top_holes = (
    base_sketch.faces(">Z")
    .workplane()
    # Define a rectangle of hole positions centered on the face
    .rect(width_top * 0.7, length * 0.75, forConstruction=True)
    .vertices()
    .hole(hole_diameter)
)

# End hole
# The image shows a hole on the visible end face. Let's assume it's the -Y face.
result = (
    plate_with_top_holes.faces("<Y")
    .workplane()
    .center(0, thickness/3) # Shift up slightly from the bottom edge
    .hole(side_hole_dia, depth=10)
)

# Depending on interpretation, there might be holes on the slanted sides (the dimples). 
# However, the image shows 4 clear holes on top, and one on the end face.
# Let's stick to the 4 top holes and 1 end hole interpretation.

# Refined parameters for visual match
length = 120.0
width_top = 40.0
width_bottom = 60.0
thickness = 12.0
hole_dia_top = 3.0
hole_dia_end = 2.5

# Final Code Construction
result = (
    cq.Workplane("XZ")
    .polyline([
        (-width_bottom / 2, 0),
        (width_bottom / 2, 0),
        (width_top / 2, thickness),
        (-width_top / 2, thickness)
    ])
    .close()
    .extrude(length/2, both=True) # Center the part on the origin along Y
)

# Add Top Holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (-width_top/3, -length/3),
        (width_top/3, -length/3),
        (-width_top/3, length/3),
        (width_top/3, length/3)
    ])
    .hole(hole_dia_top)
)

# Add End Hole
result = (
    result.faces("<Y")
    .workplane()
    # The workplane center is the center of mass of the trapezoid face.
    # We want it roughly in the middle of that face, which is usually fine, 
    # but let's shift it slightly down if the CoM is too high due to the taper.
    # For a symmetrical trapezoid, CoM is vertically correct.
    .hole(hole_dia_end, depth=15.0)
)