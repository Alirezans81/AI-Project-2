import time
import copy

backtracks = 0


def backtracking(assignment, domains, matches, stadiums, sensitive):

    global backtracks

    if len(assignment) == len(matches):
        return assignment

    var = select_unassigned(assignment, matches)

    for value in domains[var]:

        if consistent(var, value, assignment, matches, sensitive):

            new_assignment = assignment.copy()
            new_assignment[var] = value

            new_domains = copy.deepcopy(domains)

            if forward_check(var, value, new_domains, matches):

                result = backtracking(new_assignment, new_domains, matches, stadiums, sensitive)

                if result:
                    return result

    backtracks += 1
    return None


def select_unassigned(assignment, matches):
    for i in range(len(matches)):
        if i not in assignment:
            return i


def consistent(var, value, assignment, matches, sensitive):

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

    # two or more sensitive game conflict
    if var in sensitive:
      for m, v in assignment.items():
          if m in sensitive and v[0] == day:
              return False


    return True


def forward_check(var, value, domains, matches):

    day, hour, stadium = value
    t1, t2 = matches[var]

    for m in domains:

        if m == var:
            continue

        new_domain = []

        for d, h, s in domains[m]:

            a, b = matches[m]

            if d == day and h == hour and s == stadium:
                continue

            if d == day and (t1 in [a, b] or t2 in [a, b]):
                continue

            new_domain.append((d, h, s))

        domains[m] = new_domain

        if len(domains[m]) == 0:
            return False

    return True


def main():

    global backtracks

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

    sensitive = set()
    for _ in range(K):
        a, b = input().split()
        sensitive.add(tuple(sorted((a, b))))

    if N > S * D * H or K > D:
        print("No Solution")
        return

    domains = {}

    for i in range(N):
        domains[i] = []
        for d in range(1, D + 1):
            for h in range(1, H + 1):
                for s in stadiums:
                    domains[i].append((d, h, s))

    start = time.time()

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
