package com.example.demo;

import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer;

/**
 * [외장 톰캣 배포를 위한 서블릿 초기화 클래스]
 * - 프로젝트를 WAR 파일로 묶어 독립적인 외부 톰캣(Tomcat) 서버에 배포할 때,
 *   외부 톰캣이 스프링 부트 애플리케이션을 정상적으로 구동할 수 있도록 진입점을 설정해 줍니다.
 * - (내장 톰캣을 통한 단독 실행 시에는 BootHello01Application의 main()이 구동됩니다.)
 */
public class ServletInitializer extends SpringBootServletInitializer {

	@Override
	protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
		// 메인 부트 애플리케이션 클래스를 소스로 등록
		return application.sources(BootHello01Application.class);
	}

}

