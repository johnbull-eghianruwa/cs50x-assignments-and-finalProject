-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28;

-- Interviews were conducted today with three witnesses who were present at the time-each of their interview transcripts mentions the backery
SELECT transcript FROM interviews
WHERE year = 2021 AND month = 7 AND day 