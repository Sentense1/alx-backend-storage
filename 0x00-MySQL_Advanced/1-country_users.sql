-- Creates a table with attributes: id, email, name, and country
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255),
	country CHAR(2) NOT NULL DEFAULT 'US' CHECK (country IN ('US', 'CO', 'TN'))
);
