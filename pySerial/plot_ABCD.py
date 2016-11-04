###############
# 
# script to read and plot ABCD data
# 
# Date: Oct. 30, 2016
# Author: Qianshu Lu

import numpy as np
import matplotlib.pyplot as plt

filenames = ['ABCD_20161027_LabVIEW.txt', 'ABCD_20161027_152722.txt']
A_L, B_L, C_L, D_L = np.loadtxt(filenames[0], delimiter=',', unpack=True)
A, B, C, D = np.loadtxt(filenames[1], unpack=True)
print(A)
print(B)
print(C)
print(D)

plt.style.use('color')
figA, axA = plt.subplots()
axA.plot(A)
axA.plot(A_L)
axA.set_xlabel("time [second]")
axA.set_ylabel("counts")
figA.suptitle("A count from LabVIEW and pySerial")
axA.legend(["pySerial", "LabVIEW"], frameon=False)

figB, axB = plt.subplots()
axB.plot(B)
axB.plot(B_L)
axB.set_xlabel("time [second]")
axB.set_ylabel("counts")
figB.suptitle("B count from LabVIEW and pySerial")
axB.legend(["pySerial", "LabVIEW"], frameon=False)

figC, axC = plt.subplots()
axC.plot(C)
axC.plot(C_L)
axC.set_xlabel("time [second]")
axC.set_ylabel("counts")
figC.suptitle("C count from LabVIEW and pySerial")
axC.legend(["pySerial", "LabVIEW"], frameon=False)

figD, axD = plt.subplots()
axD.plot(D)
axD.plot(D_L)
axD.set_xlabel("time [second]")
axD.set_ylabel("counts")
figD.suptitle("D count from LabVIEW and pySerial")
axD.legend(["pySerial", "LabVIEW"], frameon=False)

plt.show()
