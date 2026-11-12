package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * [Spring Boot 2차 DB 연동 애플리케이션 메인 클래스]
 * 
 * - @SpringBootApplication: 
 *   자동 구성(@EnableAutoConfiguration), 설정 등록(@SpringBootConfiguration),
 *   하위 패키지 컴포넌트 자동 스캔(@ComponentScan - Controller, Service, DAO 등)을 수행합니다.
 */
@SpringBootApplication
public class Boot2DbApplication {

	public static void main(String[] args) {
		// 스프링 부트 애플리케이션 실행 및 내장 톰캣 서버 구동
		SpringApplication.run(Boot2DbApplication.class, args);
	}

}

