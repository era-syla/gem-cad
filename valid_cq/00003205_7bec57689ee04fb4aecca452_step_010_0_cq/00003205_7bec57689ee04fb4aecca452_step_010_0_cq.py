import cadquery as cq

# --- Parametric Dimensions ---
plate_length = 200.0  # Total length of the plate
plate_width = 50.0    # Total width (height) of the plate
plate_thickness = 10.0 # Thickness of the plate

hole_diameter = 4.0   # Diameter of the screw holes

# Hole positions
# Based on visual estimation, there are pairs of holes.
# Let's define offsets from the center.

# Horizontal spacing
end_hole_dist_from_edge = 10.0
inner_hole_dist_from_center = 25.0 

# Vertical spacing
hole_dist_from_top_edge = 8.0
hole_vert_spacing = plate_width - (2 * hole_dist_from_top_edge)

# Calculate x coordinates for the holes (relative to center)
x_outer = (plate_length / 2) - end_hole_dist_from_edge
x_inner = inner_hole_dist_from_center

# Calculate y coordinates for the holes (relative to center)
y_offset = hole_vert_spacing / 2

# List of all hole centers as (x, y) tuples
hole_centers = [
    # Left end
    (-x_outer, y_offset),
    (-x_outer, -y_offset),
    
    # Left middle
    (-x_inner, y_offset),
    (-x_inner, -y_offset),
    
    # Right middle
    (x_inner, y_offset),
    (x_inner, -y_offset),
    
    # Right end
    (x_outer, y_offset),
    (x_outer, -y_offset)
]

# --- Modeling ---

# Create the base rectangular plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_thickness)
    .faces(">Z") # Select the top face
    .workplane() # Create a workplane on top of the face
    .pushPoints(hole_centers) # Push the locations for the holes
    .hole(hole_diameter) # Cut the holes through the entire part
)

# Export or visualization steps would go here, but only the object is required.