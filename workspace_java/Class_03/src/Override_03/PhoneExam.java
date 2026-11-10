package Override_03;

import melon_02.Song; // 벨소리로 사용할 Song 클래스 임포트

/**
 * [PhoneExam 실행 클래스 - 일반 전화기와 스마트폰의 동작 및 상속 관계 실습]
 * 
 * 💡 핵심 흐름:
 * 1. 일반 Phone 객체(phone1, phone2) 생성 및 통화 시뮬레이션
 * 2. 외부 Song 객체를 생성하여 phone1의 벨소리 교체 (ringtone)
 * 3. 자식 클래스인 SmartPhone 객체(s1, s2) 생성
 *    - 부모의 기능인 call(), ring(), receive()가 그대로 동작함을 확인
 *    - 오버라이딩된 message() 메서드가 실행되는 것을 확인
 *    - 스마트폰만의 고유 메서드인 search() 실행 확인
 */
public class PhoneExam {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		// ==========================================
		// 1. 일반 전화기(Phone) 객체 생성 및 테스트
		// ==========================================
		Phone phone1 = new Phone("010-1234-5678");
		Phone phone2 = new Phone("010-5674-3214");
		
		// phone1 전원 켜기
		phone1.setPower(true);
		
		// phone1의 벨소리 바꾸기 (Song 객체를 새로 만들어 ringtone 메서드로 전달)
		Song song = new Song("링마벨", "다듀");
		phone1.ringtone(song);

		// phone2 전원 켜기
		phone2.setPower(true);

		// phone2가 phone1의 번호(phone1.getNumber())로 전화를 검 (50% 확률 성공)
		if (phone2.call(phone1.getNumber())) {
			phone1.ring();    // 연결 성공 시 phone1의 벨소리 울림 ("링마벨을 재생합니다.")
			phone1.receive(); // 전화 받음 ("누구세요?")
		}
		
		// ==========================================
		// 2. 스마트폰(SmartPhone) 객체 생성 및 상속/오버라이딩 테스트
		// ==========================================
		// SmartPhone 객체 생성 시 생성자 내부에서 super()가 호출되고 전화번호와 기본벨이 울림
		SmartPhone s1 = new SmartPhone("010");
		SmartPhone s2 = new SmartPhone("011");
		
		// [상속의 장점] SmartPhone에는 call(), ring(), receive()를 직접 구현하지 않았지만
		// 부모(Phone)로부터 물려받았기 때문에 그대로 사용 가능!
		if (s2.call(s1.getNumber())) {
			s1.ring();
			s1.receive();
		}
		
		// [오버라이딩 확인] SmartPhone에서 재정의한 message()가 실행됨
		s1.message(s2.getNumber() , " 자니? ");
		
		// [고유 기능 확인] SmartPhone에만 존재하는 인터넷 검색 기능 실행
		s1.search("검색");
	}

}
