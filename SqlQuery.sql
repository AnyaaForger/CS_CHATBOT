-- CREATE TABLE personal_data (
--     id INT IDENTITY(1,1) PRIMARY KEY,
--     name NVARCHAR(255) NULL,
--     number NVARCHAR(255) NULL,
--     email NVARCHAR(255) NULL,
--     city NVARCHAR(255) NULL
-- );

CREATE TABLE gym_membership (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    price DECIMAL(10, 3),
    session int NULL
);

ALTER TABLE gym_membership
ADD member_goals_info NVARCHAR(500)

CREATE TABLE prospect_member (
    id INT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    number NVARCHAR(255) NULL,
    email NVARCHAR(255) NULL,
	city NVARCHAR(255) NULL,
	member_goals NVARCHAR(255) NULL
);