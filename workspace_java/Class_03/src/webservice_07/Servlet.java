package webservice_07;

/**
 * [서블릿(Servlet) 인터페이스 - 웹 요청 규격]
 * - 웹 브라우저에서 서버로 들어오는 대표적인 HTTP 요청 방식 4가지를 정의한 규격입니다.
 *   1) doGet: 데이터 조회/가져오기 (Read)
 *   2) doPost: 새로운 데이터 등록/생성 (Create)
 *   3) doPut: 기존 데이터 수정 (Update)
 *   4) doDelete: 데이터 삭제 (Delete)
 */
public interface Servlet {
	String doGet();
	String doPost();
	String doPut();
	String doDelete();
}
