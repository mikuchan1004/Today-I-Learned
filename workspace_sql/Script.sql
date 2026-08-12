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

-- 부서별 최고 연봉자 
-- 1. 부서별 최고 연봉

select max(sal) 
from emp
group by deptno

select ename, sal
from emp
-- where sal = 3000 or sal = 2850 or sal = 5000;
where sal in (3000, 2850, 5000);

select ename, sal, deptno
from emp 
where sal in (select max(sal)
			  from emp
			  group by deptno);

select sal from emp where ename = 'SCOTT';
select * from salgrade;

select grade 
from salgrade
where 3000 between losal and hisal;

select sal, ename, 
		(select grade 
			from salgrade
			where 3000 between losal and hisal)
from emp where ename = 'SCOTT';

select * from dept

select * 
from emp, dept;

select * 
from emp, dept
where emp.deptno = dept.deptno;

select * 
from emp e, dept d
where e.deptno = d.deptno;

-- select ename, dname, deptno
-- from emp e, dept d 
-- where e.deptno = d.deptno;

select e.ename, d.dname, e.deptno
from emp e, dept d
where e.deptno = d.deptno;

select * from salgrade;

-- 스미스의 연봉 등급은?
-- 이름, 월급, 등급, losal, hisal
select * from salgrade 
where (800) >= losal and 800 <= hisal;

select sal from emp
where ename = 'SMITH';

select ename, sal, grade, losal, hisal
from emp e , salgrade s 
where sal >= losal and sal <= hisal
and ename = 'SMITH';

select * from emp;

select mgr 
from emp 
where ename = 'SMITH';

select 
	ename
from emp 
where empno = 7902;

select 
	ename
from emp 
where empno = (select 
				MGR 
				from emp
				where ename = 'SMITH');

-- mgr이 null인 것은 빠진다.
select e1.ename , e2.ename
from emp e1, emp e2
where e1.mgr = e2.empno
and e1.ename = 'SMITH';

-- 문제
-- 모든 사람의 이름, 부서명, 급여 등급, 등급 순 내림차순
select ename, sal, dname, grade
from emp e, dept d, salgrade s
where e.deptno = d.deptno 
and e.sal between s.losal and s.hisal
order by grade desc , sal desc;

select ename, ename from emp;
select ename, emp.* from emp;
select ename, e.* from emp e;

select e.deptno
from emp e join dept d on(e.deptno = d.deptno);

select deptno
from emp e join dept d using(deptno);

select e1.empno, e1.ename, e2.empno, e2.ename
from emp e1
	left outer join emp e2 on e1.mgr = e2.empno;

select e1.empno, e1.ename, e2.empno, e2.ename
from emp e1
	right outer join emp e2 on e1.mgr = e2.empno;

select * from dept;

-- 문제
-- deptno, dname, empno, ename
-- 모든 부서가 다 나오게
-- 부서번호 오름차순, 부서번호가 같으면 이름 오름차순
select deptno, dname, empno, ename
from dept d
	left outer join emp e using(deptno)
order by deptno, ename;


-- having 없이 서브쿼리로 해결해보자 
-- 1. 부서 별 평균 연봉 출력

select avg(sal)
from emp
group by deptno;

-- 2. 부서 별 평균 연봉이 2000 이상인 부서만 출력

select avg(sal) avg_sal
from emp
-- where avg_sal >= 2000 -- 별칭은 select 이후에 사용 가능
-- where avg(sal) >= 2000 -- 집계 함수 사용 불가
group by deptno
having avg(sal) >= 2000;

-- 서브쿼리를 써보자

select * 
from (
	select avg(sal) avg_sal
	from emp
	group by deptno
)a
where avg_sal >= 2000;

-- DDL
-- create

desc emp;

create table emp2(
	empno int(4) primary key, 
	ename varchar(10) not null,
	job varchar(9),
	mgr int(4),
	hiredate date,
	sal decimal(7,2), -- 총 7자리, 그 중 2자리 소수점
	comm decimal(7,2),
	deptno int(2)
);

select * from emp2;

desc emp2;

desc dept;

create table dept2 (
	deptno int(2) primary key,
	dname varchar(14),
	loc varchar(13)
);

select * from dept2;

-- 테이블 복사

create table emp_copy 
as select * from emp;
select * from emp_copy;

create table emp_copy2
as select * from emp where 1 <> 1;
select * from emp_copy2;

create table dept3 
as select * from dept where 1 != 1;
select * from dept3;

create table emp3 (
	empno int(4), 
	ename varchar(10) not null,
	job varchar(9),
	mgr int(4),
	hiredate date,
	sal decimal(7,2), 
	comm decimal(7,2),
	deptno int(2),
	primary key(empno),
	foreign key(deptno) references dept3(deptno)
);

-- 테이블 삭제 

drop table dept3;

create table dept3 (
	deptno int(2) primary key,
	dname varchar(14),
	loc varchar(13)
);

-- ALTER

alter table emp3
add gender varchar(10) not null default '남';
select * from emp3;

alter table emp3
change gender gender2 varchar(10);
select * from emp3;

alter table emp3
rename column gender2 to gender3;
select * from emp3;

alter table emp3
drop column gender;
select * from emp3;

alter table emp3
rename to emp4;
select * from emp4;

drop table emp4;
drop table dept3;

select * from emp_copy;
truncate table emp_copy; -- 아주 위험한 코드니까 주의!
select * from emp_copy;

select * from dept2;
drop table dept2;

select * from emp2;
drop table emp2;

create table dept2 (
	deptno int(2) primary key,
	dname varchar(14),
	loc varchar(13)
);

create table emp2 (
	empno int(4), 
	ename varchar(10) not null,
	job varchar(9) default 'CLERK',
	mgr int(4),
	hiredate date default now(),
	sal decimal(7,2), 
	comm decimal(7,2),
	deptno int(2),
	primary key(empno),
	foreign key(deptno) references dept2(deptno)
);

select * from emp2;

insert into dept2 
values(
	10,
	'휴먼',
	'천안'
);

insert into emp2 
values(
		1000, 
		'김상우', 
		'MANAGER', 
		2000, 
		'2026-08-09',
		3000,
		50,
		10
);

select * from emp2;

insert into emp2 (empno, ename, sal, comm, deptno)
values (
	1001, '홍길동', 4100, 150, 10
);

select * from emp2;

-- ename은 not null 제한이 있고
-- insert에 누락하면 null이 들어간다 
-- 그래서 에러 발생

/*insert into emp2 (empno, sal, comm, deptno)
values (
	1001, 4100, 150, 10
);
*/

-- primary key
-- unique + not null

/*
insert into emp2 (empno, ename, sal, comm, deptno)
values (
	1001, '홍길동', 4100, 150, 10
);
*/

-- dept 테이블에 deptno 20값이 없어서 에러

/*
insert into emp2 (empno, ename, sal, comm, deptno)
values (
	1002, '홍길동', 4100, 150, 20
);
*/

insert into emp2 (empno, ename, sal, comm, deptno)
values 
(1012, '홍길동2', 4100, 150, 10),
(1013, '홍길동3', 4100, 150, 10),
(1014, '홍길동4', 4100, 150, 10);

select * from emp2;

-- UPDATE

update emp2
set 
	sal = 1000,
	comm = 200;

select * from emp2;

update emp2
set	
	sal = sal * 1.1,
	comm = comm * 1.2
where empno = 1002;

select * from emp2;

update dept2
set deptno = 20
where deptno = 10;

-- DELETE

delete from emp2
where empno = 1002;
select * from emp2;

delete from emp2;
select * from emp2;

rollback;
select * from emp2;
select * from dept2;

commit;
rollback;

delete from emp2
where empno = 1013;
rollback;
select * from emp2;


select * 
from emp e
	left outer join emp2 e2 on(e.mgr = e2.empno)
	left outer join dept d on(e.deptno = d.deptno)
order by e.ename desc;

select * from emp
where deptno = 10;

-- INDEX

create index idx_emp_empno_desc
on emp(empno desc);

select * from emp
order by empno desc;

create index idx_emp_deptno
on emp(deptno);

select * from emp 
order by deptno = 10;

select * 
from emp force index(idx_emp_deptno)
where deptno = 10
order by deptno;

-- mariadb 한글 한 글자는 3Byte

select length('한글');
select length('ab');

select max(empno)+1 from emp;

-- sequence 

create table emp_auto (
	empno int auto_increment,
	ename varchar(50),	
	primary key(empno)
);

insert into emp_auto(ename)
values ('민수');

select * from emp_auto;

insert into emp_auto(ename)
values ('민수2');
select * from emp_auto;

-- 무한 대댓글

select 
	empno, ename, mgr, 1 as level
from emp 
where mgr is null
union all 
select 
	empno, ename, mgr, 2 as level
from emp 
where mgr = 7839;

with recursive emp_recu as (
	select 
		empno, ename, mgr,
		lpad(ename, length(ename), ' '),
		1 as level, 
		cast(ename as char(200)) as sort_key
	from emp 
	where mgr is null
	union all 
	select 
		e.empno, e.ename, e.mgr, 
		lpad(e.ename, (er.level*4)+length(e.ename), ' '),
		er.level+1 as level,
		concat(er.sort_key, '-', cast(e.ename as char(200))) as sort_key
	from emp e
		join emp_recu er on (e.mgr = er.empno)
)
select * from emp_recu
order by sort_key;

-- 문제 1
-- 1981년에 입사한 사원 중에서 
-- 급여가 가장 낮은 사원을 조회하시오

select ename, hiredate, sal
from emp
where substr(hiredate, 1, 4) = '1981'
and sal = (
	select min(sal)
	from emp 
	where substr(hiredate, 1, 4) = '1981'
)

-- 문제 2
-- 각 부서 별 급여가 가장 높은 사원과 가장 낮은 사원의 차이를 조회하시오.
-- 결과 : 부서명, 차이 금액

select 
	d.dname,
	max(e.sal)-min(e.sal) as '차이 금액'
from
	emp e
join
	dept d on e.deptno = d.deptno
group by
	d.deptno, d.dname;

-- 문제 3
-- BLAKE보다 높은 연봉을 받는 사람들 출력

select ename, sal
from emp
where sal > (select sal from emp
			 where ename = 'BLAKE')

-- 문제 4
-- JONES랑 같은 job을 가진 사람들

select * from emp
where job = (select job from emp
			where ename = 'JONES')

-- 문제 5 
-- 급여 등급 별 사원 수를 등급 오름차순으로 정렬 
-- 단, 모든 등급을 표시한다.

select
	s.grade, count(*)
from 
	emp e
join 
	salgrade s on e.sal between s.losal and s.hisal
group by 
	s.grade 
order by 
	s.grade asc;

-- 문제 6
-- 이름, 급여, 급여 등급, 부서 이름 조회
-- 단, 급여 등급 3 이상만 조회
-- 급여 등급 내림차순, 등급이 같은 경우 급여 내림차순, 급여가 같은 경우 이름 내림차순

select e.ename, e.sal, s.grade, d.dname 
from emp e
join dept d on e.deptno = d.deptno
join salgrade s on e.sal between s.losal and s.hisal 
where s.grade >= 3
order by s.grade desc, e.sal desc, e.ename desc

-- 문제 7
-- 부서명이 SALES인 사원 중 급여 등급이 2 또는 3인 사원을 급여 내림차순으로 정렬

select e.ename, e.sal, s.grade, d.dname
from emp e 
join dept d on e.deptno = d.deptno
join salgrade s on e.sal between s.losal and s.hisal
where d.dname = 'SALES' and s.grade between 2 and 3
order by e.sal desc

-- 데이터 스토리지 설계 (RDB·문서·벡터) 시험 문제 풀이

/*
 문제 1
 급여가 2000을 초과하는 사원의 사원명, 급여, 부서이름을 조회하세요. 
 */

select e.ename, e.sal , d.dname
from emp e
join dept d on e.deptno = d.deptno
where sal > 2000;

/*
 문제 2 
 급여가 1000 이상 3000 이하인 사원의 사원명, 급여, 급여등급을 조회하세요.
 */

select e.ename, e.sal, s.grade
from emp e
join salgrade s on e.sal between s.losal and s.hisal
where sal >= 1000 and sal <= 3000;

/*
 문제3
 입사일이 빠른 순으로 사원명, 입사일, 부서이름을 출력하세요.
 */

select e.ename, e.hiredate, d.dname 
from emp e
join dept d on e.deptno = d.deptno
order by hiredate;

/*
 문제 4
 급여등급이 3 이상인 사원만 사원명, 부서이름, 급여, 급여등급을 급여 기준 내림차순
 정렬하세요.
 */

select e.ename, d.dname, e.sal, s.grade
from emp e
join dept d on e.deptno = d.deptno
join salgrade s on e.sal between s.losal and s.hisal 
where grade >= 3
order by e.sal desc;

/*
 문제 5
 각 부서 별로 평균 급여보다 높은 사원만 사원명, 부서이름, 급여, 평균급여를 
 부서이름 오름차순, 급여 내림차순으로 정렬하세요.
 */

select e.ename as 사원명, d.dname as 부서명, e.sal as 급여, round(dept_avg.avg_sal, 2) as 평균급여
from emp e
join dept d on e.deptno = d.deptno 
join (
	select deptno, avg(sal) as avg_sal
	from emp 
	group by deptno
)dept_avg
	on e.deptno = dept_avg.deptno
where e.sal > dept_avg.avg_sal
order by d.dname asc, e.sal desc;