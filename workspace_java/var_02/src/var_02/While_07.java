package var_02;

public class While_07 {

	public static void main(String[] args) {
		
		//while 기본형
		int i = 3;
		while(i < 10) {
			System.out.println(i);
			i++;
		}
		
		do {
			System.out.println(i);
			i++;
		}while(i < 10);
		
		System.out.println("----------------------");
		// 짝수만 출력하기
		i = 0;
		while(i < 10) {
			i++;
			if(i % 2 != 0) { // 홀수 검증
				continue;
			}
			System.out.println(i);
			
		}

	}

}
