import sys
from collections import Counter

def solve():
    """
    Solves the "Defining Prizes" problem using binary search on the answer.
    """
    try:
        # Read N and M
        line = sys.stdin.readline()
        if not line.strip(): return None
        N, M = map(int, line.split())
        
        # Read scores A
        line = sys.stdin.readline()
        if not line.strip(): return None
        A = list(map(int, line.split()))
        
        # Read merch counts B
        line = sys.stdin.readline()
        if not line.strip(): return None
        B = list(map(int, line.split()))

    except (IOError, ValueError):
        return None

    # --- Preprocessing ---
    
    # 1. Get total available merchandise
    total_merch = sum(B)
    
    # 2. Group competitors by score
    score_counts = Counter(A)
    unique_scores = sorted(score_counts.keys())
    
    # 3. Create a list of group sizes, from highest score to lowest
    # D = number of distinct score groups
    D = len(unique_scores)
    # top_score_groups[i] = number of people in the (i+1)-th highest scoring group
    top_score_groups = [score_counts[s] for s in reversed(unique_scores)]

    # 4. Precompute the total people and total cost for rewarding the top g groups
    # people_so_far[g] = total people in top g groups
    # cost_so_far[g] = total items needed to reward top g groups
    people_so_far = [0] * (D + 1)
    cost_so_far = [0] * (D + 1)
    
    current_people = 0
    current_cost = 0
    
    for g in range(1, D + 1):
        # Number of people in the g-th highest group
        num_people_in_group_g = top_score_groups[g - 1]
        
        # The cost increases in two ways:
        # 1. All existing people (current_people) need one more item
        # 2. The new group (num_people_in_group_g) needs 1 item
        current_cost += current_people + num_people_in_group_g
        current_people += num_people_in_group_g
        
        people_so_far[g] = current_people
        cost_so_far[g] = current_cost

    # --- Binary Search for the Answer ---
    
    # We are looking for the largest g (number of groups) that is possible.
    low = 0
    high = D
    max_g = 0
    
    while low <= high:
        g = (low + high) // 2
        
        if g == 0:
            max_g = max(max_g, g)
            low = g + 1
            continue

        # Check(g):
        # 1. Do we have enough merch *types*?
        possible_types = (g <= M)
        # 2. Do we have enough *total* merch?
        possible_items = (cost_so_far[g] <= total_merch)
        
        if possible_types and possible_items:
            max_g = max(max_g, g)
            low = g + 1  # Try to reward even more groups
        else:
            high = g - 1 # This g is impossible, try a smaller g
            
    # The answer is the total number of people in the top max_g groups
    return people_so_far[max_g]

def main():
    """
    Main function to handle multiple test cases from a file.
    """
    try:
        line = sys.stdin.readline()
        if not line.strip(): return
        num_test_cases = int(line)
        
        for i in range(1, num_test_cases + 1):
            result = solve()
            if result is not None:
                print(f"Case #{i}: {result}")

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