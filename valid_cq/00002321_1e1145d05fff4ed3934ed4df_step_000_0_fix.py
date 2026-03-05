import cadquery as cq

# Build the complex shape by creating a base and adding/subtracting features
# Looking at the image, this appears to be a flat plate with notches and tabs

# Create the shape using a 2D profile and extrude
height = 5

# Define the outline as a series of points for a complex polygon
# The shape looks like a cross/bracket shape with notches

result = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (10, 0),
        (10, -10),
        (20, -10),
        (20, 0),
        (30, 0),
        (30, 10),
        (50, 10),
        (50, 20),
        (40, 20),
        (40, 30),
        (30, 30),
        (30, 40),
        (20, 40),
        (20, 30),
        (10, 30),
        (10, 40),
        (0, 40),
        (0, 30),
        (-10, 30),
        (-10, 20),
        (-20, 20),
        (-20, 10),
        (-10, 10),
        (-10, 0),
        (0, 0),
    ])
    .close()
    .extrude(height)
)

# Let me redesign based on more careful observation of the image
# The shape appears to have:
# - A main body
# - A tab extending to the upper right
# - A notch cut on the left
# - Steps/notches on the bottom

# Start fresh with a cleaner approach
w = 60
h = 50
t = 6  # thickness

# Main rectangular base
base = cq.Workplane("XY").rect(w, h).extrude(t)

# Cut top-left notch
cut1 = cq.Workplane("XY").transformed(offset=(-15, 10, 0)).rect(20, 20).extrude(t)

# Cut bottom-right notch  
cut2 = cq.Workplane("XY").transformed(offset=(15, -10, 0)).rect(20, 20).extrude(t)

# Let me try a direct polygon approach more carefully

pts = [
    (-30, -25),
    (10, -25),
    (10, -35),
    (20, -35),
    (20, -25),
    (30, -25),
    (30, -15),
    (45, -15),
    (45, 0),
    (30, 0),
    (30, 15),
    (20, 15),
    (20, 25),
    (10, 25),
    (10, 15),
    (-10, 15),
    (-10, 25),
    (-20, 25),
    (-20, 15),
    (-30, 15),
    (-30, 5),
    (-40, 5),
    (-40, -5),
    (-30, -5),
    (-30, -25),
]

result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(t)
)