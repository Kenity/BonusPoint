import bcrypt
import base64

class Hashing():
	def __init__(self):
		pass

	def hashPassword(self, password):
		salt = bcrypt.gensalt()
		hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
		return base64.b64encode(hashed).decode('utf-8')

	def verifyPassword(self, password, hashedPassword):
		hashed = base64.b64decode(hashedPassword.encode('utf-8'))
		return bcrypt.checkpw(password.encode('utf-8'), hashed)