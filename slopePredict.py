class Table(dict):

    def __init__(self):
        self.value_indices = {}

    def set(self, i, j, v):
        self[(i, j)] = v
        if i in self.value_indices:
            self.value_indices[i].add(j)
        else:
            self.value_indices[i] = set([j])

    def read(self, i, j):
        return self.get((i, j), None)

    def hasValues(self, i):
        idx = self.value_indices.get(i, None)
        return idx

    def findB(self, i, j):
        column1 = self.hasValues(i)
        column2 = self.hasValues(j)
        if column1 & column2:
            overlap = column1.intersection(column2)
            slope = 0
            for hits in overlap:
                slope += self.read(j,hits) - self.read(i,hits)
            slope = (slope * 1.0)/ (1.0*len(overlap))
            return slope
        else:
            return 0

    def createSlopeTable(self):
        slopeTable = Table()
        users = 1
        nestedUsers = 1
        while(users < 19):
            while(nestedUsers < users):
                slopeTable.set(nestedUsers,users,self.findB(nestedUsers,users))
                nestedUsers += 1
            nestedUsers = 1
            users += 1
        return slopeTable

    def calculateRating(self, slopeTable, movie_id, user_id):
        foundMovie = False
        foundMovieRating = 0
        predictedRating = 0
        i = user_id - 1
        j = user_id + 1
        while(not foundMovie):
            if self.read(i,movie_id) is None:
                i -= 1
            else:
                foundMovie = True
                foundMovieRating = self.read(i,movie_id)
                print user_id
                print movie_id
                print foundMovieRating
                print i
                if slopeTable.read(user_id,i) is None:
                    predictedRating = foundMovieRating + slopeTable.read(i, user_id)
                    break
                else:
                    predictedRating = foundMovieRating + slopeTable.read(user_id,i)
                    break
            if self.read(j,movie_id) is None:
                j += 1
            else:
                foundMovie = True
                foundMovieRating = self.read(j,movie_id)
                print user_id
                print movie_id
                print foundMovieRating
                print j
                if slopeTable.read(user_id,j) is None:
                    predictedRating = foundMovieRating + slopeTable.read(j, user_id)
                    break
                else:
                    predictedRating = foundMovieRating + slopeTable.read(user_id,j)
                    break

        return predictedRating



#Table Creations
#slopeTable = Table()
baseTable = Table()

#reading data to baseTable
f = open('u1.base','r')
for line in f.readlines()[:1500]:
    line = line.split('\t')
    user_id = int(line[0])
    movie_id = int(line[1])
    rating = float(line[2])
    print user_id, movie_id, rating
    baseTable.set(user_id,movie_id,rating)
f.close()
print "-----------------------------------------"
slopeTable = baseTable.createSlopeTable()
print slopeTable
print "-----------------------------------------"
f1 = open('u1.test','r')
target1 = open('u_1.test.UnknownRating','w')
for line in f1.readlines()[:80000]:
    line = line.split('\t')
    userTest_id = int(line[0])
    movieTest_id = int(line[1])
    ratingTest = float(line[2])
    target1.write(str(userTest_id)+'\t'+str(movieTest_id)+'\t'+ str(baseTable.calculateRating(slopeTable,movieTest_id, userTest_id)))
    target1.write("\n")
target1.close()
f1.close()
f2 = open('u2.test','r')
target2 = open('u_2.test.UnknownRating','w')
for line in f2.readlines()[:80000]:
    line = line.split('\t')
    userTest_id = int(line[0])
    movieTest_id = int(line[1])
    ratingTest = float(line[2])
    target2.write(str(userTest_id)+'\t'+str(movieTest_id))
    target2.write("\n")
target2.close()
f2.close()
f3 = open('u3.test','r')
target3 = open('u_3.test.UnknownRating','w')
for line in f3.readlines()[:80000]:
    line = line.split('\t')
    userTest_id = int(line[0])
    movieTest_id = int(line[1])
    ratingTest = float(line[2])
    target3.write(str(userTest_id)+'\t'+str(movieTest_id))
    target3.write("\n")
target3.close()
f3.close()
f4 = open('u4.test','r')
target4 = open('u_4.test.UnknownRating','w')
for line in f4.readlines()[:80000]:
    line = line.split('\t')
    userTest_id = int(line[0])
    movieTest_id = int(line[1])
    ratingTest = float(line[2])
    target4.write(str(userTest_id)+'\t'+str(movieTest_id))
    target4.write("\n")
target4.close()
f4.close()
f5 = open('u5.test','r')
target5 = open('u_5.test.UnknownRating','w')
for line in f5.readlines()[:80000]:
    line = line.split('\t')
    userTest_id = int(line[0])
    movieTest_id = int(line[1])
    ratingTest = float(line[2])
    target5.write(str(userTest_id)+'\t'+str(movieTest_id))
    target5.write("\n")
target5.close()
f5.close()
print baseTable.calculateRating(slopeTable,6,1)


#f2 = open('u1.test', 'w')
#for line in f2.readlines()[:300]:
#    line = line.split('\t')
#    user_id = int(line[0])
#    movie_id = int(line[1])
