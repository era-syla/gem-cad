import cadquery as cq

# --- Parameters ---
beam_width = 10.0
beam_height = 10.0

# Left Assembly Parameters
left_spine_length = 35.0
left_back_arm_length = 90.0
left_front_arm_length = 50.0
# Offset of the front arm relative to the gap face of the spine
left_front_offset = 10.0 

# Right Assembly Parameters
gap_size = 4.0
right_head_length = 15.0
right_head_height = 20.0
right_tail_length = 70.0

# --- Geometry Generation ---

# 1. Left Component Construction
# The 'spine' is the central block connecting the two arms.
# We position the gap center at x=0.
spine_end_x = -gap_size / 2.0
spine_center_x = spine_end_x - (left_spine_length / 2.0)

# Create Spine
spine = cq.Workplane("XY").center(spine_center_x, 0).box(left_spine_length, beam_width, beam_height)

# Create Back Arm (Long, pointing in +Y)
# Attached at the far left end of the spine
back_arm_x = spine_end_x - left_spine_length + (beam_width / 2.0)
back_arm_y = (left_back_arm_length / 2.0) - (beam_width / 2.0)
back_arm = cq.Workplane("XY").center(back_arm_x, back_arm_y).box(beam_width, left_back_arm_length, beam_height)

# Create Front Arm (Short, pointing in -Y)
# Attached closer to the gap
front_arm_x = spine_end_x - left_front_offset - (beam_width / 2.0)
front_arm_y = -((left_front_arm_length / 2.0) - (beam_width / 2.0))
front_arm = cq.Workplane("XY").center(front_arm_x, front_arm_y).box(beam_width, left_front_arm_length, beam_height)

# Combine Left Parts
left_part = spine.union(back_arm).union(front_arm)


# 2. Right Component Construction

# Create the Head (the block facing the gap)
head_start_x = gap_size / 2.0
head_center_x = head_start_x + (right_head_length / 2.0)

head_block = cq.Workplane("XY").center(head_center_x, 0).box(right_head_length, beam_width, right_head_height)

# Create the curved face on the head
# We select the vertical edges (|Z) that are at the minimum X coordinate (<X) of the block
# and apply a fillet to create the rounded "cam follower" shape.
# Radius is set slightly less than half width to ensure robustness.
head_curved = head_block.edges("|Z and <X").fillet(beam_width / 2.0 - 0.01)

# Create the Tail (Arm extending in +X)
tail_start_x = head_start_x + right_head_length
tail_center_x = tail_start_x + (right_tail_length / 2.0)
tail = cq.Workplane("XY").center(tail_center_x, 0).box(right_tail_length, beam_width, beam_height)

# Combine Right Parts
right_part = head_curved.union(tail)

# --- Final Assembly ---
result = left_part.union(right_part)