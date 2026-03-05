import cadquery as cq

# Geometric parameters
length_crossbar = 160.0  # Length of the top-left beam
length_stem = 100.0      # Length of the bottom-right beam
width = 20.0             # Width of the L-profile legs
thickness = 2.5          # Thickness of the material
gap = 4.0                # Gap between the two beams

# Create Beam 1 (Crossbar)
# Oriented along the Y-axis. 
# The L-profile is sketched on the XZ plane.
# The vertical leg is positioned at X = -width (back side), horizontal leg on Z=0.
beam1 = (
    cq.Workplane("XZ")
    .workplane(offset=-length_crossbar / 2.0)  # Start extrusion to center the beam
    .moveTo(-width, width)
    .lineTo(-width, 0)
    .lineTo(0, 0)
    .lineTo(0, thickness)
    .lineTo(-width + thickness, thickness)
    .lineTo(-width + thickness, width)
    .close()
    .extrude(length_crossbar)
)

# Create Beam 2 (Stem)
# Oriented along the X-axis.
# The L-profile is sketched on the YZ plane.
# The vertical leg is positioned at Y = -width (right side), horizontal leg on Z=0.
# The beam starts at X = gap (offset from the crossbar) and is centered on the Y-axis.
beam2 = (
    cq.Workplane("YZ")
    .workplane(offset=gap)
    .moveTo(-width, width)
    .lineTo(-width, 0)
    .lineTo(0, 0)
    .lineTo(0, thickness)
    .lineTo(-width + thickness, thickness)
    .lineTo(-width + thickness, width)
    .close()
    .extrude(length_stem)
    .translate((0, width / 2.0, 0))  # Center the stem relative to the crossbar
)

# Combine the two beams into the final assembly
result = beam1.union(beam2)