class User:
    def __init__(self,id, username,password):
        self.id = id
        self.username = username
        self.password = password
        self.products = {}
    
    def __repr__(self):
        return f'<User: {self.username}>'


users = [] 
admin = User(id=1,username='admin',password = '123')
users.append(admin)  