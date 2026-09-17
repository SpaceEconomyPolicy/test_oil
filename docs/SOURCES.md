# Источники

Материалы постановщика отделены от независимой научной/методической литературы. Синтетические параметры кейса должны ссылаться на первую группу, а не на внешние статьи.

## A. Материалы постановщика

1. `Кейс_2_Топливный_космоконтур_2035.docx` — основная постановка, данные, контрольные правила, требования к результатам.
2. `Критерии_оценки_Кейс_2_КЭП_upd.xlsx.docx` — шкала 100 + до 5 бонусных баллов и предмет проверки критериев.
3. `Пояснительная_записка_для_жюри_Кейс_2_КЭП.docx` — трактовка контрольного расчёта, mandatory stress, воспроизводимость и границы экспертной проверки.
4. `52 признака AI-текста на русском_ полный список.pdf` — редакторский чек-лист для языка; не является научным источником по экономике/логистике.
5. `humanizer-ru` — дополнительный living editorial catalog, используется только для редактуры естественного русского текста: https://github.com/ilyautov/humanizer-ru

### Отсутствующий первичный источник данных

Постановка ссылается на `Анкета_постановщика_КосмоХакатон_ЕТ.xlsx`, лист `Данные кейса 2`. Этот файл не был предоставлен в комплекте, из которого создана текущая версия starter repository. См. `ERRATA_AND_PROVENANCE.md`.

## B. Официальные и научные источники

### NASA model credibility

NASA. **NASA-STD-7009B — Standard for Models and Simulations**. Version B, document date 2024-03-05.  
Official page: https://standards.nasa.gov/standard/nasa/nasa-std-7009

NASA. **NASA-HDBK-7009B — NASA Handbook for Models and Simulations: An Implementation Guide for NASA-STD-7009B**. Version B, document date 2026-02-03.  
Official page: https://standards.nasa.gov/standard/NASA/NASA-HDBK-7009

### Space logistics

Ho, K. (2024). **Space Logistics Modeling and Optimization: Review of the State of the Art**. *Journal of Spacecraft and Rockets*, 61(5).  
DOI: https://doi.org/10.2514/1.A35982

### Cryogenic propellant management

Simonini, A., Dreyer, M., Urbano, A., Sanfedino, F., Himeno, T., Behruzi, P., Avila, M., Pinho, J., Peveroni, L., & Gouriet, J.-B. (2024). **Cryogenic propellant management in space: open challenges and perspectives**. *npj Microgravity*, 10, 34.  
DOI: https://doi.org/10.1038/s41526-024-00377-5

### Lunar propellant / orbital depot economics

Sommariva, A., Gaudenzi, P., Pianorsi, M., Pasquali, M., Vittori, E., Eugeni, M., Italiano, M., Telli, C., Di Nicola, M., Gori, L., & Chizzolini, B. (2023). **Preliminary analyses on technical and economic viability of moon-mined propellant for on-orbit refueling**. *Acta Astronautica*, 204, 425–433.  
DOI: https://doi.org/10.1016/j.actaastro.2023.01.004

### Robust optimization

Bertsimas, D., & Sim, M. (2004). **The Price of Robustness**. *Operations Research*, 52(1), 35–53.  
DOI: https://doi.org/10.1287/opre.1030.0065

### MCDA and adaptive management

Linkov, I., Satterstrom, F. K., Kiker, G., Batchelor, C., Bridges, T., & Ferguson, E. (2006). **From comparative risk assessment to multi-criteria decision analysis and adaptive management: Recent developments and applications**. *Environment International*, 32(8), 1072–1093.  
DOI: https://doi.org/10.1016/j.envint.2006.06.013

### Monte Carlo uncertainty guidance

Joint Committee for Guides in Metrology (JCGM). (2008). **JCGM 101:2008 — Evaluation of measurement data — Supplement 1 to the Guide to the expression of uncertainty in measurement — Propagation of distributions using a Monte Carlo method**.  
Official BIPM/DOI page: https://www.bipm.org/en/doi/10.59161/jcgm101-2008  
DOI: https://doi.org/10.59161/JCGM101-2008

Это метрологическое руководство приводится как методический ориентир по propagation of distributions; его перенос на экономические/логистические риски требует отдельного обоснования.

### Dual sourcing and supply resilience

Han, B., Zhang, Y., Wang, S., & Park, Y. (2023). **The efficient and stable planning for interrupted supply chain with dual-sourcing strategy: a robust optimization approach considering decision maker's risk attitude**. *Omega*, 115, 102775.  
DOI: https://doi.org/10.1016/j.omega.2022.102775

Guo, Y., Liu, F., Song, J.-S., & Wang, S. (2025). **Supply chain resilience: A review from the inventory management perspective**. *Fundamental Research*, 5(2), 450–463.  
DOI: https://doi.org/10.1016/j.fmre.2024.08.002

### In-space cryogenic propellant transfer

Perrin, T. M. (2025). **Guidelines for In-Space Cryogenic Propellant Transfer (ISCPT)**. Presentation, 31st Space Cryogenic Workshop. NASA Technical Reports Server, Document ID 20250003540.  
NTRS: https://ntrs.nasa.gov/citations/20250003540

Kenny, R. J., Eddleman, D. E., Keplinger, J. D., Stephens, J. R., Hartwig, J. W., & Perrin, T. M. (2025). **Guidelines for In-Space Cryogenic Propellant Transfer**. AIAA AVIATION FORUM and ASCEND 2025.  
DOI: https://doi.org/10.2514/6.2025-4122  
NASA NTRS record cited by the case setter: https://ntrs.nasa.gov/citations/20250004625

## Правило использования списка

Наличие статьи в этом файле не означает, что её числа можно переносить в `CASE_INPUT`. Связь каждого источника с framework и границы применимости описаны в `SCIENTIFIC_BASIS.md`.
