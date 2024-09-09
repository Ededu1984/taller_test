import re
import unittest
import uuid

"""
1. Complete the `App.create_user()` method to allow our application to create new users.

2. Complete the `User.pay()` method to allow users to pay each other. Consider the following: if user A is paying user B, user's A balance should be used if there's enough balance to cover the whole payment, if not, user's A credit card should be charged instead.

3. Application has the Feed functionality, that shows the payments that users have been doing in the app. If Bobby paid Carol $5, and then Carol paid Bobby $15, it should look something like this

Bobby paid Carol $5.00 for Coffee
Carol paid Bobby $15.00 for Lunch

Implement the `User.retrieve_activity()` and `App.render_feed()` methods so the application can render the feed.

4. Now users should be able to add friends. Implement the `User.add_friend()` method to allow users to add friends.
5. Now modify the methods involved in rendering the feed to also show when user's added each other as friends.

"""

class UsernameException(Exception):
    pass


class PaymentException(Exception):
    pass


class CreditCardException(Exception):
    pass


class Payment:

    def __init__(self, amount, actor, target, note):
        self.id = str(uuid.uuid4())
        self.amount = float(amount)
        self.actor = actor
        self.target = target
        self.note = note
 

class User:

    def __init__(self, username):
        self.credit_card_number = None
        self.balance = 0.0

        if self._is_valid_username(username):
            self.username = username
        else:
            raise UsernameException('Username not valid.')


    def retrieve_feed(self):
        #return []
        pass

    def add_friend(self, new_friend):
        self.friend = new_friend

    def add_to_balance(self, amount):
        self.balance += float(amount)

    def add_credit_card(self, credit_card_number):
        if self.credit_card_number is not None:
            raise CreditCardException('Only one credit card per user!')

        if self._is_valid_credit_card(credit_card_number):
            self.credit_card_number = credit_card_number

        else:
            raise CreditCardException('Invalid credit card number.')

    def pay(self, target, amount, note):
        self.target = target

        if self.balance > amount:
            self.balance -= amount
        else:
            self.credit_card_number = amount - self.balance
            self.balance = 0

        self.note = note

    def pay_with_card(self, target, amount, note):
        amount = float(amount)

        if self.username == target.username:
            raise PaymentException('User cannot pay themselves.')

        elif amount <= 0.0:
            raise PaymentException('Amount must be a non-negative number.')

        elif self.credit_card_number is None:
            raise PaymentException('Must have a credit card to make a payment.')

        self._charge_credit_card(self.credit_card_number)
        payment = Payment(amount, self, target, note)
        target.add_to_balance(amount)

        return payment

    def pay_with_balance(self, target, amount, note):
        self.target = target
        self.balance -= amount
        self.note = note

    def _is_valid_credit_card(self, credit_card_number):
        return credit_card_number in ["4111111111111111", "4242424242424242"]

    def _is_valid_username(self, username):
        return re.match('^[A-Za-z0-9_\\-]{4,15}$', username)

    def _charge_credit_card(self, credit_card_number):
        # magic method that charges a credit card thru the card processor
        pass


class App:

    def create_user(self, username, balance, credit_card_number): # 
        user = User(username)
        user.balance = balance
        user.credit_card_number = credit_card_number
        return user

    def render_feed(self, feed):
        pass
        # Bobby paid Carol $5.00 for Coffee
        # Carol paid Bobby $15.00 for Lunch


    @classmethod
    def run(cls):
        application = cls()

        bobby = application.create_user("Bobby", 5.00, "4111111111111111")
        carol = application.create_user("Carol", 10.00, "4242424242424242")

        try:    
            
            # should complete using balance
            bobby.pay(carol, 5.00, "Coffee")
 
            # should complete using card
            carol.pay(bobby, 15.00, "Lunch")

        except PaymentException as e:
            print(e)

        feed = bobby.retrieve_feed()
        application.render_feed(feed)

        bobby.add_friend(carol)


class TestUser(unittest.TestCase):

    def test_this_works(self):
        with self.assertRaises(UsernameException):
            raise UsernameException()


if __name__ == '__main__':

    application = App()
    print(application.run())
    #unittest.main()
