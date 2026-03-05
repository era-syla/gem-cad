import cadquery as cq

# Parameters
outer_w = 78
outer_h = 150
wall_th = 2
base_th = 2
wall_h = 12

# Camera cut parameters
camera_w = 20
camera_h = 12
camera_offset = 10  # distance from top edge to camera center
camera_z = base_th + 0.1  # small z‐extent so cut only through base

# Side pocket parameters
pocket_w = 12
pocket_h = 6

# Bottom hook parameters
hook_w = 12
hook_h = 4

# Build base plate
result = cq.Workplane("XY").rect(outer_w, outer_h).extrude(base_th)

# Build side walls
result = result.faces(">Z").workplane().rect(outer_w - 2 * wall_th, outer_h - 2 * wall_th).extrude(wall_h)

# Fillet all vertical outer edges
result = result.edges("|Z").fillet(1.5)

# Cut camera opening through base plate only
result = result.cut(
    cq.Workplane("XZ", origin=(0, outer_h / 2 - camera_offset, base_th / 2))
      .rect(camera_w, camera_z)
      .extrude(-100)
)

# Cut side button pockets
x_pock = outer_w / 2 - wall_th / 2
z_pock = base_th + wall_h / 2

# Right pocket
pocket = (
    cq.Workplane("YZ", origin=(x_pock, 0, z_pock))
      .rect(pocket_w, pocket_h)
      .extrude(-100)
)
result = result.cut(pocket)

# Left pocket
pocket2 = (
    cq.Workplane("YZ", origin=(-x_pock, 0, z_pock))
      .rect(pocket_w, pocket_h)
      .extrude(100)
)
result = result.cut(pocket2)

# Cut bottom hooks
inner_w = outer_w - 2 * wall_th
y_hook = -(outer_h / 2 - wall_th / 2)

# Right hook
cut1 = (
    cq.Workplane("XY", origin=(inner_w / 2 - hook_w / 2, y_hook, 0))
      .rect(hook_w, hook_h)
      .extrude(wall_h + 1)
)
result = result.cut(cut1)

# Left hook
cut2 = (
    cq.Workplane("XY", origin=(-(inner_w / 2 - hook_w / 2), y_hook, 0))
      .rect(hook_w, hook_h)
      .extrude(wall_h + 1)
)
result = result.cut(cut2)