import cadquery as cq

# =============================================================================
# Parameters
# =============================================================================
hex_outer_diameter = 100.0  # Point-to-point diameter of the hexagon
thickness = 6.0             # Thickness of the plate
notch_width = 8.0           # Width of the rectangular notches
notch_depth = 1.5           # Depth of the cut into the side face
notch_spacing = 30.0        # Center-to-center distance between notches on a side
chamfer_size = 0.8          # Size of the chamfer on the top edge

# Derived Dimensions
# Radius is half the diameter
radius = hex_outer_diameter / 2.0
# Apothem is the distance from center to the middle of a flat face
apothem = radius * 0.86602540378  # radius * cos(30 degrees)

# =============================================================================
# Geometry Generation
# =============================================================================

# 1. Create the base Hexagon
# We rotate the polygon 30 degrees so that we have a flat face perpendicular 
# to the X-axis (located at X = apothem). This aligns faces with the global axes.
base = (
    cq.Workplane("XY")
    .transformed(rotate=(0, 0, 30))
    .polygon(6, hex_outer_diameter)
    .extrude(thickness)
)

# 2. Create the Cutting Tool (Notches)
# We create a solid representing the negative volume of the notches for one face.
# We define this on the YZ plane, offset by the apothem to lie on the face surface.
# The base is extruded from Z=0 to Z=thickness. The cutter is centered on Z=0
# so we make it tall enough to cut through the plate.

# Define the 2D profile of the two notches on one face
cutter_sketch = (
    cq.Workplane("YZ")
    .workplane(offset=apothem)
    # Move to the position of the first notch (positive Y along the face)
    .center(notch_spacing / 2.0, 0)
    .rect(notch_width, thickness * 3)  # Height exceeds thickness to ensure clean cut
    # Move to the position of the second notch (relative move)
    .center(-notch_spacing, 0)
    .rect(notch_width, thickness * 3)
)

# Extrude the sketch inwards (negative normal direction) to create the solid cutter
# combine=False allows us to keep it as a separate object for patterning
single_face_cutter = cutter_sketch.extrude(-notch_depth, combine=False)

# 3. Pattern the Cutter
# Rotate the single face cutter around the Z-axis to replicate it on all 6 faces
all_cutters = single_face_cutter
for i in range(1, 6):
    all_cutters = all_cutters.union(
        single_face_cutter.rotate((0, 0, 0), (0, 0, 1), i * 60)
    )

# 4. Boolean Cut
# Subtract all cutters from the base hexagon
result = base.cut(all_cutters)

# 5. Finishing
# Apply a chamfer to the top edges (faces with normal pointing up in Z)
result = result.faces(">Z").edges().chamfer(chamfer_size)

# The variable 'result' now contains the final CadQuery object