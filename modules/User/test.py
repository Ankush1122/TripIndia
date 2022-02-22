from User import UserRepo
from User import UserModel

import bcrypt
password = "password"
password = str(password).encode('utf-8')
hashed = bcrypt.hashpw(password, bcrypt.gensalt())
hashed = hashed.decode()

user = UserModel.User(None,
                      "Ankush Deshmukh", "deshmukh.1@iitj.ac.in", hashed, "superadmin", 1, "Full Stack Developer", "India", "Student", "12/12/2002")

db = UserRepo.Repo()
# db.createUserTable()


db.addUser(user)
# db.deleteUserById(user1.userid)

# print(db.isUserIdUsed(user1.userid))

#users = db.getAllUsers()
# db.createUserTable()

#newUser = db.getUserById("danku")

"""
for newUser in users:
    print(newUser.name)
    print(newUser.userid)
    print(newUser.password)
    print(newUser.usertype)
    """
