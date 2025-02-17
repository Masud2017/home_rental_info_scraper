class SearchPreference:
    def __init__(self, id, user_id, min_price, max_price, cities, neighborhoods, min_rooms, max_rooms):
        self._id = id
        self._user_id = user_id
        self._min_price = min_price
        self._max_price = max_price
        self._cities = cities
        self._neighborhoods = neighborhoods
        self._min_rooms = min_rooms
        self._max_rooms = max_rooms

    def __repr__(self):
        return (f"SearchPreference(id={self._id}, user_id={self._user_id}, min_price={self._min_price}, "
                f"max_price={self._max_price}, cities={self._cities}, neighborhoods={self._neighborhoods}, "
                f"min_rooms={self._min_rooms}, max_rooms={self._max_rooms})")

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def min_price(self):
        return self._min_price

    @min_price.setter
    def min_price(self, value):
        self._min_price = value

    @property
    def max_price(self):
        return self._max_price

    @max_price.setter
    def max_price(self, value):
        self._max_price = value

    @property
    def cities(self):
        return self._cities

    @cities.setter
    def cities(self, value):
        self._cities = value

    @property
    def neighborhoods(self):
        return self._neighborhoods

    @neighborhoods.setter
    def neighborhoods(self, value):
        self._neighborhoods = value

    @property
    def min_rooms(self):
        return self._min_rooms

    @min_rooms.setter
    def min_rooms(self, value):
        self._min_rooms = value

    @property
    def max_rooms(self):
        return self._max_rooms

    @max_rooms.setter
    def max_rooms(self, value):
        self._max_rooms = value
