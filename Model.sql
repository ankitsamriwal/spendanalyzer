
create or replace view v_daily_mtd as
select date_trunc('day', ordered_at) as day, category, sum(amount_aed) as amount
from txn where ordered_at >= date_trunc('month', now())
group by 1,2 order by 1,2;

create or replace view v_mtd_by_category as
select category, sum(amount_aed) as amount
from txn where ordered_at >= date_trunc('month', now())
group by category;

create or replace view v_budget_progress as
select b.category, b.limit_aed, coalesce(t.amount,0) as spent, (b.limit_aed - coalesce(t.amount,0)) as remaining
from budget b
left join (
  select category, sum(amount_aed) as amount
  from txn
  where ordered_at >= date_trunc('month', now())
  group by category
) t using (category)
where b.month = date_trunc('month', now())::date;
