from collections import deque

def tsp_local_search(graph):
    graph.set_current_path(graph.initial_path)
    node_count = graph.node_count
    reversals = []
    i=0
    while True:
        min_path_length = float('inf')
        
        # buscamos el vecino con menor longitud #################
        for start in range(0, node_count - 1): 
            for end in range(start + 2, node_count):
                if (end - start) > node_count - 2:
                    continue
                    
                new_path = graph.invert_current_path(start, end)
                new_path_length = graph.path_length(new_path)
                
                # Almacenamos la inversión con menor longitud
                if  new_path_length < min_path_length:
                    min_path_length = new_path_length
                    min_path, min_start, min_end = new_path, start, end - 1  
        ###############################################################
                    
        if min_path_length < graph.current_path_length:
            graph.set_current_path(min_path)
            reversals.append((min_start,min_end))
            i+= 1
        else:
            break
            
    return graph, reversals, i

def tsp_tabu_search(graph, max_failures=10, max_tabu_elements=0):
    graph.set_current_path(graph.initial_path)
    best_global_path = graph.current_path
    best_global_path_length = graph.path_length(best_global_path)
    current_path = graph.current_path
    node_count = graph.node_count
    # lista tabú (cola)
    tabu_list = deque()
    # número máximo de elemento que pueden estar en la lista tabú
    if max_tabu_elements <= 0:
        max_tabu_elements = node_count // 4 + (4 - (node_count // 4) % 4) # ej. 10 nodos -> max: 4
    failed = 0
    i = 0

    while True:

        min_path_length = float('inf')
        paths_in_neighborhood_not_tabu = 0

        for start in range(0, node_count - 1):
            for end in range(start + 2, node_count):
                if (end - start) > node_count - 2:
                    continue

                tie1_start = current_path[(start - 1) % node_count].key
                tie1_end = current_path[(start) % node_count].key
                removed_tie1 = (tie1_start, tie1_end) if tie1_start < tie1_end else (tie1_end, tie1_start)

                tie2_start = current_path[(end - 1) % node_count].key
                tie2_end = current_path[(end) % node_count].key
                removed_tie2 = (tie2_start, tie2_end) if tie2_start < tie2_end else (tie2_end, tie2_start)

                new_path = graph.invert_current_path(start, end)
                new_path_length = graph.path_length(new_path)
                
                if (removed_tie1 in tabu_list) and\
                    (removed_tie2 in tabu_list) and\
                    (best_global_path_length <= new_path_length):
                    continue

                if new_path_length < min_path_length:
                    min_path_length = new_path_length
                    min_path, min_start, min_end = new_path, start, end - 1
                    min_removed_tie1 = removed_tie1
                    min_removed_tie2 = removed_tie2
                    min_added_tie1 = (tie1_start, tie2_start) if tie1_start < tie2_start else (tie2_start, tie1_start)
                    min_added_tie2 = (tie1_end, tie2_end) if tie1_end < tie2_end else (tie2_end, tie1_end)

                paths_in_neighborhood_not_tabu += 1

        if paths_in_neighborhood_not_tabu > 0:
            if not (min_path_length < best_global_path_length):
                failed += 1
                if failed >= max_failures:
                    break
            else:
                failed = 0
                
            graph.set_current_path(min_path)
            i += 1
            if graph.current_path_length < best_global_path_length:
                best_global_path = graph.current_path
                best_global_path_length = graph.current_path_length
                
            tabu_added_vertices = [min_removed_tie1, min_removed_tie2, min_added_tie1, min_added_tie2]
            
            if len(tabu_list) >= max_tabu_elements:
                [tabu_list.popleft() for _ in range(4)]
            tabu_list.extend(tabu_added_vertices)
        else:
            break
            
    graph.set_current_path(best_global_path)
    return graph, i