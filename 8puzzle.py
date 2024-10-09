import tkinter as tk
from tkinter import messagebox
from collections import deque
import heapq

class PuzzleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("8-Puzzle Solver")
        self.root.geometry("700x600")

        self.bg_color = "#deb887"
        self.tile_color = "#f4a460"
        self.text_color = "#8b4513"

        self.root.config(bg=self.bg_color)

        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)
            self.root.grid_rowconfigure(i, weight=1)

        self.start_state = [
            [2, 8, 3], 
            [1, 6, 4], 
            [7, 0, 5]
        ]
        
        self.goal_state = [
            [1, 2, 3], 
            [8, 0, 4], 
            [7, 6, 5]
        ]

        self.tiles = [[None for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.tiles[i][j] = tk.Label(self.root, text=str(self.start_state[i][j]) if self.start_state[i][j] != 0 else ' ',
                                             font=('Arial', 36), width=4, height=2, bg=self.tile_color, fg=self.text_color,
                                             borderwidth=2, relief="solid")
                self.tiles[i][j].grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
                
        self.bfs_button = tk.Button(self.root, text="Solve\n with BFS", command=self.solve_bfs, bg=self.tile_color, fg=self.text_color, font=('Arial', 12), borderwidth=2, relief="solid")
        self.bfs_button.grid(row=0, column=3, rowspan=1, sticky="nsew", padx=5, pady=5)
        
        self.dfs_button = tk.Button(self.root, text="Solve\n with DFS", command=self.solve_dfs, bg=self.tile_color, fg=self.text_color, font=('Arial', 12), borderwidth=2, relief="solid")
        self.dfs_button.grid(row=1, column=3, rowspan=1, sticky="nsew", padx=5, pady=5)
        
        self.ucs_button = tk.Button(self.root, text="Solve\n with UCS", command=self.solve_ucs, bg=self.tile_color, fg=self.text_color, font=('Arial', 12), borderwidth=2, relief="solid")
        self.ucs_button.grid(row=2, column=3, rowspan=1, sticky="nsew", padx=5, pady=5)
        
        self.reset_button = tk.Button(self.root, text="Reset", command=self.reset, bg=self.tile_color, fg=self.text_color, font=('Arial', 12), borderwidth=2, relief="solid")
        self.reset_button.grid(row=3, column=3, rowspan=1, sticky="nsew", padx=5, pady=5)
        
        self.step_label = tk.Label(self.root, text="Steps: 0\nCost: 0\nMoves: ", bg=self.tile_color, fg=self.text_color, font=('Arial', 17), borderwidth=2, relief="solid")
        self.step_label.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)
        
        self.steps = []
        self.step_count = 0
        self.solution_process = None
        self.current_cost = 0

        self.costs = {
            'UP': 2,
            'DOWN': 2,
            'LEFT': 1,
            'RIGHT': 1
        }

        self.MOVES = {
            'UP': (-1, 0),
            'DOWN': (1, 0),
            'LEFT': (0, -1),
            'RIGHT': (0, 1)
        }

    def update_tiles(self, state):
        for i in range(3):
            for j in range(3):
                self.tiles[i][j].config(text=str(state[i][j]) if state[i][j] != 0 else '')

    def is_goal(self, state):
        return state == self.goal_state

    def find_blank(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j

    def get_neighbors(self, state):
        neighbors = []
        x, y = self.find_blank(state)

        for direction, (dx, dy) in self.MOVES.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < 3 and 0 <= ny < 3:
                new_state = [row[:] for row in state]
                new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
                neighbors.append((direction, new_state))

        return neighbors

    def bfs(self, start):
        queue = deque([(start, [], 0)])
        visited = set()
        visited.add(tuple(map(tuple, start)))

        while queue:
            current, path, cost = queue.popleft()
            if self.is_goal(current):
                return path + [(None, current)], cost

            for direction, neighbor in self.get_neighbors(current):
                neighbor_tuple = tuple(map(tuple, neighbor))
                new_cost = cost + self.costs[direction]
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    queue.append((neighbor, path + [(direction, neighbor)], new_cost))
                    
        return None, 0

    def dfs(self, start):
        stack = [(start, [], 0)]
        visited = set()
        visited.add(tuple(map(tuple, start)))

        while stack:
            current, path, cost = stack.pop()
            if self.is_goal(current):
                return path + [(None, current)], cost

            for direction, neighbor in self.get_neighbors(current):
                neighbor_tuple = tuple(map(tuple, neighbor))
                new_cost = cost + self.costs[direction]
                if neighbor_tuple not in visited:
                    visited.add(neighbor_tuple)
                    stack.append((neighbor, path + [(direction, neighbor)], new_cost))
                    
        return None, 0

    def uniform_cost_search(self, start):
        priority_queue = [(0, start, [])]
        costs_for_states = {tuple(map(tuple, start)): 0}

        while priority_queue:
            total_cost, current_state, path = heapq.heappop(priority_queue)

            if self.is_goal(current_state):
                return path + [(None, current_state)], total_cost

            for direction, neighbor in self.get_neighbors(current_state):
                state_tuple = tuple(map(tuple, neighbor))
                move_cost = self.costs[direction]
                new_cost = total_cost + move_cost

                if state_tuple not in costs_for_states or new_cost < costs_for_states[state_tuple]:
                    costs_for_states[state_tuple] = new_cost
                    heapq.heappush(priority_queue, (new_cost, neighbor, path + [(direction, neighbor)]))

        return None, 0

    def show_solution(self, steps):
        if steps:
            current_move = steps.pop(0)
            self.update_tiles(current_move[1])
            self.step_count += 1
            
            if current_move[0] is not None:
                current_cost = self.costs[current_move[0]]
                self.current_cost += current_cost

            self.step_label.config(text=f"Steps: {self.step_count}\nCost: {self.current_cost}\nMoves: {current_move[0]}")
            
            self.solution_process = self.root.after(500, lambda: self.show_solution(steps))
        else:
            messagebox.showinfo("Success", "Puzzle Solved!")

    def solve_bfs(self):
        result, total_cost = self.bfs(self.start_state)
        if result:
            self.steps = result
            self.step_count = 0
            self.current_cost = 0
            self.show_solution(self.steps)
        else:
            messagebox.showinfo("Failure", "No solution found with BFS.")

    def solve_dfs(self):
        result, total_cost = self.dfs(self.start_state)
        if result:
            self.steps = result
            self.step_count = 0
            self.current_cost = 0
            self.show_solution(self.steps)
        else:
            messagebox.showinfo("Failure", "No solution found with DFS.")

    def solve_ucs(self):
        result, total_cost = self.uniform_cost_search(self.start_state)
        if result:
            self.steps = result
            self.step_count = 0
            self.current_cost = 0
            self.show_solution(self.steps)
        else:
            messagebox.showinfo("Failure", "No solution found with UCS.")

    def reset(self):
        self.update_tiles(self.start_state)
        self.step_count = 0
        self.current_cost = 0
        self.step_label.config(text="Steps: 0\nCost: 0\nMoves: ")
        if self.solution_process:
            self.root.after_cancel(self.solution_process)
            self.solution_process = None

if __name__ == "__main__":
    root = tk.Tk()
    app = PuzzleApp(root)
    root.mainloop()