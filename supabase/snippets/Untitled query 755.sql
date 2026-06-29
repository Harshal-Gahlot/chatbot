grant all on public.chats_history to anon;
grant all on public.chats_history to authenticated;

alter table public.chats_history enable row level security;

create policy "Allow all inserts" on public.chats_history for insert to anon with check (true);
create policy "Allow all reads" on public.chats_history for select to anon using (true);