import cadquery as cq

# Parametric dimensions
r_outer = 50.0
h = 16.0
r_inner = 16.0
slit_w = 0.3

# Calculate the radius of the sphere to achieve the desired dome height and outer radius
R = (h**2 + r_outer**2) / (2 * h)

# Create the main dome body
dome = (
    cq.Workplane("XY")
    .sphere(R)
    .translate((0, 0, h - R))
)

# Cut the bottom half of the sphere to create a flat base
cut_box = cq.Workplane("XY").box(R*3, R*3, R*3).translate((0, 0, -R*1.5))
dome = dome.cut(cut_box)

# Create the circular groove (inner circle)
circ_groove = (
    cq.Workplane("XY")
    .circle(r_inner + slit_w/2)
    .extrude(h + 5)
    .cut(
        cq.Workplane("XY")
        .circle(r_inner - slit_w/2)
        .extrude(h + 5)
    )
)

# Create the radial groove (slit from the inner circle to the outer edge)
L = r_outer - r_inner + 5
rad_groove = (
    cq.Workplane("XY")
    .rect(L, slit_w)
    .extrude(h + 5)
    .translate((L/2 + r_inner - 1, 0, 0))
    .rotate((0, 0, 0), (0, 0, 1), 210)  # Rotate to match the perspective in the image
)

# Subtract the grooves from the dome
result = dome.cut(circ_groove).cut(rad_groove)