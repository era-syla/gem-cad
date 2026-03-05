import cadquery as cq

# --- Parameter Definitions ---

# Overall Dimensions
frame_width = 3000      # Approximate width of the entire structure
frame_depth = 4000      # Approximate depth of the main deck section
extension_depth = 1200  # Depth of the smaller side extension
post_height = 2500      # Height of the vertical posts

# Component Dimensions
beam_width = 150
beam_height = 50
joist_width = 50
joist_height = 150
post_size = 100         # Square post dimension
footing_radius = 80
footing_height = 150

# Spacing
joist_spacing = 400     # Center-to-center spacing of joists

# Decking (for the section that has planks)
decking_thickness = 25
decking_width = 140
decking_gap = 5

# --- Helper Functions ---

def create_footing(x, y, z):
    """Creates a cylindrical footing at position x, y, z (top center)."""
    return (cq.Workplane("XY")
            .workplane(offset=z - footing_height)
            .circle(footing_radius)
            .extrude(footing_height)
            .translate((x, y, 0)))

def create_beam(length, profile_w, profile_h, x, y, z, axis='x'):
    """Creates a rectangular beam centered at x,y,z with specified orientation."""
    res = (cq.Workplane("XY")
           .box(length, profile_w, profile_h)
           .translate((x, y, z)))
    if axis == 'y':
        res = res.rotate((0,0,0), (0,0,1), 90)
    return res

# --- Geometry Construction ---

# 1. Main Frame Structure (The large L-shape underneath)
# It consists of a main rectangular area and a side extension.

# Main section perimeter beams
main_beam_x_pos = create_beam(frame_width, beam_width, beam_height, 0, frame_depth/2, 0, axis='x')
main_beam_x_neg = create_beam(frame_width, beam_width, beam_height, 0, -frame_depth/2, 0, axis='x')
main_beam_y_pos = create_beam(frame_depth - beam_width, beam_width, beam_height, frame_width/2 - beam_width/2, 0, 0, axis='y')
main_beam_y_neg = create_beam(frame_depth - beam_width, beam_width, beam_height, -frame_width/2 + beam_width/2, 0, 0, axis='y')

# Extension frame (the smaller L-part sticking out to the left in the image)
# Based on image, it looks like an extension on the -X side
ext_width = 1500
ext_depth = 2000
ext_offset_y = 1000 # Shifted relative to center

ext_beam_x = create_beam(ext_width, beam_width, beam_height, -frame_width/2 - ext_width/2, ext_offset_y + ext_depth/2, 0, axis='x')
ext_beam_y = create_beam(ext_depth, beam_width, beam_height, -frame_width/2 - ext_width + beam_width/2, ext_offset_y, 0, axis='y')
# Connecting beam for extension
ext_connect = create_beam(ext_width, beam_width, beam_height, -frame_width/2 - ext_width/2, ext_offset_y - ext_depth/2, 0, axis='x')

frame = main_beam_x_pos.union(main_beam_x_neg).union(main_beam_y_pos).union(main_beam_y_neg)
frame = frame.union(ext_beam_x).union(ext_beam_y).union(ext_connect)

# 2. Joists (The thinner beams running across)
# Main section joists
joists = cq.Workplane("XY")
num_joists = int((frame_depth - beam_width) / joist_spacing)
start_y = -frame_depth/2 + beam_width + joist_spacing/2

for i in range(num_joists):
    y_pos = start_y + i * joist_spacing
    if y_pos < frame_depth/2 - beam_width:
        # Create joist running X direction inside the main frame
        joist = (cq.Workplane("XY")
                 .box(frame_width - 2*beam_width, joist_width, joist_height)
                 .translate((0, y_pos, joist_height/2 - beam_height/2)))
        joists = joists.union(joist)

# Extension joists
num_ext_joists = int((ext_depth - beam_width) / joist_spacing)
start_ext_y = ext_offset_y - ext_depth/2 + beam_width + joist_spacing/2

for i in range(num_ext_joists):
    y_pos = start_ext_y + i * joist_spacing
    if y_pos < ext_offset_y + ext_depth/2 - beam_width:
         joist = (cq.Workplane("XY")
                 .box(ext_width - beam_width, joist_width, joist_height)
                 .translate((-frame_width/2 - ext_width/2 + beam_width/2, y_pos, joist_height/2 - beam_height/2)))
         joists = joists.union(joist)


# 3. Posts (Vertical columns)
# 4 posts creating a rectangle on the main deck
post_offset_x = frame_width/2 - beam_width/2
post_offset_y = frame_depth/2 - beam_width/2 

# Front right
p1 = (cq.Workplane("XY").box(post_size, post_size, post_height)
      .translate((post_offset_x, -post_offset_y, post_height/2 + beam_height/2)))
# Back right
p2 = (cq.Workplane("XY").box(post_size, post_size, post_height)
      .translate((post_offset_x, post_offset_y/3, post_height/2 + beam_height/2))) # Adjusted based on image showing it not at very edge
# Front left (near the extension)
p3 = (cq.Workplane("XY").box(post_size, post_size, post_height)
      .translate((-post_offset_x, -post_offset_y, post_height/2 + beam_height/2)))
# Back left
p4 = (cq.Workplane("XY").box(post_size, post_size, post_height)
      .translate((-post_offset_x, post_offset_y/3, post_height/2 + beam_height/2)))

posts = p1.union(p2).union(p3).union(p4)

# 4. Footings (Supports under the frame)
footings = cq.Workplane("XY")
# Corners of main frame
foot_locs = [
    (frame_width/2, frame_depth/2),
    (frame_width/2, -frame_depth/2),
    (-frame_width/2, frame_depth/2),
    (-frame_width/2, -frame_depth/2),
    # Extension corners
    (-frame_width/2 - ext_width, ext_offset_y + ext_depth/2),
    (-frame_width/2 - ext_width, ext_offset_y - ext_depth/2),
]

for x, y in foot_locs:
    footings = footings.union(create_footing(x, y, -beam_height/2))


# 5. Decking (The planks on the front section)
# It appears only the front section (negative Y) has decking applied in the image.
decking = cq.Workplane("XY")
deck_area_depth = 1200 # How far back the planks go
deck_z = joist_height - beam_height/2 + decking_thickness/2

num_planks = int(deck_area_depth / (decking_width + decking_gap))
start_deck_y = -frame_depth/2 + decking_width/2

for i in range(num_planks):
    y_pos = start_deck_y + i * (decking_width + decking_gap)
    # The planks run X-wise, covering the full width
    plank = (cq.Workplane("XY")
             .box(frame_width + 100, decking_width, decking_thickness) # Slightly wider for overhang
             .translate((0, y_pos, deck_z)))
    
    # Cutouts for posts if plank intersects post area
    # Simplified collision check logic for the demo
    plank_min_y = y_pos - decking_width/2
    plank_max_y = y_pos + decking_width/2
    post_y = -post_offset_y
    
    if (plank_min_y <= post_y + post_size/2 and plank_max_y >= post_y - post_size/2):
        # Cut for front left post
        cutter1 = (cq.Workplane("XY").box(post_size + 5, post_size + 5, decking_thickness * 2)
                   .translate((-post_offset_x, -post_offset_y, deck_z)))
        # Cut for front right post
        cutter2 = (cq.Workplane("XY").box(post_size + 5, post_size + 5, decking_thickness * 2)
                   .translate((post_offset_x, -post_offset_y, deck_z)))
        plank = plank.cut(cutter1).cut(cutter2)
        
    decking = decking.union(plank)

# 6. Diagonal Bracing (The black bar in the image)
# Looks like a flat bar connecting a joist to the main beam or post area
brace_start = (-frame_width/2 + beam_width, ext_offset_y - ext_depth/2 + beam_width, joist_height/2)
brace_end = (-frame_width/2 + beam_width + 800, ext_offset_y - ext_depth/2 + beam_width, joist_height/2) # Simplified location

# Actually, looking closer at the image, there is a dark diagonal element 
# between the main frame and the extension frame joists.
# Let's approximate a diagonal stiffener.
brace = (cq.Workplane("XY")
         .box(1000, 10, 50)
         .rotate((0,0,0), (0,0,1), 45)
         .translate((-frame_width/2, 500, 0)))


# Combine all parts
result = frame.union(joists).union(posts).union(footings).union(decking)

# If the dark bar is significant, add it (colored usually, but geometry here)
# result = result.union(brace) 

# Export or Display
# show_object(result) # Used in CQ-Editor