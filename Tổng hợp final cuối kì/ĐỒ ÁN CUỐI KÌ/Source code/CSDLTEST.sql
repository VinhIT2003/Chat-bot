-- Chọn cơ sở dữ liệu
USE test;
GO

-- Tạo bảng customers
CREATE TABLE customers (
    id INT PRIMARY KEY,
    first_name NVARCHAR(50),
    last_name NVARCHAR(50),
    email NVARCHAR(100),
    phone NVARCHAR(20),
    address NVARCHAR(255),
    created_at DATETIME DEFAULT GETDATE()
);

-- Dữ liệu mẫu cho customers
INSERT INTO customers VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '123456789', '123 Main St', GETDATE()),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '987654321', '456 Elm St', GETDATE());


-- Tạo bảng products
CREATE TABLE products (
    id INT PRIMARY KEY,
    name NVARCHAR(100),
    description NVARCHAR(255),
    price DECIMAL(10,2),
    category NVARCHAR(50),
    in_stock INT,
    created_at DATETIME DEFAULT GETDATE()
);

-- Dữ liệu mẫu cho products
INSERT INTO products VALUES
(1, 'Laptop', 'Powerful laptop', 1200.00, 'Electronics', 50, GETDATE()),
(2, 'Phone', 'Smartphone with good camera', 700.00, 'Electronics', 100, GETDATE()),
(3, 'Headphones', 'Noise-cancelling headphones', 150.00, 'Accessories', 200, GETDATE());


-- Tạo bảng orders
CREATE TABLE orders (
    id INT PRIMARY KEY,
    customer_id INT FOREIGN KEY REFERENCES customers(id),
    order_date DATE,
    status NVARCHAR(20),
    total_amount DECIMAL(10,2),
    created_at DATETIME DEFAULT GETDATE()
);

-- Dữ liệu mẫu cho orders
INSERT INTO orders VALUES
(1, 1, '2025-04-01', 'Completed', 1900.00, GETDATE()),
(2, 2, '2025-04-05', 'Pending', 700.00, GETDATE());


-- Tạo bảng order_items
CREATE TABLE order_items (
    id INT PRIMARY KEY,
    order_id INT FOREIGN KEY REFERENCES orders(id),
    product_id INT FOREIGN KEY REFERENCES products(id),
    quantity INT,
    price_per_unit DECIMAL(10,2)
);

-- Dữ liệu mẫu cho order_items
INSERT INTO order_items VALUES
(1, 1, 1, 1, 1200.00), -- John bought 1 Laptop
(2, 1, 3, 2, 150.00),  -- John bought 2 Headphones
(3, 2, 2, 1, 700.00);  -- Jane bought 1 Phone


select * from products