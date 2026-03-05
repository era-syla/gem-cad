import cadquery as cq
import math

# --- Parameters ---
# Dimensions based on standard robotics U-channel (e.g., Actobotics)
# All units in mm
num_patterns = 12
pitch = 38.1           # Spacing between large hole clusters (1.5 inches)
length = num_patterns * pitch
width = 38.1           # Outer width (1.5 inches)
height = 38.1          # Outer height (1.5 inches)
thickness = 2.54       # Wall thickness (0.1 inches)

# Hole dimensions
center_hole_dia = 12.7      # Large center hole (0.5 inches)
planet_hole_dia = 3.6       # Small surrounding holes (#6 screw clearance)
planet_circle_dia = 19.56   # Diameter of the ring of small holes (0.77 inches)
planet_radius = planet_circle_dia / 2.0
inter_hole_dia = 3.6        # Intermediate single hole

# --- Geometry Construction ---

# 1. Define the base U-Channel profile
# Drawn on YZ plane: (0,0) is bottom-left corner of the cross-section
pts = [
    (0, height),                # Top left outer
    (0, 0),                     # Bottom left outer
    (width, 0),                 # Bottom right outer
    (width, height),            # Top right outer
    (width - thickness, height),# Top right inner
    (width - thickness, thickness), # Inner corner
    (thickness, thickness),     # Inner corner
    (thickness, height)         # Top left inner
]

# Extrude profile along X axis to create the beam
result = cq.Workplane("YZ").polyline(pts).close().extrude(length)

# 2. Generate Hole Pattern Points
# We calculate coordinates relative to the center of the face to use with standard workplanes.

# Calculate X positions relative to the center of the beam length
# Pattern: [Cluster] - [Small Hole] - [Cluster] ...
# First cluster is at pitch/2. Center of beam is length/2.
large_hole_x_rel = [(pitch/2 + i*pitch) - (length/2) for i in range(num_patterns)]
small_hole_x_rel = [(pitch + i*pitch) - (length/2) for i in range(num_patterns - 1)]

# Generate lists of (x, y) points for the local workplane
# Since faces are symmetric, y=0 corresponds to the centerline of the face (width/2 or height/2)

# Points for Large Center Holes
pts_large = [(x, 0) for x in large_hole_x_rel]

# Points for Intermediate Small Holes
pts_small = [(x, 0) for x in small_hole_x_rel]

# Points for Planetary Holes (Ring of 8)
pts_planet = []
for x in large_hole_x_rel:
    for i in range(8):
        angle = math.radians(i * 45)
        # x offset from hole center, y offset from hole center
        px = x + planet_radius * math.cos(angle)
        py = 0 + planet_radius * math.sin(angle)
        pts_planet.append((px, py))

# 3. Apply Cuts to Sides
# Select the face at Y=0 (Side 1) and cut through all (hitting Side 2 as well)
# Workplane center is automatically determined at the face center
result = (
    result.faces("<Y").workplane()
    .pushPoints(pts_large).circle(center_hole_dia / 2).cutThruAll()
    .pushPoints(pts_small).circle(inter_hole_dia / 2).cutThruAll()
    .pushPoints(pts_planet).circle(planet_hole_dia / 2).cutThruAll()
)

# 4. Apply Cuts to Bottom
# Select the face at Z=0 (Bottom outer face) and cut through
result = (
    result.faces("<Z").workplane()
    .pushPoints(pts_large).circle(center_hole_dia / 2).cutThruAll()
    .pushPoints(pts_small).circle(inter_hole_dia / 2).cutThruAll()
    .pushPoints(pts_planet).circle(planet_hole_dia / 2).cutThruAll()
)

# The variable 'result' now contains the finished model