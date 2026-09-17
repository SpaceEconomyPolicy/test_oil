from __future__ import annotations
import math
from dataclasses import dataclass
from typing import Any
import numpy as np
import pandas as pd
from .scenarios import demand_for_scenario, delivery_factor, scenario_metadata, variable_price

@dataclass(frozen=True)
class SimulationInputs:
    scenario:str='standard'; real_discount_rate:float=.05; initial_inventory_t:float=0.; initial_inventory_source:str=''; initial_inventory_cost_m:float=0.; earth_new_lead_days:int=730; research_variable_price_multipliers:dict[str,dict[str,float]]|None=None
@dataclass
class SimulationResult:
    annual:pd.DataFrame; monthly:pd.DataFrame; source_costs:pd.DataFrame; constraints:pd.DataFrame; investment_status:dict[str,Any]; metrics:dict[str,Any]; warnings:list[str]
    @property
    def feasible_hard_constraints(self):
        h=self.constraints[self.constraints.severity.eq('hard')] if not self.constraints.empty else self.constraints
        return bool(h.ok.all()) if not h.empty else True

def derive_investment_status(inv, cfg, lead):
    x=inv.copy().sort_values('year')
    cols=['zbo_capex_m','isru_capex_m','earth_new_option_fee_m','earth_new_exercise_capex_m']
    for c in cols:x[c]=pd.to_numeric(x[c],errors='coerce').fillna(0.).astype(float)
    def first(c,need,lo=-10**9):
        s=0
        for y,v in zip(x.year.astype(int),x[c]):
            s+=v
            if y>=lo and s+1e-9>=need:return int(y)
    zreq=float(cfg['storage']['upgrade']['capex_m']); zy=first('zbo_capex_m',zreq,int(cfg['storage']['upgrade']['available_from']))
    ireq=float(cfg['investments']['lunar_isru']['capex_m']); dead=int(cfg['investments']['lunar_isru']['funded_by_year_end']); iby=float(x.loc[x.year.astype(int)<=dead,'isru_capex_m'].sum()); ifund=iby+1e-9>=ireq
    ecfg=cfg['investments']['earth_new']; oy=first('earth_new_option_fee_m',float(ecfg['option_fee_m'])); ey=first('earth_new_exercise_capex_m',float(ecfg['exercise_capex_m'])); active=ey+math.ceil(lead/365) if oy is not None and ey is not None and oy<=ey else None
    return {'zbo_total_capex_m':float(x.zbo_capex_m.sum()),'zbo_active_year':zy,'isru_total_capex_m':float(x.isru_capex_m.sum()),'isru_funded_by_2037_m':iby,'isru_funded':ifund,'isru_active_year':int(cfg['investments']['lunar_isru']['available_from']) if ifund else None,'earth_new_option_fee_total_m':float(x.earth_new_option_fee_m.sum()),'earth_new_exercise_capex_total_m':float(x.earth_new_exercise_capex_m.sum()),'earth_new_option_year':oy,'earth_new_exercise_year':ey,'earth_new_active_year':active,'earth_new_lead_days_assumption':int(lead)}

def _days():return [31,28,31,30,31,30,31,31,30,31,30,31]
def _period(month):
    d=_days(); return sum(d[month-1:])/365.,sum(d[month-1:])
def _avail(sid,y,st,row):
    if sid=='C':return st['earth_new_active_year'] is not None and y>=st['earth_new_active_year']
    if sid=='D':return st['isru_active_year'] is not None and y>=st['isru_active_year']
    return y>=int(float(row.get('available_from',y)))
def _storage(y,st,cfg):
    if st['zbo_active_year'] is not None and y>=st['zbo_active_year']:
        u=cfg['storage']['upgrade']; return 'CFM/ZBO-like upgrade',float(u['capacity_t']),float(u['loss_rate_on_gross_inbound']),float(u['fixed_opex_m_per_year'])
    b=cfg['storage']; return 'base storage',float(b['base_capacity_t']),float(b['base_loss_rate_on_gross_inbound']),0.
def _crow(name,y,ok,actual,limit,severity,reason):return {'constraint':name,'year':y,'ok':bool(ok),'actual':actual,'limit':limit,'severity':severity,'reason':reason}

def simulate_plan(demand,sources,config,plan,investments,reserve_evidence=None,inputs=None):
    inputs=inputs or SimulationInputs(real_discount_rate=float(config['default_assumptions']['real_discount_rate']))
    if not 0<=inputs.real_discount_rate<=1:raise ValueError('real_discount_rate must be between 0 and 1')
    if inputs.initial_inventory_t<0 or inputs.initial_inventory_cost_m<0:raise ValueError('Initial inventory and its cost cannot be negative')
    if inputs.initial_inventory_t>0 and (not inputs.initial_inventory_source.strip() or inputs.initial_inventory_cost_m<=0):raise ValueError('Initial inventory requires an explicit source and financing/cost')
    H=[int(y) for y in config['horizon']]; S=sources.copy(); S.source_id=S.source_id.astype(str); sidx=S.set_index('source_id',drop=False)
    p=plan.copy(); req={'year','source_id','reserved_capacity_tpy','planned_gross_delivery_t','role'}
    if req-set(p.columns):raise ValueError('Plan missing required columns')
    if 'first_delivery_month' not in p:p['first_delivery_month']=1
    if 'order_date' not in p:p['order_date']=''
    if p.duplicated(['year','source_id']).any():raise ValueError('Duplicate year/source rows in plan')
    p.year=p.year.astype(int); p.source_id=p.source_id.astype(str)
    for c in ['reserved_capacity_tpy','planned_gross_delivery_t']:p[c]=pd.to_numeric(p[c],errors='raise').astype(float)
    p.first_delivery_month=pd.to_numeric(p.first_delivery_month,errors='coerce').fillna(1).astype(int)
    if ((p.first_delivery_month<1)|(p.first_delivery_month>12)).any():raise ValueError('first_delivery_month must be an integer from 1 to 12')
    p.order_date=p.order_date.fillna('').astype(str).str.strip(); p.role=p.role.fillna('base').astype(str)
    idx=pd.MultiIndex.from_product([H,S.source_id],names=['year','source_id']); p=p.set_index(['year','source_id']).reindex(idx).reset_index()
    for c,v in [('reserved_capacity_tpy',0.),('planned_gross_delivery_t',0.),('first_delivery_month',1),('order_date',''),('role','base')]:p[c]=p[c].fillna(v)
    p.first_delivery_month=p.first_delivery_month.astype(int)
    inv=investments.copy(); inv.year=inv.year.astype(int)
    for c in [x for x in inv.columns if x!='year']:inv[c]=pd.to_numeric(inv[c],errors='coerce').fillna(0.).astype(float)
    st=derive_investment_status(inv,config,inputs.earth_new_lead_days); cons=[]; warn=[]; sc=[]
    for _,r in p.iterrows():
        y=int(r.year); sid=str(r.source_id); s=sidx.loc[sid]; res=float(r.reserved_capacity_tpy); q=float(r.planned_gross_delivery_t); m=int(r.first_delivery_month); frac,active_days=_period(m); cap=float(s.max_capacity_tpy)*frac
        if res<0 or q<0:raise ValueError('Plan quantities cannot be negative')
        if res>cap+1e-9:cons.append(_crow('capacity_reservation',y,False,res,cap,'hard',f'{sid}: reserved capacity exceeds active-period capacity'))
        if q>res+1e-9:cons.append(_crow('delivery_vs_reserved',y,False,q,res,'hard',f'{sid}: planned delivery exceeds reserved capacity'))
        available=_avail(sid,y,st,s)
        if (q>1e-9 or res>1e-9) and not available:cons.append(_crow('source_availability',y,False,sid,'available after investment/available_from','hard',f'{sid} is not available in {y}'))
        od=str(r.order_date).strip(); used=(q>1e-9 or res>1e-9)
        if used and sid in {'A','B'}:
            if not od:cons.append(_crow('lead_time',y,False,'missing order_date',int(s.lead_time_max_days),'hard',f'{sid}: order_date required'))
            else:
                first=pd.Timestamp(y,m,1); delta=(first-pd.Timestamp(od)).days
                if delta+1e-9<float(s.lead_time_max_days):cons.append(_crow('lead_time',y,False,delta,float(s.lead_time_max_days),'hard',f'{sid}: insufficient lead time'))
        price=variable_price(s,y,inputs.scenario,config)
        mul=(inputs.research_variable_price_multipliers or {}).get(sid,{}).get(str(y),1.0); price*=float(mul)
        actual=q*delivery_factor(sid,y,inputs.scenario,config) if available else 0.
        top=float(s.take_or_pay_share); paid=max(q,top*res*frac); reserv=float(s.reservation_fee_m_per_tpy)*res*frac
        sc.append({'year':y,'source_id':sid,'role':r.role,'reserved_capacity_tpy':res,'planned_gross_delivery_t':q,'actual_gross_delivery_t':actual,'first_delivery_month':m,'order_date':od,'contract_period_fraction':frac,'variable_price_m_per_t':price,'paid_quantity_t':paid,'variable_payment_m':price*paid,'reservation_payment_m':reserv,'source_cost_m':price*paid+reserv})
    source_costs=pd.DataFrame(sc)
    dsc=demand_for_scenario(demand,inputs.scenario,config).set_index('year'); inv2=inv.groupby('year').sum(numeric_only=True).reindex(H,fill_value=0.); inv2['capex_total_m']=inv2.sum(axis=1)
    reserve=(reserve_evidence.copy() if reserve_evidence is not None else pd.DataFrame({'year':H,'physical_start_inventory_target_t':0,'emergency_reserved_t':0,'bridge_coverage_t':0,'note':''})).set_index('year')
    monthly=[]; annual=[]; inventory=float(inputs.initial_inventory_t)
    for y in H:
        label,storage_cap,loss_rate,fixed=_storage(y,st,config); start=inventory; td=float(dsc.loc[y,'total_demand_t']); cd=float(dsc.loc[y,'critical_demand_t']); ys=source_costs[source_costs.year.eq(y)].set_index('source_id'); served=crit_served=loss=overflow=hold=0.; daylist=_days()
        for mo,days in enumerate(daylist,1):
            gross=0.
            for sid,row in ys.iterrows():
                if mo>=int(row.first_delivery_month):gross+=float(row.actual_gross_delivery_t)*days/sum(daylist[int(row.first_delivery_month)-1:])
            l=gross*loss_rate; loss+=l; before=inventory+gross-l; ov=max(before-storage_cap,0.); overflow+=ov; before=min(before,storage_cap); crit=cd*days/365.; total=td*days/365.; cs=min(before,crit); before-=cs; ns=min(before,max(total-crit,0.)); before-=ns; served+=cs+ns; crit_served+=cs; end=before; hold+=(inventory+end)/2*days/365.*float(config['storage']['holding_cost_m_per_t_year']); inventory=end
            monthly.append({'year':y,'month':mo,'days':days,'start_inventory_t':max(inventory-(gross-l-cs-ns),0.),'gross_arrival_t':gross,'case_loss_t':l,'capacity_overflow_t':ov,'total_demand_t':total,'critical_demand_t':crit,'total_served_t':cs+ns,'critical_served_t':cs,'total_shortage_t':total-cs-ns,'critical_shortage_t':crit-cs,'end_inventory_t':end})
        ts=served/td if td else 1.; cs=crit_served/cd if cd else 1.; ereq=td*45/365.; er=float(ys.loc['E','reserved_capacity_tpy']) if 'E' in ys.index else 0.; bridge=float(reserve.loc[y,'bridge_coverage_t']) if y in reserve.index else 0.; bridge_req=td*42/365.; physical=start+1e-9>=ereq; contractual=er+1e-9>=ereq and bridge+start+1e-9>=bridge_req
        cost=float(source_costs[source_costs.year.eq(y)].source_cost_m.sum()); capex=float(inv2.loc[y,'capex_total_m']); initcost=inputs.initial_inventory_cost_m if y==H[0] else 0.; isruopex=float(config['investments']['lunar_isru']['fixed_opex_m_per_year']) if st['isru_active_year'] is not None and y>=st['isru_active_year'] else 0.; nominal=cost+hold+fixed+isruopex+capex+initcost; pv=nominal/(1+inputs.real_discount_rate)**(y-H[0])
        annual.append({'year':y,'scenario':inputs.scenario,'storage_mode':label,'storage_capacity_t':storage_cap,'loss_rate':loss_rate,'start_inventory_t':start,'end_inventory_t':inventory,'gross_arrival_t':float(ys.actual_gross_delivery_t.sum()),'case_loss_t':loss,'capacity_overflow_t':overflow,'total_demand_t':td,'critical_demand_t':cd,'total_served_t':served,'critical_served_t':crit_served,'total_shortage_t':td-served,'critical_shortage_t':cd-crit_served,'total_service_level':ts,'critical_service_level':cs,'reserve_required_t':ereq,'emergency_reserved_t':er,'bridge_required_t':bridge_req,'bridge_external_t':bridge,'physical_reserve_ok':physical,'contractual_reserve_ok':contractual,'reserve_ok':physical or contractual,'source_contract_cost_m':cost,'holding_cost_m':hold,'fixed_opex_m':fixed+isruopex,'capex_m':capex,'initial_inventory_cost_m':initcost,'nominal_cost_m':nominal,'pv_cost_m':pv})
    annual=pd.DataFrame(annual); monthly=pd.DataFrame(monthly); meta=scenario_metadata(inputs.scenario,config); sev='hard' if meta.get('service_is_hard_constraint') else 'target'; cmin=float(config['service_constraints_standard']['critical_min']); tmin=float(config['service_constraints_standard']['total_min'])
    for _,r in annual.iterrows():
        y=int(r.year); cons += [_crow('critical_service',y,r.critical_service_level+1e-12>=cmin,float(r.critical_service_level),cmin,sev,'Critical service level'),_crow('total_service',y,r.total_service_level+1e-12>=tmin,float(r.total_service_level),tmin,sev,'Total service level'),_crow('45_day_reserve',y,bool(r.reserve_ok),f"physical={r.start_inventory_t:.3f}; emergency={r.emergency_reserved_t:.3f}; bridge={r.bridge_external_t:.3f}",f"equivalent={r.reserve_required_t:.3f} t",'hard','Physical stock or emergency reserve plus bridge coverage')]
        if r.capacity_overflow_t>1e-9:cons.append(_crow('storage_capacity',y,False,float(r.capacity_overflow_t),0.,'hard','Storage overflow'))
        if inputs.scenario=='mandatory_stress' and y>=2038:
            lim=float(config['stress']['max_storage_loss_rate_from_2038']); cons.append(_crow('stress_storage_loss_rate',y,r.loss_rate<=lim+1e-12,float(r.loss_rate),lim,'hard','Stress loss-rate ceiling'))
    cum=annual.set_index('year').capex_m.cumsum(); c37=float(cum.loc[2037]) if 2037 in cum.index else float(cum.iloc[-1]); c40=float(cum.loc[2040]) if 2040 in cum.index else float(cum.iloc[-1]); cons += [_crow('capex_through_2037',2037,c37<=float(config['capex_limits_m']['through_2037'])+1e-9,c37,float(config['capex_limits_m']['through_2037']),'hard','Cumulative CAPEX limit'),_crow('capex_through_2040',2040,c40<=float(config['capex_limits_m']['through_2040'])+1e-9,c40,float(config['capex_limits_m']['through_2040']),'hard','Cumulative CAPEX limit')]
    zt=st['zbo_total_capex_m']; zr=float(config['storage']['upgrade']['capex_m']); it=st['isru_total_capex_m']; ir=float(config['investments']['lunar_isru']['capex_m']); ot=st['earth_new_option_fee_total_m']; et=st['earth_new_exercise_capex_total_m']; ec=config['investments']['earth_new']
    if 1e-9<zt<zr-1e-9:cons.append(_crow('zbo_funding',None,False,zt,zr,'hard','Partial funding does not activate upgrade'))
    if it>1e-9 and not st['isru_funded']:cons.append(_crow('isru_funding_deadline',2037,False,st['isru_funded_by_2037_m'],ir,'hard','Full ISRU CAPEX must be funded by end-2037'))
    if et>1e-9 and ot+1e-9<float(ec['option_fee_m']):cons.append(_crow('earth_new_option_before_exercise',None,False,ot,float(ec['option_fee_m']),'hard','Option fee required before exercise'))
    if zt>zr+1e-9:warn.append('ZBO/CFM overpayment')
    if it>ir+1e-9:warn.append('ISRU overpayment')
    e=source_costs[source_costs.source_id.eq('E')].sort_values('year'); run=0
    for _,r in e.iterrows():
        run=run+1 if r.planned_gross_delivery_t>1e-9 and str(r.role).lower()!='insurance' else 0
        if run>2:cons.append(_crow('emergency_base_use_consecutive_years',int(r.year),False,run,2,'hard','Emergency cannot be base supply >2 consecutive years'))
    if inputs.initial_inventory_t>float(annual.iloc[0].storage_capacity_t)+1e-9:cons.append(_crow('initial_inventory_capacity',H[0],False,inputs.initial_inventory_t,float(annual.iloc[0].storage_capacity_t),'hard','Initial stock exceeds storage'))
    cdf=pd.DataFrame(cons).drop_duplicates(subset=['constraint','year','actual','limit','reason']).reset_index(drop=True) if cons else pd.DataFrame(columns=['constraint','year','ok','actual','limit','severity','reason'])
    total_served=float(annual.total_served_t.sum()); nominal=float(annual.nominal_cost_m.sum()); pv=float(annual.pv_cost_m.sum()); metrics={'scenario':inputs.scenario,'total_demand_t':float(annual.total_demand_t.sum()),'total_served_t':total_served,'total_shortage_t':float(annual.total_shortage_t.sum()),'min_total_service_level':float(annual.total_service_level.min()),'min_critical_service_level':float(annual.critical_service_level.min()),'total_case_loss_t':float(annual.case_loss_t.sum()),'total_capacity_overflow_t':float(annual.capacity_overflow_t.sum()),'nominal_lifecycle_cost_m':nominal,'present_cost_m':pv,'cost_per_served_t_m':nominal/total_served if total_served else float('inf'),'capex_through_2037_m':c37,'capex_through_2040_m':c40,'final_inventory_t':float(annual.iloc[-1].end_inventory_t),'hard_constraints_ok':bool(cdf.loc[cdf.severity.eq('hard'),'ok'].all()) if not cdf.empty else True}
    return SimulationResult(annual,monthly,source_costs,cdf,st,metrics,sorted(set(warn)))
