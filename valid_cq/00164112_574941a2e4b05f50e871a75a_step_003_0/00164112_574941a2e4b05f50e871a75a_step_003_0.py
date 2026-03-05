import cadquery as cq
import math

# ------------------------------------------------------------------------------
# Parameters
# ------------------------------------------------------------------------------
height = 80.0           # Total height of the cylinder
radius = 20.0           # Outer radius
wall_thickness = 1.0    # Thickness of the cylinder wall
turns = 1.5             # Number of turns for the spiral (1.5 turns = 540 deg)
steps_per_turn = 12     # Number of "stair" steps per revolution
gap = 0.5               # Width of the spiral cut
tab_length = 35.0       # Length of the top/bottom tabs
tab_width = 12.0        # Width of the tabs
tab_thickness = 1.0     # Thickness of the tabs

# ------------------------------------------------------------------------------
# Derived Parameters
# ------------------------------------------------------------------------------
total_steps = int(turns * steps_per_turn)
d_theta = 360.0 / steps_per_turn
d_z = height / total_steps
r_mid = radius - wall_thickness / 2.0
inner_radius = radius - wall_thickness
overlap = 0.1 # Overlap for boolean operations

# ------------------------------------------------------------------------------
# Geometry Construction
# ------------------------------------------------------------------------------

# 1. Base Cylinder
cylinder = cq.Workplane("XY").circle(radius).circle(inner_radius).extrude(height)

# 2. Center Pin (Axis)
pin = cq.Workplane("XY").circle(2.5).extrude(height)

# 3. Cutters for the Stepped Spiral
# We construct a compound of cutter solids to subtract from the cylinder
cutters = []

# Definition of the Horizontal Cutter (Sector/Arc Slot)
# We create a profile on XZ plane and revolve it to create an arc segment
# Profile is a rectangle centered on the wall radius
h_cutter_profile = (
    cq.Workplane("XZ")
    .moveTo(r_mid, 0)
    .rect(wall_thickness * 3, gap) # Width covers wall, Height is gap
)
# Revolve creates the solid arc. By default revolves around Z.
# We create it starting at angle 0.
h_cutter_base = h_cutter_profile.revolve(d_theta, (0,0,0), (0,0,1)).val()

# Definition of the Vertical Cutter (Vertical Slot)
# A box representing the vertical riser of the step
v_box_height = d_z + overlap
v_cutter_base = (
    cq.Workplane("XY")
    .box(wall_thickness * 3, gap, v_box_height) # Radial, Tangential, Vertical
    .translate((r_mid, 0, 0)) # Move to radius
    .val()
)

# Generate the stepped path
for i in range(total_steps):
    angle_start = i * d_theta
    z_start = i * d_z
    
    # -- Horizontal Segment --
    # Rotated to current angle, translated to current height
    hc = h_cutter_base.copy()
    hc.rotate(cq.Vector(0,0,0), cq.Vector(0,0,1), angle_start)
    hc.translate(cq.Vector(0,0,z_start))
    cutters.append(hc)
    
    # -- Vertical Segment --
    # Connects the end of current horizontal segment to the start of the next
    # Located at angle_start + d_theta
    vc = v_cutter_base.copy()
    
    angle_corner = angle_start + d_theta
    z_center_v = z_start + d_z / 2.0
    
    # Rotate to the corner angle
    vc.rotate(cq.Vector(0,0,0), cq.Vector(0,0,1), angle_corner)
    # Translate to the midpoint of the vertical step
    vc.translate(cq.Vector(0,0,z_center_v))
    
    cutters.append(vc)

# Combine all cutters into one object
cutter_compound = cq.Compound.makeCompound(cutters)

# Apply the cut to the cylinder
slotted_cylinder = cylinder.cut(cq.Workplane(obj=cutter_compound))

# 4. Tabs
# Bottom Tab: Attached at the start of the spiral (Z=0)
# We orient it radially outward. Assuming start angle is 0 (X-axis).
bottom_tab = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_thickness)
    .translate((r_mid + tab_length/2.0, 0, tab_thickness/2.0))
)

# Top Tab: Attached at the end of the spiral (Z=Height)
# End angle depends on turns.
end_angle = turns * 360.0
top_tab = (
    cq.Workplane("XY")
    .box(tab_length, tab_width, tab_thickness)
    .translate((r_mid + tab_length/2.0, 0, height - tab_thickness/2.0))
    .rotate((0,0,0), (0,0,1), end_angle)
)

# 5. Final Assembly
result = slotted_cylinder.union(bottom_tab).union(top_tab).union(pin)