package var_02;

public class If_04 {

	public static void main(String[] args) {
		
		if(3 < 2) {
			System.out.println("3 < 2");
		}else if (3 != 3) {
			System.out.println("3 != 2");
		}else {
			System.out.println("else");
		}
		
		if(3 > 2) {
			System.out.println("3 > 2");
		}
		
		if (3 > 2) System.out.println("3 > 2");
		else 	   System.out.println("거짓");
		
		int a = 3;
		// 기습문제 
		// a를 홀, 짝으로 출력하시오.
		if (a % 2 == 1) {
			System.out.println("홀");
		} else {
			System.out.println("짝");
		}
	
		double rand = Math.random();
		int min = 3;
		int max = 7;
		// 기습문제
		// rand의 결과가 min~max로 나오게 하시오.
		rand = Math.random() * 5;
		System.out.println(rand);
		
		// 1단계 : 0~7까지만 나오게
		// 0~0.99999999 >>>> 0~7.999999
		rand = Math.random() * (max+1);
		rand = (int)(Math.random() * (max+1));
		
		// 2단계 : 3~10까지 나오게
		rand = (int) (Math.random() * (max+1)) + min;
		
		// 3단계 : 3~7까지 나오게 
		rand = (int) (Math.random() * ((min-max)+1)) + min;
		
		System.out.println(rand);
		
		rand = (int)(Math.random() * 10000) % ((max-min)+1) + min;
		
		int num = 3;
		int num2 = 0;
		if (num / num2 == 0) {
			System.out.println("참");
		}else {
			System.out.println("거짓");
		}
		
		if (num2 != 0 && num / num2 == 0) {
			System.out.println("참");
		}else {
			System.out.println("거짓");
		}
		
	}

}
