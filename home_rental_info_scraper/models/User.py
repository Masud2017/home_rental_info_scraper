from datetime import datetime
import re

class User:
    def __init__(self,id:int = 0, username: str = '', password: str = '') -> None:
        self.id = id
        self.username = username
        self.password = password
        
    def __repr__(self) -> str:
        return str(self)
        
    def __str__(self) -> str:
        return f"{self.id}, {self.username}"
        
    def __eq__(self, other: 'User') -> bool:
        if self.username.lower() == other.user.lower():
            if self.id == other.id:
                return True
        return False
    
    @property
    def id(self) -> int:
        return self._id
        
    @id.setter
    def id(self, id: int) -> None:
        self._id = id
        
    @property
    def username(self) -> str:
        return self._username
    
    @username.setter
    def username(self, username: str) -> None:
        self._username = username
    
    @property
    def password(self) -> str:
        return self._password
    
        
    @password.setter
    def password(self, password: str) -> None:
        self._password = password
        
if __name__ == "__main__":
    user = User(id=1, username='john_doe', password='securepassword123')
    print(user)
    