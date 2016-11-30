import math

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
                B = (slope*1.0)/(1.0*len(overlap))
                return B

            else:
                return None
        else:
            return None

    def createSlopeTable(self):
        newSlopeTable = Table()
        movies = 1
        nestedMovies = 1
        while(movies <= 1682):
            while(nestedMovies < movies):
                newSlopeTable.set(nestedMovies,movies,self.findOneB(movieTable,nestedMovies,movies))
                nestedMovies += 1
            nestedMovies = 1
            movies += 1
        return newSlopeTable

    def calculateRating(self, slopeTable, movie_id, user_id):
        ratedMovies = self.hasValues(user_id)
        avgMovieRatings = 0
        counter = 0.0
        for i in ratedMovies:
            if(i < movie_id):
                if(slopeTable.read(i, movie_id) is None):
                    avgMovieRatings += self.read(user_id,i)
                else:
                    avgMovieRatings += self.read(user_id, i) + slopeTable.read(i, movie_id)
                    counter += 1
        if  counter == 0:
            return 3.0
        else:
            predictedRating = avgMovieRatings/(counter)
            return predictedRating

#Tables created to be written into from the given base file.
userTable = Table()
movieTable = Table()


f = open('data/u5.base','r')
for line in f.readlines():
    line = line.split('\t')
    user_id = int(line[0])
    movie_id = int(line[1])
    rating = float(line[2])
    userTable.set(user_id, movie_id,rating)
    movieTable.set(movie_id, user_id, rating)
slopeTable = userTable.createSlopeTable()
f.close()

#Opens up the test file as well as the file to be written.
f2 = open('data/u5.test', 'r')
f3 = open('u5.prediction', 'w')
meanSquaredError = 0
total_predictions = 0
for line in f2.readlines():
    line = line.split('\t')
    user_id = int(line[0])
    movie_id = int(line[1])
    actual_rating = int(line[2])
    guess = userTable.calculateRating(slopeTable, movie_id, user_id)

    if guess < 9:
        meanSquaredError += math.pow((guess)-(actual_rating), 2)
        total_predictions += 1

    f3.write(str(user_id) + "\t" + str(movie_id) + "\t" + str(guess) + "\n")

f3.close()
f2.close()

meanSquaredError = meanSquaredError/total_predictions
print meanSquaredError
