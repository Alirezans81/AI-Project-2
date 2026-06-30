import time
import copy

backtracks = 0


def backtracking(assignment, domains, matches, stadiums, sensitive):
    """
    Performs backtracking search to assign a valid time and stadium to every match.
    It uses MRV for variable selection, LCV for value ordering, and Forward Checking
    to reduce the domains of the remaining unassigned matches.
    """

    global backtracks

    if len(assignment) == len(matches):
        return assignment

    # MRV: choose the unassigned match with the smallest remaining domain
    var = select_unassigned(assignment, domains, matches)

    # LCV: try values that remove fewer future options first
    for value in order_domain_values(var, domains, matches, assignment, sensitive):

        if consistent(var, value, assignment, matches, sensitive):

            new_assignment = assignment.copy()
            new_assignment[var] = value

            new_domains = copy.deepcopy(domains)

            if forward_check(var, value, new_domains, matches, new_assignment, sensitive):

                result = backtracking(new_assignment, new_domains, matches, stadiums, sensitive)

                if result:
                    return result

    backtracks += 1
    return None


def select_unassigned(assignment, domains, matches):
    """
    Selects the next unassigned match using the MRV heuristic.
    MRV chooses the match with the smallest remaining domain to detect conflicts earlier.
    """

    unassigned = []

    for i in range(len(matches)):
        if i not in assignment:
            unassigned.append(i)

    return min(unassigned, key=lambda i: len(domains[i]))


def order_domain_values(var, domains, matches, assignment, sensitive):
    """
    Orders the possible values of a match using the LCV heuristic.
    LCV tries values that remove the fewest options from future matches first.
    """

    return sorted(
        domains[var],
        key=lambda value: count_removed_values(var, value, domains, matches, assignment, sensitive)
    )


def count_removed_values(var, value, domains, matches, assignment, sensitive):
    """
    Counts how many values would be removed from other unassigned matches
    if the current match was assigned to the given value. This count is used by LCV.
    """

    day, hour, stadium = value
    t1, t2 = matches[var]

    removed_count = 0

    for m in domains:

        if m == var or m in assignment:
            continue

        a, b = matches[m]

        for d, h, s in domains[m]:

            # stadium conflict
            if d == day and h == hour and s == stadium:
                removed_count += 1
                continue

            # team rest constraint
            if d == day and (t1 in [a, b] or t2 in [a, b]):
                removed_count += 1
                continue

            # sensitive match constraint
            if var in sensitive and m in sensitive and d == day:
                removed_count += 1

    return removed_count


def consistent(var, value, assignment, matches, sensitive):
    """
    Checks whether assigning a specific day, hour, and stadium to a match
    is consistent with all already assigned matches.
    It checks stadium conflict, team daily conflict, and sensitive match conflict.
    """

    day, hour, stadium = value
    t1, t2 = matches[var]

    for m, v in assignment.items():

        d, h, s = v
        a, b = matches[m]

        # stadium conflict
        if d == day and h == hour and s == stadium:
            return False

        # team rest constraint
        if day == d and (t1 in [a, b] or t2 in [a, b]):
            return False

        # sensitive match constraint
        if var in sensitive and m in sensitive and day == d:
            return False

    return True


def forward_check(var, value, domains, matches, assignment, sensitive):
    """
    Applies Forward Checking after assigning a value to a match.
    It removes invalid values from the domains of unassigned matches.
    If any domain becomes empty, the assignment is rejected and backtracking happens.
    """

    day, hour, stadium = value
    t1, t2 = matches[var]

    for m in domains:

        if m == var or m in assignment:
            continue

        new_domain = []
        a, b = matches[m]

        for d, h, s in domains[m]:

            # stadium conflict
            if d == day and h == hour and s == stadium:
                continue

            # team rest constraint
            if d == day and (t1 in [a, b] or t2 in [a, b]):
                continue

            # sensitive match constraint
            if var in sensitive and m in sensitive and d == day:
                continue

            new_domain.append((d, h, s))

        domains[m] = new_domain

        if len(domains[m]) == 0:
            return False

    return True


def main():
    """
    Reads input, builds the CSP domains, performs feasibility checks,
    runs the backtracking search, and prints the final schedule or No Solution.
    """
    
    global backtracks
    backtracks = 0

    S = int(input())
    stadiums = input().split()

    D = int(input())
    H = int(input())

    N = int(input())

    matches = []
    for _ in range(N):
        t1, t2 = input().split()
        matches.append((t1, t2))

    K = int(input())

    sensitive_pairs = set()
    for _ in range(K):
        a, b = input().split()
        sensitive_pairs.add(tuple(sorted((a, b))))

    sensitive = set()
    for i, match in enumerate(matches):
        if tuple(sorted(match)) in sensitive_pairs:
            sensitive.add(i)

    print("-" * 30)
    print("Output:")
    print("-" * 30)

    start = time.time()

    # Feasibility check: total capacity
    if N > S * D * H:
        print("No Solution")
        print("Backtracks:", backtracks)
        print("Time:", round(time.time() - start, 4), "seconds")
        return

    # Feasibility check: sensitive matches
    if K > D:
        print("No Solution")
        print("Backtracks:", backtracks)
        print("Time:", round(time.time() - start, 4), "seconds")
        return

    domains = {}

    for i in range(N):
        domains[i] = []
        for d in range(1, D + 1):
            for h in range(1, H + 1):
                for s in stadiums:
                    domains[i].append((d, h, s))

    result = backtracking({}, domains, matches, stadiums, sensitive)

    end = time.time()

    if result:

        for i, (t1, t2) in enumerate(matches):
            d, h, s = result[i]
            print(t1, t2, d, h, s)

    else:
        print("No Solution")

    print("Backtracks:", backtracks)
    print("Time:", round(end - start, 4), "seconds")


if __name__ == "__main__":
    main()