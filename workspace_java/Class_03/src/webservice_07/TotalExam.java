package webservice_07;

import java.util.ArrayList;
import java.util.List;

/**
 * [통합 실습 (TotalExam)]
 * - 위에서 파일별로 분리했던 웹 서비스 구조(DAO -> Service -> JSP -> Controller)를
 *   하나의 main 메서드 안에 절차지향적으로 모아놓은 비교 분석용 코드입니다.
 * - 한곳에 모아보면 흐름은 한눈에 보이지만, 코드가 길어지고 유지보수가 어려워지기 때문에
 *   실무에서는 위의 파일들처럼 각 계층(역할)별로 분리해서 개발합니다.
 */
public class TotalExam {

	public static void main(String[] args) {
		
		// [1단계: DAO 영역]
		// 데이터베이스에서 원본 데이터를 조회해오는 부분
		List<Integer> list = new ArrayList<Integer>();
		list.add(1111);
		list.add(2222);
		list.add(3333);
		list.add(4444);
		list.add(5555);
		
		// [2단계: Service 영역]
		// 가져온 원본 데이터 중 비즈니스 규칙(3000 초과)에 맞는 데이터만 필터링/가공
		List<Integer> result = new ArrayList<Integer>();
		for(int i = 0; i < list.size(); i++) {
			if((int) list.get(i) > 3000) {
				result.add(list.get(i));
			}
		}
		
		// [3단계: JSP (View) 영역]
		// 가공된 순수 데이터를 사용자가 브라우저에서 볼 수 있도록 HTML 문자열로 조립
		StringBuffer sb = new StringBuffer();
		
		for(int empno : result) {
			sb.append("<div>" + empno + "<div>\n");
		}
		
		String html = sb.toString();
		
		// [4단계: Controller & ServletExam 영역]
		// 만들어진 최종 HTML 결과물을 화면(브라우저)에 출력
		System.out.println(html);

	}

}
