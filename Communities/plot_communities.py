#!/usr/bin/env python3
"""
Plot every community from one or more runs: x = community size, y = edge density.
Each run is drawn in its own color, with a matching dashed line at its size-weighted
mean density (each community weighted by its number of nodes, i.e. the mean over
nodes of the edge density of the node's community).

Usage:
  python plot_communities.py --graph edges.txt \
      --run Leiden=leiden.txt --run Louvain=louvain.txt --run infomap.txt \
      [--out plot.png] [--logx] [--include-singletons]

--run may be repeated. Each one accepts "label=path" or just "path"
(a bare path is labeled with its file name, minus the extension).

Graph file: one edge per line, "u v" (extra columns ignored, lines starting
with # or % skipped). Treated as undirected and unweighted; self-loops and
duplicate edges are dropped.

Community file: one community per line, whitespace-separated node IDs.
"""
import argparse
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_graph(path):
    edges = set()
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line[0] in "#%":
                continue
            parts = line.split()
            u, v = int(parts[0]), int(parts[1])
            if u == v:
                continue
            edges.add((min(u, v), max(u, v)))
    return edges


def read_communities(path):
    comms = []
    with open(path) as f:
        for line in f:
            nodes = [int(x) for x in line.split()]
            if nodes:
                comms.append(nodes)
    return comms


def per_community(edges, comms, include_singletons=False):
    """Return (sizes, densities, Q). Singletons are skipped unless requested."""
    m = len(edges)
    deg = defaultdict(int)
    for u, v in edges:
        deg[u] += 1
        deg[v] += 1

    comm_of = {}
    for i, nodes in enumerate(comms):
        for n in nodes:
            if n in comm_of:
                raise ValueError(f"Node {n} appears in more than one community "
                                 "(overlapping communities are not supported)")
            comm_of[n] = i

    edges_in = defaultdict(int)
    for u, v in edges:
        cu, cv = comm_of.get(u), comm_of.get(v)
        if cu is not None and cu == cv:
            edges_in[cu] += 1

    sizes, densities = [], []
    q = 0.0
    for i, nodes in enumerate(comms):
        n = len(nodes)
        d_c = sum(deg[x] for x in nodes)
        q += edges_in[i] / m - (d_c / (2.0 * m)) ** 2
        if n < 2:
            if include_singletons:
                sizes.append(n)
                densities.append(0.0)
            continue
        sizes.append(n)
        densities.append(edges_in[i] / (n * (n - 1) / 2.0))
    return sizes, densities, q


def size_weighted_mean(sizes, densities):
    """Mean density with each community weighted by its node count.

    Equivalent to giving every node the density of its community and averaging
    over nodes. Only communities in `sizes`/`densities` (i.e. the plotted ones)
    contribute.
    """
    total = sum(sizes)
    if total == 0:
        return 0.0
    return sum(s * d for s, d in zip(sizes, densities)) / total


def parse_run(spec):
    """Turn 'label=path' or 'path' into (label, path)."""
    if os.path.exists(spec) or "=" not in spec:
        return os.path.splitext(os.path.basename(spec))[0], spec
    label, path = spec.split("=", 1)
    return label, path


def get_colors(n):
    """n distinct colors: tab10 for up to 10 runs, tab20 up to 20, else evenly spaced hues."""
    if n <= 10:
        cmap = plt.get_cmap("tab10")
        return [cmap(i) for i in range(n)]
    if n <= 20:
        cmap = plt.get_cmap("tab20")
        return [cmap(i) for i in range(n)]
    cmap = plt.get_cmap("hsv")
    return [cmap(i / n) for i in range(n)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graph", required=True)
    ap.add_argument("--run", required=True, action="append",
                    help="label=path or path; repeat for multiple runs")
    ap.add_argument("--out", default="communities_plot.png")
    ap.add_argument("--logx", action="store_true", help="log-scale x axis")
    ap.add_argument("--include-singletons", action="store_true",
                    help="plot singleton communities with density 0 (default: skip)")
    args = ap.parse_args()

    runs = [parse_run(spec) for spec in args.run]
    colors = get_colors(len(runs))

    edges = read_graph(args.graph)
    print(f"Graph: {len(edges)} undirected edges")

    fig, ax = plt.subplots(figsize=(8, 5))

    for (label, path), color in zip(runs, colors):
        comms = read_communities(path)
        sizes, densities, q = per_community(edges, comms, args.include_singletons)

        mean_d = size_weighted_mean(sizes, densities)
        print(f"{label}: communities={len(comms)}  plotted={len(sizes)}  "
              f"size-weighted mean density={mean_d:.4f}  Q={q:.4f}")

        ax.scatter(sizes, densities, s=18, alpha=0.6, color=color,
                   edgecolors="none",
                   label=f"{label} (n={len(sizes)}, wtd mean={mean_d:.3f})")
        ax.axhline(mean_d, color=color, linestyle="--", linewidth=1, alpha=0.8)

    if args.logx:
        ax.set_xscale("log")
    ax.set_xlabel("Community size (nodes)")
    ax.set_ylabel("Edge density")
    ax.set_ylim(-0.02, 1.02)
    if len(runs) == 1:
        ax.set_title(f"{runs[0][0]}: communities by size and density")
    else:
        ax.set_title(f"Community size vs. edge density ({len(runs)} runs)")
    ax.grid(alpha=0.3)

    leg = ax.legend()
    # Scatter points are semi-transparent; make the legend markers solid.
    handles = getattr(leg, "legend_handles", None) or getattr(leg, "legendHandles", [])
    for h in handles:
        h.set_alpha(1)

    fig.tight_layout()
    fig.savefig(args.out, dpi=150)
    print(f"Saved plot to {args.out}")


if __name__ == "__main__":
    main()
