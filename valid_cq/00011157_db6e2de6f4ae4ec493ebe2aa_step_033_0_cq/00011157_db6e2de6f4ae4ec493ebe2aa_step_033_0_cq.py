import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions
total_height = 20.0
flange_height = 1.5
tooth_section_height = 8.0
hub_height = total_height - flange_height - tooth_section_height

# Diameters
outer_flange_dia = 20.0
tooth_outer_dia = 16.0  # Outside diameter of the teeth
tooth_root_dia = 14.0   # Diameter at the base of the teeth
hub_dia = 18.0
bore_dia = 5.0

# Tooth profile
num_teeth = 20
tooth_depth = (tooth_outer_dia - tooth_root_dia) / 2.0
tooth_width_ratio = 0.5 # Ratio of tooth width to gap width (approximate for GT2)

# Set screw parameters
set_screw_dia = 3.0
set_screw_head_dia = 4.5 # Slightly larger for the counterbore/protrusion look
set_screw_offset_z = hub_height / 2.0  # Centered on the hub

# --- Helper Function for Gear Profile ---
def create_pulley_profile(outer_d, root_d, num_teeth):
    """
    Creates a simplified trapezoidal timing belt profile.
    """
    profile = cq.Workplane("XY")
    
    angle_per_tooth = 360.0 / num_teeth
    tooth_angle = angle_per_tooth * 0.45 # Width of the tooth land
    gap_angle = angle_per_tooth - tooth_angle
    
    outer_r = outer_d / 2.0
    root_r = root_d / 2.0
    
    # Create points for one tooth section
    # P1: Root start
    # P2: Tooth slope start (at root)
    # P3: Tooth tip start
    # P4: Tooth tip end
    # P5: Tooth slope end (at root)
    
    # We will build this by revolving/extruding a sketch, 
    # but for CadQuery usually it's easier to subtract teeth or add them to a cylinder.
    # Let's subtract gaps from an outer cylinder.
    return None # Strategy shift: Add teeth to a root cylinder

# --- Modeling Strategy ---
# 1. Create the main central body (Hub + Root of gear + Flange)
# 2. Cut the teeth into the gear section
# 3. Create the central bore with chamfer
# 4. Add the set screw detail

# 1. Main Body Construction
# We will construct from bottom to top
# Hub
hub = cq.Workplane("XY").circle(hub_dia / 2.0).extrude(hub_height)

# Gear section (initially just the outer cylinder)
gear_blank = (cq.Workplane("XY")
              .workplane(offset=hub_height)
              .circle(tooth_outer_dia / 2.0)
              .extrude(tooth_section_height))

# Flange
flange = (cq.Workplane("XY")
          .workplane(offset=hub_height + tooth_section_height)
          .circle(outer_flange_dia / 2.0)
          .extrude(flange_height))

main_body = hub.union(gear_blank).union(flange)

# 2. Cut the Teeth
# We will create a cutting tool that represents the gaps between teeth
gap_depth = (tooth_outer_dia - tooth_root_dia) / 2.0
# Calculate the arc length at the outer diameter
circumference = math.pi * tooth_outer_dia
tooth_pitch = circumference / num_teeth
# Trapezoidal gap shape
gap_top_width = tooth_pitch * 0.55
gap_bottom_width = tooth_pitch * 0.35

# Sketch the gap profile on the XZ plane, projected out to the radius
gap_profile = (cq.Workplane("XZ")
               .workplane(offset=tooth_outer_dia/2.0) # Move to outer surface
               .moveTo(-gap_top_width/2.0, hub_height) # Start at bottom of gear section, outer surface
               .lineTo(-gap_bottom_width/2.0, hub_height) # Move Inward? No, we need to cut inward.
               )

# Alternative Strategy: Create a full cutter profile and extrude/cut
cutter_pts = [
    (-gap_top_width/2.0, 0),
    (-gap_bottom_width/2.0, -gap_depth),
    (gap_bottom_width/2.0, -gap_depth),
    (gap_top_width/2.0, 0)
]

# Create one cutter
cutter = (cq.Workplane("XY")
          .workplane(offset=hub_height)
          .transformed(rotate=(90, 0, 0)) # Rotate to sketch on a vertical plane
          .moveTo(tooth_outer_dia/2.0, 0) # Move to the edge
          .workplane(offset=tooth_outer_dia/2.0) # Move sketch plane to tangent
          .polyline(cutter_pts).close()
          .extrude(tooth_section_height, combine=False) # Extrude downwards relative to sketch, which is Z-up
          )

# Re-orient cutter properly if needed. 
# Actually, simpler method: Loft/Extrude a shape radially.
# Let's try polarArray subtraction.

# Create the cutting shape for one gap
# We sketch on the top face of the gear section and extrude down
cutter_sketch = (cq.Workplane("XY")
                 .workplane(offset=hub_height + tooth_section_height)
                 .polarArray(tooth_outer_dia/2, 0, 360, num_teeth)
                 .rect(gap_depth*2, gap_top_width) # Rough rectangular cut to verify, then refine
                 )

# Refined cutter: Trapezoidal prism
def trapezoid_cutter(loc):
    # Local coordinate system at the perimeter
    return cq.Solid.makeLoft([
        # Outer face
        cq.Workplane("YZ").workplane(offset=tooth_outer_dia/2.0).polyline(
            [(-gap_top_width/2, 0), (gap_top_width/2, 0), (gap_top_width/2, tooth_section_height), (-gap_top_width/2, tooth_section_height)]
        ).close().val(),
        # Inner face (root)
        cq.Workplane("YZ").workplane(offset=tooth_root_dia/2.0).polyline(
            [(-gap_bottom_width/2, 0), (gap_bottom_width/2, 0), (gap_bottom_width/2, tooth_section_height), (-gap_bottom_width/2, tooth_section_height)]
        ).close().val()
    ])

# Generate all cutters
cutters = []
for i in range(num_teeth):
    angle = i * (360.0 / num_teeth)
    c = trapezoid_cutter(None).rotate((0,0,0), (0,0,1), angle)
    c = c.translate((0, 0, hub_height))
    cutters.append(c)

# Subtract all cutters from main body
for c in cutters:
    main_body = main_body.cut(c)

# 3. Central Bore with Chamfer
main_body = main_body.faces(">Z").workplane().hole(bore_dia)

# Add chamfer to the top of the bore
main_body = main_body.faces(">Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5) 
# Note: RadiusNthSelector(0) usually selects the inner hole edge on a simple washer shape

# 4. Set Screw Feature
# Create a hole on the side of the hub
main_body = (main_body.faces("<Z").workplane(centerOption="CenterOfBoundBox")
             .transformed(offset=(0, 0, set_screw_offset_z), rotate=(90, 0, 0))
             .hole(set_screw_dia, depth=hub_dia))

# Create the mock screw head protruding slightly
# We model this as a cylinder added to the side
screw_head = (cq.Workplane("XZ")
              .workplane(offset=-hub_dia/2.0 + 0.5) # Positioned just inside surface
              .moveTo(0, set_screw_offset_z)
              .circle(set_screw_head_dia/2.0)
              .extrude(2.0)) # Extrude outwards

# Make the Hex socket in the screw head
screw_head = (screw_head.faces(">Y").workplane()
              .polygon(6, set_screw_dia * 0.8) # Hex size
              .cutBlind(-1.5)) # Cut into the head

# Union the screw head to the body
result = main_body.union(screw_head)

# Optional: Add small fillets to the transition between flange and gear, and gear and hub
result = result.edges(cq.selectors.NearestToPointSelector((0, tooth_outer_dia/2, hub_height))).fillet(0.2)
result = result.edges(cq.selectors.NearestToPointSelector((0, tooth_outer_dia/2, hub_height + tooth_section_height))).fillet(0.2)

if "show_object" in locals():
    show_object(result)