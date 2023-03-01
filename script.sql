DROP TYPE role CASCADE;

CREATE TYPE role AS ENUM ('driver', 'mechanic');

DROP TABLE users CASCADE;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(50) UNIQUE NOT NULL,
  password VARCHAR(1000) NOT NULL,
  role role NOT NULL DEFAULT 'driver'
);

COMMIT;