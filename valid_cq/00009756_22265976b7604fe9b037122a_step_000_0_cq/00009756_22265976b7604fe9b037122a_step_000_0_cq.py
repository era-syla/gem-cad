import cadquery as cq

# Parametric dimensions
sheet_length = 200.0  # Total length of the corrugated sheet
sheet_height = 100.0  # Height of the sheet
sheet_thickness = 1.0 # Thickness of the material
pitch = 20.0          # Distance between repeating profiles
depth = 10.0          # Depth of the corrugation (amplitude)
top_width = 8.0       # Width of the flat top section
bottom_width = 8.0    # Width of the flat bottom section
num_repeats = int(sheet_length / pitch)

# Function to create a single trapezoidal profile section
def create_profile_path(current_x):
    # Calculate half the horizontal distance consumed by the slope
    # Total pitch = bottom_width + slope + top_width + slope
    slope_run = (pitch - top_width - bottom_width) / 2.0
    
    # Define points for one cycle relative to current_x
    p0 = (current_x, 0)
    p1 = (current_x + bottom_width, 0)
    p2 = (current_x + bottom_width + slope_run, depth)
    p3 = (current_x + bottom_width + slope_run + top_width, depth)
    p4 = (current_x + pitch, 0)
    
    return [p1, p2, p3, p4]

# Generate the full profile wire
points = [(0.0, 0.0)]
current_x = 0.0

for i in range(num_repeats):
    # Generate points for one wave cycle
    cycle_points = create_profile_path(current_x)
    points.extend(cycle_points)
    current_x += pitch

# Add a final small extension if needed to match exact length or just end cleanly
# (The loop ends at y=0, which is consistent with the image)

# Create the sketch/wire
# We construct a polyline from the calculated points
profile_wire = cq.Workplane("XY").polyline(points)

# Extrude the profile to create the sheet height
# Since it's a sheet metal part, we first extrude the line to make a surface (conceptually)
# but in CQ, it's easier to offset the wire to create a closed face, then extrude, 
# or extrude the open wire as a surface and thicken.
# Let's try the offset method on the 2D profile first to make it a solid profile.

# Method: Create the 2D "ribbon" shape by offsetting the polyline
profile_solid_base = (
    cq.Workplane("XY")
    .polyline(points)
    .offset2D(sheet_thickness / 2.0) # Offset to give it thickness
)

# Extrude to create the 3D sheet
result = profile_solid_base.extrude(sheet_height)

# Note: The image shows the extrusion going vertically. 
# The code above creates the profile on XY and extrudes in Z.
# If we want the orientation exactly like the image (standing up), 
# we might want to rotate it or model on a different plane.
# However, for a generic CAD model, Z-extrusion is standard. 
# Let's orient it to match the isometric view better by extruding the other way or rotating.
# The image looks like the profile is on the XZ plane and extruded along Y.

# Let's Refine for "standing up" orientation (Profile on XZ, Extrude Y)
pts_xz = [(p[0], p[1]) for p in points] # Use same points logic

result = (
    cq.Workplane("XZ")
    .polyline(pts_xz)
    .offset2D(sheet_thickness, "intersection") # Create the thick profile
    .extrude(sheet_height) # Extrude along Y
)