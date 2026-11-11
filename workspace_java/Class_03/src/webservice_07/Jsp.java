package webservice_07;

import java.util.List;

/**
 * [JSP (JavaServer Pages / View 계층)]
 * - 개념: "사용자(브라우저)에게 보여줄 화면(HTML)을 예쁘게 플레이팅하는 역할"
 * - Controller로부터 순수 데이터(List)를 넘겨받아, 브라우저가 읽을 수 있는 HTML 태그 문자열로 조립합니다.
 */
public class Jsp {
	
	// 사원 번호 리스트를 받아 HTML 태그(<div>)로 감싸서 문자열로 만들어주는 메서드
	String view(List<Integer> list) {
		// 문자열을 빈번하게 합칠 때는 '+' 연산자보다 성능이 뛰어난 StringBuffer를 사용합니다.
		StringBuffer sb = new StringBuffer();
		
		// 향상된 for문(foreach)으로 리스트의 사원 번호를 하나씩 꺼내 HTML 태그로 조립
		for(int empno : list) {
			sb.append("<div>" + empno + "<div>\n");
		}
		
		// 조립이 끝난 StringBuffer를 일반 문자열(String)로 변환하여 반환
		String result = sb.toString();
		return result;
	}
}
