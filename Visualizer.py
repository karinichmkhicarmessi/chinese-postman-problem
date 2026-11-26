import tkinter as tk

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Visualizer:
    @staticmethod
    def visualize_graph(frame, graph, text):
        for widget in frame.winfo_children():
            widget.destroy()

        fig, axis = plt.subplots(figsize=(8, 5))
        pos = nx.spring_layout(graph, seed=42)
        nx.draw_networkx_nodes(graph, pos, node_color='lavender', node_size=700, ax=axis)
        nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold', ax=axis)

        for u, v, w in graph.edges(data=True):
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)],
                                   width=1.5, edge_color='black', style='solid', ax=axis)
            weights = w['weight']
            axis.text((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2,
                      str(weights), color='indigo', ha='center', va='center',
                      bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        axis.set_title(text, fontsize=14)
        plt.tight_layout()

        figure = FigureCanvasTkAgg(fig, master=frame)
        figure.draw()
        figure.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    @staticmethod
    def visualize_solution(frame, graph, solution, algorithm):
        for widget in frame.winfo_children():
            widget.destroy()

        if not solution.get('duplicates', []):
            fig, axis = plt.subplots(figsize=(8, 5))
            pos = nx.spring_layout(graph, seed=42)

            nx.draw_networkx_nodes(graph, pos, node_color='lavender', node_size=500, ax=axis)
            nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold', ax=axis)

            for u, v, data in graph.edges(data=True):
                nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], width=1.5, edge_color='black', style='solid',
                                       ax=axis)
                weight = data['weight']
                axis.text((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2,
                          str(weight), color='indigo', ha='center', va='center',
                          bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

            axis.set_title("Эйлеров граф", fontsize=14)
            plt.tight_layout()

            figure = FigureCanvasTkAgg(fig, master=frame)
            figure.draw()
            figure.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            return

        if algorithm == "Гуяна":
            fig, (axis1, axis2) = plt.subplots(1, 2, figsize=(12, 5))
            pos = nx.spring_layout(graph, seed=42)
            Visualizer.draw_graph(axis1, graph, pos, "Исходный граф")
            Visualizer.graph_with_duplicates(axis2, graph, pos, solution['duplicates'], "Полученный эйлеров граф")

        else:
            fig, (axis1, axis2, axis3) = plt.subplots(1, 3, figsize=(18, 5))
            pos = nx.spring_layout(graph, seed=42)
            Visualizer.draw_graph(axis1, graph, pos, "Исходный граф")
            Visualizer.k_graph(axis2, solution['G'], solution['match'], "Полный граф для нечетных вершин")
            Visualizer.graph_with_duplicates(axis3, graph, pos, solution['duplicates'], "Полученный эйлеров граф")

        plt.tight_layout()

        figure = FigureCanvasTkAgg(fig, master=frame)
        figure.draw()
        figure.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    @staticmethod
    def draw_graph(axis, graph, pos, text):
        nx.draw_networkx_nodes(graph, pos, node_color='lavender', node_size=700, ax=axis)
        nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold', ax=axis)
        for u, v, w in graph.edges(data=True):
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], width=1.5, edge_color='black', style='solid', ax=axis)
            weights = w['weight']
            axis.text((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2,
                      str(weights), color='indigo', ha='center', va='center',
                      bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        axis.set_title(text, fontsize=14)

    @staticmethod
    def graph_with_duplicates(axis, graph, pos, duplicates, text):
        Visualizer.draw_graph(axis, graph, pos, text)
        for u, v, data in graph.edges(data=True):
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], width=1.5, edge_color='black', style='solid', ax=axis)
        for u, v in duplicates:
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], width=1.5, edge_color='blueviolet',arrows=True, style='dashed',
                                   connectionstyle='arc3,rad=0.2', ax=axis)

    @staticmethod
    def k_graph(axis, graph, match, text):
        pos = nx.spring_layout(graph, seed=42)
        nx.draw_networkx_nodes(graph, pos, node_color='lavender', node_size=700, ax=axis)
        nx.draw_networkx_labels(graph, pos, font_size=10, font_weight='bold', ax=axis)
        for u, v, w in graph.edges(data=True):
            nx.draw_networkx_edges(graph, pos, edgelist=[(u, v)], width=1.5, edge_color='black', style='solid', ax=axis)
            weight = w['weight']
            axis.text((pos[u][0] + pos[v][0]) / 2, (pos[u][1] + pos[v][1]) / 2,
                      str(weight), color='indigo', ha='center', va='center',
                      bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))
        if match:
            nx.draw_networkx_edges(graph, pos, edgelist=match, width=2, edge_color='thistle', style='dashed', ax=axis)
        axis.set_title(text, fontsize=14)