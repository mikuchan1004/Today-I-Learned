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

-- 집계 함수

select count(ename) from emp;
select count(mgr) from emp;
select count(comm) from emp; -- null은 개수에서 제외 
select count(*) from emp;

select max(sal) from emp;
select min(sal) from emp;

select sum(sal) from emp;
select avg(sal) from emp;

select length(ename) , ename from emp;

-- select count(*), ename from emp; 원하는 결과가 나오지 않기때문에 쓰지 않는것이 좋다.

select * from emp 
where length(ename) = 4;

-- 대상의 몇 번재부터 몇 개를 잘라오기

select substring(ename, 2, 3 ), ename from emp;
select substr(ename, 2, 3), ename from emp;

-- 전부 교체

select replace (ename, 'A' ,'에이'), ename from emp;

-- 대상의 자리수를 맞춰주고 남으면 채워준다

select lpad(ename, 10, '#') from emp;
select lpad(ename, 3, '#') from emp;

select rpad(ename, 10, '#') from emp;

select lpad(sal, 10, '0') from emp;
select lpad(ename, 10, ' ') from emp;

select trim(' a b c  ')

select concat(ename, job) from emp;
select concat(ename, ' ' , job) from emp;

-- 오라클에서 합치기 ename || job으로 사용 가능

select concat_ws('-' , ename, job, empno) from emp;

-- 반올림

select round(3.14);
select round(3.145, 2);

-- 올림

select ceil(3.14);
select ceil(-3.14);

-- 내림

select floor(3.14);
select floor(-3.14);

-- 버림

select truncate(-3.14, 1);

-- 나머지 

select mod(10, 3);

-- 현재 시간

select now();
select sysdate();

-- 날짜 출력 양식 지정

select date_format(now(), '%Y년 %M월 %D일 %H시 %i분 %s초');

-- 문자를 날짜 형으로 변환

select str_to_date('2026-08-07', '%Y-%m-%d');

select ifnull(comm, 0), comm from emp;
select coalesce(comm, 0), comm from emp;

select sal * 12 + comm from emp;
select sal * 12 + ifnull(comm, 0) from emp;

-- 문제
-- ename 앞 두 글자만 출력

select substr(ename, 1, 2) , ename from emp;

-- ename의 앞 두글자만 원본 그대로 추력하고 
-- 4개의 *을 붙여서 출력 

select substr(ename, 1, 2) , rpad('' , 4, '*') from emp;

select rpad(substring(ename, 1, 2), 6, '*') from emp;

-- ename의 앞 두 글자만 원본 그대로 출력하고 
-- 나머지 이름 만큼의 * 출력

select rpad(substring(ename, 1, 2), length(ename), '*') from emp; 

-- case문 

select * from emp;

select 
	job, sal,
	case job 
		when 'CLERK' then sal * 1.05
		when 'SALESMAN' then sal * 1.03
		else sal 
	end as upsal
from emp;

select 
	job, sal,
	case 
		when job = 'CLERK' then sal * 1.05
		when job = 'SALESMAN' then sal * 1.03
		else sal 
	end as upsal
from emp;

select 
	sal, comm,
	case
		when comm is null then 0
		else comm
	end
from emp;

-- GROUP BY절

select deptno from emp
group by deptno;

select 
	deptno, count(*), sum(sal)
from emp
group by deptno;

select deptno, job, count(*)
from emp
group by deptno, job;

select deptno, job
from emp
where deptno = 10
group by deptno, job;

select deptno, job
from emp
where deptno = 10
group by deptno, job
order by job;

select avg(sal) from emp;

-- select 
-- 		avg(sal)
-- from emp
-- where sal >= avg(sal);

select 
	avg(sal) as avg_sal,
	deptno,
	job
from emp 
group by deptno, job
having avg(sal) >= 2000;

-- where 조건을 having에 적을 수 있지만
-- 통상 group by와 관련된 것만 적는다.


-- 직업 별로 연봉 1000 이상인 사람이 3명 이상인 경우만 출력

select
	job,count(*) cnt
from emp
where sal >= 1000
group by job
having count(*) >= 3;

/* 5 */select job, 1 as num
/* 1 */from emp
/* 2 */where sal > 1000
/* 3 */group by job
/* 4 */having count(*) >= 3
/* 6 */order by job desc, num

select * from emp where deptno = 10
union
select * from emp where deptno = 10;

select * from emp where deptno = 10
union all
select * from emp where deptno = 10;

-- 서브 쿼리문

select * from emp
where sal > 1250;

-- 'WARD'의 연봉만 출력
select sal
from emp
where ename = 'WARD';

select * from emp
where sal > (select sal
			from emp 
			where ename = 'WARD');

select * from emp
where sal > (select avg(sal) from emp);



