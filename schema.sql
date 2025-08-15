
create extension if not exists pgcrypto;

create table if not exists app_user(
  id uuid primary key default gen_random_uuid(),
  email text unique not null,
  phone_e164 text,
  tz text default 'Asia/Dubai',
  created_at timestamptz default now()
);

create table if not exists merchant(
  id serial primary key,
  name text not null,
  domain text,
  normalized text unique,
  category text check (category in ('GROCERY','FOOD','ONLINE','OTHER')) not null
);

create table if not exists raw_event(
  id uuid primary key default gen_random_uuid(),
  user_id uuid references app_user(id),
  source text check (source in ('EMAIL','SMS','BANK_CSV')) not null,
  payload jsonb not null,
  received_at timestamptz default now()
);

create table if not exists txn(
  id uuid primary key default gen_random_uuid(),
  user_id uuid references app_user(id),
  event_id uuid references raw_event(id),
  merchant_id int references merchant(id),
  merchant_text text,
  category text check (category in ('GROCERY','FOOD','ONLINE','OTHER')) not null,
  amount_aed numeric(12,2) not null,
  currency text default 'AED',
  ordered_at timestamptz not null,
  notes text
);

create table if not exists budget(
  id uuid primary key default gen_random_uuid(),
  user_id uuid references app_user(id),
  month date not null,
  category text check (category in ('GROCERY','FOOD','ONLINE','OTHER','TOTAL')) not null,
  limit_aed numeric(12,2) not null,
  unique(user_id, month, category)
);

create table if not exists notification_log(
  id uuid primary key default gen_random_uuid(),
  user_id uuid references app_user(id),
  kind text check (kind in ('WHATSAPP','EMAIL')) not null,
  template text,
  sent_at timestamptz default now(),
  payload jsonb
);
