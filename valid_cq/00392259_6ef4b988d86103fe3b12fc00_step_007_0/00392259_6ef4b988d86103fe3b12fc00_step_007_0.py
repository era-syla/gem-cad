import cadquery as cq

# -- Parametric Dimensions --
total_height = 45.0
extrusion_width = 18.0
base_depth = 12.0      # Depth at the bottom before fillet
hook_tip_depth = 28.0  # Maximum depth at the top hook
hook_thickness = 6.0   # Vertical height of the hook feature
hook_overhang = 5.0    # Horizontal length of the hook lip
neck_depth = hook_tip_depth - hook_overhang

# Fillet radii based on visual estimation
fillet_bottom = 10.0
fillet_hook_tip = 2.0

# -- Geometry Construction --

# Define the points for the side profile on the XY plane
# (0,0) is the bottom-back corner
points = [
    (0, 0),                                       # Bottom-Left (Back)
    (0, total_height),                            # Top-Left (Back)
    (hook_tip_depth, total_height),               # Top-Right (Hook Tip)
    (hook_tip_depth, total_height - hook_thickness), # Hook Tip Bottom
    (neck_depth, total_height - hook_thickness),     # Hook Undercut/Neck
    (base_depth, 0)                               # Bottom-Right (Base start)
]

# Create the main body by extruding the profile
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(extrusion_width)
)

# -- Edge Refinement --

# Apply the large curve at the bottom front
# Selector finds the edge nearest to the theoretical sharp bottom-front corner
result = result.edges(
    cq.NearestToPointSelector((base_depth, 0, extrusion_width / 2))
).fillet(fillet_bottom)

# Apply the rounded lip to the top of the hook
# Selector finds the top-front edge
result = result.edges(
    cq.NearestToPointSelector((hook_tip_depth, total_height, extrusion_width / 2))
).fillet(fillet_hook_tip)