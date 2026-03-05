import cadquery as cq

# Parameters
# Overall dimensions
frame_width = 1000.0  # Width between the outer edges of the side beams
frame_length = 1500.0 # Length of the side beams
frame_height = 800.0  # Height from floor to top of side beams

# Side Beam (C-Channel) dimensions
beam_h = 150.0 # Height of the C-channel
beam_w = 60.0  # Flange width
beam_t = 6.0   # Thickness of the web and flanges

# Leg (I-Beam/H-Beam) dimensions
leg_h = 120.0 # Height of the I-beam profile
leg_w = 120.0 # Width of the I-beam profile
leg_t = 8.0   # Thickness
leg_length = frame_height - beam_h # Length of the leg
foot_plate_t = 12.0 # Thickness of the foot plate
foot_plate_extension = 20.0 # Extension beyond the leg profile

# Cross Roller/Slat Support dimensions
num_rollers = 5
roller_spacing = frame_length / (num_rollers + 1)
roller_w = 50.0 # Width of the flat bar support
roller_t = 6.0  # Thickness of the flat bar support

# Angle Iron (Guide Rail) dimensions
angle_size = 50.0 # Leg length of the angle iron
angle_t = 5.0     # Thickness
angle_offset_x = 20.0 # Offset from the edge of the C-channel

# Helper function to create a C-Channel profile
def make_c_channel(h, w, t, length):
    pts = [
        (0, 0), (w, 0), (w, t), (t, t),
        (t, h - t), (w, h - t), (w, h), (0, h)
    ]
    return cq.Workplane("YZ").polyline(pts).close().extrude(length)

# Helper function to create an I-Beam profile
def make_i_beam(h, w, t_web, t_flange, length):
    pts = [
        (0, 0), (w, 0), (w, t_flange), 
        (w/2 + t_web/2, t_flange), (w/2 + t_web/2, h - t_flange),
        (w, h - t_flange), (w, h), (0, h),
        (0, h - t_flange), (w/2 - t_web/2, h - t_flange),
        (w/2 - t_web/2, t_flange), (0, t_flange)
    ]
    # Center the profile
    return cq.Workplane("XY").polyline(pts).close().extrude(length).translate((-w/2, -h/2, 0))

# 1. Create Side Beams (C-Channels)
# Left Beam (Toes pointing inward)
left_beam = make_c_channel(beam_h, beam_w, beam_t, frame_length)
# Orient correctly: Web vertical, toes pointing right (positive X)
left_beam = left_beam.rotate((0,0,0), (0,1,0), 90).rotate((0,0,0), (0,0,1), 90)
# Position
left_beam = left_beam.translate((-frame_width/2 + beam_t, -frame_length/2, leg_length))

# Right Beam (Toes pointing inward)
right_beam = make_c_channel(beam_h, beam_w, beam_t, frame_length)
# Orient correctly: Web vertical, toes pointing left (negative X)
right_beam = right_beam.rotate((0,0,0), (0,1,0), 90).rotate((0,0,0), (0,0,1), -90)
# Position (mirroring the left essentially, but manually positioned for control)
right_beam = right_beam.translate((frame_width/2 - beam_t, -frame_length/2, leg_length))

side_beams = left_beam.union(right_beam)

# 2. Create Legs
leg_profile = make_i_beam(leg_h, leg_w, leg_t, leg_t, leg_length)
# Position legs under the left beam
leg_l_front = leg_profile.translate((-frame_width/2 + beam_w/2, -frame_length/2 + 100, 0))
leg_l_back = leg_profile.translate((-frame_width/2 + beam_w/2, frame_length/2 - 100, 0))

# Create foot plates
foot_plate_dim = max(leg_h, leg_w) + foot_plate_extension * 2
foot_plate = cq.Workplane("XY").rect(foot_plate_dim, foot_plate_dim).extrude(foot_plate_t)
foot_l_front = foot_plate.translate((-frame_width/2 + beam_w/2, -frame_length/2 + 100, 0))
foot_l_back = foot_plate.translate((-frame_width/2 + beam_w/2, frame_length/2 - 100, 0))

legs = leg_l_front.union(leg_l_back).union(foot_l_front).union(foot_l_back)

# We only see legs on one side in the reference image for the full C-channel structure, 
# but usually frames are symmetric. The image shows a heavy cross-member at the front.
# Let's assume the legs shown are supports for a larger assembly. 
# Based on the image, there is a heavy cross member connecting the legs.

# 3. Heavy Cross Member (between legs)
# It looks like a large C-channel or I-beam connecting the two front legs
cross_member_h = 200.0
cross_member = make_c_channel(cross_member_h, beam_w, beam_t, frame_width - beam_w) # Length approx between webs
cross_member = cross_member.rotate((0,0,0), (0,1,0), -90).rotate((0,0,0), (1,0,0), 180)
# Position it
cross_member = cross_member.translate((-frame_width/2 + beam_w/2, -frame_length/2 + 100 + leg_w/2, leg_length - cross_member_h + 20))


# 4. Cross Slats (Flat bars connecting side beams)
slat = cq.Workplane("XY").rect(frame_width - 2*beam_t, roller_w).extrude(roller_t)
# Move to top of beams but sunken slightly (flush or resting on lower flange?) 
# Image shows them resting on the bottom flange or welded to web. Let's weld to web.
slat_z = leg_length + beam_h/2 # Mid-height of beam
slats = cq.Workplane("XY")

for i in range(num_rollers):
    y_pos = -frame_length/2 + (i + 1) * roller_spacing
    new_slat = slat.translate((0, y_pos, slat_z))
    if i == 0:
        slats = new_slat
    else:
        slats = slats.union(new_slat)

# 5. Top Guide Rail (Angle Iron on top of one beam)
def make_angle(size, t, length):
    pts = [
        (0,0), (size, 0), (size, t), (t, t), (t, size), (0, size)
    ]
    return cq.Workplane("YZ").polyline(pts).close().extrude(length)

guide_rail = make_angle(angle_size, angle_t, frame_length)
# Rotate to sit on top face
guide_rail = guide_rail.rotate((0,0,0), (0,1,0), 90).rotate((0,0,0), (0,0,1), 90)
# Position on left beam
guide_rail_z = leg_length + beam_h
guide_rail_x = -frame_width/2 + beam_w/2 # Center on flange roughly
guide_rail = guide_rail.translate((guide_rail_x, -frame_length/2, guide_rail_z))

# Add holes to the vertical face of the angle iron
hole_spacing = frame_length / 8
for i in range(7):
    hole_y = -frame_length/2 + (i + 1) * hole_spacing
    # Position a cylinder to cut
    cutter = cq.Workplane("YZ").circle(4).extrude(20).translate((guide_rail_x - 10, hole_y, guide_rail_z + angle_size/2))
    guide_rail = guide_rail.cut(cutter)


# Combine all parts
result = side_beams.union(legs).union(cross_member).union(slats).union(guide_rail)

# Optional: Add the right side legs if symmetry is desired, but image focus is on one side structure
# Adding right legs for stability of the 'model' logic
leg_r_front = leg_profile.translate((frame_width/2 - beam_w/2, -frame_length/2 + 100, 0))
leg_r_back = leg_profile.translate((frame_width/2 - beam_w/2, frame_length/2 - 100, 0))
foot_r_front = foot_plate.translate((frame_width/2 - beam_w/2, -frame_length/2 + 100, 0))
foot_r_back = foot_plate.translate((frame_width/2 - beam_w/2, frame_length/2 - 100, 0))
right_legs = leg_r_front.union(leg_r_back).union(foot_r_front).union(foot_r_back)
result = result.union(right_legs)

# Export or display
# show_object(result)