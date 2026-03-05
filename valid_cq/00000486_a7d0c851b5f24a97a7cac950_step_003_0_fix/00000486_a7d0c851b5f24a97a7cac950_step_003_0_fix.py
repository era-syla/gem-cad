import cadquery as cq
import math

# Thickness of sheet metal
t = 1.5

# ─── Part 1: Rectangular bar with curl hooks on each end ───────────────────

bar_l = 80
bar_w = 18
bar_t = t

# Main bar
bar = cq.Workplane("XY").box(bar_l, bar_w, bar_t)

# Curl hooks on each end: small cylindrical curl
curl_r = 4
curl_t = bar_w - 4

def make_curl(outer_r, thickness, angle_deg=270):
    """Make a curl (partial torus cross-section swept) as a solid."""
    # Use revolve to make a curl: a rectangle revolved around an axis
    inner_r = outer_r - t
    # Profile in XZ plane, revolution around Z axis at x = outer_r
    pts = []
    for a in range(0, angle_deg + 1, 10):
        rad = math.radians(a)
        pts.append((outer_r * math.cos(rad), outer_r * math.sin(rad)))
    
    # Build curl as a swept arc of rectangular cross-section
    path = (cq.Workplane("XY")
            .moveTo(outer_r - t/2, 0)
            .radiusArc((-(outer_r - t/2), 0), -(outer_r - t/2))
            )
    
    profile = (cq.Workplane("XZ")
               .workplane(offset=0)
               .center(outer_r - t/2, 0)
               .rect(t, thickness)
               )
    return profile.sweep(path)

# Build curl hooks manually using revolve
def make_hook(outer_r, width):
    inner_r = outer_r - t
    hook = (cq.Workplane("XZ")
            .moveTo(inner_r, -width/2)
            .lineTo(outer_r, -width/2)
            .lineTo(outer_r, width/2)
            .lineTo(inner_r, width/2)
            .close()
            .revolve(270, (0, 0, 0), (0, 1, 0))
            )
    return hook

hook_r = 5
hook_w = bar_w - 2

hook1 = make_hook(hook_r, hook_w)
# Position hook1 at +x end of bar, rotated so open side faces inward
hook1 = hook1.translate((bar_l/2 + hook_r - t, 0, 0))

hook2 = make_hook(hook_r, hook_w)
hook2 = hook2.rotate((0,0,0),(0,0,1), 180).translate((-bar_l/2 - hook_r + t, 0, 0))

bar_assembly = bar.union(hook1).union(hook2)

# ─── Part 2: Star/clover shaped plate with center hole and hooks ────────────

# Base disc
disc_r = 22
disc = cq.Workplane("XY").workplane(offset=30).circle(disc_r).extrude(t)

# Three lobes for the clover shape
lobe_r = 10
lobe_dist = 18
for angle in [90, 210, 330]:
    rad = math.radians(angle)
    lx = lobe_dist * math.cos(rad)
    ly = lobe_dist * math.sin(rad)
    lobe = cq.Workplane("XY").workplane(offset=30).center(lx, ly).circle(lobe_r).extrude(t)
    disc = disc.union(lobe)

# Three notch cuts between lobes
notch_r = 12
for angle in [150, 270, 30]:
    rad = math.radians(angle)
    nx = (disc_r - 2) * math.cos(rad)
    ny = (disc_r - 2) * math.sin(rad)
    notch = cq.Workplane("XY").workplane(offset=29).center(nx, ny).circle(notch_r).extrude(t + 2)
    disc = disc.cut(notch)

# Center hole
center_hole = cq.Workplane("XY").workplane(offset=29).circle(4).extrude(t + 2)
disc = disc.cut(center_hole)

# Hook on one lobe (top lobe at 90 degrees)
hook3 = make_hook(hook_r, 8)
hook3 = hook3.rotate((0,0,0),(1,0,0), 90).translate((0, disc_r + hook_r - t, 30 + t/2))
disc = disc.union(hook3)

# Connecting tab between bar and disc
tab_l = 20
tab_w = 8
tab = (cq.Workplane("XY")
       .workplane(offset=30)
       .center(-bar_l/2 + tab_l/2 - 5, 0)
       .box(tab_l, tab_w, t)
       )

# Combine everything
result = bar_assembly.union(disc).union(tab)