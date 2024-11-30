import sys,  os

def get_plaintext():
    """
    If there is already plain text, 
    the path is specified. 
    If not, the plain text is entered directly.
    """
    yesorno = input("✏️  평문을 가져오겠습니까? [y/n]: ")
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
        """
        텍스트를 연속으로 입력받는 부분.
        'END'를 단독으로 입력해야 종료.
        """
        print("\n여러 단락을 입력하세요. 입력을 종료하려면 'END'를 단독으로 입력하세요.")
        print("✏️ 평문을 입력하세요: ")
        Msg = ""  # 빈 텍스트
        for line in sys.stdin:
            if line.strip() == 'END':  # 'END'를 단독으로 입력해야 종료
                break
            Msg += line
    return Msg