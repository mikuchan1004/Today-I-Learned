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
       
    })

    const btn4 = document.querySelector('#btn4')
    btn4.addEventListener('click' , function(){
        const xhr2 = new XMLHttpRequest()

        xhr2.open('GET' , 'https://jsonplaceholder.typicode.com/users')

        xhr2.send()

        xhr2.onload = function() {
            const result = JSON.parse(xhr2.responseText)
            console.log(result[0])
            // console.log(result[1]['name'])
            // console.log(result[0].name)
            // console.log(result[0].address.zipcode)
            // console.log(result[0].company.name)

            const tbody = document.querySelector('#member')
            for (i = 0; i < result.length; i++) {
                const tr = document.createElement('tr')
                tbody.append(tr) 

                const td = document.createElement('td')
                td.textContent = result[i].id
                tr.append(td)

                const td2 = document.createElement('td')
                td2.textContent = result[i].name
                tr.append(td2)
                
                const td3 = document.createElement('td')
                td3.textContent = result[i].address.zipcode
                tr.append(td3)

                const td4 = document.createElement('td')
                td4.textContent = result[i].company.name
                tr.append(td4)

                // console.log(result[i].id)
                // console.log(result[i].name)
                // console.log(result[i].address.zipcode)
                // console.log(result[i].company.name)
            }
            
        }
    })

    const btn5 = document.querySelector('#btn5')
    btn5.addEventListener('click' , function(){

        // let a = undefined
        // try {
        //     a.push(1)
        // }catch(e) {
        //     console.log(e)
        // }

        const url = 'https://jsonplaceholder.typicode.com/users'

        // fetch(주소, 옵션json)
        fetch(url , {
            method: 'GET'
        }).then(function (response){
            return response.json()
        }).then(function(data){
            console.log(data)
        }).catch(function (error){
            console.error(error)
        })
            

    })
    const btn6 = document.querySelector('#btn6')
    btn6.addEventListener('click' , function(){
        debugger

        console.log('btn6 클릭')
        debug()
        console.log('끝')
    })

}

function debug() {
    
    let a = 1

    console.log(a)
}