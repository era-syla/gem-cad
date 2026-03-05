import cadquery as cq

# --- Parametric Dimensions ---
# Estimated dimensions based on the provided image
total_length = 90.0
shaft_diameter = 6.0

# Threaded Section Details
thread_length = 15.0
thread_pitch = 1.0
thread_major_diam = 6.0  # Nominal M6

# Mechanism End Details (Neck and Head)
neck_length = 3.5
neck_diameter = 3.8  # Thinner than shaft
head_length = 4.0
head_diameter = 5.2  # Slightly smaller than main shaft
head_chamfer = 0.5

# Shaft length derived from other features
# Structure: [Thread] --- [Smooth Shaft] --- [Neck] --- [Head]
shaft_length = total_length - thread_length - neck_length - head_length

# --- Geometry Construction ---

# 1. Main Body Construction (Revolution)
# We define the profile of the shaft in the XY plane and revolve it around the X-axis.
# This ensures perfect concentricity for the shaft, neck, and head.

# Define profile points (x, y) where y is the radius
pts = [
    (0, 0),                                                                 # Center start
    (0, thread_major_diam / 2.0),                                           # Thread start radius
    (thread_length + shaft_length, shaft_diameter / 2.0),                   # End of smooth shaft
    (thread_length + shaft_length, neck_diameter / 2.0),                    # Step down to neck
    (thread_length + shaft_length + neck_length, neck_diameter / 2.0),      # End of neck
    (thread_length + shaft_length + neck_length, head_diameter / 2.0),      # Step up to head
    (total_length, head_diameter / 2.0),                                    # End of head
    (total_length, 0)                                                       # Center end
]

# Create the base revolved solid
main_body = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .revolve(360, (0, 0, 0), (1, 0, 0)) # Explicit revolution around X-axis
)

# 2. Add Chamfers
# Apply chamfer to the threaded end (standard lead-in)
# Select the face with the minimum X coordinate
result = main_body.faces("<X").chamfer(0.8)

# Apply chamfer to the head end (button-like appearance)
# Select the face with the maximum X coordinate
result = result.faces(">X").chamfer(head_chamfer)

# 3. Create Physical Threads (Optional but requested by visual)
# We perform a helical cut to represent the threads.
# Note: In production CAD, threads are often cosmetic, but we model it here for the visual match.

# Define thread cutter parameters
# Start slightly before the part to ensure a clean entrance cut
cut_start_offset = -1.0
cut_len = thread_length + 1.5  # Cut slightly past the thread length
turns = cut_len / thread_pitch
angle = 360.0 * turns

# Create the cutter tool
# We use a triangular profile swept along a helix (twistExtrude)
thread_cutter = (
    cq.Workplane("YZ")  # Plane perpendicular to the shaft axis (X)
    .workplane(offset=cut_start_offset)
    .center(0, thread_major_diam / 2.0) # Position at the surface
    .polygon(3, thread_pitch * 0.75)    # Triangular thread profile
    .twistExtrude(cut_len, angle)       # Helical sweep
)

# Subtract the thread cutter from the main body
result = result.cut(thread_cutter)

# Result contains the final solid geometry