import matplotlib.pyplot as plt
import math
import random

random.seed(42) # Để kết quả giống nhau mỗi lần chạy
num_customers = int(input("Nhập số lượng khách hàng: "))
locations = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(num_customers + 1)]

for i, loc in enumerate(locations):
    if i == 0:
        print(f"Kho (Depot): {loc}")
    else:
        print(f"Khách hàng {i}: {loc}")


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def solve_vrp_nearest_neighbor(locs):
    unvisited = list(range(1, len(locs)))
    route = [0]
    current = 0
    
    while unvisited:
        next_node = min(unvisited, key=lambda node: distance(locs[current], locs[node]))
        route.append(next_node)
        unvisited.remove(next_node)
        current = next_node
        
    route.append(0) # Quay về kho
    return route

# 3. Vẽ lộ trình bằng Matplotlib
def plot_route(locs, route):
    plt.figure(figsize=(10, 7))
    
    # Vẽ các điểm khách hàng
    x = [l[0] for l in locs]
    y = [l[1] for l in locs]
    plt.scatter(x[1:], y[1:], c='blue', label='Khách hàng')
    plt.scatter(x[0], y[0], c='red', marker='s', s=100, label='Kho (Depot)')
    
    # Vẽ các mũi tên lộ trình
    for i in range(len(route) - 1):
        start_node = route[i]
        end_node = route[i+1]
        plt.annotate("",
                     xy=locs[end_node], xycoords='data',
                     xytext=locs[start_node], textcoords='data',
                     arrowprops=dict(arrowstyle="->", connectionstyle="arc3", color="green", lw=1.5))
        
    # Đánh số thứ tự các điểm
    for i, txt in enumerate(range(len(locs))):
        plt.annotate(txt, (x[i]+1, y[i]+1))

    plt.title("Minh họa lộ trình VRP (Heuristic: Nearest Neighbor)")
    plt.legend()
    plt.grid(True)
    plt.show()

# Thực thi
best_route = solve_vrp_nearest_neighbor(locations)
print(f"Lộ trình: {best_route}")
plot_route(locations, best_route)