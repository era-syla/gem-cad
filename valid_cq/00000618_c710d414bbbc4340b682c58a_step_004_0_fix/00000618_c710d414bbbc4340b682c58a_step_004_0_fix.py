import cadquery as cq

# 20x20 T-slot aluminum extrusion profile
# Length along Z axis

length = 80
size = 20
slot_width = 6
slot_depth = 4
slot_inner_width = 10
lip_height = 1.5
center_hole = 4.2

def make_tslot_profile():
    """Create a 20x20 T-slot extrusion cross-section"""
    
    # Start with a 20x20 square
    profile = (
        cq.Workplane("XY")
        .rect(size, size)
    )
    
    # We'll build the profile using face operations
    # Build cross section as a 2D profile
    
    pts_outer = [
        (-size/2, -size/2),
        (size/2, -size/2),
        (size/2, size/2),
        (-size/2, size/2),
    ]
    
    return profile

# Build the extrusion profile manually using vertices
# 20x20 profile with 4 T-slots (one on each face)

# Cross section points for T-slot profile
# Bottom face slot
sw = slot_width / 2      # 3
siw = slot_inner_width / 2  # 5
sd = slot_depth           # 4
lh = lip_height           # 1.5
s = size / 2              # 10

# Build cross-section as a wire
# The profile has slots on all 4 sides
# Let's build it step by step using polygon points

def tslot_cross_section(wp):
    """Draw T-slot 20x20 cross section"""
    pts = []
    
    # Going around the perimeter, starting from bottom-left, CCW
    # Bottom face with center slot
    pts += [
        (-s, -s),           # bottom-left corner
        (-siw, -s),         # bottom slot outer left
        (-siw, -s+lh),      # bottom slot lip left inner
        (-sw, -s+lh),       # bottom slot throat left
        (-sw, -s+sd),       # bottom slot inner left
        (sw, -s+sd),        # bottom slot inner right
        (sw, -s+lh),        # bottom slot throat right
        (siw, -s+lh),       # bottom slot lip right inner
        (siw, -s),          # bottom slot outer right
        (s, -s),            # bottom-right corner
    ]
    
    # Right face with slot
    pts += [
        (s, -siw),
        (s-lh, -siw),
        (s-lh, -sw),
        (s-sd, -sw),
        (s-sd, sw),
        (s-lh, sw),
        (s-lh, siw),
        (s, siw),
    ]
    
    # Top face with slot
    pts += [
        (siw, s),
        (siw, s-lh),
        (sw, s-lh),
        (sw, s-sd),
        (-sw, s-sd),
        (-sw, s-lh),
        (-siw, s-lh),
        (-siw, s),
        (-s, s),
    ]
    
    # Left face with slot
    pts += [
        (-s, siw),
        (-s+lh, siw),
        (-s+lh, sw),
        (-s+sd, sw),
        (-s+sd, -sw),
        (-s+lh, -sw),
        (-s+lh, -siw),
        (-s, -siw),
    ]
    
    return wp.polyline(pts).close()

# Create the profile
profile_wp = cq.Workplane("XY")
profile_wp = tslot_cross_section(profile_wp)

# Extrude to create the solid
solid = profile_wp.extrude(length)

# Add center hole
solid = (
    solid
    .faces(">Z")
    .workplane()
    .circle(center_hole / 2)
    .cutThruAll()
)

# Add small chamfers at slot corners - skip to avoid complexity
# The basic profile is done

result = solid