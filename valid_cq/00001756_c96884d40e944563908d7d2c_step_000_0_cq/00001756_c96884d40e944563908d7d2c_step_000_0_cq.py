import cadquery as cq

# Parameters
ground_size_x = 200
ground_size_y = 200
ground_thickness = 1

# Main house parameters
house_main_width = 80
house_main_depth = 40
house_main_height = 30
roof_height = 15

# Wing parameters
wing_width = 40
wing_depth = 50
wing_height = 20

# Tree/Prop parameters
tree_trunk_h = 10
tree_trunk_r = 2
tree_top_h = 30
tree_top_r = 8

# Helper function to create a basic house block with gable roof
def make_house_section(width, depth, wall_height, roof_height, orientation='x'):
    # Base box
    walls = cq.Workplane("XY").box(width, depth, wall_height, centered=(True, True, False))
    
    # Roof prism
    if orientation == 'x':
        # Roof ridge runs along X
        pts = [
            (-width/2, -depth/2),
            (width/2, -depth/2),
            (0, 0) # Peak relative to center
        ]
        # Wedge shape creation for roof is easier with extrusion of a triangle
        roof_profile = cq.Workplane("YZ").workplane(offset=-width/2).moveTo(-depth/2, wall_height).lineTo(depth/2, wall_height).lineTo(0, wall_height + roof_height).close()
        roof = roof_profile.extrude(width)
    else:
        # Roof ridge runs along Y
        roof_profile = cq.Workplane("XZ").workplane(offset=-depth/2).moveTo(-width/2, wall_height).lineTo(width/2, wall_height).lineTo(0, wall_height + roof_height).close()
        roof = roof_profile.extrude(depth)
        
    return walls.union(roof)

# --- Construction ---

# 1. Ground Plane
ground = cq.Workplane("XY").box(ground_size_x, ground_size_y, ground_thickness, centered=(True, True, False))

# 2. Main Building (2-story section)
main_building = make_house_section(house_main_width, house_main_depth, house_main_height, roof_height, orientation='x')
main_building = main_building.translate((0, 20, 0))

# 3. Side Wing (Single story, intersecting main)
wing = make_house_section(wing_width, wing_depth, wing_height, roof_height * 0.8, orientation='y')
wing = wing.translate((-30, -10, 0))

# 4. Front Porch / Sunroom extension
porch_width = 30
porch_depth = 20
porch_height = 15
porch_roof_h = 8
porch = make_house_section(porch_width, porch_depth, porch_height, porch_roof_h, orientation='x')
porch = porch.translate((-30, -50, 0)) # Positioned in front of the wing

# 5. Small entrance gable
entry_width = 15
entry_depth = 10
entry_height = 15
entry_roof_h = 8
entry = make_house_section(entry_width, entry_depth, entry_height, entry_roof_h, orientation='y')
entry = entry.translate((-50, -35, 0)) # Stick out to the left side

# 6. Windows and Doors (Subtractions)
# Main building windows
win_w, win_h = 8, 10
windows = cq.Workplane("XY")

# Front facing windows on main building
for x_pos in [10, 25]:
    windows = windows.union(cq.Workplane("XZ").workplane(offset=20 - house_main_depth/2).moveTo(x_pos, 20).rect(win_w, win_h).extrude(5))
    windows = windows.union(cq.Workplane("XZ").workplane(offset=20 - house_main_depth/2).moveTo(x_pos, 8).rect(win_w, win_h).extrude(5))

# Side wing windows
for y_pos in [-10, -25]:
    windows = windows.union(cq.Workplane("YZ").workplane(offset=-30 + wing_width/2).moveTo(y_pos, 10).rect(win_w, win_h).extrude(5))

# Sunroom windows (multiple narrow ones)
sunroom_cuts = cq.Workplane("XY")
for x_pos in range(-40, -20, 5):
     sunroom_cuts = sunroom_cuts.union(cq.Workplane("XZ").workplane(offset=-60).moveTo(x_pos, 8).rect(3, 8).extrude(5))
    
# 7. Small Shed
shed_w = 15
shed_d = 15
shed_h = 12
shed = make_house_section(shed_w, shed_d, shed_h, 5, orientation='y')
shed = shed.translate((-20, -80, 0))

# 8. Trees
def make_tree():
    trunk = cq.Workplane("XY").circle(tree_trunk_r).extrude(tree_trunk_h)
    top = cq.Workplane("XY").workplane(offset=tree_trunk_h).circle(tree_top_r).extrude(tree_top_h)
    # Fillet the top to make it organic
    top = top.edges(">Z").fillet(tree_top_r - 0.1)
    return trunk.union(top)

tree1 = make_tree().translate((40, -70, 0))
tree2 = make_tree().translate((80, -40, 0))

# 9. Patio / Walkway
patio = cq.Workplane("XY").rect(40, 60).extrude(0.5).translate((20, -20, 0.5))
pool_cutout = cq.Workplane("XY").rect(20, 30).extrude(1).translate((20, -20, 0))

# Combine assembly
house_assembly = main_building.union(wing).union(porch).union(entry)
house_assembly = house_assembly.cut(windows).cut(sunroom_cuts)

# Final Result
result = ground.union(house_assembly).union(shed).union(tree1).union(tree2).union(patio)
result = result.cut(pool_cutout) 

# Export for visualization if needed (not required by prompt but good practice)
# cq.exporters.export(result, "house.step")