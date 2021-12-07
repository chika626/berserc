import sys
import yaml
import json
from matplotlib import pyplot as plt


def cuest_ATK(unitATK, unitGUTS, runeATK, runeHIGH, unitB):
    return unitATK*((9+unitGUTS)/10)*(1+runeATK+runeHIGH/5+unitB)

def mindYUURIHOSEI(unitHOSEI , selectnum):
    return (unitHOSEI*0.06)*selectnum

def cuest_HOSEI(unitHOSEI, mindYURI, mindOMAKE, runeZOKUSEI, seedBREAK, runeICHRYS, runeENHANCER):
    return ((unitHOSEI + mindYUURIHOSEI(unitHOSEI, mindYURI) + mindOMAKE) * (1+runeZOKUSEI)) + (seedBREAK * 5) + (runeICHRYS / 3) + (runeENHANCER / 3)

def YATK(cuest_ATK, cuest_HOSEI, seedSOUL, flagSPECIAL):
    return cuest_ATK * cuest_HOSEI * (1+seedSOUL)**5 * (1+flagSPECIAL*.35)

def DPS(damage, unitKANAKU, runeQUICK, unitGUTS, unitASS, monsterASS, wariai, runeARCHE = 0, runeBERSE=0.33):
    unitGUTS = min(11, unitGUTS)
    all_damage = damage * min(unitASS, monsterASS) / (unitKANAKU * (1 - runeQUICK) * (1 - (unitGUTS - 1)* 0.04))
    return  all_damage + (all_damage * (wariai) * (runeBERSE) * (runeBERSE) * 8) + (runeARCHE * all_damage * 0.5)

def yoD(damage, unitKANAKU, runeQUICK, unitGUTS, unitASS, monsterASS, wariai, runeARCHE = 0, runeBERSE=0.33):
    unitGUTS = min(11, unitGUTS)
    all_damage = damage * min(unitASS, monsterASS) / 5
    return  all_damage + (all_damage * (wariai) * (runeBERSE) * (runeBERSE) * 8) + (runeARCHE * all_damage * 0.5)

def HPS(unitHP, unitGUTS, runeHIGH, unitB, runeRIFE = 0):
    return unitHP * (0.9 + unitGUTS/10) * (1 + runeRIFE + runeHIGH/2 + unitB) / (1-unitB)

def createlist(runeARCHE=0, runeZOKUSEI = 0, unitGUTS = 28, runeHIGH = 0, runeRIFE = 0, unitB = 0, mindYURI = 0):
    unitATK = 7545
    unitKANAKU = 2.26
    unitASS = 1
    monsterASS = 1
    runeATK = 0.33
    runeQUICK = 0.33
    unitHOSEI = 1.6
    mindOMAKE = 0
    seedBREAK = 0.315
    runeICHRYS = 0
    runeENHANCER = 0
    seedSOUL = 0
    flagSPECIAL = 0
    unitHP = 5000
    
    hidamage = 1000
    zyoui_ari = []
    x_ari = []
    while True:
        ari_c = cuest_ATK(unitATK, unitGUTS, runeATK, runeHIGH, unitB)
        ari_zh = cuest_HOSEI(unitHOSEI, mindYURI, mindOMAKE, runeZOKUSEI, seedBREAK, runeICHRYS, runeENHANCER)
        ari_damage = YATK(ari_c, ari_zh, seedSOUL, flagSPECIAL)
        ari_HP = HPS(unitHP, unitGUTS, runeHIGH, unitB, runeRIFE)
        # 残りHPの計算
        ari_nokori_HP = ari_HP - hidamage
        ari_wariai = 1 - ari_nokori_HP / ari_HP

        keisan = False
        if ari_nokori_HP >= 0:
            ari_dps = DPS(ari_damage, unitKANAKU, runeQUICK, unitGUTS, unitASS, monsterASS, ari_wariai, runeARCHE)
            x_ari.append(hidamage)
            zyoui_ari.append(ari_dps)
            keisan = True
        hidamage += 1000
        if not keisan:
            break
    return zyoui_ari, x_ari

def debug():
    # zyoui_ari, x_ari = createlist(runeZOKUSEI = 0.30)
    # zyoui_arch, x_arch = createlist(runeARCHE = 0.30)
    # zyoui_guts, x_guts = createlist(unitGUTS = 30)
    # zyoui_nasi, x_nasi = createlist()
    # zyoui_zyoi, x_zyoi = createlist(runeHIGH= 0.30)
    # zyoui_rife, x_rife = createlist(runeRIFE= 0.30)
    # zyoui_bougo, x_bougo = createlist(unitB= 0.15)

    # plt.plot(x_ari, zyoui_ari, label="zokusei")
    # plt.plot(x_nasi, zyoui_nasi, label="none")
    # plt.plot(x_arch, zyoui_arch, label="arche")
    # plt.plot(x_guts, zyoui_guts, label="guts")
    # plt.plot(x_zyoi, zyoui_zyoi, label="zyoi")
    # plt.plot(x_rife, zyoui_rife, label="rife")
    # plt.plot(x_bougo, zyoui_bougo, label="bougo")
    a, b = createlist(mindYURI=2)
    c, d = createlist(runeARCHE=0.30)
    e, f = createlist(runeZOKUSEI=0.30)
    g, h = createlist(unitGUTS=30)
    plt.plot(b, a, label="yuri")
    plt.plot(d, c, label="arch")
    plt.plot(f, e, label="zokusei")
    plt.plot(h, g, label="guts")
    plt.legend()
    plt.show()

def RODAIN(runeARCHE=0, runeZOKUSEI = 0.33, unitGUTS = 12, runeHIGH = 0, runeRIFE = 0, unitB = 0.12, mindYURI = 0):
    unitATK = 10851
    unitKANAKU = 2.95
    unitASS = 3
    monsterASS = 3
    runeATK = 0.33
    runeQUICK = 0.33
    unitHOSEI = 1.75
    mindOMAKE = 0
    seedBREAK = 0.315
    runeICHRYS = 0
    runeENHANCER = 0
    seedSOUL = 0
    flagSPECIAL = 0
    unitHP = 8910
    
    hidamage = 0
    zyoui_ari = []
    x_ari = []
    while True:
        ari_c = cuest_ATK(unitATK, unitGUTS, runeATK, runeHIGH, unitB)
        ari_zh = cuest_HOSEI(unitHOSEI, mindYURI, mindOMAKE, runeZOKUSEI, seedBREAK, runeICHRYS, runeENHANCER)
        ari_damage = YATK(ari_c, ari_zh, seedSOUL, flagSPECIAL)
        ari_HP = HPS(unitHP, unitGUTS, runeHIGH, unitB, runeRIFE)
        # 残りHPの計算
        ari_nokori_HP = ari_HP - hidamage
        ari_wariai = 1 - ari_nokori_HP / ari_HP

        keisan = False
        if  1 >= ari_wariai:
            ari_dps = DPS(ari_damage, unitKANAKU, runeQUICK, unitGUTS, unitASS, monsterASS, ari_wariai, runeARCHE)
            x_ari.append(hidamage)
            zyoui_ari.append(ari_dps)
            keisan = True
        hidamage += 1000
        if not keisan:
            break
    print("G: ",unitGUTS, " ",HPS(unitHP, unitGUTS, runeHIGH, unitB, runeRIFE))
    return zyoui_ari, x_ari

def RODAIN_DEBUG():
    yo, x = RODAIN()
    yo_G, x_G = RODAIN(unitGUTS=14)
    yo_B, x_B = RODAIN(unitB=0.15)
    yo_Z, x_Z = RODAIN(runeHIGH=0.33)
    yo_GB, x_GB = RODAIN(unitGUTS=14, unitB=0.15)
    yo_GZ, x_GZ = RODAIN(unitGUTS=14, runeHIGH=0.33)
    yo_BZ, x_BZ = RODAIN(unitB=0.15, runeHIGH=0.33)
    yo_GBZ, x_GBZ = RODAIN(unitGUTS=14, unitB=0.15, runeHIGH=0.33)
    plt.plot(x, yo, label="none")
    plt.plot(x_G, yo_G, label="guts=27.001")
    plt.plot(x_B, yo_B, label="bougo=15.000")
    plt.plot(x_Z, yo_Z, label="zyoi=27.021")
    plt.plot(x_GB, yo_GB, label="guts=27.001 bougo=15.000")
    plt.plot(x_GZ, yo_GZ, label="guts=27.001 zyoi=27.021")
    plt.plot(x_BZ, yo_BZ, label="bougo=15.000 zyoi=27.021")
    plt.plot(x_GBZ, yo_GBZ, label="all")
    # 正しくは29753????
    plt.legend()
    plt.show()


def main():
    # print(HPS(13525, 12, 0, 0))
    # debug()
    RODAIN_DEBUG()
    # import matplotlib.font_manager
    # print([f.name for f in matplotlib.font_manager.fontManager.ttflist])

        

# 4部位水打銃有利
# 5部位風斬魔有利

# How To Use
if __name__ == "__main__":
    main()