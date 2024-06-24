#!/usr/bin/python
from poetry import cu_gala as gala 
from poetry import _options
import math
import time 
start_time = time.time()  # 获取开始时间  

# ----------- start 读取配置文件, 生成 output folder -----------
import argparse
import json
from pathlib import Path
# Create the parser
parser = argparse.ArgumentParser(description='Read a config file.')
parser.add_argument('--config', type=str, help='Path to the config file')
args = parser.parse_args()
if not args.config:
    print("ERROR: config file is not provided!")
    exit()

with open(args.config) as f:
    config = json.load(f)
### 待传入参数：数目
N0 = config['N0']  # N0=100 #mol0:异氰酸酯预聚体 NCO值=12.8  E(BA28B)3E 
N1 = config['N1']  # N1=5 #mol1:PTMG1000
N2 = config['N2']  # N2=0 #mol2:PTMG2000
N3 = config['N3']  # N3=10 #mol3:330N
N4 = config['N4']  # N4=0 #mol4:BDO
N5 = config['N5']  # N5=0 #mol5:水
Temperature = config.get('Temperature',30)  #k

job_id = str(config['job_id'])
output_dir = Path.cwd()/job_id
output_dir.mkdir(parents=True, exist_ok=True)

import sys
# Remove '--config' and its value, to avoid conflict with poetry
if '--config' in sys.argv:
    index = sys.argv.index('--config')
    sys.argv.pop(index)  # Removes '--config'
    sys.argv.pop(index)  # Removes '123.json'

print(f"N0: {N0}, N1: {N1}, N2: {N2}, N3: {N3}, N4: {N4}, N5: {N5}, output_dir: {output_dir}") 
# ----------- end  -----------

from poetry import cu_gala as gala 
from poetry import _options
##待传入参数1.数目 2.温度 3.反应概率
N0=100 #mol0:异氰酸酯预聚体 NCO值=12.8  E(BA28B)3E 
N1=5 #mol1:PTMG1000
N2=0 #mol2:PTMG2000
N3=10 #mol3:330N
N4=10 #mol4:BDO
N5=0 #mol5:水

T=1.0


# dt = 0.005
# # Temperature = 30  #k
# T = (Temperature+273.15)*8.3143/1000.0#reduced unit
# Pressure =1
# P =Pressure/16.3882449645417

# Ea_active=50
# k_b=8.314*10**(-3)
# T0=273.15+50
# Ea0=33
# probability=math.exp(Ea0/(k_b*T0))*math.exp(-Ea_active/(k_b* (Temperature+273.15)))
# print(probability)
# # exit()

N1_Pr=1  #PTMG1000
N2_Pr=0.5  #PTMG2000
N3_Pr1=0.6  #330N
N3_Pr2=0.7
N3_Pr3 =0.8
N4_Pr =0.9   #BDO
N5_Pr=0.4   #水 
N6_Pr=0.1   #氨基甲酸分解
N7_Pr=0.2   #胺
N8_Pr=0.3   #脲   

reaction_probabilities = {
    ('E', 'F'): N1_Pr,
    ('E', 'L'): N2_Pr,
    ('E', 'K01'): N3_Pr1,
    ('E', 'K02'): N3_Pr2,
    ('E', 'K03'): N3_Pr3,
    ('E', 'C'): N4_Pr,
    ('E', 'O'): N5_Pr,
}

#1皮秒的物理过程，需要执行1/0.005 = 200个时间步长

# 根据摩尔数是否为0来确定布尔开关
N0_switch = int(N0 != 0)  # 如果N0不为0，则为1，否则为0
N1_switch = int(N1 != 0)
N2_switch = int(N2 != 0)
N3_switch = int(N3 != 0)
N4_switch = int(N4 != 0)
N5_switch = int(N5 != 0)


dt = 0.002
P=1.0
filename = "NCO_"+ str(N0) +"_PTMG1000_"+str(N1)+"_PTMG2000_"+str(N2)+"_330N_"+str(N3)+"_BDO_"+str(N4)+"_H2O_"+str(N5)+'.xml'
build_method = gala.XMLReader(filename)
perform_config = gala.PerformConfig(_options.gpu)
all_info = gala.AllInfo(build_method, perform_config)
app = gala.Application(all_info, dt)  # build up an application with system information and integration time-step

epsilonHH=6
epsilonSS=1
epsilonSH=2.449
sigma=1
alpha=1
k=30
r0=1.5   #最大键长                                      
b0=0.97  #平衡键长
epsilon0=5
# rcut1=(2)**(1./6.) #cut- off of wca potential

# rcut2=2.5

#异氰酸酯NCO
N0_particles=["E","B","A"]
N0_bond=["E-B","B-A","B-B","A-A"]
N0_change_type=["E"]
N0_new_bond=["B-E1"]
N0_soft_particles=["A"]
N0_hard_particles=["B", "E", "E1"]


#PTMG1000
N1_Pr=N1_Pr
N1_particles=["F","G"]
N1_bond=["F-G","G-G"]
N1_change_type=["F"]
N1_new_bond=["E1-F1"]
N1_soft_particles=["G"]
# N1_hard_particles=["F1"]

#PTMG2000
N2_Pr=N2_Pr
N2_particles=["L","M"]
N2_bond=["L-M","M-M"]
N2_change_type=["L"]
N2_new_bond=["E1-L1"]
N2_soft_particles=["M"]
# N2_hard_particles=["L1"]

#330N
N3_Pr1=N3_Pr1
N3_Pr2=N3_Pr2
N3_Pr3=N3_Pr3
N3_particles=["I","J","K01","K02","K03"]
N3_bond=["I-J","J-J","J-K01","J-K02","J-K03"]
N3_change_type=["K01", "K02", "K03"]
N3_new_bond=["E1-K011","E1-K021","E1-K031"]
N3_soft_particles=["J"]
# N3_hard_particles=["K011","K021","K031"]


#BDO
N4_Pr=N4_Pr
N4_particles=["C","D"]
N4_bond=["C-D"]
N4_change_type=["C"]
N4_new_bond=["E1-C1"]
N4_soft_particles=["C"]
# N4_hard_particles=["C1"]

#水
N5_Pr=N5_Pr
N5_particles=["O","H"]
N5_bond=["O-H"]
N5_change_type1=["O"]
N5_new_type1=["O1", "H1"]
N5_new_type2=["O2","O3","O4","E2"]
N5_new_bond1=["E1-O1"]  #NCO+水=氨基甲酸
N5_new_bond2=["B-E2","O2-E2"]  #氨基甲酸=胺+二氧化碳
N5_new_bond3=["O3-E2", "E1-O3"]  #胺+异氰酸酯=脲
N5_new_bond4=["O4-E2", "E1-O4"]  #脲+异氰酸酯=缩二脲
N5_new_type=N5_new_type1+N5_new_type2
N5_new_bond= N5_new_bond1+ N5_new_bond2+ N5_new_bond3+ N5_new_bond4
N5_soft_particles=["O"]
N5_hard_particles=["E1"]


#######################################################################

old_particles = N0_switch * N0_particles + N1_switch * N1_particles + N2_switch * N2_particles + N3_switch * N3_particles + N4_switch * N4_particles + N5_switch * N5_particles
old_bond=  N0_switch * N0_bond + N1_switch * N1_bond + N2_switch * N2_bond + N3_switch * N3_bond + N4_switch * N4_bond + N5_switch * N5_bond
change_typelist1=  N0_switch * N0_change_type + N1_switch * N1_change_type + N2_switch * N2_change_type + N3_switch * N3_change_type + N4_switch * N4_change_type 
new_typelist2=N5_switch * N5_new_type
new_bond= N0_switch * N0_new_bond + N1_switch * N1_new_bond + N2_switch * N2_new_bond + N3_switch * N3_new_bond + N4_switch * N4_new_bond + N5_switch * N5_new_bond

ChangeTypeInReaction1=  N0_switch * N0_change_type + N1_switch * N1_change_type + N2_switch * N2_change_type + N3_switch * N3_change_type + N4_switch * N4_change_type+ N5_switch *N5_change_type1

hard_particles=N0_switch*N0_hard_particles+ N5_switch*N5_hard_particles
soft_particles=N0_switch * N0_soft_particles + N1_switch * N1_soft_particles + N2_switch * N2_soft_particles + N3_switch * N3_soft_particles + N4_switch * N4_soft_particles + N5_switch * N5_soft_particles
# print("old_particles:",old_particles)
# print("old_bond:",old_bond)
# print("change_typelist:",change_typelist1)
# print("new_bond:",new_bond)
# print("hard_particles:",hard_particles)
# print("soft_particles:",soft_particles)
# exit()
#######################################################################
#          all sorts list 
#######################################################################
# old_soft_particles=["A","B","C", "D","E","F","G", "H","I","J", "K01", "K02", "K03", "L","M","O"]
# old_bond=["E-B","B-A","B-B","A-A","F-G","G-G","L-M","M-M","I-J","J-J","J-K01","J-K02","J-K03","C-D","O-H"]
# change_typelist = ["C", "E", "F", "K01", "K02", "K03", "L", "O"]
# new_bond=["C1-E1", "E1-F1", "E1-L1","E1-O1","E1-O1","E1-K011","E1-K021","E1-K031"]

# hard_particles=["B", "E", " E1"]
# soft_particles=["A", "G","M", "J" ]
# old_particles/old_bond/change_typelist/new_bond/soft_particles

HH_pairs=[]
for i in range(len(hard_particles)):
    for j in range(i, len(hard_particles)):
        H1=hard_particles[i]
        H2=hard_particles[j]
        hard_pairs=(H1,H2)
        HH_pairs.append(hard_pairs)

HS_pairs=[]
for i in range(len(hard_particles)):
    for j in range(len(soft_particles)):
        H=hard_particles[i]
        S=soft_particles[j]
        hard_soft_pairs=(H,S)
        HS_pairs.append(hard_soft_pairs)
# print("HH_pairs:",HH_pairs)
# print("HS_pairs:",HS_pairs)
# exit()

new_list1=[]
for particle in change_typelist1:
    new_particles = f"{particle}1"
    new_list1.append(new_particles)
new_list=new_list1+ new_typelist2
# print("new_list:",new_list)

# print(new_list)
# exit()
for new_particles in new_list:
    all_info.addParticleType(new_particles)
#     print("all_info.addParticleType",new_particles)
# exit()
all_particles=old_particles+new_list
all_bond=old_bond+ new_bond
# # 使用列表推导式和条件语句去重，并保持原始顺序
# all_particles = [x for i, x in enumerate(all_particles) if x not in all_particles[:i]]

# 打印去重后的列表
# print("all_particles:",all_particles)
# print("all_bond:",all_bond)
# exit()
neighbor_list = gala.NeighborList(all_info, 2.5 ,0.25)#(,rcut,rbuffer)

#######################################################################
#          LJForce 
# #######################################################################
# WCA1= gala.LJForce(all_info, neighbor_list,  rcut1*sigma)
# for i in range(len(all_particles)):
#     for j in range(i, len(all_particles)):
#         particle1 = all_particles[i]
#         # if i != j:
#         particle2 = all_particles[j] 
#         if (particle1, particle2) in HH_pairs:
#             epsilon = epsilonHH
#         elif (particle1, particle2) in HS_pairs:
#             epsilon = epsilonSH
#         else:
#             epsilon = epsilonSS
#         WCA1.setParams(f"{particle1}", f"{particle2}", epsilon ,sigma ,alpha)
#         print("WCA1.setParams"f"{particle1}", f"{particle2}", epsilon ,sigma ,alpha)

# WCA1.setEnergy_shift()
# app.add(WCA1)

# #######################################################################
# #          WCA2--ordinary particles
# #######################################################################
# WCA2= gala.LJForce(all_info, neighbor_list,  rcut1*sigma)
# for i in range(len(all_particles)):
#     for j in range(i, len(all_particles)):
#         particle1 = all_particles[i]
#         # if i != j:
#         particle2 = all_particles[j] 
#         if (particle1, particle2) in HH_pairs:
#             epsilon = 0
#         elif (particle1, particle2) in HS_pairs:
#             epsilon = 0
#         else:
#             epsilon = epsilonSS
#         WCA2.setParams(f"{particle1}", f"{particle2}", epsilon ,sigma ,alpha)
#         print("WCA2.setParams"f"{particle1}", f"{particle2}", epsilon ,sigma ,alpha)
# WCA2.setEnergy_shift()
# # app.add(WCA2)
# #######################################################################
# #          LJForce--Hydrogen bond
#######################################################################
LJ = gala.LJForce(all_info, neighbor_list, 2.5) #( , , rcut)
# 循环遍历列表，并为每个元素与其自身配对
# print(sigma)
for i in range(len(all_particles)):
    for j in range(i, len(all_particles)):
        particle1 = all_particles[i]
        # if i != j:
        particle2 = all_particles[j] 
        if (particle1, particle2) in HH_pairs:
            epsilon = epsilonHH
        elif (particle1, particle2) in HS_pairs:
            epsilon = epsilonSH
        else:
             epsilon = epsilonSS
        LJ.setParams(f"{particle1}", f"{particle2}", epsilonSS ,sigma ,alpha)
        # print("lj.setParams"f"{particle1}", f"{particle2}", epsilon ,sigma ,alpha)
# exit()
app.add(LJ)
#######################################################################
#          FENE 
#######################################################################
all_info.addBondTypeByPairs()
FENE = gala.BondForceFENE(all_info) # bond stretching interaction by harmonic potential
#反应物本身的化学键
for i in range(len(all_bond)):
    bond=all_bond[i]
    FENE.setParams(f"{bond}",k, r0)
    print(f"{bond}",k, r0)
app.add(FENE)

# exit()
group = gala.ParticleSet(all_info, "all")# a collection of particles
comp_info = gala.ComputeInfo(all_info, group)  # calculating system informations, such as temperature, pressure, and momentum

npt = gala.NPT(all_info, group, comp_info, comp_info,T, P, 0.5 ,1.0) #( 温度，压力,tauT, tauP)
app.add(npt)

sort_method = gala.Sort(all_info) # memory sorting to improve data reading performance 
sort_method.setPeriod(80)
app.add(sort_method)
                                                                                                                                                                                                                                                                                                                                                                                     
zm = gala.ZeroMomentum(all_info) 
zm.setPeriod(100) 
app.add(zm) 

name="NCO_"+ str(N0) +"_PTMG1000_"+str(N1)+"_PTMG2000_"+str(N2)+"_330N_"+str(N3)+"_BDO_"+str(N4)+"_H2O_"+str(N5)

DInfo = gala.DumpInfo(all_info, comp_info, 'data.log')
DInfo.setPeriod(500)# (period)
DInfo.dumpBoxSize()
DInfo.dumpVirial(LJ)
DInfo.dumpVirial(FENE)
DInfo.dumpVirialMatrix(LJ)
DInfo.dumpVirialMatrix(FENE)
app.add(DInfo)

#write bin file
binary2 = gala.BinaryDump(all_info, name)
binary2.setPeriod(10000)# (period)
binary2.setOutput(['image', 'bond'])
binary2.setOutputForRestart()
app.add(binary2)
 

xml = gala.XMLDump(all_info, "allparticles") # output the configuration files in xml formatxml.setPeriod(100000)# (period)
xml.setPeriod(1000)# (period)
xml.setOutputType(True)
xml.setOutputBond(True)
xml.setOutputImage(True)
xml.setOutputVelocity(True)
xml.setOutputInit(True)
xml.setOutputCris(True)
xml.setOutputPotential(True)
# xml.setOutputLocalVirial(True)
# xml.setOutputMass(True)
app.add(xml)
app.run(10000)

#######################################################################
#          resize box
#######################################################################
v = gala.VariantLinear()
v.setPoint(500000, 100) # time step, box length.
v.setPoint(1000000, 40)

axs = gala.AxialStretching(all_info, group)
axs.setBoxLength(v, 'Y')
axs.setBoxLength(v, 'X')
axs.setBoxLength(v, 'Z')
app.add(axs)
app.run(500000)
# exit()
app.remove(lnvt)
app.remove(axs)
# exit()
npt = gala.NPT(all_info, group, comp_info, comp_info,T, P, 0.5 ,1.0) #( 温度，压力,tauT, tauP)
app.add(npt)
app.remove(WCA1)
app.add(LJ)
app.add(WCA2)
#######################################################################
#          Polymerization
#######################################################################
reaction1 = gala.Polymerization(all_info, neighbor_list, 2**(1.0/6.0), 16361)
#(func_rule, K, r_0, b_0, epsilon0, function)
#设置反应概率，E和每一个change_type
# change_typelist = ["C", "E", "F", "K01", "K02", "K03", "L", "O"]
pp_particles= N1_switch * N1_change_type + N2_switch * N2_change_type + N3_switch * N3_change_type + N4_switch * N4_change_type + N5_switch * N5_change_type1
init_particles=N0_switch *N0_change_type
# print(reaction_particles)
for i in range(len(init_particles)):
    for j in range(len(pp_particles)):
        p=init_particles[i]
        pp=pp_particles[j]
        if (p, pp) in reaction_probabilities:
        # 如果存在，获取对应的概率值
            reaction_probability = reaction_probabilities[(p, pp)]
            # 设置反应
            # 概率到 reaction1 对象中
            reaction1.setPr(p, pp, reaction_probability)
            # print("reaction1.setPr", (p, pp, reaction_probability))                   
    
# exit()
# reaction1.setPr('E' ,'F', 0.01)
# reaction1.setPr('E' ,'L', 0.01)
# reaction1.setPr('E' ,'K01', 0.01)
# reaction1.setPr('E' ,'K02', 0.01)
# reaction1.setPr('E' ,'K03', 0.01)
# reaction1.setPr('E' ,'C', 0.01)
# reaction1.setPr('E' ,'O', 0.01)

reaction_particles=init_particles+ pp_particles
# print(reaction_particles)
# exit()
reaction1.setNewBondTypeByPairs()
for i in range(len(reaction_particles)):
    reaction1.setMaxCris(reaction_particles[i], 1)
    # print("reaction1.setMaxCris",(reaction_particles[i], 1))
# reaction1.setMaxCris("E",  1)
# reaction1.setMaxCris("F",  1)
# reaction1.setMaxCris("L",  1)
# reaction1.setMaxCris("K01",  1)
# reaction1.setMaxCris("K02",  1)
# reaction1.setMaxCris("K03",  1)
# reaction1.setMaxCris("C",  1)
# reaction1.setMaxCris("O",  1)

for type in ChangeTypeInReaction1:
    reaction1.setChangeTypeInReaction(f"{type}",f"{type}1")
    # print("reaction1.setChangeTypeInReaction",(f"{type}",f"{type}1"))
# exit()
# reaction1.setChangeTypeInReaction("E", "E1")
# reaction1.setChangeTypeInReaction("F", "F1")
# reaction1.setChangeTypeInReaction("L", "L1")
# reaction1.setChangeTypeInReaction("K01", "K011")
# reaction1.setChangeTypeInReaction("K02", "K021")
# reaction1.setChangeTypeInReaction("K03", "K031")
# reaction1.setChangeTypeInReaction("C", "C1")
# reaction1.setChangeTypeInReaction("O", "O1")

reaction1.setPeriod(200)

xml.setPeriod(2000)
app.add(reaction1)


if N5_switch == 1:
    #depolymerization氨基甲酸分解成胺和CO2
    reaction2 = gala.DePolymerization(all_info, 1.0, 16361)
    reaction2.setParams('O-H', k, r0, b0, epsilon0, N6_Pr, gala.DePolyFunc.FENE)
    # sets bondname, k, r_0, b_0, epsilon0, Pr, and function.
    reaction2.setCrisQualify()
    reaction2.setChangeTypeInReaction("O1", "O2")
    reaction2.setChangeTypeInReaction("H", "H1")
    reaction2.setCountUnbonds(1000)
    reaction2.setPeriod(200)
    
    # app.run(30000)

    #polymerization:异氰酸酯+胺=脲
    reaction3 = gala.Polymerization(all_info, neighbor_list, 2**(1.0/6.0), 16361)
    #(func_rule, K, r_0, b_0, epsilon0, function)
    reaction3.setPr('E' ,'O2', N7_Pr)
    reaction3.setMaxCris("E",  1)
    reaction3.setMaxCris("O2",  2)
    reaction3.setNewBondTypeByPairs()
    reaction3.setChangeTypeInReaction("E", "E1")
    reaction3.setChangeTypeInReaction("O2", "O3")
    reaction3.setPeriod(200)

    #polymerization:异氰酸酯+脲=缩二脲
    reaction4 = gala.Polymerization(all_info, neighbor_list, 2**(1.0/6.0), 16361)
    #(func_rule, K, r_0, b_0, epsilon0, function)
    reaction4.setPr('E' ,'O3', N8_Pr)
    reaction4.setMaxCris("E",  1)
    reaction4.setMaxCris("O3",  3)
    reaction4.setNewBondTypeByPairs()
    reaction4.setChangeTypeInReaction("O3", "O4")
    reaction4.setPeriod(200)
  
    app.add(reaction3)
    app.add(reaction2)
    app.add(reaction4)

app.run(200000)

neighbor_list.printStats()

end_time = time.time()  # 获取结束时间  
  
elapsed_time = end_time - start_time  # 计算运行时间  
print(f"代码运行时间: {elapsed_time}秒")