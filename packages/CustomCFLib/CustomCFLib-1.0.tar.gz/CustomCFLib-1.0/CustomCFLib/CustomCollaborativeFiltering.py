import mlflow


class MyCF(mlflow.pyfunc.PythonModel):
    def __init__(self,k):
        self.itemitem = { }
        self.k = k # k je maksimalni kartidalni broj skupa sličnih itema koje sustav preporuke razmatra prilikom računanja vrijednosti
        self._estimator_type = "CF"
    def get_params(self, deep=True):
        return {"k": self.k, "itemitem" : self.itemitem}

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

    def sim_pearson(self,x : dict, y : dict) :
        upper = 0

        xx = dict(x)
        yy = dict(y)

        sum_x = 0
        not_null_x = len(x.keys())

        for key in x.keys():
            sum_x += x[key]

        avg_x = sum_x / not_null_x

        sum_y = 0
        not_null_y = len(y.keys())

        for key in y.keys():
            sum_y += y[key]

        avg_y = sum_y / not_null_y


        for key in xx.keys() :
            val = xx[key]
            val -= avg_x
            xx[key] = val

        for key in yy.keys() :
            val = yy[key]
            val -= avg_y
            yy[key] = val


        for keyx in xx.keys() :
            if keyx in yy :
                upper += xx[keyx] * yy[keyx]

        sumx = 0
        for key in xx.keys() :
            val = xx[key]
            sumx += val * val

        sumy = 0
        for key in yy.keys() :
            val = yy[key]
            sumy += val * val

        lower = (sumx * sumy) ** 0.5

        return upper / lower

    # u[0] je id usera, u[1] je id itema
    def resolve(self,u):
        sim = []
        if self.itemitem.keys().__contains__(u[0]) == False:
           print("Vraćam nula jer ne postoji user s tim id")
           return 0;
        x1dict = self.itemitem[u[0]]
        for key in self.itemitem.keys() :
            if key != u[0] and u[1] in self.itemitem[key] :
                sim.append(self.sim_pearson(x1dict,self.itemitem[key]))
            else :
                sim.append(0.0)

        upper = 0
        lower = 0

        sorted_sim = sorted(sim)
        prag = sorted_sim[len(sorted_sim)-self.k]

        j = 0
        for key in self.itemitem.keys():
            similarity = sim[j]


            if similarity >= prag and similarity > 0:
                vals = self.itemitem[key]
                upper += similarity * vals[u[1]]
                lower += similarity
            j += 1

        return upper / lower


    # x je (user,item), a y ocjena
    def fit(self, X, y):
        if len(X) < self.k :
            print("NEUSPJELI FIT")
            return
        
        i = 0
        for x in X :
            if x[0] in self.itemitem :
                val = self.itemitem[x[0]]
            else :
                val = { }
            val[x[1]] = y[i]
            self.itemitem[x[0]] =val
            i += 1

    def predict(self, X):
        retval = self.resolve(X)
        print(retval)
        return retval
    
# cf = MyCF(10)
# #cf.fit([[1,1],[1,2],[1,4],[1,5],[2,1],[2,3],[2,5],[3,1],[3,2],[3,4],[4,2],[4,3],[4,5],[5,1],[5,3],[5,4]],[1,2,2,4,2,3,5,3,1,4,2,4,4,1,3,4])
# #cf.predict([5,6])

# infile = open('ratings.csv', 'r')
    
# X = []
# y = []

# for row in infile.readlines() :
#     podaci = row.split(',')
#     X.append([int(podaci[0]),int(podaci[1])])
#     y.append(float(podaci[2]))

# cf.fit(X,y)
# print("Gotov fit")

# start = time.time()


# end = time.time()
# print(end - start) # time in seconds

# print("Gotov predict")


