import json
from typing import List
from MySympy import ModInverse
from prime import PrimeTest
from LongText import get_plaintext

class RSACipher:
    def text_to_number(self, letters: str, alpha: str) -> List[int]:
        """Convert text to a list of numbers."""
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
                    print(f"⚠️ 경고: 문자 '{char}' 알파벳 리스트에서 찾을 수 없습니다.")
        return numbers_list

    def number_to_text(self, numbers: List[int], alpha: str) -> str:
        """Convert a list of numbers back to text."""
        result = []
        for number in numbers:
            if number == alpha.index("|"):
                result.append(" ")
            elif number == alpha.index("`"):
                result.append("\n")
            else:
                result.append(alpha[number])
        return ''.join(result)

    def encryption(self, msg: str, public_key: List[int], alpha: str):
        """Encrypt with the converted numbers."""
        msg = msg.replace('’', '\'').replace('‘', '\'').replace('”', '\"').replace('“', '\"')
        numbers = self.text_to_number(msg, alpha)
        encrypted_numbers = [pow(num, public_key[0], public_key[1]) for num in numbers]
        return {"encrypted_numbers": encrypted_numbers}

    def decryption(self, numbers: List[int], private_key: List[int], alpha: str):
        """Decrypt the converted numbers and convert them back to text."""
        decrypted_numbers = [pow(num, private_key[0], private_key[1]) for num in numbers]
        decrypted_texts = self.number_to_text(decrypted_numbers, alpha)
        return {"decrypted_numbers": decrypted_numbers, "decrypted_texts": decrypted_texts}

class RSAMain(RSACipher):
    
    ALPHA_FILE = "data/alpha.txt"
    PATH1 = "data/MyKey.json"
    PATH2 = "data/MyCipher.json"

    def __init__(self):
        super().__init__()
        """Receives a decimal bit size and generates a decimal number."""
        self.primetest = PrimeTest()
        bits_num1 = int(input("p의 비트수를 입력하세요(예: 1024 2048 4096): "))
        bits_num2 = int(input("q의 비트수를 입력하세요(예: 1024 2048 4096): "))
        
        print("p에 대한 소수를 생성 중입니다...")
        self.__p = self.primetest.generate_large_prime(bits_num1)
        print("q에 대한 소수를 생성 중입니다...")
        self.__q = self.primetest.generate_large_prime(bits_num2)
        self.alpha = self.load_alpha()

    def load_alpha(self):
        """Select the alphabet, numbers, and special characters you want to convert."""
        try:
            with open(self.ALPHA_FILE, 'r') as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"⚠️ {self.ALPHA_FILE} 파일이 존재하지 않습니다. 기본 ALPHA 사용합니다."
                )
    
    def make_key(self):
        """Generate and store public and private keys"""
        n = self.__p * self.__q
        phi_n = (self.__p - 1) * (self.__q - 1)
        e = [3, 17, 65537]
        # p와 q 삭제
        del self.__p
        del self.__q
        d = ModInverse(e[2], phi_n).result
        key_dic = {"public_key": [e[2], n], "private_key": [d, n]}
        with open(self.PATH1, 'w') as file:
            json.dump(key_dic, file)

    def load_key(self):
        """Load saved keys"""
        try:
            with open(self.PATH1, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            pass

    def encrypt_message(self):
        """Start encryption"""
        print("✏️  메시지 암호화를 시작합니다.")
        key_dic = self.load_key()
        if not key_dic:
            print("🔑 키가 없으므로 새 키를 생성합니다.")
            self.make_key()
            key_dic = self.load_key()
        msg = get_plaintext()
        cipher_dic = self.encryption(msg=msg, public_key=key_dic["public_key"], alpha=self.alpha)
        with open(self.PATH2, 'w') as file:
            json.dump(cipher_dic, file)
        print(f"📜 암호화 완료! 결과가 {self.PATH2}에 저장되었습니다.")

    def decrypt_message(self):
        """Start decryption"""
        print("✏️  메시지 복호화를 시작합니다.")
        key_dic = self.load_key()
        if not key_dic:
            raise FileNotFoundError("🔑 키 파일이 없습니다. 복호화를 진행할 수 없습니다.")
        try:
            with open(self.PATH2, 'r') as file:
                cipher_dic = json.load(file)
            plain_dic = self.decryption(
                numbers=cipher_dic["encrypted_numbers"],
                private_key=key_dic["private_key"],
                alpha=self.alpha
            )
            print(f"📜 복호화 완료: {plain_dic['decrypted_texts']}")
        except FileNotFoundError:
            raise FileNotFoundError(f"⚠️ {self.PATH2} 파일이 존재하지 않습니다.")

    def main_run(self):
        """Select the option you want to repeat"""
        while True:
            print("\n" + " " * 10 + "🔐 옵션 🔐")
            print("1. 암호화")
            print("2. 복호화")
            print("3. 종료")
            option = input("번호를 선택하세요: ").strip()
            if option == "1":
                self.encrypt_message()
            elif option == "2":
                self.decrypt_message()
            elif option == "3":
                print("프로그램을 종료합니다. 👋")
                break
            else:
                print("⚠️ 올바르지 않은 선택입니다. 다시 시도하세요.")

if __name__ == "__main__":
    main = RSAMain()
    main.main_run()
