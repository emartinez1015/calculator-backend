from peewee import Model, DecimalField, CharField, BooleanField, DateTimeField, ForeignKeyField
from chalicelib.database import DatabaseConnection
from chalice import ChaliceViewError

db = DatabaseConnection().get_connection()


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        table_name = 'users'  
    username = CharField()
    status = BooleanField()
    balance = DecimalField(default=5000)
    cognito_user_id = CharField()

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'status': self.status,
            'balance': self.balance,
            'cognito_user_id': self.cognito_user_id
        }

    def update_balance(self, value):
        self.balance = self.balance - value
        self.save()
        return self.balance

class Operation(BaseModel):
    class Meta:
        table_name = 'operations'

    type = CharField()
    cost = DecimalField()
    symbol = CharField()
    is_arithmetic = BooleanField()
    
    def to_dict(self):
        return {
            'type': self.type,
            'cost': str(self.cost),
            'symbol': self.symbol,
            'is_arithmetic': self.is_arithmetic
        }

class Record(BaseModel):
    class Meta:
        table_name = 'records'
    
    operation = ForeignKeyField(Operation, backref='records')
    user_id = ForeignKeyField(User, backref='users')
    amount = DecimalField()
    user_balance = DecimalField()
    operation_response = CharField()
    date = DateTimeField()
    active = BooleanField()

    def save(self, *args, **kwargs):
        if self._pk is None:
            operation = self.operation
            user = self.user_id

            if user.balance < operation.cost:
                raise ChaliceViewError("Insufficient balance for the operation.")

            self.user_balance = user.update_balance(operation.cost)
        super().save(*args, **kwargs)

    def to_dict(self):
        return {
            'id': self.id,
            'operation': self.operation.to_dict(),
            'user_id': self.user_id.to_dict(),
            'amount': str(self.amount),
            'user_balance': str(self.user_balance),
            'operation_response': self.operation_response,
            'date': self.date.strftime('%Y-%m-%d %H:%M:%S'),
        }
