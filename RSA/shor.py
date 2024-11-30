import random


class ShorBreaker:
    """Initailize the class variable N"""
    N = None

    def __init__(self, n : int = None):
        """
        Enter N from the terminal or 
        enter it as a class parameter.
        """
        print(f"{'='*17} Shor's Algorithm {'='*17}")
        if n is None:
            ShorBreaker.N = int(input(f"쇼어 알고리즘을 진행할 N을 입력하세요: "))
        else:
            ShorBreaker.N = n

    @staticmethod
    def execute():
        """
        The Shore algorithm proceeds in a total of three steps 
        and performs prime factorization of the input N 
        into the product of prime numbers.
        """
        def step1():
            """Step 1 randomly sets a random integer between 1 and N"""
            print(f"\n{'-'*20} step1 진행 {'-'*20}\n")
            a = random.randrange(start=2, stop=ShorBreaker.N)
            print(f"1과 n 사이의 값을 찾았습니다: {a}\n")
            return step2(a)

        def step2(a):
            """
            Step 2 checks whether the greatest common divisor of a 
            and N is 1, and if it is not 1, p and q can be found directly.
            """
            print(f"{'-'*20} step2 진행 {'-'*20}\n")
            x, y = ShorBreaker.N, a
            print(f"Calculating gcd({x}, {y})")
            while True:
                mod_times = 0
                if x >= y:
                    mod_times = x // y
                    x = x % y
                x, y = y, x
                if y == 1:
                    print("\ngcd 결과가 1입니다.\n")
                    return step3(a)
                elif y == 0:
                    print(f"\np와 q는 {x}, {ShorBreaker.N // x}입니다.")
                    print(f"{'='*52}", end='')
                    return x, ShorBreaker.N // x

        def step3(a):
            """
            When f(x)=a^x mod N, 
            find the period r in which the function value is repeated.

            If the cycle is an even number, proceed to step 4. 
            Otherwise, proceed from the beginning again.
            """
            print(f"{'-'*20} step3 진행 {'-'*20}\n")
            x = 1
            mod_result = []
            print(f"주기 r을 찾는 중...\n")
            while True:
                calc = (a ** x) % ShorBreaker.N
                mod_result.append(calc)
                if mod_result[0] == calc and x != 1:
                    r = x - 1
                    if r % 2 == 0:
                        print(f"주기 r을 찾았습니다: {r}\n")
                        return step4(a, r)
                    else:
                        print(f"step1부터 다시 시작합니다.\n")
                        return step1()
                else:
                    x += 1

        def step4(a, r):
            """ 
            GCD1 = gcd(N, a^(r/2) + 1)
            GCD2 = gcd(N, a^(r/2) - 1)
            
            Calculate the above and store the gcd result. 
            If the result is 1 or N, proceed again from step 1. 
            Otherwise, return it as p and q.
            """
            print(f"{'-'*20} step4 진행 {'-'*20}\n")
            gcd_result = []
            for i in range(0, 4, 2):
                x, y = ShorBreaker.N, int((a ** (r / 2))) + (i - 1)
                if x < y:
                    x, y = y, x
                print(f"{' '*14} Calculating gcd({x}, {y}) \n")
                while True:
                    mod_times = 0
                    if x >= y:
                        mod_times = x // y
                        x = x % y
                        print(f"Current step: gcd({x}, {y}) ->", end=' ')
                    print(f"{x} = {x + mod_times * y} - {mod_times} * {y}")
                    x, y = y, x
                    if y == 1:
                        print("\ngcd 결과가 1입니다.\n")
                        gcd_result.append(y)
                        break
                    if y == 0:
                        print("\n최대공약수가 1이 아닙니다.\n")
                        gcd_result.append(x)
                        break
            if (ShorBreaker.N in gcd_result) or (1 in gcd_result):
                print(f"{' '*5}{'*'*43}\n")
                return step1()
            else:
                print(f"{' '*5}{'*'*43}\n")
                print(f"p와 q는 {gcd_result[0]}, {gcd_result[1]}입니다.")
                print(f"{'='*52}", end='')
                return gcd_result[0], gcd_result[1]

        # Execute step1 to start the process
        return step1()

# 실행
shorbreaker = ShorBreaker()
ShorBreaker.execute()
