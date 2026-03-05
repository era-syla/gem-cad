import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions of the grille/radiator
total_width = 800.0   # Total width
total_height = 1000.0 # Total height

# Frame dimensions (vertical posts)
frame_thickness = 30.0 # Size of the square profile for vertical posts
frame_width = 30.0

# Horizontal slat dimensions
slat_height = 15.0     # Vertical height of each slat
slat_depth = 15.0      # Thickness/depth of each slat (Z direction)
slat_spacing = 50.0    # Center-to-center vertical spacing
num_slats = 18         # Approximate count based on visual inspection

# --- Modeling ---

# 1. Create the two vertical side posts
# Left post
left_post = (
    cq.Workplane("XY")
    .box(frame_width, total_height, frame_thickness)
    .translate((-total_width/2 + frame_width/2, 0, 0))
)

# Right post
right_post = (
    cq.Workplane("XY")
    .box(frame_width, total_height, frame_thickness)
    .translate((total_width/2 - frame_width/2, 0, 0))
)

# 2. Create the horizontal slats
# Calculate the effective width of a slat (between the posts)
# We can make them slightly overlap into the posts to ensure a solid union, 
# or fit exactly between them. Let's make them span the full width minus the post offsets,
# but practically they often weld to the inside faces. 
# Here, I'll model a single slat and pattern it.

slat_length = total_width - 2 * frame_width
# Alternatively, make the slat span the whole width if they are set 'on' the posts,
# but the image shows them 'between' the posts mostly flush or slightly recessed.
# Let's assume they are flush with the front/back or centered.
# Based on the image, the slats look like they might be welded between the posts.

def create_slats():
    # Base slat centered at origin
    slat = cq.Workplane("XY").box(slat_length, slat_height, slat_depth)
    
    # Calculate starting vertical position
    # To center the array of slats vertically within the frame
    total_slat_span = (num_slats - 1) * slat_spacing
    start_y = -total_slat_span / 2
    
    slats = cq.Workplane("XY")
    
    for i in range(num_slats):
        y_pos = start_y + (i * slat_spacing)
        # Add each slat
        new_slat = slat.translate((0, y_pos, 0))
        slats = slats.union(new_slat)
        
    return slats

all_slats = create_slats()

# 3. Combine everything
result = left_post.union(right_post).union(all_slats)

# Export or display
# show_object(result)