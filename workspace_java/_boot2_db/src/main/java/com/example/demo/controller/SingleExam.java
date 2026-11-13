package com.example.demo.controller;

/**
 * [싱글톤 패턴 테스트 실행 클래스]
 * - Singleton 클래스가 실제로 하나의 객체만 공유해서 쓰는지 확인해 보는 예제.
 */
public class SingleExam {

	public static void main(String[] args) {
		// private 생성자 때문에 'new Singleton()'은 사용할 수 없음
		// 대신 getInstance()를 호출해 객체를 받아옴 (이때 처음이므로 객체 1개가 새로 생성됨)
		Singleton s1 = Singleton.getInstance();
		
		// 두 번째 호출: 이미 위에서 만들어진 객체가 있으므로 새로 만들지 않고, s1과 '똑같은 객체'를 돌려받음
		Singleton s2 = Singleton.getInstance();

		// 결과적으로 s1과 s2는 변수 이름만 다를 뿐, 메모리상 완전히 같은 하나의 객체를 가리키게 됨 (s1 == s2 는 true)
	}

}
