import cadquery as cq

# Create a bellows/accordion shape with multiple disc-like flanges
# The shape has a central cylinder with multiple disc flanges stacked vertically

# Parameters
inner_radius = 8
outer_radius = 18
flange_thickness = 3
gap_thickness = 3
num_flanges = 5
total_height = num_flanges * (flange_thickness + gap_thickness)

# Build using union of cylinders and discs
result = cq.Workplane("XY")

# Start with the central cylinder (spine)
result = cq.Workplane("XY").cylinder(total_height, inner_radius)

# Add each flange disc
for i in range(num_flanges):
    z_pos = -total_height/2 + i * (flange_thickness + gap_thickness) + flange_thickness/2
    flange = cq.Workplane("XY").workplane(offset=z_pos).circle(outer_radius).extrude(flange_thickness, both=True)
    result = result.union(flange)

# The top cap (smaller disc at very top)
top_z = total_height/2
top_cap = cq.Workplane("XY").workplane(offset=top_z - flange_thickness/2).circle(inner_radius + 3).extrude(flange_thickness, both=True)
result = result.union(top_cap)