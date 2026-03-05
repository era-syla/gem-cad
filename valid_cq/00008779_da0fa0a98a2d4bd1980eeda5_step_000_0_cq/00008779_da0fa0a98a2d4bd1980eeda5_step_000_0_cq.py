import cadquery as cq

# --- Parameters ---
# Main Box Dimensions
box_width = 80.0
box_depth = 50.0
box_height = 50.0
wall_thickness = 3.0

# Finger/Arm Dimensions
arm_base_width = 15.0
arm_length = 60.0
arm_thickness = 5.0
pad_radius = 20.0
finger_width = 8.0

# Vertical Back Structure
back_struct_height = 80.0
back_struct_width = 10.0
back_struct_depth = 5.0
back_struct_spacing = 30.0  # spacing between the two posts

# Cutout Slot Dimensions
slot_width = 20.0
slot_length = 60.0

# Internal Mechanism (Mockup)
axle_radius = 1.5
axle_length = box_width + 10.0


# --- Helper Functions ---
def create_finger_joint_box(w, d, h, t):
    """Creates a basic box with the internal cavity.
    Simplification: Visual solid box with hollow interior,
    ignoring complex finger joint boolean operations for simplicity
    but adding aesthetic cuts to mimic them."""
    
    # Main outer shell
    outer = cq.Workplane("XY").box(w, d, h)
    
    # Inner cavity (hollow it out)
    inner = (cq.Workplane("XY")
             .box(w - 2*t, d - 2*t, h - 2*t))
    
    box = outer.cut(inner)
    
    # Aesthetic vertical cuts to simulate laser-cut joints
    corner_cut_w = t
    corner_cut_h = h / 3.0
    
    cuts = (cq.Workplane("XY")
            .rect(w + 10, d + 10)  # Larger than box
            .extrude(h)
           )
           
    # Actual implementation: Just use a simple hollow box for the visual representation
    # Adding joint details often overcomplicates the script without proper joinery lib.
    # Instead, we will simulate the "look" by creating the panels separately if needed,
    # or just creating the solid shape with the slot. Let's go with the solid shape with slot.
    
    return box

# --- Construction ---

# 1. The Main Enclosure
# Create the base box
box = (cq.Workplane("XY")
       .box(box_width, box_depth, box_height)
       .faces(">Z").shell(-wall_thickness) # Create hollow box
       )

# Create the top slot for the arm
top_face = box.faces(">Z").workplane()
slot = (top_face
        .center(0, 0)
        .rect(slot_length, slot_width)
        .cutThruAll()
       )

# Add side holes (for axles/screws seen in image)
side_face = box.faces(">Y").workplane()
holes = (side_face
         .pushPoints([(10, -5), (-10, -5), (10, 5)])
         .circle(1.5)
         .cutThruAll()
        )

# Add the small protruding axle
axle = (side_face
        .center(-15, -5)
        .circle(axle_radius)
        .extrude(15) # Stick out from the side
       )

# 2. The Arm / Paddle Mechanism
# This is the complex part on top. It looks like a lever with a round pad.

# The round pad
pad = (cq.Workplane("XY")
       .workplane(offset=box_height/2 + arm_thickness/2) # Position on top
       .center(-box_width/2 - pad_radius/2 + 10, 0) # Stick out front
       .circle(pad_radius)
       .extrude(2)
      )

# The lever arms connecting to the pad
# Let's create a shape that represents the arm structure
arm_sketch = (cq.Workplane("XY")
              .workplane(offset=box_height/2)
              .center(-10, 0) # Centered somewhat in the slot
              .rect(arm_length, finger_width)
              .extrude(arm_thickness)
              )

# Detailed features on the arm (ribs/structure)
# Two parallel rails
rail_width = 2.0
rail_spacing = 4.0
rail_height = 4.0

rail_l = (cq.Workplane("XY")
          .workplane(offset=box_height/2 + arm_thickness)
          .center(-10, rail_spacing/2 + rail_width/2)
          .rect(arm_length * 0.8, rail_width)
          .extrude(rail_height)
         )

rail_r = (cq.Workplane("XY")
          .workplane(offset=box_height/2 + arm_thickness)
          .center(-10, -(rail_spacing/2 + rail_width/2))
          .rect(arm_length * 0.8, rail_width)
          .extrude(rail_height)
         )

# Cross brace on the arm
cross_brace = (cq.Workplane("XY")
               .workplane(offset=box_height/2 + arm_thickness)
               .center(-20, 0)
               .rect(5, finger_width + 4)
               .extrude(rail_height)
              )

arm_assembly = arm_sketch.union(pad).union(rail_l).union(rail_r).union(cross_brace)

# Rotate the arm slightly to look like it's resting or acting
# (Optional, but makes it look more realistic if pivot point is defined)
# For this static model, we keep it flat as it simplifies the CSG.


# 3. The Vertical Back Structure (Tower)
# Looks like two tall posts with a crossbar at the top.

# Right Post
post_r = (cq.Workplane("XY")
          .workplane(offset=-box_height/2) # Start from bottom of box
          .center(box_width/2 + back_struct_depth/2, back_struct_spacing/2)
          .rect(back_struct_depth, back_struct_width)
          .extrude(box_height + back_struct_height)
         )

# Left Post
post_l = (cq.Workplane("XY")
          .workplane(offset=-box_height/2)
          .center(box_width/2 + back_struct_depth/2, -back_struct_spacing/2)
          .rect(back_struct_depth, back_struct_width)
          .extrude(box_height + back_struct_height)
         )

# Top Crossbar / Axis
top_axis = (cq.Workplane("YZ")
            .workplane(offset=box_width/2)
            .center(0, box_height/2 + back_struct_height - 5)
            .circle(2)
            .extrude(back_struct_depth * 2) # Stick out a bit
           )

# Top Connector Block
top_block = (cq.Workplane("XY")
             .workplane(offset=box_height/2 + back_struct_height - 10)
             .center(box_width/2 + back_struct_depth/2, 0)
             .rect(back_struct_depth + 4, back_struct_spacing + back_struct_width)
             .extrude(10)
            )
            
# Hollow out the top block between the posts
top_block_cutout = (cq.Workplane("XY")
                    .workplane(offset=box_height/2 + back_struct_height - 11)
                    .center(box_width/2 + back_struct_depth/2, 0)
                    .rect(back_struct_depth + 10, back_struct_spacing - back_struct_width)
                    .extrude(12)
                   )
top_structure = post_r.union(post_l).union(top_block).cut(top_block_cutout)


# 4. Joint Details (Box Finger Joints Simulation)
# To make it look like the laser cut box in the image, we add corner notches.
def make_notches(part):
    # Vertical corners
    notches = cq.Workplane("XY").rect(box_width + 2, box_depth + 2).extrude(box_height)
    # This is a simplification. Real finger joints are tedious to code manually without loops.
    # We will skip specific finger joint geometry for clean code, focusing on the overall form.
    return part

# Combine all parts
final_box = holes.union(axle)
result = final_box.union(arm_assembly).union(top_structure)

# Export or Render
# if 'show_object' in globals():
#     show_object(result)