import numpy as np
from sympy import Matrix, mod_inverse
from typing import List

class CipherManager:
    def __init__(self, alpha : str, keys : List, keys_len : int):
        """Initialize"""
        self.alpha = alpha
        self.modnum= len(self.alpha)
        self.keys = keys
        self.keys_len = keys_len
        # 키행렬을 reshape -> (2x2, 3x3, 4x4, 5x5)
        self.key_matrix = np.array(self.keys).reshape(self.keys_len, self.keys_len) 

    def encrypt_text_to_number(self, text : str):
        """텍스트를 키 크기 단위로 분할하여 숫자로 변환"""
        # 텍스트를 키 크기 단위로 분할
        letters = [list(text[i:i + self.keys_len]) for i in range(0, len(text), self.keys_len)] 
        numbers_list = [] # 숫자 리스트 초기화
        for group in letters: # [[], [], []]에서 작은 []들이 iteration 
            numbers = [] # 숫자 배열을 저장할 리스트 초기화
            for char in group: # 그룹 안에 문자들이 
                if char in self.alpha: # alpha에 있으면
                    # 유효한 문자만 처리
                    numbers.append(self.alpha.index(char)) 
                else: # 없으면
                    if char==' ':
                        numbers.append(self.alpha.index('|'))
                    elif char=='\n':
                        numbers.append(self.alpha.index('`'))
                    else:
                        print(f"경고: 문자 {char} 알파벳 리스트에서 찾을 수 없습니다.")
            # 암호화시에 X패딩
            # 숫자 길이 초기화 -> 키의 길이가 4인데 2일 경우 2번 X패딩
            i = len(numbers) 
            # 마지막 []의 길이가 부족한 경우 X로 패딩
            while i < self.keys_len: 
                # X로 패딩하여 숫자로 매칭하는 부분
                numbers.append(self.alpha.index('X')) 
                i += 1 # 길이 1 증가
            # 숫자 리스트를 배열로 변환하고 열벡터로 만듦
            numbers_list.append(np.array(numbers).reshape(-1, 1)) 
        return numbers_list  # 숫자 배열 반환

    def encrypt_number_to_text(self, numbers_list : List):
        """숫자 배열을 알파벳 문자열로 변환"""
        result = [] # 알파벳 리스트 초기화
        # [[], [], []]에서 작은 []들이 iteration
        for numbers in numbers_list: 
            # 작은 []안에 숫자들이 인덱스이고 그 인덱스에 알파벳 매칭
            result.extend(self.alpha[num[0]] for num in numbers) 
        return ''.join(result) # 리스트안에 값들을 병합하기 
    
    def decrypt_text_to_number(self, text : str):
        """텍스트를 키 크기 단위로 분할하여 숫자로 변환"""
        # 텍스트를 키 크기 단위로 분할
        letters = [list(text[i:i + self.keys_len]) for i in range(0, len(text), self.keys_len)] 
        # 숫자 리스트 초기화
        numbers_list = [] 
        # [[], [], []]에서 작은 []들이 iteration 
        for group in letters: 
            # 숫자 배열을 저장할 리스트 초기화
            numbers = [] 
            for char in group: # 그룹 안에 문자들이 
                # alpha에 있으면
                if char in self.alpha: 
                    # 유효한 문자만 처리
                    numbers.append(self.alpha.index(char))  
                else: # 없으면'
                    print(f"경고: 문자 {char} 알파벳 리스트에서 찾을 수 없습니다.")
             # 숫자 리스트를 배열로 변환하고 열벡터로 만듦
            numbers_list.append(np.array(numbers).reshape(-1, 1))
        return numbers_list  # 숫자 배열 반환

    def decrypt_number_to_text(self, numbers_list : List):
        """숫자 배열을 알파벳 문자열로 변환"""
        result = [] # 알파벳 리스트 초기화
        # [[], [], []]에서 작은 []들이 iteration
        for numbers in numbers_list:
            # 작은 []안에 숫자들이 인덱스이고 그 인덱스에 알파벳 매칭
            for num in numbers:
                if num[0] == self.alpha.index("|"):
                    result.append(" ")
                elif num[0] == self.alpha.index("`"):
                    result.append("\n")
                else:
                    result.append(self.alpha[num[0]]) 
        # 암호화시에 X패딩 원복
        # 마지막 원소부터 키의 길이만큼 이전까지 거꾸로
        for text in result[-1:-self.keys_len:-1]:
            # 텍스트가 X일 때
            if text == 'X':
                # 마지막 원소 없애기
                result.pop() 
        # 리스트안에 값들을 병합하기 
        return ''.join(result) 
    
class EncryptionManager(CipherManager):
    def __init__(self, alpha : str, keys : List, keys_len : int):
        """Initialize"""
        # 변수 함수들을 상속
        super().__init__(alpha, keys, keys_len) 

    def encrypt(self, plaintext):
        """텍스트 암호화"""
        # 받은 평문을 숫자로 변환
        numbers_list = self.encrypt_text_to_number(plaintext) 
        # 키행렬과 숫자행렬의 곱하기 연산 후 다시 모듈로 연산 (수식 증명)
        encrypted_list = [(np.dot(self.key_matrix, num) % self.modnum) for num in numbers_list] 
        # 결국엔 숫자를 다시 알파벳으로 반환 (암호화)
        return self.encrypt_number_to_text(encrypted_list) 

class DecryptionManager(CipherManager):
    def __init__(self, alpha : str, keys : List, keys_len : int):
        """Initialize"""
        #변수 함수들을 상속
        super().__init__(alpha, keys, keys_len) 
        # 키행렬의 역행렬 구하기 
        self.inverse_key = self.calculate_inverse_key() 

    def calculate_inverse_key(self):
        """키 행렬의 역행렬 계산 (행렬식, 여인수행렬의 전치, 행렬식 역원)"""
        # 키 list를 배열로 변환
        arr = Matrix(self.keys)
        # 행렬식
        detA = arr.det()  
        # 여인수행렬의 전치행렬
        cofactor_matrix = arr.cofactor_matrix().T 
        # det(A)mod26의 역원 구하기
        mod_inverse_detA = mod_inverse(int(detA), self.modnum) 
        # 결국엔 키행렬의 역행렬의 mod26 결과 반환 
        return (mod_inverse_detA * cofactor_matrix) % self.modnum 
    
    def decrypt(self, cipher_text):
        """텍스트 복호화"""
        # 암호문을 숫자로 변환 
        numbers_list = self.decrypt_text_to_number(cipher_text) 
        # 키의 역행렬과 숫자행렬의 곱하기 연산 후 다시 모듈로 연산 (수식 증명)
        decrypted_list = [(np.dot(self.inverse_key, num) % self.modnum) for num in numbers_list] 
        # 결국엔 숫자를 다시 알파벳으로 반환 (복호화)
        return self.decrypt_number_to_text(decrypted_list) 