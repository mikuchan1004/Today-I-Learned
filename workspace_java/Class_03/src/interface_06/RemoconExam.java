package interface_06;

/**
 * [인터페이스 다형성(Polymorphism) 실습]
 */
public class RemoconExam {

	public static void main(String[] args) {
		
		// 1. Tv 본체 객체 생성
		Tv tv = new Tv();
		tv.powerOn(); // TV 켜기
		
		// 2. 인터페이스 타입으로 변환 (다형성)
		// "TV는 리모컨으로 제어할 수 있는 기기(RemoteControl)이다" -> 성립
		// rc 변수를 통해서는 RemoteControl에 정의된 버튼(기능)들만 쓸 수 있습니다.
		RemoteControl rc = tv;
		
		// 3. 또 다른 인터페이스 타입으로 변환
		// "TV는 OTT 기기이다" -> 성립
		// ott 변수를 통해서는 OTT에 정의된 netflix() 기능만 볼 수 있습니다.
		OTT ott = tv;

	}

}
