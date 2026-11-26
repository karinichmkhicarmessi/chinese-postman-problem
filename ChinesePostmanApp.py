import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from AlgorithmSolver import AlgorithmSolver
from GraphManager import GraphManager
from Visualizer import Visualizer


class ChinesePostmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Решение задачи китайского почтальона")
        self.root.state('zoomed')
        self.root.resizable(False, False)
        self.manager = GraphManager()
        self.res = AlgorithmSolver()
        self.visual = Visualizer()
        self.solution = None
        self.create_widgets()

    def create_widgets(self):
        frame1 = ttk.LabelFrame(self.root, text="Данные графа", padding=10)
        frame1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame1, text="Введите вершины через запятую:").grid(row=0, column=0, sticky="w")
        self.vertices = ttk.Entry(frame1, width=50)
        self.vertices.grid(row=0, column=2, padx=5, pady=5)
        self.vertices.insert(0, "1,2,3,4,5,6,7,8,9,10,11")

        ttk.Label(frame1, text="Введите ребра через запятую (u-v-вес):").grid(row=1, column=0, sticky="w")
        self.edges = ttk.Entry(frame1, width=50)
        self.edges.grid(row=1, column=2, padx=5, pady=5)
        self.edges.insert(0, "1-2-8,1-6-6,1-7-3,2-3-3,2-5-5,3-4-4,4-11-6,4-5-4,5-10-8,5-6-3,6-9-7,6-7-4,7-9-6,7-8-2,8-9-3,10-9-2,10-11-7")

        buttons = ttk.Frame(frame1)
        buttons.grid(row=2, column=1, columnspan=3, pady=5)

        ttk.Button(buttons, text="Построить граф", command=self.build_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons, text="Загрузить из файла", command=self.load_from_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons, text="Сохранить в файл", command=self.save_to_file).pack(side=tk.LEFT, padx=5)

        algorithms = ttk.Frame(frame1)
        algorithms.grid(row=3, column=1, columnspan=3, pady=5)
        ttk.Label(algorithms, text="Выберите алгоритм:").pack(side=tk.LEFT)
        self.s = tk.StringVar(value="Гуяна")
        ttk.Radiobutton(algorithms, text="Гуяна", variable=self.s, value="Гуяна").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(algorithms, text="Эдмондса", variable=self.s, value="Эдмондса").pack(side=tk.LEFT, padx=5)

        ttk.Button(frame1, text="Решить задачу", command=self.solve_problem).grid(row=4, column=1, columnspan=3,
                                                                                       pady=5)
        frame2 = ttk.LabelFrame(self.root, text="Результаты", padding=10)
        frame2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        ttk.Label(frame2, text="Эйлеров цикл:").grid(row=0, column=1, sticky="w")
        self.result = tk.Text(frame2, width=60, height=10, wrap=tk.WORD, font=("Calibri", 12))
        self.result.grid(row=1, column=1, padx=5, pady=5)

        scrollbar = ttk.Scrollbar(frame2, orient="vertical", command=self.result.yview)
        scrollbar.grid(row=1, column=2, sticky="ns")
        self.result.configure(yscrollcommand=scrollbar.set)

        self.frame3 = ttk.Frame(self.root)
        self.frame3.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def build_graph(self):
        try:
            if self.manager.build_graph(self.vertices, self.edges):
                self.visual.visualize_graph(self.frame3, self.manager.graph, "Исходный граф")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def load_from_file(self):
        try:
            if self.manager.load_from_file(self.vertices, self.edges):
                messagebox.showinfo("Успех", "Граф успешно загружен!")
            self.build_graph()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def save_to_file(self):
        try:
            if self.manager.save_to_file(self.vertices, self.edges, self.solution):
                messagebox.showinfo("Успех", "Результаты успешно сохранены!")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def solve_problem(self):
        if not self.manager.graph.nodes():
            messagebox.showerror("Ошибка", "Сначала постройте граф!")
            return
        try:
            algorithm = self.s.get()
            if algorithm == "Гуяна":
                self.solution = self.res.guan_algorithm(self.manager.graph)
            else:
                self.solution = self.res.edmonds_algorithm(self.manager.graph)

            text = [
                f"Вы выбрали алгоритм {algorithm}",
                "Эйлеров цикл:",
                ", ".join(f"{u}\u2011{v}"
                for u, v in self.solution['result']),
                f"\nОбщий вес пути: {self.solution['TW']}"
            ]

            self.result.delete(1.0, tk.END)
            self.result.insert(tk.END, "\n".join(text))
            self.visual.visualize_solution(
                self.frame3, self.manager.graph, self.solution, algorithm
            )
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при решении задачи: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ChinesePostmanApp(root)
    root.protocol("WM_DELETE_WINDOW", lambda: [plt.close('all'), root.destroy()])
    try:
        root.mainloop()
    except (KeyboardInterrupt, tk.TclError):
        plt.close('all')
        root.destroy()