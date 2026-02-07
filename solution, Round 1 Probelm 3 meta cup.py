import sys

def solve():
    """
    Solves the "Scaling Coolness" problem by constructing a valid sequence of multipliers.
    """
    try:
        # Read N, A, and B for the current test case.
        line = sys.stdin.readline()
        if not line.strip(): return None
        N, A, B = map(int, line.split())

    except (IOError, ValueError):
        return None

    # This list will hold the final 2*N multipliers.
    multipliers = []

    # --- Phase 1: First N days ---

    # For the first N-1 days, be conservative. Using a multiplier of 1 keeps the
    # coolness at its initial value of 1, ensuring we don't exceed A too early.
    for _ in range(N - 1):
        multipliers.append(1)

    # On day N, we need to choose a multiplier. The total coolness after this day
    # will be this multiplier's value. We need to find the largest possible coolness
    # that is less than or equal to A AND is a divisor of the final target B.
    # We search from A downwards. Since a solution is guaranteed, we will find one.
    coolness_at_N = 0
    for i in range(A, 0, -1):
        if B % i == 0:
            coolness_at_N = i
            break
            
    # The multiplier for day N is this value.
    multipliers.append(coolness_at_N)

    # --- Phase 2: Second N days ---

    # The remaining product we need to achieve is B divided by our current coolness.
    remaining_product = B // coolness_at_N
    
    # Again, be conservative for the next N-1 days by using multipliers of 1.
    for _ in range(N - 1):
        multipliers.append(1)
        
    # The final multiplier on day 2*N must be whatever is left to reach the target.
    multipliers.append(remaining_product)
    
    # Return the full sequence as a space-separated string.
    return " ".join(map(str, multipliers))

def main():
    """
    Main function to handle multiple test cases from a file.
    """
    try:
        # Read the total number of test cases from stdin.
        line = sys.stdin.readline()
        if not line.strip(): return
        num_test_cases = int(line)
        
        # Process each test case.
        for i in range(1, num_test_cases + 1):
            result_string = solve()
            if result_string is not None:
                # The solve function now returns a formatted string.
                print(f"Case #{i}: {result_string}")

    except (IOError, ValueError) as e:
        print(f"An error occurred while reading the number of test cases: {e}", file=sys.stderr)

if __name__ == "__main__":
    input_filename = 'input.txt'
    output_filename = 'output.txt'

    # Store original stdin and stdout to restore them later.
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    
    output_file = None

    try:
        # Redirect input to read from input.txt and output to write to output.txt.
        sys.stdin = open(input_filename, 'r')
        output_file = open(output_filename, 'w')
        sys.stdout = output_file
        
        main()

    except FileNotFoundError:
        print(f"Error: '{input_filename}' not found. Please create this file in the same directory.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
    finally:
        # Restore original stdin and stdout.
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        # CRITICAL: Close the output file to ensure all data is written to disk.
        if output_file:
            output_file.close()

