# Amendment to Test Oil Reference Repository Implementation Plan

This amendment is part of the self-review of `2026-09-18-test-oil-implementation-plan.md` and overrides one representation detail in Task 2 / Task 4.

## Emergency lead time: preserve the source exactly

The organizer source states `Emergency lead time = 6 weeks`.

Do **not** convert this to `1.5 months` in machine-readable source data, because that would introduce a convention not stated by the organizer.

For `data/supply_sources.csv`, use the following lead-time fields instead of forcing every source into months:

```csv
source_id,name,capacity_t_per_year,variable_cost_mln_per_t,reservation_rate_mln_per_t_year_capacity,take_or_pay_share,lead_time_min_value,lead_time_max_value,lead_time_unit,reliability_profile,available_from_year,status,notes
A,Earth-Core,190,6.2,0.45,0.70,12,12,month,"constant:0.96",2035,CASE_INPUT,"long-term Earth-to-orbit channel"
B,Earth-Flex,110,8.9,0.15,0.00,4,4,month,"constant:0.985",2035,CASE_INPUT,"flexible Earth-to-orbit channel"
C,Earth-New,130,7.1,0.30,0.50,18,24,month,"first_operating_year:0.88;later:0.94",,CASE_INPUT,"capacity available only after option exercise and preparation"
D,Lunar-ISRU,120,3.0,0.00,0.00,1,2,month,"2038:0.78;2039:0.90;2040:0.93",2038,CASE_INPUT,"available after required CAPEX financing and commissioning"
E,Emergency,80,13.8,0.35,0.00,6,6,week,"constant:0.995",2035,CASE_INPUT,"authoritative organizer lead time is six weeks"
```

Update `schemas/supply_sources.schema.json` and `docs/DATA_DICTIONARY.md` to use:

- `lead_time_min_value`: non-negative number;
- `lead_time_max_value`: number greater than or equal to the minimum;
- `lead_time_unit`: enum `day`, `week`, `month`, `year`.

No participant implementation should be forced to convert these durations until its own time model requires conversion. When conversion is necessary, the implementation must disclose its convention.

All other parts of the implementation plan remain unchanged.
