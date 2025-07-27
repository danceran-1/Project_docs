DROP TABLE IF EXISTS roles;
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
    user_password  VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

INSERT INTO users (name, user_password) VALUES 
('Леха','$2b$12$Q/BWj6KpvXeegUJbC79m8Oh3cN7ugiqTr8Rbt/LpNkK3V4/jhi97G'),
('Ольга', '$2b$12$EicQ7HZ.B8W6J7X3Y2nYp.9gT7U1wRjJq3kYlLmNpQsWvX1V2sZbG'),
('Дмитрий', '$2b$12$N9qo8uLOickgx2ZMRZoMy.Mrq4L9n7M3B6YFJYzQjFjTfYV6WY1Oe'),
('Елена', '$2b$12$3mR5W7vTcR1H9qKJ8bL0NuYjXz2V4sDr9wA1B2C3D4E5F6G7H8I9J'),
('Сергей', '$2b$12$7yH8J9K0L1M2N3O4P5Q6R.SaTbUcVdWeXfYgZhAiBjCkDlEmFnGoH'),
('Анна', '$2b$12$1A2B3C4D5E6F7G8H9I0J.KlMnOpQrStUvWxYzZaBcDeEfFgGhHiJkL');

DROP TABLE IF EXISTS loging_password;
CREATE TABLE loging_password(
    id SERIAL PRIMARY KEY,
    role_id INT REFERENCES roles(id),
    loggin VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
)

INSERT INTO loging_password(role_id, loggin, password) 
VALUES 
(1, 'admin', '$2b$12$rvsio4NfVE9vXiMPT7KO5.fNr01NyAhTY.NGF7YfSuHDPoHEqzn7u'),
(2, 'manager', '$2b$12$LjaQPEGZGqXsMY.z00jm9eRmAcMIgA2Wo6tiNayDt3LmiJXPxtw4i'),
(3, 'user', '$2b$12$qcXYWK6duTdCOlsLWBajGeo0oO0i.EO6g5e1GsIEhWR6mkVEqnMnK');

#индексы

CREATE INDEX idx_users_username ON users(name);
CREATE INDEX idx_users_role  ON users(user_password);