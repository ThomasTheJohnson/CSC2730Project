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

        #calcB(T,i,j):
    def findOneB(self, movieTable, movieI, movieJ):
        slope = 0
        ratedMovieI = movieTable.hasValues(movieI)
        ratedMovieJ = movieTable.hasValues(movieJ)
        if ratedMovieI and ratedMovieJ:
            overlap = ratedMovieI.intersection(ratedMovieJ)
            if overlap:
                for users in overlap:
                    slope += self.read(users,movieJ) - self.read(users,movieI)
                B = slope/len(overlap)
                return B
            else:
                return 0
        else:
            return 0

#This is where our logic issue is. We are comparing users to users, we need to be comparing movies to movies.
#or maybe theyre just mislabeled, but we should check still.
    def createSlopeTable(self):
        slopeTable = Table()
        movies = 1
        nestedMovies = 1
        while(movies <= 1682):
            while(nestedMovies < movies):
                slopeTable.set(nestedMovies,movies,self.findOneB(movieTable,nestedMovies,movies))
                nestedMovies += 1
            nestedMovies = 1
            movies += 1
        return slopeTable

        #B = Table()
        #cols = T.getCols()
        #n = len(cols)
        #for i in range(n-1):
        # for j in range()

    def calculateRating(self, slopeTable, movie_id, user_id):
        ratedMovies = self.hasValues(user_id)
        avgMovieRatings = 0
        for movies in ratedMovies:
            avgMovieRatings += self.read(user_id,movies) + slopeTable.read(movies, movie_id)
        predictedRating = avgMovieRatings/len(ratedMovies)
        return predictedRating





#Table Creations
userTable = Table()
movieTable = Table()

f = open('u1.base','r')
for line in f.readlines():
    line = line.split('\t')
    user_id = int(line[0])
    movie_id = int(line[1])
    rating = float(line[2])
    userTable.set(user_id, movie_id,rating)
    movieTable.set(movie_id, user_id, rating)
f.close()
print userTable.findOneB(movieTable,16,17)
print "-----------------------------------------"
slopeTable = userTable.createSlopeTable()
print slopeTable
print "-----------------------------------------"
print userTable.calculateRating(slopeTable,14,1)

#f = open('u5.base', 'r')
#f2 = open('u.test', 'w')
#for line in f.readlines()[:300]:
#    line = line.split('\t')
#    user_id = int(line[0])
#    movie_id = int(line[1])
#f.close()


# def findB(self, i, j):
#     column1 = self.hasValues(i)
#     column2 = self.hasValues(j)
#     if column1 and column2:
#         overlap = column1.intersection(column2)
#         print overlap
#         if overlap:
#             slope = 0
#             for hits in overlap:
#                 slope += self.read(hits, j) - self.read(hits,i)
#             slope = slope/len(overlap)
#         else:
#             return None
#     else:
#          return None


# foundMovie = False
# foundMovieRating = 0
# predictedRating = 0
# i = user_id - 1
# j = user_id + 1
# while(not foundMovie):
#     if self.read(i,movie_id) is None:
#         i -= 1
#     else:
#         foundMovie = True
#         foundMovieRating = self.read(i,movie_id)
#         print user_id
#         print movie_id
#         print foundMovieRating
#         print i
#         if slopeTable.read(user_id,i) is None:
#             predictedRating = foundMovieRating + slopeTable.read(i, user_id)
#             break
#         else:
#             predictedRating = foundMovieRating + slopeTable.read(user_id,i)
#             break
#     if self.read(j,movie_id) is None:
#         j += 1
#     else:
#         foundMovie = True
#         foundMovieRating = self.read(j,movie_id)
#         print user_id
#         print movie_id
#         print foundMovieRating
#         print j
#         if slopeTable.read(user_id,j) is None:
#             predictedRating = foundMovieRating + slopeTable.read(j, user_id)
#             break
#         else:
#             predictedRating = foundMovieRating + slopeTable.read(user_id,j)
#             break
#
# return predictedRating
