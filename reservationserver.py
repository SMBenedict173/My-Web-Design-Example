from datetime import*
import os
import cgi
import cgitb

class Reservation:
    def _init_(self, firstName = '', lastName = '', start = date (1, 1, 1), end = date (1, 1, 1)):
        self.createReservation(start, end)

    def createReservation(self, first, last, start, end):
        self.start = start
        self.end = end
        self.firstName = first
        self.lastName = last
        

    def output(self):
        resString = self.firstName + ' ' + self.lastName + ' '  + str(self.start.year) + ' ' + str(self.start.month) + \
                    ' ' + str(self.start.day) + ' ' + str(self.end.year) + ' ' + str(self.end.month) \
                    + ' ' + str(self.end.day) + ' '
        return resString

    def isEqual(self, other):
        if (self.firstName == other.firstName) and (self.lastName == other.lastName) \
           and (self.start == other.start) and (self.end == other.end):
            return True
        else:
            return False
    
class Room:
    def _init_(self, roomNum = 0, reservations = []):
        self.createRoom(roomNum, reservations)
        
    def createRoom(self, roomNum, reservations):
        self.number = roomNum
        self.reservations = reservations

    def checkReservation(self, newRes):
        if newRes.start < date.today():
            return False
        else:
            for i in range (len(self.reservations)):
                if not (((self.reservations[i].start < newRes.end) or (self.reservations[i].end < newRes.start)) == True):
                    success = False
                    break
                else:
                    success = True
                    continue
            if success == True:
                return True
            else:
                return False
            
           

    def output(self):
        roomString = str(self.number) + ' '
        for i in range (len(self.reservations)):
            roomString = roomString + self.reservations[i].output()
        return roomString

    def addReservation(self, newRes):
        self.reservations.append(newRes)

    def removeReservation(self, canceledRes):
        for i in range(len(self.reservations)):
            if self.reservations[i].isEqual(canceledRes):
                self.reservations.remove(self.reservations[i])
                success = True
                break
            else:
                success = False
                continue
        if success == True:
            return True
        else:
            return False
                       
class Lodge:
    def _init_(self, roomNums = [], roomInfo = {}):
        self.createLodge(roomNums, roomInfo)

    def createLodge (self, roomNums, roomInfo):   
        self.roomNums = roomNums
        self.roomInfo = roomInfo
    
    def addRoom(self, newRoom):
        self.roomNums.append(newRoom.number)
        self.roomInfo[newRoom.number] = newRoom

    def checkReservation (self, newRes):
        for i in range (len(self.roomNums)):
            if self.roomInfo[self.roomNums[i]].checkReservation(newRes) == True:
                self.saveLodge()
                success = True
                break
            else:
                continue
        if success == True:
            return True
        else:
            return False

    def removeReservation (self, canceledRes):
        for i in range(len(self.roomNums)):
            if self.roomInfo[self.roomNums[i]].removeReservation(canceledRes) == True:
                self.saveLodge()
                success = True
                break
            else:
                success = False
                continue
        if success == True:
            return True
        else:
            return False
        
        

    def saveLodge (self):
        lodgeText = ''
        with open('lodge.txt', 'w') as lodgeFile:
            for i in range (len(self.roomNums)):
                lodgeText = lodgeText + self.roomInfo[self.roomNums[i]].output() 
                lodgeText = lodgeText + '\n'
            lodgeFile.write(lodgeText)
            

    def loadLodge (self):
        with open ('lodge.txt') as lodgeFile:
            for line in lodgeFile:
                roomSource = line
                roomFacts = roomSource.split(' ')
                newRoomNum = int(roomFacts[0])
                newRoomReservations = []
                for i in range (1, len(roomFacts), 8):
                    try:
                        newRoomReservation = Reservation()
                        newRoomReservation.createReservation(roomFacts[i], roomFacts[i + 1], \
                                            date(int(roomFacts[i + 2]), int(roomFacts[i + 3]), int(roomFacts[i + 4])),\
                                            date(int(roomFacts[i + 5]), int(roomFacts[i + 6]), int(roomFacts[i + 7])))
                        newRoomReservations.append(newRoomReservation)
                    except(IndexError):
                        break
                newRoom = Room ()
                newRoom.createRoom(newRoomNum, newRoomReservations)
                self.addRoom(newRoom)

def processDate (dateString):
    dateList = dateString.split('-')
    theDate = date(int(dateList[0]), int(dateList[1]), int(dateList[2]))
    return theDate
    
cgitb.enable()
mountGoodTimes = Lodge()
mountGoodTimes.createLodge([], {})
mountGoodTimes.loadLodge()
form = cgi.FieldStorage()
newRes = Reservation()
newRes.createReservation(form.getvalue("first_name"), form.getvalue("last_name"), processDate(form.getvalue("start")), \
                         processDate(form.getvalue("end")))
if form.getvalue("action") == "create": 
    if mountGoodTimes.checkReservation(newRes) == True:
        text = '<p> Your reservation was made successfully.</p>'
    else:
        text = "<p> We're sorry, but we were unable to find a room available for those dates.</p>"
elif form.getvalue("action") == "cancel": 
    if mountGoodTimes.removeReservation(newRes) == True:
        text = '<p> Your reservation was cancelled successfully. </p>'
    else:
        text = '<p> Your reservation could not be found and therefore could not be cancelled. </p>'
print("Content-Type: text/html\r\n\r\n")
print()

print('<DOCTYPE! html>' + '\n' + '<html lang = "en">' + '\n' + '<head>' + '\n' + \
      '<meta charset = "utf-8">' + '\n' + '<link href = "skilodgesubpage.css" rel= "stylesheet">' + \
      '\n' + '<title>Booking</title>' + '\n' + '</head>' + '\n' + '<body>' + '\n' + '<header>' + '\n' \
      + '<h1> Booking </h1>' + '\n' + '</header>' + '\n' + '<div>' + '\n' + '<nav class = "navbar">' \
      + '\n' + '<ul style= "text-decoration:none">' + '\n' + '<li> <a href="skilodgehome.html" class = "navbar"> <b> Home </b> </a> </li>'\
      + '\n' + '<li><a href="skilodgereservations.html" class = "navbar"> <b> Make a Reservation </b> </a></li>' \
      + '\n' + '<li> <a href="skilodgegallery.html" class = "navbar"> <b> Image Gallery </b> </a> </li>' + '\n' + \
      '<li> <a href="skilodgecontact.html" class = "navbar"> <b> Contact Us </b> </a> </li>' + '\n' + '</ul>' \
      + '\n' +'</nav>' + '\n' + '<main>' + '\n' + '<h1> Thank You </h1> %s' % text)
print('<p> Please do not use the back button or refresh this page, as doing so could cause unexpected errors. </p>' \
      '</main>' + '\n' + '</div>' + '\n' + '<footer>' + '\n' + '<ul>' + '\n' +\
      '<li><a href="skilodgehome.html" alt = "Home Page Link"> Home </a> </li>' + '\n' + \
      '<li><a href="skilodgereservations.html" alt = "Make a Reservation"> Make a Reservation </a></li>' \
      + '\n' + '<li><a href="skilodgegallery.html" alt = "Image Gallery"> Image Gallery </a> </li>' \
      + '\n' + '</ul>' + '\n' + '<ul>' \
      + '\n' + '<li><a href="skilodgecontact.html" alt = "Contact Us"> Contact Us </a> </li>' \
      + '\n' + '<li><a href="skilodgeprivacy.html" alt = "Privacy Policy"> PrivacyPolicy </a> </li>'
      + '\n' + '</ul>' + '\n' + '</footer>' + '\n' + '<body>' + '\n' + '</html>')
            
