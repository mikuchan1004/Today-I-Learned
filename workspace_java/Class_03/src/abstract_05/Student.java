package abstract_05;

import java.util.ArrayList;
import java.util.List;

/**
 * [추상 클래스 (Abstract Class)]
 * - 개념: "미완성 설계도" 또는 "공통 부모 전용 클래스"
 * - 특징:
 *   1) 내용이 덜 완성된 메서드(abstract 메서드)를 가질 수 있습니다.
 *   2) 미완성 설계도이므로 직접 물건(객체)을 찍어낼 수 없습니다. -> new Student() 불가능!
 *   3) 오직 다른 자식 클래스에게 '상속(extends)'되기 위해서만 존재합니다.
 */
public abstract class Student {
	
	// 학생이라면 공통으로 가질 수 있는 기술 목록 (필드/변수)
	List skills = new ArrayList();
	
	// [생성자]
	// 추상 클래스는 직접 new 할 수는 없지만,
	// 자식 클래스(Sangwoo 등)가 생성될 때 부모로서 먼저 호출되어 실행됩니다.
	Student() {
		System.out.println("Student 생성자 실행");
	}
	
	// [일반 메서드]
	// 모든 학생이 똑같이 행동하는 공통 기능은 부모가 미리 직접 만들어 둡니다.
	void eat() {
		System.out.println("우걱 우걱 밥 먹는다");
	}
	
	/**
	 * [추상 메서드 (Abstract Method)]
	 * - 개념: "이름만 있고 내용(실행 블록 {})은 없는 껍데기 메서드"
	 * - 특징:
	 *   1) 학생마다 공부하는 방식이 제각각이므로, 부모는 "공부하는 기능이 있어야 한다"는 틀만 잡습니다.
	 *   2) 자식 클래스에게 "너가 상속받아서 이 메서드의 실제 내용을 반드시 채워 넣어라!" 하고 강제(숙제)합니다.
	 *   3) 끝에 세미콜론(;)으로 끝납니다. (중괄호 {}가 있으면 에러 발생)
	 */
	abstract void study();
}
