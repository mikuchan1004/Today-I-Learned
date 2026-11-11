package try_08;

import java.io.FileInputStream;
import java.io.IOException;

/**
 * [예외 처리 (Exception Handling)]
 * - 개념: "프로그램 실행 중 예기치 못한 사고(에러)가 터졌을 때 프로그램이 비정상 종료되지 않게 막아주는 에어백/안전장치"
 * - try: 에러가 발생할 가능성이 있는 코드 작성
 * - catch: 실제로 에러가 발생했을 때 수습(처리)하는 코드 작성
 * - finally: 에러가 나든 안 나든 무조건 마지막에 반드시 실행되는 뒷정리 코드 작성
 */
public class TryExam {

	// main 메서드 뒤의 'throws Exception'은 혹시 처리되지 않은 에러가 있다면 자바 가상머신(JVM)에 떠넘기겠다는 선언
	public static void main(String[] args) throws Exception {
		
		// -------------------------------------------------------------
		// [방식 1: 고전적인 try-catch-finally 자원 해제 방식]
		// -------------------------------------------------------------
		FileInputStream fis = null;
		
		try {
			// 파일 열기 시도 (만약 c:\test.txt 파일이 없으면 FileNotFoundException 발생)
			fis = new FileInputStream("c:\\test.txt");
			
		} catch(Exception e) {
			// 에러가 났을 때 빨간색으로 에러 추적 로그(어디서 왜 터졌는지)를 출력
			e.printStackTrace();
			
		} finally {
			// [뒷정리 영역]
			// 파일을 열었으면 컴퓨터 메모리와 OS 자원을 위해 반드시 닫아주어야(close) 합니다.
			// 에러가 나든 정상 실행되든 finally는 100% 실행됩니다.
			if(fis != null) {
				try {
					fis.close(); // 닫는 도중에도 에러가 날 수 있으므로 또 try-catch가 필요해서 코드가 지저분해짐
				} catch(IOException e) {
					e.printStackTrace();
				} catch(Exception e) {
					e.printStackTrace();
				}
			}
		}
		
		// -------------------------------------------------------------
		// [방식 2: 최신 자바의 try-with-resources 자동 자원 해제 문법 (Java 7+)]
		// -------------------------------------------------------------
		// try 뒤의 괄호() 안에 파일을 열어두면,
		// try 블록이 끝나는 순간 자바가 알아서 자동으로 close()를 호출해 줍니다! (finally 불필요, 매우 깔끔)
		try (
			FileInputStream fis2 = new FileInputStream("C:\\text.txt");
		) {
			System.out.println("뭔가 함");
		} catch (Exception e) {
			e.printStackTrace();
		}
		
		// -------------------------------------------------------------
		// [방식 3: 고의로 예외(에러)를 발생시키는 throw]
		// -------------------------------------------------------------
		// 특정 조건에서 개발자가 직접 의도적으로 에러를 터뜨려 흐름을 중단시킬 때 사용합니다.
		throw new Exception("내가 만든 에러");
		
	}

}
