package webservice_07;

import java.util.ArrayList;
import java.util.List;

/**
 * [DAO 구현 클래스 (Data Access Object Implementation)]
 * - EmpDAO 인터페이스의 규격을 실제로 구현하여, 데이터베이스(DB)에서 데이터를 가져오는 역할을 담당합니다.
 * - (현재는 실제 DB 연결 대신 가상의 사원 번호 리스트를 만들어 반환하고 있습니다)
 */
public class EmpDAOImpl implements EmpDAO {

	@Override
	public List SelectEmp() {
		// 가상의 DB 데이터(사원 번호 목록) 생성
		List list = new ArrayList();
		list.add(1111);
		list.add(2222);
		list.add(3333);
		list.add(4444);
		list.add(5555);
		
		// DB 조회 결과를 호출한 쪽(Service)으로 반환
		return list;
	}

}
