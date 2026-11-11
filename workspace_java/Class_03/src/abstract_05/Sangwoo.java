package abstract_05;

/**
 * [구체 클래스 (Concrete Class)]
 * - Student(추상 클래스)를 상속받은 자식 클래스입니다.
 * - 부모가 남겨둔 미완성 추상 메서드(study)를 반드시 구현(완성)해야만 에러가 나지 않습니다.
 */
public class Sangwoo extends Student {

	/**
	 * [@Override (재정의)]
	 * - 부모(Student)가 "공부해라(study)"라고 이름만 만들어둔 숙제를
	 *   상우만의 방식("오늘은 집중해야지...")으로 실제 내용을 채워 넣는 작업입니다.
	 */
	@Override
	void study() {
		System.out.println("오늘은 집중해야지...");
	}

}
