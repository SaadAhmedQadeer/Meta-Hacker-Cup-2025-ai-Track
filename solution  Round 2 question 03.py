import sys
from collections import deque, defaultdict

def solve():
    """
    Optimized solution using BFS with route segment tracking to avoid redundant explorations.
    """
    try:
        line = sys.stdin.readline()
        if not line.strip():
            return None
        N, K, M = map(int, line.split())
        
        routes = []
        court_to_routes = defaultdict(list)
        
        for i in range(M):
            route_data = list(map(int, sys.stdin.readline().split()))
            L = route_data[0]
            route_stops = route_data[1:]
            routes.append(route_stops)
            
            for j in range(len(route_stops)):
                court_to_routes[route_stops[j]].append((i, j))
                
    except (IOError, ValueError):
        return None
    
    # BFS with visited route segments tracking
    dist = [-1] * (N + 1)
    dist[1] = 0
    
    # Track which (route_id, starting_index) combinations we've already explored
    visited_segments = set()
    
    queue = deque([1])
    
    while queue:
        u = queue.popleft()
        current_dist = dist[u]
        
        # Explore all routes passing through court u
        for route_id, u_index in court_to_routes[u]:
            # Skip if we've already explored from this position on this route
            segment_key = (route_id, u_index)
            if segment_key in visited_segments:
                continue
            visited_segments.add(segment_key)
            
            route = routes[route_id]
            L = len(route)
            
            # Explore up to K stops forward on this route
            for steps in range(1, min(K + 1, L - u_index)):
                v_index = u_index + steps
                v = route[v_index]
                
                # Update distance if this is the first time reaching v
                if dist[v] == -1:
                    dist[v] = current_dist + 1
                    queue.append(v)
    
    # Calculate the result
    result = sum(dist[i] * i for i in range(1, N + 1))
    return result

def main():
    """
    Main function to handle multiple test cases.
    """
    try:
        line = sys.stdin.readline()
        if not line.strip():
            return
        num_test_cases = int(line)
        
        for case_num in range(1, num_test_cases + 1):
            result = solve()
            if result is not None:
                print(f"Case #{case_num}: {result}")
                
    except (IOError, ValueError) as e:
        print(f"An error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    input_filename = 'input.txt'
    output_filename = 'output.txt'
    
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    output_file = None
    
    try:
        sys.stdin = open(input_filename, 'r')
        output_file = open(output_filename, 'w')
        sys.stdout = output_file
        main()
    except FileNotFoundError:
        print(f"Error: '{input_filename}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        if output_file:
            output_file.close()