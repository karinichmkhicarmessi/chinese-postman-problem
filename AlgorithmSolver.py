import networkx as nx
from itertools import combinations

class AlgorithmSolver:
    @staticmethod
    def guan_algorithm(graph):
        if nx.is_eulerian(graph):
            cycle = list(nx.eulerian_circuit(graph))
            return {
                'result': cycle,
                'TW': sum(s['weight'] for u, v, s in graph.edges(data=True)),
                'duplicates': []
            }
        odd_v = [v for v, degree in graph.degree() if degree % 2 != 0]

        def min_weight(u, v):
            edg = graph.get_edge_data(u, v)
            if not edg:
                return float('inf')
            weights = [data['weight'] for data in edg.values()]
            return min(weights)

        g = nx.Graph()
        for u, v in combinations(odd_v, 2):
            try:
                length = nx.shortest_path_length(graph, u, v, weight='weight')
                g.add_edge(u, v, weight=length)
            except nx.NetworkXNoPath:
                continue
        # шаг 1
        m = nx.algorithms.matching.min_weight_matching(g, weight='weight')
        graph1 = nx.MultiGraph(graph.copy())
        duplicates = []

        for u, v in m:
            try:
                path = nx.shortest_path(graph, u, v, weight='weight')
                for i in range(len(path) - 1):
                    e = (path[i], path[i + 1])
                    duplicates.append(e)
                    w = min_weight(*e)
                    graph1.add_edge(e[0], e[1], weight=w)
            except nx.NetworkXNoPath:
                continue

        # шаг 2
        graph2 = nx.MultiGraph(graph1)
        duplicate_dict = {}
        for u, v in graph.edges():
            duplicate_dict[(u, v)] = graph.number_of_edges(u, v)

        for (u, v), k in duplicate_dict.items():
            cur = graph2.number_of_edges(u, v)
            if cur > k:
                removed = (cur - k) // 2 * 2
                for i in range(removed):
                    min_key = min(graph2[u][v], key=lambda c: graph2[u][v][c]['weight'])
                    graph2.remove_edge(u, v, min_key)
                    try:
                        duplicates.remove((u, v))
                    except ValueError:
                        pass
        # шаг 3
        graph3 = nx.MultiGraph(graph2)
        flag = True
        while flag:
            flag = False
            g1 = nx.Graph(graph3.edges())
            cycles = nx.cycle_basis(g1)

            for i in cycles:
                if len(i) < 3:
                    continue
                cycle_edges = list(zip(i, i[1:] + [i[0]]))
                dw = 0
                for u, v in cycle_edges:
                    if graph3.number_of_edges(u, v) > graph.number_of_edges(u, v):
                        dw += min_weight(u, v)
                tw = sum(min_weight(u, v) for u, v in cycle_edges)

                if dw > tw / 2:
                    flag = True
                    for u, v in cycle_edges:
                        ex = graph3.number_of_edges(u, v) - graph.number_of_edges(u, v)
                        for _ in range(ex):
                            graph3.remove_edge(u, v, min(graph3[u][v], key=lambda c: graph3[u][v][c]['weight']))
                            try:
                                duplicates.remove((u, v))
                            except ValueError:
                                pass

                        graph3.add_edge(u, v, weight=min_weight(u, v))
                        duplicates.append((u, v))
                    break

        # шаг 4
        cycle = list(nx.eulerian_circuit(graph3))

        ow = sum(data['weight'] for u, v, data in graph.edges(data=True))
        dw = sum(min_weight(u, v) for u, v in duplicates)
        tw = ow + dw
        return {
            'result': cycle,
            'TW': tw,
            'duplicates': duplicates,
            'match': m if 'matching' in locals() else None,
        }

    @staticmethod
    def edmonds_algorithm(graph):
        # шаг 1
        odd_v = [v for v, degree in graph.degree() if degree % 2 != 0]

        if not odd_v:
            cycle = list(nx.eulerian_circuit(graph))
            return {
                'result': cycle,
                'TW': sum(data['weight'] for u, v, data in graph.edges(data=True)),
                'duplicates': [],
                'match': None,
                'G': None
            }
        # шаг 2(a)
        dist = {}
        for u, v in combinations(odd_v, 2):
            try:
                d = nx.shortest_path_length(graph, u, v, weight='weight')
                dist[(u, v)] = d
                dist[(v, u)] = d
            except nx.NetworkXNoPath:
                raise ValueError
        # шаг 2(b)
        full_graph = nx.Graph()
        for u in odd_v:
            for v in odd_v:
                if u != v:
                    full_graph.add_edge(u, v, weight=dist[(u, v)])

        # шаг 2(с)
        match = nx.algorithms.matching.min_weight_matching(full_graph, weight='weight')

        # шаг 3
        graph1 = nx.MultiGraph(graph.copy())
        duplicates = []
        for u, v in match:
            try:
                path = nx.shortest_path(graph, u, v, weight='weight')
                for i in range(len(path) - 1):
                    e = (path[i], path[i + 1])
                    duplicates.append(e)
                    w = min(data['weight'] for data in graph.get_edge_data(*e).values())
                    graph1.add_edge(*e, weight=w)
            except nx.NetworkXNoPath:
                raise ValueError

        # шаг 4
        cycle = list(nx.eulerian_circuit(graph1))

        ow = sum(data['weight'] for u, v, data in graph.edges(data=True))
        dw = 0
        for u, v in duplicates:
            edg = graph.get_edge_data(u, v)
            if edg:
                w = min(i['weight'] for i in edg.values())
                dw += w
        return {
            'result': cycle,
            'TW': ow + dw,
            'duplicates': duplicates,
            'match': match,
            'G': full_graph
        }