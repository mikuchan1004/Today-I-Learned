package interface_06;

/**
 * [TV 클래스 - 단일 상속과 다중 인터페이스 구현]
 * - extends Display: Display 클래스를 1개 상속받음 (클래스는 단일 상속만 가능)
 * - implements RemoteControl, OTT: 리모컨과 OTT 인터페이스 2개를 동시에 장착 (인터페이스는 다중 구현 가능)
 * - 결과적으로 RemoteControl의 powerOn/powerOff와 OTT의 netflix를 모두 완성(@Override)해야 합니다.
 */
public class Tv extends Display implements RemoteControl, OTT {

	// RemoteControl 인터페이스의 전원 켜기 규격 완성
	@Override
	public void powerOn() {
		System.out.println("TV 켜기");
	}

	// RemoteControl 인터페이스의 전원 끄기 규격 완성
	@Override
	public void powerOff() {
		System.out.println("TV 끄기");
	}
	
	// OTT 인터페이스의 넷플릭스 규격 완성
	@Override
	public void netflix() {
		System.out.println("넷플릭스 시청하기");
	}
	
}
