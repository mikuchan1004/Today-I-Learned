<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%-- JSTL(JSP Standard Tag Library) 코어 태그 라이브러리 (조건문, 반복문 지원) --%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%-- 숫자/날짜 포맷팅용 JSTL 라이브러리 --%>
<%@ taglib prefix="fmt" uri="http://java.sun.com/jsp/jstl/fmt" %>
<%-- 문자열 처리 함수 라이브러리 --%>
<%@ taglib prefix="fn" uri="http://java.sun.com/jsp/jstl/functions" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>결과 페이지</title>
</head>
<body>
<%-- 
  [사원 목록 / 상세 조회 결과 출력 화면]
  - 컨트롤러에서 model.addAttribute()로 전달한 데이터를 받아 화면에 표 형태로 출력합니다.
  - 리스트가 있으면 전체 목록을 반복 출력하고, 단건 조회의 경우 사원 1명의 정보를 출력합니다.
--%>
<table border=1>
	<thead>
		<tr>
			<th>empno</th>
			<th>ename</th>
			<th>job</th>
			<th>sal</th>
			<th>mgr</th>
			<th>hiredate</th>
			<th>comm</th>
			<th>deptno</th>
		</tr>
	</thead>
	<tbody>
		<%-- 1. [목록 조회인 경우] 컨트롤러에서 넘겨준 ${list}가 비어있지 않을 때 실행 --%>
		<c:if test="${not empty list }">
			<%-- <c:forEach>: 자바의 for(EmpDTO dto : list)와 동일하게 목록을 하나씩 꺼내어 반복 --%>
			<c:forEach var="dto" items="${list}">
			<tr>
				<td>${dto.empno }</td>
				<td>
					<%-- 이름을 클릭하면 사원번호(empno)를 파라미터로 붙여 단건 상세 조회(/getEmpno?empno=...)로 이동 --%>
					<a href="getEmpno?empno=${dto.empno }">${dto.ename }</a>
				</td>
				<td>${dto.job }</td>
				<td>${dto.sal }</td>
				<td>${dto.mgr }</td>
				<td>${dto.hiredate }</td>
				<td>${dto.comm }</td>
				<td>${dto.deptno }</td>
			</tr>
			</c:forEach>
		</c:if>
		
		<%-- 2. [단건 상세 조회인 경우] ${list}가 없을 때 컨트롤러의 ${empDTO} 단건 출력 --%>
		<c:if test="${empty list }">
			<tr>
				<td>${empDTO.empno }</td>
				<td>${empDTO.ename }</td>
				<td>${empDTO.job }</td>
				<td>${empDTO.sal }</td>
				<td>${empDTO.mgr }</td>
				<td>${empDTO.hiredate }</td>
				<td>${empDTO.comm }</td>
				<td>${empDTO.deptno }</td>
			</tr>
		</c:if>
	</tbody>
</table>
</body>
</html>