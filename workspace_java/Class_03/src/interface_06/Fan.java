package interface_06;

/**
 * [선풍기 클래스]
 * - RemoteControl 인터페이스를 단독으로 구현(implements)한 기기입니다.
 * - 리모컨 규격에 맞추어 선풍기 켜기/끄기 기능을 완성했습니다.
 */
public class Fan implements RemoteControl {

	// RemoteControl 규격 구현: 선풍기 켜기
	@Override
	public void powerOn() {
		System.out.println("선풍기 켜기");
	}

	// RemoteControl 규격 구현: 선풍기 끄기
	@Override
	public void powerOff() {
		System.out.println("선풍기 끄기");
	}

}
