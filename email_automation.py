import csv
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# 1. .env 파일에서 안전하게 환경 변수 불러오기 (깃허브에는 안 올라감!)
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

def send_result_emails(csv_file_path):
    print("=== 📧 채용 결과 안내 개인화 메일 발송 시스템 (실제 발송 테스트) ===")
    
    if not SENDER_EMAIL or not SENDER_PASSWORD:
        print("🚨 오류: .env 파일에 이메일 정보가 세팅되지 않았습니다.")
        return

    success_count = 0
    
    try:
        # 2. SMTP 서버 연결 (네이버 기준)
        server = smtplib.SMTP('smtp.naver.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        # 3. 데이터 읽기 및 발송
        with open(csv_file_path, mode='r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                name = row['이름']
                email = row['이메일']
                result = row['결과'] 
                
                # 1. 합격/불합격에 따른 메일 제목 및 내용 분기 처리
                if result == '합격':
                    subject = f"[제로웍스] {name}님, 서류 전형 합격을 축하드립니다."
                    body = (
                        f"안녕하세요 {name}님,\n\n"
                        f"제로웍스 채용 전형에 지원해 주셔서 진심으로 감사드리며, 서류 전형 합격 소식을 전해드립니다. 축하합니다!\n\n"
                        f"보내주신 소중한 지원서를 통해 {name}님이 갖추신 훌륭한 역량과 잠재력을 확인할 수 있어 아주 기쁜 마음으로 다음 전형에 모시게 되었습니다.\n"
                        f"이어지는 면접 전형과 관련된 세부 일정 및 안내 사항은 빠른 시일 내에 별도로 안내해 드릴 예정입니다.\n\n"
                        f"다시 한번 제로웍스에 보여주신 관심에 깊이 감사드리며, 면접에서 뵙고 더 많은 이야기를 나눌 수 있기를 기대하겠습니다.\n\n"
                        f"감사합니다.\n\n"
                        f"제로웍스 경영지원팀 드림"
                    )
                else:
                    subject = f"[제로웍스] {name}님, 서류 전형 결과 안내의 건"
                    body = (
                        f"안녕하세요 {name}님,\n\n"
                        f"제로웍스 채용 전형에 지원해 주셔서 진심으로 감사드립니다.\n\n"
                        f"{name}님의 뛰어난 역량과 잠재력에도 불구하고, 제한된 채용 T/O와 내부 상황으로 인해 안타깝게도 이번 전형에서는 모시지 못하게 되었습니다.\n\n"
                        f"비록 이번 채용에서는 아쉬운 소식을 전하게 되었으나, 향후 더 좋은 기회로 다시 인사드릴 수 있기를 바랍니다.\n"
                        f"{name}님의 앞날에 늘 좋은 일만 가득하시기를 기원합니다.\n\n"
                        f"감사합니다.\n\n"
                        f"제로웍스 경영지원팀 드림"
                    )
                
                # 메일 객체 생성
                msg = MIMEMultipart()
                msg['From'] = SENDER_EMAIL
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'plain'))
                
                # 실제 메일 발송!
                server.send_message(msg)
                print(f"✅ [{result}] {name} ({email}) 님께 실제 메일 발송 완료!")
                
                success_count += 1
        
        # 발송 완료 후 서버 연결 안전하게 종료
        server.quit()
                
    except FileNotFoundError:
        print(f"🚨 오류: {csv_file_path} 파일을 찾을 수 없습니다.")
        return
    except smtplib.SMTPAuthenticationError:
        print("🚨 오류: 이메일 로그인 실패. '앱 비밀번호'를 사용했는지 확인해주세요.")
        return
    except Exception as e:
        print(f"🚨 메일 발송 중 오류 발생: {e}")
        return
        
    print(f"\n🎉 총 {success_count}명의 지원자에게 메일 발송이 완료되었습니다.")

# 코드 실행
if __name__ == "__main__":
    send_result_emails('applicants.csv')