from matplotlib import pyplot as plt, patches as pa
import seaborn as sns
import numpy as np
import random
import json

solar_generation1 = [0, 73038848, 143091455, 126369351, 187255410, 248244750, 352681169, 325432204, 427058152, 434109776, 460998426]
solar_generation2 = [0, 64016751, 122891914, 102364597, 204725674, 244765633, 327710166, 375055867, 341708443, 501589280, 501589280]
solar_generation3 = [0, 66508823, 90317589, 130513856, 173694188, 210953114, 270584454, 310581355, 341912713, 442340975, 457212646]
solar_generation4 = [0, 66508823, 90317589, 130513856, 173694188, 210953114, 270584454, 310581355, 341912713, 442340975, 457212646]
solar_generation5 = [0, 73038848, 133764619, 117042515, 177928574, 238917914, 343354333, 316105368, 394223968, 433493347, 468174437]
solar_generation6 = [0, 68747019, 91383052, 134708436, 193083220, 240141335, 322568588, 314483101, 399606768, 464175196, 483058297]

wind_generation1 = [499724830, 476499355, 479232273, 420899765, 349215465, 278116716, 292446256, 200334699, 239327121, 190025234, 182782299]
wind_generation2 = [659630534, 564661589, 540233662, 481224650, 420431971, 303529146, 259506414, 258183157, 196240082, 199979400, 199979400]
wind_generation3 = [613772249, 444095875, 474365254, 490775824, 382156112, 365817085, 239695742, 209736948, 218944666, 205175612, 189214027]
wind_generation4 = [896439504, 606271223, 679934595, 680842029, 561927879, 538507111, 393193131, 328498580, 371235900, 334203319, 320495371]
wind_generation5 = [735461564, 681527797, 754908897, 690552813, 550274186, 427054507, 434689484, 347570783, 342859890, 283682001, 316139979]
wind_generation6 = [931108574, 647591171, 560550956, 472157151, 520128161, 407508067, 359454578, 403007584, 340944184, 328486546, 323939734]

total_generation1 = [499724830, 549538204, 622323729, 547269116, 536470875, 526361466, 645127425, 525766903, 666385274, 624135010, 643780725]
total_generation2 = [659630534, 628678340, 663125577, 583589248, 625157645, 548294779, 587216581, 633239024, 537948526, 701568680, 701568680]
total_generation3 = [613772249, 510604699, 564682844, 621289681, 555850300, 576770199, 510280196, 520318304, 560857379, 647516587, 646426673]
total_generation4 = [896439504, 672780047, 770252184, 811355886, 735622067, 749460226, 663777585, 639079936, 713148613, 776544294, 777708017]
total_generation5 = [735461564, 754566646, 888673517, 807595328, 728202761, 665972421, 778043818, 663676151, 737083859, 717175349, 784314417]
total_generation6 = [931108574, 716338191, 651934009, 606865588, 713211382, 647649402, 682023167, 717490685, 740550953, 792661743, 806998032]

power_consumed = 145993167
percentage = np.array([0,10,20,30,40,50,60,70,80,90,100])

opacity = 1
sns.set_theme()
sns.set(font_scale=3)
# Plot
fig, ax = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
plt.plot(percentage, total_generation1,label='1 wind turbine')
plt.plot(percentage, total_generation2,label='2 wind turbines')
plt.plot(percentage, total_generation3,label='3 wind turbines')
plt.plot(percentage, total_generation4,label='4 wind turbines')
plt.plot(percentage, total_generation5,label='5 wind turbines')
plt.plot(percentage, total_generation6,label='6 wind turbines')
plt.hlines(power_consumed, 0, 100, linestyles='solid', label='Power consumed')
plt.xlabel('% with solar cells')
plt.ylabel('Power [MW]')
plt.xlim(0, 100)
#plt.title('Total power production for all cities', fontsize=30)
plt.yticks(plt.yticks()[0], [int(i/1000000) for i in plt.yticks()[0]], fontsize=30)
plt.grid(True, which='both', color="#93a1a1", alpha=0.3)
plt.legend(loc='best', fontsize=27)

plt.tight_layout()
plt.show()

fig2, ax2 = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
plt.plot(percentage, solar_generation1,label='1 wind turbine')
plt.plot(percentage, solar_generation2,label='2 wind turbines')
plt.plot(percentage, solar_generation3,label='3 wind turbines')
plt.plot(percentage, solar_generation4,label='4 wind turbines')
plt.plot(percentage, solar_generation5,label='5 wind turbines')
plt.plot(percentage, solar_generation6,label='6 wind turbines')
plt.hlines(power_consumed, 0, 100, linestyles='solid', label='Power consumed')
plt.xlabel('% with solar cells')
plt.ylabel('Power [MW]')
plt.xlim(0, 100)
#plt.title('Total solar production for all cities', fontsize=20)
plt.yticks(plt.yticks()[0], [int(i/1000000) for i in plt.yticks()[0]], fontsize=30)
plt.grid(True, which='both', color="#93a1a1", alpha=0.3)
plt.legend(loc='best', fontsize=27)

plt.tight_layout()
plt.show()

fig3, ax3 = plt.subplots(1, 1, figsize=(16, 9), dpi=80)
plt.plot(percentage, wind_generation1,label='1 wind turbines')
plt.plot(percentage, wind_generation2,label='2 wind turbines')
plt.plot(percentage, wind_generation3,label='3 wind turbines')
plt.plot(percentage, wind_generation4,label='4 wind turbines')
plt.plot(percentage, wind_generation5,label='5 wind turbines')
plt.plot(percentage, wind_generation6,label='6 wind turbines')
plt.hlines(power_consumed, 0, 100, linestyles='solid', label='Power consumed')
plt.xlabel('% with solar cells')
plt.ylabel('Power [MW]')
plt.xlim(0, 100)
#plt.title('Total wind production for all cities', fontsize=20)
plt.yticks(plt.yticks()[0], [int(i/1000000) for i in plt.yticks()[0]], fontsize=10)
plt.grid(True, which='both', color="#93a1a1", alpha=0.3)
plt.legend(loc='best', fontsize=16)

plt.tight_layout()
plt.show()