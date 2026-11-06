package var_02;

public class Type_03 {

	public static void main(String[] args) {
		// StringBuffer
		StringBuffer sb = new StringBuffer();
		sb.append("A");
		sb.append("B");
		sb.append("C");
		System.out.println("sb:" + sb);
		// StringBuffer를 String으로 형변환하는 방법
		String s1 = sb.toString();
		
		// 배열
		int a1[]; // C 언어 스타일 
		int[] a2; // java 스타일 
		// list[int] // python 
		int[][] a3; // 2차원 배열
		
		// null : 참조가 없는 상태 
		// 기본 타입에는 null을 넣을 수 없다.
//		int a = null;
		// 참조 타입에는 null을 넣을 수 있다.
		a1 = null;
		
		int[] a4 = new int[30];
		a4[0] = 10;
		a4[1] = 20;
		
		System.out.println("a4[0]:" + a4[0]);
		System.out.println("a4:" + a4);
//		a4[2] = null;
		
		// 배열 선언 두 번째 방법 
		// 값을 알고 있을 때 
		int[] a5 = new int[] {1,2,3,4};
		System.out.println("a5[2]:" + a5[2]);
	
		int[] a6 = {1,2,3,4};
		System.out.println("a6.length:" + a6.length);
//		System.out.println(a6[100]);
		
		int[] a = {1,2,3,4,5};
		for (int i=0; i<a.length; i++) {
			System.out.println(a[i]);
		}
		
		// 이차원 배열
		int[] floor1 = new int[10];
		int[] floor2 = new int[10];
		int[] floor3 = new int[10];

		int[][] 백자 = new int[3][10];
		System.out.println(백자);
		System.out.println(백자.length); 
		
		// 1층의 개수를 출력하시오.
		System.out.println(백자[0].length);
		System.out.println(백자[0][0]); // 기본값 0, false, null
		
		int[][] 백자2 = {
				{1,2,3},
				{11,12,13},
				{31,32,33,34}
		};
		// 백자2의 모든 내용을 출력하시오.
		for (int i=0; i<백자2.length; i++) {
			for(int j=0; j<백자2[i].length; j++) {
				System.out.println(백자2[i][j]);
			}
		}
		
		int [] b = {7,12,8,5};
		int [] c = new int[b.length];
		c[0] = b[3]; // length - (0+1) // length - 1 - 0
		c[1] = b[2]; // length - (1+2) // length - 1 - 1
		c[2] = b[1]; // length - (2+1)
		c[3] = b[0];
		// c 배열에 b 배열의 reverse 값이 들어가게.
		for (int i=0; i<b.length; i++) {
			c[i] = b[b.length -1 -i];
		}
		for (int i=0; i<c.length; i++) {
			System.out.println(c[i]);
		}
		
		// b의 마지막에 3을 추가한 배열 d를 만들어서 출력하시오.
//		int [] d = 7, 12, 8, 5, 3
		// int d[0] = 7 
		// int d[1] = 12 
		// int d[2] = 8
		// int d[3] = 5
		// int d[4] = 3
		// b의 마지막에 3을 추가하려면... append? 자바에 append가 있던가? 
		
		b = new int[] {7, 12, 8, 5};
		int new_value = 3;
		
		int [] d = new int[b.length + 1];
		for (int i=0; i<b.length; i++) {
			d[i] = b[i];
		}
		
		d[d.length - 1] = new_value;
		
		for (int i = 0; i < d.length; i++) {
            System.out.println("d[" + i + "] = " + d[i]);
        }
		
		// b의 맨 처음에 3을 추가한 배열 e를 만들어서 출력하시오 
		int[] e = new int[b.length+1];
		e[0] = 3;
//		e[1] = b[0];
//		e[2] = b[1];
//		e[3] = b[2];
//		e[4] = b[3];
		
		for (int i=0; i<b.length; i++) {
			e[i+1] = b[i];
		}
		
		
		// e 중에 홀수의 개수는?
		int count = 0;
		for (int i=0; i<e.length; i++) {
			if (e[i] % 2 == 1) {
				count++;
			}
		}
		
		// b의 맨 2번 자리에 3을 추가한 배열 f를 만들어서 출력하시오.
		int index = 2;
		int value = 3;
		int [] f = new int[b.length];
		// f[0] = b[0];
		// f[1] = 3;
		// f[2] = b[1];
		// f[3] = b[2];
		// f[4] = b[3];
		for (int i=0; i<f.length; i++) {
			if (i == index) {
				f[i] = value;
			
			}else if(i < index) {
				f[i] = b[i];
			}else if(i > index) {
				f[i] = b[i-1];
			}
		}
		for(int i=0; i<f.length; i++) {
			System.out.println(f[i]);
		}
   		
		// 주말 숙제 
		// 임시 비밀번호를 만들거다 총 10자리 
		// 대문자 하나, 소문자 하나, 숫자 하나 이상으로 구성.
		// HINT : 아스키코드, char
	}

}
