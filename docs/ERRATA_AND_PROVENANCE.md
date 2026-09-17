# Происхождение данных, расхождения и границы исходного набора

Этот файл фиксирует, откуда перенесено каждое обязательное числовое условие стартового репозитория. Если исходные материалы расходятся или нужный файл отсутствует, репозиторий не подменяет это догадкой.

## Правила переноса

1. `CASE_INPUT` переносится без скрытого исправления смысла.
2. Если значение задано диапазоном, диапазон сохраняется.
3. Если одна и та же величина описана в нескольких материалах, фиксируются все источники и выбранная трактовка.
4. Если первичный файл отсутствует, это отмечается явно.
5. Научная публикация не заменяет синтетические цены, мощности и лимиты организатора.

## Источники текущей сборки

Основные значения перенесены из `Кейс_2_Топливный_космоконтур_2035.docx` и сверены с `Пояснительная_записка_для_жюри_Кейс_2_КЭП.docx` и `Критерии_оценки_Кейс_2_КЭП_upd.xlsx.docx`.

Постановка ссылается на `Анкета_постановщика_КосмоХакатон_ЕТ.xlsx`, лист `Данные кейса 2`, однако этот XLSX не присутствует в наборе материалов, использованном для создания `test_oil`. Поэтому машинно-читаемые значения репозитория должны быть повторно сверены с XLSX, если организатор предоставит его позднее. Отсутствующее содержимое не восстанавливается догадками.

## Контрольные значения

| parameter_id | value | unit | status | organizer_source | interpretation_note | unresolved_issue |
|---|---:|---|---|---|---|---|
| demand_2035_total | 100 | t/year | CASE_INPUT | case DOCX | critical included in total | source XLSX absent |
| demand_2035_critical | 80 | t/year | CASE_INPUT | case DOCX | subset of total | source XLSX absent |
| demand_2035_low | 80 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2035_high | 110 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2036_total | 140 | t/year | CASE_INPUT | case DOCX | critical included in total | source XLSX absent |
| demand_2036_critical | 105 | t/year | CASE_INPUT | case DOCX | subset of total | source XLSX absent |
| demand_2036_low | 112 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2036_high | 154 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2037_total | 190 | t/year | CASE_INPUT | case DOCX | critical included in total | source XLSX absent |
| demand_2037_critical | 135 | t/year | CASE_INPUT | case DOCX | subset of total | source XLSX absent |
| demand_2037_low | 152 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2037_high | 209 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2038_total | 250 | t/year | CASE_INPUT | case DOCX | critical included in total | source XLSX absent |
| demand_2038_critical | 170 | t/year | CASE_INPUT | case DOCX | subset of total | source XLSX absent |
| demand_2038_low | 200 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2038_high | 312.5 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2039_total | 320 | t/year | CASE_INPUT | case DOCX | critical included in total | source XLSX absent |
| demand_2039_critical | 210 | t/year | CASE_INPUT | case DOCX | subset of total | source XLSX absent |
| demand_2039_low | 256 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2039_high | 400 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2040_total | 390 | t/year | CASE_INPUT | case DOCX | critical included in total | source XLSX absent |
| demand_2040_critical | 250 | t/year | CASE_INPUT | case DOCX | subset of total | source XLSX absent |
| demand_2040_low | 312 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| demand_2040_high | 487.5 | t/year | CASE_INPUT | case DOCX | sensitivity input | source XLSX absent |
| earth_core_capacity | 190 | t/year | CASE_INPUT | case DOCX | max channel capacity | source XLSX absent |
| earth_core_variable_cost | 6.2 | mln units/t | CASE_INPUT | case DOCX | includes delivery to hub in aggregate model | source XLSX absent |
| earth_core_reservation | 0.45 | mln units per t/year capacity | CASE_INPUT | case DOCX | annual reservation rate | source XLSX absent |
| earth_core_top | 0.70 | share | CASE_INPUT | case DOCX | take-or-pay share | source XLSX absent |
| earth_core_lead | 12 | months | CASE_INPUT | case DOCX | exact source wording | source XLSX absent |
| earth_core_reliability | 0.96 | index | CASE_INPUT | case DOCX | risk input, not BASE multiplier | source XLSX absent |
| earth_flex_capacity | 110 | t/year | CASE_INPUT | case DOCX | max channel capacity | source XLSX absent |
| earth_flex_variable_cost | 8.9 | mln units/t | CASE_INPUT | case DOCX | aggregate delivered price | source XLSX absent |
| earth_flex_reservation | 0.15 | mln units per t/year capacity | CASE_INPUT | case DOCX | annual reservation rate | source XLSX absent |
| earth_flex_top | 0 | share | CASE_INPUT | case DOCX | no TOP minimum | source XLSX absent |
| earth_flex_lead | 4 | months | CASE_INPUT | case DOCX | exact source wording | source XLSX absent |
| earth_flex_reliability | 0.985 | index | CASE_INPUT | case DOCX | risk input | source XLSX absent |
| earth_new_capacity | 130 | t/year | CASE_INPUT | case DOCX | after exercise/preparation | source XLSX absent |
| earth_new_variable_cost | 7.1 | mln units/t | CASE_INPUT | case DOCX | aggregate delivered price | source XLSX absent |
| earth_new_reservation | 0.30 | mln units per t/year capacity | CASE_INPUT | case DOCX | annual reservation rate | source XLSX absent |
| earth_new_top | 0.50 | share | CASE_INPUT | case DOCX | after startup | source XLSX absent |
| earth_new_lead | 18–24 | months | CASE_INPUT | case DOCX | preserve range | source XLSX absent |
| earth_new_reliability | 0.88 first year; 0.94 later | index | CASE_INPUT | case DOCX | risk input | source XLSX absent |
| lunar_isru_capacity | 120 | t/year | CASE_INPUT | case DOCX | after required CAPEX | source XLSX absent |
| lunar_isru_variable_cost | 3.0 | mln units/t | CASE_INPUT | case DOCX | aggregate delivered price | source XLSX absent |
| lunar_isru_reservation | 0 | mln units per t/year capacity | CASE_INPUT | case DOCX | no reservation charge | source XLSX absent |
| lunar_isru_top | 0 | share | CASE_INPUT | case DOCX | no TOP | source XLSX absent |
| lunar_isru_lead | 1–2 | months | CASE_INPUT | case DOCX | after commissioning | source XLSX absent |
| lunar_isru_reliability | 0.78 / 0.90 / 0.93 | index | CASE_INPUT | case DOCX | 2038 / 2039 / 2040 | source XLSX absent |
| emergency_capacity | 80 | t/year | CASE_INPUT | case DOCX | emergency/spot maximum | source XLSX absent |
| emergency_variable_cost | 13.8 | mln units/t | CASE_INPUT | case DOCX | aggregate delivered price | source XLSX absent |
| emergency_reservation | 0.35 | mln units per t/year capacity | CASE_INPUT | case DOCX | capacity-reserve contract | source XLSX absent |
| emergency_lead | 6 | weeks | CASE_INPUT | case DOCX | preserve weeks exactly | source XLSX absent |
| emergency_reliability | 0.995 | index | CASE_INPUT | case DOCX | risk input | source XLSX absent |
| base_storage_capacity | 70 | t | CASE_INPUT | case DOCX | existing storage | source XLSX absent |
| base_storage_loss | 0.045 | share of throughput | CASE_INPUT | case DOCX | applied to gross inflow | source XLSX absent |
| holding_cost | 0.72 | mln units/t-year | CASE_INPUT | case DOCX | average physical inventory | source XLSX absent |
| zbo_capex | 180 | mln units | CASE_INPUT | case DOCX | option from 2036 | source XLSX absent |
| zbo_capacity | 120 | t | CASE_INPUT | case DOCX | capacity after modernization | source XLSX absent |
| zbo_loss | 0.012 | share of throughput | CASE_INPUT | case DOCX | model coefficient, not universal tech fact | source XLSX absent |
| zbo_opex | 12 | mln units/year | CASE_INPUT | case DOCX | additional OPEX | source XLSX absent |
| lunar_isru_capex | 1250 | mln units | CASE_INPUT | case DOCX | finance before 2038 | source XLSX absent |
| lunar_isru_fixed_opex | 70 | mln units/year | CASE_INPUT | case DOCX | after commissioning | source XLSX absent |
| earth_new_option_fee | 90 | mln units | CASE_INPUT | case DOCX | right to introduce capacity | source XLSX absent |
| earth_new_exercise | 270 | mln units | CASE_INPUT | case DOCX | paid on exercise | source XLSX absent |
| earth_new_total | 360 | mln units | CASE_INPUT | case DOCX + jury note | total is 90+270, not an extra payment | source XLSX absent |
| base_critical_service | 0.99 | share | CASE_INPUT | case DOCX | annual BASE minimum | source XLSX absent |
| base_total_service | 0.97 | share | CASE_INPUT | case DOCX | annual BASE minimum | source XLSX absent |
| capex_through_2037 | 1800 | mln units | CASE_INPUT | case DOCX | upper bound | source XLSX absent |
| capex_through_2040 | 2800 | mln units | CASE_INPUT | case DOCX | cumulative upper bound | source XLSX absent |
| reserve_days | 45 | days | CASE_INPUT | case DOCX | physical or demonstrated contracted equivalent | source XLSX absent |
| emergency_base_streak | 2 | consecutive years max | CASE_INPUT | case DOCX | Emergency cannot be base beyond this streak | source XLSX absent |

## Mandatory stress provenance

| Parameter | 2035–2037 | 2038 | 2039 | 2040 |
|---|---:|---:|---:|---:|
| total base demand multiplier | 1.00 | 1.15 | 1.15 | 1.15 |
| critical base demand multiplier | 1.00 | 1.15 | 1.15 | 1.15 |
| Earth-Core variable-price multiplier | 1.00 | 1.25 | 1.25 | 1.00 |
| Earth-Flex variable-price multiplier | 1.00 | 1.25 | 1.25 | 1.00 |
| Lunar-ISRU actual-delivery share | plan | 0.55 | 0.75 | 1.00 |
| stress loss ceiling | n/a | 0.02 | 0.02 | 0.02 |

The 0.55 and 0.75 values are actual delivery shares for the mandatory stress and are **not** multiplied by reliability again. Reservation tariffs, CAPEX and unrelated prices are not changed by the mandatory +25% price shock. The mandatory stress is not automatically combined with high demand or an optional geopolitical scenario.

## Known source limitations

- The source XLSX referenced in the case is absent from the current material set.
- `Emergency lead time` remains six weeks. No hidden conversion to 1.5 months is stored as an organizer fact.
- `ZBO 1.2%` is a synthetic case coefficient, not a universal technology claim.
- No external paper is used to replace organizer prices/capacities.
- Post-2040 values are not organizer forecasts unless separately supplied.
