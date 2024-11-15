import sys, os
from Cipher import DecryptionManager, EncryptionManager
from Key import KeyManager

class Hill:
    def __init__(self, alpha, key_manager : KeyManager):
        """Initilaize"""
        self.alpha = alpha
        self.modnum = len(self.alpha)
        self.key_manager = key_manager

    def MainRun(self):
        """옵션 번호 입력"""
        while True:
            print(" " * 15 + "🔐 옵션 🔐")
            print("✏️  1. 암호화")
            print("📜  2. 복호화")
            print("🔚  3. 종료")
            self.num = int(input("번호 입력: "))
            if self.num == 1: # 암호화
                # 프로그램 시작 메시지
                print(" " * 10 + f"🛡️  Hill 암호화 프로그램 시작  🛡️")
                self.ENrun()
            elif self.num == 2: # 복호화
                # 프로그램 시작 메시지
                print(" " * 10 + f"🛡️  Hill 복호화 프로그램 시작  🛡️")
                self.DENrun()
            elif self.num == 3: # 종료
                # 프로그램 종료 메시지
                print(" " * 15 + "프로그램을 종료합니다.")
                break    
            
    def input_lines(self):
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
    
    def ENrun(self):
        yesorno = input("✏️ 평문을 가져오겠습니까? [y/n]: ")
        if yesorno.lower() == "y":
            filepath = input("📂 파일경로 입력하세요:")
            while not os.path.exists(filepath):     
                print("❌ 존재하지 않는 파일 경로입니다.")   
                filepath = input("📂 파일경로 입력하세요:")
            with open(filepath, 'r', encoding='utf-8') as file:
                self.Text = file.read()
        else:
            self.Text = self.input_lines()
        # 텍스트를 입력 받아서 암호화
        self.Text = self.Text.replace('’', '\'').replace('‘', '\'').replace('”', '\"').replace('“', '\"') 
        keys, keys_len = self.key_manager.input_key(len(self.Text))
        self.key_manager.Check_key(keys, self.modnum) # 텍스트의 길이 
        self.encryption_manager = EncryptionManager(alpha, keys, keys_len)
        cipher_text = self.encryption_manager.encrypt(self.Text) 
        print(f"📜 암호화된 결과: \n{cipher_text}") 
        # 'w'는 텍스트 쓰기 모드
        with open(f'MyCipher.txt', 'w') as f:  
            # pickle 대신 write() 사용
            f.write(cipher_text)  

    def DENrun(self):
        yesorno = input("✏️ 암호문을 가져오겠습니까? [y/n]: ")
        if yesorno.lower() == "y":
            # 'wb'는 바이너리 읽기 모드
            with open(f'MyCipher.txt', 'r') as f:  
                self.Text = f.read()
        else:
            self.Text = self.input_lines()
        # 텍스트를 입력 받아서 복호화 
        self.Text = self.Text.replace('’', '\'').replace('‘', '\'').replace('”', '\"').replace('“', '\"') 
        keys, keys_len = self.key_manager.input_key(len(self.Text))
        self.decryption_manager = DecryptionManager(alpha, keys, keys_len)
        plainText = self.decryption_manager.decrypt(self.Text) 
        print(f"📜 복호화된 결과: \n{plainText}") 
        if os.path.exists("./MyKeys.pkl"):
            os.remove("./MyKeys.pkl")
         
if __name__=="__main__":
    alpha = f'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz,.<>/?:;\'\"=+-_()*&^%$#@!~`|1234567890' 
    key_manager = KeyManager()
    hill = Hill(alpha, key_manager)
    hill.MainRun()