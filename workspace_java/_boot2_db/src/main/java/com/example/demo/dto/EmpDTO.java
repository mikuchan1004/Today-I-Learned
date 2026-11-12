package com.example.demo.dto;

import java.sql.Date;
import java.util.List;

import lombok.Data;

/**
 * [사원 정보 DTO (Data Transfer Object)]
 * - 계층 간(Controller, Service, DAO, MyBatis 매퍼, JSP 화면) 데이터를 전달하는 바구니 객체
 * - 데이터베이스 EMP 테이블의 컬럼들과 1:1 매핑되는 변수들과
 *   검색(동적 쿼리), 페이징 처리를 위해 필요한 추가 변수들을 함께 담고 있습니다.
 */
public class EmpDTO {

	// ==========================================
	// 1. EMP 테이블의 컬럼과 대응되는 필드들
	// ==========================================
	private int empno;                    // 사원 번호 (기본키)
	private String ename;                 // 사원 이름
	private String job;                   // 직무/담당 업무
	private int sal = Integer.MIN_VALUE;  // 급여 (동적 쿼리에서 0 이상의 값이 들어왔는지 구분하기 위해 최소값으로 초기화)
	private Integer mgr;                  // 직속 상사의 사원번호 (null 허용이므로 Wrapper 클래스인 Integer 사용)
	private Date hiredate;                // 입사일자
	private Integer comm;                 // 보너스/커미션 (null 허용)
	private int deptno;                   // 부서 번호
	
	// ==========================================
	// 2. 페이징 처리를 위한 필드들 (게시판/목록 분할용)
	// ==========================================
	private int size = 10;                // 한 페이지당 보여줄 게시글/사원 수
	private int page = 1;                 // 현재 보고 있는 페이지 번호
	private int start = 0;                // DB 조회 시작 row 번호 (LIMIT/OFFSET 등에서 사용)
	private int end;                      // 끝 row 번호
	
	// ==========================================
	// 3. 동적 검색(MyBatis dynamic query)용 필드들
	// ==========================================
	private String type;                  // 검색 조건 종류 (예: 'ename', 'sal', 'job')
	private String keyword;               // 사용자가 입력한 검색어
	
	// ==========================================
	// 4. 다중 선택 검색용 (MyBatis <foreach> 실습용)
	// ==========================================
	private List empnos;                  // 사원번호 목록 (예: [7369, 7499, 7521] -> IN 절 조건 생성)


	public int getEmpno() {
		return empno;
	}

	public void setEmpno(int empno) {
		this.empno = empno;
	}

	public String getEname() {
		return ename;
	}

	public void setEname(String ename) {
		this.ename = ename;
	}

	public String getJob() {
		return job;
	}

	public void setJob(String job) {
		this.job = job;
	}

	public int getSal() {
		return sal;
	}

	public void setSal(int sal) {
		this.sal = sal;
	}

	public Integer getMgr() {
		return mgr;
	}

	public void setMgr(Integer mgr) {
		this.mgr = mgr;
	}

	public Date getHiredate() {
		return hiredate;
	}

	public void setHiredate(Date hiredate) {
		this.hiredate = hiredate;
	}

	public Integer getComm() {
		return comm;
	}

	public void setComm(Integer comm) {
		this.comm = comm;
	}

	public int getDeptno() {
		return deptno;
	}

	public void setDeptno(int deptno) {
		this.deptno = deptno;
	}

	public int getSize() {
		return size;
	}

	public void setSize(int size) {
		this.size = size;
	}

	public int getPage() {
		return page;
	}

	public void setPage(int page) {
		this.page = page;
	}

	public int getStart() {
		return start;
	}

	public void setStart(int start) {
		this.start = start;
	}

	public int getEnd() {
		return end;
	}

	public void setEnd(int end) {
		this.end = end;
	}

	public String getType() {
		return type;
	}

	public void setType(String type) {
		this.type = type;
	}

	public String getKeyword() {
		return keyword;
	}

	public void setKeyword(String keyword) {
		this.keyword = keyword;
	}

	public List getEmpnos() {
		return empnos;
	}

	public void setEmpnos(List empnos) {
		this.empnos = empnos;
	}
}
