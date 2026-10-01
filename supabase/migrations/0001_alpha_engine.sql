-- Alpha Engine paper-trading persistence. Server-side access only (service role).
create table if not exists ae_state (
  id int primary key default 1 check (id = 1),
  cash double precision not null,
  realized_pnl double precision not null default 0,
  positions jsonb not null default '[]'::jsonb,
  killed boolean not null default false,
  day_start_equity double precision not null,
  day date not null default current_date,
  updated_at timestamptz not null default now()
);
create table if not exists ae_cycles (
  id bigint generated always as identity primary key,
  ts timestamptz not null default now(),
  scanned int not null,
  approved int not null,
  equity double precision not null
);
create table if not exists ae_decisions (
  id bigint generated always as identity primary key,
  cycle_id bigint references ae_cycles(id) on delete cascade,
  market_id text not null,
  question text,
  side text not null,
  price double precision not null,
  prob double precision not null,
  edge double precision not null,
  stake double precision not null,
  approved boolean not null,
  reason text
);
alter table ae_state enable row level security;
alter table ae_cycles enable row level security;
alter table ae_decisions enable row level security;
-- No policies: anon/authenticated roles have no access; the service role bypasses RLS.
