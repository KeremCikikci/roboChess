import math

tahtaYKonumu = 200
yükseklik = 20

minSapma = 5 # son kare icin bu kadar fazla söylüyor 20
maxSapma = 45 # ilk kare icin bu kadar fazla söylüyor 300
deltaSapma = maxSapma - minSapma

yerdenYükseklik = 104
masadanUzaklik = 95
masadanYükseklik = 95
deltaYükseklik = yerdenYükseklik - masadanYükseklik

birinciKol = 234
ikinciKol = 224
sonKol = 95


yKonumu = tahtaYKonumu + masadanUzaklik - (maxSapma - deltaSapma / 280 * (tahtaYKonumu-20))
print(yKonumu)



# Alpha birinci motor acisi
alpha = 90
# Beta ikinci motor acisi
beta = math.degrees(math.acos((birinciKol**2 + ikinciKol**2 - yKonumu**2) / (2 * birinciKol * ikinciKol)))
alpha = math.degrees(math.acos((birinciKol**2 + yKonumu**2 - ikinciKol**2) / (2 * birinciKol * yKonumu))) + math.degrees(math.asin(yükseklik/yKonumu))

# Gama ucuncu motor acisi

print(alpha, beta)