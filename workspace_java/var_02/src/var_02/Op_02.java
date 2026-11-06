package var_02;

public class Op_02 {
	public static void main(String[] args) {
		// 1. 증감 연산자 (전위 vs 후위)
		int x = 10;
		x++; // 후위 증가: 다음 라인으로 넘어가며 x는 11이 됨
		System.out.println("x:" + x); // 11
		
		++x; // 전위 증가: x는 12가 됨
		System.out.println("x:" + x); // 12
		
		x = 10;
		int y = ++x; // 전위 연산: x를 먼저 1 증가(11)시킨 후 y에 대입
		System.out.println("y:" + y); // 11 
		
		x = 10;
		y = x++; // 후위 연산: 현재 x(10)를 y에 먼저 대입한 뒤, x가 1 증가(11)
		System.out.println("y:" + y); // 10
		System.out.println("x:" + x); // 11
		
		// 2. 복합 증감 연산 분석
		x = 10;
		// x++(평가값 10, 이후 x는 11) + ++x(x를 12로 증가시킨 후 평가값 12) = 10 + 12 = 22
		y = x++ + ++x;
		System.out.println(y);
		
		x = 10;
		// x++(10, x=11) * --x(10, x=10) / ++x(11, x=11) - x--(11, x=10)
		// 연산 우선순위(*, / 먼저 -> - 나중):
		// 1) 10 * 10 = 100
		// 2) 100 / 11 = 9 (정수 나눗셈)
		// 3) 9 - 11 = -2
		y = x++ * --x / ++x - x--;
		System.out.println("x:" + x + ", y:" + y); // x:10, y:-2
		
		x = 10;
		// 괄호 우선: (--x / ++x) -> (9 / 10 = 0)
		// x++(10, x=11) + 0 - x--(11, x=10) -> 10 + 0 - 11 = -1
		y = x++ + (--x / ++x) - x--;
		System.out.println("x:" + x + ", y:" + y); // x:10, y:-1
		
		x = 0;
		// 출력 시점에는 현재 값을 찍고, 직후에 1씩 증가
		System.out.println(x++); // 0 출력 (x=1)
		System.out.println(x++); // 1 출력 (x=2)
		System.out.println(x++); // 2 출력 (x=3)
		
		// 3. 산술 연산 및 나머지 연산자(%)
		double a = 7.3;
		int b = 2; 
		System.out.println(a / b); // 실수가 포함되었으므로 실수 나눗셈(3.65)
		
		System.out.println(10 % 3); // 나머지 연산: 10을 3으로 나눈 나머지(1)
		
		// [기습 문제] 특정 자리수 추출
		int c = 149;
		// 149 / 10 == 14 (1의 자리를 잘라냄)
		// 14 % 10 == 4   (10의 자리만 추출)
		System.out.println("10의 자리: " + (c / 10 % 10));
		
		// 4. 부동소수점 정밀도 한계 (근사치 저장)
		float d = 0.1f;
		double e = 0.1;
		boolean f = d == e; // float(32비트)과 double(64비트)의 이진수 근사치 정밀도가 달라 false
		System.out.println(f);
		
		// 5. 문자열 비교 주의점
		String s1 = "s1";
		String s2 = "s1";
		// 문자열 내용(값) 비교는 '=='(주소 비교) 대신 반드시 equals() 메서드를 사용해야 함
		System.out.println(s1.equals(s2));
		System.out.println("abcd".equals(s2));
		
		// [문제 2] 할인율 계산
		// 정가 120만원의 15% 할인가 계산
		int rtx5060 = 1200000;
		double sale = 0.15;
		double price = rtx5060 - rtx5060 * sale; // 또는 rtx5060 * (1 - sale)
		System.out.println(price);
		
		// [문제 3] 서식 지정자를 이용한 소수점 제한 출력
		double v1 = 1000;
		double v2 = 794.0;
		double re = v1 / v2; // 1.2594458...
		// %.3f : 부동소수점 실수를 소수점 이하 3번째 자리까지만 반올림하여 출력
		System.out.printf("결과 : %.3f\n", re);
		
		// 6. 삼항(조건) 연산자 -> 조건식 ? 참일_때_값 : 거짓일_때_값
		int score = 85;
		String grade = (score >= 90) ? "A학점" : "B학점";
		System.out.println(grade);
		
		// [문제 4] 다중 조건 분기 (중첩 삼항 연산자)
		// 90 이상: A, 80 이상: B, 그 외: C
		// 90점 미만인 경우(false 분기)에 다시 (score >= 80) 조건을 검사하는 체인 구조
		String upgrade = (score >= 90) ? "A학점" : ((score >= 80) ? "B학점" : "C학점");
		System.out.println("최종 등급: " + upgrade);
	}
}