-- db/initdb/init.sql

CREATE TABLE sample_data (
  id          SERIAL,
  first_name  VARCHAR(100) NOT NULL,
  last_name   VARCHAR(100) NOT NULL,
  company_name VARCHAR(255),
  address     TEXT,
  city        VARCHAR(100),
  state       CHAR(2) CHECK (state ~ '^[A-Za-z]{2}$'),
  zip         VARCHAR(10),
  phone1      VARCHAR(20),
  phone2      VARCHAR(20),
  email       VARCHAR(255) NOT NULL,
  department  VARCHAR(100),
  PRIMARY KEY (first_name, last_name, email)
);
