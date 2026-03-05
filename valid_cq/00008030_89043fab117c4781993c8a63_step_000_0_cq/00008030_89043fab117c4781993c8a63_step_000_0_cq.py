import cadquery as cq
import math

# --- Parameters ---
# Overall scaling factor to keep things reasonable
scale = 1.0

# Base parameters
base_radius_bottom = 70.0 * scale
base_radius_top = 50.0 * scale
base_height = 80.0 * scale
base_fillet = 5.0 * scale

# Joint Parameters (simplified as generic segments)
# The arm consists of alternating "links". Let's define a generic link function.
# A link typically has a joint at the bottom and a joint at the top, often rotated 90 degrees.
# This specific robot (like a Kuka iiwa) has very organic, flowing shapes. 
# We will approximate this with lofted profiles and fillets.

def create_link(length, r_start, r_mid, r_end, rotation_angle=0):
    """
    Creates a generic arm link segment using lofting.
    """
    # Define profiles for lofting
    # Bottom profile
    p1 = cq.Workplane("XY").circle(r_start)
    
    # Middle profile - bulges out a bit for the motor housing
    p2 = cq.Workplane("XY").workplane(offset=length * 0.4).circle(r_mid)
    
    # Top profile - often smaller
    p3 = cq.Workplane("XY").workplane(offset=length).circle(r_end)
    
    # Create the loft
    # Note: CadQuery's loft can be finicky with multiple sections if they aren't aligned well,
    # but circles are robust.
    link = cq.Workplane("XY").add(p1.val()).add(p2.val()).add(p3.val()).toPending().loft(ruled=True)
    
    # Add a cut/joint interface at the top
    # Visual separation ring
    ring_cut = (cq.Workplane("XY")
                .workplane(offset=length - 2)
                .rect(r_end*2.5, r_end*2.5)
                .extrude(2)
                .intersect(
                    cq.Workplane("XY").workplane(offset=length-2).circle(r_end - 1).extrude(2)
                )
               )
    
    # We won't actually cut it deeply to keep it simple, just add the solid mass.
    return link

def create_joint_detail(r):
    # Creates a stylized joint band
    return cq.Workplane("XY").circle(r).extrude(15)

# --- Building the Robot ---

# 1. Base
base = (cq.Workplane("XY")
        .circle(base_radius_bottom)
        .workplane(offset=base_height)
        .circle(base_radius_top)
        .loft()
        )

# Add some connector detail to the base side
connector_housing = (cq.Workplane("XZ")
                     .workplane(offset=-base_radius_bottom * 0.6)
                     .moveTo(base_height * 0.3, 0)
                     .rect(30, 40)
                     .extrude(20)
                     .edges("|Y").fillet(5)
                     )
base = base.union(connector_housing)

# Add mounting scollops to base
for i in range(4):
    cutout = (cq.Workplane("XY")
              .workplane(offset=10)
              .moveTo(base_radius_bottom - 5, 0)
              .circle(5)
              .extrude(20)
              .rotate((0,0,0), (0,0,1), i*90 + 45)
             )
    base = base.cut(cutout)

# 2. Link 1 (Vertical)
l1_height = 140.0 * scale
l1 = create_link(l1_height, base_radius_top, base_radius_top * 1.2, base_radius_top * 0.9)
# Move L1 to top of base
l1 = l1.translate((0, 0, base_height))

# 3. Joint 2 (Horizontal rotation axis relative to previous)
# To simulate the "organic" curves, we will stack lofts that are slightly offset or rotated.
# This robot structure alternates joint axes.
# We will construct the visual shape by stacking segments vertically but simulating the shape.

# Segment 2
l2_height = 140.0 * scale
# This segment bulges to one side visually in the image.
# We can approximate with a simpler symmetrical shape for stability in code generation.
l2 = create_link(l2_height, base_radius_top * 0.9, base_radius_top * 1.15, base_radius_top * 0.85)
l2 = l2.rotate((0,0,0), (1,0,0), 0) # No rotation, just vertical stacking for the static model
l2 = l2.translate((0, 0, base_height + l1_height))

# Joint Ring 1-2
j1_ring = create_joint_detail(base_radius_top * 0.9).translate((0,0, base_height + l1_height - 7.5))

# Segment 3
l3_height = 140.0 * scale
l3 = create_link(l3_height, base_radius_top * 0.85, base_radius_top * 1.1, base_radius_top * 0.8)
l3 = l3.translate((0, 0, base_height + l1_height + l2_height))

# Joint Ring 2-3
j2_ring = create_joint_detail(base_radius_top * 0.85).translate((0,0, base_height + l1_height + l2_height - 7.5))

# Segment 4
l4_height = 120.0 * scale
l4 = create_link(l4_height, base_radius_top * 0.8, base_radius_top * 1.0, base_radius_top * 0.75)
l4 = l4.translate((0, 0, base_height + l1_height + l2_height + l3_height))

# Joint Ring 3-4
j3_ring = create_joint_detail(base_radius_top * 0.8).translate((0,0, base_height + l1_height + l2_height + l3_height - 7.5))

# Segment 5
l5_height = 100.0 * scale
l5 = create_link(l5_height, base_radius_top * 0.75, base_radius_top * 0.9, base_radius_top * 0.7)
l5 = l5.translate((0, 0, base_height + l1_height + l2_height + l3_height + l4_height))

# Joint Ring 4-5
j4_ring = create_joint_detail(base_radius_top * 0.75).translate((0,0, base_height + l1_height + l2_height + l3_height + l4_height - 7.5))

# Segment 6 (Wrist)
l6_height = 80.0 * scale
l6 = create_link(l6_height, base_radius_top * 0.7, base_radius_top * 0.8, base_radius_top * 0.6)
l6 = l6.translate((0, 0, base_height + l1_height + l2_height + l3_height + l4_height + l5_height))

# Joint Ring 5-6
j5_ring = create_joint_detail(base_radius_top * 0.7).translate((0,0, base_height + l1_height + l2_height + l3_height + l4_height + l5_height - 7.5))

# End Effector Flange
flange_height = 30.0 * scale
flange_radius = 40.0 * scale
flange_pos_z = base_height + l1_height + l2_height + l3_height + l4_height + l5_height + l6_height

flange = (cq.Workplane("XY")
          .workplane(offset=flange_pos_z)
          .circle(base_radius_top * 0.6)
          .workplane(offset=flange_height)
          .circle(flange_radius)
          .loft()
          )

# Tool Connector / Cap
cap_radius = 35.0 * scale
cap = (cq.Workplane("XY")
       .workplane(offset=flange_pos_z + flange_height)
       .circle(cap_radius)
       .extrude(15)
       )

# Detail on cap (screw holes)
for i in range(8):
    hole = (cq.Workplane("XY")
            .workplane(offset=flange_pos_z + flange_height + 15)
            .moveTo(cap_radius - 8, 0)
            .circle(2.5)
            .extrude(-5)
            .rotate((0,0,0), (0,0,1), i * (360/8))
            )
    cap = cap.cut(hole)
    
# Add central ring detail on cap
cap_ring = (cq.Workplane("XY")
            .workplane(offset=flange_pos_z + flange_height + 15)
            .circle(cap_radius - 12)
            .circle(cap_radius - 15)
            .extrude(-2)
           )
cap = cap.cut(cap_ring)


# Combine all parts
# To emulate the specific 'zig-zag' organic look of the Kuka iiwa, 
# we need to shift the center of the 'bulge' sections of the links.
# However, modifying the generic link function to produce valid lofts with offset centers 
# is complex without exact spline data.
# A simple vertical stack captures the topology and volume.
# Let's apply slight rotations to segments to mimic the "S" curve appearance if viewed from an angle,
# or simply leave them vertical as a "home position" representation which is what the image essentially shows 
# (though the image shows alternating motor housings).

# Let's add the "Joint bands" texturing (cuts) to make it look more like the image
# The image shows angled cuts/separations between links.
def angled_cut(shape, z_pos, radius, angle_deg):
    cut_vol = (cq.Workplane("XY")
               .workplane(offset=z_pos)
               .rect(radius*3, radius*3)
               .extrude(5)
               .rotate((0,0,0), (1,0,0), angle_deg)
               )
    return shape # Simplified: Skipping complex angled cuts to ensure stability of the script

result = base
result = result.union(l1)
result = result.union(j1_ring)
result = result.union(l2)
result = result.union(j2_ring)
result = result.union(l3)
result = result.union(j3_ring)
result = result.union(l4)
result = result.union(j4_ring)
result = result.union(l5)
result = result.union(j5_ring)
result = result.union(l6)
result = result.union(flange)
result = result.union(cap)

# Filleting the base for a smoother look
try:
    result = result.edges(cq.selectors.NearestToPointSelector((0, base_radius_bottom, 0))).fillet(2)
except:
    pass

# Adding "KUKA" style recessed text or detail lines would be complex without projection,
# so we stick to the primary geometry.