import cadquery as cq
import math

# Ring parameters
inner_radius = 8.5
outer_radius_band = 10.5
signet_width = 14.0
signet_height = 5.0
band_height = 6.0
total_height = 10.0

# Create the base ring band using revolution
# Build the ring profile in 2D then revolve

# The signet ring has:
# - A circular band at the bottom
# - A raised oval/rectangular signet face at top

# Create main ring body by revolving a profile
# Profile in XZ plane (X = radial, Z = axial)

# Band profile points (cross-section)
band_inner = inner_radius
band_outer = outer_radius_band

# Create the outer shell of the ring
# Use a swept/revolved approach

# Build ring as: outer torus-like shape minus inner cylinder hole

# Step 1: Create the signet top pad
# Step 2: Create the band
# Step 3: Union them
# Step 4: Subtract inner bore

# Create band (torus-like ring)
band = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .circle(outer_radius_band)
    .circle(inner_radius)
    .extrude(band_height)
)

# Create the signet face - elevated oval on top of band
# Position it at the top of the ring (positive X direction)
signet_elevation = band_height

# Create signet base - an elliptical mound on top
# Use a box-like shape with rounded top that sits on the ring

# Signet platform
signet = (
    cq.Workplane("XY")
    .workplane(offset=signet_elevation)
    .transformed(offset=cq.Vector(0, 0, 0))
    .ellipse(signet_width/2, signet_width/2 * 0.75)
    .extrude(signet_height)
)

# Now we need to shape the signet to follow the ring curvature
# Simplify: create a dome-like signet using a sphere intersection

# Create a large sphere to dome the top
dome_sphere = (
    cq.Workplane("XY")
    .workplane(offset=signet_elevation + signet_height - 3)
    .sphere(signet_width * 0.9)
)

# Combine band and signet
ring_outer = band.union(signet)

# Dome the top by intersecting with sphere region - skip complex boolean
# Instead create the signet top as ellipse extrude with fillet

# Better approach: build full ring with revolve profile
# Ring cross section: trapezoidal band that widens at top on one side

# Complete rebuild with simpler geometry
# Main ring torus
result_band = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius_band, 0)
    .lineTo(outer_radius_band, band_height)
    .lineTo(inner_radius, band_height)
    .close()
    .revolve(360, (0, 0, 0), (0, 1, 0))
)

# Signet top - create on top face, centered at angle 0 (along X axis)
# Place a rounded rectangular pad
signet_pad = (
    cq.Workplane("XY")
    .workplane(offset=band_height)
    .transformed(offset=cq.Vector(outer_radius_band - 1, 0, 0))
    .ellipse(signet_width/2 - 1, (signet_width/2 - 1) * 0.78)
    .extrude(signet_height)
)

# Union band and signet pad
ring_body = result_band.union(signet_pad)

# Fillet the signet edges
try:
    ring_body = ring_body.edges("|Z").edges(cq.NearestToPointSelector((outer_radius_band + signet_width/2, 0, band_height + signet_height/2))).fillet(2.0)
except:
    pass

# Cut the inner bore through everything
inner_bore = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .circle(inner_radius)
    .extrude(band_height + signet_height + 2)
)

ring_body = ring_body.cut(inner_bore)

# Add letter C on the signet face (engraved)
letter_c = (
    cq.Workplane("XY")
    .workplane(offset=band_height + signet_height - 0.8)
    .transformed(offset=cq.Vector(outer_radius_band - 1, 0, 0))
    .text("C", 7, 1.0, cut=False, halign='center', valign='center')
)

try:
    result = ring_body.cut(letter_c)
except:
    result = ring_body