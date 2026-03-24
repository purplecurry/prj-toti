-- 유저 테이블
CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email VARCHAR(100),
  password VARCHAR(200),
  nickname VARCHAR(50),
  goal_minutes INTEGER DEFAULT 120,
  default_focus_time INTEGER DEFAULT 25,
  default_break_time INTEGER DEFAULT 5,
  ai_mode VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
);

-- 포모도로 세션 테이블 (날짜 단위)
CREATE TABLE pomodoro_sessions (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  date DATE,
  total_completed INTEGER DEFAULT 0
);

-- 세션 상세 테이블 (하루에 여러 개)
CREATE TABLE session_details (
  id SERIAL PRIMARY KEY,
  session_id INTEGER REFERENCES pomodoro_sessions(id),
  started_at TIMESTAMP,
  ended_at TIMESTAMP,
  duration INTEGER,
  is_completed BOOLEAN DEFAULT FALSE,
  session_type VARCHAR(10)
);

-- 메모 테이블 (유저당 여러 개)
CREATE TABLE memos (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  title TEXT,
  content TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- 투두 테이블 (캘린더 전용, 날짜별 여러 개)
CREATE TABLE todos (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  date DATE,
  content TEXT,
  is_completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

-- 공부기록 테이블 (집중시간만 계산)
CREATE TABLE study_records (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  date DATE,
  total_minutes INTEGER DEFAULT 0,
  completed_sessions INTEGER DEFAULT 0,
  goal_achieved BOOLEAN DEFAULT FALSE
);

-- AI 로그 테이블
CREATE TABLE ai_logs (
  id SERIAL PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),
  message TEXT,
  mode VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW()
);
