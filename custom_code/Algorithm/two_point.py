n, m = 5,5
data = [1,2,3,2,5]

result = 0
summary = 0
end =0

# start를 차례대로 증가시키며 반복
for start in range(n):
    # end를 가능한 만큼 이동시키기
    while summary < m and end < n:
        summary += data[end]
        end +=1
        # 부분 합이 m일 때, 카운트 증가
    if summary == m:
        result +=1
    summary -= data[start]
print(result)

"""
구간 합 빠르게 구하기
1. 아래와 같이 N개의 정수로 구성된 수열이 존재
2. M개의 쿼리(Query) 정보가 제공
    - 각 쿼리는 L과 R로 구성됩니다.
    - [L, R]구간에 해당하는 데이터들의 합을 모두 구하는 문제
3. 시간 제한 : O(N+M)

=> 해결방법 : 접두사 합(Prefix Sum)
Prefix Sum : 매 M개의 쿼리 정보를 확인할 때, 구간 합은 P[R]-P[L-1]
"""
# 데이터의 개수 N과 데이터 입력 받기
n = 5
data = [10,20,30,40,50]
# Prefix Sum배열 계산
summary = 0
prefix_sum = [0]
for i in data:
    summary += i
    prefix_sum.append(summary)
# 구간 합 계산
left = 3
right = 4
print(prefix_sum[right] - prefix_sum[left-1])
