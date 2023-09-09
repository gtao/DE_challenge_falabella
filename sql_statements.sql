CREATE USER de_chall WITH PASSWORD 'pass321';
GRANT postgres TO de_chall;

CREATE TABLE raw_data (
id INT PRIMARY KEY,
name VARCHAR(255),
email VARCHAR(255),
date_of_birth DATE,
address VARCHAR(500),
purchase_amount DECIMAL(10, 2),
last_purchase DATE
);

CREATE TABLE cleaned_data (
id INT PRIMARY KEY,
name VARCHAR(255),
email VARCHAR(255) NULL,
date_of_birth DATE,
address VARCHAR(500),
purchase_amount DECIMAL(10, 2),
last_purchase DATE
);

-- data de tabla `raw_data` generada con función db.generate_data.py a través de librería Faker