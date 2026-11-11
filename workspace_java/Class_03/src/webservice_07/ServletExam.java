package webservice_07;

/**
 * [서블릿 실행 테스트 (웹 서비스 시뮬레이션)]
 * - 브라우저가 서버에 "사원 목록 화면 주세요(doGet)"라고 요청하는 과정을 시뮬레이션합니다.
 */
public class ServletExam {

	public static void main(String[] args) {
		
		// 1. 서블릿 규격을 만족하는 컨트롤러 객체 생성 (다형성 활용)
		Servlet s = new EmpController();
		
		// 2. 조회 요청(doGet) 호출
		// -> 내부적으로 Controller -> Service -> DAO -> Jsp 를 거쳐 최종 HTML이 생성되어 돌아옵니다.
		String html = s.doGet();
		
		// 3. 브라우저가 받게 될 최종 HTML 화면 출력
		System.out.println(html);

	}

}
