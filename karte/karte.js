(function(){
'use strict';
var D=window.KARTE, KEY='pizzaofen-karte-v3', st={};
try{st=JSON.parse(localStorage.getItem(KEY)||'{}')||{}}catch(e){st={}}
function save(){try{localStorage.setItem(KEY,JSON.stringify(st))}catch(e){}}
var NS='http://www.w3.org/2000/svg';
var app=document.querySelector('.app'), svg=document.getElementById('map'), geo=document.getElementById('geo'),
    pinsG=document.getElementById('pins'), lblG=document.getElementById('lbl'), scG=document.getElementById('scale');
var W=0,H=0,v={s:1,tx:0,ty:0},sFit=1,ph=st.ph||'1',sel=null;
function el(n,a,p){var e=document.createElementNS(NS,n);for(var k in a)e.setAttribute(k,a[k]);if(p)p.appendChild(e);return e}
function fmt(x){return Math.round(x).toString().replace(/\B(?=(\d{3})+(?!\d))/g,"'")}
function chf(x){var s=x.toFixed(2).split('.');return s[0].replace(/\B(?=(\d{3})+$)/g,"'")+'.'+s[1]}
/* ---------- Ansicht ---------- */
function size(){var r=svg.getBoundingClientRect();W=r.width;H=r.height;svg.setAttribute('viewBox','0 0 '+W+' '+H)}
function scaleFor(b,pad){return Math.min((W-2*pad)/(b[2]-b[0]),(H-2*pad)/(b[3]-b[1]))}
function fit(b,pad){pad=pad==null?36:pad;var s=scaleFor(b,pad);v.s=s;v.tx=W/2-s*(b[0]+b[2])/2;v.ty=H/2-s*(b[1]+b[3])/2;draw()}
function clampS(s){return Math.max(sFit*0.5,Math.min(sFit*14,s))}
function zoomAt(f,cx,cy){var ns=clampS(v.s*f);f=ns/v.s;v.tx=cx-(cx-v.tx)*f;v.ty=cy-(cy-v.ty)*f;v.s=ns;draw()}
function X(p){return v.tx+v.s*p[0]}function Y(p){return v.ty+v.s*p[1]}
function draw(){geo.setAttribute('transform','translate('+v.tx+','+v.ty+') scale('+v.s+')');drawPins();drawScale()}
function drawPins(){
  pinsG.textContent='';lblG.textContent='';
  var pins=D.pins[ph], occ=[];
  pins.forEach(function(p){
    var o=D.orte[p[0]], x=X(o), y=Y(o), home=p[3]==='h', cls='pin '+(home?'h':'k'+p[3]);
    var key=D.first[ph][p[0]]; if(sel&&!home&&D.tripRoute[sel]===p[0])cls+=' sel';
    var g=el('g',{'class':cls,transform:'translate('+x.toFixed(1)+','+y.toFixed(1)+')'},pinsG);
    if(key){g.setAttribute('tabindex','0');g.setAttribute('role','button');g.setAttribute('aria-label',p[2]+' – Fahrt '+key+' zeigen')}
    el('circle',{r:home?9:(p[1].length>1?14:12)},g);
    el('text',{'class':'ic','font-size':p[1].length>1?10:12},g).textContent=p[1];
    var side=p[4]||'r', right=side==='r'?x<W-160:x<150, dy=p[5]||0, w=7*p[2].length;
    var lb=el('text',{'class':'lb',x:right?18:-18,y:dy,'text-anchor':right?'start':'end'},g);lb.textContent=p[2];
    occ.push(right?[x-14,y+dy-14,x+20+w,y+dy+14]:[x-20-w,y+dy-14,x+14,y+dy+14]);
    if(key){g.addEventListener('click',function(){select(key,true)});g.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();select(key,true)}})}
  });
  D.places.forEach(function(t){
    var big=t.t==='city'; if(!big&&v.s<sFit*1.35)return;
    var x=X(t.p),y=Y(t.p); if(x<-40||y<-20||x>W+40||y>H+20)return;
    var w=(big?7.4:6.4)*t.n.length/2+3, bb=[x-w,y-8,x+w,y+8]; if(bb[0]<4||bb[2]>W-4||bb[1]<4||bb[3]>H-30)return;
    for(var i=0;i<occ.length;i++){var o=occ[i];if(bb[0]<o[2]&&bb[2]>o[0]&&bb[1]<o[3]&&bb[3]>o[1])return}
    occ.push(bb);el('text',{'class':'town'+(big?' city':''),x:x.toFixed(1),y:y.toFixed(1)},lblG).textContent=t.n;
  });
}
function drawScale(){
  scG.textContent='';var kmPerU=0.1113, target=110/v.s*kmPerU, nice=[0.5,1,2,5,10,20,50], km=nice[0];
  for(var i=0;i<nice.length;i++)if(nice[i]<=target)km=nice[i];
  var px=km/kmPerU*v.s, g=el('g',{'class':'sc',transform:'translate(12,'+(H-28)+')'},scG);
  el('line',{x1:0,y1:0,x2:px,y2:0},g);el('line',{x1:0,y1:-5,x2:0,y2:0},g);el('line',{x1:px,y1:-5,x2:px,y2:0},g);
  el('text',{x:px+6,y:0,'dominant-baseline':'central'},g).textContent=km+' km';
}
/* ---------- Routen und Phase ---------- */
var routes=[].slice.call(document.querySelectorAll('.rt'));
var ON={'1':['oftringen','kies','volketswil'],'2':['volketswil2','winterthur'],'a':['oftringen','kies','volketswil','volketswil2','winterthur']};
function routeEl(key){var r=D.tripRoute[key], p2=document.querySelector('#t-'+key).dataset.phase==='2';return r==='volketswil'&&p2?'volketswil2':r}
function selRoutes(){if(!sel)return[];var r=routeEl(sel);return sel==='C'?[r,'winterthur']:[r]}
function styleRoutes(){
  var sr=selRoutes();
  routes.forEach(function(r){var n=r.dataset.r, s=sr.indexOf(n)>=0;
    r.classList.toggle('on',ON[ph].indexOf(n)>=0||s);r.classList.toggle('sel',s);r.classList.toggle('dim',sr.length>0&&!s)});
}
function setPhase(p,refit){
  ph=p;st.ph=p;save();app.dataset.ph=p;
  document.querySelectorAll('.tabs button').forEach(function(b){b.setAttribute('aria-selected',b.dataset.ph===p?'true':'false')});
  var k=D.kpi[p];document.getElementById('k-chf').textContent='CHF '+chf(k.chf);document.getElementById('k-n').textContent=k.n;document.getElementById('k-kg').textContent=fmt(k.kg)+' kg';
  document.getElementById('k-vor').textContent=chf(D.kpi['1'].vor);
  if(sel&&document.getElementById('t-'+sel).dataset.phase!==p&&p!=='a')select(null);
  sFit=scaleFor(D.fit.a,36);styleRoutes();if(refit!==false)fit(D.fit[p]);else draw();
}
function select(key,fromMap){
  document.querySelectorAll('.trip.sel').forEach(function(c){c.classList.remove('sel')});
  sel=key;styleRoutes();
  if(!key){draw();return}
  var card=document.getElementById('t-'+key);card.classList.add('sel');
  var rr=routeEl(key), b=D.routes[key==='C'?'winterthur':rr==='volketswil2'?'volketswil':rr];
  fit(b,40);
  if(fromMap)card.scrollIntoView({behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth',block:'start'});
}
document.querySelectorAll('.tabs button').forEach(function(b){b.addEventListener('click',function(){setPhase(b.dataset.ph)})});
document.querySelectorAll('[data-show]').forEach(function(b){b.addEventListener('click',function(){
  select(b.dataset.show);var m=document.querySelector('.mapwrap'),r=m.getBoundingClientRect();
  if(r.top<0||r.bottom>innerHeight)m.scrollIntoView({behavior:'smooth',block:'start'});
})});
/* ---------- Bedienung Karte ---------- */
var pts={},last=null;
function mid(){var a=Object.keys(pts).map(function(k){return pts[k]});return a.length<2?null:{x:(a[0].x+a[1].x)/2,y:(a[0].y+a[1].y)/2,d:Math.hypot(a[0].x-a[1].x,a[0].y-a[1].y)}}
function loc(e){var r=svg.getBoundingClientRect();return{x:e.clientX-r.left,y:e.clientY-r.top}}
svg.addEventListener('pointerdown',function(e){if(e.target.closest&&e.target.closest('.pin'))return;svg.setPointerCapture(e.pointerId);pts[e.pointerId]=loc(e);last=mid();svg.classList.add('drag')});
svg.addEventListener('pointermove',function(e){
  if(!pts[e.pointerId])return;var p=loc(e),o=pts[e.pointerId];pts[e.pointerId]=p;var m=mid();
  if(m&&last){v.tx+=m.x-last.x;v.ty+=m.y-last.y;if(last.d>0)zoomAt(m.d/last.d,m.x,m.y);else draw();last=m}
  else if(!m){v.tx+=p.x-o.x;v.ty+=p.y-o.y;draw()}
});
function up(e){delete pts[e.pointerId];last=mid();if(!Object.keys(pts).length)svg.classList.remove('drag')}
svg.addEventListener('pointerup',up);svg.addEventListener('pointercancel',up);
svg.addEventListener('wheel',function(e){e.preventDefault();var p=loc(e);zoomAt(Math.exp(-e.deltaY*0.0018),p.x,p.y)},{passive:false});
svg.addEventListener('dblclick',function(e){var p=loc(e);zoomAt(1.8,p.x,p.y)});
document.getElementById('zin').addEventListener('click',function(){zoomAt(1.6,W/2,H/2)});
document.getElementById('zout').addEventListener('click',function(){zoomAt(1/1.6,W/2,H/2)});
document.getElementById('zfit').addEventListener('click',function(){select(null);fit(D.fit[ph])});
var rz;window.addEventListener('resize',function(){clearTimeout(rz);rz=setTimeout(function(){var cx=(W/2-v.tx)/v.s,cy=(H/2-v.ty)/v.s;size();sFit=scaleFor(D.fit.a,36);v.tx=W/2-cx*v.s;v.ty=H/2-cy*v.s;draw()},120)});
/* ---------- Haekchen ---------- */
var boxes=[].slice.call(document.querySelectorAll('.item input'));
boxes.forEach(function(b){if(st['c'+b.dataset.k])b.checked=true;b.addEventListener('change',function(){st['c'+b.dataset.k]=b.checked;save()})});
var reset=document.getElementById('reset'),conf=document.getElementById('confirm');
reset.addEventListener('click',function(){reset.hidden=true;conf.hidden=false});
document.getElementById('no').addEventListener('click',function(){reset.hidden=false;conf.hidden=true});
document.getElementById('yes').addEventListener('click',function(){Object.keys(st).forEach(function(k){if(k.charAt(0)==='c')delete st[k]});save();boxes.forEach(function(b){b.checked=false});reset.hidden=false;conf.hidden=true});
/* ---------- Nutzlast ---------- */
var gg=document.getElementById('gg'),lg=document.getElementById('lg'),mf=document.getElementById('mf'),out=document.getElementById('calc-out');
['gg','lg','mf'].forEach(function(k){if(st[k]!=null)document.getElementById(k).value=st[k]});
function calc(){
  var G=+gg.value,L=+lg.value,B=Math.max(0,Math.min(2,+mf.value||0));st.gg=gg.value;st.lg=lg.value;st.mf=mf.value;save();
  var nl=G-L, av=nl-75*B-20, P=Math.floor(av*0.9/10)*10, msg='';
  if(!(G>0&&L>0)||nl<=0){out.innerHTML='<span class="bad">Bitte Gesamtgewicht und Leergewicht aus dem Fahrzeugausweis eintragen.</span>';P=0}
  else if(G>3500){out.innerHTML='<span class="bad">Gesamtgewicht über 3\'500 kg: Dieses Fahrzeug dürft ihr mit Kat. B nicht fahren (Kat. C1 nötig).</span>';P=0}
  else{
    var nk=Math.ceil(D.kies_kg/P);
    msg='Nutzlast laut Ausweis <b>'+fmt(nl)+' kg</b>. Abzüglich '+B+' Beifahrer und 20 kg Gurte/Kästen bleiben '+fmt(av)+' kg, mit 10 % Sicherheit für Schätzfehler beim Kies: <b>max. '+fmt(P)+' kg pro Fahrt</b>. ';
    if(nl>=2000)msg+='<span class="ok">Laut diesen Werten wären 2 t möglich.</span> Prüft die Zahlen im Ausweis nochmals, beim Talento ist das nicht realistisch. ';
    else msg+='<span class="bad">2\'000 kg Ladung gehen mit diesem Bus nicht</span>, das wären '+fmt(L+2000+75*B)+' kg statt erlaubt '+fmt(G)+' kg. ';
    var bad=[].slice.call(document.querySelectorAll('.trip')).filter(function(c){return +c.dataset.kg>P}).map(function(c){return c.dataset.key});
    msg+=bad.length?'<span class="bad">Zu schwer für eine Fahrt: '+bad.join(', ')+'.</span> Kies dann in '+nk+' statt 4 Fahrten holen und die Kästen weniger voll machen.'+(bad.indexOf('B')>=0?' Bei B die Schalungssteine auf zwei Fahrten verteilen.':''):'<span class="ok">Alle Fahrten passen.</span>';
    out.innerHTML=msg;
  }
  document.querySelectorAll('.trip').forEach(function(c){
    var k=+c.dataset.kg, l=c.querySelector('.load'), pct=P?Math.min(100,k/P*100):100;
    l.querySelector('.bar').style.width=pct+'%';l.classList.toggle('over',!P||k>P);
    l.querySelector('.lt').textContent=fmt(k)+' kg von max. '+(P?fmt(P):'?')+' kg'+(P&&k>P?' – zu schwer, aufteilen':'');
  });
}
[gg,lg,mf].forEach(function(i){i.addEventListener('input',calc)});
/* ---------- Start ---------- */
size();calc();setPhase(ph);
})();
