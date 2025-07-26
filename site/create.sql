CREATE TABLE roles(
    id SERIAL PRIMARY KEY,
    role_name VARCHAR(10) UNIQUE NOT NULL
);

INSERT INTO roles (role_name) VALUES ('admin');
INSERT INTO roles (role_name) VALUES ('manager');
INSERT INTO roles (role_name) VALUES ('user');
INSERT INTO roles (role_name) VALUES ('guest');

DROP TABLE IF EXISTS users;
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    name VARCHAR(20) NOT NULL UNIQUE,
    user_password VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (name, user_password) VALUES 
('Ольга', '123'),
('Дмитрий', '111'),
('Елена', '222'),
('Сергей', '333'),
('Анна', '000');


CREATE TABLE loging_password(
    id SERIAL PRIMARY KEY,
    role_id INT REFERENCES roles(id),
    loggin VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL
)

INSERT INTO loging_password(role_id, loggin, password) 
VALUES 
(1, 'admin', 'Iadmin'),
(2, 'manager', 'Imanager'),
(3, 'user', 'Iuser'),
(4, 'guest', '123');

CREATE INDEX idx_users_username ON users(name);
CREATE INDEX idx_users_role  ON users(role_id);