import matplotlib.pyplot as plt
import numpy as np
import math
import random
import time

# ----------------------------
# 1. Tạo dữ liệu
# ----------------------------

random.seed(42)

num_customers = int(input("Nhập số lượng khách hàng: "))
vehicle_capacity = int(input("Nhập tải trọng tối đa của xe: "))
vehicle_speed = float(input("Nhập vận tốc xe (km/h): "))

locations = [(random.randint(0,100), random.randint(0,100)) for _ in range(num_customers+1)]

demands = [0] + [random.randint(1,10) for _ in range(num_customers)]


# ----------------------------
# 2. Hàm tính khoảng cách
# ----------------------------

def distance(p1,p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)


# ----------------------------
# 3. Thuật toán Nearest Neighbor
# ----------------------------

def solve_vrp(locs,demands,capacity,speed):

    start_time = time.time()

    unvisited = list(range(1,len(locs)))
    route = [0]

    current = 0
    load = 0

    total_distance = 0
    total_time = 0

    vehicle_count = 1
    overload = False

    while unvisited:

        next_node = min(unvisited,
        key=lambda node: distance(locs[current],locs[node]))

        # kiểm tra tải trọng
        if load + demands[next_node] > capacity:

            d = distance(locs[current],locs[0])

            total_distance += d
            total_time += d/speed

            route.append(0)

            current = 0
            load = 0

            vehicle_count += 1

            continue

        d = distance(locs[current],locs[next_node])

        total_distance += d
        total_time += d/speed

        route.append(next_node)

        load += demands[next_node]

        if load > capacity:
            overload = True

        unvisited.remove(next_node)

        current = next_node


    d = distance(locs[current],locs[0])

    total_distance += d
    total_time += d/speed

    route.append(0)

    end_time = time.time()

    execution_time = end_time - start_time

    return route,total_distance,total_time,vehicle_count,execution_time,overload


# ----------------------------
# 4. Vẽ lộ trình
# ----------------------------

def plot_route(locs,route):

    plt.figure(figsize=(10,7))

    x=[l[0] for l in locs]
    y=[l[1] for l in locs]

    plt.scatter(x[1:],y[1:],c='blue',label="Khách hàng")
    plt.scatter(x[0],y[0],c='red',s=120,label="Kho")

    for i in range(len(route)-1):

        s=route[i]
        e=route[i+1]

        plt.annotate("",
        xy=locs[e],
        xytext=locs[s],
        arrowprops=dict(arrowstyle="->",color="green"))

    for i in range(len(locs)):
        plt.text(x[i]+1,y[i]+1,str(i))

    plt.title("VRP - Nearest Neighbor")
    plt.legend()
    plt.grid(True)
    plt.show()


# ----------------------------
# 5. Chạy chương trình
# ----------------------------

route,total_distance,total_time,vehicle_count,execution_time,overload = solve_vrp(
    locations,
    demands,
    vehicle_capacity,
    vehicle_speed
)

print("\nNhu cầu mỗi khách:")
print(demands)

print("\nLộ trình xe:")
route_display = [f"{node}[{demands[node]}]" if node != 0 else "0" for node in route]
print(" -> ".join(route_display))

print("\n------ ĐÁNH GIÁ HIỆU SUẤT ------")

print("Tổng quãng đường:", round(total_distance,2),"km")

print("Tổng thời gian vận chuyển:", round(total_time,2),"giờ")

print("Số xe sử dụng:", vehicle_count)

# print("Thời gian thực thi thuật toán:", round(execution_time,6),"giây")

if overload:
    print("CẢNH BÁO: Có xe vượt tải!")
else:
    print("Tất cả xe đều tuân thủ tải trọng.")

plot_route(locations,route)