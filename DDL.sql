CREATE DATABASE epam_reviews;

CREATE SCHEMA hr_brand;

CREATE TABLE hr_brand.countries
(
	id INT IDENTITY PRIMARY KEY,
	country VARCHAR(20) NOT NULL,
	country_code VARCHAR(3) NOT NULL,
	updated_date DATETIME DEFAULT getdate()
);

CREATE TABLE hr_brand.cities
(
	id INT IDENTITY PRIMARY KEY,
	city VARCHAR(20) NOT NULL,
	city_rus VARCHAR(20),
	country_id INT NOT NULL,
	updated_date DATETIME DEFAULT getdate(),
	FOREIGN KEY (country_id) REFERENCES hr_brand.countries (id)
);

CREATE TABLE hr_brand.employees
(
	id INT IDENTITY PRIMARY KEY,
	job_title VARCHAR(100),
	work_experience VARCHAR(10),
	is_active CHAR(1),
	city_id INT DEFAULT 1,
	updated_date DATETIME DEFAULT getdate(),
	FOREIGN KEY (city_id) REFERENCES hr_brand.cities (id)
);

CREATE TABLE hr_brand.company_reviews
(
	id INT IDENTITY PRIMARY KEY,
	title VARCHAR(300),
	review VARCHAR(2000),
	advantage VARCHAR(1000),
	disadvantage VARCHAR(1000),
	improvement_idea VARCHAR(500),
	score DECIMAL(2,1),
	employee_id INT NOT NULL,
	source VARCHAR(20) NOT NULL,
	review_date DATETIME,
	updated_date DATETIME DEFAULT getdate(),
	FOREIGN KEY (employee_id) REFERENCES hr_brand.employees (id)
);

INSERT INTO hr_brand.countries (country, country_code)
VALUES 
	('N/A', 'N/A'),
	('Belarus', 'BLR'),
	('Russia', 'RUS'),
	('Kyrgyzstan', 'KGZ'),
	('Kazakhstan', 'KAZ'),
	('Ukraine', 'UKR'),
	('Lithuania', 'LTU'),
	('Unitated States', 'USA');

INSERT INTO hr_brand.cities (city, city_rus, country_id)
VALUES 
	('N/A', 'N/A', 1),
	('Minsk', 'Минск', 2),
	('Gomel', 'Гомель', 2),
	('Grodno', 'Гродно', 2),
	('Mogilev', 'Могилев', 2),
	('Brest', 'Брест', 2),
	('Vitebsk', 'Витебск', 2),
	('Moscow', 'Москва', 3),
	('Saint Petersburg', 'Санкт-Петербург', 3),
	('Novosibirsk', 'Новосибирск', 3),
	('Kazan', 'Казань', 3),
	('Nizhny Novgorod', 'Нижний Новгород', 3),
	('Samara', 'Самара', 3),
	('Voronezh', 'Воронеж', 3),
	('Tyumen', 'Тюмень', 3),
	('Stavropol', 'Ставрополь', 3),
	('Tolyatti', 'Тольятти', 3),
	('Saratov', 'Саратов', 3),
	('Bishkek', 'Бишкек', 4),
	('Nur-Sultan', 'Нур-Султан', 5),
	('Lviv', 'Львов', 6),
	('Kiev', 'Киев', 6),
	('Khmelnytskyi', 'Хмельницкий', 6),
	('Kharkiv', 'Харьков', 6),
	('Vilnius', 'Вильнюс', 7),
	('San Jose', NULL, 8),
	('Austin', NULL, 8),
	('Los Angeles', NULL, 8),
	('Mountain View', NULL, 8),
	('Boston', NULL, 8),
	('Irvine', NULL, 8),
	('Westwood', NULL, 8),
	('Bellevue', NULL, 8),
	('New York City', NULL, 8),
	('Newtown', NULL, 8),
	('Dallas', NULL, 8),
	('Weehawken', NULL, 8),
	('San Francisco', NULL, 8),
	('Princeton', NULL, 8),
	('Buffalo', NULL, 8),
	('Sunnyvale', NULL, 8),
	('Rockford', NULL, 8),
	('Wheeling', NULL, 8),
	('Sunnyvale', NULL, 8),
	('Rockford', NULL, 8),
	('Wheeling', NULL, 8),
	('Belmar', NULL, 8);


select * from hr_brand.countries;
select * from hr_brand.cities;
select * from hr_brand.employees;
select * from hr_brand.company_reviews;
