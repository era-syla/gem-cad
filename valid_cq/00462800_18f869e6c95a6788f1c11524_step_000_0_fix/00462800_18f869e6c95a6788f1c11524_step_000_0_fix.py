import cadquery as cq

# Parameters
postW = 20        # width of each post
postH = 50        # total height of each post
barH = 20         # height of the bottom bar
gap = 60          # distance between the inner faces of the posts
thickness = 3     # wall thickness for the hollow posts
depth = 20        # depth of the bracket (along Y axis)
filletR = 3       # fillet radius
baseW = 2 * postW + gap  # overall width in X

# Create the 2D cross‐section in the XZ plane
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (baseW, 0),
        (baseW, barH),
        (postW + gap, barH),
        (postW + gap, postH),
        (postW, postH),
        (postW, barH),
        (0, barH)
    ])
    .close()
)

# Extrude the profile to a solid
solid = profile.extrude(depth)

# Create inner pockets for hollowing the two posts
inner_h = postH - barH - thickness
inner_pocket = cq.Workplane("XY").box(postW - 2*thickness, depth + 1, inner_h)

# Position the pockets for left and right posts
pocket1 = inner_pocket.translate((postW/2, 0, barH + thickness + inner_h/2))
pocket2 = inner_pocket.translate((baseW - postW/2, 0, barH + thickness + inner_h/2))

# Subtract the pockets from the solid and fillet all edges
result = solid.cut(pocket1).cut(pocket2).edges().fillet(filletR)