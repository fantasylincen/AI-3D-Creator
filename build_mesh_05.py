import cadquery as cq
import math

length = 120.0
width = 80.0
height = 15.0
wall_thickness = 2.5
outer_fillet = 5.0

grid_length = 60.0
grid_width = 40.0
hex_flat_to_flat = 3.0
hex_wall = 1.5

hex_radius = hex_flat_to_flat / math.sqrt(3.0)
dx = hex_flat_to_flat + hex_wall
dy = dx * math.sqrt(3.0) / 2.0

col_count = int(math.ceil(grid_length / dx)) + 2
row_count = int(math.ceil(grid_width / dy)) + 2

outer_box = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

x_min, x_max = -length/2.0, length/2.0
y_min, y_max = -width/2.0, width/2.0
z_min, z_max = 0.0, height

c1 = cq.selectors.BoxSelector((x_min - 1, y_min - 1, z_min - 1), (x_min + outer_fillet + 1, y_min + outer_fillet + 1, z_max + 1))
c2 = cq.selectors.BoxSelector((x_max - outer_fillet - 1, y_min - 1, z_min - 1), (x_max + 1, y_min + outer_fillet + 1, z_max + 1))
c3 = cq.selectors.BoxSelector((x_max - outer_fillet - 1, y_max - outer_fillet - 1, z_min - 1), (x_max + 1, y_max + 1, z_max + 1))
c4 = cq.selectors.BoxSelector((x_min - 1, y_max - outer_fillet - 1, z_min - 1), (x_min + outer_fillet + 1, y_max + 1, z_max + 1))

selected_edges = outer_box.edges("|Z").edges(c1).add(outer_box.edges("|Z").edges(c2)).add(outer_box.edges("|Z").edges(c3)).add(outer_box.edges("|Z").edges(c4))
outer_box = selected_edges.fillet(outer_fillet)

inner_box = cq.Workplane("XY").box(
    length - 2.0 * wall_thickness, 
    width - 2.0 * wall_thickness, 
    height - wall_thickness, 
    centered=(True, True, False)
)
shell = outer_box.cut(inner_box)

hex_pattern = cq.Workplane("XY", origin=(0, 0, height - wall_thickness - 1))

hex_centers = []
start_x = -((col_count - 1) * dx) / 2.0
start_y = -((row_count - 1) * dy) / 2.0

for r in range(row_count):
    y = start_y + r * dy
    shift_x = dx / 2.0 if (r % 2 == 1) else 0.0
    for c in range(col_count):
        x = start_x + c * dx + shift_x
        if (abs(x) <= grid_length / 2.0) and (abs(y) <= grid_width / 2.0):
            hex_centers.append((x, y))

if hex_centers:
    hex_pattern = hex_pattern.pushPoints(hex_centers).polygon(6, hex_radius * 2.0, circumscribed=True).extrude(wall_thickness + 2.0, combine=False)
    result = shell.cut(hex_pattern)
else:
    result = shell

cq.exporters.export(result, "output_model.3mf")
