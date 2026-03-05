import cadquery as cq
import math

# --- Parameters ---

# Wall Mount Base
base_dia = 50.0
base_height = 15.0
base_chamfer = 2.0

# Middle Articulation Joint
joint_cyl_dia = 20.0
joint_cyl_width = 30.0
knob_dia = 25.0
knob_height = 8.0
knob_knurl_count = 24
knob_knurl_depth = 1.0
knob_knurl_width = 2.0

# Pivot Arm
arm_width = 12.0
arm_length = 20.0
arm_thickness = 8.0

# Main Lamp Head Body
head_rear_sphere_dia = 40.0
head_mid_cyl_dia = 40.0
head_mid_cyl_length = 30.0
head_mid_groove_count = 6
head_mid_groove_depth = 1.5
head_mid_groove_pitch = 4.0

# Lamp Bell/Cone
bell_start_dia = 40.0
bell_end_dia = 80.0
bell_length = 50.0

# Front Ring/Lens Holder
ring_dia = 85.0
ring_height = 10.0
ring_groove_count = 36
ring_groove_width = 3.0
ring_groove_depth = 1.5

# --- Geometry Definition ---

# 1. Wall Base
# Cylinder with a chamfer on the front edge
base = cq.Workplane("XY").circle(base_dia / 2).extrude(base_height)
base = base.faces(">Z").chamfer(base_chamfer)

# 2. Mounting Stem (connecting base to joint)
# A smaller cylinder protruding from the base
stem_dia = 15.0
stem_height = 15.0
stem = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(stem_dia / 2)
    .extrude(stem_height)
)

# 3. Pivot Joint Assembly
# The horizontal cylinder axis
joint_center_z = base_height + stem_height + joint_cyl_dia/2

# The main pivot cylinder
pivot_cyl = (
    cq.Workplane("XZ")
    .workplane(offset=-joint_cyl_width/2)
    .center(0, joint_center_z)
    .circle(joint_cyl_dia / 2)
    .extrude(joint_cyl_width)
)

# Knurled Knob on the side of the pivot
# Create a cylinder first
knob = (
    cq.Workplane("XZ")
    .workplane(offset=joint_cyl_width/2)
    .center(0, joint_center_z)
    .circle(knob_dia / 2)
    .extrude(knob_height)
)

# Create the knurling pattern (cuts)
knob_cutter = (
    cq.Workplane("XZ")
    .workplane(offset=joint_cyl_width/2)
    .center(0, joint_center_z)
    .polarArray(knob_dia/2, 0, 360, knob_knurl_count)
    .rect(knob_knurl_width, knob_knurl_depth*2) # Oversize depth for clean cut
    .extrude(knob_height)
)
knob = knob.cut(knob_cutter)

# Add a simple handle bar on the knob
handle_width = 4.0
handle_height = 6.0
handle_len = knob_dia * 0.8
knob_handle = (
    cq.Workplane("XZ")
    .workplane(offset=joint_cyl_width/2 + knob_height)
    .center(0, joint_center_z)
    .rect(handle_height, handle_len)
    .extrude(handle_width)
)

# 4. Connecting Arm to Lamp Head
# A rectangular arm extending from the pivot cylinder
arm = (
    cq.Workplane("YZ")
    .center(0, joint_center_z)
    .workplane(offset=0) # Centered on YZ plane
    .rect(arm_thickness, joint_cyl_dia)
    .extrude(arm_length + head_rear_sphere_dia/2) # Extend into the head
    .translate((arm_length/2, 0, 0)) # Shift it out along X
)
# Rotate arm to angle it down slightly like in the image
arm = arm.rotate((0, joint_center_z, 0), (1, joint_center_z, 0), -15)

# Calculate where the head attaches based on arm length and rotation
head_center_x = arm_length * 1.5
head_center_z = joint_center_z - 10 

# 5. Lamp Head Construction
# Axis for the lamp head. Let's align it somewhat horizontally for construction, then rotate.
# Actually, constructing it along X axis is easiest, then we move it.

# Rear Sphere
head_rear = (
    cq.Workplane("YZ")
    .sphere(head_rear_sphere_dia/2)
    # Cut off the front half to attach the cylinder
    .cut(cq.Workplane("YZ").rect(head_rear_sphere_dia*2, head_rear_sphere_dia*2).extrude(head_rear_sphere_dia))
)

# Mid Cylinder with Cooling Fins/Grooves
mid_cyl = (
    cq.Workplane("YZ")
    .circle(head_mid_cyl_dia/2)
    .extrude(head_mid_cyl_length)
)

# Create cuts for fins
fin_cutter_profile = cq.Workplane("YZ").circle(head_mid_cyl_dia/2 + 1) # Outer bound
fin_cut_solid = (
    cq.Workplane("YZ")
    .circle(head_mid_cyl_dia/2 - head_mid_groove_depth)
    .extrude(head_mid_groove_pitch/2)
)
# Make multiple cuts
for i in range(head_mid_groove_count):
    mid_cyl = mid_cyl.cut(fin_cut_solid.translate((head_mid_groove_pitch * (i+1), 0, 0)))

# Conical Bell
bell = (
    cq.Workplane("YZ")
    .workplane(offset=head_mid_cyl_length)
    .circle(bell_start_dia/2)
    .workplane(offset=bell_length)
    .circle(bell_end_dia/2)
    .loft(combine=True)
)

# Front Ring
front_ring = (
    cq.Workplane("YZ")
    .workplane(offset=head_mid_cyl_length + bell_length)
    .circle(ring_dia/2)
    .extrude(ring_height)
)

# Front Ring Detail (Rectangular indents around the perimeter)
ring_cutters = (
    cq.Workplane("YZ")
    .workplane(offset=head_mid_cyl_length + bell_length)
    .polarArray(ring_dia/2, 0, 360, ring_groove_count)
    .rect(ring_groove_depth*2, ring_groove_width) # Depth creates radial cut
    .extrude(ring_height * 0.8) # Not full depth
    .translate((-ring_groove_depth, 0, ring_height * 0.1)) # Center the cut
)
front_ring = front_ring.cut(ring_cutters)

# Assemble the Lamp Head parts
lamp_head_assembly = head_rear.union(mid_cyl).union(bell).union(front_ring)

# Orient and position the lamp head
# The head seems to be pointing roughly perpendicular to the arm
lamp_head_assembly = lamp_head_assembly.rotate((0,0,0), (0,1,0), 90) # Point along X
lamp_head_assembly = lamp_head_assembly.rotate((0,0,0), (0,0,1), -15) # Tilt down matching arm
lamp_head_assembly = lamp_head_assembly.translate((head_center_x + 15, 0, head_center_z - 5))

# Combine everything
result = (
    base
    .union(stem)
    .union(pivot_cyl)
    .union(knob)
    .union(knob_handle)
    .union(arm)
    .union(lamp_head_assembly)
)

# Optional: Add the small detail at the very back of the sphere (wire exit or molding mark)
back_detail = (
    cq.Workplane("YZ")
    .circle(2.0)
    .extrude(2.0)
    .rotate((0,0,0), (0,1,0), 90)
    .rotate((0,0,0), (0,0,1), -15)
    .translate((head_center_x + 15 - head_rear_sphere_dia/2, 0, head_center_z - 5))
    # Adjust position slightly back along the vector
    .translate((-math.cos(math.radians(15))*2, -math.sin(math.radians(15))*2, 0))
)
result = result.union(back_detail)

# Export or Display
# show_object(result) # Only for CQ-editor environment