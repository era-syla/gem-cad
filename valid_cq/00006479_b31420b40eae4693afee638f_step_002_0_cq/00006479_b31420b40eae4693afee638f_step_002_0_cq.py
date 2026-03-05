import cadquery as cq

# --- Parametric Dimensions ---

# Main box dimensions (estimated from visual proportions)
box_length = 80.0
box_width = 60.0
box_height = 40.0
wall_thickness = 2.0
fillet_radius = 2.0

# Hinge/Tab dimensions (top surface)
hinge_height = 15.0
hinge_width = 12.0
hinge_thickness = 3.0
hinge_hole_diam = 4.0
hinge_spacing = 30.0  # Distance between hinge pairs
hinge_pair_gap = 10.0 # Distance between the two tabs in a pair
rib_thickness = 1.5   # Thickness of support ribs on hinges

# Mounting post dimensions (top surface)
post_height = 10.0
post_diam = 5.0
post_hole_diam = 2.5
post_offset_x = 30.0
post_offset_y = 20.0

# Bottom cutout dimensions
side_cutout_width = 25.0
side_cutout_height = 15.0
side_cutout_divider_width = 4.0 # Divider between the two rectangular holes

# Bottom plate (looks like a separate PCB or mounting plate, simpler representation)
base_plate_thickness = 2.0
base_plate_standoff_height = 5.0

# --- Modeling Steps ---

# 1. Create the main hollow box
# Create outer shell
main_body = (
    cq.Workplane("XY")
    .box(box_length, box_width, box_height)
    .edges("|Z")
    .fillet(fillet_radius)
)

# Hollow it out (shelling from bottom)
# Since shelling can sometimes be tricky with complex bottoms, 
# let's just make a smaller box and cut it.
inner_body = (
    cq.Workplane("XY")
    .box(box_length - 2*wall_thickness, 
         box_width - 2*wall_thickness, 
         box_height - 2*wall_thickness)
    .edges("|Z")
    .fillet(fillet_radius - wall_thickness if fillet_radius > wall_thickness else 0.1)
)

# Combine to make the hollow shell, open at the bottom (Z-)
shell = main_body.cut(inner_body.translate((0, 0, -wall_thickness)))

# 2. Create the Hinge Tabs on Top
# Define a single hinge tab shape
def create_hinge_tab():
    tab = (
        cq.Workplane("XZ")
        .rect(hinge_width, hinge_height)
        .extrude(hinge_thickness)
        .edges(">Z and |Y") # Select top edge
        .fillet(hinge_width/2 - 0.1) # Round top
        .faces(">Y").workplane()
        .hole(hinge_hole_diam)
    )
    
    # Add triangular support rib
    rib = (
        cq.Workplane("YZ")
        .moveTo(0, 0)
        .lineTo(hinge_height * 0.7, 0)
        .lineTo(0, hinge_width * 0.6)
        .close()
        .extrude(rib_thickness/2, both=True)
    )
    # Orient rib to align with tab (tab is extruded in Y, rib needs to be centered on it)
    rib = rib.rotate((0,0,0), (0,1,0), 90).translate((0, hinge_thickness/2, 0))
    
    return tab.union(rib)

hinge_geometry = create_hinge_tab()

# Position the hinges
# We have two pairs.
hinge_y_pos = box_width/2 - 15 # Position from center
hinge_x_spacing = 35

# Left pair
h1 = hinge_geometry.translate((-hinge_x_spacing, hinge_y_pos, box_height/2))
h2 = hinge_geometry.translate((-hinge_x_spacing + hinge_pair_gap, hinge_y_pos, box_height/2))
# Right pair
h3 = hinge_geometry.translate((hinge_x_spacing - hinge_pair_gap, hinge_y_pos, box_height/2))
h4 = hinge_geometry.translate((hinge_x_spacing, hinge_y_pos, box_height/2))

hinges = h1.union(h2).union(h3).union(h4)


# 3. Create Mounting Posts on Top
def create_post():
    p = (
        cq.Workplane("XY")
        .circle(post_diam/2)
        .extrude(post_height)
        .faces(">Z").workplane()
        .hole(post_hole_diam, depth=post_height) # Blind hole
    )
    return p

post_geo = create_post()

# Position posts (3 visible in image, seemingly roughly arranged)
# Front Left
p1 = post_geo.translate((-box_length/2 + 10, -box_width/2 + 10, box_height/2))
# Front Center/Right-ish
p2 = post_geo.translate((0, -box_width/2 + 10, box_height/2))
# Far Right
p3 = post_geo.translate((box_length/2 - 8, box_width/2 - 8, box_height/2))

posts = p1.union(p2).union(p3)

# 4. Create Side Cutouts
# Looking at the front/right face
cutout_sketch = (
    cq.Workplane("XZ")
    .rect(side_cutout_width, side_cutout_height)
    .translate((box_length/3, -box_height/2 + side_cutout_height/2)) 
)

# There seem to be two rectangular cutouts separated by a thin wall on the side
cutout1 = (
    cq.Workplane("YZ")
    .rect(12, 18)
    .extrude(10) # Cut depth
    .translate((box_length/2, 5, -box_height/2 + 9))
)

cutout2 = (
    cq.Workplane("YZ")
    .rect(12, 18)
    .extrude(10)
    .translate((box_length/2, -10, -box_height/2 + 9))
)

# 5. Create the Bottom Plate/Structure
# This looks like a base plate attached via standoffs
base_plate = (
    cq.Workplane("XY")
    .box(box_length + 4, box_width + 4, base_plate_thickness)
    .edges("|Z")
    .fillet(fillet_radius)
    .translate((0, 0, -box_height/2 - base_plate_standoff_height - base_plate_thickness/2))
)

# Standoffs connecting shell to base
standoff_geo = (
    cq.Workplane("XY")
    .circle(3.5)
    .extrude(base_plate_standoff_height)
    .translate((0, 0, -box_height/2 - base_plate_standoff_height))
)

standoffs = (
    standoff_geo.translate((box_length/2 - 5, box_width/2 - 5, 0))
    .union(standoff_geo.translate((-box_length/2 + 5, box_width/2 - 5, 0)))
    .union(standoff_geo.translate((box_length/2 - 5, -box_width/2 + 5, 0)))
    .union(standoff_geo.translate((-box_length/2 + 5, -box_width/2 + 5, 0)))
)


# --- Assembly ---

# Combine top features
top_assembly = shell.union(hinges).union(posts)

# Apply cutouts
top_assembly = top_assembly.cut(cutout1).cut(cutout2)

# Combine with bottom assembly
result = top_assembly.union(base_plate).union(standoffs)

# Optional: Add small detail cutouts to the base plate to match image (slots)
slot_cut = (
    cq.Workplane("XY")
    .rect(4, 10)
    .extrude(5)
    .translate((box_length/2, 0, -box_height/2 - base_plate_standoff_height))
)
result = result.cut(slot_cut)

# Return the final object
if 'show_object' in globals():
    show_object(result)