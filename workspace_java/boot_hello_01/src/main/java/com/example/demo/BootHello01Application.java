package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * [스프링 부트 애플리케이션의 시작 클래스]
 * 
 * @SpringBootApplication: 스프링 부트의 가장 핵심적인 어노테이션으로 다음 3가지 기능을 한 번에 수행합니다.
 *   1. @SpringBootConfiguration : 스프링 부트 설정 클래스임을 선언
 *   2. @EnableAutoConfiguration : 복잡한 설정을 자동으로 처리 (웹 서버, DB 드라이버 등 자동 구성)
 *   3. @ComponentScan           : 현재 패키지(com.example.demo)와 하위 패키지에서 @Controller, @Service, @Repository 등의 빈(Bean)을 찾아 스프링 컨테이너에 등록
 */
@SpringBootApplication
public class BootHello01Application {

	/**
	 * 자바 애플리케이션의 시작점(main 메서드)
	 * - SpringApplication.run()을 실행하면 내장 톰캣(Tomcat) 서버가 자동으로 시작되며 웹 애플리케이션이 구동됩니다.
	 */
	public static void main(String[] args) {
		System.out.println("hello world");
		// 현재 클래스를 전달하여 스프링 부트 환경을 초기화하고 실행
		SpringApplication.run(BootHello01Application.class, args);
	}

}

