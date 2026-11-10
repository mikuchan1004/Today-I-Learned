package game_04;

/**
 * [Jax 클래스 - 챔피언 '잭스' (Champ를 상속받은 자식 클래스)]
 * 
 * 💡 핵심 개념:
 * 1. extends Champ:
 *    - Champ 부모 클래스를 상속받았기 때문에, attack(), skill(), recall() 코드를
 *      직접 작성하지 않아도 그대로 사용할 수 있습니다.
 * 2. 메서드 오버라이딩:
 *    - 부모의 심심한 move() ("이동 합니다.") 대신,
 *      잭스만의 개성 넘치는 대사를 출력하도록 move() 메서드를 재정의했습니다.
 */
public class Jax extends Champ {
	
	/**
	 * [오버라이딩] 잭스만의 이동 동작
	 * 부모의 "이동 합니다." 대신 잭스 고유의 대사를 출력합니다.
	 */
	@Override
	void move() {
		System.out.println("잭스 온더 비치! 외치면서 바다로 이동");
	}
}
