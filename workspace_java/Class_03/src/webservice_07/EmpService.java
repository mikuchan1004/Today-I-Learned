package webservice_07;

import java.util.List;

/**
 * [서비스 인터페이스 (Service Interface)]
 * - 개념: "비즈니스 로직(업무 규칙)"을 처리하는 계층의 규격
 * - 역할: 필요한 비즈니스 로직을 거쳐 최종 사원 목록을 가져오는 약속(규격)을 선언합니다.
 */
public interface EmpService {
	
	// 업무 규칙에 맞게 가공된 사원 목록을 반환하는 메서드 규격
	List getEmp();
}
