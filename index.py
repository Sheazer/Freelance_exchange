from collections import defaultdict

def can_seat_guests(N, M, pairs):
    graph = defaultdict(list)
    for u, v in pairs:
        graph[u].append(v)
        graph[v].append(u)

    color = {}  # Словарь для хранения цвета каждой вершины (0 или 1)

    def dfs(node, c):
        color[node] = c
        for neighbor in graph[node]:
            if neighbor in color:
                if color[neighbor] == c:
                    return False
            else:
                if not dfs(neighbor, 1 - c):
                    return False
        return True

    return dfs(0, 0)

# Пример использования
N, M = map(int, input().split())
pairs = []
for _ in range(M):
    pairs.append(tuple(map(int, input().split())))

if can_seat_guests(N, M, pairs):
    print("YES")
else:
    print("NO")