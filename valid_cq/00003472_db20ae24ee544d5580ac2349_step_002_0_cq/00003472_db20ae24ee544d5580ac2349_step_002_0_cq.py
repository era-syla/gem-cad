import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the case
case_length = 160.0
case_width = 80.0
case_height = 12.0
corner_radius = 10.0  # Outer corner radius

# Main recess dimensions (the large central area)
screen_recess_length = 110.0
screen_recess_width = 70.0
screen_recess_depth = 8.0
screen_corner_radius = 4.0

# Top/Bottom detail recess dimensions (the 3 cutouts at top and bottom)
# Assuming symmetry
detail_recess_depth = 5.0
small_square_size = 10.0
center_rect_width = 25.0
recess_padding = 5.0 # Distance from edge
recess_corner_radius = 2.0

# Side button cutout dimensions
button_cutout_width = 20.0
button_cutout_height = 5.0
button_cutout_depth = 2.0

# --- Geometry Construction ---

# 1. Base Block with Rounded Corners
base = (
    cq.Workplane("XY")
    .box(case_length, case_width, case_height)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Main Screen Recess
# We need to position this centrally, but perhaps offset slightly if the top/bottom sections aren't equal.
# Looking at the image, it seems fairly centered longitudinally, maybe slightly offset. Let's center it.
main_recess = (
    cq.Workplane("XY")
    .workplane(offset=case_height/2)
    .rect(screen_recess_length, screen_recess_width)
    .extrude(-screen_recess_depth)
)
# Apply fillets to the recess corners (vertical edges inside)
main_recess = main_recess.edges("|Z").fillet(screen_corner_radius)


# 3. Create the Detailed Recesses (Top and Bottom)
# We will create a helper function or loop to generate these patterns at both ends.

def create_end_details(workplane, offset_y):
    """Creates the 3-recess pattern at a given Y offset."""
    # Local coordinates relative to the center of the detail strip
    
    # Left Square
    s1 = (workplane
          .center(-center_rect_width/2 - small_square_size/2 - 5, offset_y) # 5 is spacing
          .rect(small_square_size, small_square_size)
          .extrude(-detail_recess_depth))
    
    # Center Rectangle
    s2 = (workplane
          .center(0, offset_y)
          .rect(center_rect_width, small_square_size)
          .extrude(-detail_recess_depth))
          
    # Right Square
    s3 = (workplane
          .center(center_rect_width/2 + small_square_size/2 + 5, offset_y)
          .rect(small_square_size, small_square_size)
          .extrude(-detail_recess_depth))
          
    return s1, s2, s3

# Calculate Y position for the details
# It needs to be between the main screen recess and the outer edge.
# Gap calculation: (160 - 110) / 2 = 25mm space on each end.
# Center of that space is at 110/2 + 25/2 = 55 + 12.5 = 67.5
end_offset = (screen_recess_length/2) + ((case_length - screen_recess_length)/4)

# We need a new workplane on top of the base to cut these
top_face = base.faces(">Z").workplane()

# Cutout shapes for top end (Right side in standard XY view if length is X)
# The image shows the object rotated, but assuming length is along X
# Let's assume Length is along X axis based on `box(case_length, ...)`
# We need to be careful with coordinates. Since box creates centered at origin:
# X ranges from -80 to 80. Screen ends at +/- 55.
# Detail centers should be around +/- 67.5 along X.
# Wait, the previous logic assumed Y was length. Let's stick to X as length.

# Redefine helper for X-axis alignment
def create_details_along_x(center_x):
    # We will build a sketch of the three shapes and extrude cut them
    # Center Rectangle
    r_center = (
        cq.Workplane("XY")
        .workplane(offset=case_height/2)
        .center(center_x, 0)
        .rect(small_square_size, center_rect_width) # Swapped dimensions for orientation
    )
    
    # Top Square (positive Y)
    r_top = (
        cq.Workplane("XY")
        .workplane(offset=case_height/2)
        .center(center_x, center_rect_width/2 + small_square_size/2 + 3) # 3mm gap
        .rect(small_square_size, small_square_size)
    )
    
    # Bottom Square (negative Y)
    r_bottom = (
        cq.Workplane("XY")
        .workplane(offset=case_height/2)
        .center(center_x, -(center_rect_width/2 + small_square_size/2 + 3))
        .rect(small_square_size, small_square_size)
    )
    return r_center, r_top, r_bottom

# Let's identify the orientation from the image.
# It looks like the "Top" and "Bottom" contain the 3 pockets.
# If Length (160) is the long dimension, the 3 pockets are arranged TRANSVERSELY.
# So the pattern is: [Square] [Rectangle] [Square] across the width.

# Correct logic for the 3-pocket pattern:
# They are at the Ends of the long axis (X).
# They are distributed along the short axis (Y).

# Position for the details along X
detail_x_pos = (case_length / 2) - (case_length - screen_recess_length)/4

# Build the cutouts
# We do this by collecting solid bodies for the cuts
cuts = []

for x_factor in [-1, 1]: # Both ends
    x_pos = detail_x_pos * x_factor
    
    # Center Rectangle
    cuts.append(
        cq.Workplane("XY").workplane(offset=case_height/2)
        .center(x_pos, 0)
        .rect(small_square_size, center_rect_width) # 10 x 25
        .extrude(-detail_recess_depth)
        .edges("|Z").fillet(recess_corner_radius)
    )
    
    # "Top" Square (Positive Y)
    cuts.append(
        cq.Workplane("XY").workplane(offset=case_height/2)
        .center(x_pos, center_rect_width/2 + 5 + small_square_size/2) # 5mm gap
        .rect(small_square_size, small_square_size)
        .extrude(-detail_recess_depth)
        .edges("|Z").fillet(recess_corner_radius)
    )
    
    # "Bottom" Square (Negative Y)
    cuts.append(
        cq.Workplane("XY").workplane(offset=case_height/2)
        .center(x_pos, -(center_rect_width/2 + 5 + small_square_size/2))
        .rect(small_square_size, small_square_size)
        .extrude(-detail_recess_depth)
        .edges("|Z").fillet(recess_corner_radius)
    )

# 4. Side Button Cutout
# On one of the long sides (Face <Y or >Y)
side_cutout = (
    cq.Workplane("XZ") # Working on the side plane
    .workplane(offset=case_width/2) # Move to the front face
    .center(0, 0) # Center of the side face
    .rect(button_cutout_width, button_cutout_height)
    .extrude(-button_cutout_depth)
    .edges("|Y").fillet(button_cutout_height/2 - 0.1) # Full round ends
)

# 5. Combine Operations
result = base.cut(main_recess)

# Cut the end details
for cut_obj in cuts:
    result = result.cut(cut_obj)

# Cut the side button
result = result.cut(side_cutout)

# 6. Final Fillets
# Add a small chamfer or fillet to the top edge for a smoother look
result = result.faces(">Z").edges().fillet(1.0)
result = result.faces("<Z").edges().fillet(1.0)

# Optional: Add the parting line groove seen on the side
# The image shows a horizontal line running around the side.
parting_line = (
    cq.Workplane("XY")
    .rect(case_length + 2, case_width + 2) # Slightly larger than case
    .extrude(0.5) # Thin slice
    .translate((0, 0, -0.25)) # Center vertically
)
# Often this is a slight indentation or a chamfer, but let's keep it simple
# The image shows a groove.
groove = (
    cq.Workplane("XY")
    .rect(case_length + 5, case_width + 5) # Large outer
    .rect(case_length - 0.5, case_width - 0.5) # Inner cut boundary
    .extrude(0.5)
    .edges("|Z").fillet(corner_radius) # Match corner radius roughly
    .translate((0,0, -0.25))
)
# result = result.cut(groove) # Uncomment if strict parting line geometry is needed

# Refine side button position - image shows it clearly on the long edge
# but my code put it there. The image also shows a slight recess around the button area
# making the wall thinner there.
button_area_recess = (
    cq.Workplane("XZ")
    .workplane(offset=case_width/2)
    .center(0, 0)
    .rect(button_cutout_width + 10, case_height)
    .extrude(-1.0) # Shallow recess
)
# result = result.cut(button_area_recess) # Optional detail based on interpretation

# --- Final Export/Return ---
if 'show_object' in globals():
    show_object(result)