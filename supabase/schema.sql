-- Run this once in Supabase: SQL Editor → New query → paste → Run

create table if not exists learning_goals (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  target_hours numeric,
  progress_percent numeric not null default 0,
  notes text not null default '',
  resources jsonb not null default '[]',
  weekly_hours jsonb not null default '[]',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists experiments (
  id uuid primary key default gen_random_uuid(),
  title text not null,
  description text not null default '',
  dependencies jsonb not null default '[]',
  next_action text not null default '',
  status text not null default 'not_started' check (status in ('not_started', 'in_progress', 'completed')),
  notes text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table if not exists service_entries (
  id uuid primary key default gen_random_uuid(),
  date date not null,
  description text not null,
  hours numeric not null,
  reflection text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

-- Optional: trigger to keep updated_at in sync (run if you want auto updated_at)
create or replace function set_updated_at()
returns trigger as $$
begin
  new.updated_at = now();
  return new;
end;
$$ language plpgsql;

drop trigger if exists learning_goals_updated_at on learning_goals;
create trigger learning_goals_updated_at
  before update on learning_goals
  for each row execute function set_updated_at();

drop trigger if exists experiments_updated_at on experiments;
create trigger experiments_updated_at
  before update on experiments
  for each row execute function set_updated_at();

drop trigger if exists service_entries_updated_at on service_entries;
create trigger service_entries_updated_at
  before update on service_entries
  for each row execute function set_updated_at();
