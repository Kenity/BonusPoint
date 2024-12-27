import customtkinter as ctk 
from db import DataBase
import random
from CTkMessagebox import CTkMessagebox

class Windows(ctk.CTk):

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		ctk.set_appearance_mode('dark')
		self.resizable(False, False)

		container = ctk.CTkFrame(self, height = 400, width = 300)
		container.pack(side = 'top', fill = 'both', expand = True)
		container.grid_rowconfigure(0, weight = 1)
		container.grid_columnconfigure(0, weight = 1)

		self.frames = {}
		self.login = None

		for F in (Registration, Authorization, MainMenu, ForgotPassword):

			frame = F(container, self)

			self.frames[F] = frame

			frame.grid(row = 0, column = 0, sticky = 'nsew')

		self.show_frame(Authorization)

	def setLogin(self, login):
		self.login = login

	def show_frame(self, cont):
		frame = self.frames[cont]

		if cont == MainMenu:
			frame.updateLogin(self.login)

		frame.tkraise()

class Registration(ctk.CTkFrame):

	def __init__(self, parent, controller):

		super().__init__(parent)

		self.font = ("Arial", 18, "bold")

		self.controller = controller

		self.label = ctk.CTkLabel(self, font = self.font, text = 'Регистрация').pack(side = 'top', pady = 10)

		self.LabelLogin = ctk.CTkLabel(self, font = self.font, text = "Логин:").pack(side = 'top')
		self.entryLogin = ctk.CTkEntry(self, font = self.font, width = 200)
		self.entryLogin.pack(side = 'top', pady = 5)

		self.LabelLogin = ctk.CTkLabel(self, font = self.font, text = "Пароль:").pack(side = 'top')
		self.entryPassword = ctk.CTkEntry(self, font = self.font, width = 200)
		self.entryPassword.pack(side = 'top', pady = 5)

		self.LabelLogin = ctk.CTkLabel(self, font = self.font, text = "Почта:").pack(side = 'top')
		self.entryMail = ctk.CTkEntry(self, font = self.font, width = 200)
		self.entryMail.pack(side = 'top', pady = 5)

		self.buttonRegistration = ctk.CTkButton(self, font = self.font, text = 'Зарегистрироваться!', command = self.registration).pack(side = 'top', pady = 5)
		self.buttonAuthorization = ctk.CTkButton(self, font = self.font, text = 'Авторизоваться', command = lambda: controller.show_frame(Authorization)).pack()

	def registration(self):

		if DataBase.createUser(self, self.entryLogin.get(), self.entryPassword.get(), self.entryMail.get()):

			self.controller.show_frame(Authorization)
		else:
			CTkMessagebox(
				title = 'Ошибка!',
				message="Что то пошло не так!", 
                icon="cancel", 
                option_1="OK")



class Authorization(ctk.CTkFrame):

	def __init__(self, parent, controller):

		super().__init__(parent)

		self.login = 'hi'

		self.font = ("Arial", 18, "bold")
		self.controller = controller

		self.label = ctk.CTkLabel(self, font = self.font, text = 'Авторизация').pack(side = 'top', pady = 10)

		self.LabelLogin = ctk.CTkLabel(self, font = self.font, text = "Логин:").pack(side = 'top')
		self.entryLogin = ctk.CTkEntry(self, font = self.font, width = 200)
		self.entryLogin.pack(side = 'top', pady = 5)

		self.LabelLogin = ctk.CTkLabel(self, font = self.font, text = "Пароль:").pack(side = 'top')
		self.entryPassword = ctk.CTkEntry(self, font = self.font, width = 200)
		self.entryPassword.pack(side = 'top', pady = 5)

		self.buttonAuthorization = ctk.CTkButton(self, font = self.font, text = 'Авторизоваться', command = self.authorization).pack(side = 'top', pady = 5)
		self.buttonRegistration = ctk.CTkButton(self, font = self.font, text = 'Нет аккаунта? Зарегистрируйся!', command = lambda: controller.show_frame(Registration)).pack(side = 'top', pady = 5)

		self.buttonForgotPassword = ctk.CTkButton(self, font = self.font, text = 'Восстановить пароль', command = lambda: controller.show_frame(ForgotPassword)).pack(side = 'bottom')

	def authorization(self):
		if DataBase.authorization(self, self.entryLogin.get(), self.entryPassword.get()):
			self.controller.setLogin(self.entryLogin.get())
			self.controller.show_frame(MainMenu)
		else:
			CTkMessagebox(
				title = 'Ошибка!',
				message="Что то пошло не так!", 
                icon="cancel", 
                option_1="OK")			

class MainMenu(ctk.CTkFrame):

	def __init__(self, parent, controller):

		super().__init__(parent)

		self.font = ("Arial", 18, "bold")
		self.controller = controller
		self.login = None
		self.accessLevel = None
		self.bonusPoints = None

		self.labelLogin = ctk.CTkLabel(self, font = self.font)
		self.labelLogin.pack(side = 'top', pady = 10)

		self.labelBonusPoints = ctk.CTkLabel(self, font = self.font)
		self.labelBonusPoints.pack(side = 'top', pady = 10)

		self.buttonExit = ctk.CTkButton(self, font = ("Arial", 12, "bold"), text = 'Выйти из аккаунта', height = 10, command = lambda: controller.show_frame(Authorization))
		self.buttonExit.pack(side = 'bottom', anchor = 'e')

		self.labelText = ctk.CTkLabel(self, font = self.font, text = 'Укажите пользователя')
		self.entryUser = ctk.CTkEntry(self, font = self.font)
		self.buttonPlus = ctk.CTkButton(self, font = self.font, text = 'добавить 10 баллов', command = self.updateBonus)
		self.buttonMinus = ctk.CTkButton(self, font = self.font, text = 'списать 10 баллов')

	def updateLogin(self, login):
		self.login = login

		info = DataBase.getInfo(self, login)

		self.bonusPoints = info[0]
		self.accessLevel = info[1]

		self.labelBonusPoints.configure(text = f'Баллы: {self.bonusPoints}')
		self.labelLogin.configure(text = f'{login}({self.accessLevel})')
		self.isAdmin()
		

	def isAdmin(self):
		if self.accessLevel == "admin":
			self.labelText.pack(pady = 5)
			self.entryUser.pack(pady = 5)
			self.buttonPlus.pack(pady = 5)
			self.buttonMinus.pack(pady = 5)
			self.labelBonusPoints.pack_forget()
		else:
			self.labelText.pack_forget()
			self.entryUser.pack_forget()
			self.buttonPlus.pack_forget()
			self.buttonMinus.pack_forget()
			self.labelBonusPoints.pack()
			self.labelBonusPoints.pack()

	def updateBonus(self):
		DataBase.plusBonusPoint(self, self.entryUser.get())



class ForgotPassword(ctk.CTkFrame):

	def __init__(self, parent, controller):

		super().__init__(parent)

		self.code = None
		self.mail = None
		self.newPass = None

		self.controller = controller
		self.font = ("Arial", 18, "bold")
		self.controller = controller

		self.label = ctk.CTkLabel(self, font = self.font, text = "Восстановление пароля").pack(side = 'top')

		self.entryMail = ctk.CTkEntry(self, font = self.font, width = 200)
		self.entryMail.pack(side = 'top', pady = 20)

		self.buttonFirst = ctk.CTkButton(self, font = self.font, text = "Восстановить", command = self.firsStage)
		self.buttonFirst.pack(pady = 10)

		self.labelText = ctk.CTkLabel(self, font = self.font, text = 'Почта:')
		self.labelText.place(x = 30, y = 46)

		self.entryCode = ctk.CTkEntry(self, font = self.font, width = 200)
		self.buttonFSecond = ctk.CTkButton(self, font = self.font, text = 'Продолжить', command = self.secondStage)

		self.entryPasswordFirst = ctk.CTkEntry(self, font = self.font, width = 200)
		self.entryPasswordSecond = ctk.CTkEntry(self, font = self.font, width = 200)

		self.labelTextpass = ctk.CTkLabel(self, font = self.font, width = 200, text = 'Пароль: ')
		self.labelTextpassTwo = ctk.CTkLabel(self, font = self.font, width = 200, text = 'Подтвердите пароль: ')

		self.buttonLast = ctk.CTkButton(self, font = self.font, text = 'Сбросить паоль', command = self.updatePassword)

	def firsStage(self):
		self.code = random.randrange(10000, 99999)

		self.mail = self.entryMail.get()

		self.entryMail.pack_forget()
		self.buttonFirst.pack_forget()

		print("code:", self.code)

		self.labelText.configure(text = "Код:")

		self.entryCode.pack(side = 'top', pady = 20)
		self.buttonFSecond.pack(side = 'top')

	def secondStage(self):

		if int(self.entryCode.get()) == int(self.code):

			self.labelText.place_forget()

			self.entryCode.pack_forget()
			self.buttonFSecond.pack_forget()


			self.labelTextpass.pack(side = 'top')
			self.entryPasswordFirst.pack(side = 'top', pady = 20, padx = 10)

			self.labelTextpassTwo.pack(side = 'top')
			self.entryPasswordSecond.pack(side = 'top', pady = 10)

			self.buttonLast.pack(side = 'top')
		else:
			CTkMessagebox(
				title = 'Ошибка!',
				message="Не верный код", 
                icon="cancel", 
                option_1="OK")

	def updatePassword(self):
		
		if self.entryPasswordFirst.get() == self.entryPasswordSecond.get():
			self.newPass = self.entryPasswordFirst.get()
			DataBase.updatePassword(self, self.mail, self.newPass)
			CTkMessagebox(
				title = 'Успех!',
				message="Пароль успешно изменен", 
                icon="check", 
                option_1="OK")
			self.controller.show_frame(Authorization)
		
		else:
			CTkMessagebox(
				title = 'Ошибка!',
				message="пароли не совпадают", 
                icon="cancel", 
                option_1="OK")


			



			
		


if __name__ == "__main__":

	DataBase()
	object_window = Windows()
	object_window.geometry('400x350')
	object_window.mainloop()
