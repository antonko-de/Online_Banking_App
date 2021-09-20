import random
# imports the random library that we will need later
import sqlite3
conn = sqlite3.connect('card.s3db')
cursor = conn.cursor()
# imports the sql lite library that we are going to use
import sys

cursor.execute('DROP TABLE IF EXISTS card')
cursor.execute("CREATE TABLE IF NOT EXISTS card('id' INTEGER PRIMARY KEY, 'number' TEXT, 'pin' TEXT , 'balance' INTEGER);")
# checks if there is the table we need in the db and if not, it creates it


def acc_creation():
    # a function that creates random valid account information and pin code

    biin = '{:09d}'.format(random.randint(000000000, 999999999))
    card_num = "400000" + biin
    pin = '{:04d}'.format(random.randrange(0000, 9999))
    list_id = [int(i) for i in card_num]

    for i in range(0, len(list_id), 2):
        list_id[i] = list_id[i] * 2
        if list_id[i] > 9:
            list_id[i] = list_id[i] - 9

    if sum(list_id) % 10 > 0:
        checksum = 10 - (sum(list_id) % 10)
    else:
        checksum = 0
    # loop and a statement to ensure the luhn algorithm applies to the card
    card_num = "400000" + biin + str(checksum)
    balance = 0
    cursor.execute(" SELECT COUNT(id) FROM card;")
    conn.commit()
    curr_id = cursor.fetchone()[0] + 1
    cursor.execute("INSERT INTO card VALUES (?,?,?,?)", (curr_id, card_num, pin, balance))
    conn.commit()
    print('Your card has been created')
    print(f'Your card number:\n{card_num}')
    print(f'Your card number:\n{pin}')
    # add the acc info into the database and print the required statement



def login_menu():
    # function that prints out the login menu and takes the input necessary for the next

    choice_login = input(f"1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n> ")
    return choice_login


def acc_pass_check(cardnum, pincode):
    # functions that validates card and pin pair for logging in

    ifLogged = False
    for i in cursor.execute('SELECT number, pin FROM card;'):
        if i[0] == cardnum and i[1] == pincode:
            ifLogged = True
    if ifLogged:
        print('You have successfully logged in!')
        current_card = cardnum
        return current_card
    else:
        print('Wrong card number or PIN!')
        return False
    # returns boolean for validity and logged card number for later use



def add_income(current_number):
    # function used to add money into the existing bank account
    value = input('Enter income:\n')
    cursor.execute("SELECT balance FROM card WHERE number = ?", (current_number,))
    curr_balance = int(cursor.fetchone()[0])
    updated_balance = curr_balance + int(value)
    cursor.execute("UPDATE card SET balance=? WHERE number =?", (updated_balance, current_number))
    conn.commit()
    print('Income was added!')


def transfer_validation_card_num (user_acc):
    # function that validates if the transfer account is eligible
    tr_account = input('Transfer\nEnter card number:\n>')
    ifLuhn = False
    ifExists = False

    list_transfer_acc = [int(x) for x in tr_account]
    check_num = list_transfer_acc.pop()

    for i in range(0, len(list_transfer_acc), 2):
        list_transfer_acc[i] = list_transfer_acc[i] * 2
        if list_transfer_acc[i] > 9:
            list_transfer_acc[i] = list_transfer_acc[i] - 9
    if (sum(list_transfer_acc) + check_num) % 10 == 0:
        ifLuhn = True
    # a for cycle to determine the luhn validation

    for row in cursor.execute("SELECT number from card;"):
        if tr_account == row[0]:
            ifExists = True
            break

    if tr_account == user_acc:
        print("You can't transfer money to the same account!")
        return False
    elif not ifLuhn:
        print('Probably you made a mistake in the card number. Please try again!')
        return False
    elif not ifExists:
        print('Such a card does not exist.')
        return False
    else:
        return tr_account


def transfer_sum_validation (user_acc, transfer_account):
    # functions that checks if the funds are available and if yes transfers them to the correct acc
    transfer_sum = input('Enter how much money you want to transfer:\n>')
    cursor.execute("SELECT balance FROM card WHERE number = ?", (user_acc,))
    curr_balance = int(cursor.fetchone()[0])

    if curr_balance < int(transfer_sum):
        print('Not enough money!')
        return False
    else:
        curr_balance -= int(transfer_sum)
        cursor.execute("UPDATE card SET balance =? WHERE number=?",(curr_balance, user_acc))
        conn.commit()

    cursor.execute("SELECT balance FROM card WHERE number =?", (transfer_account,))
    transfer_balance  =int(cursor.fetchone()[0])
    transfer_balance += int(transfer_sum)
    cursor.execute("UPDATE card SET balance=? WHERE number =?", (transfer_balance, transfer_account))
    conn.commit()
    print('Success')


def del_acc(user_acc):
    # function that deletes the current acc from the database
    cursor.execute("DELETE FROM card WHERE number=?", (user_acc,))
    conn.commit()
    print('Account has been closed!')

def check_balance(user_acc):
    # function that prints out the current card balance
    cursor.execute("SELECT balance FROM card WHERE number=?", (user_acc,))
    balance_acc = cursor.fetchone()[0]
    return balance_acc

while True:
    # the main program loop
    choice = input("1. Create an account\n2. Log into account\n0. Exit\n> ")
    # takes in user choice as an input
    if choice == '1':
        acc_creation()
    # the create an account option
    elif choice == '0':
        print('Bye!')
        break
    # the exit option
    while choice == '2':
        If_logged = True
        id = input(f"Enter your card number:\n")
        pn = input(f"Enter your PIN:\n")
        # log into our account option
        user_id = acc_pass_check(id, pn)
        while If_logged:
            # a while loop with a boolean to keep us in the login menu
            choice_login_id = login_menu()
            if choice_login_id:
                # a statement to check what our required action is and to complete it
                if choice_login_id == '1':
                    print(f"Balance: {check_balance(user_id)}")
                elif choice_login_id == '2':
                    add_income(user_id)
                    continue
                elif choice_login_id == '3':
                    valid_acc = transfer_validation_card_num(user_id)
                    if valid_acc:
                        transfer_sum_validation(user_id, valid_acc)
                elif choice_login_id == '4':
                    del_acc(user_id)
                elif choice_login_id == '5':
                    If_logged = False
                    choice = None
                elif choice_login_id == '0':
                    print('Bye!')
                    sys.exit()








