CREATE TABLE transactions(
   member_id INT NOT NULL,
   date DATE,
   country VARCHAR(2) NOT NULL,
   gender VARCHAR(6) NOT NULL,
   ip_address VARCHAR(15) NOT NULL,
   amount FLOAT NOT NULL,
   vip VARCHAR(100) NOT NULL,
   product_id INT NOT NULL,
   card_type VARCHAR(100) NOT NULL,
   serial VARCHAR(12) NOT NULL,
   zone VARCHAR(6) NOT NULL
) ENGINE=NDBCLUSTER DEFAULT CHARSET=latin1;