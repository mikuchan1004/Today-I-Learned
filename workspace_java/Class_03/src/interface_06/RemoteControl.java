package interface_06;

/**
 * [인터페이스 (Interface)]
 * - 개념: "모든 기기에서 공통으로 지켜야 할 표준 규격(버튼 목록)"
 * - 특징:
 *   1) 변수를 선언하면 무조건 '상수(public static final)'가 됩니다. (값 변경 불가)
 *   2) 메서드를 선언하면 기본적으로 '추상 메서드(public abstract)'가 됩니다. (틀만 제공)
 *   3) 자바 8부터는 default 키워드를 붙여 기본 동작을 가진 메서드도 작성 가능합니다.
 */
public interface RemoteControl {
	// [인터페이스의 상수]
	// 기본적으로 'public static final' 속성을 갖기 때문에 생략해도 똑같이 상수가 됩니다.
	public static final int 보증기간 = 3;
	
	// 'public static final'이 생략되어 있어도 자동으로 상수로 취급됩니다.
	String company = "휴먼전자";
	
	// [추상 메서드]
	// 이 리모컨 규격을 따르는 기기(TV, 선풍기 등)는 무조건 전원 켜기 기능을 만들어야 합니다.
	public abstract void powerOn();
	
	// 'public abstract'가 생략되어 있어도 자동으로 추상 메서드로 취급됩니다.
	void powerOff();
	
	// [디폴트 메서드 (Java 8+)]
	// 인터페이스지만 기본 구현(몸통 {})을 가질 수 있는 특별한 메서드입니다.
	// 기존 기기들을 고치지 않고도 새로운 공통 기능을 추가할 때 유용하게 쓰입니다.
//	void mic(String text);
	default void mic(String text) {
		System.out.println(text + "를 들었습니다.");
	}
}
