package var_02;

public class Var_01 {
	/**
	 * 자바 기본 문법: 변수, 기본 자료형(Primitive Type), 참조 자료형(String), 형변환(Casting)
	 * @param args
	 */
	public static void main(String[] args) {
		
		// 한 줄 주석: 슬래시 두 개 뒤의 내용은 컴파일러가 무시함
		/*
		 여러 줄 주석 
		 블록 단위로 긴 설명을 적을 때 사용
		 */
		
		// 1. 변수 선언 및 초기화
		int a; // 변수 선언: 메모리에 정수형 공간 할당
		a = 10; // 값 대입(초기화)
		
		int b = 20; // 선언과 동시에 초기화
		
		System.out.print(a); // 줄바꿈 없는 출력
		System.out.println(b); // 출력 후 줄바꿈
		
		System.out.println(a + ", " + b); // 문자열 연결 연산자(+)
		
		// 자바는 정적 타입 언어이므로 선언된 타입과 다른 타입을 대입하면 컴파일 에러 발생
//		b = 3.5; // 에러: int 변수에 실수를 대입할 수 없음
//		b = "a"; // 에러: int 변수에 문자열을 대입할 수 없음
		
		// 2. 문자형 (char) - 작은따옴표(''), 내부적으로 유니코드(정수)로 처리
		char c1 = 'A';
		System.out.println("c1:" + c1); // 'A'
		
		char c2 = 65; // ASCII/Unicode 65에 매핑된 문자 'A'
		System.out.println("c2:" + c2);
		
		char c3 = 65 + 3; // 68에 매핑된 문자 'D'
		System.out.println("c3:" + c3);
		
		// 3. 정수형 (long) - 4바이트(int) 범위를 초과하는 리터럴은 끝에 접미사 L(또는 l) 필수
		long l1 = 22000000000L;
		long l2 = 30; // int 범위 내의 값은 자동 형변환 대입
		
		// 4. 문자열 (String) - 큰따옴표("") 사용, 참조형(클래스) 타입
		String s1 = "최민수";
		System.out.println("s1:" + s1);
		
		// 이스케이프 문자(Escape Sequence)
		String s2 = "최\"민\"수"; // \": 문자열 내 큰따옴표 표현
		System.out.println("s2:" + s2);
		
		String s3 = "최\n민수"; // \n: 줄바꿈
		System.out.println("s3:" + s3);
		
		// 5. 문자열 연결 연산과 사칙연산 우선순위
		System.out.println("글씨" + 3);       // "글씨3" (문자열 + 숫자 -> 문자열 결합)
		System.out.println("글씨" + 3 + 2);   // "글씨32" (왼쪽부터 차례대로 문자열 결합)
		System.out.println("글씨" + (3 + 2)); // "글씨5" (괄호 안의 덧셈이 먼저 수행됨)
		System.out.println("글씨" + 3 * 2);   // "글씨6" (곱셈(*)이 덧셈(+)보다 우선순위가 높음)
		System.out.println(2 + 3 + "글씨");   // "5글씨" (왼쪽 정수 덧셈 후 문자열과 결합)
		
		// 6. 실수형 (float, double)
		float f1 = 3.14f; // float 리터럴은 접미사 f(또는 F) 필수 (기본 실수는 double로 인식)
		double d1 = 3.14; // 실수의 기본 타입(8바이트)
		
		// 7. 논리형 (boolean) - true 또는 false
		boolean stop = true;
		boolean start = false;
		
		System.out.println("stop:" + stop);

		// [문제 1] 내 나이를 저장하고 출력하시오.
		int age;
		age = 28;
		System.out.println(">>>>>>>>>>");
		System.out.println("age:" + age);
		
		// [문제 2] 운전면허가 있다 없다를 저장하고 출력하시오 
		boolean driver_license = true;
		System.out.println(">>>>>>>>>>");
		System.out.println("driver_license:" + driver_license);
 		
		// [문제 3] 1평은 3.3 제곱미터다. 5평이 몇 제곱미터인지 계산해서 저장하고 출력하시오
		double square_meter = 3.3; // 1평당 제곱미터
		int square_footage = 5;    // 평수
		double answer = square_meter * square_footage;
		System.out.println(">>>>>>>>>>");
		System.out.println("5평을 제곱미터로 환산하면:" + answer);
				
		// [문제 4] 두 변수 x, y에 각자 숫자를 넣고 출력 결과 : "3 > 4의 결과는 false 입니다."
		int x = 3; 
		int y = 4; 
		boolean result = x > y; // 관계 연산자(비교 연산)의 결과는 boolean
		System.out.println(">>>>>>>>>>");
		System.out.println(x + " > " + y + "의 결과는 " + result + " 입니다.");
		
		// [문제 5] 회식비 분할 계산
		// 5-1 : 원 단위까지 출력 
		// 5-2 : 만원 단위까지만 출력
		// 5-3 : 나머지는 주최자가 낸다. 그럼 주최자가 낼 돈은?
		int total = 78500;
		int members = 3;
		int member = total / members; // 정수 간 나눗셈은 소수점이 버려짐 (몫만 취함)
		System.out.println(">>>>>>>>>>");
		System.out.println("인 당 얼마? : " + member + " 원"); 
		
		// 만원 단위 절사: 10000으로 나누어 정수 몫만 남긴 후 다시 10000을 곱함
		int money1 = (member / 10000) * 10000;
		System.out.println("인 당 얼마?(만원 단위) : " + money1 + " 원"); 
		
		// 전체 금액에서 나머지 인원들이 낸 만원 단위 금액을 뺀 나머지
		int money2 = total - (money1 * (members - 1));
		System.out.println("주최자가 낼 돈 : " + money2 + " 원"); 

		// [문제 6] 두 변수의 값 교환 (Swap 알고리즘)
		String left = "국밥";
		String right = "돈까스";
		
		// 임시 변수 temp를 활용해 값을 보관 후 맞바꿈
		String temp = left;
		left = right;
		right = temp;
		
		System.out.println("left:" + left);   // 돈까스
		System.out.println("right:" + right); // 국밥
		
		// 8. 형변환 (타입 변환, Type Casting)
		int i1 = 10;
		long i2 = (long)i1; // 자동 형변환(Promotion): 작은 타입 -> 큰 타입 (명시적 캐스팅 생략 가능)
		i2 = i1; 
		
		i1 = (int)i2; // 강제 형변환(Casting): 큰 타입 -> 작은 타입 (데이터 손실 가능성 명시)
		
		i2 = 2200000000L;
		i1 = (int)i2; // int의 표현 범위(약 21억)를 초과하여 오버플로우 발생 -> 엉뚱한 음수 출력
		System.out.println("i1:" + i1);
		
		float ff1 = 1.23f;
		double ff2 = ff1;    // 자동 형변환 (float -> double)
		ff1 = (float)ff2;   // 강제 형변환 (double -> float)
		
		int i3 = 2100000000;
		int i4 = i3 * 3; // int 범위 초과로 인한 정수 오버플로우 발생
		System.out.println(i4);
		
		int i5 = 10;
		double i6 = i5; // 자동 형변환 (10 -> 10.0)
		System.out.println("i6:" + i6);
		
		// 정수 나눗셈 주의점
		int i7 = 33;
		int i8 = 10;
		double i9 = i7 / i8; // 정수/정수 연산이 먼저 수행되어 3이 된 후 double(3.0)로 변환됨
		System.out.println("i9:" + i9);
		
		double d2 = 10 / 4; // 10 / 4 = 2 -> 2.0으로 저장
		System.out.println("d2:" + d2);
		
		double d3 = 10.0 / 4; // 피연산자 중 하나가 실수면 실수 연산 수행 -> 2.5
		System.out.println("d3:" + d3);
		
		double d4 = (double)10 / 4; // 한쪽을 double로 강제 형변환하여 실수 연산 유도 -> 2.5
		
		// 9. 문자열 파싱 (String -> int)
		String s4 = "123";
//		int ii1 = (int)s4; // 기본형과 참조형 간에는 직접 캐스팅 불가
		int ii1 = Integer.parseInt(s4); // Wrapper 클래스의 parseInt 메서드를 이용해 숫자로 변환

		// 10. 진법 표현 (16진수 접두사 0x)
		int ii2 = 0xF; // 16진수 F = 10진수 15
		System.out.println("ii2: " + ii2);
	}
}