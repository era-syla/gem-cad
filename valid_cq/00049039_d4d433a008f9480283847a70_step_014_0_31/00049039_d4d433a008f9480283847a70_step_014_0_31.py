import cadquery as cq

# Parameters
crankcase_length = 100
crankcase_width = 60
crankcase_height = 80

cylinder_radius = 20
cylinder_height = 60
cylinder_angle_v = 90  # V-angle
cylinder_fin_count = 15
cylinder_fin_thickness = 1
cylinder_fin_spacing = 3

head_height = 25
head_width = 45
head_length = 50

# Crankcase main body
crankcase = (
    cq.Workplane("XY")
    .box(crankcase_length, crankcase_width, crankcase_height)
    .edges("|Z")
    .fillet(10)
)

# Function to create a cylinder with cooling fins
def create_cylinder():
    cyl = cq.Workplane("XY").circle(cylinder_radius).extrude(cylinder_height)
    
    # Add cooling fins
    fin_z = 10
    for _ in range(cylinder_fin_count):
        fin = cq.Workplane("XY").workplane(offset=fin_z).circle(cylinder_radius + 5).extrude(cylinder_fin_thickness)
        cyl = cyl.union(fin)
        fin_z += cylinder_fin_thickness + cylinder_fin_spacing
        
    return cyl

# Function to create a cylinder head
def create_head():
    head = (
        cq.Workplane("XY")
        .box(head_length, head_width, head_height)
        .edges("|Z")
        .fillet(8)
        .edges(">Z")
        .fillet(5)
    )
    # Add some detail to the top
    detail = cq.Workplane("XY").workplane(offset=head_height/2).box(head_length - 10, head_width - 10, 5)
    head = head.union(detail)
    return head

# Create left cylinder and head
cyl_left = create_cylinder()
head_left = create_head()
full_cyl_left = cyl_left.union(head_left.translate((0, 0, cylinder_height + head_height/2)))

# Create right cylinder and head
cyl_right = create_cylinder()
head_right = create_head()
full_cyl_right = cyl_right.union(head_right.translate((0, 0, cylinder_height + head_height/2)))

# Position cylinders in a V configuration
angle_rad = cylinder_angle_v / 2
offset_y = crankcase_width / 4

full_cyl_left = full_cyl_left.rotate((0,0,0), (1,0,0), -angle_rad).translate((0, offset_y, crankcase_height/2))
full_cyl_right = full_cyl_right.rotate((0,0,0), (1,0,0), angle_rad).translate((0, -offset_y, crankcase_height/2))

# Combine everything
result = crankcase.union(full_cyl_left).union(full_cyl_right)

# Add some front details (gearbox/pump area)
front_box = cq.Workplane("YZ").workplane(offset=crankcase_length/2).box(crankcase_width*0.8, crankcase_height*0.6, 30)
front_box = front_box.edges("|X").fillet(5)
result = result.union(front_box)

front_cyl1 = cq.Workplane("YZ").workplane(offset=crankcase_length/2 + 30).center(15, -10).circle(8).extrude(20)
front_cyl2 = cq.Workplane("YZ").workplane(offset=crankcase_length/2 + 30).center(-15, -10).circle(8).extrude(20)
result = result.union(front_cyl1).union(front_cyl2)

# Add a rear detail (flywheel cover)
rear_cover = cq.Workplane("YZ").workplane(offset=-crankcase_length/2).circle(35).extrude(-15)
result = result.union(rear_cover)
