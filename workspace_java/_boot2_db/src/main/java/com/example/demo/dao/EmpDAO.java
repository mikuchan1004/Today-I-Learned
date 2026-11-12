package com.example.demo.dao;

import java.util.List;
import java.util.Map;

import com.example.demo.dto.EmpDTO;

/**
 * [사원 데이터 접근 객체 인터페이스 (DAO, Data Access Object)]
 * 
 * - 데이터베이스(DB)와의 CRUD(생성, 조회, 수정, 삭제) 작업을 전담하는 계층의 규격입니다.
 * - Service 계층은 오직 이 DAO 인터페이스의 메서드만 호출하며,
 *   실제 어떤 DB 기술(MyBatis, JPA 등)을 사용하는지는 신경 쓰지 않아도 되는 구조를 만듭니다.
 */
public interface EmpDAO {
	
	/**
	 * 전체 사원 목록을 DB에서 조회하는 DAO 메서드
	 */
	List<EmpDTO> selectAllEmp();
	
	/**
	 * 사원번호(empno)로 특정 사원을 DB에서 조회하는 DAO 메서드
	 */
	public EmpDTO selectEmpno(int empno);

}

