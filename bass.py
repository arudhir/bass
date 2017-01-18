import operator
from operator import *

# TODO: Add error handling
# TODO: Add in switch statements in main() to make the code more robust
# TODO: Wrap the for loop in main()
# TODO: don't use break statements like a scrub
# In[]:
class BassTeam:

    def __init__(self, school, names, place=-1, weight=0):
        # self.school = schoolinput("Input the school name")
        # self.names = [input("Input the members of the team - last name only, each one separated by a space")]
        self.school = school
        self.names = names
        self.place = place
        self.weight = weight

    # def __init__(self, school, names, weight, place):
    #     '''temporary init'''
    #     self.school = school
    #     self.names = names
    #     self.place = place
    #     self.weight = weight
    #
    # @classmethod
    # def initTeam(self, school, names, place, weight):
    #     '''Using this as an alternate constructor for testing convenience'''
    #     self.school = school
    #     self.names = names
    #     self.place = place
    #     self.weight = weight


    def updatePlace(self):
        self.place = int(input("Enter the current standing of team %s" %self.school))

    def print_team(self):
        names_str = " ".join(str(name) for name in self.names)
        team = "{}: {}".format(self.school, names_str)
        print(team)

    def print_place(self):
        print("team: {}".format(self.school) + '\n' + "place: {}".format(self.place)
            + '\n' + "weight: {}".format(self.weight))

    def getPlace(self):
        return self.place

    def addWeight(self, weight):
        self.weight = self.weight + weight

# In[]:
def updatePlace(teams):
    for i in range(len(teams)):
        teams[i].place = i+1

def rankTeamsByWeight(teams):
    teams.sort(key=lambda x:x.weight, reverse=True)

def printCompetitors(competitors):
    for i in range(len(competitors)):
        print(competitors[i].names + ": " + str(competitors[i].weight))
# Main function will create a list of BassTeam objects
# Then start an infinite loop that allows for changing of results and shit until enter is hit twice
# In[]:

if __name__ == '__main__':
    competitors = []

    while True:
        name = input("Enter competitor's name: ")
        if (name == ''):
            break
        school = input("Enter competitor's school: ")
        if (school == ''):
            break

        entry = BassTeam(school, name)
        competitors.append(entry)

    while True:
        # Initialize the competitors

        update_name = input("Enter the name of the competitor to be updated: ")
        #competitor = list(filter((lambda x: x.names.lower() == update_name.lower()), competitors))
        index = -1
        for i in range(len(competitors)):
            if (competitors[i].names.lower() == update_name.lower()):
                index = i
                break

        weight = int(input("Enter the weight to be added: "))
        # printCompetitors(competitors)


        competitors[i].addWeight(weight)
        competitors.sort(key=lambda x:x.weight, reverse=True)

        # printCompetitors(competitors)
        quit = input("Press q to quit, press anything else add another weight: ")
        if (quit == 'q'):
            break
        else:
            continue
