-- 주석
/*
범위 주석
*/

select * from emp;
select * from dept;
select * from salgrade;

select empno from emp;
select empno, ename from emp;

select job from emp;

-- 중복 결과를 하나만 보여준다 --

select distinct job from emp;

select job as '직업' from emp;

select job 직업 from emp;

select sal, sal*12 from emp;

select 100*12;

select sal, comm , sal + comm from emp;

select * from emp;

select * 
from emp
where deptno = 20;

select *
from emp 
where deptno = 20 and job = 'CLERK';

select * from emp
where deptno = 20 or job = 'CLERK';

select * from emp
where deptno = 30 or deptno = 20 and job = 'CLERK';

select * from emp
where (deptno = 30 or deptno = 20) and job = 'CLERK';

select * from emp
where sal = 3000;

select * from emp
where sal != 3000;

select * from emp
where sal <> 3000;

select * from emp
where not(sal = 3000);

-- 문제 1. 급여가 2000 이상이고 3000 미만인 사원을 출력

select * from emp 
where sal >= 2000 and sal < 3000;

-- beetween A and B 
-- A 이상 and B 이하

select * from emp 
where sal between 2000 and 3000;

-- 문제 2. job이 CLERK 이거나 급여가 2000 초과이면서 부서 번호가 10인 사원만 출력

select * from emp 
where job ='CLERK' or (sal > 2000 and deptno = 10);

select * from emp 
where deptno = 20 or deptno = 30 or deptno = 10

-- 컬럼이 같고 or로 연결되어 있는 경우 
-- in으로 간편하게 표현 가능

select * from emp 
where deptno in(20, 30)

select * from emp 
where deptno not in(20, 30)

-- % : 모든 글자를 뜻함(심지어 글씨가 없어도 포함)

select * from emp
where ename like 'S%';

select * from emp
where ename like '%N';

select * from emp
where ename like '%AM%';

-- _ : 아무 글자 딱 하나를 뜻함

select * from emp
where ename like '_L%';

-- 문제
-- 이름이 5글자인 사람을 출력하시오

select * from emp
where ename like '_____';

select 'Human';
select lower('Human');
select upper('Human');

-- 문제 'Am'을 이용해 am이 이름 중간에 들어가는 사람만 출력
-- (mariaDB는 like에서 대소문자 구분을 원래 안함)

select * from emp
where ename like lower('%am');

-- 문제
-- 부서 10 또는 20의 사원 중 이름에 A가 들어가는 사원만 출력 

select * from emp
where deptno in (10, 20) and ename like('%A%');

-- null 다루기 

select * from emp
where comm = null;

select * from emp
where comm < 100;

select * from emp
where comm is null

select * from emp
where comm is not null


-- order by

select * from emp
order by sal;

-- asc : 오름차순, 생략 가능 

select * from emp 
order by sal asc; 

-- desc : 내림차순

select * from emp 
order by sal desc; 

select * from emp
order by deptno;

-- order by에 여러 컬럼이 적혀있는 경우
-- 왼쪽부터 정렬되고 동일한 값이 있는 경우 다음 조건이 적용된다.

select * from emp
order by deptno desc, job;

select * from emp
order by deptno desc, job asc, empno;

select * from emp
where sal > 1000
order by deptno desc, job asc, empno;

-- limit : 보여줄 row의 수 제한 

select * from emp
where sal > 1000
order by deptno desc, job asc, empno
limit 3;

-- limit offset, rows
-- offset만큼 건너뛰고 rows만 보여줌

select * from emp
where sal > 1000
order by deptno desc, job asc, empno
limit 5,3;

-- 문제 3. 부서번호가 20 또는 30인 사원 중에서 
-- 급여가 2000~3000 사이(포함)인 사원의 
-- 연봉이 작은 순으로 출력하시오
-- 단, 연봉이 같으면 이름을 내림차순으로

select * from emp
where 
	(deptno = 20 or deptno = 30) 
	and sal between 2000 and 3000
order by sal asc, ename desc;


