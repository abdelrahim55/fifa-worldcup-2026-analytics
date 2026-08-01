from __future__ import annotations

import streamlit as st

CSS = r'''
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');
:root{
  --bg:#070b12;
  --bg2:#0d1420;
  --surface:#101927;
  --surface2:#131f2f;
  --paper:#f4f6f8;
  --white:#ffffff;
  --text:#0b1422;
  --muted:#6c7886;
  --muted2:#8c98a6;
  --line:#e2e8ee;
  --green:#43e58b;
  --green2:#16b967;
  --red:#ff4f61;
  --gold:#f5c451;
  --cyan:#4fdcff;
  --blue:#4b7dff;
  --shadow:0 18px 50px rgba(8,18,32,.10);
}
html,body,[class*="css"]{font-family:'Inter',sans-serif;}
body{background:var(--paper);}
.stApp{background:
  radial-gradient(circle at 12% -10%, rgba(79,220,255,.11), transparent 24%),
  radial-gradient(circle at 90% 5%, rgba(67,229,139,.10), transparent 22%),
  var(--paper);
}
.block-container{max-width:1520px;padding:1.0rem 1.5rem 4rem;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#070b12 0%,#0a111b 100%);border-right:1px solid rgba(255,255,255,.07);}
section[data-testid="stSidebar"] *{color:#eef3f7 !important;}
section[data-testid="stSidebar"] hr{border-color:rgba(255,255,255,.10);}
[data-testid="stSidebarNav"]{display:none;}

/* top navigation */
.site-nav{position:sticky;top:0;z-index:100;display:flex;align-items:center;gap:9px;padding:8px 10px;margin:0 0 14px;background:rgba(255,255,255,.82);border:1px solid rgba(218,225,232,.85);border-radius:18px;box-shadow:0 10px 30px rgba(14,29,46,.07);backdrop-filter:blur(16px);}
.nav-brand{display:flex;align-items:center;gap:9px;padding:4px 11px 4px 5px;min-width:190px;}
.nav-ball{width:34px;height:34px;display:grid;place-items:center;border-radius:11px;background:linear-gradient(145deg,#101d2b,#1e344a);color:#fff;font-size:16px;box-shadow:inset 0 1px 0 rgba(255,255,255,.18);}
.nav-brand__name{font-family:'Barlow Condensed';font-size:21px;font-weight:900;letter-spacing:.04em;line-height:.95;color:#0c1622;}
.nav-brand__tag{font-size:8px;text-transform:uppercase;letter-spacing:.14em;color:#758291;margin-top:4px;}
.nav-spacer{flex:1;}
.nav-note{font-size:9px;font-weight:800;text-transform:uppercase;letter-spacing:.13em;color:#82909f;}
.nav-link-wrap div[data-testid="stPageLink"]{display:block;}
.nav-link-wrap a{border-radius:12px !important;border:1px solid transparent !important;padding:8px 11px !important;text-decoration:none !important;font-size:11px !important;font-weight:800 !important;color:#506071 !important;background:transparent !important;transition:.2s ease !important;}
.nav-link-wrap a:hover{background:#edf2f6 !important;color:#0d1521 !important;transform:translateY(-1px);}
.nav-active a{background:#0d1826 !important;color:#fff !important;box-shadow:0 8px 20px rgba(7,15,25,.14);}

/* newsroom hero */
.hero{position:relative;overflow:hidden;border-radius:30px;color:#fff;background:linear-gradient(118deg,#070d15 0%,#0b1b2b 52%,#17354a 100%);box-shadow:0 28px 80px rgba(10,28,46,.20);margin-bottom:16px;border:1px solid rgba(255,255,255,.06);}
.hero--newsroom{padding:26px 30px 30px;min-height:280px;}
.hero__topline{display:flex;align-items:center;gap:8px;font-size:10px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:#a9bac8;}
.live-dot{width:8px;height:8px;background:var(--red);border-radius:50%;box-shadow:0 0 0 0 rgba(255,79,97,.65);animation:pulse 1.8s infinite;}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(255,79,97,.7)}70%{box-shadow:0 0 0 10px rgba(255,79,97,0)}100%{box-shadow:0 0 0 0 rgba(255,79,97,0)}}
.hero h1{font-family:'Barlow Condensed';font-size:72px;line-height:.90;letter-spacing:-.03em;margin:15px 0 12px;max-width:960px;position:relative;z-index:2;}
.hero p{max-width:820px;color:rgba(255,255,255,.73);font-size:13px;line-height:1.72;margin:0;position:relative;z-index:2;}
.hero__meta{display:flex;align-items:center;flex-wrap:wrap;gap:8px;margin-top:17px;position:relative;z-index:2;}
.hero-pill{display:inline-flex;align-items:center;gap:6px;padding:7px 10px;border:1px solid rgba(255,255,255,.11);background:rgba(255,255,255,.055);border-radius:999px;color:#d9e5ee;font-size:9px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;}
.hero__shape{position:absolute;border-radius:999px;filter:blur(.2px);}
.hero__shape--one{width:360px;height:360px;right:-100px;top:-150px;background:radial-gradient(circle,rgba(79,220,255,.16),rgba(79,220,255,0) 65%);animation:float 9s ease-in-out infinite;}
.hero__shape--two{width:310px;height:310px;right:160px;bottom:-200px;background:radial-gradient(circle,rgba(67,229,139,.18),rgba(67,229,139,0) 65%);animation:float 11s ease-in-out infinite reverse;}
.hero__shape--grid{right:30px;bottom:28px;width:270px;height:140px;opacity:.25;background-image:linear-gradient(rgba(255,255,255,.12) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.12) 1px,transparent 1px);background-size:18px 18px;transform:skewY(-7deg);}
@keyframes float{0%,100%{transform:translate3d(0,0,0)}50%{transform:translate3d(0,16px,0)}}

/* ticker */
.ticker{overflow:hidden;position:relative;margin:0 0 16px;border-radius:14px;border:1px solid #dfe6ec;background:#fff;box-shadow:0 8px 24px rgba(14,29,46,.05);}
.ticker__track{display:flex;width:max-content;gap:28px;padding:9px 0;animation:tickerMove 28s linear infinite;}
.ticker__item{font-size:9px;font-weight:900;letter-spacing:.12em;text-transform:uppercase;color:#6d7b89;white-space:nowrap;}
.ticker__item b{color:#0d1826;}
.ticker__item .dot{display:inline-block;width:5px;height:5px;background:var(--red);border-radius:50%;margin:0 9px 1px;}
@keyframes tickerMove{from{transform:translateX(0)}to{transform:translateX(-50%)}}

/* page intro / explainer */
.page-intro{display:flex;align-items:stretch;gap:12px;margin:0 0 15px;}
.page-intro__main{flex:1;padding:14px 16px;border-radius:17px;background:#fff;border:1px solid var(--line);box-shadow:0 8px 24px rgba(14,29,46,.04);}
.page-intro__eyebrow{font-size:9px;font-weight:900;text-transform:uppercase;letter-spacing:.13em;color:#6f7e8d;}
.page-intro__title{font-family:'Barlow Condensed';font-size:28px;line-height:1;margin:5px 0 5px;color:#0c1622;}
.page-intro__text{font-size:11px;line-height:1.6;color:#687585;max-width:900px;}
.page-intro__how{width:330px;padding:14px 16px;border-radius:17px;background:linear-gradient(145deg,#0d1826,#13263a);color:#e6eef5;border:1px solid rgba(255,255,255,.05);}
.page-intro__how strong{color:#fff;font-size:11px;}
.page-intro__how p{font-size:10px;line-height:1.55;color:#9eafbf;margin:5px 0 0;}

/* filters */
.filter-strip{display:flex;align-items:center;gap:10px;background:#fff;border:1px solid var(--line);padding:10px 13px;border-radius:14px;margin-bottom:16px;font-size:10px;color:#7a8794;box-shadow:0 8px 24px rgba(26,53,44,.04);}
.filter-strip__label{font-size:9px;font-weight:900;color:#0b9b5b;letter-spacing:.13em;}
.filter-strip__dates{margin-left:auto;font-variant-numeric:tabular-nums;}

/* cards + kpis */
.section-title{font-family:'Barlow Condensed';font-size:36px;font-weight:900;color:#0b1422;line-height:1;margin:12px 0 4px;}
.section-subtitle{font-size:11px;color:#758392;margin-bottom:12px;}
.kpi{position:relative;background:linear-gradient(180deg,#fff,#fbfcfd);border:1px solid var(--line);border-radius:20px;padding:18px 20px;min-height:122px;box-shadow:var(--shadow);transition:transform .22s ease,box-shadow .22s ease;animation:rise .45s ease both;overflow:hidden;}
.kpi:hover{transform:translateY(-5px);box-shadow:0 22px 48px rgba(14,29,46,.13);}
.kpi:before{content:'';position:absolute;right:-25px;top:-28px;width:100px;height:100px;border-radius:50%;background:radial-gradient(circle,rgba(67,229,139,.18),rgba(67,229,139,0) 68%);}
.kpi--dark{background:linear-gradient(145deg,#0b1624,#102238);border-color:#203249;color:#fff;}
.kpi--dark .kpi__label{color:#91a5b8}.kpi--dark .kpi__value{color:#fff}.kpi--dark .kpi__note{color:#6df2aa}
.kpi__label{font-size:9px;text-transform:uppercase;letter-spacing:.13em;color:#7d8a97;font-weight:900;}
.kpi__value{font-family:'Barlow Condensed';font-size:39px;font-weight:900;color:#0c1622;margin-top:5px;line-height:.98;overflow-wrap:anywhere;}
.kpi__note{font-size:10px;color:#0d9e5f;font-weight:800;margin-top:8px;}
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.card,.match-card,.feature-card,.mini-stat,.explain-card{background:#fff;border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow);}
.card{padding:18px;}
.match-card{padding:17px;transition:transform .22s ease,box-shadow .22s ease;}
.match-card:hover{transform:translateY(-3px);box-shadow:0 20px 46px rgba(14,29,46,.12);}
.score{font-family:'Barlow Condensed';font-size:44px;font-weight:900;color:#0b1422;line-height:1;}
.team{font-size:15px;font-weight:900;color:#0b1422;}
.muted{font-size:10px;color:#7e8b98;}
.badge{display:inline-flex;align-items:center;padding:5px 8px;border-radius:999px;background:#edf8f1;color:#0b9e5c;font-size:9px;font-weight:900;text-transform:uppercase;letter-spacing:.07em;}
.badge--red{background:#fff0f2;color:#f04758;}
.badge--dark{background:#eef2f6;color:#445566;}
.explain-card{padding:17px 18px;margin:0 0 15px;background:linear-gradient(145deg,#0d1826,#12263a);color:#fff;}
.explain-card__kicker{font-size:9px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:#6df2aa;}
.explain-card__title{font-family:'Barlow Condensed';font-size:25px;font-weight:900;line-height:1;margin:6px 0;}
.explain-card__text{font-size:11px;line-height:1.65;color:#a9bac8;}
.explain-card__grid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-top:12px;}
.explain-card__item{padding:10px;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.04);border-radius:13px;}
.explain-card__item b{display:block;font-size:9px;text-transform:uppercase;letter-spacing:.08em;color:#fff;margin-bottom:3px;}
.explain-card__item span{font-size:9px;color:#91a5b8;line-height:1.5;}

/* landing */
.home-grid{display:grid;grid-template-columns:1.5fr 1fr 1fr;gap:13px;margin:15px 0 22px;}
.feature-card{position:relative;padding:21px;min-height:182px;overflow:hidden;transition:transform .25s ease,border-color .25s ease,box-shadow .25s ease;background:linear-gradient(180deg,#fff,#fafcfd);}
.feature-card:hover{transform:translateY(-6px);border-color:#b8d8ca;box-shadow:0 24px 54px rgba(14,29,46,.12);}
.feature-card:after{content:'';position:absolute;right:-50px;bottom:-65px;width:180px;height:180px;border-radius:50%;background:radial-gradient(circle,rgba(79,220,255,.11),rgba(79,220,255,0) 68%);}
.feature-card--wide{background:linear-gradient(135deg,#0b1624,#132b3e);color:#fff;border-color:#14293b;}
.feature-card--wide h3,.feature-card--wide p{color:#fff;}.feature-card--wide .feature-kicker{color:#6df2aa;}
.feature-kicker{font-size:9px;font-weight:900;letter-spacing:.14em;color:#0a9c5c;}
.feature-card h3{font-family:'Barlow Condensed';font-size:31px;line-height:1;margin:13px 0 7px;color:#0b1422;}
.feature-card p{font-size:11px;line-height:1.65;color:#70808e;max-width:330px;}
.feature-arrow{position:absolute;right:18px;bottom:12px;font-size:22px;font-weight:900;color:#0c9b5c;z-index:2;}
.mini-stat{padding:18px 20px;}.mini-stat__value{font-family:'Barlow Condensed';font-size:34px;font-weight:900;color:#0b1422;line-height:1;}.mini-stat__label{font-size:10px;text-transform:uppercase;letter-spacing:.11em;font-weight:900;margin-top:6px;color:#3b4b5a;}.mini-stat__note{font-size:10px;color:#7b8895;margin-top:4px;}

/* streamlit widgets */
.stSelectbox label,.stMultiSelect label,.stDateInput label,.stTextInput label{font-size:10px !important;font-weight:800 !important;text-transform:uppercase;letter-spacing:.10em;color:#73808d !important;}
div[data-baseweb="select"]>div{border-radius:12px !important;border-color:#dfe5eb !important;background:#fff !important;}
.stTextInput>div>div{border-radius:12px !important;border-color:#dfe5eb !important;background:#fff !important;}
.stButton>button{border-radius:12px !important;font-weight:900 !important;border:1px solid #12263a !important;background:#0d1826 !important;color:#fff !important;box-shadow:0 10px 22px rgba(13,24,38,.12) !important;transition:.2s ease !important;}
.stButton>button:hover{transform:translateY(-2px);box-shadow:0 14px 28px rgba(13,24,38,.16) !important;}
.stTabs [data-baseweb="tab-list"]{gap:6px;}
.stTabs [data-baseweb="tab"]{background:#fff;border:1px solid var(--line);border-radius:999px;padding:8px 14px;font-size:10px;font-weight:800;}
.stTabs [aria-selected="true"]{background:#0d1826 !important;color:#fff !important;border-color:#0d1826 !important;}
.stDataFrame{border:1px solid var(--line);border-radius:14px;overflow:hidden;}

/* footer */
.footer{margin-top:30px;padding:16px 4px;border-top:1px solid #dce3e9;color:#7d8996;font-size:9px;letter-spacing:.04em;display:flex;justify-content:space-between;gap:10px;}
.footer b{color:#273746;}

@media(max-width:1100px){.nav-note{display:none}.nav-brand{min-width:150px}.home-grid{grid-template-columns:1fr 1fr}.page-intro{flex-direction:column}.page-intro__how{width:auto}.explain-card__grid{grid-template-columns:1fr;}.hero h1{font-size:58px;}}
@media(max-width:700px){.block-container{padding:1rem .75rem 3rem}.site-nav{overflow:auto}.nav-brand{min-width:135px}.hero--newsroom{min-height:250px;padding:22px}.hero h1{font-size:48px}.home-grid{grid-template-columns:1fr}.filter-strip{flex-wrap:wrap}.filter-strip__dates{margin-left:0;width:100%;}.kpi__value{font-size:33px;}}
</style>
'''

def apply_theme() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
