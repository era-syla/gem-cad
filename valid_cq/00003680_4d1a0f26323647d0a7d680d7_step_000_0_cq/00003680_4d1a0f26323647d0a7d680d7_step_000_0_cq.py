import cadquery as cq

# -- Parametric Dimensions --
# Main dimensions
height = 100.0      # Total height of the stand
base_width = 40.0   # Width of the base (front to back)
thickness = 3.0     # Thickness of the material

# Vertical spine dimensions
top_width = 5.0     # Width at the very top
spine_bottom_width = 15.0 # Approximate width of the spine at the bottom connection

# Hook/Foot dimensions
hook_height = 15.0  # Height of the front hook
hook_width = 5.0    # Thickness of the hook lip
foot_angle_height = 10.0 # Height where the foot connects to the main spine

# Notch dimensions (for assembly, likely)
notch_depth = 3.0
notch_height = 10.0
notch1_pos_y = 30.0 # Height from bottom to bottom of first notch
notch2_pos_y = 65.0 # Height from bottom to bottom of second notch

# -- Constructing the Profile --
# We will draw the 2D profile on the XY plane and extrude it.

# Coordinates calculation
# Let's place the bottom-right corner (back of the stand) at (0,0)
# Points are (x, y)

p_bottom_back = (0, 0)
p_top_back = (0, height)
p_top_front = (-top_width, height)

# The spine slopes down. We need the point where the foot starts.
# Let's define the spine's front edge at the bottom.
p_spine_base_front = (-spine_bottom_width, foot_angle_height) 

# The foot extends forward to the left.
p_hook_top_back = (-base_width + hook_width, hook_height)
p_hook_top_front = (-base_width, hook_height)
p_hook_bottom_front = (-base_width, 0) # Bottom front corner

# Create the sketch
result = (
    cq.Workplane("XY")
    .moveTo(*p_bottom_back)
    .lineTo(*p_top_back)
    .lineTo(*p_top_front)
    .lineTo(*p_spine_base_front)
    .lineTo(*p_hook_top_back)
    .lineTo(*p_hook_top_front)
    .lineTo(*p_hook_bottom_front)
    .close() # Closes back to (0,0)
    .extrude(thickness)
)

# -- Adding Notches --
# Cut rectangular notches out of the back edge (which is at x=0)
# Notch 1
result = result.faces(">X").workplane().center(0, notch1_pos_y - height/2 + notch_height/2).rect(notch_depth*2, notch_height).cutBlind(-thickness)

# Notch 2
# Note: Since the workplane center is relative, it's safer to use absolute positioning or a new workplane
# Let's do it cleanly by selecting the back face again or using global coordinates relative to the object.
# Actually, it's easier to just cut sketches from the side profile before extruding, or cut solids after.
# Let's cut solids.

# Define notch cutters
notch1 = (
    cq.Workplane("XY")
    .rect(notch_depth * 2, notch_height) # Width is double so we don't worry about alignment perfectly on edge
    .extrude(thickness)
    .translate((0, notch1_pos_y + notch_height/2, 0)) # Position Y
)

notch2 = (
    cq.Workplane("XY")
    .rect(notch_depth * 2, notch_height)
    .extrude(thickness)
    .translate((0, notch2_pos_y + notch_height/2, 0)) # Position Y
)

# Cut the notches from the main body
# Since the rect was centered at (0,0) before translation, and our back edge is at X=0, 
# the rect spans from -notch_depth to +notch_depth. This cuts into the material (X < 0).
result = result.cut(notch1).cut(notch2)

# Export or Render
# if __name__ == '__main__':
#     show_object(result)