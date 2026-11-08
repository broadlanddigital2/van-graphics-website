(function(){
'use strict';


/* ---------- storage helpers ---------- */
const LS = {
  get(k,d){ try{ const v=localStorage.getItem(k); return v?JSON.parse(v):d; }catch(e){ return d; } },
  set(k,v){ try{ localStorage.setItem(k,JSON.stringify(v)); }catch(e){} },
  del(k){ try{ localStorage.removeItem(k); }catch(e){} }
};
const $ = s => document.querySelector(s);
const esc = s => String(s==null?'':s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

/* ---------- data ---------- */
const VANS = {
  'Ford':['Transit Connect|small','Transit Custom|medium','Transit|large','E-Transit|large'],
  'Mercedes-Benz':['Citan|small','Vito|medium','Sprinter|large'],
  'Volkswagen':['Caddy|small','Transporter|medium','ID. Buzz Cargo|medium','Crafter|large'],
  'Vauxhall':['Combo|small','Vivaro|medium','Movano|large'],
  'Renault':['Kangoo|small','Trafic|medium','Master|large'],
  'Citroën':['Berlingo|small','Dispatch|medium','Relay|large'],
  'Peugeot':['Partner|small','Expert|medium','Boxer|large'],
  'Toyota':['Proace City|small','Proace|medium','Proace Max|large'],
  'Nissan':['Townstar|small','Primastar|medium','Interstar|large'],
  'Fiat':['Doblo|small','Scudo|medium','Ducato|large']
};
const COLOURS = [
  ['White','#f3f4f6'],['Black','#16181c'],['Silver','#c2c6cc'],['Grey','#5a5f66'],
  ['Blue','#1e4f9e'],['Red','#b4232c'],['Green','#2e6a3b'],['Yellow','#f1c232'],['Orange','#de6a1d']
];
const TRADES = {
  'Plumbing & heating':['Plumbing','Heating','Boiler Installs','Boiler Servicing','Bathrooms','Emergency Callouts'],
  'Electrical':['Rewires','Fuse Boards','EV Chargers','Lighting','Testing & Inspection','Smart Home'],
  'Building':['Extensions','Renovations','Loft Conversions','Brickwork','Groundworks','Kitchens'],
  'Roofing':['New Roofs','Roof Repairs','Flat Roofs','Guttering','Fascias & Soffits','Chimneys'],
  'Landscaping':['Garden Design','Patios','Fencing','Turfing','Decking','Maintenance'],
  'Cleaning':['Domestic','Commercial','End of Tenancy','Carpets','Windows','Pressure Washing'],
  'Removals':['House Moves','Office Moves','Storage','Packing','Man & Van','Clearances'],
  'Other':[]
};
const TRUST = ['Free Quotes','Fully Insured','24/7 Callouts','Family Run','No Job Too Small','Local & Reliable'];

/* ---------- state ---------- */
const DEFAULT = {
  reg:'', make:'Ford', model:'Transit Custom', size:'medium', lwb:false,
  body:'#f3f4f6', bodyName:'White', mode:'graphics',
  logo:null, logoAR:1, P:'#0b4fb3', S:'#ffcc00',
  company:'', tagline:'', phone:'', web:'', email:'', social:'',
  show:{company:true,tagline:true,phone:true,web:true,email:false,social:false},
  trade:'Plumbing & heating', services:['Plumbing','Heating','Boiler Installs','Bathrooms'], trust:['Free Quotes','Fully Insured'],
  designed:false, layout:0, view:'studio', scene:'motorway'
};
let S = Object.assign({}, DEFAULT, LS.get('nvg_state',{}));
S.show = Object.assign({}, DEFAULT.show, S.show||{});
let session = null; let AUTH = LS.get('nvg_auth', null); let DESIGNS = []; let CUR_ID = LS.get('nvg_design_id', null);

/* ---------- colour utils ---------- */
function hex2rgb(h){ h=h.replace('#',''); if(h.length===3) h=h.split('').map(c=>c+c).join(''); const n=parseInt(h,16); return [n>>16&255,n>>8&255,n&255]; }
function rgb2hex(r,g,b){ return '#'+[r,g,b].map(v=>Math.max(0,Math.min(255,Math.round(v))).toString(16).padStart(2,'0')).join(''); }
function lum(h){ const [r,g,b]=hex2rgb(h).map(v=>{v/=255;return v<=.03928?v/12.92:Math.pow((v+.055)/1.055,2.4);}); return .2126*r+.7152*g+.0722*b; }
function contrastText(h){ return lum(h)>0.45?'#111318':'#ffffff'; }
function dist(a,b){ const A=hex2rgb(a),B=hex2rgb(b); return Math.sqrt((A[0]-B[0])**2+(A[1]-B[1])**2+(A[2]-B[2])**2); }
function mix(a,b,t){ const A=hex2rgb(a),B=hex2rgb(b); return rgb2hex(A[0]+(B[0]-A[0])*t,A[1]+(B[1]-A[1])*t,A[2]+(B[2]-A[2])*t); }

/* ---------- van geometry ---------- */
const VW=1100, VH=480, GROUND=440;
const TYPES={
  small:{len:640,roofY:178,wsX:118,wsY:280,rsX:262,noseY:318,botY:405,r:42},
  medium:{len:770,roofY:128,wsX:108,wsY:268,rsX:250,noseY:312,botY:406,r:45},
  large:{len:860,roofY:70,wsX:82,wsY:258,rsX:222,noseY:302,botY:408,r:47}
};
function geom(size,lwb){
  const t=Object.assign({},TYPES[size]);
  if(lwb) t.len += size==='large'?120:size==='medium'?90:70;
  const x0=(VW-t.len)/2, xr=x0+t.len;
  const wheelY=GROUND-t.r;
  const fx=x0+t.wsX+40, rx=xr-(size==='large'?150:128);
  const wsTopX=x0+t.rsX-22, wsTopY=t.roofY+8;
  const lineX=y=>x0+t.wsX+(t.wsY-y)/(t.wsY-wsTopY)*(wsTopX-(x0+t.wsX));
  const winTop=t.roofY+24, winBot=t.wsY-6;
  const doorX=x0+t.rsX+92;
  const win=[[lineX(winBot)+20,winBot],[lineX(winTop)+20,winTop],[doorX-14,winTop],[doorX-14,winBot]];
  const archTop=wheelY-(t.r+11);
  const cargo={x1:doorX+20,x2:xr-24,y1:t.roofY+24,y2:archTop-12};
  const door={x1:lineX(winBot)+12,x2:doorX-12,y1:winBot+12,y2:archTop-6};
  const strip={x1:fx+t.r+26,x2:rx-t.r-26,y:t.botY-16};
  const body=`M${x0+12} ${t.botY} L${x0} ${t.botY-18} L${x0} ${t.noseY} Q${x0} ${t.noseY-26} ${x0+32} ${t.noseY-32} L${x0+t.wsX} ${t.wsY} L${wsTopX} ${wsTopY} Q${x0+t.rsX} ${t.roofY} ${x0+t.rsX+34} ${t.roofY} L${xr-16} ${t.roofY} Q${xr} ${t.roofY} ${xr} ${t.roofY+16} L${xr} ${t.botY-12} Q${xr} ${t.botY} ${xr-12} ${t.botY} Z`;
  return Object.assign(t,{x0,xr,fx,rx,wheelY,win,doorX,cargo,door,strip,body,archTop,wsTopX,wsTopY});
}

/* ---------- svg text helpers ---------- */
const F_BLACK='Archivo Black, Arial Black, sans-serif', F_REG='Archivo, Arial, sans-serif';
function fit(text,maxW,maxS,f){ if(!text) return maxS; return Math.max(9,Math.min(maxS,maxW/(String(text).length*(f||0.58)))); }
let FLIP=false;
function T(x,y,size,text,fill,o){ o=o||{}; if(!text) return ''; if(FLIP){ o=Object.assign({},o,{a:o.a==='end'?'start':o.a==='middle'?'middle':'end'}); } return `<text${FLIP?` transform="translate(${(2*x).toFixed(1)} 0) scale(-1 1)"`:''} x="${x.toFixed(1)}" y="${y.toFixed(1)}" font-size="${size.toFixed(1)}" fill="${fill}" font-family="${o.fam||F_REG}" font-weight="${o.w||700}" text-anchor="${o.a||'start'}"${o.ls?` letter-spacing="${o.ls}"`:''}${o.op?` opacity="${o.op}"`:''}>${esc(text)}</text>`; }
function initials(name){ const w=String(name||'Your Company').trim().split(/\s+/).filter(Boolean); return ((w[0]||'Y')[0]+((w[1]||'')[0]||'')).toUpperCase(); }
function logoBox(st,x,y,w,h,align,plate){
  let lw,lh;
  if(st.logo){ const ar=st.logoAR||1; if(ar>w/h){lw=w;lh=w/ar;} else {lh=h;lw=h*ar;} }
  else { lw=lh=Math.min(w,h); }
  const lx = align==='center'? x+(w-lw)/2 : align==='right'? x+w-lw : x;
  const ly = y+(h-lh)/2;
  let s='';
  if(st.logo){
    if(plate) s+=`<rect x="${(lx-10).toFixed(1)}" y="${(ly-10).toFixed(1)}" width="${(lw+20).toFixed(1)}" height="${(lh+20).toFixed(1)}" rx="12" fill="#fff"/>`;
    s+=`<image${FLIP?` transform="translate(${(2*(lx+lw/2)).toFixed(1)} 0) scale(-1 1)"`:''} href="${st.logo}" x="${lx.toFixed(1)}" y="${ly.toFixed(1)}" width="${lw.toFixed(1)}" height="${lh.toFixed(1)}" preserveAspectRatio="xMidYMid meet"/>`;
  } else {
    const r=lw/2, cx=lx+r, cy=ly+r;
    const fill = plate? '#ffffff' : st.P;
    const ink = plate? st.P : contrastText(st.P);
    s+=`<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${r.toFixed(1)}" fill="${fill}"/>`;
    if(!plate) s+=`<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="${(r-5).toFixed(1)}" fill="none" stroke="${st.S}" stroke-width="3"/>`;
    s+=T(cx,cy+r*0.36,r*0.95,initials(st.company),ink,{fam:F_BLACK,a:'middle'});
  }
  return {svg:s,w:lw,h:lh,x:lx,y:ly};
}
function info(st){
  const on=k=>st.show[k]&&String(st[k]||'').trim();
  return {
    name: on('company')? st.company.trim() : (st.show.company?'Your Company':''),
    tag: on('tagline')? st.tagline.trim() : '',
    phone: on('phone')? st.phone.trim() : (st.show.phone?'01632 960 000':''),
    web: on('web')? st.web.trim() : (st.show.web?'www.yourcompany.co.uk':''),
    email: on('email')? st.email.trim() : '',
    social: on('social')? st.social.trim() : '',
    svc: (st.services||[]).slice(0,6).join('  •  '),
    trust: (st.trust||[]).slice(0,2).join('  ·  ')
  };
}

/* ---------- layouts ---------- */
function graphicsInk(st){ return lum(st.body)>0.42 ? (lum(st.P)<0.32? st.P : '#111318') : '#ffffff'; }
function graphicsAcc(st){ if(dist(st.P,st.body)>110) return st.P; if(dist(st.S,st.body)>110) return st.S; return graphicsInk(st); }

const LAYOUTS = {
graphics:[
 { name:'Classic', draw(st,g){
   const C=g.cargo, cw=C.x2-C.x1, ch=C.y2-C.y1, I=info(st), ink=graphicsInk(st), acc=graphicsAcc(st);
   let back='', front='';
   // swoosh stripe
   back+=`<path d="M${g.x0-5} ${g.botY-40} C${g.x0+g.len*.35} ${g.botY-14} ${g.x0+g.len*.62} ${g.botY-50} ${g.xr+5} ${g.botY-62} L${g.xr+5} ${g.botY-46} C${g.x0+g.len*.62} ${g.botY-32} ${g.x0+g.len*.35} ${g.botY+2} ${g.x0-5} ${g.botY-24} Z" fill="${acc}"/>`;
   back+=`<path d="M${g.x0-5} ${g.botY-50} C${g.x0+g.len*.35} ${g.botY-25} ${g.x0+g.len*.62} ${g.botY-62} ${g.xr+5} ${g.botY-74}" fill="none" stroke="${st.S===acc?st.P:st.S}" stroke-width="5"/>`;
   const L=logoBox(st,C.x1,C.y1+4,cw*.34,ch*.42,'left');
   front+=L.svg;
   const nx=L.x+L.w+20, nw=C.x2-nx;
   const ns=fit(I.name,nw,ch*.2,.7);
   front+=T(nx,C.y1+4+L.h*.5+ns*.2,ns,I.name,ink,{fam:F_BLACK});
   front+=T(nx,C.y1+4+L.h*.5+ns*.2+ns*.75,fit(I.tag,nw,ns*.42,.55),I.tag,ink,{w:600});
   const sy=C.y1+L.h+4+ (C.y2-(C.y1+L.h+4))*.42;
   front+=T(C.x1,sy,fit(I.svc,cw,ch*.085,.56),I.svc,ink,{w:700});
   const ps=fit(I.phone,cw*.6,ch*.17,.62);
   front+=T(C.x1,C.y2-2,ps,I.phone,ink,{fam:F_BLACK});
   front+=`<rect x="${C.x1}" y="${(C.y2+6).toFixed(1)}" width="${(I.phone?Math.min(cw*.6,I.phone.length*ps*.62):0).toFixed(1)}" height="4" fill="${acc}"/>`;
   const rw=cw*.38;
   front+=T(C.x2,C.y2-2-(I.email?ch*.09:0),fit(I.web,rw,ch*.075,.55),I.web,ink,{a:'end',w:700});
   front+=T(C.x2,C.y2-2,fit(I.email,rw,ch*.065,.55),I.email,ink,{a:'end',w:600});
   front+=T(C.x2,sy-ch*.13,fit(I.trust,cw*.5,ch*.06,.55),I.trust.toUpperCase(),ink,{a:'end',w:800,ls:1,op:.8});
   // door
   const D=g.door, dw=D.x2-D.x1;
   const DL=logoBox(st,D.x1,D.y1,dw,(D.y2-D.y1)*.5,'center');
   front+=DL.svg;
   front+=T(D.x1+dw/2,D.y2-4,fit(I.phone,dw,(D.y2-D.y1)*.2,.6),I.phone,ink,{a:'middle',fam:F_BLACK});
   front+=T(D.x1+dw/2,D.y2-4-(D.y2-D.y1)*.22,fit(I.social,dw,13,.55),I.social,ink,{a:'middle',w:600});
   return {back,front};
 }},
 { name:'Bold band', draw(st,g){
   const C=g.cargo, cw=C.x2-C.x1, ch=C.y2-C.y1, I=info(st), ink=graphicsInk(st), acc=graphicsAcc(st);
   const by=C.y1+ch*.36, bh=ch*.3, bt=contrastText(acc);
   let back=`<rect x="${g.x0-5}" y="${by.toFixed(1)}" width="${g.len+10}" height="${bh.toFixed(1)}" fill="${acc}"/><rect x="${g.x0-5}" y="${(by+bh+4).toFixed(1)}" width="${g.len+10}" height="5" fill="${st.S===acc?st.P:st.S}"/>`;
   let front='';
   const L=logoBox(st,C.x1,C.y1,cw*.4,by-C.y1-10,'left');
   front+=L.svg;
   front+=T(C.x2,C.y1+(by-C.y1)*.62,fit(I.tag,cw-L.w-24,ch*.075,.55),I.tag,ink,{a:'end',w:600});
   front+=T(C.x1+cw/2,by+bh*.68,fit(I.name,cw-24,bh*.6,.7),I.name,bt,{a:'middle',fam:F_BLACK});
   const below=C.y2-(by+bh+9);
   front+=T(C.x1+cw/2,by+bh+9+below*.4,fit(I.svc,cw,ch*.08,.56),I.svc,ink,{a:'middle'});
   front+=T(C.x1,C.y2-2,fit(I.phone,cw*.55,ch*.15,.62),I.phone,ink,{fam:F_BLACK});
   front+=T(C.x2,C.y2-2,fit(I.web,cw*.42,ch*.07,.55),I.web,ink,{a:'end'});
   const D=g.door, dw=D.x2-D.x1;
   front+=T(D.x1+dw/2,by+bh*.62,fit(I.phone,dw-10,bh*.4,.6),I.phone,bt,{a:'middle',fam:F_BLACK});
   // lower strip
   const sw=g.strip.x2-g.strip.x1;
   front+=T(g.strip.x1+sw/2,g.strip.y,fit([I.email,I.social].filter(Boolean).join('   ·   '),sw,13,.55),[I.email,I.social].filter(Boolean).join('   ·   '),ink,{a:'middle',w:600});
   return {back,front};
 }},
 { name:'Rear sweep', draw(st,g){
   const C=g.cargo, I=info(st), ink=graphicsInk(st), acc=graphicsAcc(st);
   const sx=g.xr-g.len*.24, my=(g.roofY+g.botY)/2;
   let back=`<path d="M${sx} ${g.roofY-5} Q${sx-70} ${my} ${sx+50} ${g.botY+5} L${g.xr+5} ${g.botY+5} L${g.xr+5} ${g.roofY-5} Z" fill="${acc}"/>`;
   back+=`<path d="M${sx-20} ${g.roofY-5} Q${sx-90} ${my} ${sx+30} ${g.botY+5}" fill="none" stroke="${st.S===acc?st.P:st.S}" stroke-width="7"/>`;
   let front='';
   const ax1=C.x1, ax2=sx-70, aw=ax2-ax1, ch=C.y2-C.y1;
   const L=logoBox(st,ax1,C.y1+2,aw,ch*.4,'center');
   front+=L.svg;
   const ny=C.y1+2+ch*.4+ch*.2;
   front+=T(ax1+aw/2,ny,fit(I.name,aw,ch*.17,.7),I.name,ink,{a:'middle',fam:F_BLACK});
   front+=T(ax1+aw/2,ny+ch*.12,fit(I.svc,aw,ch*.07,.56),I.svc,ink,{a:'middle'});
   front+=T(ax1+aw/2,C.y2-2,fit(I.phone,aw,ch*.15,.62),I.phone,ink,{a:'middle',fam:F_BLACK});
   const st2=contrastText(acc), sw=g.xr-sx-30;
   front+=T(g.xr-18,C.y1+ch*.2,fit(I.trust,sw,13,.55),I.trust.toUpperCase(),st2,{a:'end',w:800});
   front+=T(g.xr-18,C.y2-(I.email?ch*.1:0),fit(I.web,sw,ch*.07,.55),I.web,st2,{a:'end'});
   front+=T(g.xr-18,C.y2,fit(I.email,sw,ch*.06,.55),I.email,st2,{a:'end',w:600});
   const D=g.door, dw=D.x2-D.x1;
   front+=logoBox(st,D.x1,D.y1,dw,(D.y2-D.y1)*.55,'center').svg;
   front+=T(D.x1+dw/2,D.y2-4,fit(I.tag||I.social,dw,12,.55),I.tag||I.social,ink,{a:'middle',w:600});
   return {back,front};
 }}
],
wrap:[
 { name:'Split cab', draw(st,g){
   const C=g.cargo, I=info(st), base=st.P, ink=contrastText(base), sc=contrastText(st.S);
   let back=`<rect x="${g.x0-10}" y="${g.roofY-10}" width="${g.len+20}" height="${g.botY-g.roofY+20}" fill="${base}"/>`;
   back+=`<polygon points="${g.x0-10},${g.roofY-10} ${g.doorX-30},${g.roofY-10} ${g.doorX+70},${g.botY+10} ${g.x0-10},${g.botY+10}" fill="${st.S}"/>`;
   back+=`<polygon points="${g.doorX-30},${g.roofY-10} ${g.doorX-16},${g.roofY-10} ${g.doorX+84},${g.botY+10} ${g.doorX+70},${g.botY+10}" fill="#fff" opacity=".9"/>`;
   back+=`<polygon points="${g.xr-g.len*.16},${g.botY+10} ${g.xr+10},${g.botY-55} ${g.xr+10},${g.botY+10}" fill="${st.S}"/>`;
   let front='';
   const x1=g.doorX+96, x2=C.x2, w=x2-x1, ch=C.y2-C.y1;
   const L=logoBox(st,x1+10,C.y1+12,w*.38,ch*.34,'left',true);
   front+=L.svg;
   const nx=L.x+L.w+28, nw=x2-nx;
   front+=T(nx,C.y1+12+ch*.17+ch*.04,fit(I.name,nw,ch*.17,.7),I.name,ink,{fam:F_BLACK});
   front+=T(nx,C.y1+12+ch*.17+ch*.04+ch*.11,fit(I.tag,nw,ch*.065,.55),I.tag,ink,{w:600});
   front+=T(x1,C.y1+ch*.66,fit(I.svc,w,ch*.08,.56),I.svc,ink);
   front+=T(x1,C.y2-2,fit(I.phone,w*.5,ch*.16,.62),I.phone,ink,{fam:F_BLACK});
   front+=T(x2,C.y2-2-(I.email?ch*.09:0),fit(I.web,w*.42,ch*.07,.55),I.web,ink,{a:'end'});
   front+=T(x2,C.y2-2,fit(I.email,w*.42,ch*.06,.55),I.email,ink,{a:'end',w:600});
   front+=T(x2,C.y1+ch*.66-ch*.13,fit(I.trust,w*.5,12,.55),I.trust.toUpperCase(),ink,{a:'end',w:800,op:.85});
   const D=g.door, dw=D.x2-D.x1;
   front+=T(D.x1+dw/2-10,D.y1+(D.y2-D.y1)*.45,fit(I.phone,dw-20,(D.y2-D.y1)*.2,.6),I.phone,sc,{a:'middle',fam:F_BLACK});
   front+=T(D.x1+dw/2-10,D.y1+(D.y2-D.y1)*.45+18,fit(I.social,dw-20,12,.55),I.social,sc,{a:'middle',w:600});
   return {back,front};
 }},
 { name:'Wave', draw(st,g){
   const C=g.cargo, I=info(st), base=st.P, ink=contrastText(mix(base,'#000',.2)), sc=contrastText(st.S);
   const wt=g.archTop-18, L0=g.x0-10, L1=g.xr+10, len=g.len;
   let back=`<defs><linearGradient id="${g.id}wg" x1="0" x2="1"><stop offset="0" stop-color="${mix(base,'#000',.35)}"/><stop offset=".55" stop-color="${base}"/><stop offset="1" stop-color="${mix(base,'#fff',.12)}"/></linearGradient></defs>`;
   back+=`<rect x="${L0}" y="${g.roofY-10}" width="${len+20}" height="${g.botY-g.roofY+20}" fill="url(#${g.id}wg)"/>`;
   back+=`<path d="M${L0} ${wt+30} C${g.x0+len*.25} ${wt-25} ${g.x0+len*.5} ${wt+55} ${g.x0+len*.75} ${wt+5} S${L1} ${wt-40} ${L1} ${wt-40} L${L1} ${g.botY+10} L${L0} ${g.botY+10} Z" fill="${st.S}"/>`;
   back+=`<path d="M${L0} ${wt+12} C${g.x0+len*.25} ${wt-43} ${g.x0+len*.5} ${wt+37} ${g.x0+len*.75} ${wt-13} S${L1} ${wt-58} ${L1} ${wt-58}" fill="none" stroke="#fff" stroke-width="6" opacity=".55"/>`;
   back+=`<path d="M${g.x0+len*.15} ${g.roofY-10} C${g.x0+len*.4} ${g.roofY+60} ${g.x0+len*.7} ${g.roofY-20} ${L1} ${g.roofY+50}" fill="none" stroke="#fff" stroke-width="2" opacity=".18"/>`;
   let front='';
   const x1=C.x1, x2=C.x2, w=x2-x1, top=C.y1, bot=wt-40, h=bot-top;
   const L=logoBox(st,x1+10,top+10,w*.34,h*.42,'left',true);
   front+=L.svg;
   const nx=L.x+L.w+26, nw=x2-nx;
   front+=T(nx,top+10+h*.21+h*.06,fit(I.name,nw,h*.22,.7),I.name,ink,{fam:F_BLACK});
   front+=T(nx,top+10+h*.21+h*.06+h*.14,fit(I.tag,nw,h*.08,.55),I.tag,ink,{w:600});
   front+=T(x1,top+h*.78,fit(I.svc,w,h*.1,.56),I.svc,ink);
   front+=T(x1,bot+h*.06,fit(I.phone,w*.62,h*.2,.62),I.phone,ink,{fam:F_BLACK});
   const sw=g.strip.x2-g.strip.x1, low=[I.web,I.email,I.social].filter(Boolean).join('   ·   ');
   front+=T(g.strip.x1+sw/2,g.strip.y-2,fit(low,sw,15,.55),low,sc,{a:'middle',w:700});
   front+=T(g.strip.x1+sw/2,g.strip.y-24,fit(I.trust,sw,11,.55),I.trust.toUpperCase(),sc,{a:'middle',w:800,op:.85});
   const D=g.door, dw=D.x2-D.x1;
   front+=logoBox(st,D.x1+8,D.y1,dw-16,(D.y2-D.y1)*.5,'center',true).svg;
   return {back,front};
 }},
 { name:'Velocity', draw(st,g){
   const C=g.cargo, I=info(st);
   const base=mix(st.P,'#0b0c0f',.78);
   const hi = lum(st.P)>0.14 ? st.P : (lum(st.S)>0.14 ? st.S : mix(st.P,'#ffffff',.55));
   let back=`<rect x="${g.x0-10}" y="${g.roofY-10}" width="${g.len+20}" height="${g.botY-g.roofY+20}" fill="${base}"/>`;
   const ys=C.y1+(C.y2-C.y1)*.42;
   [[0,hi,18],[34,st.S,10],[60,hi,6]].forEach(([o,c,w])=>{ back+=`<line x1="${g.xr+60}" y1="${ys+o}" x2="${g.xr-300}" y2="${ys+o+360}" stroke="${c}" stroke-width="${w}"/>`; });
   back+=`<rect x="${g.x0-10}" y="${g.botY-34}" width="${g.len*.55}" height="6" fill="${hi}"/>`;
   back+=`<line x1="${g.x0+g.len*.08}" y1="${g.roofY-10}" x2="${g.x0+g.len*.02}" y2="${g.botY+10}" stroke="${hi}" stroke-width="4" opacity=".8"/>`;
   let front='';
   const x1=C.x1, x2=C.x2, w=x2-x1, ch=C.y2-C.y1;
   const L=logoBox(st,x1+10,C.y1+10,w*.32,ch*.32,'left',true);
   front+=L.svg;
   const nx=L.x+L.w+26, nw=x2-nx;
   front+=T(nx,C.y1+10+ch*.16+ch*.05,fit(I.name,nw,ch*.17,.7),I.name,'#fff',{fam:F_BLACK});
   front+=T(nx,C.y1+10+ch*.16+ch*.05+ch*.11,fit(I.tag,nw,ch*.065,.55),I.tag,hi,{w:700});
   front+=T(x1,C.y1+ch*.64,fit(I.svc,w*.72,ch*.075,.56),I.svc,'#fff');
   front+=T(x1,C.y2-2-(I.web?ch*.12:0),fit(I.phone,w*.56,ch*.16,.62),I.phone,'#fff',{fam:F_BLACK});
   front+=T(x1,C.y2-2,fit(I.web,w*.5,ch*.075,.55),I.web,hi,{w:800});
   front+=T(x1,C.y1+ch*.64-ch*.13,fit(I.trust,w*.6,12,.55),I.trust.toUpperCase(),'#cfd3da',{w:800,ls:1});
   const sw=g.strip.x2-g.strip.x1, low=[I.email,I.social].filter(Boolean).join('   ·   ');
   front+=T(g.strip.x1,g.strip.y-2,fit(low,sw*.6,13,.55),low,'#cfd3da',{w:600});
   const D=g.door, dw=D.x2-D.x1;
   front+=T(D.x1+dw/2,D.y1+(D.y2-D.y1)*.42,fit(I.phone,dw-14,(D.y2-D.y1)*.2,.6),I.phone,'#fff',{a:'middle',fam:F_BLACK});
   front+=T(D.x1+dw/2,D.y1+(D.y2-D.y1)*.42+18,fit(I.web,dw-14,12,.55),I.web,hi,{a:'middle',w:700});
   return {back,front};
 }}
]};

/* ---------- van renderer ---------- */
let uid=0;
function renderVan(st,opts){
  opts=opts||{};
  const g=geom(st.size,st.lwb), id='v'+(++uid); g.id=id;
  const bodyCol = st.body;
  let design={back:'',front:''};
  if(opts.design){ const L=LAYOUTS[st.mode][opts.layout||0]; FLIP=!!opts.flip; try{ design=L.draw(st,g); } finally { FLIP=false; } }
  const glass=`url(#${id}gl)`;
  const wheel=(cx)=>{ const r=g.r; return `<g><circle cx="${cx}" cy="${g.wheelY}" r="${r}" fill="#121316"/><circle cx="${cx}" cy="${g.wheelY}" r="${r*.62}" fill="#a9b0b8"/><circle cx="${cx}" cy="${g.wheelY}" r="${r*.5}" fill="#8b929b"/>${[0,72,144,216,288].map(a=>{const rad=a*Math.PI/180;return `<circle cx="${(cx+Math.cos(rad)*r*.3).toFixed(1)}" cy="${(g.wheelY+Math.sin(rad)*r*.3).toFixed(1)}" r="${(r*.06).toFixed(1)}" fill="#5c6168"/>`;}).join('')}<circle cx="${cx}" cy="${g.wheelY}" r="${r*.14}" fill="#4a4f56"/></g>`; };
  const s=[];
  s.push(`<svg viewBox="0 0 ${VW} ${VH}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(st.make+' '+st.model)} ${st.mode} design preview">`);
  s.push(`<defs><clipPath id="${id}c"><path d="${g.body}"/></clipPath>
    <linearGradient id="${id}gl" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3a4552"/><stop offset=".5" stop-color="#25303b"/><stop offset="1" stop-color="#1a222b"/></linearGradient>
    <linearGradient id="${id}sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".22"/><stop offset=".35" stop-color="#fff" stop-opacity="0"/><stop offset=".8" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient>
    <radialGradient id="${id}gr" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>`);
  if(!opts.noFloor) s.push(`<rect x="0" y="${GROUND}" width="${VW}" height="${VH-GROUND}" fill="${opts.floor||'rgba(0,0,0,.05)'}"/>`);
  if(!opts.bare) s.push(`<ellipse cx="${VW/2}" cy="${GROUND+4}" rx="${g.len*.56}" ry="16" fill="url(#${id}gr)"/>`);
  s.push(`<g clip-path="url(#${id}c)"><rect x="0" y="0" width="${VW}" height="${VH}" fill="${bodyCol}"/>`);
  s.push(design.back);
  // panel lines + arches
  s.push(`<line x1="${g.doorX}" y1="${g.roofY+12}" x2="${g.doorX}" y2="${g.botY-24}" stroke="#000" stroke-opacity=".22" stroke-width="2"/>`);
  s.push(`<line x1="${g.doorX+(g.xr-g.doorX)*.5}" y1="${g.roofY+14}" x2="${g.doorX+(g.xr-g.doorX)*.5}" y2="${g.botY-24}" stroke="#000" stroke-opacity=".1" stroke-width="2"/>`);
  s.push(`<line x1="${g.xr-8}" y1="${g.roofY+14}" x2="${g.xr-8}" y2="${g.botY-20}" stroke="#000" stroke-opacity=".14" stroke-width="2"/>`);
  s.push(design.front);
  s.push(`<rect x="0" y="0" width="${VW}" height="${VH}" fill="url(#${id}sh)"/>`);
  s.push(`<circle cx="${g.fx}" cy="${g.wheelY}" r="${g.r+11}" fill="#1b1d21"/><circle cx="${g.rx}" cy="${g.wheelY}" r="${g.r+11}" fill="#1b1d21"/>`);
  s.push(`<rect x="${g.x0-2}" y="${g.botY-36}" width="70" height="26" rx="6" fill="#2a2d33"/><rect x="${g.xr-46}" y="${g.botY-30}" width="50" height="20" rx="5" fill="#2a2d33"/>`);
  s.push(`</g>`);
  // windscreen edge + side window
  s.push(`<polygon points="${g.x0+g.wsX+3},${g.wsY-1} ${g.wsTopX+3},${g.wsTopY+3} ${g.wsTopX+12},${g.wsTopY+5} ${g.x0+g.wsX+13},${g.wsY-3}" fill="${glass}" clip-path="url(#${id}c)"/>`);
  s.push(`<polygon points="${g.win.map(p=>p[0].toFixed(1)+','+p[1].toFixed(1)).join(' ')}" fill="${glass}"/>`);
  s.push(`<polygon points="${(g.win[1][0]+8).toFixed(1)},${(g.win[1][1]+6).toFixed(1)} ${(g.win[1][0]+40).toFixed(1)},${(g.win[1][1]+6).toFixed(1)} ${(g.win[0][0]+30).toFixed(1)},${(g.win[0][1]-6).toFixed(1)} ${(g.win[0][0]+8).toFixed(1)},${(g.win[0][1]-6).toFixed(1)}" fill="#fff" opacity=".08"/>`);
  // mirror, handle, lights
  if(!opts.bare) s.push(`<path d="M${g.win[0][0]-6} ${g.win[0][1]-30} l-22 -4 l-4 26 l24 4 z" fill="#1f2226"/>`);
  s.push(`<rect x="${g.doorX-40}" y="${g.wsY+22}" width="24" height="7" rx="3.5" fill="#000" opacity=".35"/>`);
  s.push(`<path d="M${g.x0+2} ${g.noseY-6} q16 -20 40 -22 l2 18 q-22 2 -42 12 z" fill="#e9eef3" stroke="#9aa3ad"/>`);
  s.push(`<rect x="${g.xr-10}" y="${g.roofY+40}" width="10" height="${Math.min(70,g.botY-g.roofY-120)}" rx="3" fill="#b4232c" opacity=".9"/>`);
  if(!opts.bare) s.push(wheel(g.fx)+wheel(g.rx));
  if(opts.flip){ s.splice(1,0,`<g transform="matrix(-1 0 0 1 ${VW} 0)">`); s.push('</g>'); }
  s.push(`</svg>`);
  return s.join('');
}

/* ---------- lifestyle scenes (illustrated; live site swaps in AI photo-real) ---------- */
const SCENES=[['motorway','Motorway'],['city','City street'],['site','On the job'],['country','Country lane'],['coast','Coast'],['night','Night']];
function renderScene(st,opts,scene){
  const SW=1100, SH=640, gy=575, K=0.74; // van ground line and scale in scene
  const van=renderVan(st,Object.assign({},opts,{noFloor:true})).replace('<svg ','<svg x="'+((SW-SW*K)/2)+'" y="'+(gy-GROUND*K)+'" width="'+(SW*K)+'" height="'+(VH*K)+'" ');
  let bg='', fg='', refl='';
  const sky=(a,b)=>`<defs><linearGradient id="sk" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient></defs><rect width="${SW}" height="${SH}" fill="url(#sk)"/>`;
  const dashes=(y,c,w)=>Array.from({length:12},(_,i)=>`<rect x="${i*100-20}" y="${y}" width="${w||55}" height="6" fill="${c}"/>`).join('');
  if(scene==='motorway'){
    bg=sky('#8ec5f0','#dbeefb')+`<path d="M0 470 Q200 440 420 462 T820 455 T1100 462 V520 H0Z" fill="#9cc57a"/><path d="M0 495 Q300 480 600 492 T1100 488 V530 H0Z" fill="#7fb062"/>`+
      `<rect y="505" width="${SW}" height="14" fill="#9aa0a6"/><rect y="508" width="${SW}" height="3" fill="#d6d9dc"/>`+Array.from({length:23},(_,i)=>`<rect x="${i*50}" y="497" width="4" height="22" fill="#7d8389"/>`).join('')+
      `<rect y="519" width="${SW}" height="${SH-519}" fill="#4b4f55"/>`+dashes(540,'#f2f2f2')+`<rect y="614" width="${SW}" height="6" fill="#f2f2f2"/>`;
    fg=Array.from({length:7},(_,i)=>`<rect x="${-40+i*14}" y="${300+i*34}" width="${140-i*10}" height="3" rx="1.5" fill="#fff" opacity=".55"/>`).join('');
  } else if(scene==='city'){
    bg=sky('#a9cbe6','#e8f1f8');
    const cols=['#c9a27e','#b5654a','#e2d6c2','#8d6e63','#d7b98e','#a9a9a9','#c46a4c'];
    let x=-10; let i=0; while(x<SW){ const w=120+((i*53)%70), h=250+((i*71)%130), c=cols[i%cols.length]; bg+=`<rect x="${x}" y="${530-h}" width="${w}" height="${h}" fill="${c}"/>`; for(let r=0;r<Math.floor((h-80)/55);r++){ for(let k=0;k<Math.floor((w-20)/38);k++){ bg+=`<rect x="${x+16+k*38}" y="${530-h+20+r*55}" width="22" height="32" fill="#2f3b47" opacity=".75"/>`; } } bg+=`<rect x="${x}" y="${470}" width="${w}" height="60" fill="${i%2?'#2d4a3e':'#6b2d2d'}" opacity=".85"/>`; x+=w; i++; }
    bg+=`<rect y="528" width="${SW}" height="22" fill="#c9c6bf"/><rect y="548" width="${SW}" height="6" fill="#8f8c86"/><rect y="554" width="${SW}" height="${SH-554}" fill="#55595e"/>`+dashes(600,'#e8e8e8',40);
  } else if(scene==='site'){
    bg=sky('#b9d6ee','#eef5fb')+`<rect x="560" y="250" width="420" height="290" fill="#b4573f"/>`+Array.from({length:14},(_,r)=>`<line x1="560" y1="${265+r*20}" x2="980" y2="${265+r*20}" stroke="#9a4834" stroke-width="2"/>`).join('')+
      `<polygon points="540,250 770,140 1000,250" fill="#5a5f66"/><rect x="640" y="330" width="70" height="90" fill="#2f3b47"/><rect x="820" y="330" width="70" height="90" fill="#2f3b47"/>`+
      [520,620,720,820,920,1020].map(x=>`<line x1="${x}" y1="200" x2="${x}" y2="540" stroke="#9aa3ad" stroke-width="6"/>`).join('')+[230,330,430].map(y=>`<line x1="510" y1="${y}" x2="1030" y2="${y}" stroke="#9aa3ad" stroke-width="6"/><rect x="510" y="${y-8}" width="520" height="8" fill="#c9a26b"/>`).join('')+
      `<rect y="530" width="${SW}" height="${SH-530}" fill="#8a8173"/><rect y="530" width="${SW}" height="10" fill="#6f675b"/>`;
    fg=[90,1010].map(x=>`<polygon points="${x},${gy+2} ${x+18},${gy-46} ${x+36},${gy+2}" fill="#f26b1d"/><rect x="${x+8}" y="${gy-26}" width="20" height="7" fill="#fff"/>`).join('');
  } else if(scene==='country'){
    bg=sky('#9fd0f5','#eaf6ff')+`<path d="M0 420 Q250 350 520 410 T1100 390 V560 H0Z" fill="#a8cf86"/><path d="M0 460 Q300 410 640 455 T1100 440 V560 H0Z" fill="#86b866"/>`+
      Array.from({length:9},(_,i)=>`<circle cx="${60+i*130}" cy="${505-((i*37)%25)}" r="${44+((i*13)%18)}" fill="#4f7d3a"/>`).join('')+`<rect y="512" width="${SW}" height="30" fill="#4f7d3a"/>`+
      `<rect y="540" width="${SW}" height="${SH-540}" fill="#6f6a62"/><rect y="540" width="${SW}" height="8" fill="#5c7a3f"/>`;
  } else if(scene==='coast'){
    bg=sky('#7fc2ef','#e3f3fd')+`<rect y="400" width="${SW}" height="110" fill="#2f86b8"/>`+Array.from({length:10},(_,i)=>`<path d="M${i*120} ${430+(i%3)*22} q30 -8 60 0" stroke="#fff" stroke-width="3" fill="none" opacity=".6"/>`).join('')+
      `<rect y="500" width="${SW}" height="30" fill="#e8d4a6"/><rect y="490" width="${SW}" height="6" fill="#d9dde1"/>`+Array.from({length:23},(_,i)=>`<rect x="${i*50}" y="470" width="5" height="26" fill="#d9dde1"/>`).join('')+`<rect y="470" width="${SW}" height="5" fill="#d9dde1"/>`+
      `<rect y="530" width="${SW}" height="${SH-530}" fill="#6d7177"/>`+Array.from({length:6},(_,i)=>`<rect x="${i*200}" y="600" width="6" height="40" fill="#f2f2f2"/>`).join('');
  } else if(scene==='night'){
    bg=sky('#0b1020','#1e2a44')+Array.from({length:40},(_,i)=>`<circle cx="${(i*97)%SW}" cy="${(i*53)%300}" r="${i%3?1:1.6}" fill="#fff" opacity=".7"/>`).join('')+
      `<rect y="380" width="${SW}" height="160" fill="#141a2b"/>`+Array.from({length:14},(_,i)=>`<rect x="${i*80+10}" y="${400+(i%4)*20}" width="14" height="18" fill="#f7d774" opacity="${i%3?'.5':'.85'}"/>`).join('')+
      [150,550,950].map(x=>`<rect x="${x}" y="300" width="8" height="240" fill="#3a4152"/><rect x="${x-30}" y="296" width="44" height="8" rx="4" fill="#3a4152"/><circle cx="${x-24}" cy="306" r="70" fill="#ffd27a" opacity=".12"/><ellipse cx="${x-24}" cy="${gy+20}" rx="120" ry="18" fill="#ffd27a" opacity=".12"/>`).join('')+
      `<rect y="540" width="${SW}" height="${SH-540}" fill="#1b1f27"/>`+dashes(600,'#9aa0a6',40);
    refl=renderVan(st,Object.assign({},opts,{noFloor:true})).replace('<svg ','<svg x="'+((SW-SW*K)/2)+'" y="'+(gy-GROUND*K)+'" width="'+(SW*K)+'" height="'+(VH*K)+'" ');
    refl=`<g transform="translate(0 ${2*gy}) scale(1 -1)" opacity=".18">${refl}</g>`;
    fg=`<rect width="${SW}" height="${SH}" fill="#0b1020" opacity=".28"/>`+Array.from({length:30},(_,i)=>`<line x1="${(i*41)%SW}" y1="${(i*67)%SH}" x2="${(i*41)%SW-6}" y2="${(i*67)%SH+18}" stroke="#cfd8e6" stroke-width="1.2" opacity=".35"/>`).join('');
  }
  return `<svg viewBox="0 0 ${SW} ${SH}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Lifestyle view: ${esc(scene)}">${bg}${refl}${van}${fg}</svg>`;
}
function fillScenes(){
  const el=$('#scenes'); const on=S.view==='life';
  el.classList.toggle('hidden',!on);
  if(!on) return;
  el.innerHTML='<span class="lbl">Scene</span>'+SCENES.map(([k,n])=>`<button type="button" class="chip${S.scene===k?' on':''}" data-scene="${k}">${n}</button>`).join('')+'<span class="scene-note">Illustrated preview. On the live site this becomes a photo-real image of your van in the scene.</span>';
  el.querySelectorAll('[data-scene]').forEach(b=>b.addEventListener('click',()=>{ S.scene=b.dataset.scene; saveState(); renderPreview(); }));
}
document.querySelectorAll('.viewtoggle button').forEach(b=>b.addEventListener('click',()=>{ S.view=b.dataset.view; saveState(); renderPreview(); if(session) track({event:'view_'+S.view}); if(S.view==='360') apiEvent('view_360'); if(S.view==='lifestyle') apiEvent('lifestyle_view'); }));


/* ---------- home demo animation ---------- */
const NAME_A=['Brightspark','Greenleaf','Flowright','Topnotch','Swiftline','Clearview','Ironside','Bluebell','Redwood','Silverline','Oakridge','Sparkle','Hedgehog','Firefly','Bramble','Copperpot','Tidewell','Hilltop','Pebble','Wildfern','Lionheart','Quickfix','Truecut','Sunbeam'];
const NAME_B=['','','','& Sons','& Co','Pro'];
const TRADE_DEMOS=[
  {t:'Plumbing',tag:'Heating, boilers & bathrooms',svc:['Plumbing','Heating','Boilers','Bathrooms']},
  {t:'Electrical',tag:'Domestic & commercial electricians',svc:['Rewires','EV Chargers','Fuse Boards','Lighting']},
  {t:'Gardens',tag:'Garden design & landscaping',svc:['Patios','Fencing','Turfing','Decking']},
  {t:'Cleaning',tag:'Homes, offices & end of tenancy',svc:['Domestic','Commercial','Carpets','Windows']},
  {t:'Roofing',tag:'New roofs, repairs & guttering',svc:['New Roofs','Repairs','Flat Roofs','Guttering']},
  {t:'Removals',tag:'House & office moves made easy',svc:['House Moves','Office Moves','Packing','Storage']},
  {t:'Building',tag:'Extensions, renovations & more',svc:['Extensions','Renovations','Lofts','Brickwork']},
  {t:'Dog Grooming',tag:'Mobile grooming at your door',svc:['Full Groom','Bath & Brush','Nail Trims','Puppy Care']},
  {t:'Joinery',tag:'Bespoke kitchens & carpentry',svc:['Kitchens','Doors','Staircases','Fitted Furniture']},
  {t:'Pest Control',tag:'Fast, discreet pest control',svc:['Wasps','Rodents','Birds','Insects']}
];
const PALETTES=[['#0b4fb3','#ffcc00'],['#f2b705','#111318'],['#1f7a3a','#a3e635'],['#e11d48','#ffffff'],['#7c3aed','#f5d0fe'],['#0f766e','#fbbf24'],['#111318','#f97316'],['#b91c1c','#fde68a'],['#0369a1','#7dd3fc'],['#4d7c0f','#fef08a']];
const DEMO_VANS=[['Ford','Transit Custom','medium',false],['Mercedes-Benz','Sprinter','large',true],['Volkswagen','Transporter','medium',false],['Citroën','Berlingo','small',false],['Renault','Trafic','medium',true],['Vauxhall','Vivaro','medium',false],['Ford','Transit','large',false],['Peugeot','Partner','small',false]];
const BODIES=['#f3f4f6','#f3f4f6','#f3f4f6','#16181c','#c2c6cc'];
const pick=a=>a[Math.floor(Math.random()*a.length)];
let lastName='';
function randomDemo(){
  let name; do{ const tr=pick(TRADE_DEMOS); const b=pick(NAME_B); name={tr, co:(pick(NAME_A)+' '+tr.t+(b?' '+b:'')).replace(/\s+/g,' ').trim()}; } while(name.co===lastName);
  lastName=name.co;
  const v=pick(DEMO_VANS), pal=pick(PALETTES), mode=Math.random()<.5?'graphics':'wrap';
  const slug=name.co.toLowerCase().replace(/&/g,'and').replace(/[^a-z0-9]+/g,'');
  const num='01632 960 '+String(Math.floor(Math.random()*1000)).padStart(3,'0');
  return {mode,layout:Math.floor(Math.random()*3),make:v[0],model:v[1],size:v[2],lwb:v[3],body:mode==='graphics'?pick(BODIES):'#f3f4f6',P:pal[0],S:pal[1],
    company:name.co,tagline:name.tr.tag,phone:num,web:'www.'+slug.slice(0,22)+'.co.uk',services:name.tr.svc,trust:pick([['Free Quotes','Fully Insured'],['24/7 Callouts','Fully Insured'],['Family Run','Free Quotes'],['No Job Too Small']])};
}
let plainPhase=true, demoCur=null;
function demoTick(){
  if(!demoCur) demoCur=randomDemo();
  const d=Object.assign({},DEFAULT,demoCur,{show:Object.assign({},DEFAULT.show),logo:null});
  if(plainPhase){ $('#nvgDemo').innerHTML=renderVan(d,{design:false,floor:'rgba(255,255,255,.04)'}); (document.getElementById('demoName')||{}).textContent='Plain '+d.make+' '+d.model; }
  else { $('#nvgDemo').innerHTML=renderVan(d,{design:true,layout:d.layout,floor:'rgba(255,255,255,.04)'}); (document.getElementById('demoName')||{}).textContent=(d.mode==='wrap'?'Full wrap':'Graphics')+' · '+d.company; demoCur=randomDemo(); }
  plainPhase=!plainPhase;
}
function gateArt(){ const d=Object.assign({},DEFAULT,randomDemo(),{mode:'wrap',show:Object.assign({},DEFAULT.show),logo:null}); $('#gateSvg').innerHTML=renderVan(d,{design:true,layout:d.layout,floor:'rgba(255,255,255,.04)'}); }


if(document.getElementById('nvgDemo')){ demoTick(); const t=setInterval(demoTick,2400); }
if(!document.getElementById('nvg-designer')) return;
/* ---------- 360 viewer (WebGL, no libraries) ---------- */
const V3={gl:null,prog:null,loc:{},meshes:[],tex:{},yaw:-0.75,pitch:0.16,zoom:1,auto:true,raf:0,geoKey:'',seq:0,failed:false,idle:0};
const M4={
  persp(f,a,n,fa){ const t=1/Math.tan(f/2); return [t/a,0,0,0, 0,t,0,0, 0,0,(fa+n)/(n-fa),-1, 0,0,2*fa*n/(n-fa),0]; },
  look(e,c,u){ const sub=(a,b)=>[a[0]-b[0],a[1]-b[1],a[2]-b[2]], nrm=v=>{const l=Math.hypot(v[0],v[1],v[2])||1;return [v[0]/l,v[1]/l,v[2]/l];}, cr=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]], dt=(a,b)=>a[0]*b[0]+a[1]*b[1]+a[2]*b[2];
    const z=nrm(sub(e,c)), x=nrm(cr(u,z)), y=cr(z,x); return [x[0],y[0],z[0],0, x[1],y[1],z[1],0, x[2],y[2],z[2],0, -dt(x,e),-dt(y,e),-dt(z,e),1]; },
  mul(a,b){ const o=new Array(16); for(let c=0;c<4;c++) for(let r=0;r<4;r++){ let v=0; for(let k=0;k<4;k++) v+=a[k*4+r]*b[c*4+k]; o[c*4+r]=v; } return o; }
};
function v3Init(){
  if(V3.gl||V3.failed) return !!V3.gl;
  const cv=$('#gl'); let gl=null;
  try{ gl=cv.getContext('webgl',{antialias:true,preserveDrawingBuffer:true,alpha:true}); }catch(e){}
  if(!gl){ V3.failed=true; return false; }
  const vs=`attribute vec3 p;attribute vec3 n;attribute vec2 uv;uniform mat4 mvp;varying vec3 vn;varying vec2 vuv;varying vec3 vp;void main(){vn=n;vuv=uv;vp=p;gl_Position=mvp*vec4(p,1.0);}`;
  const fs=`precision mediump float;varying vec3 vn;varying vec2 vuv;varying vec3 vp;uniform sampler2D t;uniform vec4 col;uniform float mode;uniform vec3 eye;
  void main(){
    if(mode>1.5){ float d=length((vuv-vec2(0.5))*vec2(1.0,1.0)); float a=smoothstep(0.5,0.05,d)*0.42; gl_FragColor=vec4(0.0,0.0,0.0,a); return; }
    vec4 base = mode>0.5 ? texture2D(t,vuv) : col;
    vec3 N=normalize(vn); vec3 V=normalize(eye-vp); if(dot(N,V)<0.0) N=-N;
    vec3 L=normalize(vec3(0.35,0.9,0.55)); vec3 L2=normalize(vec3(-0.6,0.35,-0.45));
    float diff=0.42+max(dot(N,L),0.0)*0.55+max(dot(N,L2),0.0)*0.22;
    vec3 H=normalize(L+V); float spec=pow(max(dot(N,H),0.0),48.0)*0.28*col.a;
    gl_FragColor=vec4(min(base.rgb*diff+spec,1.0),1.0);
  }`;
  const sh=(type,src)=>{ const o=gl.createShader(type); gl.shaderSource(o,src); gl.compileShader(o); if(!gl.getShaderParameter(o,gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(o)); return o; };
  try{
    const pr=gl.createProgram(); gl.attachShader(pr,sh(gl.VERTEX_SHADER,vs)); gl.attachShader(pr,sh(gl.FRAGMENT_SHADER,fs)); gl.linkProgram(pr);
    if(!gl.getProgramParameter(pr,gl.LINK_STATUS)) throw new Error('link');
    V3.prog=pr; gl.useProgram(pr);
    ['p','n','uv'].forEach(k=>V3.loc[k]=gl.getAttribLocation(pr,k));
    ['mvp','t','col','mode','eye'].forEach(k=>V3.loc[k]=gl.getUniformLocation(pr,k));
  }catch(e){ V3.failed=true; return false; }
  gl.enable(gl.DEPTH_TEST); gl.enable(gl.BLEND); gl.blendFunc(gl.SRC_ALPHA,gl.ONE_MINUS_SRC_ALPHA);
  V3.gl=gl;
  // interaction
  let drag=null, pinch=null; const pts=new Map();
  cv.addEventListener('pointerdown',e=>{ cv.setPointerCapture(e.pointerId); pts.set(e.pointerId,[e.clientX,e.clientY]); drag=[e.clientX,e.clientY,V3.yaw,V3.pitch]; setAuto(false); });
  cv.addEventListener('pointermove',e=>{
    if(!pts.has(e.pointerId)) return; pts.set(e.pointerId,[e.clientX,e.clientY]);
    if(pts.size===2){ const [a,b]=[...pts.values()]; const d=Math.hypot(a[0]-b[0],a[1]-b[1]); if(pinch) V3.zoom=Math.max(.6,Math.min(1.6,pinch[1]*pinch[0]/d)); else pinch=[d,V3.zoom]; return; }
    if(!drag) return; const w=cv.clientWidth||600;
    V3.yaw=drag[2]-(e.clientX-drag[0])/w*Math.PI*1.6;
    V3.pitch=Math.max(0.02,Math.min(0.75,drag[3]+(e.clientY-drag[1])/w*1.6));
  });
  const end=e=>{ pts.delete(e.pointerId); if(pts.size<2) pinch=null; if(!pts.size) drag=null; };
  cv.addEventListener('pointerup',end); cv.addEventListener('pointercancel',end);
  cv.addEventListener('wheel',e=>{ e.preventDefault(); V3.zoom=Math.max(.6,Math.min(1.6,V3.zoom*(e.deltaY>0?1.08:0.92))); },{passive:false});
  return true;
}
function setAuto(on){ V3.auto=on; $('#spin360').classList.toggle('paused',!on); }
$('#spin360').addEventListener('click',()=>setAuto(!V3.auto));

function hex3(h){ return hex2rgb(h).map(v=>v/255); }
function perimColour(st){ if(st.mode!=='wrap'||!st.designed) return st.body; return st.layout===2? mix(st.P,'#0b0c0f',.78) : st.P; }
function outline(g){
  const P=[]; const add=(x,y,tag)=>P.push({x,y,tag});
  const q=(x0,y0,cx,cy,x1,y1,tag,n)=>{ for(let i=1;i<=n;i++){ const t=i/n, a=(1-t)*(1-t), b=2*(1-t)*t, c=t*t; add(a*x0+b*cx+c*x1, a*y0+b*cy+c*y1, tag); } };
  const x0=g.x0, xr=g.xr;
  add(x0+12,g.botY,'bottom');
  add(x0,g.botY-18,'front'); add(x0,g.noseY,'front');
  q(x0,g.noseY,x0,g.noseY-26,x0+32,g.noseY-32,'nose',6);
  add(x0+g.wsX,g.wsY,'bonnet'); add(g.wsTopX,g.wsTopY,'ws');
  q(g.wsTopX,g.wsTopY,x0+g.rsX,g.roofY,x0+g.rsX+34,g.roofY,'roof',6);
  add(xr-16,g.roofY,'roof');
  q(xr-16,g.roofY,xr,g.roofY,xr,g.roofY+16,'roof',5);
  add(xr,g.botY-12,'rear');
  q(xr,g.botY-12,xr,g.botY,xr-12,g.botY,'bottom',4);
  P.push({x:x0+12,y:g.botY,tag:'bottom'});
  return P;
}
function v3BuildMeshes(st){
  const g=geom(st.size,st.lwb); const S3=1/100; const hw=g.len*S3*0.2;
  const X=x=>(x-VW/2)*S3, Y=y=>(GROUND-y)*S3;
  const meshes=[]; const mk=(mat)=>{ const m={p:[],n:[],uv:[],mat}; meshes.push(m); return m; };
  const tri=(m,a,b,c)=>{ for(const v of [a,b,c]){ m.p.push(v.p[0],v.p[1],v.p[2]); m.n.push(v.n[0],v.n[1],v.n[2]); m.uv.push(v.uv[0],v.uv[1]); } };
  const quad=(m,a,b,c,d)=>{ tri(m,a,b,c); tri(m,a,c,d); };
  const P=outline(g);
  // side caps (convex profile -> fan)
  const cx=P.reduce((s,p)=>s+p.x,0)/P.length, cy=P.reduce((s,p)=>s+p.y,0)/P.length;
  const left=mk({tex:'L'}), right=mk({tex:'R'});
  for(let i=0;i<P.length-1;i++){
    const a=P[i], b=P[i+1];
    for(const [m,z,nz,flip] of [[left,hw,1,false],[right,-hw,-1,true]]){
      const uv=p=>[flip?(VW-p.x)/VW:p.x/VW, p.y/VH];
      tri(m,{p:[X(cx),Y(cy),z],n:[0,0,nz],uv:uv({x:cx,y:cy})},{p:[X(a.x),Y(a.y),z],n:[0,0,nz],uv:uv(a)},{p:[X(b.x),Y(b.y),z],n:[0,0,nz],uv:uv(b)});
    }
  }
  // perimeter strips
  const pc=perimColour(st);
  const body=mk({col:hex3(pc),spec:1}), dark=mk({col:[.12,.13,.15],spec:0}), glass=mk({col:[.13,.17,.22],spec:1});
  const rear=mk({tex:'B'}), front=mk({tex:'F'});
  for(let i=0;i<P.length-1;i++){
    const a=P[i], b=P[i+1], tag=b.tag;
    const dx=X(b.x)-X(a.x), dy=Y(b.y)-Y(a.y), l=Math.hypot(dx,dy)||1, n=[-dy/l,dx/l,0];
    const V=(p,z,uv)=>({p:[X(p.x),Y(p.y),z],n,uv:uv||[0,0]});
    if(tag==='ws'){
      const pz=hw*0.86;
      quad(body,V(a,hw),V(b,hw),V(b,pz),V(a,pz)); quad(body,V(a,-pz),V(b,-pz),V(b,-hw),V(a,-hw));
      quad(glass,V(a,pz),V(b,pz),V(b,-pz),V(a,-pz));
    } else if(tag==='rear'){
      const vt=g.roofY+16, vb=g.botY-12, v=p=>(p.y-vt)/(vb-vt);
      quad(rear,V(a,hw,[0,v(a)]),V(b,hw,[0,v(b)]),V(b,-hw,[1,v(b)]),V(a,-hw,[1,v(a)]));
    } else if(tag==='front'){
      const vt=g.noseY, vb=g.botY, v=p=>(p.y-vt)/(vb-vt);
      quad(front,V(a,hw,[1,v(a)]),V(b,hw,[1,v(b)]),V(b,-hw,[0,v(b)]),V(a,-hw,[0,v(a)]));
    } else {
      quad(tag==='bottom'?dark:body,V(a,hw),V(b,hw),V(b,-hw),V(a,-hw));
    }
  }
  // wheels
  const tyre=mk({col:[.07,.075,.085],spec:0}), rim=mk({col:[.68,.71,.75],spec:1}), hub=mk({col:[.33,.35,.38],spec:1});
  const r=g.r*S3, wy=g.r*S3, ww=0.44, seg=28;
  for(const wx of [X(g.fx),X(g.rx)]) for(const side of [1,-1]){
    const zo=side*(hw+0.02), zi=side*(hw-ww+0.02);
    for(let k=0;k<seg;k++){
      const t0=k/seg*Math.PI*2, t1=(k+1)/seg*Math.PI*2, c0=Math.cos(t0), s0=Math.sin(t0), c1=Math.cos(t1), s1=Math.sin(t1);
      quad(tyre,{p:[wx+c0*r,wy+s0*r,zo],n:[c0,s0,0],uv:[0,0]},{p:[wx+c1*r,wy+s1*r,zo],n:[c1,s1,0],uv:[0,0]},{p:[wx+c1*r,wy+s1*r,zi],n:[c1,s1,0],uv:[0,0]},{p:[wx+c0*r,wy+s0*r,zi],n:[c0,s0,0],uv:[0,0]});
      const disc=(m,rad,z)=>tri(m,{p:[wx,wy,z],n:[0,0,side],uv:[0,0]},{p:[wx+c0*rad,wy+s0*rad,z],n:[0,0,side],uv:[0,0]},{p:[wx+c1*rad,wy+s1*rad,z],n:[0,0,side],uv:[0,0]});
      const ring=(m,r0,r1,z)=>quad(m,{p:[wx+c0*r0,wy+s0*r0,z],n:[0,0,side],uv:[0,0]},{p:[wx+c1*r0,wy+s1*r0,z],n:[0,0,side],uv:[0,0]},{p:[wx+c1*r1,wy+s1*r1,z],n:[0,0,side],uv:[0,0]},{p:[wx+c0*r1,wy+s0*r1,z],n:[0,0,side],uv:[0,0]});
      ring(tyre,r*0.62,r,zo); disc(rim,r*0.62,zo+side*0.004); disc(hub,r*0.16,zo+side*0.008); disc(tyre,r,zi);
    }
  }
  // soft shadow
  const sm=mk({shadow:true}); const sx=g.len*S3*0.62, sz=hw*1.9;
  quad(sm,{p:[-sx,0.003,-sz],n:[0,1,0],uv:[0,0]},{p:[sx,0.003,-sz],n:[0,1,0],uv:[1,0]},{p:[sx,0.003,sz],n:[0,1,0],uv:[1,1]},{p:[-sx,0.003,sz],n:[0,1,0],uv:[0,1]});
  const gl=V3.gl;
  V3.meshes.forEach(m=>{ ['bp','bn','bu'].forEach(k=>m[k]&&gl.deleteBuffer(m[k])); });
  meshes.forEach(m=>{ m.count=m.p.length/3; const buf=a=>{ const b=gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER,b); gl.bufferData(gl.ARRAY_BUFFER,new Float32Array(a),gl.STATIC_DRAW); return b; }; m.bp=buf(m.p); m.bn=buf(m.n); m.bu=buf(m.uv); });
  V3.meshes=meshes; V3.height=(GROUND-g.roofY)*S3; V3.len=g.len*S3;
}
function loadImg(src){ return new Promise((res,rej)=>{ const i=new Image(); i.onload=()=>res(i); i.onerror=rej; i.src=src; }); }
async function svgToCanvas(svg,w,h){
  const s2=svg.replace('<svg ','<svg width="'+w+'" height="'+h+'" preserveAspectRatio="none" ');
  const url=URL.createObjectURL(new Blob([s2],{type:'image/svg+xml'}));
  try{ const img=await loadImg(url); const c=document.createElement('canvas'); c.width=w; c.height=h; c.getContext('2d').drawImage(img,0,0,w,h); return c; }
  finally{ URL.revokeObjectURL(url); }
}
async function rearCanvas(st){
  const c=document.createElement('canvas'); c.width=1024; c.height=1024; const x=c.getContext('2d');
  const pc=perimColour(st); x.fillStyle=pc; x.fillRect(0,0,1024,1024);
  x.fillStyle='rgba(0,0,0,.18)'; x.fillRect(509,0,6,1024);
  x.fillStyle='#1d252e'; x.fillRect(90,70,390,250); x.fillRect(544,70,390,250);
  const I=info(st), ink=st.designed? (st.mode==='wrap'? contrastText(pc) : graphicsInk(st)) : 'rgba(0,0,0,0)';
  if(st.designed){
    if(st.logo){ try{ const im=await loadImg(st.logo); const ar=im.width/im.height||1; let w=420,h=w/ar; if(h>200){h=200;w=h*ar;} if(st.mode==='wrap'){ x.fillStyle='#fff'; x.beginPath(); x.roundRect? x.roundRect(512-w/2-18,395-h/2-18,w+36,h+36,22) : x.rect(512-w/2-18,395-h/2-18,w+36,h+36); x.fill(); } x.drawImage(im,512-w/2,395-h/2,w,h); }catch(e){} }
    else { x.fillStyle=st.P; x.beginPath(); x.arc(512,395,95,0,Math.PI*2); x.fill(); x.fillStyle=contrastText(st.P); x.font='900 92px "Archivo Black", Arial Black, sans-serif'; x.textAlign='center'; x.textBaseline='middle'; x.fillText(initials(st.company),512,400); }
    x.fillStyle=ink; x.textAlign='center'; x.textBaseline='alphabetic';
    const fitTxt=(t,max,sz,f)=>{ let s=sz; x.font=f.replace('{s}',s); while(s>18&&x.measureText(t).width>max){ s-=2; x.font=f.replace('{s}',s); } };
    if(I.name){ fitTxt(I.name,860,84,'900 {s}px "Archivo Black", Arial Black, sans-serif'); x.fillText(I.name,512,610); }
    if(I.phone){ fitTxt(I.phone,860,96,'900 {s}px "Archivo Black", Arial Black, sans-serif'); x.fillText(I.phone,512,740); }
    if(I.web){ fitTxt(I.web,860,48,'700 {s}px Archivo, Arial, sans-serif'); x.fillText(I.web,512,830); }
  }
  x.fillStyle='#b4232c'; x.fillRect(14,140,34,260); x.fillRect(976,140,34,260);
  x.fillStyle='#2a2d33'; x.fillRect(0,930,1024,94);
  x.fillStyle='#ffd21f'; x.fillRect(372,946,280,62); x.fillStyle='#111'; x.font='800 40px Archivo, Arial, sans-serif'; x.textAlign='center'; x.fillText(st.reg||'',512,992);
  return c;
}
function frontCanvas(st){
  const c=document.createElement('canvas'); c.width=512; c.height=256; const x=c.getContext('2d');
  x.fillStyle=perimColour(st); x.fillRect(0,0,512,256);
  x.fillStyle='#1b1d21'; x.fillRect(130,30,252,95);
  x.fillStyle='#e9eef3'; x.fillRect(16,26,96,52); x.fillRect(400,26,96,52);
  x.fillStyle='#2a2d33'; x.fillRect(0,165,512,91);
  x.fillStyle='#ffffff'; x.fillRect(176,180,160,44); x.fillStyle='#111'; x.font='800 26px Archivo, Arial, sans-serif'; x.textAlign='center'; x.fillText(st.reg||'',256,211);
  return c;
}
function upload(name,canvas){
  const gl=V3.gl; let t=V3.tex[name]; if(!t){ t=gl.createTexture(); V3.tex[name]=t; }
  gl.bindTexture(gl.TEXTURE_2D,t); gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL,false);
  gl.texImage2D(gl.TEXTURE_2D,0,gl.RGBA,gl.RGBA,gl.UNSIGNED_BYTE,canvas);
  gl.generateMipmap(gl.TEXTURE_2D);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR_MIPMAP_LINEAR); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
  gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
}
let v3T=null;
function v3Update(){
  if(!v3Init()){ $('#hint360').textContent='3D view isn\'t supported on this device'; return; }
  clearTimeout(v3T); v3T=setTimeout(async()=>{
    const my=++V3.seq, st=Object.assign({},S);
    const key=st.size+'|'+st.lwb+'|'+perimColour(st);
    if(key!==V3.geoKey){ v3BuildMeshes(st); V3.geoKey=key; }
    try{
      const o={design:st.designed,layout:st.layout,noFloor:true,bare:true};
      const [L,R,B]=await Promise.all([svgToCanvas(renderVan(st,o),2048,1024),svgToCanvas(renderVan(st,Object.assign({},o,{flip:true})),2048,1024),rearCanvas(st)]);
      if(my!==V3.seq) return;
      upload('L',L); upload('R',R); upload('B',B); upload('F',frontCanvas(st));
    }catch(e){ console.warn('3D texture failed',e); }
    v3Loop();
  },120);
}
function v3Draw(){
  const gl=V3.gl, cv=$('#gl'); if(!gl||!V3.meshes.length) return;
  const dpr=Math.min(2,window.devicePixelRatio||1), w=Math.round(cv.clientWidth*dpr), h=Math.round(cv.clientHeight*dpr);
  if(!w||!h) return;
  if(cv.width!==w||cv.height!==h){ cv.width=w; cv.height=h; }
  gl.viewport(0,0,w,h); gl.clearColor(0,0,0,0); gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
  const tgt=[0,V3.height*0.42,0], d=V3.len*1.2*V3.zoom;
  const eye=[tgt[0]+d*Math.cos(V3.pitch)*Math.sin(V3.yaw), tgt[1]+d*Math.sin(V3.pitch), tgt[2]+d*Math.cos(V3.pitch)*Math.cos(V3.yaw)];
  const mvp=M4.mul(M4.persp(0.62,w/h,0.1,100),M4.look(eye,tgt,[0,1,0]));
  gl.uniformMatrix4fv(V3.loc.mvp,false,new Float32Array(mvp)); gl.uniform3fv(V3.loc.eye,eye); gl.uniform1i(V3.loc.t,0);
  const order=V3.meshes.filter(m=>!m.mat.shadow).concat(V3.meshes.filter(m=>m.mat.shadow));
  for(const m of order){
    if(!m.count) continue;
    const mode=m.mat.shadow?2:(m.mat.tex?1:0);
    if(mode===1){ const t=V3.tex[m.mat.tex]; if(!t) continue; gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D,t); }
    gl.uniform1f(V3.loc.mode,mode); const c=m.mat.col||[1,1,1]; gl.uniform4f(V3.loc.col,c[0],c[1],c[2],mode===1?1:(m.mat.spec?1:0));
    if(m.mat.shadow) gl.depthMask(false);
    [['bp','p',3],['bn','n',3],['bu','uv',2]].forEach(([b,a,sz])=>{ gl.bindBuffer(gl.ARRAY_BUFFER,m[b]); gl.enableVertexAttribArray(V3.loc[a]); gl.vertexAttribPointer(V3.loc[a],sz,gl.FLOAT,false,0,0); });
    gl.drawArrays(gl.TRIANGLES,0,m.count);
    if(m.mat.shadow) gl.depthMask(true);
  }
}
function v3Loop(){
  if(V3.raf) return;
  const step=()=>{ if(S.view!=='360'||$('#nvg-app').classList.contains('hidden')){ V3.raf=0; return; } if(V3.auto) V3.yaw+=0.005; v3Draw(); V3.raf=requestAnimationFrame(step); };
  V3.raf=requestAnimationFrame(step);
}
window.v3Debug=()=>V3;

/* ---------- designer inputs ---------- */
function saveState(){ const c=Object.assign({},S); if(c.logo && c.logo.length>1500000) c.logo=null; LS.set('nvg_state',c); if(typeof scheduleSave==='function') scheduleSave(); }
function fillMakes(){
  $('#make').innerHTML=Object.keys(VANS).map(m=>`<option${m===S.make?' selected':''}>${esc(m)}</option>`).join('');
  fillModels();
}
function fillModels(){
  const list=VANS[S.make]||[];
  if(!list.some(x=>x.split('|')[0]===S.model)){ const mid=list.find(x=>x.endsWith('|medium'))||list[0]; S.model=mid.split('|')[0]; }
  $('#model').innerHTML=list.map(x=>{const [n,sz]=x.split('|');return `<option value="${esc(n)}"${n===S.model?' selected':''}>${esc(n)} (${sz==='small'?'small':sz==='medium'?'medium':'large'})</option>`;}).join('');
  const hit=list.find(x=>x.split('|')[0]===S.model); S.size=hit?hit.split('|')[1]:'medium';
}
$('#make').addEventListener('change',e=>{ S.make=e.target.value; fillModels(); changed(); });
$('#model').addEventListener('change',e=>{ S.model=e.target.value; fillModels(); changed(); });
document.querySelectorAll('#wbSeg button').forEach(b=>b.addEventListener('click',()=>{ S.lwb=b.dataset.v==='lwb'; changed(); }));
$('#findReg').addEventListener('click',()=>{
  const v=$('#reg').value.toUpperCase().replace(/\s+/g,'');
  const n=$('#regNotice'); n.classList.remove('hidden');
  if(!/^[A-Z0-9]{2,7}$/.test(v)){ n.textContent='That doesn\'t look like a UK registration. Check it, or choose your make and model below.'; return; }
  S.reg=v.length===7? v.slice(0,4)+' '+v.slice(4) : v; $('#reg').value=S.reg;
  n.innerHTML='<b>Reg saved: '+esc(S.reg)+'.</b> Checking the DVLA record…';
  changed();
  regLookup(v).then(r=>{
    if(r && r.available && r.found && r.vehicle){
      const mk=Object.keys(VANS).find(m=>m.toLowerCase().replace(/[^a-z]/g,'')===String(r.vehicle.make||'').toLowerCase().replace(/[^a-z]/g,''));
      if(mk && mk!==S.make){ S.make=mk; const first=VANS[mk][0].split('|'); S.model=first[0]; S.size=first[1]; }
      const col=String(r.vehicle.colour||'').toLowerCase(); const hit=COLOURS.find(([nm])=>nm.toLowerCase()===col);
      if(hit){ S.body=hit[1]; S.bodyName=hit[0]; }
      n.innerHTML='<b>Found: '+esc(r.vehicle.colour||'')+' '+esc(r.vehicle.make||'')+(r.vehicle.yearOfManufacture?' ('+r.vehicle.yearOfManufacture+')':'')+'.</b> Now pick your exact model and wheelbase below.';
      changed();
    } else if(r && r.available && !r.found){
      n.innerHTML='<b>We couldn\'t find '+esc(S.reg)+'.</b> Check the reg, or choose your make, model and colour below.';
    } else {
      n.innerHTML='<b>Reg saved: '+esc(S.reg)+'.</b> Please choose your make, model and colour below. We\'ll check the exact vehicle before quoting.';
    }
  });
});
$('#reg').addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); $('#findReg').click(); } });
function fillSwatches(){
  $('#swatches').innerHTML=COLOURS.map(([n,c])=>`<button class="sw${S.body===c?' on':''}" title="${n}" aria-label="${n}" data-c="${c}" data-n="${n}" style="background:${c}"></button>`).join('')+`<label class="sw-custom" title="Custom colour"><input type="color" id="customBody" value="${S.body}"></label>`;
  document.querySelectorAll('#swatches .sw').forEach(b=>b.addEventListener('click',()=>{ S.body=b.dataset.c; S.bodyName=b.dataset.n; changed(); }));
  $('#customBody').addEventListener('input',e=>{ S.body=e.target.value; S.bodyName='Custom '+e.target.value.toUpperCase(); changed(); });
  $('#colourName').textContent='Selected: '+S.bodyName;
}
document.querySelectorAll('.style-opt').forEach(b=>b.addEventListener('click',()=>{ S.mode=b.dataset.mode; S.layout=0; changed(); }));
// logo
const drop=$('#drop');
['dragenter','dragover'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.add('over');}));
['dragleave','drop'].forEach(ev=>drop.addEventListener(ev,e=>{e.preventDefault();drop.classList.remove('over');}));
drop.addEventListener('drop',e=>{ const f=e.dataTransfer.files&&e.dataTransfer.files[0]; if(f) readLogo(f); });
$('#logoFile').addEventListener('change',e=>{ const f=e.target.files[0]; if(f) readLogo(f); e.target.value=''; });
function readLogo(f){
  if(!/^image\//.test(f.type)){ $('#colHint').textContent='Please upload an image file (PNG, JPG or SVG).'; return; }
  if(f.size>8*1024*1024){ $('#colHint').textContent='That file is over 8 MB. Please upload a smaller logo.'; return; }
  const rd=new FileReader();
  rd.onload=()=>{
    const img=new Image();
    img.onload=()=>{
      // downscale large rasters to keep things fast
      let url=rd.result, w=img.naturalWidth||400, h=img.naturalHeight||200;
      const c=document.createElement('canvas'); const max=900; const k=Math.min(1,max/Math.max(w,h));
      c.width=Math.max(1,Math.round(w*k)); c.height=Math.max(1,Math.round(h*k));
      const cx=c.getContext('2d'); cx.drawImage(img,0,0,c.width,c.height);
      if(f.type!=='image/svg+xml'){ try{ url=c.toDataURL('image/png'); }catch(e){} }
      S.logo=url; S.logoAR=w/h||1; apiEvent('logo_uploaded');
      const cols=extractColours(cx,c.width,c.height);
      if(cols){ S.P=cols[0]; S.S=cols[1]; $('#colHint').textContent='Brand colours picked from your logo. Change them any time.'; }
      else $('#colHint').textContent='Logo added. Pick your brand colours above.';
      changed();
    };
    img.onerror=()=>{ $('#colHint').textContent='We couldn\'t read that image. Try a PNG or JPG.'; };
    img.src=rd.result;
  };
  rd.readAsDataURL(f);
}
function extractColours(cx,w,h){
  let data; try{ data=cx.getImageData(0,0,w,h).data; }catch(e){ return null; }
  const buckets={}; const step=Math.max(1,Math.floor((w*h)/12000));
  for(let i=0;i<w*h;i+=step){
    const p=i*4, r=data[p],g=data[p+1],b=data[p+2],a=data[p+3];
    if(a<200) continue; const mx=Math.max(r,g,b), mn=Math.min(r,g,b);
    if(mn>232) continue; // near white
    const key=(r>>4)+','+(g>>4)+','+(b>>4);
    const o=buckets[key]||(buckets[key]={n:0,r:0,g:0,b:0,sat:mx-mn}); o.n++; o.r+=r;o.g+=g;o.b+=b;
  }
  const list=Object.values(buckets).map(o=>({hex:rgb2hex(o.r/o.n,o.g/o.n,o.b/o.n),n:o.n,sat:o.sat})).sort((a,b)=>(b.n*(1+b.sat/120))-(a.n*(1+a.sat/120)));
  if(!list.length) return null;
  const P=list[0].hex; const second=list.find(o=>dist(o.hex,P)>90);
  const Sx= second? second.hex : (lum(P)>0.4? '#111318' : '#ffcc00');
  return [P,Sx];
}
$('#removeLogo').addEventListener('click',()=>{ S.logo=null; $('#colHint').textContent='Logo removed.'; changed(); });
$('#cP').addEventListener('input',e=>{ S.P=e.target.value; changed(true); });
$('#cS').addEventListener('input',e=>{ S.S=e.target.value; changed(true); });
$('#swapCols').addEventListener('click',()=>{ const t=S.P; S.P=S.S; S.S=t; changed(); });
// fields
const FIELD_IDS={company:'#fCompany',tagline:'#fTagline',phone:'#fPhone',web:'#fWeb',email:'#fEmail',social:'#fSocial'};
Object.entries(FIELD_IDS).forEach(([k,sel])=>{ $(sel).addEventListener('input',e=>{ S[k]=e.target.value; changed(true); }); });
document.querySelectorAll('.field input[type=checkbox]').forEach(cb=>cb.addEventListener('change',()=>{ S.show[cb.dataset.k]=cb.checked; changed(); }));
function fillTrades(){
  $('#trade').innerHTML=Object.keys(TRADES).map(t=>`<option${t===S.trade?' selected':''}>${esc(t)}</option>`).join('');
}
$('#trade').addEventListener('change',e=>{ S.trade=e.target.value; S.services=(TRADES[S.trade]||[]).slice(0,4); changed(); });
function fillChips(){
  const pool=Array.from(new Set([...(TRADES[S.trade]||[]),...S.services]));
  $('#serviceChips').innerHTML=pool.map(s=>`<button type="button" class="chip${S.services.includes(s)?' on':''}" data-s="${esc(s)}">${esc(s)}</button>`).join('')||'<span class="muted" style="font-size:13px">Add your services below.</span>';
  document.querySelectorAll('#serviceChips .chip').forEach(b=>b.addEventListener('click',()=>{ const s=b.dataset.s; if(S.services.includes(s)) S.services=S.services.filter(x=>x!==s); else if(S.services.length<6) S.services=[...S.services,s]; changed(); }));
  $('#trustChips').innerHTML=TRUST.map(s=>`<button type="button" class="chip${S.trust.includes(s)?' on':''}" data-s="${esc(s)}">${esc(s)}</button>`).join('');
  document.querySelectorAll('#trustChips .chip').forEach(b=>b.addEventListener('click',()=>{ const s=b.dataset.s; if(S.trust.includes(s)) S.trust=S.trust.filter(x=>x!==s); else S.trust=[...S.trust,s].slice(-2); changed(); }));
}
$('#addSvc').addEventListener('click',()=>{ const v=$('#customSvc').value.trim(); if(!v) return; if(!S.services.includes(v)&&S.services.length<6) S.services=[...S.services,v]; $('#customSvc').value=''; changed(); });
$('#customSvc').addEventListener('keydown',e=>{ if(e.key==='Enter'){ e.preventDefault(); $('#addSvc').click(); } });

function syncInputs(){
  Object.entries(FIELD_IDS).forEach(([k,sel])=>{ if(document.activeElement!==$(sel)) $(sel).value=S[k]||''; });
  document.querySelectorAll('.field input[type=checkbox]').forEach(cb=>{ cb.checked=!!S.show[cb.dataset.k]; cb.parentElement.classList.toggle('off',!cb.checked); });
  $('#cP').value=S.P; $('#cS').value=S.S;
  $('#reg').value=S.reg||'';
  document.querySelectorAll('#wbSeg button').forEach(b=>b.classList.toggle('on',(b.dataset.v==='lwb')===!!S.lwb));
  document.querySelectorAll('.style-opt').forEach(b=>b.classList.toggle('on',b.dataset.mode===S.mode));
  $('#dropInner').innerHTML = S.logo? `<img src="${S.logo}" alt="Your logo"><span>Click to replace</span>` : '<b style="color:var(--ink)">Upload your logo</b><br>PNG, JPG or SVG · drag &amp; drop or click';
  $('#removeLogo').classList.toggle('hidden',!S.logo);
  fillMakes(); fillSwatches(); fillTrades(); fillChips();
}

let rT=null;
function changed(light){
  saveState();
  if(!light) syncInputs(); else { $('#cP').value=S.P; $('#cS').value=S.S; }
  clearTimeout(rT); rT=setTimeout(renderPreview, light?60:0);
}

function renderPreview(){
  const designed=S.designed;
  const is3=S.view==='360';
  $('#mainSvg').classList.toggle('hidden',is3); $('#gl').classList.toggle('hidden',!is3); $('#hint360').classList.toggle('hidden',!is3); $('#spin360').classList.toggle('hidden',!is3);
  if(is3) v3Update();
  if(!is3) $('#mainSvg').innerHTML = S.view==='life' ? renderScene(S,{design:designed,layout:S.layout},S.scene) : renderVan(S,{design:designed,layout:S.layout});
  document.querySelectorAll('.viewtoggle button').forEach(b=>b.classList.toggle('on',b.dataset.view===S.view));
  fillScenes();
  const sceneName=(SCENES.find(x=>x[0]===S.scene)||['',''])[1];
  $('#stageBadge').innerHTML = S.view==='360' ? `360° view · <b>${esc(S.make)} ${esc(S.model)}</b>` : S.view==='life' ? `Lifestyle · <b>${esc(sceneName)}</b>` : designed? `${S.mode==='wrap'?'Full wrap':'Graphics'} · <b>${esc(LAYOUTS[S.mode][S.layout].name)}</b>` : `${esc(S.make)} ${esc(S.model)} · ${esc(S.bodyName)}`;
  $('#variantsWrap').classList.toggle('hidden',!designed);
  $('#actions').classList.toggle('hidden',!designed);
  $('#emptyHint').classList.toggle('hidden',designed);
  if(designed){
    $('#variants').innerHTML=LAYOUTS[S.mode].map((L,i)=>`<button class="variant${i===S.layout?' on':''}" data-i="${i}">${renderVan(S,{design:true,layout:i,noFloor:true})}${esc(L.name)}</button>`).join('');
    document.querySelectorAll('#variants .variant').forEach(b=>b.addEventListener('click',()=>{ S.layout=+b.dataset.i; saveState(); renderPreview(); }));
  }
  // style option thumbnails
  const thumbG=Object.assign({},S,{mode:'graphics'}), thumbW=Object.assign({},S,{mode:'wrap'});
  $('#optGsvg').innerHTML=renderVan(thumbG,{design:true,layout:0,noFloor:true});
  $('#optWsvg').innerHTML=renderVan(thumbW,{design:true,layout:0,noFloor:true});
  $('#summary').innerHTML=`<span><b>Van:</b> ${esc(S.make)} ${esc(S.model)} ${S.lwb?'LWB':'SWB'}${S.reg?' · '+esc(S.reg):''}</span><span><b>Colour:</b> ${esc(S.bodyName)}</span><span><b>Style:</b> ${S.mode==='wrap'?'Full wrap':'Graphics'}</span>`;
}
function renderAll(){ syncInputs(); renderPreview(); }

$('#designBtn').addEventListener('click',()=>{
  if(!session){ showApp(); return; }
  $('#designing').classList.add('on');
  setTimeout(()=>{
    S.designed=true; S.layout=0; saveState(); renderPreview();
    $('#designing').classList.remove('on');
    apiEvent('designs_generated',{vehicle:S.make+' '+S.model,style:S.mode}); scheduleSave(true);
    track({event:'design'});
    if(window.innerWidth<980) $('.preview').scrollIntoView({behavior:'smooth'});
  },900);
});
$('#shuffleBtn').addEventListener('click',()=>{ const t=S.P; S.P=S.S; S.S=t; S.layout=(S.layout+1)%3; changed(); });


/* ---------- accounts, saved designs and quotes (van-designer CRM function) ---------- */
const ROOT=document.getElementById('nvg-designer');
const CFG=ROOT?{api:ROOT.dataset.api||'',endpoint:ROOT.dataset.endpoint||'',key:ROOT.dataset.key||'',secret:ROOT.dataset.secret||'',email:ROOT.dataset.email||''}:{};
(function captureSource(){
  try{
    const q=new URLSearchParams(location.search), keep={};
    ['utm_source','utm_medium','utm_campaign','gclid'].forEach(k=>{ if(q.get(k)) keep[k]=q.get(k); });
    if(Object.keys(keep).length) LS.set('nvg_source',Object.assign({landing:location.href,ref:document.referrer},keep));
  }catch(e){}
})();
function dl(event,extra){ try{ (window.dataLayer=window.dataLayer||[]).push(Object.assign({event},extra||{})); }catch(e){} }
function layoutName(){ return (LAYOUTS[S.mode][S.layout]||{}).name||''; }
function designSummary(){
  return [
    'Vehicle: '+S.make+' '+S.model+' '+(S.lwb?'LWB':'SWB')+(S.reg?' ('+S.reg+')':''),
    'Body colour: '+S.bodyName,
    'Style: '+(S.mode==='wrap'?'Full wrap':'Graphics')+(S.designed?' · layout '+layoutName():''),
    'Company on van: '+(S.company||'-'), 'Tagline: '+(S.tagline||'-'), 'Phone on van: '+(S.phone||'-'),
    'Website: '+(S.web||'-'), 'Services: '+((S.services||[]).join(', ')||'-'), 'Logo uploaded: '+(S.logo?'yes':'no'),
    'Brand colours: '+S.P+' / '+S.S
  ].join('\n');
}
function track(extra){ if(session) dl('designer_'+((extra&&extra.event)||'event'),{vehicle:S.make+' '+S.model,style:S.mode}); }

async function api(action,data){
  if(!CFG.api) throw Object.assign(new Error('offline'),{status:0});
  const r=await fetch(CFG.api,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(Object.assign({action},data||{}))});
  let j={}; try{ j=await r.json(); }catch(e){}
  if(!r.ok) throw Object.assign(new Error(j.error||'Something went wrong. Please try again.'),{status:r.status});
  return j;
}
const authed=()=>!!(AUTH&&AUTH.token&&session);
function apiEvent(type,data){ if(authed()) api('event',{token:AUTH.token,type,data:data||null}).catch(()=>{}); }
async function regLookup(reg){ if(!authed()) return null; try{ return await api('reg',{token:AUTH.token,reg}); }catch(e){ return null; } }

function applyAccount(r){
  if(r.token){ AUTH={token:r.token}; LS.set('nvg_auth',AUTH); }
  session=Object.assign({},r.user||{});
  DESIGNS=r.designs||[];
  if(CUR_ID && !DESIGNS.some(d=>d.id===CUR_ID)){ CUR_ID=null; LS.del('nvg_design_id'); }
  if(!S.company && session.company) S.company=session.company;
  if(!S.phone && session.phone) S.phone=session.phone.replace(/^\+44/,'0');
  if(!S.email && session.email) S.email=session.email;
}
function signOutLocal(){ session=null; AUTH=null; DESIGNS=[]; CUR_ID=null; LS.del('nvg_auth'); LS.del('nvg_design_id'); LS.del('nvg_session'); }

/* saving */
let saveT=null, saving=false, saveAgain=false;
function setSaveState(t,cls){ const el=$('#saveState'); if(el){ el.textContent=t; el.className='save-state '+(cls||''); } }
function designPayload(){
  const st=Object.assign({},S,{layoutName:layoutName()});
  let svg=''; try{ svg=renderVan(S,{design:true,layout:S.layout,noFloor:true}); }catch(e){}
  return {id:CUR_ID||undefined, name:(S.company||'My design')+' – '+S.make+' '+S.model,
    vehicle:{make:S.make,model:S.model,size:S.size,lwb:!!S.lwb,reg:S.reg||'',colour:S.bodyName,body:S.body},
    state:st, preview_svg:svg.length<380000?svg:''};
}
function scheduleSave(now){
  if(!authed()||!S.designed) return;
  clearTimeout(saveT); setSaveState('Unsaved changes','');
  saveT=setTimeout(saveNow, now?50:2500);
}
async function saveNow(){
  if(!authed()||!S.designed) return null;
  if(saving){ saveAgain=true; return CUR_ID; }
  saving=true; setSaveState('Saving…','');
  try{
    const r=await api('save_design',{token:AUTH.token,design:designPayload()});
    if(r.id && r.id!==CUR_ID){ CUR_ID=r.id; LS.set('nvg_design_id',CUR_ID); }
    if(r.created){ dl('designer_design_saved'); refreshDesigns(); }
    setSaveState('Saved to your account','ok');
  }catch(e){
    if(e.status===401){ signOutLocal(); showApp(); gateNotice('Your session has ended. Sign in again to keep saving designs.'); }
    else setSaveState('Not saved – will retry','warn');
  }
  saving=false;
  if(saveAgain){ saveAgain=false; return saveNow(); }
  return CUR_ID;
}
async function refreshDesigns(){ if(!authed()) return; try{ const r=await api('me',{token:AUTH.token}); DESIGNS=r.designs||[]; updateWho(); }catch(e){} }

/* gate, login link, account bar */
function gateNotice(t,ok){ const n=$('#gNotice'); if(!n) return; n.textContent=t||''; n.classList.toggle('hidden',!t); n.classList.toggle('ok',!!ok); }
function updateWho(){
  if(!session) return;
  $('#whoName').textContent=session.name||session.email||'';
  const b=$('#myDesigns'); if(b) b.textContent='My designs ('+DESIGNS.length+')';
}
function showApp(){
  const on=!!session;
  $('#nvg-gate').classList.toggle('hidden',on); $('#nvg-app').classList.toggle('hidden',!on);
  document.querySelectorAll('[data-nvg-guest]').forEach(el=>el.classList.toggle('hidden',on));
  if(on){ updateWho(); renderAll(); }
}
$('#gateForm').addEventListener('submit',async e=>{
  e.preventDefault();
  const name=$('#gName').value.trim(), email=$('#gEmail').value.trim();
  if(!name){ $('#gErr').textContent='Please enter your name.'; return; }
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){ $('#gErr').textContent='Please enter a valid email address.'; return; }
  $('#gErr').textContent='';
  const btn=$('#gateForm button[type=submit]'); btn.disabled=true; btn.textContent='Creating your account…';
  const payload={name,email,phone:$('#gPhone').value.trim(),company:$('#gCompany').value.trim(),consent:$('#gConsent').checked,source:LS.get('nvg_source',{}),page:location.href};
  try{
    const r=await api('signup',payload);
    applyAccount(r); saveState(); dl('designer_signup',{returning:!!r.returning}); showApp();
    if(r.returning && DESIGNS.length) setSaveState('Welcome back – your saved designs are under My designs','ok');
  }catch(err){
    if(err.status>=400 && err.status<500){ $('#gErr').textContent=err.message; }
    else {
      // Back end unreachable: let them design now, and send the sign-up to the CRM inbox as a fallback.
      session={name,email,phone:payload.phone,company:payload.company,consent:payload.consent,offline:true};
      postLead('sign-up','Signed up to use the Van Designer (account service unavailable).'+(payload.consent?' Marketing consent: yes.':' Marketing consent: no.'));
      dl('designer_signup',{offline:true}); showApp(); setSaveState('Designs are kept on this device for now','warn');
    }
  }
  btn.disabled=false; btn.textContent='Start designing';
  $('#nvg-app').scrollIntoView({behavior:'smooth',block:'start'});
});
$('#gLoginToggle').addEventListener('click',()=>{ $('#loginForm').classList.toggle('hidden'); $('#lEmail').focus(); });
$('#loginForm').addEventListener('submit',async e=>{
  e.preventDefault();
  const email=$('#lEmail').value.trim();
  if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)){ $('#lMsg').textContent='Please enter a valid email address.'; return; }
  $('#lMsg').textContent='Sending…';
  try{ await api('request_link',{email}); $('#lMsg').textContent='If that email has an account, a login link is on its way. It works once and lasts 48 hours.'; }
  catch(err){ $('#lMsg').textContent=err.message; }
});
$('#logout').addEventListener('click',async()=>{
  if(authed()) api('logout',{token:AUTH.token}).catch(()=>{});
  signOutLocal(); showApp(); gateNotice('You have signed out. Your designs are saved to your account.',true);
});

/* my designs */
function fmtDate(s){ try{ return new Date(s).toLocaleDateString('en-GB',{day:'numeric',month:'short',year:'numeric'}); }catch(e){ return ''; } }
function openDesigns(){
  const card=$('#quoteCard');
  const items=DESIGNS.map(d=>`<article class="my-design${d.id===CUR_ID?' current':''}"><div class="my-design__svg">${d.preview_svg||''}</div>
    <div class="my-design__meta"><b>${esc(d.name||'Untitled design')}</b><span>${esc((d.vehicle&&d.vehicle.make)||'')} ${esc((d.vehicle&&d.vehicle.model)||'')} · ${fmtDate(d.updated_at)}</span>
    ${d.status==='quote_requested'?'<em class="tag-q">Quote requested</em>':''}${d.id===CUR_ID?'<em class="tag-c">Open now</em>':''}</div>
    <div class="my-design__act"><button class="btn btn-dark" data-open="${d.id}" type="button">Open</button><button class="btn btn-ghost" data-del="${d.id}" type="button" aria-label="Delete design">Delete</button></div></article>`).join('');
  card.innerHTML=`<h3>My designs</h3><p class="muted">Every design is saved to your account, so you can pick it up on any device.</p>
    <div class="my-designs">${items||'<p class="muted">No saved designs yet. Press <b>Design my van</b> and your first design saves automatically.</p>'}</div>
    <div class="actions"><button class="btn btn-ghost" id="mdClose" type="button">Close</button><button class="btn btn-hv" id="mdNew" type="button">Start a new design</button></div>`;
  $('#quoteModal').classList.add('on');
  $('#mdClose').onclick=()=>$('#quoteModal').classList.remove('on');
  $('#mdNew').onclick=()=>{ CUR_ID=null; LS.del('nvg_design_id'); S=Object.assign({},DEFAULT,{show:Object.assign({},DEFAULT.show),company:session.company||'',phone:(session.phone||'').replace(/^\+44/,'0'),email:session.email||''}); saveState(); renderAll(); $('#quoteModal').classList.remove('on'); setSaveState('New design – press Design my van to save it',''); };
  card.querySelectorAll('[data-open]').forEach(b=>b.onclick=async()=>{
    b.disabled=true; b.textContent='Opening…';
    try{ const r=await api('get_design',{token:AUTH.token,id:b.dataset.open}); const st=r.design.state||{};
      S=Object.assign({},DEFAULT,st); S.show=Object.assign({},DEFAULT.show,st.show||{}); CUR_ID=r.design.id; LS.set('nvg_design_id',CUR_ID);
      LS.set('nvg_state',S); renderAll(); apiEvent('design_opened',{design_id:CUR_ID}); $('#quoteModal').classList.remove('on'); setSaveState('Saved to your account','ok');
    }catch(e){ b.textContent='Try again'; b.disabled=false; }
  });
  card.querySelectorAll('[data-del]').forEach(b=>b.onclick=async()=>{
    if(!confirm('Delete this design?')) return;
    try{ const r=await api('delete_design',{token:AUTH.token,id:b.dataset.del}); DESIGNS=r.designs||[]; if(b.dataset.del===CUR_ID){ CUR_ID=null; LS.del('nvg_design_id'); } updateWho(); openDesigns(); }catch(e){}
  });
}
$('#myDesigns').addEventListener('click',openDesigns);

/* fallback lead post (used only if the account service is down) */
async function postLead(kind,message){
  if(!CFG.endpoint||!CFG.key||!CFG.secret||!session) return false;
  const src=LS.get('nvg_source',{});
  try{
    const r=await fetch(CFG.endpoint,{method:'POST',headers:{'content-type':'application/json','x-rcg-channel-key':CFG.key,'x-rcg-channel-secret':CFG.secret},body:JSON.stringify({
      name:session.name,email:session.email,phone:session.phone||'',company:session.company||'',subject:'Van Designer – '+kind,message,source_url:location.href,
      utm_source:src.utm_source||'',utm_medium:src.utm_medium||'',utm_campaign:src.utm_campaign||'',gclid:src.gclid||''})});
    return r.ok;
  }catch(e){ return false; }
}

/* quote */
$('#quoteBtn').addEventListener('click',()=>{
  const card=$('#quoteCard');
  card.innerHTML=`<h3>Request a quote for this design</h3>${renderVan(S,{design:true,layout:S.layout,noFloor:true})}
   <label class="f">Anything we should know?<textarea id="qNotes" rows="3" placeholder="e.g. 2 vans, fitting needed by March, rear doors too"></textarea></label>
   <div class="row2"><label class="f">Best way to contact you<select id="qPref"><option>Phone</option><option>Email</option><option>WhatsApp</option></select></label>
   <label class="f">Phone<input id="qPhone" type="tel" value="${esc((session.phone||S.phone||'').replace(/^\+44/,'0'))}"></label></div>
   <div class="err" id="qErr"></div>
   <div class="actions"><button class="btn btn-ghost" id="qCancel" type="button">Cancel</button><button class="btn btn-hv" id="qSend" type="button">Send to the Norwich team</button></div>`;
  $('#quoteModal').classList.add('on');
  $('#qCancel').onclick=()=>$('#quoteModal').classList.remove('on');
  $('#qSend').onclick=async()=>{
    const btn=$('#qSend'); btn.disabled=true; btn.textContent='Sending…';
    const notes=$('#qNotes').value.trim(), pref=$('#qPref').value, phone=$('#qPhone').value.trim();
    if(phone) session.phone=phone;
    const first=esc((session.name||'').split(' ')[0]||'there');
    let sent=false;
    if(authed()){
      try{ const id=await saveNow(); const r=await api('quote',{token:AUTH.token,design_id:id,notes,pref,phone,page:location.href}); DESIGNS=r.designs||DESIGNS; updateWho(); sent=true; }
      catch(e){ $('#qErr').textContent=e.status===404?'Press Design my van first so we can save your design.':''; if(e.status===404){ btn.disabled=false; btn.textContent='Send to the Norwich team'; return; } }
    }
    if(!sent) sent=await postLead('quote request',designSummary()+'\n\nContact preference: '+pref+(phone?'\nPhone: '+phone:'')+(notes?'\nNotes: '+notes:''));
    dl('designer_quote',{vehicle:S.make+' '+S.model,style:S.mode});
    if(sent){
      card.innerHTML=`<div class="done"><div class="tick">✓</div><h3>Thanks, ${first} – your design is with the team.</h3><p class="muted">We'll be in touch by ${esc(pref.toLowerCase())} with a quote, and we've emailed you a confirmation. Your design is saved under My designs.</p><button class="btn btn-dark" id="qClose" type="button">Back to my design</button></div>`;
    } else {
      const to=CFG.email||'';
      const subject='Van Designer quote request – '+S.make+' '+S.model;
      const body='Name: '+session.name+'\nEmail: '+session.email+'\nPhone: '+(phone||'-')+'\n\n'+designSummary()+(notes?'\n\nNotes: '+notes:'');
      card.innerHTML=`<div class="done"><div class="tick">✓</div><h3>Nearly there, ${first}.</h3><p class="muted">Your email app should open with your design details ready to send to ${esc(to)}. If it doesn't, call us and mention your ${esc(S.make)} ${esc(S.model)} design.</p><button class="btn btn-dark" id="qClose" type="button">Back to my design</button></div>`;
      try{ window.location.href='mailto:'+to+'?subject='+encodeURIComponent(subject)+'&body='+encodeURIComponent(body); }catch(e){}
    }
    $('#qClose').onclick=()=>$('#quoteModal').classList.remove('on');
  };
});
$('#quoteModal').addEventListener('click',e=>{ if(e.target.id==='quoteModal') $('#quoteModal').classList.remove('on'); });
document.addEventListener('keydown',e=>{ if(e.key==='Escape') $('#quoteModal').classList.remove('on'); });

/* boot: login link → stored session → gate */
async function boot(){
  gateArt();
  const q=new URLSearchParams(location.search), link=q.get('login');
  if(link){
    q.delete('login'); history.replaceState(null,'',location.pathname+(q.toString()?'?'+q:'')+location.hash);
    try{ applyAccount(await api('redeem',{link})); dl('designer_login'); }
    catch(e){ gateNotice(e.message); $('#loginForm').classList.remove('hidden'); }
  } else if(AUTH && AUTH.token){
    try{ applyAccount(await api('me',{token:AUTH.token})); }
    catch(e){ if(e.status===401){ signOutLocal(); gateNotice('Please sign in again to see your saved designs.'); $('#loginForm').classList.remove('hidden'); } }
  }
  showApp();
  if(session && link) setSaveState('Signed in – your saved designs are under My designs','ok');
}
boot();
})();
