import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def manhattan_distance(p1, p2):
    """Depo içi dik açılı koridor hareketleri için Manhattan mesafesi."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def solve_tsp_nearest_neighbor(depot, pick_points):
    """En Yakın Komşu (Nearest Neighbor) sezgiseli ile sipariş toplama sırası bulma."""
    unvisited = pick_points.copy()
    current = depot
    route = [current]
    total_dist = 0
    
    while unvisited:
        nearest = min(unvisited, key=lambda p: manhattan_distance(current, p))
        dist = manhattan_distance(current, nearest)
        total_dist += dist
        current = nearest
        route.append(current)
        unvisited.remove(nearest)
        
    # Başlangıç noktasına (Depo / Paketleme Masası) geri dönüş
    total_dist += manhattan_distance(current, depot)
    route.append(depot)
    
    return route, total_dist

def plot_warehouse_route(depot, pick_points, route, total_dist):
    """Depo yerleşimi ve optimize edilmiş rotayı görselleştirir."""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    # Depo raflarını çiz (Gri bloklar)
    shelf_blocks = [(2, 1, 1.2, 7), (5, 1, 1.2, 7), (8, 1, 1.2, 7)]
    for x, y, w, h in shelf_blocks:
        rect = patches.Rectangle((x, y), w, h, linewidth=1, edgecolor='#475569', 
                                 facecolor='#cbd5e1', alpha=0.6, label='Raf Blokları' if x == 2 else "")
        ax.add_patch(rect)
    
    # Rotayı çiz (Oklar ve kesikli çizgiler)
    xs, ys = zip(*route)
    ax.plot(xs, ys, color='#ef4444', linestyle='--', linewidth=2, zorder=2, label='Toplama Rotası')
    
    # Rota yönü için oklar
    for i in range(len(route) - 1):
        x1, y1 = route[i]
        x2, y2 = route[i + 1]
        ax.annotate('', xy=((x1 + x2)/2, (y1 + y2)/2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color='#b91c1c', lw=1.5), zorder=3)
    
    # Toplama noktalarını işaretle
    pxs, pys = zip(*pick_points)
    ax.scatter(pxs, pys, color='#2563eb', s=120, zorder=4, label='Sipariş Kalemleri')
    for idx, (x, y) in enumerate(pick_points):
        ax.text(x + 0.15, y + 0.15, f"P{idx+1}", fontweight='bold', color='#1e3a8a')

    # Depo (Başlangıç/Bitiş) noktası
    ax.scatter(depot[0], depot[1], color='#16a34a', s=180, marker='s', zorder=5, label='Depo / Çıkış (0,0)')
    ax.text(depot[0] - 0.2, depot[1] - 0.6, "BAŞLANGIÇ", fontweight='bold', color='#166534')

    ax.set_title(f"Optimize Edilmiş Depo Sipariş Toplama Rotası (Toplam Mesafe: {total_dist} m)", 
                 fontsize=13, fontweight='bold')
    ax.set_xlabel("Depo Genişliği (X Ekseni - Metre)", fontsize=11)
    ax.set_ylabel("Depo Derinliği (Y Ekseni - Metre)", fontsize=11)
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 10)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc='upper right')
    
    plt.tight_layout()
    plt.savefig("warehouse_route.png", dpi=300)
    plt.show()

if __name__ == "__main__":
    depot_location = (0, 0)
    # Örnek sipariş listesindeki lokasyonlar (x, y)
    order_picks = [(2.5, 2), (3.5, 7), (5.5, 4), (6.5, 8), (8.5, 3), (9.5, 6)]
    
    best_route, distance = solve_tsp_nearest_neighbor(depot_location, order_picks)
    print("Optimize Edilmiş Rota Sırası:", best_route)
    print(f"Toplam Toplama Mesafesi: {distance} birim/metre")
    plot_warehouse_route(depot_location, order_picks, best_route, distance)
