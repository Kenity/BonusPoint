import sqlite3
from hashing import Hashing


class DataBase():

	def __init__(self):

		conn = sqlite3.connect('db.db')
		cur = conn.cursor()

		cur.execute('''CREATE TABLE IF NOT EXISTS users (
			login TEXT,
			password TEXT,
			bonusPoints INT,
			mail TEXT,
			accessLevel Text
		)''')

		conn.commit()
		conn.close()

	def createUser(self, login, password, mail):

		if login == '' or password == '' or mail == '':

			print('поля не могут быть пустыми!')

		else:
			conn = sqlite3.connect('db.db')
			cur = conn.cursor()

			if cur.execute(f"SELECT * FROM users WHERE login = '{login}'").fetchall() == []:
				
				cur.execute(f"INSERT INTO users (login, password, bonusPoints, mail, accessLevel) VALUES ('{login}', '{Hashing.hashPassword(self, password)}', 0, '{mail}', 'user')")

				conn.commit()
				conn.close()

				return True

			else:
				print('Есть дупликат!')

	def authorization(self, login, password):

		if login == '' or password == '':
			print('поля не могут быть пустыми!')

		else:

			conn = sqlite3.connect('db.db')
			cur = conn.cursor()

			if cur.execute(f"SELECT * FROM users WHERE login = '{login}'").fetchall() == []:
				print('Логин или пароль не правильны!')

			else:

				if Hashing.verifyPassword(self, password, cur.execute(f"SELECT password FROM users WHERE login = '{login}'").fetchone()[0]):
					print('Успех!')
					return True

				else:
					print('Логин или пароль не правильны!')

	def getInfo(self, login):
		info = []

		conn = sqlite3.connect('db.db')
		cur = conn.cursor()

		userInfo = cur.execute(f"SELECT * FROM users WHERE login = '{login}'").fetchall()[0]
		print(userInfo)
		info.append(userInfo[2])
		info.append(userInfo[4])

		return info

	def updatePassword(self, mail, password):

		conn = sqlite3.connect('db.db')
		cur = conn.cursor()

		password = Hashing.hashPassword(self, password)

		cur.execute(f"UPDATE users SET password = '{password}' WHERE mail = '{mail}'")

		conn.commit()
		conn.close()

	def plusBonusPoint(self, login):
		conn = sqlite3.connect('db.db')
		cur = conn.cursor()

		nowPoint = cur.execute(f"SELECT bonusPoints FROM users WHERE login = '{login}'").fetchone()[0]
		
		nowPoint += 10

		cur.execute(f"UPDATE users SET bonusPoints = {nowPoint} WHERE login = '{login}'")

		conn.commit()
		conn.close()

