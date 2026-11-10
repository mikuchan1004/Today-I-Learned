package Override_03;

import melon_02.Song; // melon_02 패키지에 만들어둔 Song 클래스를 벨소리로 활용하기 위해 불러옴(import)

/**
 * [Phone 클래스 - 기본 전화기 (부모 클래스 / Super Class)]
 * 
 * 💡 핵심 개념:
 * 1. 상속의 부모 클래스:
 *    - 일반 전화기(Phone)는 전화 걸기, 받기, 문자 보내기, 벨소리 울리기 등 가장 기본적인 통신 기능을 가집니다.
 *    - 나중에 스마트폰(SmartPhone)이 이 Phone 클래스를 상속(extends)받아 기능을 물려받게 됩니다.
 * 2. final 키워드:
 *    - 'final'이 붙은 변수는 한 번 값이 정해지면 절대 수정할 수 없는 상수(읽기 전용)가 됩니다.
 *    - 전화기 번호(number)는 개통 시 결정되면 기기 자체에서 임의로 바꿀 수 없도록 보호합니다.
 * 3. 캡슐화와 Getter / Setter:
 *    - private으로 보호된 변수(power, ring)는 외부에서 직접 접근할 수 없으므로,
 *      안전한 통로인 Getter(읽기)와 Setter(쓰기) 메서드를 통해 다룹니다.
 */
public class Phone {
	
	// ==========================================
	// 1. 필드(Field) : 전화기의 속성
	// ==========================================
	final String number;   // 내 전화번호 (final: 개통 후 번호 변경 불가)
	private boolean power; // 전원 상태 (true: 켜짐, false: 꺼짐) -> 외부 직접 변경 방지(private)
	private Song ring;     // 벨소리 (melon_02.Song 객체를 벨소리로 보관)
	
	// ==========================================
	// 2. 생성자(Constructor) : 전화기 개통 시 초기 상태 설정
	// ==========================================
	Phone(String number) {
		this.number = number;                          // 부여받은 전화번호 저장
		this.power = false;                            // 처음에는 전원이 꺼진 상태
		this.ring = new Song("기본벨" , "삼성");        // 초기 벨소리는 "삼성"의 "기본벨"로 장착
	}
	
	// ==========================================
	// 3. 메서드(Method) : 전화기의 통신 기능
	// ==========================================
	
	/**
	 * 전화 걸기 기능
	 * @param number 전화를 걸 상대방 번호
	 * @return true(통화 연결 성공), false(통화 연결 실패)
	 * 
	 * 💡 Math.random(): 0.0 ~ 1.0 사이의 난수를 생성하여 50% 확률로 통화 성공 여부를 시뮬레이션합니다.
	 */
	boolean call(String number) {
		if(Math.random() > 0.5) {
			System.out.println("전화 연결 성공 :" + number);
			return true;
		}else {
			System.out.println("전화 연결 실패 :" + number );
			return false;
		}
		
	} 
	
	/**
	 * 전화 받기 기능
	 */
	void receive() {
		System.out.println("누구세요?");
	}
	
	/**
	 * 문자 메시지 전송 기능
	 * @param number 받는 사람 번호
	 * @param text   보낼 내용
	 */
	void message(String number, String text) {
		System.out.println(number + "번호로" + text + "라고 보냈습니다.");
	}
	
	/**
	 * 전화벨 울리기 기능
	 * 현재 설정된 벨소리(Song) 객체의 play() 메서드를 호출하여 재생합니다.
	 */
	void ring() {
		// 전화벨 출력
		this.ring.play();
	}
	
	/**
	 * 벨소리 변경 기능
	 * @param song 새로 설정할 Song 객체
	 */
	void ringtone(Song song) {
		// 전화벨 교체
		this.ring = song;
	}

	// ==========================================
	// 4. Getter / Setter : 은닉된 private 필드를 안전하게 다루는 통로
	// ==========================================
	
	// 전원 켜짐/꺼짐 상태 확인
	public boolean isPower() {
		return power;
	}

	// 전원 켜기/끄기 설정
	public void setPower(boolean power) {
		this.power = power;
	}

	// 현재 설정된 벨소리 객체 조회
	public Song getRing() {
		return ring;
	}

	// 벨소리 교체
	public void setRing(Song ring) {
		this.ring = ring;
	}

	// 전화번호 조회 (final 변수이므로 setNumber는 없고 getNumber만 존재)
	public String getNumber() {
		return number;
	}	
	
}
