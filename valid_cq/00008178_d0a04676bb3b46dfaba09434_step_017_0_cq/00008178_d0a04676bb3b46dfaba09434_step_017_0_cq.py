import cadquery as cq
import math

# --- Parameters ---
# Overall dimensions
pulley_width = 16.0       # Width of the toothed section
flange_width = 1.5        # Thickness of the side flanges
flange_diameter = 40.0    # Outer diameter of the flanges
bore_diameter = 5.0       # Diameter of the center shaft hole

# Tooth parameters (approximating a GT2 or similar timing belt profile)
num_teeth = 40
pitch = 2.0               # Distance between teeth
tooth_depth = 0.75        # Height of the tooth cut
tooth_width_ratio = 0.5   # Ratio of tooth cut width to pitch

# Calculations derived from parameters
# Pitch circumference = num_teeth * pitch
# Pitch diameter = Pitch circumference / pi
pitch_diameter = (num_teeth * pitch) / math.pi
outer_diameter = pitch_diameter - (2 * 0.254) # Typically slightly smaller than pitch diameter for GT2
root_radius = (outer_diameter / 2) - tooth_depth
outer_radius = outer_diameter / 2

# --- Modeling ---

# 1. Create the main cylindrical body (the hub)
# We make it slightly wider than the tooth width to seat into the flanges, 
# or we can model the whole stack. Let's model the core hub first.
hub = cq.Workplane("XY").circle(outer_radius).extrude(pulley_width)

# 2. Create the Tooth Cutter
# We'll create a single tooth cut profile and polar array it.
# A simple trapezoidal or rounded profile works for visualization.
tooth_cut_width = pitch * tooth_width_ratio
tooth_angle = 360.0 / num_teeth

# Create a cutting tool for one tooth gap
# We position it at the top (Y-axis)
cutter_profile = (
    cq.Workplane("XY")
    .workplane(offset=pulley_width / 2) # Center vertically relative to extrude
    .moveTo(0, outer_radius + 1.0) # Start outside
    .lineTo(tooth_cut_width / 2, outer_radius + 1.0)
    .lineTo(tooth_cut_width / 3, root_radius) # Taper in to root
    .lineTo(-tooth_cut_width / 3, root_radius)
    .lineTo(-tooth_cut_width / 2, outer_radius + 1.0)
    .close()
)

# Extrude the cutter through the hub length
cutter = cutter_profile.extrude(-pulley_width * 2) # Make sure it cuts through everything

# 3. Apply the cut in a polar array
for i in range(num_teeth):
    angle = i * tooth_angle
    # Rotate the cutter and subtract
    rotated_cutter = cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    hub = hub.cut(rotated_cutter)

# 4. Create the Flanges
# Left Flange
flange_l = (
    cq.Workplane("XY")
    .workplane(offset=-flange_width)
    .circle(flange_diameter / 2)
    .extrude(flange_width)
)

# Right Flange
flange_r = (
    cq.Workplane("XY")
    .workplane(offset=pulley_width)
    .circle(flange_diameter / 2)
    .extrude(flange_width)
)

# 5. Combine Parts
result = hub.union(flange_l).union(flange_r)

# 6. Create the Bore (Shaft Hole)
# Cut through the entire assembly
result = result.faces(">Z").workplane().circle(bore_diameter / 2).cutThruAll()

# 7. Final Polish (Optional Chamfers on the flanges for aesthetics)
# Select the outer edges of the flanges
result = result.edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5)

# Export or Render
if __name__ == "__main__":
    try:
        from cadquery import exporters
        # exporters.export(result, "pulley.step")
        pass # Used when running as script
    except ImportError:
        pass # Used in CQ-Editor