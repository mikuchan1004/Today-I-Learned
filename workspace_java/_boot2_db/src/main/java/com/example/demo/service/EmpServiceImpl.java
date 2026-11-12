package com.example.demo.service;

import java.util.List;
import java.util.Map;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.demo.dao.EmpDAO;
import com.example.demo.dto.EmpDTO;

/**
 * [사원 비즈니스 로직 구현체 (Service Implementation)]
 * 
 * - @Service: 스프링이 이 클래스를 비즈니스 로직을 수행하는 서비스 빈(Bean)으로 관리하도록 등록합니다.
 * - 컨트롤러로부터 전달받은 요청을 처리하며, 필요에 따라 가공, 계산, 트랜잭션(@Transactional) 처리 등을 수행하고
 *   데이터 접근이 필요하면 DAO(Data Access Object)를 호출합니다.
 */
@Service
public class EmpServiceImpl implements EmpService {

	/**
	 * DAO 객체 주입받기
	 * - 데이터베이스와 직접 통신하는 EmpDAO 구현체(EmpDAOImpl)를 스프링이 자동으로 주입해 줍니다.
	 */
	@Autowired
	EmpDAO empDAO;
	
	/**
	 * 전체 사원 목록 조회 처리
	 */
	@Override
	public List<EmpDTO> getEmpList() {
		// DAO의 selectAllEmp()를 호출하여 DB에서 사원 전체 데이터를 조회해 반환
		List<EmpDTO> result = empDAO.selectAllEmp();
		return result;
	}

	/**
	 * 사원번호 기준 단건 상세 조회 처리
	 */
	@Override
	public EmpDTO getEmpno(int empno) {
		// DAO의 selectEmpno()를 호출하여 특정 사원의 정보를 DB에서 가져옴
		EmpDTO empDTO = empDAO.selectEmpno(empno);
		return empDTO;
	}

}

