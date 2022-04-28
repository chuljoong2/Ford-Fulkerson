from sys import maxsize

INF = maxsize


def dfs(now, res):
    if now == n:
        return res

    for next in range(2, n + 1):
        if network[now][next] and not visited[next]:
            visited[next] = True
            w = dfs(next, min(res, network[now][next]))
            if w > 0:
                network[now][next] -= w
                network[next][now] += w
                return w
    return 0


n, m = map(int, input().split())
network = [[0 for _ in range(n+1)] for _ in range(n + 1)]


for _ in range(m):
    u, v, capacity = map(int, input().split())
    network[u][v] += capacity

total_flow = 0
flow = 1
idx = 0
print("🔥🔥실행결과🔥🔥")
while flow:
    visited = [False for _ in range(n+1)]
    flow = dfs(1, INF)
    total_flow += flow
    if flow != 0:
        idx += 1
        print(str(idx) + "번째 경로일 때:" + str(flow))
print("네트워크의 최대 유량: " + str(total_flow))
