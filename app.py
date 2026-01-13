import requests
import urllib3
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# [설정] SSL 보안 경고 메시지 무시 (터미널이 지저분해지는 것 방지)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_safe_response(url, params=None):
    """
    웹/클라우드 환경에서 차단당하지 않고 데이터를 가져오는 안전한 함수
    """
    # 1. 사람인 척 위장하는 '주민등록증' (헤더)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/"
    }

    # 2. 연결이 끊기면 3번까지 다시 시도하는 설정
    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5) # 0.5초 간격으로 3번 재시도
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        # 3. 실제 데이터 요청 (verify=False로 보안 인증서 무시)
        response = session.get(
            url, 
            headers=headers, 
            params=params, 
            verify=False, 
            timeout=10 # 10초 넘게 응답 없으면 포기
        )
        response.raise_for_status() # 에러가 있는지 체크
        return response
    except Exception as e:
        # 에러 발생 시 내용을 출력해서 원인 파악
        print(f"❌ 연결 실패: {e}") 
        return None
