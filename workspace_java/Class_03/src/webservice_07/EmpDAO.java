package webservice_07;

import java.util.List;

/**
 * [DAO 인터페이스 (Data Access Object)]
 * - 개념: "데이터베이스(DB)와 직접 대화하는 전담 창구"의 규격
 * - 역할: DB에서 사원(Emp) 목록을 가져오는 약속(규격)을 선언합니다.
 */
public interface EmpDAO {
	
	// 사원 목록을 DB에서 조회해오는 메서드 규격
	List SelectEmp();
}
