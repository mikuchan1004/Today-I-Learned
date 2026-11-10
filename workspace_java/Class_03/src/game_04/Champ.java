package game_04;

/**
 * [Champ 클래스 - 롤(LoL) 챔피언 공통 부모 클래스]
 * 
 * 💡 핵심 개념:
 * 1. 객체지향의 추상화 및 공통 규격:
 *    - 롤에 등장하는 모든 챔피언(바이, 잭스 등)은 겉모습이나 스킬은 달라도
 *      공통적으로 '공격(attack)', '이동(move)', '스킬 사용(skill)', '귀환(recall)'이라는 기본 행동을 공유합니다.
 *    - 이처럼 챔피언들의 공통된 특징을 묶어 부모 클래스(Champ)로 정의해두면,
 *      새로운 챔피언을 만들 때마다 기본 기능들을 처음부터 다시 만들 필요 없이 상속받아 확장할 수 있습니다.
 * 2. 다형성(Polymorphism)의 토대:
 *    - 모든 챔피언은 'Champ'라는 하나의 공통 타입으로 묶어서 다룰 수 있습니다.
 */
public class Champ {
	
	/**
	 * 기본 공격 동작
	 */
	void attack() {
		System.out.println("기본 공격 입니다.");
	}
	
	/**
	 * 기본 이동 동작
	 * (자식 클래스인 Jax나 VI에서 각자의 개성에 맞게 오버라이딩하여 재정의할 수 있습니다.)
	 */
	void move() {
		System.out.println("이동 합니다.");
	}
	
	/**
	 * 스킬 사용 동작
	 * @param key 누른 키보드 자판 ("R": 궁극기, "F": 스펠 점멸)
	 */
	void skill(String key) {
		if(key.equals("R")) {
			System.out.println("궁극기를 사용 합니다.");
		}else if(key.equals("F")) {
			System.out.println("점멸을 사용합니다.");
		}
	}
	
	/**
	 * 본진 귀환 동작
	 */
	void recall() {
		System.out.println("귀환 합니다.");
	}
}
