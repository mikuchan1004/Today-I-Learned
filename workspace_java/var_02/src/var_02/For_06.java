package var_02;

public class For_06 {

	public static void main(String[] args) {
		
		// for문의 형식 
//		for (; ;) {
//			
//		}
		for (int i=0; i<10; i++) {
			System.out.println(i);
		}
		
		// 0부터 10까지 모두 더하시오
		int result = 0;
		for (int i=0; i<11; i++) {
			result += i;		
		}
		System.out.println(result);
		
		// 문제1 
		// 주사위 2개를 굴려서 
		// 나올 수 있는 모든 조합 출력
		for (int i=1; i<6; i++) {
			for (int j=1; j<6; j++) {
				System.out.println("나올 수 있는 모든 출력 :" + i + " " + j);
			}
		}
		
		// 문제2
		// 주사위 2개를 굴려서
		// 나올 수 있는 모든 조합을 
		// 합 별로 출력
		for (int k=2; k<=12; k++) {
			System.out.print(k + ":");
			for(int i=1; i<=6; i++) {
				for (int j=1; j<=6; j++) {
					if (i+j == k) {
						System.out.printf("[%d, %d]" , i, j);
					}
				}
			}
			System.out.println();
		}
		
		// 문제3
		// 주사위 2개를 굴려서
		// 나올 수 있는 모든 조합을 
		// 합 별로 출력
		// 단, 중복 없이
		for (int k=2; k<=12; k++) {
			System.out.print(k + ":");
			for(int i=1; i<=6; i++) {
				for (int j=1; j<=6; j++) {
					if (i+j == k && i <= j ) {
						System.out.printf("[%d, %d]" , i, j);
					}
				}
			}
			System.out.println();
		}
	}

}
