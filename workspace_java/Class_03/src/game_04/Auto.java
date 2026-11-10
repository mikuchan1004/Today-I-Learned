package game_04;

/**
 * [Auto 클래스 - 챔피언 매크로 자동 실행 시스템 (다형성과 다운캐스팅의 핵심)]
 * 
 * 💡 핵심 개념:
 * 1. 매개변수의 다형성 (Polymorphism):
 *    - run(Champ champ): 매개변수의 타입이 부모인 'Champ'입니다.
 *    - 부모 타입 그릇 하나만 만들어 두면, 자식 객체인 Jax든 VI든 어떤 챔피언이 들어와도 다 받아낼 수 있습니다!
 *    - (만약 다형성이 없다면 run(Jax jax), run(VI vi) 등 챔피언 종류마다 메서드를 수십 개씩 따로 만들어야 합니다.)
 * 
 * 2. 동적 바인딩 (Dynamic Method Binding):
 *    - 'champ.move()'를 실행할 때, 겉보기 타입은 부모인 Champ이지만,
 *      자바는 메모리에 실제로 들어있는 진짜 알맹이(Jax인지 VI인지)를 스스로 찾아가서
 *      오버라이딩된 각자의 전용 move() 메서드를 똑똑하게 실행해줍니다.
 * 
 * 3. instanceof 연산자와 다운캐스팅 (Downcasting):
 *    - 부모 타입(Champ) 상태에서는 바이(VI)만의 고유 기능인 '징크스랑놀기()'가 보이지 않습니다.
 *    - 따라서 'champ instanceof VI'로 "너 진짜 바이 맞니?"라고 먼저 안전하게 확인한 뒤,
 *    - '(VI)champ'처럼 자식 타입으로 형태를 되돌려(다운캐스팅) 고유 기능을 실행합니다.
 *    - ※ 잭스(Jax)에게 억지로 바이 행세를 시키면 에러(ClassCastException)가 나므로 instanceof 검사가 필수입니다.
 */
public class Auto {
	
	/**
	 * 어떤 챔피언이든 전달받아서 공격, 이동, 스킬, 귀환을 자동으로 순차 실행하는 매크로 메서드
	 * @param champ 챔피언 객체 (Champ를 상속받은 모든 자식 챔피언 가능)
	 */
	void run(Champ champ) {
		// [공통 동작 실행]
		// 부모 Champ 규격에 있는 동작들이 차례대로 실행됩니다.
		champ.attack();    // 기본 공격
		champ.move();      // 💡 동적 바인딩: 들어온 챔피언(Jax/VI)의 오버라이딩된 대사가 각각 출력됨!
		champ.skill("F");  // 점멸 사용
		champ.skill("R");  // 궁극기 사용
		champ.recall();    // 귀환
		
		// [특정 챔피언 전용 고유 동작 처리 (다운캐스팅)]
		// 만약 지금 들어온 champ 객체의 실제 정체가 'VI(바이)'라면?
		if(champ instanceof VI) {			
			// Champ 타입 그릇을 VI 타입 그릇으로 안전하게 형변환(다운캐스팅)
			VI vi = (VI)champ;
			
			// 이제 바이만의 고유 메서드를 호출할 수 있게 됩니다!
			vi.징크스랑놀기();
		}
	}
}