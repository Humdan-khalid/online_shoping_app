class DatabaseError(Exception):
    pass

class UserAlreadyExist(Exception):
    pass

class DatabaseError(Exception):
    pass

class DatabaseConnectionFailed(Exception):
    pass

class UserNotFound(Exception):
    pass

class InvalidCredentials(Exception):
    pass

class AdminAlreadyExist(Exception):
    pass

class AdminNotFound(Exception):
    pass

class SellerAlreadyExist(Exception):
    pass

class SellerNotExist(Exception):
    pass

class InvalidToken(Exception):
    pass

class UnauthorizedSeller(Exception):
    pass

class ProductNotFound(Exception):
    pass

class QuantityOrderError(Exception):
    pass

class StockFinished(Exception):
    pass

class InvalidQuantity(Exception):
    pass

class SellerProductNotFound(Exception):
    pass
