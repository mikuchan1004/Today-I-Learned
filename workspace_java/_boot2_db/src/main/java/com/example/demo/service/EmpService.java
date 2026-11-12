package com.example.demo.service;

import java.util.List;
import java.util.Map;

import com.example.demo.dto.EmpDTO;

/**
 * [사원 비즈니스 로직 인터페이스 (Service Interface)]
 * 
 * [인터페이스를 따로 두는 이유]
 * - 컨트롤러와 실제 구현체(ServiceImpl) 사이에 규격(명세)을 두어 느슨한 결합(Loose Coupling)을 만듭니다.
 * - 나중에 비즈니스 로직의 구현 방식이 바뀌거나 트랜잭션, AOP, 테스트 Mock 객체를 적용할 때
 *   컨트롤러 코드를 고칠 필요 없이 유연하게 교체할 수 있습니다.
 */
public interface EmpService {

	/**
	 * 전체 사원 목록을 조회하는 비즈니스 메서드
	 */
	List<EmpDTO> getEmpList();
	
	/**
	 * 특정 사원번호(empno)에 해당하는 사원 1명의 정보를 조회하는 비즈니스 메서드
	 */
	EmpDTO getEmpno(int empno);
}

