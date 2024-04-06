import multiprocessing

def calculate_sum(start, end, result_queue):
    total = sum(range(start, end + 1))
    result_queue.put(total)

if __name__ == "__main__":
    n = int(input("Nhập số nguyên dương n: "))

    # Tạo một hàng đợi kết quả để thu thập kết quả từ các process con
    result_queue = multiprocessing.Queue()

    # Số phần tử trong mỗi phạm vi con
    chunk_size = n // multiprocessing.cpu_count()

    # Danh sách để lưu trữ các process
    processes = []

    # Chia nhỏ phạm vi từ 1 đến n thành các phạm vi nhỏ hơn và tạo một process cho mỗi phạm vi
    for i in range(0, n, chunk_size):
        start = i + 1
        end = min(i + chunk_size, n)
        process = multiprocessing.Process(target=calculate_sum, args=(start, end, result_queue))
        processes.append(process)
        process.start()

    # Chờ cho tất cả các process kết thúc
    for process in processes:
        process.join()

    # Thu thập kết quả từ hàng đợi và tính tổng cuối cùng
    total_sum = 0
    while not result_queue.empty():
        total_sum += result_queue.get()

    print("Tổng của các số từ 1 đến", n, "là:", total_sum)
