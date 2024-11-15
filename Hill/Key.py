import pickle, os
from math import gcd
from sympy import Matrix
from random import choices

class KeyManager:    
    def determine_key_size(self, length):
        """텍스트 길이에 따라 키 크기를 결정"""
        if length <= 10:
            return 2  # 키행렬 2x2
        elif length <= 30:
            return 3  # 키행렬 3x3
        elif length <= 50:
            return 4  # 키행렬 4x4
        elif length <= 70:
            return 5  # 키행렬 5x5
        elif length <= 90:
            return 6  # 키행렬 6x6
        elif length <= 120:
            return 7  # 키행렬 7x7
        else:
            return 8  # 키행렬 8x8

    def Check_key(self, keys, modnum):
        """키가 사용이 가능한지를 확인 (행렬식이 0이 아닌지, 26과 서로소인지)"""
        while True:
            # 매트릭스로 만들기 
            arr = Matrix(keys) 
            # 행렬식 계산 
            detA = arr.det() 

            """키 행렬 출력"""
            print("\n🔑 < key Array Information > 🔑")
            print(f"{'=' * 40}")
            print(f"🧮  행렬 A [det(A) = {detA}]")
            print(f"{'-' * 40}")
            for row in keys:
                # 키 행렬을 열마다 출력
                print("|", " ".join(f"{num:3}" for num in row), " |")  
            print('=' * 40)

            # 행렬식이 0인 경우 
            if detA == 0: 
                # 결국엔 키를 다시 입력받기
                print("❌ 역행렬이 존재하지 않음. 다른 키를 입력해주세요.\n") 
            # 행렬식과 모듈로 제수의 최대공약수가 1이 아닌 경우
            elif gcd(detA, modnum) != 1: 
                # 결국엔 키를 다시 입력받기
                print("❌ modulo 연산이 불가능합니다. 다른 키를 입력해주세요.\n") 
            else:
                print("✔ 키 형식에 문제가 없습니다.") 
                break

    def input_key(self, length):
        """사용자로부터 키를 입력받고 예외처리"""
        while True:
            keys_len = self.determine_key_size(length); keys = []  # 키 행렬 초기화
            yesorno = input("🔑 저장된 키를 사용하겠습니까? [y/n]: ")
            # 저장된 키를 불러오는 경우
            if yesorno.lower() == "y":
                if os.path.exists('MyKeys.pkl'):
                    # 'rb'는 읽기 모드
                    with open('MyKeys.pkl', 'rb') as f: 
                        # 저장된 키 불러오기
                        keys_load = pickle.load(f)  
                        return keys_load, keys_len
                else:
                    print("❌ 저장된 키 파일이 없습니다.")
            # 새로운 키를 입력받는 경우
            else:    
                print(f"🔢 행렬의 크기는 {keys_len}x{keys_len}로 설정되었습니다.")
                print("🔑 키 값을 띄어쓰기로 구분하여 입력해주세요.")
                yesorno = input("🔑 키를 직접 입력하겠습니까? [y/n]: ")
                for i in range(keys_len):
                    try:
                        if yesorno.lower() == "y":
                            # 직접 입력받음
                            row = list(map(int, input(f"Row {i + 1}: ").split()))  
                        else:
                            # 랜덤 값 생성
                            row = list(map(int, choices(range(1, 101), k=keys_len)))  
                        if len(row) != keys_len:
                            print("입력 형식 오류: 올바른 행 길이를 입력해주세요.")
                            continue
                        if any(num < 0 for num in row):
                            print("입력 형식 오류: 양수의 숫자를 입력해주세요.")
                            continue
                        keys.append(row)  # 키 행렬에 추가            
                    except ValueError:
                        print("입력 형식 오류: 유효한 숫자를 입력해주세요.")
                # 키 저장
                # 'wb'는 쓰기 모드
                with open('MyKeys.pkl', 'wb') as f:  
                    pickle.dump(keys, f)
            return keys, keys_len