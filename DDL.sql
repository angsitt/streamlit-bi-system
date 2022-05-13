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

ALTER TABLE hr_brand.cities ALTER COLUMN city_rus VARCHAR(20)
  COLLATE Cyrillic_General_CI_AS;

CREATE TABLE hr_brand.employees
(
	id INT IDENTITY PRIMARY KEY,
	job_title VARCHAR(100),
	work_experience VARCHAR(10),
	is_active CHAR(1),
	source VARCHAR(20) NOT NULL,
	city_id INT DEFAULT 1,
	updated_date DATETIME DEFAULT getdate(),
	FOREIGN KEY (city_id) REFERENCES hr_brand.cities (id)
);

CREATE TABLE hr_brand.reviews
(
	id INT IDENTITY PRIMARY KEY,
	title VARCHAR(300),
	review VARCHAR(2000),
	advantage VARCHAR(1000),
	disadvantage VARCHAR(1000),
	improvement_idea VARCHAR(500),
	score DECIMAL(2,1),
	sentiment VARCHAR(10),
	lang VARCHAR(3) NOT NULL,
	employee_id INT NOT NULL,
	source VARCHAR(20) NOT NULL,
	review_date DATETIME,
	updated_date DATETIME DEFAULT getdate(),
	FOREIGN KEY (employee_id) REFERENCES hr_brand.employees (id)
);

insert into hr_brand.employees (source) 
values ('a')

insert into hr_brand.reviews (review, lang, employee_id, source) 
values ('Happy Birthday to me!', 'eng', 1, 'life')

insert into [hr_brand.#update_sentiment]
values (1, 'pos')

ALTER TABLE hr_brand.reviews ALTER COLUMN title VARCHAR(300)
  COLLATE Cyrillic_General_CI_AS;
ALTER TABLE hr_brand.reviews ALTER COLUMN review VARCHAR(2000)
  COLLATE Cyrillic_General_CI_AS;
ALTER TABLE hr_brand.reviews ALTER COLUMN advantage VARCHAR(1000)
  COLLATE Cyrillic_General_CI_AS;
ALTER TABLE hr_brand.reviews ALTER COLUMN disadvantage VARCHAR(1000)
  COLLATE Cyrillic_General_CI_AS;

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
	('Minsk', N'Минск', 2),
	('Gomel', N'Гомель', 2),
	('Grodno', N'Гродно', 2),
	('Mogilev', N'Могилев', 2),
	('Brest', N'Брест', 2),
	('Vitebsk', N'Витебск', 2),
	('Moscow', N'Москва', 3),
	('Saint Petersburg', N'Санкт-Петербург', 3),
	('Novosibirsk', N'Новосибирск', 3),
	('Kazan', N'Казань', 3),
	('Nizhny Novgorod', N'Нижний Новгород', 3),
	('Samara', N'Самара', 3),
	('Voronezh', N'Воронеж', 3),
	('Tyumen', N'Тюмень', 3),
	('Stavropol', N'Ставрополь', 3),
	('Tolyatti', N'Тольятти', 3),
	('Saratov', N'Саратов', 3),
	('Bishkek', N'Бишкек', 4),
	('Nur-Sultan', N'Нур-Султан', 5),
	('Lviv', N'Львов', 6),
	('Kiev', N'Киев', 6),
	('Khmelnytskyi', N'Хмельницкий', 6),
	('Kharkiv', N'Харьков', 6),
	('Vilnius', N'Вильнюс', 7),
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
select * from hr_brand.reviews;
select * from [hr_brand.#update_sentiment];

create TABLE [hr_brand.#update_sentiment] (id INT PRIMARY KEY, sentiment_upd VARCHAR(10))

UPDATE
             hr_brand.reviews
        SET
             sentiment = u.sentiment_upd
        FROM
             hr_brand.reviews AS t
        INNER JOIN 
             [hr_brand.#update_sentiment] AS u 
        ON
             u.id=t.id and t.sentiment is NULL;