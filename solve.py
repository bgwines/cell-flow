#!/opt/homebrew/bin/python3

import copy
import math
import networkx
import re

# Python-only params
X = 0
Y = 1
Z = 2
PT_NAME_RE = re.compile(r'x=(\d+),y=(\d+),z=(\d+)')
TRUE_SOURCE_NAME = "true_source"
TRUE_SINK_NAME = "true_sink"

# OpenSCAD-only params
GRANULARITY = 10
CELL_H = 5

# dimensions
PLATE_LEN_X = 40
PLATE_LEN_Y = 20
PLATE_LEN_Z = 5
POINTS = [[x, y, z]
          for x in range(PLATE_LEN_X)
          for y in range(PLATE_LEN_Y)
          for z in range(PLATE_LEN_Z)]
EMPTY_MESH = [[[
            None for _ in range(PLATE_LEN_Z)
        ] for _ in range(PLATE_LEN_Y)
    ] for _ in range(PLATE_LEN_X)]

# locations
SOURCES = [[5,14,PLATE_LEN_Z-1]]
SINKS = [[15,5,0], [29,16,0], [0,0,0]]

# graph params
EDGE_CAPACITY = 1
EDGE_WEIGHT = 1
SOURCE_OUTFLOW_CAPACITY = 5 * EDGE_CAPACITY
SINK_INFLOW_CAPACITY = SOURCE_OUTFLOW_CAPACITY / len(SINKS)


def write_spec(mesh):
    with open("spec.scad", "w") as f:
        f.write(f"""
    $GRANULARITY = {GRANULARITY};

    $PLATE_LEN_X = {PLATE_LEN_X};
    $PLATE_LEN_Y = {PLATE_LEN_Y};
    $PLATE_LEN_Z = {PLATE_LEN_Z};

    $CELL_H = {CELL_H};
    $SOURCES = {SOURCES};
    $SINKS = {SINKS};

    $COLORS = {mesh};
    """)


def in_bounds(pt):
    return (0 <= pt[X] and pt[X] < PLATE_LEN_X and
            0 <= pt[Y] and pt[Y] < PLATE_LEN_Y and
            0 <= pt[Z] and pt[Z] < PLATE_LEN_Z)


def neighbors(pt):
    def apply_(delta, pt):
        (i, d) = delta
        new_pt = pt.copy()
        new_pt[i] = pt[i] + d
        return new_pt

    deltas = [(i, d) for i in range(3) for d in (-1,1)]
    candidates = [apply_(delta, pt) for delta in deltas]
    return [c for c in candidates if in_bounds(c)]


def solve():
    name = lambda pt: f"x={pt[X]},y={pt[Y]},z={pt[Z]}"
    graph = networkx.DiGraph()
    for pt in POINTS:
        for n in neighbors(pt):
            graph.add_edge(name(pt), name(n), capacity=EDGE_CAPACITY, weight=EDGE_WEIGHT)

    for source in SOURCES:
        graph.add_edge(TRUE_SOURCE_NAME, name(source), capacity=SOURCE_OUTFLOW_CAPACITY)
    for sink in SINKS:
        graph.add_edge(name(sink), TRUE_SINK_NAME, capacity=SINK_INFLOW_CAPACITY)


    min_cost_flow = networkx.max_flow_min_cost(
        graph, TRUE_SOURCE_NAME, TRUE_SINK_NAME)
    # print(f"Maximum flow: {flow_value}")
    print(f"outflow capacity: {SOURCE_OUTFLOW_CAPACITY}")
    print(f"inflow capacity: {SINK_INFLOW_CAPACITY}")

    mesh = copy.deepcopy(EMPTY_MESH)
    for [x, y, z] in POINTS:
        edges = min_cost_flow[name([x, y, z])]
        mesh[x][y][z] = sum(edges.values()) / SOURCE_OUTFLOW_CAPACITY
    return mesh


def main():
    mesh = solve()
    write_spec(mesh)


if __name__ == "__main__":
    main()
