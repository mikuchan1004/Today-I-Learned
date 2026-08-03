total_sales = 0 # 전체 매출을 담을 바구니 

#  조건1. order.txt를 읽기 모드로 읽기
with open ('order.txt' , 'r' , encoding='utf-8') as file :
    lines = file.readlines()

    for line in lines :
        #  컴마 기준으로 자르기 
        items  = line.split(',')

        # 조건3. 텍스트 클랜징 
        # 앞뒤 공백 제거 
        # '원' 글자 제거
        name = items[0].strip()
        qty_str = items[1].strip()
        price_str = items[2].strip().replace('원' , '')

        # 수량과 가격은 정수형으로 변환
        quantity = int(qty_str)
        price = int(price_str)

        # 조건2. 이상치 제거 
        # 가격이 0보다 작거나, 10000보다 크거나 , 개수가 0보다 작으면 계산하지 않고 건너띔
        if price < 0 or price > 10000 or quantity < 0 :
            continue 

        # 조건 4 : 전체 매출 구하기 

        # 수량과 가격을 곱해서 전체 매출 바구니에 담는다
        total_sales += (quantity * price)

# 전체 매출 
print(f"전체 매출 :  {total_sales} 원" )


    
