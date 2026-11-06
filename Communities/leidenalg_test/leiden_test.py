import igraph as ig
import leidenalg as la
from collections import defaultdict
from infomap import Infomap
import sys

G = ig.Graph.Read_Edgelist(sys.argv[1], directed=False)

# 0 Leiden
# 1 Infomap
# 2 Walktrap NOTE: it uses some wacky function that I requires weird changes...
# 3 Spinglass
# 4 Fast greedy (CNM)
# 5 Markov stability NOTE: Also uses a weird function


option = 5

# ---------- scoring ----------
def report(G, labels, name):
    deg = G.degree()
    two_m = sum(deg)

    size = defaultdict(int)
    vol = defaultdict(int)
    internal = defaultdict(int)
    cut = defaultdict(int)

    for v, c in enumerate(labels):
        size[c] += 1
        vol[c] += deg[v]
    for u, v in G.get_edgelist():
        cu, cv = labels[u], labels[v]
        if cu == cv:
            internal[cu] += 1
        else:
            cut[cu] += 1
            cut[cv] += 1

    comms = sorted(size)
    cond, dens = [], []
    for c in comms:
        denom = min(vol[c], two_m - vol[c])
        cond.append(cut[c] / denom if denom > 0 else 0.0)
        n = size[c]
        dens.append(internal[c] / (n * (n - 1) / 2) if n > 1 else 0.0)

    Q = G.modularity(labels)  # Newman-Girvan modularity

    '''print(f"=== {name} ({len(comms)} communities) ===")
    print(f"  mean conductance        : {sum(cond)/len(cond):.4f}")
    print(f"  mean intra edge density : {sum(dens)/len(dens):.4f}")
    print(f"  Newman-Girvan Q         : {Q:.4f}\n")'''



match option:
    case  0:
        leiden = la.find_partition(G, la.ModularityVertexPartition, n_iterations=-1)
        leiden_labels = leiden.membership


        #report(G, leiden_labels, "Leiden (modularity)")

        for line in leiden:
            for node in line:
                print(node, end = " ")
            print()
        
        
    case 1:
        im = Infomap(seed=123, num_trials=20, silent=True)
        for u, v in G.get_edgelist():
            im.add_link(u, v)
        im.run()
        mods = im.get_modules()
        # vertices with no edges never reach Infomap, so give each its own label
        infomap_labels = [mods.get(n, -1 - n) for n in range(G.vcount())]

        #report(G, infomap_labels, "Infomap")

        communities = defaultdict(list)
        for node_id, module_id in im.get_modules().items():
            communities[module_id].append(node_id)

        for module_id, nodes in sorted(communities.items()):
            print(f"{' '.join(map(str, sorted(nodes)))}")
        
    case  2:
        dendro = G.community_walktrap(steps=4)   # returns a dendrogram
        clusters = dendro.as_clustering()        # cuts at max modularity
        for line in clusters:
            for node in line:
                print(node, end = " ")
            print()
 
    

    case 3:
        membership = [-1] * G.vcount()
        offset = 0
        for comp in G.connected_components():
            if len(comp) == 1:                      # isolated node: its own community
                membership[comp[0]] = offset
                offset += 1
                continue
            sub = G.induced_subgraph(comp)
                                        # Claude told me spins = limit num communities
                                        # I think its num iterations? Doesn't make sense either?
            cl = sub.community_spinglass(spins=999, gamma=1.0)
            for v, c in zip(comp, cl.membership):
                membership[v] = offset + c
            offset += max(cl.membership) + 1
            
        comms = defaultdict(list)
        for node, c in enumerate(membership):
            comms[c].append(node)

        for c in sorted(comms):
            print(f"{' '.join(map(str, comms[c]))}")


    case 4:
        H = G.copy()
        H.simplify()
        fg = H.community_fastgreedy().as_clustering()   # cuts dendrogram at max modularity

        for line in fg:
            for node in line:
                print(node, end=" ")
            print()

    case 5:
        import pygenstability as pgs

        A = G.get_adjacency_sparse()    # scipy sparse adjacency matrix
        results = pgs.run(
            A,
            constructor="linearized",   # Markov stability with linearized dynamics
            min_scale=-1.5,             # log10 of Markov time range to scan
            max_scale=0.5,
            n_scale=20,
            n_tries=10,                 # Louvain restarts per scale
        )

        # use the scale picked by PyGenStability's optimal scale selection,
        # falling back to the scale with best modularity if it's absent
        sel = results.get("selected_partitions")
        if sel:
            idx = sel[0]
        else:
            idx = max(range(len(results["scales"])),
                      key=lambda i: G.modularity(list(results["community_id"][i])))

        labels = results["community_id"][idx]
        print(f"# scale index {idx}, Markov time {results['scales'][idx]:.3g}, "
              f"{results['number_of_communities'][idx]} communities", file=sys.stderr)

        groups = defaultdict(list)
        for node, c in enumerate(labels):
            groups[c].append(node)

        for c in sorted(groups):
            print(*groups[c])



