__author__ = 'allentran'

import numpy as np

class Graph(object):

    def __init__(self, graph_path):

        self.from_nodes_mapping = {}
        self.to_nodes_mapping = {}

        self.edge_dict = {}

        self._load_graph(graph_path=graph_path)
        self._create_mappings()

    # def _update_get_index(self, key):
    #
    #     if key not in self.nodes_mapping:
    #         self.nodes_mapping[key] = len(self.nodes_mapping)
    #     return self.nodes_mapping[key]

    def get_mappings(self):
        return self.from_nodes_mapping, self.to_nodes_mapping

    def _create_mappings(self):
        for key in self.edge_dict:
            self.from_nodes_mapping[key] = len(self.from_nodes_mapping)
        for to_nodes in self.edge_dict.values():
            for to_node in to_nodes:
                if to_node not in self.to_nodes_mapping:
                    self.to_nodes_mapping[to_node] = len(self.to_nodes_mapping)

    def _add_edge(self, from_idx, to_idx, degree=1):
        if from_idx not in self.edge_dict:
            self.edge_dict[from_idx] = dict()
        if to_idx in self.edge_dict[from_idx]:
            if degree >= self.edge_dict[from_idx][to_idx]:
                return
        self.edge_dict[from_idx][to_idx] = degree

    def _load_graph(self, graph_path):

        with open(graph_path, 'r') as graph_file:
            for line in graph_file:
                parsed_line = line.strip().split(' ')
                if len(parsed_line) in [2, 3]:
                    from_idx = int(parsed_line[0])
                    to_idx = int(parsed_line[1])
                    if len(parsed_line) == 3:
                        degree = int(parsed_line[2])
                        self._add_edge(from_idx, to_idx, degree)
                    else:
                        self._add_edge(from_idx, to_idx)

    def extend_graph(self, max_degree):

        def _update_min_dict(candidate_node, depth, min_set):
            if candidate_node in min_set:
                if min_set[candidate_node] <= depth:
                    return
                else:
                    min_set[candidate_node] = depth
            else:
                min_set[candidate_node] = depth

        def _get_connected_nodes(node_idx, current_depth):
            connected_dict = {}
            single_degree_nodes = [other_idx for other_idx in self.edge_dict[node_idx] if self.edge_dict[node_idx][other_idx] == 1]
            for other_idx in single_degree_nodes:
                _update_min_dict(other_idx, current_depth, connected_dict)

            if current_depth <= max_degree:
                for other_node_idx in single_degree_nodes:
                    if other_node_idx in self.edge_dict:
                        new_connected_nodes = _get_connected_nodes(other_node_idx, current_depth + 1)
                        if new_connected_nodes is not None:
                            for other_idx, depth in new_connected_nodes.iteritems():
                                _update_min_dict(other_idx, depth, connected_dict)
                return connected_dict

        from_to_idxs = []
        degrees = []

        for node in self.from_nodes_mapping.keys():
            connected_nodes = _get_connected_nodes(node_idx=node, current_depth=1)
            for other_node, degree in connected_nodes.iteritems():
                from_to_idxs.append([self.from_nodes_mapping[node], self.to_nodes_mapping[other_node]])
                degrees.append(float(1)/degree)

        return np.array(from_to_idxs).astype(np.int32), np.array(degrees).astype(np.float32)
