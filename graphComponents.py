class GraphTSP():
    def __init__(self, initial_nodes, adyacent_matrix):
        self.initial_path = initial_nodes
        self.current_path = self.initial_path
        self.adyacent_matrix = adyacent_matrix
        self.node_count = len(initial_nodes)
        self.current_path_length = self.path_length()
        self.initial_path_length = self.path_length()
        
    def path_length(self, path=[]):
        if not path:
            path = self.current_path
        path_length = 0
        previous_node = path[0]
        for next_node in path[1:]:
            path_length += self.adyacent_matrix[previous_node.key - 1][next_node.key -1]
            previous_node = next_node
        path_length += self.adyacent_matrix[path[-1].key - 1][path[0].key - 1]
        return path_length
    
    def get_cost_of_arc(self, i):
        if 0 <= i < self.node_count:
            start = self.current_path[i].key - 1
            end = (self.current_path[(i + 1) % self.node_count].key - 1) 
            return self.adyacent_matrix[start][end]
        else:
            return None
    
    def set_current_path(self, path):
        self.current_path_length = self.path_length(path)
        self.current_path = path
        
    def invert_path(self, start, end, path =[]):
        if not path:
            path = self.initial_path
        new_path_list = path[:start] + \
                                list(reversed(path[start:end])) + \
                                path[end:]
        return new_path_list
    
    def invert_current_path(self, start, end):
        new_path_list = self.current_path[:start] + \
                                list(reversed(self.current_path[start:end])) + \
                                self.current_path[end:]
        return new_path_list

    def print_path(self, path=[]):
        if not path:
            path = self.initial_path
        str_path = ""
        for node in path:
            str_path += str(node.key)+"-"
        str_path += str(path[0].key)
        return str_path

    def __str__(self):
        str_path_current = ""
        for node in self.current_path:
            str_path_current += str(node.key)+"-"
        str_path_current += str(self.current_path[0].key)
        return str_path_current
    
