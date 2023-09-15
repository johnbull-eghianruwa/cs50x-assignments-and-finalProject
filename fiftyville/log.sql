-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28;

-- Interviews were conducted today with three witnesses who were present at the time-each of their interview transcripts mentions the backery
SELECT transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day = 28 AND transcript LIKE "%bakery%";

SELECT bakery_security_logs.activity, bakery_security_logs.license_plate, people.name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE bakery_security_logs.year = 2021
AND backery_security