'''
반장선거

let names = ['규혁', '근욱', '영욱', '상우', '용준', '도영', '재성', '준석']
1. 랜덤으로 1명을 고른다
2. 1.의 행동을 100번 반복한다
3. 누가 몇표가 나왔는지 출력한다
4. 가장 많은 득표수는 누구, 몇표만 출력한다
'''
import random

names = ['규혁' , '근욱' , '영욱' , '상우' , '용준' , '도영', '재성' , '준석']  
votes = {}
for i in range(100):
    vote = random.choice(names)
    votes[vote] = votes.get(vote, 0) + 1
print(votes)

print('가장 많은 득표수 : ' , max(votes),votes[max(votes)] , '표') 