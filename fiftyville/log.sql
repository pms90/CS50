-- Keep a log of any SQL queries you execute as you solve the mystery.

-- .schema

-- The schema are:

    -- creation year INTEGER,
    -- FOREIGN KEY(person id REFERENCES people(id)
    -- );
    -- CREATE TABLE airports (
    -- id INTEGER,
    -- abbreviation TEXT,
    -- full_name TEXT,
    -- city TEXT,
    -- PRIMARY KEY(id)
    -- );
    -- CREATE TABLE flights (
    -- id INTEGER,
    -- origin_airport_id INTEGER,
    -- destination_airport_id INTEGER,
    -- year INTEGER,
    -- month INTEGER,
    -- day INTEGER,
    -- hour INTEGER,
    -- minute INTEGER,
    -- PRIMARY KEY(id),
    -- FOREIGN KEY(origin_airport_id) REFERENCES airports(id),
    -- FOREIGN KEY (destination_airport_id) REFERENCES airports(id)
    -- );
    -- CREATE TABLE passengers (
    -- flight_id INTEGER,
    -- passport_number INTEGER,
    -- seat TEXT,
    -- FOREIGN KEY(flight id) REFERENCES flights(id)
    -- );
    -- CREATE TABLE phone_calls (
    -- id INTEGER,
    -- caller TEXT,
    -- receiver TEXT,
    -- year INTEGER,
    -- month INTEGER,
    -- day INTEGER,
    -- duration INTEGER,
    -- PRIMARY KEY(id)
    -- );
    -- CREATE TABLE people (
    -- id INTEGER,
    -- name TEXT,
    -- phone_number TEXT,
    -- passport_number INTEGER,
    -- license_plate TEXT,
    -- PRIMARY KEY(id)
    -- );
    -- CREATE TABLE bakery_security_logs (
    -- id INTEGER,
    -- year INTEGER,
    -- month INTEGER,
    -- day INTEGER,
    -- hour INTEGER,
    -- minute INTEGER,
    -- activity TEXT,
    -- license_plate TEXT,
    -- PRIMARY KEY(id)
    -- );

-- .tables

-- The tables are:
    -- airports
    -- crime_scene_reports
    -- atm transactions
    -- flights
    -- bakery security logs interviews
    -- bank accounts
    -- passengers
    -- people
    -- phone calls


-- to search for comments in the report
select * from crime_scene_reports csr where csr.year = '2021' and csr.month = '7' and csr.day = '28';  --street: 'Humphrey Street'

-- with this we have some plates buy may not be usefull
select * from bakery_security_logs t where t.year = '2021' and t.month = '7' and t.day = '28';

-- just see
select * from airports t;

-- just see
select * from flights t where t.year = '2021' and t.month = '7' and t.day = '28';

-- from this we get that the thief get into a car in the vakery parking lot, and where in ATM on Leggett Street
select * from interviews where year = '2021' and month = '7' and day = '28';

-- to se the name of the airport of Fiftyville
select a.full_name from airports a
inner join flights f on f.origin_airport_id = a.id
where f.year = '2021' and f.month = '7' and f.day = '28';

-- to se the name and id of the airport of Fiftyville
select a.full_name, a.id from airports a
inner join flights f on f.origin_airport_id = a.id
where f.year = '2021' and f.month = '7' and f.day = '28';

-- to get the id of the destination of all flights from  Fiftyville that day
select f.destination_airport_id from airports a
inner join flights f on f.origin_airport_id = a.id
where f.year = '2021' and f.month = '7' and f.day = '28' and f.origin_airport_id = '8';

-- Fiftyville Regional Airport             | 8  |
-- | O'Hare International Airport            | 1  |
-- | Fiftyville Regional Airport             | 8  |
-- | Fiftyville Regional Airport             | 8  |
-- | Beijing Capital International Airport   | 2  |
-- | Logan International Airport             | 6  |
-- | O'Hare International Airport            | 1  |
-- | Dallas/Fort Worth International Airport | 5  |
-- | Logan International Airport             | 6  |
-- | Fiftyville Regional Airport             | 8  |
-- | Fiftyville Regional Airport             | 8  |
-- | Dubai International Airport             | 7  |
-- | Los Angeles International Airport       | 3  |
-- | LaGuardia Airport                       | 4

-- to get the name of the destination of all flights from  Fiftyville that day
select distinct a.full_name from airports a
inner join flights f on f.destination_airport_id = a.id
where f.year = '2021' and f.month = '7' and f.day = '28' and f.origin_airport_id = '8';

-- Result:
    -- Dubai International Airport
    -- Dallas/Fort Worth International Airport
    -- LaGuardia Airport

-- to get passport numbers
select * from passengers
where flight_id in (
    select id from flights where origin_airport_id= '8'
    and destination_airport_id in (
        select distinct a.id from airports a
        inner join flights f on f.destination_airport_id = a.id
        where f.year = '2021' and f.month = '7' and f.day = '28' and f.origin_airport_id = '8'
        )
    and year = '2021' and month = '7' and day = '28'
);

-- this try not give me results
select distinct p.id, p.name from people p
join bank_accounts ba on p.id = ba.person_id
join atm_transactions atm on ba.account_number = atm.account_number
join airports a on atm.atm_location = a.city
join flights f on a.id = f.origin_airport_id
join passengers ps on f.id = ps.flight_id
where ba.account_number IN (
    select distinct account_number from atm_transactions
    where atm_location like '%Humphrey Street%' and year = 2021 and month = 7 and day = 28
    )
and a.full_name like '%International Airport%'
and f.year = 2021 and f.month = 7 and f.day = 28
and ps.passport_number = p.passport_number;


-- select
--     select passport_number from passengers
--     where flight_id in (
--         select id from flights where origin_airport_id= '8'
--         and destination_airport_id in (
--             select distinct a.id from airports a
--             inner join flights f on f.destination_airport_id = a.id
--             where f.year = '2021' and f.month = '7' and f.day = '28' and f.origin_airport_id = '8'
--             )
--         and year = '2021' and month = '7' and day = '28'
--     );

SELECT * FROM people
JOIN bakery_security_logs bsl ON bsl.license_plate = people.license_plate
WHERE bsl.year = 2021
AND bsl.month = 7
AND bsl.day = 28
AND bsl.hour = 10
AND bsl.minute >= 15
AND bsl.minute <= 30; --10 min perception could be 15

-- Suspects acording to use of bank ATM
SELECT people.name, atm_transactions. transaction_type FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE atm_transactions.transaction_type = "withdraw"
AND atm_location = "Leggett Street"
AND atm_transactions.year = 2021
AND atm_transactions.month = 7
AND atm_transactions.day = 28;

-- Withdraws:Bruce Diana Brooke Kenny Iman Luca Taylor Benista

-- get phone numbers of suspects
SELECT caller, receiver, duration FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28
ORDER BY duration ASC;

-- Get names and phone numbers of first fly (and destination)
SELECT * FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.year = 2021 AND flights.month = 7 AND flights.day = 29
AND flights.hour = 8 AND flights.minute = 20  -- first fly (firs hypotesis)
ORDER BY passengers.passport_number;
-- destination_airport_id=4  --> LaGuardia Airport

-- Passengers: Edward Sofia Taylor Bruce Doris Kelsey Luca Kenny

-- We now con compare phone_nubers of the passengers with the callers of the previous table

-- To get the names asociated with the phone calls:
SELECT name, phone_calls.duration
FROM people
JOIN phone_calls
ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60
ORDER BY phone_calls.duration;
SELECT name, phone_calls.duration
FROM people
JOIN phone_calls
ON people.phone_number = phone_calls.receiver
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28
AND phone_calls.duration <= 60
ORDER BY phone_calls.duration;


-- Larry Jacqueline James Robin Philip Melissa Jack Anna Doris Luca


-- getting names asocieted with license plates that thay, that time
SELECT name, bsl.hour, bsl.minute FROM people
JOIN bakery_security_logs bsl ON people.license_plate = bsl.license_plate
WHERE bsl.year = 2021 AND bsl.month = 7 AND bsl.day = 28
AND bsl.activity = 'exit'
AND bsl.hour = 10 AND bsl.minute >= 15 AND bsl.minute <= 30
ORDER BY bsl.minute;

-- from here coul be bruce or diana. But we can see that diana is not a passanger (previous list)
-- So the best gues is tha Bruce is the thief!! He fly to LaGuardia Airport, New York


--
SELECT name, phone_calls.duration
FROM people
JOIN phone_calls
ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28 AND phone_calls.duration <= 60
ORDER BY phone_calls.duration;

-- Now I want to know with who people Bruce talk
SELECT *
FROM people
JOIN phone_calls
ON people.phone_number = phone_calls.caller
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28
ORDER BY people.name;
-- Bruce talk 45 minutes with just one number: (375) 555-8161

-- Now I want to know who have the nomber '(375) 555-8161'
SELECT *
FROM people
JOIN phone_calls
ON people.phone_number = phone_calls.receiver
WHERE phone_calls.year = 2021 AND phone_calls.month = 7 AND phone_calls.day = 28
AND phone_calls.receiver = '(375) 555-8161'
ORDER BY people.name;
-- This number correspond to Robin!! So Robin is the accomplice