import random
import math
import sympy
import sys
import os
from typing import List

class PrimeTest:
    # 밀러-라빈 소수성 테스트
    def is_prime(self, n, k=5):
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        
        r, d = 0, n - 1
        while d % 2 == 0:
            r += 1
            d //= 2
        
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(r - 1):
                x = pow(x, 2, n)
                if x == n - 1:
                    break
            else:
                return False
        return True

    # 큰 소수 생성
    def generate_large_prime(self, bits):
        while True:
            num = random.getrandbits(bits) | (1 << (bits - 1)) | 1
            if self.is_prime(num):
                return num
    
class CipherManager:
    # 텍스트를 숫자로 변환
    def encrypt_text_to_number(self, letters: str, alpha: str) -> List[int]:
        numbers_list = []
        for char in letters:
            if char in alpha:
                numbers_list.append(alpha.index(char))
            else:
                if char == ' ':
                    numbers_list.append(alpha.index('|'))
                elif char == '\n':
                    numbers_list.append(alpha.index('`'))
                else:
                    print(f"경고: 문자 {char} 알파벳 리스트에서 찾을 수 없습니다.")
        return numbers_list

    def decrypt_number_to_text(self, numbers: List[int], alpha: str) -> str:
        """숫자 배열을 알파벳 문자열로 변환"""
        result = [] # 알파벳 리스트 초기화
        # [[], [], []]에서 작은 []들이 iteration
        for number in numbers:
            if number == alpha.index("|"):
                result.append(" ")
            elif number == alpha.index("`"):
                result.append("\n")
            else:
                result.append(alpha[number]) 
        # 리스트안에 값들을 병합하기 
        return ''.join(result) 

class Main(CipherManager):
    def __init__(self, primetest: PrimeTest) -> None:
        super().__init__()
        self.PrimeTest = primetest
        # 문자 변환을 위한 알파벳 리스트
        self.alpha: str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.<>/?:;\'"=+-_()*&^%$#@!~`|1234567890'
        # 이모지
        self.i: List[str] = ["🟢", "평문", "암호화"]; self.ii = ["🔵", "암호문", "복호화"] 
        self.InitVar()

    def InitVar(self) -> None:
        # RSA 키 생성
        p = self.PrimeTest.generate_large_prime(512)
        q = self.PrimeTest.generate_large_prime(512)
        self.n = p * q
        pi = (p - 1) * (q - 1)

        # e 값 설정
        # for e in range(2, pi):
        #    if math.gcd(e, pi) == 1:  # 수정된 조건
        #        if e == 65537:
        #               break
                
        self.e = 65537  # 일반적으로 사용되는 안전한 값
        self.d = sympy.mod_inverse(self.e, pi)

    def input_lines(self) -> str:
        """
        텍스트를 연속으로 입력받는 부분.
        'END'를 단독으로 입력해야 종료.
        """
        print("\n여러 단락을 입력하세요. 입력을 종료하려면 'END'를 단독으로 입력하세요.")
        print("✏️ 평문을 입력하세요: ")
        Text = ""  # 빈 텍스트

        # 계속 입력받기
        for line in sys.stdin:
            if line.strip() == 'END':  # 'END'를 단독으로 입력해야 종료
                break
            Text += line

        return Text.strip()  # 마지막에 불필요한 공백 제거 후 반환
            
    def run(self) -> None:
        print("🟢" + "="*50)
        print(" " * 10 + f"🛡️  RSA 암호 프로그램 시작  🛡️")
        print("🟢" + "="*50)

        yesorno = input("✏️ 평문을 가져오겠습니까? [y/n]: ")
        if yesorno.lower() == "y":
            try:
                filepath = input("📂 파일경로 입력하세요:")
                while not os.path.exists(filepath):     
                    print("❌ 존재하지 않는 파일 경로입니다.")   
                    filepath = input("📂 파일경로 입력하세요:")
                with open(filepath, 'r', encoding='utf-8') as file:
                    Msg = file.read()
            except Exception as e:
                print(f"❌ 오류 발생: {e}")
                return
        else:
            # 실제로 입력받는 부분
            Msg = self.input_lines()
            
        Msg = Msg.replace('’', '\'').replace('‘', '\'').replace('”', '\"').replace('“', '\"')
        numbers = self.encrypt_text_to_number(Msg, self.alpha)

        # RSA 암호화 및 복호화
        encrypted_numbers = [pow(num, self.e, self.n) for num in numbers]
        decrypted_numbers = [pow(num, self.d, self.n) for num in encrypted_numbers]

        plainText = self.decrypt_number_to_text(decrypted_numbers, self.alpha)

        print("🟢" + "="*50)
        print(f"📜 복호화된 결과: \n{plainText}") 
        print("🟢" + "="*50)
        
        if plainText == Msg:
            print("✅ 암호화 및 복호화 성공적으로 완료되었습니다.")
        else:
            print("❌ 복호화된 결과가 원래 평문과 일치하지 않습니다.")

if __name__=="__main__":
    pt = PrimeTest()
    rsa = Main(pt)
    rsa.run()