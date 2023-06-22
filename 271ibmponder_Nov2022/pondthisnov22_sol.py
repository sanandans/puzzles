'''
IBM Ponder This challenge main and bonus *, Nov 22
https://research.ibm.com/haifa/ponderthis/challenges/November2022.html
Sanandan Swaminathan, submitted November 4, 2022

Main puzzle ((a,b) pair with minimal b where b >= 10^99, that gives desired probability of 1/974170):
( 181099630723241346344069027701551470717620921946351872474266510613121261599083937652514613162744645 , 
178745427266283103396356876794706381419363113822085574712877761864488064025258658211419092995058294601 )

Bonus "*" puzzle (minimal D such that there are exactly 16 pairs (a,b) giving the probability 1/D, where b < 10^99):
D = 614

For the main puzzle, it is given that (a*(a-1)/2) / (b*(b-1)/2) = 1/974170.
974170*a*(a-1) = b*(b-1)
974170(a^2 - a) = b^2 - b
We can see that this looks like a Pell-like equation. We can make it a Pell-like equation. Multiply both sides by 4.
974170*4*(a^2 - a) = 4*(b^2 - b)
974170*(4(a^2) - 4a) = 4(b^2) - 4b
974170*(4(a^2) - 4a + 1) - 974170 = 4(b^2) - 4b + 1 - 1
974170*(2a - 1)^2 - 974170 = (2b - 1)^2 - 1
Let 2b - 1 = x, 2a - 1 = y.
974170(y^2) - 974170 = x^2 - 1
x^2 - 974170(y^2) = -974169
This is a Pell-like equation x^2 - Dy^2 = n, with D = 974170 and n = -974169.

I wrote a Python program that completed instantaneously for the main puzzle, and ran for 1 minute for the bonus "*" puzzle. To find the
 solutions for a Pell-like equation, we have to first find the smallest positive fundamental solution of the Pell equation 
x^2 - Dy^2 = 1. (0,1) cannot be a solution of the Pell equation. Though (1,0) is a trivial solution, we can ignore it as it cannot 
contribute a new solution for the Pell-like equation when the Pell-like equation is multiplied by (composed with) the Pell equation. I 
iterated through values of y to find the smallest positive fundamental solution of the Pell equation: (1948339, 1974). Let's denote 
this Pell equation fundamental solution as u + v(sqrt(D)). Next, we need to find the fundamental solutions of the Pell-like equation 
x^2 - Dy^2 = n. I read a good upper bound for y is sqrt(n*(u + v(sqrt(D)))/D). I've seen tighter upper bounds, but went with this. The 
fundamental solutions (x,y) for the Pell-like equation were [[1, 1], [229969, 233], [974169, 987]]. In order to find all solutions of 
the Pell-like equation, we should also take the conjugates as fundamental solutions. So, the list of fundamental solutions for the 
Pell-like equation becomes [[1, 1], [1, -1], [229969, 233], [229969, -233], [974169, 987], [974169, -987]]. As per the Brahmagupta 
identity, we can find all solutions of x^2 - Dy^2 = n by multiplying each of its fundamental solutions with powers of the smallest 
positive fundamental solution of the Pell equation x^2 - Dy^2 = 1. I loop to find higher solutions (x,y) of the Pell-like equation, 
looking for the smallest b = (x+1)/2 that is at least 10^99. The program completed instantaneously and gave the (a,b) pair
 
( 181099630723241346344069027701551470717620921946351872474266510613121261599083937652514613162744645 , 
178745427266283103396356876794706381419363113822085574712877761864488064025258658211419092995058294601 ).

Though my approach worked well for the main puzzle, it was clear that it was not a feasible approach for the bonus "*' question where 
we have to potentially solve many Pell-like equations x^ - Dy^2 = -(D-1), with different values of D. Firstly, the iterative search 
for the smallest positive fundamental solution of the Pell equation x^2 - Dy^2 = 1 would be slow. Even if I speeded that up by using 
the continued fractions approach, the loop search for the fundamental solutions of the Pell-like equation would be prohibitive when 
the u of u+v(sqrt(D)) is large since my upper bound for the search is  sqrt(n*(u + v(sqrt(D)))/D). Then I realized that the sympy 
python module has Diophantine functions including one for solving Pell/Pell-like equations that uses the fast Lagrange-Matthews-Mollin 
(LMM) algorithm. For the bonus "*" question, I loop on values of D to find the minimal D satisfying the desired conditions. For cases 
where D is a square number D = c^2, the equation x^2 - Dy^2 = n for negative n becomes (cy+x)(cy-x) = abs(n). This can be solved by 
checking factor pairs of n. I wrote a function for the cases where D is a square number. It reports if there are exactly 16 (a,b) 
pairs with b < 10^99, where the desired probability is 1/D. When D is not a square number, I use the sympy function to find the 
smallest positive fundamental solution of the Pell equation and to find the fundamental solutions of the Pell-like equation. If 
needed, I add the conjugates of the fundamental solutions of the Pell-like equation to the set. Then I build higher solutions where 
b < 10^99. If 17 solutions are found or all fundamental solutions have been exhausted for a given D, it tries the next higher D to see 
if it meets the given conditions. The program completed in 1 minute, and reported D = 614 as the minimal answer. 
The 16 (a,b) pairs were {(181173537300, 4489303317801), (126202292444491217690755, 3127169555940700738508245), (87910292284660494049994647574606406, 2178331188455673094183163567931676005), (61236759965938149379520674077028309729923293941, 1517387107323414063145964169594024212735875407961), (42656447540673847683386444657288136340070469244141556290440, 1056985111205082021832844216093149650560966382250603790530641), (29713729429877814592590158740119889043147493399197625285885500491515415, 736277196449842517713367084863633099010309275971088220118607819653871885), (20698060141790223179722752892970880982863553542565039195879796372401624406259456666, 512877716313317106275651036775473507147470473580378687867660623243977877315726726765), (14417903839508939458417837156890237441713924570473359083306747242452219890416814045051842816681, 357261576426783606071193730839191125209408241421759187474389205776166178797442957510297737636721), (167117648946, 4141012131556), (116411208387407336709295, 2884556055108802184108196), (81089995722927989644992465126459360, 2009330900448084610488176455230610240), (56485861605881131716334887794754261106739110861, 1399664485751594782050108607722241641899213003160), (39347055489566480067890660737432144450279617978215088968286, 974981608174841694081567110698429369770616295028247145271916), (27408465263417897127269516240532570250432446800268129054783633218555035, 679155001756546805993507409882980639716729335771622465777938685943801436), (19092253759501391587240115751429273719683759349945745072970234131385062406554832620, 473087402412025491508688168131073352444923160687867903598810592740191190502912437480), (13299327419974601231296219232967559178197793030991186723140083429944180872775619449732932882521, 329544345167300065381479674449333328589496523820294641667942375103769778034250524015512961937520)}.

'''

import math
from fractions import Fraction
import datetime
from sympy.solvers.diophantine import diophantine
from sympy import symbols
from sympy.solvers.diophantine.diophantine import diop_DN

def is_square(i):
    if i < 0:
        return False
    root = math.sqrt(i)
    return i == (int(root + 0.5))**2

print("starting ",datetime.datetime.now())
D = 974170
n = -974169
LIM=99
fund_u_list = []
fund_u_list = diop_DN(D, 1)
print("Fund unit sol list: ",fund_u_list)
ux = fund_u_list[0][0]
uy = fund_u_list[0][1]
if len(fund_u_list) != 1:
    print("Too many fund_u_list sols!")
if ux < 1 or uy < 1:
    print("Error in fund_u_list!")
fund_u_set = set()
for pair in fund_u_list:
    fund_u_set.add(tuple([abs(pair[0]),abs(pair[1])]))
    fund_u_set.add(tuple([abs(pair[0]),(-1)*abs(pair[1])]))
    fund_u_set.add(tuple([(-1)*abs(pair[0]),abs(pair[1])]))
    fund_u_set.add(tuple([(-1)*abs(pair[0]),(-1)*abs(pair[1])]))
print("Fund unit sol set: ",fund_u_set)

fund_sol_list = []
fund_sol_list = diop_DN(D, n)
print("Fund sol list: ",fund_sol_list)
fund_sol_set = set()
for pair in fund_sol_list:
    fund_sol_set.add(tuple([abs(pair[0]),abs(pair[1])]))
    fund_sol_set.add(tuple([abs(pair[0]),(-1)*abs(pair[1])]))
    fund_sol_set.add(tuple([(-1)*abs(pair[0]),abs(pair[1])]))
    fund_sol_set.add(tuple([(-1)*abs(pair[0]),(-1)*abs(pair[1])]))
print("Fund sol set: ",fund_sol_set)
minsolb=10**200
minsola=0
for s in fund_sol_set:
    for u in fund_u_set:
        x = s[0]
        y = s[1]
        while True:
            newx = (x*u[0]) + (y*u[1]*D)
            newy = (x*u[1]) + (y*u[0])
            x = newx
            y = newy
            if (abs(newx)%2 == 1) and (abs(newy)%2 == 1):
                b = (abs(newx)+1)//2
                a = (abs(newy)+1)//2
                if (b>1) and (a>0) and (b >= 10**LIM):
                    if b < minsolb:
                        minsolb = b
                        minsola = a
            if abs(newx) > 10**220:
                break
minsolx = (2*minsolb)-1
minsoly = (2*minsola)-1
print("n = ",(minsolx*minsolx) - (minsoly*minsoly*D))
print("Length of minsolx ",len(str(minsolx)),"Length of minsoly ",len(str(minsoly)))
if ((minsolb*(minsolb-1)) != (minsola*(minsola-1)*D)) or (len(str(minsolb)) < LIM+1):
    print("issue!")
print("Length of b ",len(str(minsolb)),"Length of a ",len(str(minsola)))
print("Probability = ",Fraction(minsola*(minsola-1),minsolb*(minsolb-1)))
print("Answer is (a,b) pair: (",minsola,",",minsolb,")")
print("done main", datetime.datetime.now())

#extra credit
TGTSOLS=16
def count_sols_squareD(given_d, given_n):
    #(sqrt_dy+x)(sqrt_dy-x)=n=j*i, j>i
    #y=(f)
    #b=(x+1)2, a=(y+1)/2, so x,y have to be odd.
    #y=(j+i)/2sqrt_d, x=(j-i)/2.
    sqrt_d = int(math.sqrt(given_d) + 0.5)
    paircnt=0
    #given_d is square, so given_n is not
    for i in range(1,int(math.sqrt(given_n) + 2)):
        if given_n%i == 0:
            j=given_n//i
            if (j>i) and ((j-i)%2 == 0) and ( ((j-i)//2)%2 == 1 ) and ((j+i)%(2*sqrt_d) == 0) and ( ((j+i)//(2*sqrt_d))%2 == 1 ):
                x=(j-i)//2
                y=(j+i)//(2*sqrt_d)
                b=(x+1)//2
                a=(y+1)//2
                if (b > 1) and (a>0) and (b < 10**LIM):
                    paircnt += 1
                    if paircnt > TGTSOLS:
                        break
    if paircnt == TGTSOLS:
        return True
    else:
        return False

D=2
while True:
    n=(-1)*(D-1)
    if D%100 == 0:
        print("D = ",D,datetime.datetime.now())
    if is_square(D):
        if count_sols_squareD(D,abs(n)) == True:
            print("Answer is D = ",D)
            break
        else:
            D += 1
            continue
   
    fund_u_list = []
    fund_u_list = diop_DN(D, 1)
    ux = fund_u_list[0][0]
    uy = fund_u_list[0][1]
    if len(fund_u_list) != 1:
        print("Too many fund_u_list sols!")
    if ux < 1 or uy < 1:
        print("Error in fund_u_list!")
    fund_u_set = set()
    for pair in fund_u_list:
        fund_u_set.add(tuple([abs(pair[0]),abs(pair[1])]))
        fund_u_set.add(tuple([abs(pair[0]),(-1)*abs(pair[1])]))
        fund_u_set.add(tuple([(-1)*abs(pair[0]),abs(pair[1])]))
        fund_u_set.add(tuple([(-1)*abs(pair[0]),(-1)*abs(pair[1])]))

    solset = set()
    fund_sol_list = []
    fund_sol_list = diop_DN(D, n)
    fund_sol_set = set()
    for pair in fund_sol_list:
        fund_sol_set.add(tuple([abs(pair[0]),abs(pair[1])]))
        fund_sol_set.add(tuple([abs(pair[0]),(-1)*abs(pair[1])]))
        fund_sol_set.add(tuple([(-1)*abs(pair[0]),abs(pair[1])]))
        fund_sol_set.add(tuple([(-1)*abs(pair[0]),(-1)*abs(pair[1])]))
        if ((abs(pair[0]))%2 == 1) and ((abs(pair[1]))%2 == 1):
                b = (abs(pair[0]) + 1)//2
                a = (abs(pair[1]) + 1)//2
                if (b>1) and (a>0) and (b<10**LIM):
                    solset.add(tuple([a,b]))

    if len(solset) > TGTSOLS:
        D += 1
        continue
   
    trynextD=False
    for s in fund_sol_set:
        for u in fund_u_set:
            x = s[0]
            y = s[1]
            while True:
                newx = (x*u[0]) + (y*u[1]*D)
                newy = (x*u[1]) + (y*u[0])
                x = newx
                y = newy
                if (abs(newx)%2 == 1) and (abs(newy)%2 == 1):
                    b = (abs(newx)+1)//2
                    a = (abs(newy)+1)//2
                    if (b>1) and (a>0) and (b<10**LIM):
                        solset.add(tuple([a,b]))
                        if len(solset) > TGTSOLS:
                            trynextD=True
                            break
                if abs(newx) >= 10**(LIM+220):
                    break
               
            if trynextD == True:
                break

        if trynextD == True:
            break

    if len(solset) == TGTSOLS:
        maxlenb = 0
        maxb = 0
        for pair in solset:
            if ((pair[1]*(pair[1]-1) != pair[0]*(pair[0]-1)*D)) or (len(str(pair[1])) > LIM):
                print("issue! ",pair)
            if len(str(pair[1])) > maxlenb:
                maxlenb = len(str(pair[1]))
                maxb = pair[1]

        print("Maxlen of b: ",maxlenb)
        print("Max b: ",maxb)
        print("Fund unit sol list: ",fund_u_list)
        print("Fund unit sol set: ",fund_u_set)
        print("Fund sol list: ",fund_sol_list)
        print("Fund sol set: ",fund_sol_set)
        print("Answer is D = ",D," Num pairs = ",len(solset)," Sol set = ",solset)
        break
    D += 1
   
print("done extra credit", datetime.datetime.now())

