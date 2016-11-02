
DROP TABLE users;
CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(120) UNIQUE,
  phone VARCHAR(12) UNIQUE,
  passhash VARCHAR(120) UNIQUE,
  pi_id VARCHAR(120) UNIQUE,
  created_at DATETIME
);

DROP TABLE video;
CREATE TABLE video (
  id INT PRIMARY KEY,
  user_id INT,
  s3_video_url VARCHAR(120)
  s3_gif_url VARCHAR(120)
  created_at DATETIME
  FOREIGN KEY (user_id) REFERENCES users(id)
);
