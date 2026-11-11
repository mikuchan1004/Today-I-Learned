package interface_06;

/**
 * [OTT 인터페이스]
 * - 넷플릭스 등 스트리밍 서비스 규격을 정의한 인터페이스입니다.
 * - 이 인터페이스를 장착한 기기는 netflix() 기능을 반드시 구현해야 합니다.
 */
public interface OTT {
	
	// public abstract 가 생략된 추상 메서드
	void netflix();
}
