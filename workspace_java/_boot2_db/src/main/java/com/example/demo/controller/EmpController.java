package com.example.demo.controller;

import java.util.List;
import java.util.Map;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import com.example.demo.dto.EmpDTO;
import com.example.demo.service.EmpService;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpSession;

/**
 * [사원 관리 컨트롤러 (Controller)]
 * - 클라이언트(사용자 웹 브라우저)의 요청(URL)을 가장 먼저 받아 분석하고,
 *   해당 작업을 비즈니스 로직(Service)에 위임한 뒤
 *   결과 데이터를 Model에 담아 뷰(JSP) 화면으로 전달하는 중계자 역할을 합니다.
 */
@Controller // 스프링이 이 클래스를 웹 요청을 처리하는 컨트롤러 빈(Bean)으로 인식하도록 등록
public class EmpController {

	// 로그 출력을 위한 SLF4J 로거 객체 생성
	private static final Logger logger = LoggerFactory.getLogger(EmpController.class);
	
	/**
	 * @Autowired (의존성 주입 - DI, Dependency Injection)
	 * - 개발자가 직접 new EmpServiceImpl()을 호출하지 않아도,
	 *   스프링 컨테이너가 EmpService 인터페이스를 구현한 @Service 빈 객체를 찾아 자동으로 주입해 줍니다.
	 */
	@Autowired
	EmpService empService;
	
	/**
	 * [기본 루트 경로 요청 처리] - http://localhost:8080/
	 * - @ResponseBody: JSP 화면을 거치지 않고, 반환된 문자열("hello")을 브라우저에 그대로 순수 텍스트(HTTP Body)로 응답합니다.
	 */
	@ResponseBody
	@RequestMapping(value="/", method=RequestMethod.GET)
	public String hello() {
		return "hello";
	}
	
	/**
	 * [전체 사원 목록 조회] - GET http://localhost:8080/list
	 * 
	 * @param model : 컨트롤러에서 조회한 데이터를 JSP 뷰 페이지로 전달하기 위해 스프링이 제공하는 데이터 전달 상자
	 * @return "result" -> application.properties에 설정된 prefix(/WEB-INF/jsp/) + "result" + suffix(.jsp)로 결합되어
	 *                    /WEB-INF/jsp/result.jsp 페이지가 렌더링됩니다.
	 */
	@GetMapping("/list")
	public String list(Model model) {
		System.out.println("/list 실행");
		
		// 1. 서비스 계층을 호출하여 전체 사원 목록(List<EmpDTO>)을 가져옵니다.
		List<EmpDTO> list = empService.getEmpList();
		System.out.println("/list: list: "+ list);
		
		// 2. JSP 화면에서 ${list}라는 이름으로 접근할 수 있도록 Model에 담습니다.
		model.addAttribute("list", list);
		
		// 3. result.jsp 화면으로 포워딩(이동)
		return "result";
	}

	/**
	 * [사원 단건 상세 조회] - http://localhost:8080/getEmpno?empno=7788
	 * 
	 * @param model : 조회된 EmpDTO 단건 객체를 JSP에 넘겨주기 위한 모델 객체
	 * @param empno : @RequestParam을 통해 URL 쿼리스트링(?empno=7788)의 값을 정수형 int로 자동 형변환하여 받음
	 *                - required=false: 파라미터가 필수가 아님을 명시 (생략 시 기본 0 등으로 처리 가능)
	 * @return "result" -> /WEB-INF/jsp/result.jsp
	 */
	@RequestMapping("/getEmpno")
	public String getEmpno(Model model,
		@RequestParam(value="empno", required=false)
		int empno
	) {
		System.out.println("/getEmpno 실행");
		
		System.out.println("empno: "+ empno);
		// 1. 특정 사원 번호에 해당하는 사원 1명의 정보를 서비스에서 조회
		EmpDTO empDTO = empService.getEmpno(empno);

		// 2. JSP 화면에서 ${empDTO}라는 이름으로 사원 정보를 꺼낼 수 있도록 담기
		model.addAttribute("empDTO", empDTO);
		
		// 3. result.jsp 화면으로 포워딩 (result.jsp에서 list가 없으면 단건 empDTO를 출력하도록 분기되어 있음)
		return "result";
	}

}






