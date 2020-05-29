class User:
    def __init__(self,id, username,password):
        self.id = id
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<User: {self.username}>'


users = []
users.append(User(id=1,username='Snthony',password = 'password'))  
users.append(User(id=2,username='zcthony',password = 'pasord'))  
users.append(User(id=2,username='hakeroku',password = '123'))  