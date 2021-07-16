import numpy as np

# 从日志文件中读取 loss
with open("1.txt") as f:
    a1 = f.read()
with open("2.txt") as f:
    a2 = f.read()
l1=a1.split(" ")
l2=a2.split(" ")
loss1 = []
loss2 = []
for i in range(len(l1)):
    if l1[i] == "=":
        loss1.append(float(l1[i+1]))
for i in range(len(l2)):
    if l2[i] == "=":
        loss2.append(float(l2[i+1]))
train1 = loss1[::2]
val1 = loss1[1::2]
train2 = loss2[::2]
val2 = loss2[1::2]

# 画图
import matplotlib.pyplot as plt
plt.rcParams["font.size"] = 18
plt.figure(1,figsize=(10,6))
x=range(1,len(val1)+1)
m1 = 46
m2 = 57

plt.ylim(0,0.7)
plt.xlim(-5,200)
plt.ylabel("loss")
plt.xlabel("epoch")
plt.plot(x,val1,c='deepskyblue')
plt.plot(x,train1,c='royalblue')
plt.axvline(m1,ls="--",c='deepskyblue')
plt.plot(x,val2,c='lightcoral')
plt.plot(x,train2,c='red')
plt.axvline(m2,ls="--",c='r')
plt.text(m1,0.7,str(m1),c="deepskyblue",fontsize=16)
plt.text(m2,0.7,str(m2),c="r",fontsize=16)
plt.legend(("val (SDSS)","train (SDSS)","model (SDSS)","val (DESI)","train (DESI)","model (DESI)"),loc=1,fontsize=12)
plt.savefig("1.png",dpi=300)