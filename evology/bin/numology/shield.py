import numpy as np

WealthNT = 150000
WealthVI = 10000
WealthTF = 111000
TargetNT = 1/4
TargetVI = 1/2
TargetTF = 1/4

''' Addition: no negative transfer to avoid bankruptcies '''

WealthSum = WealthNT + WealthVI + WealthTF 
print([WealthNT / WealthSum, WealthVI / WealthSum, WealthTF / WealthSum])


if TargetTF + TargetVI + TargetNT != 1:
    raise ValueError('Target coordinates do not sum to 1.')

D = np.array([
[1-TargetNT,-TargetNT, -TargetNT], 
[-TargetVI, 1-TargetVI, -TargetNT],
[-TargetTF, -TargetTF, 1-TargetTF]]) 

Dx = np.array([
[TargetNT * WealthSum - WealthNT,-TargetNT, -TargetNT], 
[TargetVI * WealthSum - WealthVI, 1-TargetVI, -TargetNT],
[TargetTF * WealthSum - WealthTF, -TargetTF, 1-TargetTF]]) 

Dy = np.array([
[1-TargetNT, TargetNT * WealthSum - WealthNT, -TargetNT], 
[-TargetVI, TargetVI * WealthSum - WealthVI, -TargetNT],
[-TargetTF, TargetTF * WealthSum - WealthTF, 1-TargetTF]]) 

Dz = np.array([
[1-TargetNT, -TargetNT, TargetNT * WealthSum - WealthNT], 
[-TargetVI, 1-TargetVI, TargetVI * WealthSum - WealthVI],
[-TargetTF, -TargetTF, TargetTF * WealthSum - WealthTF]]) 

### 

TransferNT = np.linalg.det(Dx)/np.linalg.det(D)
TransferVI = np.linalg.det(Dy)/np.linalg.det(D)
TransferTF = np.linalg.det(Dz)/np.linalg.det(D)

# NewWealthNT = WealthNT + TransferNT
# NewWealthVI = WealthVI + TransferVI
# NewWealthTF = WealthTF + TransferTF
# print([NewWealthNT, NewWealthVI,NewWealthTF])
# NewSumWealth = NewWealthNT + NewWealthVI + NewWealthTF

# print(TransferNT, TransferVI, TransferTF)
# print([TargetNT, TargetVI, TargetTF])
# print([NewWealthNT / NewSumWealth, NewWealthVI / NewSumWealth, NewWealthTF / NewSumWealth])

print(TransferNT, TransferVI, TransferTF)

TransferNT = max((np.linalg.det(Dx)/np.linalg.det(D)),0)
TransferVI = max((np.linalg.det(Dy)/np.linalg.det(D)),0)
TransferTF = max((np.linalg.det(Dz)/np.linalg.det(D)),0)

NewWealthNT = WealthNT + TransferNT
NewWealthVI = WealthVI + TransferVI
NewWealthTF = WealthTF + TransferTF
# print([NewWealthNT, NewWealthVI,NewWealthTF])
NewSumWealth = NewWealthNT + NewWealthVI + NewWealthTF

print(TransferNT, TransferVI, TransferTF)
print([TargetNT, TargetVI, TargetTF])
print([NewWealthNT / NewSumWealth, NewWealthVI / NewSumWealth, NewWealthTF / NewSumWealth])




