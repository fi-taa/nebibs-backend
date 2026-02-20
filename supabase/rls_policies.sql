-- Run once in Supabase: SQL Editor → New query → paste → Run
-- Allows the anon key (used by the backend) to read and write all rows.
-- When you add auth later, replace these with user_id-scoped policies.

create policy "Allow anon all on learning_goals"
  on learning_goals for all to anon
  using (true) with check (true);

create policy "Allow anon all on experiments"
  on experiments for all to anon
  using (true) with check (true);

create policy "Allow anon all on service_entries"
  on service_entries for all to anon
  using (true) with check (true);
