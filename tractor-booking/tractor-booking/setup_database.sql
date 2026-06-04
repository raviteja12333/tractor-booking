-- ══════════════════════════════════════════════
-- KisanShakti Tractor Booking — MySQL Setup
-- Run this file once to set up your database
-- ══════════════════════════════════════════════

-- Step 1: Create the database
CREATE DATABASE IF NOT EXISTS tractor_booking
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE tractor_booking;

-- Step 2: Create the bookings table
CREATE TABLE IF NOT EXISTS bookings (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  name         VARCHAR(100)   NOT NULL,
  mobile       VARCHAR(15)    NOT NULL,
  village      VARCHAR(100)   NOT NULL,
  service      VARCHAR(100)   NOT NULL,
  acres        DECIMAL(5,2)   NOT NULL,
  booking_date DATE           NOT NULL,
  created_at   TIMESTAMP      DEFAULT CURRENT_TIMESTAMP
);

-- Step 3: Optional — add a status column for marking completed work
ALTER TABLE bookings
  ADD COLUMN status ENUM('pending','confirmed','completed','cancelled')
  DEFAULT 'pending'
  AFTER booking_date;

-- Step 4: Optional — add notes column
ALTER TABLE bookings
  ADD COLUMN notes TEXT DEFAULT NULL
  AFTER status;

-- ══════════════════════════════════════════════
-- Sample data (optional — for testing)
-- ══════════════════════════════════════════════
INSERT INTO bookings (name, mobile, village, service, acres, booking_date, status) VALUES
  ('Raju Yadav',    '9876543210', 'Dongarkhed', 'Land Ploughing',  3.5, '2025-05-20', 'confirmed'),
  ('Santosh Patil', '9812345678', 'Nanded',     'Rotavator Work',  2.0, '2025-05-22', 'pending'),
  ('Ganesh Shinde', '9898989898', 'Hingoli',    'Harvesting',      5.0, '2025-05-25', 'pending');

-- Verify
SELECT * FROM bookings;
