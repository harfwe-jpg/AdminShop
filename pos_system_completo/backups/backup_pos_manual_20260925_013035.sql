-- Respaldo SQL de POS System
-- Fecha: 2026-09-25 01:30:35

BEGIN TRANSACTION;
CREATE TABLE businesses (
	id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	owner_username VARCHAR(100) NOT NULL, 
	owner_password VARCHAR(10) NOT NULL, 
	created_at DATETIME, 
	is_active BOOLEAN, 
	PRIMARY KEY (id), 
	UNIQUE (owner_username)
);
INSERT INTO "businesses" VALUES(1,'Tienda Doña Pelos','Jaime Perez','0000','2026-09-25 07:17:50.604583',1);
CREATE TABLE licenses (
	id INTEGER NOT NULL, 
	license_key VARCHAR(100) NOT NULL, 
	license_type VARCHAR(50) NOT NULL, 
	device_id VARCHAR(100), 
	activated_at DATETIME, 
	expires_at DATETIME, 
	is_active BOOLEAN, 
	max_devices INTEGER, 
	registered_devices INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (license_key), 
	UNIQUE (device_id)
);
INSERT INTO "licenses" VALUES(1,'MEM-1M-2026-XOXTL-79F4K','TRIAL','192.168.1.5-1790320596.964392','2026-09-25 07:16:37.054509','2026-10-25 01:16:36.964392',1,1,1);
CREATE TABLE products (
	id INTEGER NOT NULL, 
	business_id INTEGER NOT NULL, 
	barcode VARCHAR(50) NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	product_type VARCHAR(50), 
	public_price FLOAT NOT NULL, 
	supplier_price FLOAT NOT NULL, 
	stock INTEGER, 
	min_stock_alert INTEGER, 
	created_at DATETIME, 
	updated_at DATETIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(business_id) REFERENCES businesses (id), 
	UNIQUE (barcode), 
	UNIQUE (name)
);
INSERT INTO "products" VALUES(1,1,'1234567890','coca-cola 600ml','pieza',28.0,20.0,24,3,'2026-09-25 07:20:10.420033','2026-09-25 07:20:33.847334');
CREATE TABLE registered_devices (
	id INTEGER NOT NULL, 
	license_id INTEGER NOT NULL, 
	device_id VARCHAR(100) NOT NULL, 
	device_type VARCHAR(50), 
	registered_at DATETIME, 
	is_active BOOLEAN, 
	PRIMARY KEY (id), 
	FOREIGN KEY(license_id) REFERENCES licenses (id), 
	UNIQUE (device_id)
);
INSERT INTO "registered_devices" VALUES(1,1,'192.168.1.5-1790320596.964392','desktop','2026-09-25 07:16:37.092932',1);
CREATE TABLE sale_items (
	id INTEGER NOT NULL, 
	sale_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	quantity FLOAT NOT NULL, 
	unit_price FLOAT NOT NULL, 
	subtotal FLOAT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(sale_id) REFERENCES sales (id), 
	FOREIGN KEY(product_id) REFERENCES products (id)
);
CREATE TABLE sales (
	id INTEGER NOT NULL, 
	business_id INTEGER NOT NULL, 
	shift_id INTEGER NOT NULL, 
	total_amount FLOAT NOT NULL, 
	payment_method VARCHAR(50) NOT NULL, 
	cash_received FLOAT, 
	change FLOAT, 
	sale_date DATETIME, 
	sale_time TIME, 
	PRIMARY KEY (id), 
	FOREIGN KEY(business_id) REFERENCES businesses (id), 
	FOREIGN KEY(shift_id) REFERENCES shifts (id)
);
CREATE TABLE shifts (
	id INTEGER NOT NULL, 
	business_id INTEGER NOT NULL, 
	shift_number INTEGER NOT NULL, 
	initial_amount FLOAT NOT NULL, 
	started_at DATETIME, 
	closed_at DATETIME, 
	is_closed BOOLEAN, 
	closed_by VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(business_id) REFERENCES businesses (id)
);
INSERT INTO "shifts" VALUES(1,1,1,2500.0,'2026-09-25 07:18:43.281059',NULL,0,NULL);
COMMIT;
