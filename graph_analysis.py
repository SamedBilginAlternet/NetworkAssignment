"""
Edge Integrity (Ayrıt Bütünlük) ve Edge Rupture Degree (Ayrıt Parçalanma Derecesi)
Yöntem  : Brute Force (Kaba Kuvvet)
Graflar : P_10, C_10, S_10, W_10, K_10
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from itertools import combinations
import time

# ══════════════════════════════════════════════════════════════
# YARDIMCI
# ══════════════════════════════════════════════════════════════

def component_info(G, removed_edges):
    """
    G'den removed_edges kaldırıldıktan sonra:
    Döndürür → (ω: bileşen sayısı, m: en büyük bileşenin tepe sayısı)
    """
    H = G.copy()
    H.remove_edges_from(removed_edges)
    comps = list(nx.connected_components(H))
    if not comps:
        return 0, 0
    sizes = [len(c) for c in comps]
    return len(comps), max(sizes)


# ══════════════════════════════════════════════════════════════
# EDGE INTEGRITY  —  I'(G) = min_{F ⊆ E(G)} { |F| + m(G−F) }
# ══════════════════════════════════════════════════════════════

def edge_integrity(G):
    edges   = list(G.edges())
    E       = len(edges)
    n       = G.number_of_nodes()

    # F = ∅ → G bağlı, m = n, değer = n
    min_val = n
    best_F  = []

    for k in range(1, E + 1):
        if k >= min_val:
            break          # |F| zaten mevcut min'e ulaştı; iyileşme imkânsız

        for F in combinations(edges, k):
            _, m = component_info(G, list(F))
            val  = k + m
            if val < min_val:
                min_val = val
                best_F  = list(F)

    return min_val, best_F


# ══════════════════════════════════════════════════════════════
# EDGE RUPTURE DEGREE
# r'(G) = max_{F ⊆ E(G), ω(G−F)>1} { ω(G−F) − |F| − m(G−F) }
# ══════════════════════════════════════════════════════════════

def edge_rupture_degree(G, time_limit=180):
    edges   = list(G.edges())
    E       = len(edges)
    n       = G.number_of_nodes()
    kappa   = nx.edge_connectivity(G)   # Graf bağlantısızlaştırmak için min ayrıt sayısı

    max_val  = float('-inf')
    best_F   = None
    timeout  = False
    start    = time.time()

    for k in range(kappa, E + 1):
        if time.time() - start > time_limit:
            timeout = True
            break

        # Üst sınır budaması: ω ≤ n, m ≥ 1  →  değer ≤ n − k − 1
        if max_val != float('-inf') and (n - k - 1) < max_val:
            break

        for F in combinations(edges, k):
            if time.time() - start > time_limit:
                timeout = True
                break

            omega, m = component_info(G, list(F))
            if omega > 1:                      # Graf bağlantısız olmalı
                val = omega - k - m
                if val > max_val:
                    max_val = val
                    best_F  = list(F)

        if timeout:
            break

    return max_val, best_F, timeout


# ══════════════════════════════════════════════════════════════
# GRAF TANIMLARI  (10 tepeli)
# ══════════════════════════════════════════════════════════════

def create_graphs():
    return {
        "P_10": ("Yol Grafi",      nx.path_graph(10)),
        "C_10": ("Cevre Grafi",    nx.cycle_graph(10)),
        "S_10": ("Yildiz Grafi",   nx.star_graph(9)),       # 1 merkez + 9 yaprak
        "W_10": ("Tekerlek Grafi", nx.wheel_graph(10)),     # 1 merkez + 9 dis tepe
        "K_10": ("Tam Graf",       nx.complete_graph(10)),
    }


# ══════════════════════════════════════════════════════════════
# GÖRSELLEŞTIRME
# ══════════════════════════════════════════════════════════════

def visualize_graphs(graphs):
    fig, axes = plt.subplots(1, 5, figsize=(22, 5))
    fig.suptitle("10 Tepeli Graflar", fontsize=14, fontweight='bold')

    layout_fn = {
        "P_10": lambda G: nx.spring_layout(G, seed=42),
        "C_10": nx.circular_layout,
        "S_10": nx.spring_layout,
        "W_10": nx.shell_layout,
        "K_10": nx.circular_layout,
    }

    for ax, (key, (label, G)) in zip(axes, graphs.items()):
        pos = layout_fn[key](G)
        nx.draw(G, pos, ax=ax,
                with_labels=True,
                node_color='#AED6F1',
                node_size=450,
                font_size=8,
                font_weight='bold',
                edge_color='#5D6D7E',
                width=1.5)
        ax.set_title(f"{key}  —  {label}\n"
                     f"n={G.number_of_nodes()},  e={G.number_of_edges()}",
                     fontsize=9)

    plt.tight_layout()
    plt.savefig("graflar.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("  Graflar 'graflar.png' olarak kaydedildi.\n")


# ══════════════════════════════════════════════════════════════
# SONUÇLARI GÖRSELLEŞTIR
# ══════════════════════════════════════════════════════════════

def visualize_results(results):
    keys   = list(results.keys())
    ei_vals = [results[k]["I'"]  for k in keys]
    er_vals = [results[k]["r'"]  for k in keys]

    x = range(len(keys))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    fig.suptitle("Edge Integrity ve Edge Rupture Degree Karsilastirmasi",
                 fontsize=13, fontweight='bold')

    bars1 = ax1.bar(x, ei_vals, color='#2E86C1', edgecolor='black', width=0.5)
    ax1.set_title("Edge Integrity  I'(G)", fontsize=11)
    ax1.set_xticks(x); ax1.set_xticklabels(keys, fontsize=10)
    ax1.set_ylabel("Deger"); ax1.set_ylim(0, max(ei_vals) + 2)
    for bar, val in zip(bars1, ei_vals):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                 str(val), ha='center', fontweight='bold')

    colors2 = ['#E74C3C' if v >= 0 else '#27AE60' for v in er_vals]
    bars2 = ax2.bar(x, er_vals, color=colors2, edgecolor='black', width=0.5)
    ax2.set_title("Edge Rupture Degree  r'(G)", fontsize=11)
    ax2.set_xticks(x); ax2.set_xticklabels(keys, fontsize=10)
    ax2.set_ylabel("Deger")
    ax2.axhline(0, color='black', linewidth=0.8, linestyle='--')
    for bar, val in zip(bars2, er_vals):
        offset = 0.2 if val >= 0 else -0.8
        ax2.text(bar.get_x() + bar.get_width()/2, val + offset,
                 str(val), ha='center', fontweight='bold', color='white'
                 if abs(val) > 3 else 'black')

    plt.tight_layout()
    plt.savefig("sonuclar.png", dpi=150, bbox_inches='tight')
    plt.show()
    print("  Sonuclar 'sonuclar.png' olarak kaydedildi.\n")


# ══════════════════════════════════════════════════════════════
# ANA PROGRAM
# ══════════════════════════════════════════════════════════════

def main():
    graphs = create_graphs()

    print("=" * 65)
    print("  EDGE INTEGRITY ve EDGE RUPTURE DEGREE  —  BRUTE FORCE")
    print("=" * 65)

    visualize_graphs(graphs)

    results = {}

    for key, (label, G) in graphs.items():
        n = G.number_of_nodes()
        e = G.number_of_edges()

        print(f"\n{'─'*65}")
        print(f"  {key}  ({label})")
        print(f"  Tepe: {n}  |  Ayrit: {e}  |  Alt kume sayisi: 2^{e} = {2**e:,}")
        print(f"{'─'*65}")

        # ── Edge Integrity ──────────────────────────────────────
        t0 = time.time()
        ei_val, ei_F = edge_integrity(G)
        ei_time = time.time() - t0

        print(f"\n  [Edge Integrity]")
        print(f"  I'({key})  = {ei_val}")
        print(f"  Optimal F = {ei_F}")
        print(f"  Sure      : {ei_time:.3f}s")

        # ── Edge Rupture Degree ─────────────────────────────────
        t0 = time.time()
        erd_val, erd_F, timeout = edge_rupture_degree(G, time_limit=180)
        erd_time = time.time() - t0

        print(f"\n  [Edge Rupture Degree]")
        if timeout:
            print(f"  r'({key}) = {erd_val}  *** ZAMAN LIMITI ASILDI (kismi sonuc) ***")
        else:
            print(f"  r'({key}) = {erd_val}")
        print(f"  Optimal F = {erd_F}")
        print(f"  Sure      : {erd_time:.3f}s")

        results[key] = {
            "label"   : label,
            "n"       : n,
            "e"       : e,
            "I'"      : ei_val,
            "I'_F"    : ei_F,
            "r'"      : erd_val,
            "r'_F"    : erd_F,
            "timeout" : timeout,
        }

    # ── Özet Tablo ──────────────────────────────────────────────
    print(f"\n{'='*65}")
    print(f"  OZET TABLO")
    print(f"{'='*65}")
    print(f"  {'Graf':<26} {'n':>4} {'e':>5} {'I(G)':>8} {'r(G)':>8}")
    print(f"  {'─'*55}")
    for key, r in results.items():
        flag = " (*)" if r["timeout"] else ""
        print(f"  {key+' — '+r['label']:<26} {r['n']:>4} {r['e']:>5} "
              f"{r['I'']:>8} {str(r['r'''])+flag:>8}")

    print(f"\n  (*) Zaman limiti nedeniyle kismi sonuc")
    print(f"{'='*65}\n")

    visualize_results(results)


if __name__ == "__main__":
    main()
