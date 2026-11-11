package webservice_07;

import java.util.List;

/**
 * [컨트롤러 (Controller)]
 * - 개념: "손님의 요청을 처음 받는 카운터 점원(중계자)"
 * - 흐름:
 *   1) 사용자가 요청(doGet)을 보냄.
 *   2) Service(요리사)를 불러 비즈니스 로직이 처리된 데이터(List)를 요청.
 *   3) 받은 데이터를 Jsp(플레이팅/화면 담당)에 넘겨서 완성된 HTML 화면을 받아옴.
 *   4) 최종 HTML 결과를 사용자(브라우저)에게 돌려줌.
 */
public class EmpController implements Servlet {

	@Override
	public String doGet() {
		
		// 1. 비즈니스 로직을 처리해줄 Service 호출
		EmpService empService = new EmpServiceImpl();
		List list = empService.getEmp(); // 3000 초과 사원 목록 수신

//		String html = "<div>name: SCOTT<div>";
		
		// 2. 받은 데이터를 화면(HTML)으로 예쁘게 렌더링하기 위해 JSP 호출
		Jsp jsp = new Jsp();
		String html = jsp.view(list);
		
		// 3. 만들어진 완성본 HTML 반환
		return html;
	}

	@Override
	public String doPost() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String doPut() {
		// TODO Auto-generated method stub
		return null;
	}

	@Override
	public String doDelete() {
		// TODO Auto-generated method stub
		return null;
	}
	
}
