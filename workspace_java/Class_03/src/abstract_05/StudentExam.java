package abstract_05;

/**
 * [추상 클래스 실행 및 다형성 실습]
 */
public class StudentExam {

	public static void main(String[] args) {
		// [1] 추상 클래스는 직접 객체 생성 불가
		// Student는 미완성 설계도이므로 new로 만들 수 없습니다. (컴파일 에러 발생)
//		Student student = new Student();
		
		// [2] 추상 클래스를 상속받아 완성한 자식 클래스는 new로 생성 가능!
		// Sangwoo 객체를 만들면, 먼저 부모(Student) 생성자가 실행된 뒤 상우가 만들어집니다.
		Sangwoo sangwoo = new Sangwoo();
		
		// 부모로부터 물려받은 일반 메서드 호출
		sangwoo.eat();
		
		// 상우가 직접 완성(@Override)한 추상 메서드 호출
		sangwoo.study();
		
		// [3] 다형성 (Polymorphism)
		// "상우는 학생이다"가 성립하므로,
		// 자식 객체(sangwoo)를 부모 타입(Student) 변수에 담을 수 있습니다.
		Student s = sangwoo;

	}

}
