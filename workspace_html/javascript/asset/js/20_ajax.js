window.addEventListener('load' , bind)

function bind() {
    const btn1 = document.querySelector('#btn1')
    btn1.addEventListener('click' , function(){

        //1.  ajax 객체 생성
        const xhr =  new XMLHttpRequest()

        // 2. 보낼 준비
        // 방식method, 주소 
        xhr.open('GET', 'https://jsonplaceholder.typicode.com/users')

        //3.  보내기 
        xhr.send()

        //4. 결과 확인
        xhr.onload = function() {
            console.log('다녀왔어')
            console.log(xhr.responseText)
            // 깜짝 퀴즈
            // 두번째 사람의 이름을 출력
            // 세번째 사람의 lat를 출력 
    
            const member = JSON.parse(xhr.responseText)
            console.log(member[1])
            console.log(member[1].name)
            console.log(member[1]['name'])
            
            console.log(member[2].address.geo.lat)
        }
        
    })

    const btn2 = document.querySelector('#btn2')
    btn2.addEventListener('click' , function(){

        //1.  ajax 객체 생성
        const xhr =  new XMLHttpRequest()

        // 2. 보낼 준비
        // 방식method, 주소 
        xhr.open('GET', '19_json.html')

        //3.  보내기 
        xhr.send()

        //4. 결과 확인
        xhr.onload = function() {
            console.log('다녀왔어')
            console.log(xhr.responseText )
        }
    })

    const btn3 = document.querySelector('#btn3')
    btn3.addEventListener('click' , function(){

        const key = '655611af65cce5c9d9eac89f849a00bb62592dfeef095490fbf938462cf0440e'

        //1.  ajax 객체 생성
        const xhr =  new XMLHttpRequest()

        let url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtFcst'
        url += '?'
        url += 'serviceKey='+key
        url += '&numOfRows=1000'
        url += '&pageNo=1'
        url += '&dataType=JSON'
        url += '&base_date=20260722'
        url += '&base_time=1500'
        url += '&nx=63'
        url += '&ny=110'

        // 2. 보낼 준비
        // 방식method, 주소 
        xhr.open('GET', url)

        //3.  보내기 
        xhr.send()

        //4. 결과 확인
        xhr.onload = function() {
            const data = JSON.parse(xhr.responseText)
            console.log(data)

            console.log(data.response.body.items.item[0].category)
            console.log(data.response.body.items.item[0].fcstValue)
            console.log(data.response.body.items.item[0].fcstTime)

            //category가 T1H(기온) , RN1(강수량) , REH(습도)
            let item = data.response.body.items.item
            // for(let i=0; i <item.length; i++) {
            //     if(item[i].category == 'T1H') {
            //         console.log(item[i])
            //     }else if(item[i].category == 'RN1') {
            //         console.log(item[i])
            //     }else if(item[i].category == 'REH') {
            //         console.log(item[i])
            //     }
            // }
          let filtered = item.filter (function(data){
            if(data.category == 'T1H' || data.category == 'RN1' || data.category == 'REH') {
                return true
            }
          })
          console.log(filtered)
        }
        // 문제1
        // 테이블로 표시
        // 예측카테고리 | 예측시간 | 값 

        // 문제2 
        // 시간 | 온도 | 습도 | 강수량 
    })

}