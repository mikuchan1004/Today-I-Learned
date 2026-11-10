package class_01;

/**
 * ============================================================================
 * [StudentExam.java - 같은 패키지 내 클래스 참조 및 객체 생성]
 * ============================================================================
 * 
 * 1. 패키지(Package)와 import 규칙
 *    - 같은 패키지(package class_01;) 안에 있는 클래스들은 
 *      별도의 'import' 문을 쓰지 않아도 서로를 자유롭게 인식하고 객체(인스턴스)를 생성할 수 있습니다.
 *    - 따라서 Student.java 파일에 정의된 'public class Student'뿐만 아니라,
 *      default 접근 제한자를 가진 'class Teacher' 역시 동일 패키지이므로 아무런 문제 없이 생성 가능합니다.
 */
public class StudentExam {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		// -------------------------------------------------------------
		// 1. Student 객체 생성
		// -------------------------------------------------------------
		// Student.java의 public class Student 객체 생성
		Student s1 = new Student();
		
		// -------------------------------------------------------------
		// 2. Teacher 객체 생성
		// -------------------------------------------------------------
		// Student.java 파일 안에 함께 선언되어 있던 class Teacher 객체 생성
		// 동일한 'class_01' 패키지에 속해 있으므로 정상적으로 인식됩니다.
		Teacher t1 = new Teacher();
	}

}
