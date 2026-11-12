package com.example.demo;

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

/**
 * [외장 톰캣 배포를 위한 서블릿 초기화 클래스]
 * - 프로젝트를 WAR 파일로 빌드하여 외부 WAS(독립 톰캣 등)에 배포할 때 구동 시작점을 지정합니다.
 */
public class ServletInitializer extends SpringBootServletInitializer {

	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
		return application.sources(Boot2DbApplication.class);
	}

}

