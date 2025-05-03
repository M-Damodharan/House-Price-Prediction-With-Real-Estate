-- Create the database
CREATE DATABASE IF NOT EXISTS fruits;

-- Use the newly created database
USE fruits;

-- Create the 'buyer' table
CREATE TABLE IF NOT EXISTS buyer (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    mail VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    password VARCHAR(100) NOT NULL,
    acc ENUM('yes', 'no') DEFAULT 'no'
);

-- Create the 'seller' table
CREATE TABLE IF NOT EXISTS seller (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    mail VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    password VARCHAR(100) NOT NULL,
    accno VARCHAR(20) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    bal DECIMAL(10,2) DEFAULT 0
);

-- Create the 'account' table
CREATE TABLE IF NOT EXISTS account (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    acc VARCHAR(20) NOT NULL,
    branch VARCHAR(50) NOT NULL,
    amount DECIMAL(10,2) NOT NULL
);

-- Create the 'products' table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seller VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(50) NOT NULL,
    hash VARCHAR(64) NOT NULL,
    img VARCHAR(255) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    `desc` TEXT
);

-- Create the 'purchase' table
CREATE TABLE IF NOT EXISTS purchase (
    id INT AUTO_INCREMENT PRIMARY KEY,
    seller VARCHAR(100) NOT NULL,
    buyer VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    rate DECIMAL(10,2) NOT NULL
);
