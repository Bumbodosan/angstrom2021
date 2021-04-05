from Crypto.Util.number import long_to_bytes

'''
When using RSA "e" is chosen such that e*d = 1 mod n
This implies that if e is large then d in small
If d is small we can use Wiener's attack (https://en.wikipedia.org/wiki/Wiener%27s_attack)
'''

n = 14750066592102758338439084633102741562223591219203189630943672052966621000303456154519803347515025343887382895947775102026034724963378796748540962761394976640342952864739817208825060998189863895968377311649727387838842768794907298646858817890355227417112558852941256395099287929105321231423843497683829478037738006465714535962975416749856785131866597896785844920331956408044840947794833607105618537636218805733376160227327430999385381100775206216452873601027657796973537738599486407175485512639216962928342599015083119118427698674651617214613899357676204734972902992520821894997178904380464872430366181367264392613853
e = 1565336867050084418175648255951787385210447426053509940604773714920538186626599544205650930290507488101084406133534952824870574206657001772499200054242869433576997083771681292767883558741035048709147361410374583497093789053796608379349251534173712598809610768827399960892633213891294284028207199214376738821461246246104062752066758753923394299202917181866781416802075330591787701014530384229203479804290513752235720665571406786263275104965317187989010499908261009845580404540057576978451123220079829779640248363439352875353251089877469182322877181082071530177910308044934497618710160920546552403519187122388217521799
c = 13067887214770834859882729083096183414253591114054566867778732927981528109240197732278980637604409077279483576044261261729124748363294247239690562657430782584224122004420301931314936928578830644763492538873493641682521021685732927424356100927290745782276353158739656810783035098550906086848009045459212837777421406519491289258493280923664889713969077391608901130021239064013366080972266795084345524051559582852664261180284051680377362774381414766499086654799238570091955607718664190238379695293781279636807925927079984771290764386461437633167913864077783899895902667170959671987557815445816604741675326291681074212227

def calc_frac(seq, curr, target):
    if curr == target - 1:
        return seq[curr]
    else:
        return seq[curr] + (1 / calc_frac(seq, curr + 1, target))

frac = continued_fraction(e / n)

for i in range(1, len(frac)):
    d = calc_frac(frac[ : i + 1], 0, i).denominator()
    res = long_to_bytes(pow(c, d, n))
    if b"actf{" in res:
        print(res.decode())
        break
