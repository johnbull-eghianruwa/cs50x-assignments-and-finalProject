-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28;

-- Interviews were conducted today with three witnesses who were present at the time-each of their interview transcripts mentions the backery
SELECT transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery
SELECT bakery_security_logs.activity, bakery_security_logs.license_plate, people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25;
-- Suspects: Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey
SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = Bank_accounts.account_number
WHERE year = 2021
AND month = 7
AND day = 28
AND atm_location = "leggett Street"
AND transaction_type = "withdraw";