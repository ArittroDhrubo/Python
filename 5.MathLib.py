import math

#Level-1

a = 10
b = 5
c = 2
d = 7

res1 = 0 
res1 += b
print(res1)
res1 *= d
print(res1)
a /= b
print(a)
d %= b
print(d) 
res1 -= d
print(res1)

print(f"res1: {res1}")
print(f"a: {a}")
print(f"b: {b}")

MinNum = min(res1,a,b)
MaxNum = max(res1,a,b)

print(f"Minimum: {MinNum}")
print(f"Minimum: {MaxNum}")

res2 = b-res1
res3 = abs(res2)
print(res2)
print(res3)

res4 = pow(res3,3)
print(res4)

#Level-2

print(math.pi)
print(math.e)
num1 = 9.67
num2 = 456.894572892

print(f"Ceil Value: {math.ceil(num1)}")
print(f"Floor Value: {math.floor(num2)}")
print(f"Sqrt Value: {math.sqrt(4)}")
print(round(num2,2))

#Level-3

radius = float(input("What is the radius? : "))

Area = math.pi * pow(radius,2)

Circumferance = 2 * math.pi * radius

print(f"Area of The Circle: {round(Area,3)}")

print(f"Circumferance of The Circle: {round(Circumferance,3)}")