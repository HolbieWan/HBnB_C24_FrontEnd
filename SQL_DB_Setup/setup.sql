-- Create User table
CREATE TABLE User (
    id CHAR(36) PRIMARY KEY, -- UUID format
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create Place table
CREATE TABLE Place (
    id CHAR(36) PRIMARY KEY, -- UUID format
    title VARCHAR(255),
    description TEXT,
    price DECIMAL(10, 2),
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Create Review table
CREATE TABLE Review (
    id CHAR(36) PRIMARY KEY, -- UUID format
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    UNIQUE (user_id, place_id) -- Ensures one review per user per place
);

-- Create Amenity table
CREATE TABLE Amenity (
    id CHAR(36) PRIMARY KEY, -- UUID format
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Create Place_Amenity table (Many-to-Many relationship)
CREATE TABLE Place_Amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);

-- Insert Administrator User
INSERT INTO User (id, first_name, last_name, email, password, is_admin) 
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 
    'Admin', 
    'HBnB', 
    'admin@hbnb.io', 
    '$2b$12$dX.JJhyV1HnDkQfb0Zzg4OY5FO.SOw7Kt0PYeIhYjtgQvdWipzJjq', -- bcrypt hash for 'admin1234'
    TRUE
);

-- Insert Initial Amenities
INSERT INTO Amenity (id, name) 
VALUES 
    ('9f83d45f-14f6-4b7e-941e-c2c1623e71b3', 'WiFi'),
    ('3b99d6f3-405e-4f7c-9f9a-cfdcba529457', 'Swimming Pool'),
    ('f03d4b9d-3b8e-4a3b-9f1f-a16f4b9c74a5', 'Air Conditioning');

-- Insert Initial Places
INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id)
VALUES 
    ('e9fa54dd-cb8e-4dca-9d1c-6299a07e9c8f', 'Tuff Gong Records', 'Rastaman\'s place', 10.00, 0.34, 0.24, '36c9050e-ddd3-4c3b-9731-9f487208bbc1');

-- Insert Initial Place_Amenity relationships
INSERT INTO Place_Amenity (place_id, amenity_id)
VALUES 
    ('e9fa54dd-cb8e-4dca-9d1c-6299a07e9c8f', '9f83d45f-14f6-4b7e-941e-c2c1623e71b3'), -- WiFi
    ('e9fa54dd-cb8e-4dca-9d1c-6299a07e9c8f', '3b99d6f3-405e-4f7c-9f9a-cfdcba529457'); -- Swimming Pool

-- Insert Initial Review
INSERT INTO Review (id, text, rating, user_id, place_id)
VALUES 
    ('d6c7e5ab-0f24-4b9b-92c9-4084d12d7df0', 'Great experience!', 5, '36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'e9fa54dd-cb8e-4dca-9d1c-6299a07e9c8f');