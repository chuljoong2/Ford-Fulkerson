# Ford-Fulkerson 알고리즘

## 개요

- 학번: 201701688
- 이름: 윤철중
- 작성일자: 22.04.28

이 글은 인천대학교 2022-1학기 `컴퓨터 알고리즘` 중간고사 대체 과제를 위해 작성하게 되었습니다. `최대 유량 알고리즘(Max Flow Algorithm)`을 `포드-풀커슨 알고리즘(Ford-Fulkerson Algorithm)`을 중심으로 살펴보도록 하겠습니다.

## 개념

### 최대 유량 문제

- 최대 유량 문제: Maximum Flow Problem
- 유량: 노드 𝑢와 𝑣 사이를 흐르는 유량(flow)은 𝑓(𝑢,𝑣)
- 용량: 노드 𝑢와 𝑣 사이를 흐르는 용량(capacity)은 𝑐(𝑢,𝑣)이며 간선에서 흐를 수 있는 최대 유량을 의미
- 유량 네트워크: 각각의 간선의 가중치가 비용이 아닌 **용량**을 갖는 방향성 그래프

즉, **최대 유량 문제는 유랑 네트워크에서 시작(source)노드 s와 도착(sink)노드 t가 주어졌을 때 각 간선의 용량을 고려해서 s에서 t까지 흘려보낼 수 있는 최대 유량을 찾는 문제이다.**

### 최대 유량 문제의 적용 사례

다음과 같이 **컴퓨터 네트워크의 대역폭을 나타낸 유량 네트워크**가 있다고 한다. 다음 **유량 네트워크에서 s에서 t로 초당 전송할 수 있는 자료의 최대 용량은 얼마인지** 살펴보도록 한다.

![https://user-images.githubusercontent.com/63987872/165857925-edd588e0-321f-4d76-999a-65b6c5c0fb56.jpg](https://user-images.githubusercontent.com/63987872/165857925-edd588e0-321f-4d76-999a-65b6c5c0fb56.jpg)

**각 경로로 보낼 수 있는 초당 최대 용량은 경로에 포함된 간선 중 가장 용량이 작은 간선에 의해 결정**된다.

예를들어 {s, a, c, t}를 순으로 자료가 전송된다고 하자.

s → a는 용량이 16이므로 16을 전부다 보낼 수 있고, a → c는 용량이 20이므로 a에서 들어온 유량 16을 모두 흘려보낸다. 하지만 c → t는 용량이 10이므로 c에서 들어온 유량 16을 모두 보낼 수 없고 오직 10만을 보낼 수 있다.

즉, {s, a, c, t}의 경로를 따라서는 경로에서 간선의 가장 작은 용량인 10만큼만 보낼 수 있다.

그렇다면 **이제 여러 패킷으로 나눠서 여러 개의 경로로 동시에 보낸다면 어떻게 될지** 살펴보도록 한다.

그림(b)와 같이 자료를 보낼 수 있다.

c → t는 어차피 10만큼만 보낼 수 있으므로 남은 유량은 b로 보내준다. b → d는 7만큼만 보낼 수 있으므로 d → t는 용량이 8이지만 7만큼 보낼 수 있다.

즉, **s에서 t까지 초당 최대 17까지 전송이 가능**하다.

### 유량 네트워크의 제약조건

1. **용량 제한 조건**: 𝑓(𝑢, 𝑣) ≤ 𝑐(𝑢, 𝑣), 유량은 용량보다 커서는 안된다.
2. **유량의 대칭성**: 𝑓(𝑢, 𝑣) = −𝑓(𝑣, 𝑢), 𝑢에서 𝑢로 유량이 흐르면, 𝑣에서 𝑢로 음수의 유량이 흐르는 것과 동일해야 한다.
3. **유량의 보존**: 한 정점에 대해서 들어오는 유량과 나가는 유량은 같아야 한다.

## Ford-Fulkerson 알고리즘

`Ford-Fulkerson 알고리즘`이 유량 네트워크 문제를 해결하기 위해 처음으로 고안된 방법으로 유량 네트워크 문제의 가장 기본적인 알고리즘이다.

### 동작 원리

1.**유량 네트워크의 모든 간선의 유량을 0으로 초기화** 하고, 2.**시작노드에서 도착노드까지 유량을 보낼 수 있는 경로를 찾아서 유량 보내기를 반복**한다.

![https://user-images.githubusercontent.com/63987872/165857932-14e85b04-bf37-4e13-a73b-5dd9e6599db6.jpg](https://user-images.githubusercontent.com/63987872/165857932-14e85b04-bf37-4e13-a73b-5dd9e6599db6.jpg)

그림(a)와 같이 유량 네트워크가 있다. 먼저 {s, a, t}의 경로인 점선을 따라서 시작노드 s에서 도착노드 t까지 최대 유량 1을 보낼 수 있다. 그 결과가 그림(b)이다. 마찬가지로 그림(b)에서 {s, b, t}의 경로인 점선을 따라서 유량 1을 보낼 수 있다. 따라서 그림(c)과 같이 도착노드에는 유량 2가 들어온다.

이렇게 s에서 t까지 가는 하나의 경로마다 증강되므로 `증강경로(augmenting path)`라고 한다.

- {s, a, t}: 최대 유량 1
- {s, b, t}: 최대 유량 1

이 증강경로를 다 찾아내는 것이 Ford-Fulkerson 알고리즘의 첫 번째 목표이다.

각 경로에서 유량을 보내려면 이미 흐르고 있는 유량 이외에 추가로 보낼 수 있는 용량이 있어야 한다. 예를들어 아래와 같이 용량이 10인 간선이 있다고 할 때, 이미 8만큼의 유량이 흐르고 있다면 추가로 보낼 수 있는 유량은 2이다.

![https://i.imgur.com/rzLyUxV.png](https://i.imgur.com/rzLyUxV.png)

이와같이 각 간선에 이미 흐르고 있는 용량 이외에 추가로 보낼 수 있는 유량을 `잔여 용량(residual capacity)`이라고 한다. u에서 v로의 잔여 용량 *𝑐𝑓*(_𝑢_,_𝑣_)는 다음과 같이 정의할 수 있다.

_𝑐𝑓_(_𝑢_, _𝑣_) = _𝑐_(_𝑢_, _𝑣_) − _𝑓_(_𝑢_, _𝑣_)

앞서 최대 유량 문제의 적용 사례에서 설명했던 것 처럼 각 경로로 보낼 수 있는 초당 최대 용량은 경로에 포함된 간선 중 가장 용량이 작은 간선에 의해 결정된다. 이를 다르게 정의할 수 있다. **증강경로로 보낼 수 있는 최대 유량은 포함된 간선의 잔여 용량 중에서 가장 작은 값**이 된다.

![https://user-images.githubusercontent.com/63987872/165857934-4998b4ae-7512-448a-8748-79ff2892946f.jpg](https://user-images.githubusercontent.com/63987872/165857934-4998b4ae-7512-448a-8748-79ff2892946f.jpg)

그림(a)와 같이 a → t는 2만큼 보낼 수 있지만 s → a가 1만큼만 보낼 수 있으므로 {s, a, t}는 최대 1만큼의 유량을 보낼 수 있다.

Ford-Fulkerson 알고리즘은 **더 이상 증강경로가 존재하지 않을 때까지 증강경로를 찾고 보낼 수 있는 최대 유량(경로가 포함된 간선들의 잔여 용량 중에서 가장 작은 값)을 경로를 따라 보내는 작업을 반복**한다. 그래프의 경로탐색 알고리즘은 대표적으로 DFS와 BFS가 있는데 **Ford-Fulkerson 알고리즘은 DFS를 사용**한다.

여기서 한가지 더 고려해야하는 경우가 있다. 만약 **그림(a)에서 {s, a, b, t}의 경로가 찾아진 경우**에 유량을 보내면 아래와 같은 결과가 나온다.

![https://user-images.githubusercontent.com/63987872/165857935-8a05a514-afb2-45e1-92ec-0f099daec752.jpg](https://user-images.githubusercontent.com/63987872/165857935-8a05a514-afb2-45e1-92ec-0f099daec752.jpg)

어떤 경로를 선택하는지에 따라서 **최대 유량을 못구하는 경우가 존재**한다.

이에 대한 해결방법은 유량 네트워크의 제약조건의 **유량의 대칭성을 이용하여 해결**할 수 있다. **b → a로 가는 간선은 없기 때문에 용량은 0**이다. 하지만 **유량의 대칭성에 의해 f(b, a) = -f(a, b) = -1**이 된다. 이를 이용하여 **잔여 용량을 구하면 _𝑐𝑓_(b, a) = _𝑐_(b, a) − _𝑓_(b, a) = 0 - (-1) = 1**이 된다.

따라서 **b → a로 간선이 실제로 존재하지는 않지만 1만큼의 유량을 보낼 수 있다.**

이와 같은 속성을 이용하여 최대 유량을 못구하는 경우를 배제하는 방법을 `유량 상쇄`라고 한다. 자세히 살펴보기 위해 아래와 같은 그림이 있다고 한다.

![https://user-images.githubusercontent.com/63987872/165857936-461e9a4f-af94-45ae-b572-fc0ae86dcf1c.jpg](https://user-images.githubusercontent.com/63987872/165857936-461e9a4f-af94-45ae-b572-fc0ae86dcf1c.jpg)

먼저 그림(a)를 보면 경로가 **{s, a, b, t}인 실선을 따라서 시작노드에서 도착노드로 최대 유량 1을 보낼 수 있다.** 그러면 **b → a로 보낼 수 있는 잔여 용량 1**이 있는데 **그림(a)의 경로가 {s, b, a, t}인 점선을 따라 시작노드에서 도착노드로 최대 유량 1을 보낼 수 있다.** 그 결과로 그림(b)가 되고 도착노드 t로 들어오는 최대 유량은 2가 된다. 이때, **a와 b는 서로 유량을 1씩 주고 받기 때문에 총 유량에 영향이 미치지 않는다.** 즉, **그림(c)와 같이 a와 b의 유량은 서로 상쇄시킬 수 있다.**

이런 과정으로 우리가 원하는 증강 경로를 정상적으로 찾는 것을 Ford-Fulkerson 알고리즘이라고 한다.

### 동작 방식

1. DFS를 이용하여 증강경로를 찾는다.
2. 찾아낸 경로에 보낼 수 있는 최대 유량을 찾는다. 그리고 잔여 용량을 구하여 네트워크를 갱신한다.
3. 증강경로를 찾을 수 없을 때까지 이 과정을 반복한다.

## 구현

### 코드

[소스코드](Ford-Fulkerson.py)

### 수행 결과

결과 확인을 위해 다음과 같은 그림이 가져왔다.

![사진출처: [https://gseok.gitbooks.io/algorithm/content/b124-d2b8-c6cc-d06c-d50c-b85c-c6b0/d3ec-b4dc-d480-cee4-c2a828-ford-fulkerson-c560-b4dc-baac-b4dc-ce74-d50428-edmonds-karp.html](https://gseok.gitbooks.io/algorithm/content/b124-d2b8-c6cc-d06c-d50c-b85c-c6b0/d3ec-b4dc-d480-cee4-c2a828-ford-fulkerson-c560-b4dc-baac-b4dc-ce74-d50428-edmonds-karp.html)](https://gseok.gitbooks.io/algorithm/content/assets/network-flow1.png)

사진출처: [https://gseok.gitbooks.io/algorithm/content/b124-d2b8-c6cc-d06c-d50c-b85c-c6b0/d3ec-b4dc-d480-cee4-c2a828-ford-fulkerson-c560-b4dc-baac-b4dc-ce74-d50428-edmonds-karp.html](https://gseok.gitbooks.io/algorithm/content/b124-d2b8-c6cc-d06c-d50c-b85c-c6b0/d3ec-b4dc-d480-cee4-c2a828-ford-fulkerson-c560-b4dc-baac-b4dc-ce74-d50428-edmonds-karp.html)

위 그림의 정점은 숫자로 **S = 1**, **T = 8**, **A ~ F = 2 ~ 7**로 표현할 수 있다고 가정한다.

- {S, A, D, T} 경로일 때 = 1
- {S, A, E, T} 경로일 때 = 2
- {S, B, E, T} 경로일 때 = 2
- {S, C, F, E, T} 경로일 때 = 1
- {S, C, F, T} 경로일 때 = 4

**네트워크의 최대 유량은 10이 나온다.**

![https://gseok.gitbooks.io/algorithm/content/assets/network-flow8.png](https://gseok.gitbooks.io/algorithm/content/assets/network-flow8.png)

### 실행 결과

![https://user-images.githubusercontent.com/63987872/165857937-a8a8aff6-b9e7-457c-b262-b5b16b200382.jpg](https://user-images.githubusercontent.com/63987872/165857937-a8a8aff6-b9e7-457c-b262-b5b16b200382.jpg)

## 성능 분석

Ford-Fulkerson 알고리즘은 DFS를 사용하여 증강경로를 찾는다. 이때, **DFS를 이용하면 시간효율이 떨어지는 경우가 있다.** 만약 다음과 같이 그림(a)의 그래프가 있다고 한다.

![https://user-images.githubusercontent.com/63987872/165857939-bc69d708-a746-4a04-a9ae-589c0585196e.jpg](https://user-images.githubusercontent.com/63987872/165857939-bc69d708-a746-4a04-a9ae-589c0585196e.jpg)

그림(b)와 같이 경로가 {s, a, b, t}인 **굵은 실선을 따라 경로를 찾았다**고 할 때, **유량은 1을 보낼 수 있다.** 1을 보내게 된다면 그림(c)와 같은 결과가 나온다. 이와 같이 다시 흘려보내게 된다면 다음 그림과 같은 결과가 나온다.

![https://user-images.githubusercontent.com/63987872/165857943-b31bf1f9-164e-4bf0-8ccf-78c5921eddad.jpg](https://user-images.githubusercontent.com/63987872/165857943-b31bf1f9-164e-4bf0-8ccf-78c5921eddad.jpg)

즉, DFS를 이용하여 경로를 찾을 때마다 유량을 1만큼만 보낼 수 있게 되어 총 경로 2개만 찾으면 해결할 수 있는 문제를 최대 유량의 수(위 그림에서는 2000번)만큼 경로를 찾고 알고리즘을 종료하게 된다.

따라서 **DFS의 시간복잡도는 매 반복 당 O(|V| + |E|)이고 그래프에서의 최대 유량이 total_flow라고 하면 `Ford-Fulkerson 알고리즘의 시간복잡도는 O((|V| + |E|) * total_flow)`가 된다.** **이때, 보통의 경우 간선의 개수가 정점의 개수보다 많기 때문에 `O(|E|) * total_flow)`가 된다. total_flow가 크다면 엄청난 시간 비효율을 겪게 될 것이다.**

**이러한 문제점은 DFS가 아닌 BFS로 증강경로를 찾아내면 해결할 수 있습니다.** 증강경로를 찾기 위해 `BFS를 사용하는 Ford-Fulkerson 알고리즘의 한 형태를 Edmonds-Karp 알고리즘`이라고 한다.

BFS를 사용하면 **`시간복잡도는 O(|V| * |E|^2)`로 줄어들게 된다.**
