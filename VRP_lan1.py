import numpy as np
import matplotlib.pyplot as plt

# 1. Hàm khởi tạo dữ liệu
def generate_custom_data(num_customers):
    # Tọa độ kho (Depot) cố định tại vị trí trung tâm (50, 50)
    depot = np.array([50, 50])
    # Tạo tọa độ khách hàng ngẫu nhiên (x, y) từ 0 đến 100
    customers = np.random.randint(0, 100, size=(num_customers, 2))
    # Tạo nhu cầu hàng hóa ngẫu nhiên (từ 1 đến 10)
    demands = np.random.randint(1, 11, size=num_customers)
    return depot, customers, demands

# 2. Tính khoảng cách Euclide
def calculate_distance(p1, p2):
    return np.sqrt(np.sum((p1 - p2)**2))

# 3. Thuật toán Nearest Neighbor (Láng giềng gần nhất)
def nearest_neighbor_solver(depot, customers, demands, capacity):
    num_customers = len(customers)
    unvisited = list(range(num_customers))
    routes = []
    total_distance = 0
    
    while unvisited:
        current_route = []
        current_load = 0
        current_pos = depot
        
        while unvisited:
            nearest_idx = -1
            min_dist = float('inf')
            
            # Tìm khách hàng gần nhất có thể phục vụ (không quá tải trọng)
            for idx in unvisited:
                dist = calculate_distance(current_pos, customers[idx])
                if current_load + demands[idx] <= capacity:
                    if dist < min_dist:
                        min_dist = dist
                        nearest_idx = idx
            
            if nearest_idx == -1:
                break
            
            # Cập nhật thông số
            total_distance += min_dist
            current_route.append(nearest_idx)
            current_load += demands[nearest_idx]
            current_pos = customers[nearest_idx]
            unvisited.remove(nearest_idx)
            
        # Kết thúc một lộ trình: Quay về kho
        total_distance += calculate_distance(current_pos, depot)
        routes.append(current_route)
    
    return routes, total_distance

# 4. Vẽ biểu đồ kết quả với mũi tên cải tiến
def visualize_results(depot, customers, routes):
    plt.figure(figsize=(12, 8))
    
    # Vẽ kho (Depot)
    plt.scatter(depot[0], depot[1], c='red', marker='s', s=200, label='Kho (Depot)', zorder=5)
    
    # Vẽ các khách hàng
    plt.scatter(customers[:,0], customers[:,1], c='blue', s=100, alpha=0.6, zorder=3)
    for i, (x, y) in enumerate(customers):
        plt.text(x+1, y+1, f"{i}", fontsize=10, fontweight='bold', zorder=4)

    # Palette màu cho các xe
    colors = plt.cm.get_cmap('tab10', len(routes))
    
    for i, route in enumerate(routes):
        # Lấy tọa độ: Depot -> Danh sách khách -> Depot
        points = [depot] + [customers[idx] for idx in route] + [depot]
        
        # Vẽ line rỗng để tạo chú thích (Legend)
        plt.plot([], [], color=colors(i), linewidth=2, label=f'Xe {i+1} ({len(route)} khách)')
        
        for j in range(len(points) - 1):
            start = points[j]
            end = points[j+1]
            
            # Sử dụng annotate để vẽ mũi tên mượt mà
            plt.annotate("",
                         xy=end, xycoords='data',
                         xytext=start, textcoords='data',
                         arrowprops=dict(
                             arrowstyle="->", 
                             color=colors(i),
                             lw=2,
                             mutation_scale=20,
                             shrinkA=7, # Lùi điểm bắt đầu (không đè lên chấm)
                             shrinkB=7  # Lùi điểm kết thúc (mũi tên chỉ vào chấm)
                         ))
            
    plt.title("Mô phỏng lộ trình VRP - Thuật toán Nearest Neighbor", fontsize=15)
    plt.xlabel("Tọa độ X")
    plt.ylabel("Tọa độ Y")
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.show()

# --- CHƯƠNG TRÌNH CHÍNH ---
if __name__ == "__main__":
    print("="*40)
    print("   HỆ THỐNG TỐI ƯU LỘ TRÌNH VRP (NN)   ")
    print("="*40)
    
    try:
        n_cust = int(input("Nhập số lượng khách hàng : "))
        cap = int(input("Nhập tải trọng tối đa xe : "))
        
        if n_cust <= 0 or cap <= 0:
            print("Vui lòng nhập giá trị lớn hơn 0!")
        else:
            # 1. Khởi tạo
            depot_pos, cust_pos, cust_demands = generate_custom_data(n_cust)
            
            # 2. Giải thuật
            final_routes, total_dist = nearest_neighbor_solver(depot_pos, cust_pos, cust_demands, cap)
            
            # 3. Xuất lộ trình chi tiết
            print("\n" + "-"*15 + " CHI TIẾT LỘ TRÌNH " + "-"*15)
            for i, r in enumerate(final_routes):
                route_str = " -> ".join(map(str, r))
                print(f"Xe {i+1}: Depot -> {route_str} -> Depot")
            
            # 4. Đánh giá hiệu suất
            print("\n" + "="*15 + " ĐÁNH GIÁ HIỆU SUẤT " + "="*15)
            print(f"| {'Thông số':<25} | {'Giá trị':<15} |")
            print("-" * 47)
            print(f"| {'Tổng quãng đường':<25} | {total_dist:>10.2f} km |")
            print(f"| {'Số xe sử dụng':<25} | {len(final_routes):>10} xe |")
            print(f"| {'Quãng đường TB/xe':<25} | {total_dist/len(final_routes):>10.2f} km |")
            print("=" * 47)
            
            # 5. Trực quan hóa
            visualize_results(depot_pos, cust_pos, final_routes)
            
    except ValueError:
        print("Lỗi: Vui lòng chỉ nhập số nguyên hợp lệ!")