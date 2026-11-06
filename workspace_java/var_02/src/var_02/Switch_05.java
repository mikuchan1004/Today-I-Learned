package var_02;

import java.util.Scanner;

public class Switch_05 {
	public static void main(String[] args) {
		
		System.out.println("숫자를 입력하세요:");
		Scanner scan = new Scanner(System.in);
		int a = scan.nextInt();
		System.out.println("a:" + a);
		
		switch(a) {
			case 1 :
				System.out.println("a는 1이다");
			case 2 : 
				System.out.println("a는 2이다");
				break;
			default : 
				System.out.println("그 외");
		}
		// 사용 가능 : byte, char, short, int, String
		// 사용 불가능 : boolean, long, float, double
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
