from simpleai.search import SearchProblem
import random

# Định nghĩa domain: mỗi vị trí là số từ 0-7 (hàng của quân hậu trên từng cột)
domain = list(range(8))

# Lớp Problem cho bài toán 8 quân hậu
class EightQueensProblem(SearchProblem):
    def __init__(self):
        # Khởi tạo trạng thái ban đầu ngẫu nhiên
        initial_state = random.sample(domain, 8)
        super().__init__(initial_state)
        self.initial_state = initial_state
    
    def actions(self, state):
        # Trả về danh sách các hành động (hoán đổi vị trí)
        actions = []
        for i in range(8):
            for j in range(i + 1, 8):
                actions.append((i, j))
        return actions
    
    def result(self, state, action):
        # Thực hiện hoán đổi hai vị trí
        i, j = action
        new_state = list(state)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        return new_state
    
    def value(self, state):
        # Hàm fitness: số cặp không xung đột (max 28)
        attacks = 0
        for i in range(8):
            for j in range(i + 1, 8):
                if abs(state[i] - state[j]) == j - i:  # Xung đột trên đường chéo
                    attacks += 1
        return 28 - attacks  # Fitness cao hơn khi ít xung đột

# Hàm tạo cá thể ngẫu nhiên
def create_individual():
    return random.sample(domain, 8)

# Hàm crossover: lai một điểm với sửa chữa hoán vị
def crossover(parent1, parent2):
    point = random.randint(1, 7)
    child1 = parent1[:point] + [x for x in parent2 if x not in parent1[:point]]
    child2 = parent2[:point] + [x for x in parent1 if x not in parent2[:point]]
    return child1, child2

# Hàm mutation: hoán đổi hai vị trí ngẫu nhiên
def mutate(individual):
    if random.random() < 0.1:  # Xác suất đột biến 10%
        i, j = random.sample(range(8), 2)
        individual[i], individual[j] = individual[j], individual[i]
    return individual

# Thuật toán GA thủ công với SimpleAI
def genetic_algorithm(population_size=100, max_generations=1000):
    # Khởi tạo dân số
    population = [create_individual() for _ in range(population_size)]
    
    for generation in range(max_generations):
        # Đánh giá fitness
        fitnesses = [EightQueensProblem().value(ind) for ind in population]
        if max(fitnesses) == 28:  # Tìm thấy giải pháp tối ưu
            best_idx = fitnesses.index(28)
            return population[best_idx], generation + 1
        
        # Reproduction: Chọn lọc roulette wheel
        total_fitness = sum(fitnesses)
        new_population = []
        for _ in range(population_size):
            pick = random.uniform(0, total_fitness)
            current = 0
            for i, fit in enumerate(fitnesses):
                current += fit
                if current > pick:
                    new_population.append(population[i])
                    break
            else:
                new_population.append(population[-1])  # Dự phòng nếu không chọn được
        
        # Đảm bảo đủ cá thể cho crossover
        while len(new_population) < population_size:
            new_population.append(create_individual())
        
        # Crossover: Tạo thế hệ mới
        next_generation = []
        while len(new_population) >= 2:
            if random.random() < 0.8:  # Xác suất crossover 80%
                p1 = new_population.pop()
                p2 = new_population.pop()
                child1, child2 = crossover(p1, p2)
                next_generation.extend([mutate(child1), mutate(child2)])
            else:
                next_generation.append(mutate(new_population.pop()))
        
        # Điền đầy nếu cần
        while len(next_generation) < population_size:
            if new_population:
                next_generation.append(mutate(new_population.pop()))
            else:
                next_generation.append(mutate(create_individual()))
        
        population = next_generation[:population_size]
    
    # Trả về cá thể tốt nhất nếu không tìm thấy giải pháp
    fitnesses = [EightQueensProblem().value(ind) for ind in population]
    best_idx = fitnesses.index(max(fitnesses))
    return population[best_idx], max_generations

# Chạy thuật toán
result, generations = genetic_algorithm()
print("Giải pháp:", result)
print("Fitness:", EightQueensProblem().value(result))
print("Số thế hệ:", generations)

# Minh họa bàn cờ
board = [["." for _ in range(8)] for _ in range(8)]
for col, row in enumerate(result):
    board[row][col] = "Q"
for row in board:
    print(" ".join(row))