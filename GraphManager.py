import tkinter as tk
from tkinter import filedialog
import networkx as nx
import json


class GraphManager:
    def __init__(self):
        self.graph = nx.MultiGraph()

    def build_graph(self, vertices, edges):
        try:
            self.graph = nx.MultiGraph()
            vertices = [v.strip() for v in vertices.get().split(",")]
            self.graph.add_nodes_from(vertices)
            edges = [e.strip() for e in edges.get().split(",")]
            for i in edges:
                parts = i.split("-")
                u, v, w = parts
                self.graph.add_edge(u, v, weight=float(w))
            return True
        except Exception:
            raise ValueError("Ошибка при построении графа")

    @staticmethod
    def load_from_file(vertices, edges):
        file = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        try:
            with open(file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            vertices.delete(0, tk.END)
            edges.delete(0, tk.END)
            vertices.insert(0, ",".join(map(str, data.get('vertices', []))))
            edges.insert(0, ",".join(f"{e[0]}-{e[1]}-{e[2]}" for e in data.get('edges', [])))
            return True
        except Exception:
            raise ValueError("Ошибка при загрузке файла")

    @staticmethod
    def save_to_file(vertices, edges, solution=None):
        file = filedialog.asksaveasfilename(
            title="Сохранить результат в файл",
            defaultextension=".json",
            filetypes=(("JSON files", "*.json"), ("All files", "*.*"))
        )
        try:
            if solution:
                cycle = [f"{u}-{v}" for u, v in solution['result']]
                res = {
                    'cycle': cycle,
                    'TW': solution['TW'],
                    'duplicates': solution['duplicates']
                }
            else:
                edg = []
                for i in edges.get().split(","):
                    parts = i.strip().split("-")
                    if len(parts) == 3:
                        edg.append((parts[0], parts[1], float(parts[2])))
                res = {
                    'vertices': [v.strip() for v in vertices.get().split(",")],
                    'edges': edg
                }
            with open(file, 'w', encoding='utf-8') as f:
                json.dump(res, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            raise ValueError("Ошибка при сохранении файла")