package com.example.demo.controller;

/**
 * [싱글톤 패턴 (Singleton Pattern) 예제]
 * - 프로그램 전체에서 단 '하나'의 객체(인스턴스)만 만들어서 모두가 공유하며 쓰기 위한 설계 방식.
 * - 매번 객체를 새로 만들면(new) 메모리가 낭비되므로, 딱 1개만 만들어 재사용할 때 사용함.
 *   (참고: 스프링 부트도 내부적으로 객체들을 이렇게 싱글톤으로 관리함)
 */
public class Singleton {
	
	// 1. 단 하나만 만들어서 보관해 둘 '공유 변수' (static이므로 프로그램 전체에서 하나만 존재)
	static Singleton instance = null;
	
	// 2. 외부에서 'new Singleton()'으로 객체를 마음대로 여러 개 만들지 못하도록 private으로 막아둠
	private Singleton() {
		
	}
	
	// 3. 외부에서 이 클래스의 객체가 필요할 때 호출하는 유일한 통로
	public static Singleton getInstance() {
		// 아직 객체가 한 번도 안 만들어졌을 때만(null일 때만) 딱 한 번 새로 생성함
		if(instance == null) {
			instance = new Singleton();
		}
		// 이미 만들어져 있다면 새로 만들지 않고, 기존에 만들어둔 객체(instance)를 그대로 돌려줌
		return instance;
		
	}

}
