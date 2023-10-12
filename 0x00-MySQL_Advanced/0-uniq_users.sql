-- Creates 'users' table if table is not existing.
CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VAR(255),
	PRIMARY KEY (id)
);
