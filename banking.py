#!/usr/bin/env python3
# -*- coding: cp1251

import sqlite3
import random


def generate_pin():
    str_pin = ''
    for i in range(4):
        str_pin += random.choice('1234567890')
    return str_pin


def luhn_algorithm(input_str):
    current_array = []
    
    # 1. отбрасываем последнюю цифру (контрольную)
    current_str = input_str[:-1]
    # 2. Умножаем нечетные цифры на 2 (для отслеживания перепутанных цифр)
    # 3. отнимаем 9 от чисел >9
    for i in range(0, len(current_str)):
        if i % 2 == 0:
            x = 2 * int(current_str[i])
            if x > 9:
                x -= 9
            current_array.append(x)
        else: 
            current_array.append(int(current_str[i]))
    # 4. складываем все цифры
    x_sum = 0
    for i in current_array:
        x_sum += i
    # 5. Результат должен быть кратным / делиться на 10 (вместе с последней цифрой)
    check_sum = x_sum % 10
    if check_sum > 0:
        check_sum = 10 - check_sum 
    
    # собираем выходную строку
    output_str = input_str[:-1] + str(check_sum)  
    
    return output_str


def logged_in(account_number):
    while True:
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
        print('0. Exit')

        x = int(input())
        print()

        if x == 1:
            print('Balance:', cards[account_number][1])
            print()
        elif x == 2:
            print('Enter income:')
            income = int(input())
            cards[account_number][1] += income

            cur.execute(f'UPDATE card SET balance = balance + {income} WHERE number = "{card_number}";')
            conn.commit()

            print('Income was added!')
            print()
        elif x == 3:  # 3. Do transfer
            print('Transfer')
            print('Enter card number:')
            card_to_transfer = input()
            if card_to_transfer == luhn_algorithm(card_to_transfer):
                # checking that the card exists
                try:
                    current_amount = cards[card_to_transfer][1]
                    current_amount = cards[account_number][1]
                except KeyError:
                    print('Such a card does not exist.')
                else:
                    print('Enter how much money you want to transfer:')
                    money_to_transfer = int(input())
                    if money_to_transfer > current_amount:
                        print('Not enough money!')
                        print()
                    else:
                        # transfer
                        cards[account_number][1] -= money_to_transfer
                        cards[card_to_transfer][1] += money_to_transfer

                        cur.execute(f'UPDATE card SET balance = balance - {money_to_transfer} WHERE number = {account_number};')
                        conn.commit()
                        cur.execute(f'UPDATE card SET balance = balance + {money_to_transfer} WHERE number = {card_to_transfer};')
                        conn.commit()

                        print('Success!')
                        print()
                        # print(cards[account_number][1])
            else:
                print('Probably you made a mistake in the card number. Please try again!')
                print()
        elif x == 4:
            # delete account
            cur.execute(f'DELETE FROM card WHERE number = "{card_number}";')
            conn.commit()

            print('The account has been closed!')
            print()

            break
        elif x == 5:
            break
        elif x == 0:
            break
    return x


conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
# cur.execute('CREATE DATABASE card.s3db;')
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY AUTOINCREMENT, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')
conn.commit()

cur.execute('DELETE FROM card;')
conn.commit()


IIN = '400000'
max_can = 844943340  # customer account number
checksum = '5'

cards = {}

while True:
    print('1. Create an account')
    print('2. Log into account')
    print('0. Exit')
    n = int(input())
    if n == 1:
        card_number = f'{IIN}{max_can}{checksum}'          
        pin = generate_pin()
        print()
        print('Your card has been created')
        print('Your card number:')
        # print(card_number)
        card_number = luhn_algorithm(card_number)
        print(card_number)
        print('Your card PIN:')
        print(pin)
        print()

        # пишем в массив
        cards[card_number] = [pin, 0]

        # пишем в базу
        sql_sql = f'INSERT INTO card (id, number, pin, balance) VALUES ({card_number}, {card_number}, {pin}, 0);'
        cur.execute(sql_sql)
        conn.commit()

        max_can += 1
    elif n == 2: 
        print('Enter your card number:')
        card_number = input()
        print('Enter your PIN:')
        pin = input()
       
        try: 
            if cards[card_number][0] == pin:
                print()
                print('You have successfully logged in!')
                print()

                if logged_in(card_number) == 0:
                    break
            else:
                print('Wrong card number or PIN!')
        except KeyError:
            print('Wrong card number or PIN!')
    elif n == 0:
        break

# cur.execute('DELETE FROM card;')
# conn.commit()
