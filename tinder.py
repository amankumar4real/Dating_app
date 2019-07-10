from guihelper import GUIhelper
from dbhelper import DBhelper
from tkinter import filedialog


class Tinder(GUIhelper):

    def __init__(self):
        self.sessionId = 0
        self.db = DBhelper()
        super(Tinder, self).__init__(self.login, self.loadRegWindow)

    def login(self):
        print(self._emailInput.get())
        print(self._passwordInput.get())
        if self._emailInput.get() == "" or self._passwordInput.get() == "":
            self.label2.configure(text="please fill both the fields", bg="yellow", fg="red")
        else:
            if '@' not in self._emailInput.get():
                self.label2.configure(text="Invalid email format", bg="yellow", fg="red")
            else:
                # searching function from database
                data = self.db.search('email', self._emailInput.get(), 'password', self._passwordInput.get(), 'users')
                if len(data) == 1:
                    self.sessionId=data[0][0]
                    self.loadProfile()

                else:
                    self.label2.configure(text="login failed", bg="yellow", fg="red")

    def loadRegWindow(self):
        self.regWindow(self.registrationHandler)

    def registrationHandler(self):
        if self._nameInput.get() == "" or self._emailInput.get() == "" or self._passwordInput.get() == "" or self._genderInput.get() == "" or self._ageInput.get() == "" or self._cityInput.get() == "":
            self.label2.configure(text="Please Fill all the fields", bg="yellow", fg="red")
        else:
            regDict = {}

            regDict['user_id'] = "NULL"
            regDict['name'] = self._nameInput.get()
            regDict['email'] = self._emailInput.get()
            regDict['password'] = self._passwordInput.get()
            regDict['gender'] = self._genderInput.get()
            regDict['age'] = self._ageInput.get()
            regDict['city'] = self._cityInput.get()

            response = self.db.insert(regDict, 'users')

            if response == 1:
                self.label2.configure(text="Registration Successful. Login to proceed", bg="white", fg="green")
                self._root.destroy()
                obj = Tinder()
            else:
                self.label2.configure(text="Registration Failed", bg="yellow", fg="red")


    def loadProfile(self):
        if self.sessionId!=0:
            data=self.db.searchOne('user_id',self.sessionId,'users',"LIKE")
            self.mainWindow(self,data,mode=1)

    def viewProfile(self, num):
        if self.sessionId!=0:
            data=self.db.searchOne('user_id',self.sessionId,'users',"NOT LIKE")
            if num==0:
                new_data=[]
                new_data.append(data[0])
                self.mainWindow(self,new_data,mode=2,num=num)
            elif num<0:
                self.message("Error","User Not Found")
            elif num>len(data)-1:
                self.message("Error","User Not Found")
            else:
                new_data = []
                new_data.append(data[num])
                self.mainWindow(self, new_data, mode=2, num=num)

    def propose(self,juliet_id):
        data=self.db.search('romeo_id',self.sessionId,'juliet_id',juliet_id,'proposals')
        if len(data)==0:
            propDict={}
            propDict['romeo_id']=str(self.sessionId)
            propDict['juliet_id']=juliet_id

            response=self.db.insert(propDict,'proposals',1)

            if response==1:
                self.message("Yayyyyyyyy","Proposal sent. Fingers Crossed")
            else:
                self.message("Nayyyyyyyy","Not Sent.")

        else:
            self.message("Invalid", "Proposal Already Sent")

    def myLogout(self):
        self._root.destroy()
        obj = Tinder()

    def editProfile(self):

        self.clean()
        if self.sessionId!=0:
            data = self.db.searchOne('user_id',self.sessionId,'users',"LIKE")
            self.mainWindow(self,data,mode=3)

    def save(self, data):

        updateDict = {}

        if self._nameInput.get() == "":
            updateDict['name'] = data[0][1]
        else:
            updateDict['name'] = self._nameInput.get()

        if self._passwordInput.get() == "":
            updateDict['password'] = data[0][3]
        else:
            updateDict['password'] = self._passwordInput.get()

        if self._genderInput.get() == "":
            updateDict['gender'] = str(data[0][4])
        else:
            updateDict['gender'] = self._genderInput.get()

        if self._ageInput.get() == "":
            updateDict['age'] = str(data[0][5])
        else:
            updateDict['age'] = self._ageInput.get()

        if self._cityInput.get() == "":
            updateDict['city'] = data[0][6]
        else:
            updateDict['city'] = self._cityInput.get()

        response = self.db.update(updateDict, 'users', str(self.sessionId))

        if response == 1:
            self.message("Message", "Update Successful!!")
        else:
            self.message("Message", "Update Failed!!")

    def editProfilePic(self):
        filename = filedialog.askopenfilename(initialdir=r"C:\Users\AMAN\PycharmProjects\tinderb3\img", title = "Select an image ", filetype=(("jpeg","*.jpg"),(r"All files","*.*")))
        filename = filename.split('/')[-1]
        self.db.setDp(filename,'users','user_id','dp',str(self.sessionIdkus))

obj = Tinder()