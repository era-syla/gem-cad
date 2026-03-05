import cadquery as cq
import math

# Parameters
inner_diameter = 20.0
band_thickness = 1.0
band_height = 2.0

prong_count = 4
prong_width = 1.0
prong_depth = 1.0
prong_height = 5.0

gem_diameter = 8.0
gem_height = 6.0
gem_chamfer = 0.5

# Create ring band
result = (
    cq.Workplane("XY")
    .circle(inner_diameter/2 + band_thickness)
    .circle(inner_diameter/2)
    .extrude(band_height)
)

# Create prongs
prongs = None
for i in range(prong_count):
    angle_deg = i * 360.0 / prong_count
    x = (inner_diameter/2) * math.cos(math.radians(angle_deg))
    y = (inner_diameter/2) * math.sin(math.radians(angle_deg))
    prong = (
        cq.Workplane("XY")
        .box(prong_width, prong_depth, prong_height)
        .translate((x, y, band_height))
        .rotate((0,0,0), (0,0,1), angle_deg)
    )
    prongs = prong if prongs is None else prongs.union(prong)

result = result.union(prongs)

# Create faceted gemstone
gem = (
    cq.Workplane("XY")
    .polygon(8, gem_diameter)
    .extrude(gem_height)
    .translate((0, 0, band_height + prong_height))
    .edges("|Z")
    .chamfer(gem_chamfer)
)

result = result.union(gem)