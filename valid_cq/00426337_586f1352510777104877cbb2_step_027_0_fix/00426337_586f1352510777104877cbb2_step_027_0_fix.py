import cadquery as cq

# Define the profile of the part in the X–Z plane
profile = [
    (0,   0),    # axis start
    (0.2, 5),    # small point
    (0.5, 10),   # narrow tip radius
    (0.5, 50),   # first main cylinder
    (0.6, 52),   # first ring
    (0.6, 150),  # long middle cylinder
    (0.4, 152),  # second ring
    (0.4, 170),  # back cylinder
    (0.45,172),  # back decorative ring 1
    (0.5, 174),  # back decorative ring 2
    (0.35,180),  # back cylinder taper
    (0.35,200),  # end cylinder
    (0,   200)   # close to axis
]

# Revolve the profile to create the 3D shape
result = cq.Workplane("XZ").polyline(profile).close().revolve()