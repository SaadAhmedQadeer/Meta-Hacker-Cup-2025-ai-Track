import sys

sys.setrecursionlimit(5000)

MOD = 998244353

def dp_not_weak(S, K, memo, index=0, tight=True, started=False, prefix_mod=0, seen_mods=frozenset()):
    """
    Count numbers that are NOT K-weak (i.e., no substring has digit sum divisible by K).
    
    A number is K-weak if any substring has digit sum ≡ 0 (mod K).
    Using prefix sums: substring [i, j] has sum = prefix[j] - prefix[i-1].
    If prefix[j] ≡ prefix[i-1] (mod K), then substring is divisible by K.
    
    We track all prefix_sum % K values seen. If we see a repeat (including 0), it's K-weak.
    """
    if index == len(S):
        # Valid number formed (started == True means we have at least one non-zero digit)
        return 1 if started else 0
    
    state = (index, tight, started, prefix_mod, seen_mods)
    if state in memo:
        return memo[state]
    
    max_digit = int(S[index]) if tight else 9
    result = 0
    
    for digit in range(max_digit + 1):
        new_tight = tight and (digit == max_digit)
        
        if not started:
            if digit == 0:
                # Leading zero - number hasn't started yet
                result = (result + dp_not_weak(S, K, memo, index + 1, new_tight, False, 0, frozenset())) % MOD
            else:
                # First non-zero digit
                new_prefix_mod = digit % K
                
                # Check if this creates a K-weak number
                # The prefix sum from start is just this digit
                # If digit % K == 0, then we have a substring (just this digit) divisible by K
                if new_prefix_mod == 0:
                    # This single digit is divisible by K, so it's K-weak - skip
                    continue
                
                # Also check if we've seen this mod before (including the implicit 0 at start)
                # We always have an implicit prefix_mod = 0 before the number starts
                new_seen = frozenset([0, new_prefix_mod])
                result = (result + dp_not_weak(S, K, memo, index + 1, new_tight, True, new_prefix_mod, new_seen)) % MOD
        else:
            # Number has started
            new_prefix_mod = (prefix_mod + digit) % K
            
            # Check if this new prefix mod has been seen before
            # If yes, then we have a substring with sum divisible by K (K-weak)
            if new_prefix_mod in seen_mods:
                # This would create a K-weak number - skip
                continue
            
            new_seen = seen_mods | {new_prefix_mod}
            result = (result + dp_not_weak(S, K, memo, index + 1, new_tight, True, new_prefix_mod, new_seen)) % MOD
    
    memo[state] = result
    return result

def count_not_weak(X_str, K):
    """Count NOT K-weak numbers in [1, X]."""
    memo = {}
    return dp_not_weak(X_str, K, memo)

def string_subtract_one(s):
    """Subtract 1 from a numeric string."""
    digits = list(s)
    i = len(digits) - 1
    
    while i >= 0:
        if digits[i] != '0':
            digits[i] = str(int(digits[i]) - 1)
            break
        digits[i] = '9'
        i -= 1
    
    # Remove leading zeros
    result = ''.join(digits).lstrip('0')
    return result if result else '0'

def string_mod(s, mod):
    """Calculate string number modulo mod."""
    result = 0
    for c in s:
        result = (result * 10 + int(c)) % mod
    return result

def solve_case():
    """Solve one test case."""
    try:
        line = sys.stdin.readline().strip()
        if not line:
            return None
        
        parts = line.split()
        L_str, R_str, K = parts[0], parts[1], int(parts[2])
        
        # Total numbers in [1, R]
        total_R = string_mod(R_str, MOD)
        not_weak_R = count_not_weak(R_str, K)
        weak_R = (total_R - not_weak_R + MOD) % MOD
        
        # Total numbers in [1, L-1]
        L_minus_1 = string_subtract_one(L_str)
        if L_minus_1 == '0':
            weak_L_minus_1 = 0
        else:
            total_L_minus_1 = string_mod(L_minus_1, MOD)
            not_weak_L_minus_1 = count_not_weak(L_minus_1, K)
            weak_L_minus_1 = (total_L_minus_1 - not_weak_L_minus_1 + MOD) % MOD
        
        # Answer: weak numbers in [L, R]
        answer = (weak_R - weak_L_minus_1 + MOD) % MOD
        return answer
        
    except (IOError, ValueError, IndexError):
        return None

def main():
    """Handle multiple test cases."""
    try:
        T = int(sys.stdin.readline().strip())
        
        for case_num in range(1, T + 1):
            result = solve_case()
            if result is not None:
                print(f"Case #{case_num}: {result}")
                
    except (IOError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)

if __name__ == "__main__":
    input_file = 'input.txt'
    output_file = 'output.txt'
    
    original_stdin = sys.stdin
    original_stdout = sys.stdout
    out_file = None
    
    try:
        sys.stdin = open(input_file, 'r')
        out_file = open(output_file, 'w')
        sys.stdout = out_file
        main()
    except FileNotFoundError:
        print(f"Error: '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
    finally:
        sys.stdin = original_stdin
        sys.stdout = original_stdout
        if out_file:
            out_file.close()