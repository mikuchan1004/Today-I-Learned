package Override_03;

/**
 * [SmartPhone 클래스 - 스마트폰 (자식 클래스 / Sub Class)]
 * 
 * 💡 핵심 개념:
 * 1. 상속 (extends):
 *    - 'SmartPhone extends Phone'은 스마트폰이 일반 전화기(Phone)의 모든 기능(전화 걸기/받기/문자 등)을 물려받는다는 의미입니다.
 *    - 자바는 다중 상속을 금지하므로 '단 하나의 부모 클래스'만 상속받을 수 있습니다.
 *    - 부모의 private 요소는 은닉되어 있으므로 자식이라도 직접 접근할 수 없습니다.
 * 2. super 키워드:
 *    - super(number): 부모 클래스(Phone)의 생성자를 호출합니다. 자식 객체가 만들어질 때는 반드시 부모 생성자가 먼저 실행되어야 합니다.
 *    - super.메서드(): 부모가 가지고 있던 원래 메서드를 명시적으로 호출할 때 사용합니다.
 * 3. 메서드 오버라이딩 (Method Overriding / @Override):
 *    - 부모로부터 물려받은 메서드를 그대로 쓰지 않고, 자식 클래스에서 내용을 새롭게 '재정의'하여 덮어쓰는 기법입니다.
 *    - @Override 어노테이션은 부모의 메서드 시그니처와 정확히 일치하는지 컴파일러에게 검사해달라고 알리는 역할을 합니다.
 */
public class SmartPhone extends Phone {
	
	// ==========================================
	// 1. 생성자(Constructor) : 스마트폰 초기화
	// ==========================================
	SmartPhone(String number) {
		// [super(number)]
		// 부모 클래스(Phone)의 생성자 Phone(String number)를 호출하여 부모 영역을 먼저 초기화합니다.
		// 자식 생성자 맨 첫 줄에는 반드시 super(...)가 와야 합니다.
		super(number);
		
		// 부모에게 물려받은 필드(number)와 메서드(ring())를 내 것처럼 자유롭게 사용 가능
		System.out.println(this.number);
		ring();
		
		// 💡 주의: 부모의 private 변수(power)는 자식이라도 직접 꺼내 쓸 수 없습니다 (컴파일 에러 발생하므로 주석 처리됨).
		// 접근하려면 부모의 public 메서드인 isPower()나 setPower()를 거쳐야 합니다.
//		System.out.println(this.power);
	}
	
	// ==========================================
	// 2. 스마트폰만의 고유한 기능 추가 (확장)
	// ==========================================
	
	/**
	 * 앱 스토어 열기 기능 (스마트폰에만 있는 고유 기능)
	 */
	void openStore() {
		System.out.println("어플 목록이 나옵니다.");
	}
	
	/**
	 * 웹 검색 기능 (스마트폰에만 있는 고유 기능)
	 * @param keyword 검색어
	 * @return 가상의 검색 결과 웹페이지
	 */
	String search(String keyword) {
		System.out.println(keyword + "검색 중 입니다...");
		
		// 부모(Phone)의 원래 message 메서드를 호출하여 로그나 알림을 보냄
		super.message("1" , "text");
		
		return keyword + "검색 결과 페이지";
	}
	
	// ==========================================
	// 3. 부모 기능 재정의 (메서드 오버라이딩 / @Override)
	// ==========================================
	
	/**
	 * [메서드 오버라이딩]
	 * 부모(Phone)의 message 메서드를 스마트폰 방식(예: 메신저 앱 스타일)으로 덮어써서 재정의합니다.
	 */
	@Override
	void message(String number, String text) {
		// super.message()를 통해 부모(Phone)의 기존 문자 전송 로직도 함께 수행
		super.message("1" , "text");
		
		// 스마트폰만의 추가적인 동작(출력) 수행
		System.out.println("1" + text);
	}
}
