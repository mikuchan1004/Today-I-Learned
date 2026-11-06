package var_02;

import java.util.Scanner;

public class Switch_05 {
	public static void main(String[] args) {
		
		/* ====================================================================
		 * 1. Scanner를 통한 사용자 키보드 입력 받기
		 * ====================================================================
		 * - Scanner scan = new Scanner(System.in);
		 *   콘솔 창에서 사용자가 키보드로 타이핑한 값을 읽어오는 객체
		 * - scan.nextInt() : 사용자가 입력한 정수(int)를 읽어서 변수 a에 저장
		 */
		System.out.println("숫자를 입력하세요:");
		Scanner scan = new Scanner(System.in);
		int a = scan.nextInt();
		System.out.println("a:" + a);
		
		
		/* ====================================================================
		 * 2. switch - case 문의 기본 구조와 break의 중요성
		 * ====================================================================
		 * - switch(변수) : 변수의 값과 일치하는 case 라벨로 바로 점프해서 실행해.
		 * - break; 의 역할:
		 *   switch 문 블록을 즉시 빠져나가라는 탈출 명령어!
		 *   ★ 만약 break가 없으면? 일치한 case 이후의 다른 case문들까지 조건 검사 없이
		 *     break를 만날 때까지 연달아 실행되어 버려 (이를 Fall-through 현상이라고 해).
		 *     (아래 코드에서 a가 1이면 case 1 출력 후 break가 없어서 case 2까지 출력됨!)
		 * - default : 일치하는 case가 하나도 없을 때 실행되는 기본 구간 (if문의 else와 같음).
		 */
		switch(a) {
			case 1 :
				System.out.println("a는 1이다");
				// break가 없으므로 아래 case 2로 흘러내려감!
			case 2 : 
				System.out.println("a는 2이다");
				break; // 여기서 비로소 switch문을 탈출
			default : 
				System.out.println("그 외");
		}
		
		
		/* ====================================================================
		 * 3. switch 조건식에 사용 가능한 자료형 vs 불가능한 자료형
		 * ====================================================================
		 * [사용 가능 O]
		 * - 정수형 : byte, short, char, int
		 * - 문자열 : String (자바 7부터 지원)
		 * - 기타   : Enum(열거형)
		 * 
		 * [사용 불가능 X]
		 * - 실수형 : float, double (부동소수점 오차 때문에 정확한 값 비교 불가)
		 * - 논리형 : boolean (참/거짓은 if문으로만 처리)
		 * - 큰정수 : long (switch의 점프 테이블 구조상 지원 안 함)
		 */
		// 사용 가능 : byte, char, short, int, String
		// 사용 불가능 : boolean, long, float, double
		
		
		/* ====================================================================
		 * 4. 여러 case를 묶어서 처리하기 (Fall-through의 유용한 활용)
		 * ====================================================================
		 * - 12, 1, 2월은 모두 겨울이므로 case들을 연달아 나열하고
		 *   마지막에만 출력문과 break를 배치하여 코드를 깔끔하게 압축할 수 있어.
		 */
		switch(a){
			case 12:
			case 1:
			case 2:
				System.out.println("겨울");
				break;
			case 3:
			case 4:
			case 5:
				System.out.println("봄");
				break;
		}
	}
}
