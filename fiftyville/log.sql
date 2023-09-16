-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28 AND street = "Humphrey Street";

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three -- -- witnesses who were present at the time – each of their interview transcripts mentions the bakery. |
SELECT transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

-- First transcript!
-- Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you
-- have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time -- frame
SELECT name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
AND bakery_security_logs.month = 7
AND bakery_security_logs.day = 28
AND bakery_security_logs.hour = 10
AND bakery_security_logs.minute >= 15
AND bakery_security_logs.minute <= 25
AND activity = "exit";
-- Suspects: Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey



