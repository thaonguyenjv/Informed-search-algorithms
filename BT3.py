from simpleai.search import SearchProblem, hill_climbing, simulated_annealing
import random
import time

N = 8  # số quân hậu


# Định nghĩa bài toán 8 quân hậu
class EightQueensProblem(SearchProblem):
    def __init__(self, initial_state):
        super(EightQueensProblem, self).__init__(initial_state)

    def actions(self, state):
        actions = []
        for col in range(N):
            for row in range(N):
                if state[col] != row:
                    actions.append((col, row))
        return actions

    def result(self, state, action):
        col, row = action
        new_state = list(state)
        new_state[col] = row
        return tuple(new_state)

    def value(self, state):
        return -self.conflicts(state)

    def conflicts(self, state):
        conflicts = 0
        for i in range(N):
            for j in range(i + 1, N):
                if state[i] == state[j]:
                    conflicts += 1
                if abs(state[i] - state[j]) == abs(i - j):
                    conflicts += 1
        return conflicts


def print_board(state):
    for row in range(N):
        line = ""
        for col in range(N):
            if state[col] == row:
                line += " Q "
            else:
                line += " . "
        print(line)
    print()


def run_experiments(runs=10):
    results_hc = []
    results_sa = []
    success_hc, success_sa = 0, 0

    print("=== KẾT QUẢ HILL CLIMBING ===")
    for i in range(runs):
        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))
        problem = EightQueensProblem(initial_state)

        start = time.time()
        hc_result = hill_climbing(problem)
        elapsed = time.time() - start
        conflicts = problem.conflicts(hc_result.state)
        results_hc.append((conflicts, hc_result.state, elapsed))

        if conflicts == 0:
            success_hc += 1

        print(f"Run {i+1}: {conflicts} conflicts, State: {hc_result.state}, Time: {round(elapsed,6)}s")

    print("\n=== KẾT QUẢ SIMULATED ANNEALING ===")
    for i in range(runs):
        initial_state = tuple(random.randint(0, N - 1) for _ in range(N))
        problem = EightQueensProblem(initial_state)

        start = time.time()
        sa_result = simulated_annealing(problem)
        elapsed = time.time() - start
        conflicts = problem.conflicts(sa_result.state)
        results_sa.append((conflicts, sa_result.state, elapsed))

        if conflicts == 0:
            success_sa += 1

        print(f"Run {i+1}: {conflicts} conflicts, State: {sa_result.state}, Time: {round(elapsed,6)}s")

    # Tìm nghiệm tốt nhất
    best_hc = min(results_hc, key=lambda x: x[0])
    best_sa = min(results_sa, key=lambda x: x[0])

    print("\n======================================================")
    print("SO SÁNH HIỆU NĂNG")
    print(f"Hill Climbing: thành công {success_hc}/{runs} lần")
    print(f"Simulated Annealing: thành công {success_sa}/{runs} lần")

    print("\nBest Hill Climbing:")
    print("Conflicts:", best_hc[0], ", State:", best_hc[1], ", Time:", round(best_hc[2], 6), "s")

    print("\nBest Simulated Annealing:")
    print("Conflicts:", best_sa[0], ", State:", best_sa[1], ", Time:", round(best_sa[2], 6), "s")

    # Ví dụ minh họa chi tiết
    print("\n======================================================")
    print("VÍ DỤ MINH HỌA CHI TIẾT")
    initial_state = tuple(random.randint(0, N - 1) for _ in range(N))
    problem = EightQueensProblem(initial_state)

    print("Trạng thái ban đầu:", initial_state)
    print("Số conflicts ban đầu:", problem.conflicts(initial_state))
    print("\nBàn cờ ban đầu:")
    print_board(initial_state)

    # Hill Climbing
    start = time.time()
    hc_result = hill_climbing(problem)
    elapsed_hc = time.time() - start
    print("Giải bằng HILL CLIMBING:")
    print("Kết quả:", problem.conflicts(hc_result.state), "conflicts, thời gian:", round(elapsed_hc, 6), "s")
    print_board(hc_result.state)

    # Simulated Annealing
    start = time.time()
    sa_result = simulated_annealing(problem)
    elapsed_sa = time.time() - start
    print("Giải bằng SIMULATED ANNEALING:")
    print("Kết quả:", problem.conflicts(sa_result.state), "conflicts, thời gian:", round(elapsed_sa, 6), "s")
    print_board(sa_result.state)


if __name__ == "__main__":
    run_experiments(10)
