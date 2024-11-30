import random

class PrimeTest:
    def is_prime(self, n, k=5):
        """
        밀러-라빈 소수성 테스트
        """
        # 1이면 소수 아님
        if n <= 1:
            return False 
        # 3이면 소수
        if n <= 3:
            return True 
        # 2, 3에 나누어 떨어지면 소수 아님 
        if n % 2 == 0 or n % 3 == 0:
            return False  
        
        # n - 1 = d * 2^r로 표현하기
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1; d //= 2
        
        for _ in range(k):
            # 2보다 크고 n - 2보다 작은 임의의 a 선택
            a = random.randint(2, n - 2)
            # x = a^d mod n 계산
            x = pow(a, d, n)
            # x=1 x=n-1일 경우 소수일 가능성 
            if x == 1 or x == n - 1:
                continue
            # 제곱 반복
            # x <- x^2 mod n을 r - 1번 반복
            for _ in range(r - 1):
                x = pow(x, 2, n)
                # x = n-1인 경우 소수일 가능성
                if x == n - 1:
                    break
                # x = 1일 경우 합성수
            # 반복 끝까지 가면 모두 합성수    
            else:
                return False
        return True
    
    def generate_large_prime(self, bits):
        """
        큰 소수 생성
        1 << (bits - 1)은 이진수 1을 자릿수 bits - 1만큼 왼쪽으로 이동
        """
        while True:
            num = random.getrandbits(bits)
            if self.is_prime(num):
                print(f"소수를 찾았습니다. -> {num}")
                return num