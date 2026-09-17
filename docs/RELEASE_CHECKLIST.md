# Release checklist стартового репозитория

Этот checklist относится к **репозиторию организатора `test_oil`**, а не к конкурсному решению команды. Его цель — не допустить публикацию противоречивых исходных данных, скрытого готового решения или документации, которая расходится с контрольными правилами.

## 1. Source-of-truth

- [ ] `data/demand.csv` сверён с таблицей спроса в постановке.
- [ ] Пять supply channels сверены по capacity, variable cost, reservation rate, take-or-pay, lead time и reliability.
- [ ] Emergency хранится как `6 week`, без неявного перевода в `1.5 month`.
- [ ] Storage и investment options сверены с постановкой.
- [ ] Earth-New отражён как `90 + 270 = 360`, без дополнительного третьего CAPEX.
- [ ] Service constraints 99% critical / 97% total находятся только там, где они заданы постановкой.
- [ ] CAPEX limits 1800 до конца 2037 и 2800 до 2040 не изменены.
- [ ] 45-day reserve описан как физический stock или доказуемо equivalent emergency reserve.
- [ ] Отсутствие `Анкета_постановщика_КосмоХакатон_ЕТ.xlsx` явно отражено в provenance.

## 2. Mandatory stress

- [ ] Total и critical base demand получают `1.15` только в 2038–2040.
- [ ] Earth-Core и Earth-Flex variable prices получают `1.25` только в 2038–2039.
- [ ] В 2040 Earth-Core/Earth-Flex возвращаются к base variable price.
- [ ] Lunar-ISRU actual delivery = 55% plan в 2038, 75% в 2039, plan в 2040.
- [ ] 55%/75% не умножаются на reliability повторно.
- [ ] Stress loss ceiling `losses / throughput <= 0.02` действует с 2038.
- [ ] Mandatory stress не объединён автоматически с high demand или geopolitical scenario.

## 3. Anti-solution audit

- [ ] В repository нет `app.py` с готовым dashboard.
- [ ] В repository нет `src/` с готовым participant calculation engine.
- [ ] Нет готового optimizer, recommended supply mix или investment schedule.
- [ ] Нет заполненного конкурсного plan на реальных case inputs.
- [ ] Synthetic examples явно помечены как synthetic.
- [ ] README не говорит, что Lunar-ISRU, Earth-New или другой канал «нужно выбрать».
- [ ] MCDA weights не заданы организатором.
- [ ] Team assumptions не маскируются под organizer facts.

## 4. Machine-readable artifacts

- [ ] Все CSV читаются стандартным parser.
- [ ] Все JSON валидны синтаксически.
- [ ] Все JSON Schemas соответствуют Draft 2020-12.
- [ ] `examples/empty_plan.json` проходит `plan.schema.json`.
- [ ] Все YAML сценариев читаются `safe_load`.
- [ ] `validation/expected_checks.json` содержит V01–V10.
- [ ] Relative Markdown links ведут к существующим файлам.

## 5. Scientific traceability

- [ ] Organizer materials отделены от independent literature.
- [ ] Для каждого method/source есть связь `source -> supported proposition -> use -> limitation`.
- [ ] NASA-STD-7009B используется как guidance по credibility/verification, а не как источник case prices.
- [ ] Cryogenic papers не используются для объявления model loss rate 1.2% реальным universal ZBO value.
- [ ] Sommariva et al. не используется как доказательство, что Lunar-ISRU обязательно является лучшим вариантом в кейсе.
- [ ] Monte Carlo не интерпретируется как доказательство реальной probability без обоснованных distributions/dependencies.
- [ ] ISCPT presentation, NTRS record и AIAA publication не смешаны в одну библиографическую запись.

## 6. Documentation quality

- [ ] README можно понять без устного пояснения организатора по базовой математике.
- [ ] Every unavoidable term (take-or-pay, reservation, throughput, ISRU, ZBO) определён или связан с определением.
- [ ] Формулы в README и `CALCULATION_RULES.md` совпадают.
- [ ] `BASE` и `MANDATORY_STRESS` описаны одинаково во всех документах.
- [ ] Типовые ошибки содержат double counting, negative inventory, reliability misuse и source-input mutation.
- [ ] Инструкция жюри описывает изменение решения, recalculation, invalid plan, stress, export, reopen и extension test.

## 7. Figures and diagrams

- [ ] Mermaid diagrams рендерятся на GitHub.
- [ ] Synthetic figures подписаны как `SYNTHETIC EXAMPLE — NOT A CASE SOLUTION`.
- [ ] Ни один synthetic plot не выглядит как опубликованный «правильный» supply plan 2035–2040.
- [ ] Графики иллюстрируют тип результата, а не дают конкурсную стратегию.

## 8. Security and repository hygiene

- [ ] Нет `.env`, private keys, API tokens, passwords или credentials.
- [ ] Нет платной внешней зависимости, необходимой просто для чтения starter kit.
- [ ] GitHub Actions выполняет только static validation starter repository.
- [ ] `python tools/validate_reference_repo.py` проходит локально.

## Команда финальной проверки

```bash
python -m pip install pyyaml jsonschema
python tools/validate_reference_repo.py
```

Release блокируется при любой ошибке validator. Если исходный XLSX появится позднее, сначала проводится reconciliation с `docs/ERRATA_AND_PROVENANCE.md`, затем повторяется полный checklist.
