import time

backtracks = 0


def backtracking(assignment, domains, matches, stadiums, sensitive):

    global backtracks

    if len(assignment) == len(matches):
        return assignment

    var = select_unassigned(assignment, matches)

    # consistent and forward_check

    backtracks += 1
    return None


def select_unassigned(assignment, matches):
    for i in range(len(matches)):
        if i not in assignment:
            return i


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
