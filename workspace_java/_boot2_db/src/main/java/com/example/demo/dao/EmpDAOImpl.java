package com.example.demo.dao;

import java.util.List;
import java.util.Map;

import org.apache.ibatis.session.SqlSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;

import com.example.demo.dto.EmpDTO;

/**
 * [사원 데이터 접근 객체 구현체 (DAO Implementation)]
 * 
 * - @Repository: 스프링이 이 클래스를 데이터베이스 접근 계층(DAO) 빈(Bean)으로 등록하며,
 *   DB 관련 예외를 스프링의 DataAccessException으로 일관되게 변환해 주는 기능도 제공합니다.
 */
@Repository
public class EmpDAOImpl implements EmpDAO {

	/**
	 * MyBatis 핵심 세션 객체 주입
	 * - SqlSession: SQL 실행, 트랜잭션 관리, 매퍼 XML 파일 호출을 담당하는 MyBatis의 핵심 인스턴스
	 * - 스프링 부트 mybatis-spring 연동 라이브러리가 스레드에 안전한(SqlSessionTemplate) 객체로 자동 주입해 줍니다.
	 */
	@Autowired
	SqlSession sqlSession;
	
	/**
	 * [전체 사원 조회]
	 * - sqlSession.selectList(매퍼_식별자)
	 *   : 매퍼 XML의 namespace가 "mapper.emp"이고 id가 "selectEmp"인 <select> 태그를 찾아 실행합니다.
	 *   : 조회 결과가 여러 건(List)일 때 사용하며, 각 행(Row)은 EmpDTO 객체로 매핑되어 List에 담깁니다.
	 */
	@Override
	public List<EmpDTO> selectAllEmp() {
		List<EmpDTO> resultList = null;
		
		resultList = sqlSession.selectList("mapper.emp.selectEmp");
		System.out.println("selectAllEmp: resultList: "+ resultList);
		
		return resultList;
	}

	/**
	 * [사원 단건 상세 조회]
	 * - sqlSession.selectOne(매퍼_식별자, 파라미터값)
	 *   : 조회 결과가 딱 1행(또는 0행)일 때 사용하는 메서드입니다.
	 *   : 두 번째 인자로 전달한 empno 값이 XML 매퍼의 #{_parameter} 위치에 바인딩됩니다.
	 */
	@Override
	public EmpDTO selectEmpno(int empno) {
		EmpDTO empDTO = null;
		
		empDTO = sqlSession.selectOne("mapper.emp.selectEmpno", empno);
		System.out.println("selectEmpno: empDTO: "+ empDTO);
		
		return empDTO;
	}

}


