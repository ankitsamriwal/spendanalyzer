
-- Set your email below, then run this file after schema.sql
insert into app_user(email) values ('you@example.com')
on conflict (email) do nothing;

-- Optional baseline budgets (edit amounts)
insert into budget(user_id, month, category, limit_aed)
select id, date_trunc('month', now())::date, cat, amt
from app_user, (values
  ('GROCERY', 2000.00),
  ('FOOD', 1500.00),
  ('ONLINE', 1000.00),
  ('OTHER', 500.00),
  ('TOTAL', 5000.00)
) as b(cat, amt)
on conflict (user_id, month, category) do nothing;
