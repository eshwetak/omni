-- django-admin startproject omni

CREATE TABLE category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(150) NOT NULL
);

CREATE TABLE country (
    id int AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(200) not null,
    iso_code VARCHAR(200) not null
);

CREATE TABLE `state` (
    id INT AUTO_INCREMENT PRIMARY KEY,
    country_id INT,
    INDEX country_ind (country_id),
    FOREIGN KEY (country_id)
        REFERENCES country(id)
        ON DELETE CASCADE,
    `name` varchar(200) not null
);

Create table vendors (
	id INT AUTO_INCREMENT PRIMARY KEY,
	country_id int,
	index country_ind (country_id),
	FOREIGN KEY (country_id) REFERENCES country(id),
	state_id int,
	index state_ind (state_id),
	FOREIGN KEY (state_id) REFERENCES state(id),
	display_name varchar(200) not null,
	latitude varchar(200) not null,
	longitude varchar(200) not null
);

alter table vendors
add column open_slot VARCHAR(250) default '9:00AM - 6:00PM';


CREATE TABLE products (
	id INT AUTO_INCREMENT PRIMARY KEY,
	display_name VARCHAR(150) NOT NULL,
	category_id int,
	index category_ind (category_id),
	FOREIGN KEY (category_id) REFERENCES category(id),
	vendor_id int,
	index vendor_ind (vendor_id),
	FOREIGN KEY (vendor_id) REFERENCES vendors(id),
	style Varchar(150),
	kind varchar(250),
	image varchar(1500),
	dimension LONGTEXT
);

create table rating (
	id INT AUTO_INCREMENT PRIMARY KEY,
	product_id int,
	index product_ind (product_id),
	FOREIGN KEY (product_id) REFERENCES products(id),
	vendor_id int,
	index vendor_ind (vendor_id),
	FOREIGN KEY (vendor_id) REFERENCES vendors(id),
	`value` int not null
);

create table stock (
	id INT AUTO_INCREMENT PRIMARY KEY,
	product_id int,
	index product_ind (product_id),
	FOREIGN KEY (product_id) REFERENCES products(id),
	vendor_id int,
	index vendor_ind (vendor_id),
	FOREIGN KEY (vendor_id) REFERENCES vendors(id),
	`status` BOOLEAN not null 
);
alter table stock
alter `status` set default True;

create table price (
	id INT AUTO_INCREMENT PRIMARY KEY,
	currency varchar(200) not null,
	amount VARCHAR(250) not null,
	product_id int,
	index product_ind (product_id),
	FOREIGN KEY (product_id) REFERENCES products(id),
	vendor_id int,
	index vendor_ind (vendor_id),
	FOREIGN KEY (vendor_id) REFERENCES vendors(id),
	country_id int,
	index country_ind (country_id),
	FOREIGN KEY (country_id) REFERENCES country(id),
	state_id int,
	index state_ind (state_id),
	FOREIGN KEY (state_id) REFERENCES state(id)
);

