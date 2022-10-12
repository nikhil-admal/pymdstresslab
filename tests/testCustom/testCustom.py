import pymdstresslab as pmsl
import numpy as np

class Custom(pmsl.MethodUser):
    def __init__(self, averagingDomainSize):
        super().__init__(averagingDomainSize)
        self.averagingDomainSize = averagingDomainSize
        self.normalizer = 8/(5 * np.pi * averagingDomainSize ** 3)
        self.constant = [self.normalizer]
        constantPolynomial = pmsl.Polynomial(self.constant)
        linear = [2 * self.normalizer, -2 * self.normalizer/averagingDomainSize]
        linearPolynomial = pmsl.Polynomial(linear)

        # Contruct Piecewise polynomial
        self.intervals = ((0, averagingDomainSize/2),(averagingDomainSize/2, averagingDomainSize))
        self.piecewisePolynomial = [constantPolynomial, linearPolynomial]

    def __call__(self, vec:np.ndarray):
        r = np.linalg.norm(vec)
        index = 0
        for i, interval in enumerate(self.intervals):
            if r >= interval[0] and r < interval[1]:
                index = i
                break
        return self.piecewisePolynomial[index](r)

    def bondFunction(self, vec1:np.ndarray, vec2:np.ndarray):
        r1 = np.linalg.norm(vec1); r2 = np.linalg.norm(vec2)
        a = 4 * np.linalg.norm(vec1 - vec2) ** 2
        b = 4 * (vec1.dot(vec2) - vec2.dot(vec1))**2 - a * r1 * r2
        sPerp =  (vec1.dot(vec2) - vec2.dot(vec1))/np.linalg.norm(vec1 - vec2)**2

        vecPerp = (1 - sPerp) * vec1 + sPerp * vec2
        rPerp = np.linalg.norm(vecPerp)
        #print(r1, r2, rPerp)
        ## assert(rPerp < (min(r1, r2) + 1e-8))
        
        if (rPerp > self.averagingDomainSize):
            return 0
        
        r1 = min(r1, self.averagingDomainSize)
        r2 = min(r2, self.averagingDomainSize)

        if ( sPerp < 0 or sPerp > 1):
            rmin = min(r1, r2)
            rmax = max(r1, r2)

            if (np.abs(rmax - rmin) > 1e-8):
                return self.integrate(a,b,rmin, rmax)
            else:
                return 0
        else:
            result = 0.0
            rmin = rPerp
            if (np.abs(r1 - rmin) > 1e-8):
                result = self.integrate(a, b, rmin, r1)
            if (np.abs(r2 - rmin) > 1e-8):
                result += self.integrate(a, b, rmin, r2)
            return result

    def integratePolynomial(self, degree:int, a:float, b:float, r1:float, r2:float):
        # assert(r1 <= r2)
        if (degree == 0):
            # assert(a * r2 ** 2 + b + 1e-8 > 0 and a * r1 ** 2 + b + 1e-8)
            return np.sqrt(a * r2 ** 2 + b + 1e-8) - np.sqrt(a * r1 ** 2 + b + 1e-8) 
        if (degree == 1):
            # assert(a * r2 ** 2 + b + 1e-8 > 0 and a * r1 ** 2 + b + 1e-8 and a > 0)
            tmp1 =np.sqrt(a) * np.sqrt( a * r1 ** 2 + b + 1e-8 )
            tmp2 =np.sqrt(a) * np.sqrt( a * r2 ** 2 + b + 1e-8 )
            return ((r2 * tmp2 - b * np.log(tmp2 + a * r2)) - 
                    (r1 * tmp1 - b * np.log(tmp1 + a * r1)))/(2 * a ** 1.5)
        raise ValueError(f"Degree {degree} polynomial not supported")
        return -1

    def integrate(self, a:float, b:float, rmin:float, rmax:float):
        # assert(rmin <= rmax and rmax <= self.averagingDomainSize)
        result = 0.0
        min_index = 0
        for i, interval in enumerate(self.intervals):
            if rmin >= interval[0] and rmin < interval[1]:
                index = i
                break
        max_index = 0
        for i, interval in enumerate(self.intervals):
            if rmax >= interval[0] and rmax < interval[1]:
                index = i
                break
        for i in range(min_index, max_index):
            if i == min_index :
                lb = rmin
            else:
                lb = self.intervals[min_index][0]

            if i == max_index :
                ub = rmax
            else:
                ub = self.intervals[max_index][1]

            degree = 0
            for coeff in self.piecewisePolynomial[i].coefficients:
                result += 2 * coeff * self.integratePolynomial(degree, a, b, lb ,ub)
                degree += 1
            if i == max_index:
                break
        return result



configFileName = "config.data"
modelname = "LJ_Smoothed_Bernardes_1958_Ar__MO_764178710049_001"

numberOfParticles = 4000

body = pmsl.Box(configFileName)
kim = pmsl.Kim(modelname)

ngrid = 10

gridFromFile = pmsl.Grid("Current", from_file="grid_cauchy.data")

hardy1 = Custom(5.29216036151419)

hardyStress1 = pmsl.Stress(hardy1, gridFromFile, name="hardy1", user_defined=True)

pmsl.calculateStress(body, kim, hardyStress1)

hardyStress1.write()
