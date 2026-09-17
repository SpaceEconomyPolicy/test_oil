from __future__ import annotations
from pathlib import Path
import sys
import pandas as pd
import plotly.express as px
import streamlit as st
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'src'))
from fuel_contour.io import load_case,load_plan,load_investments,load_reserve_evidence
from fuel_contour.model import SimulationInputs,simulate_plan
from fuel_contour.export import result_to_excel,project_bundle_json,load_project_bundle_json
from fuel_contour.risk import monte_carlo_channel_availability

st.set_page_config(page_title='Топливный космоконтур 2035',layout='wide')
st.title('Топливный космоконтур 2035')
st.caption('Интерактивный учебный контур: снабжение, запасы, контракты, CAPEX/OPEX, стресс и риски. В репозитории нет единственного «правильного» плана.')

def defaults():
    d,s,c=load_case(ROOT); p=load_plan(ROOT/'data/blank_plan.csv'); i=load_investments(ROOT/'data/investment_schedule_blank.csv'); r=load_reserve_evidence(ROOT/'data/reserve_evidence_blank.csv'); return d,s,c,p,i,r
if 'boot' not in st.session_state:
    d,s,c,p,i,r=defaults(); st.session_state.update(boot=True,demand=d,sources=s,config=c,plan=p,investments=i,reserve=r)

with st.sidebar:
    st.header('Расчёт')
    scenario=st.selectbox('Сценарий',['standard','mandatory_stress','low_demand','high_demand'],format_func=lambda x:{'standard':'Стандарт','mandatory_stress':'Обязательный стресс','low_demand':'Низкий спрос','high_demand':'Высокий спрос'}[x])
    rate=st.number_input('Реальная ставка дисконтирования',0.0,1.0,0.05,0.01)
    init=st.number_input('Начальный запас, т',0.0,500.0,0.0,1.0)
    init_src=st.text_input('Источник начального запаса','')
    init_cost=st.number_input('Стоимость начального запаса, млн у.е.',0.0,5000.0,0.0,10.0)
    lead=st.slider('Earth-New lead time, дней',548,730,730)
    if st.button('Сбросить исходные данные'):
        d,s,c,p,i,r=defaults(); st.session_state.update(demand=d,sources=s,config=c,plan=p,investments=i,reserve=r); st.rerun()
    uploaded=st.file_uploader('Открыть сохранённый проект JSON',type=['json'])
    if uploaded:
        try:
            p,i,r,d,s,settings=load_project_bundle_json(uploaded.getvalue().decode('utf-8')); st.session_state.update(plan=p,investments=i,reserve=r,demand=d,sources=s); st.success('Проект загружен')
        except Exception as e: st.error(str(e))

t1,t2,t3,t4,t5=st.tabs(['План','Инвестиции и резерв','Результат','Сценарии и риски','Методика'])
with t1:
    st.subheader('План поставок и контракты')
    st.write('Редактируйте объёмы без правки кода. Для используемых A/B укажите `order_date`; `first_delivery_month` задаёт первый месяц фактической поставки.')
    st.session_state.plan=st.data_editor(st.session_state.plan,num_rows='dynamic',use_container_width=True,key='plan_editor')
    st.subheader('Источники снабжения')
    st.session_state.sources=st.data_editor(st.session_state.sources,num_rows='dynamic',use_container_width=True,key='source_editor')
    st.info('Добавленный источник учитывает `available_from`. Для исследовательского горизонта добавьте новый год в data/config при локальном запуске; ядро это поддерживает и тестирует.')
with t2:
    c1,c2=st.columns(2)
    with c1:
        st.subheader('График инвестиций')
        st.session_state.investments=st.data_editor(st.session_state.investments,use_container_width=True,key='inv_editor')
    with c2:
        st.subheader('Доказательство 45-дневного резерва')
        st.session_state.reserve=st.data_editor(st.session_state.reserve,use_container_width=True,key='reserve_editor')
    st.caption('Физический запас проверяется на начало года. Контрактный Emergency засчитывается только с bridge coverage на 42 дня до активации.')

def calc(sc):
    return simulate_plan(st.session_state.demand,st.session_state.sources,st.session_state.config,st.session_state.plan,st.session_state.investments,st.session_state.reserve,SimulationInputs(sc,float(rate),float(init),init_src,float(init_cost),int(lead)))
try: result=calc(scenario)
except Exception as e:
    result=None; st.error(f'Ошибка входных данных: {e}')
with t3:
    if result is not None:
        m=result.metrics
        a,b,c,d=st.columns(4); a.metric('Обслужено, т',f"{m['total_served_t']:.1f}"); b.metric('Дефицит, т',f"{m['total_shortage_t']:.1f}"); c.metric('PV затрат, млн у.е.',f"{m['present_cost_m']:.1f}"); d.metric('Жёсткие ограничения','OK' if m['hard_constraints_ok'] else 'НАРУШЕНЫ')
        st.plotly_chart(px.line(result.annual,x='year',y=['total_demand_t','total_served_t','total_shortage_t'],markers=True,title='Спрос, обслуживание и дефицит'),use_container_width=True)
        st.plotly_chart(px.bar(result.source_costs,x='year',y='actual_gross_delivery_t',color='source_id',barmode='stack',title='Фактические поставки по каналам'),use_container_width=True)
        st.plotly_chart(px.line(result.annual,x='year',y=['total_service_level','critical_service_level'],markers=True,title='Уровни обслуживания'),use_container_width=True)
        st.subheader('Годовой баланс'); st.dataframe(result.annual,use_container_width=True)
        st.subheader('Проверка ограничений'); st.dataframe(result.constraints,use_container_width=True)
        st.subheader('Экономика каналов'); st.dataframe(result.source_costs,use_container_width=True)
        if result.warnings:
            for w in result.warnings: st.warning(w)
        settings={'scenario':scenario,'rate':rate,'initial_inventory_t':init,'initial_inventory_source':init_src,'initial_inventory_cost_m':init_cost,'earth_new_lead_days':lead}
        js=project_bundle_json(st.session_state.plan,st.session_state.investments,st.session_state.reserve,st.session_state.demand,st.session_state.sources,settings)
        xlsx=result_to_excel(result,st.session_state.plan,st.session_state.investments,settings,st.session_state.demand,st.session_state.sources,st.session_state.reserve)
        e1,e2=st.columns(2); e1.download_button('Сохранить проект JSON',js,'fuel_contour_project.json','application/json'); e2.download_button('Выгрузить расчёт XLSX',xlsx,'fuel_contour_results.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
with t4:
    if result is not None:
        st.subheader('Сравнение стандартного и обязательного стресса')
        base=calc('standard'); stress=calc('mandatory_stress')
        cmp=base.annual[['year','total_service_level','critical_service_level','nominal_cost_m','total_shortage_t']].merge(stress.annual[['year','total_service_level','critical_service_level','nominal_cost_m','total_shortage_t']],on='year',suffixes=('_standard','_stress'))
        st.dataframe(cmp,use_container_width=True)
        st.plotly_chart(px.line(cmp,x='year',y=['total_shortage_t_standard','total_shortage_t_stress'],markers=True,title='Дефицит: стандарт и стресс'),use_container_width=True)
        st.subheader('Дополнительный риск-экран Monte Carlo')
        n=st.slider('Число испытаний',200,10000,1000,200); seed=st.number_input('Seed',0,999999,2035); common=st.slider('Условная вероятность общего отказа земных каналов',0.0,0.5,0.0,0.01)
        if st.button('Запустить риск-экран'):
            mc=monte_carlo_channel_availability(result,st.session_state.sources,n_trials=n,seed=int(seed),common_earth_outage_probability=common); st.dataframe(mc.summary,use_container_width=True); st.caption(mc.assumptions['warning'])
with t5:
    st.markdown('''### Что считается
- контрольный год: 365 дней;
- критический спрос входит в общий и обслуживается первым;
- стандартный сценарий детерминированный, коэффициенты надёжности не умножают поставку;
- mandatory stress: +15% спрос в 2038–2040, +25% цены A/B в 2038–2039, ISRU 55%/75%/100%;
- потери: коэффициент от валового поступления один раз;
- take-or-pay: `max(отбор, доля × резерв периода)`;
- резерв: физический 45 дней или Emergency + bridge coverage;
- CAPEX Earth-New: 90 + 270, без двойного счёта.

Подробности и научные источники: `docs/methodology.md`, `docs/scientific_basis.md`, `docs/source_audit.md`.''')
