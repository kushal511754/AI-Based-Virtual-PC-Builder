/* Intro splash. Wordmark assembly ported from creator-studio-intro.html (makeWordmark, first beat 0–1.72s):
   math, easing, jitter seed and chromatic-split values unchanged. Text = "AI Virtual PC Builder".
   Added: zoom-in push, zoom-through exit, redirect to /login (~2s total). */
(function(){
  "use strict";
  var TEXT="AI Virtual PC Builder", TARGET_W=860, NEXT="/login";
  var BEAT=1.0, EXIT_AT=1.4, END=2.0, W=1280, H=720;
  var splash=document.getElementById('introSplash'), comp=document.getElementById('introComp'), ruler=document.getElementById('introRuler');
  if(!splash||!comp||!ruler) return;
  document.documentElement.classList.add('intro-lock');

  var done=false;
  function go(){ if(done) return; done=true; window.location.replace(NEXT); }

  var reduce=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var clamp=function(v,a,b){return v<a?a:(v>b?b:v)};
  var lerp=function(a,b,t){return a+(b-a)*t};
  var seg=function(t,a,b){return clamp((t-a)/(b-a||1e-6),0,1)};
  var eOut=function(t){return 1-Math.pow(1-t,3)};
  var eIn=function(t){return t*t*t};
  function rng(s){var a=s>>>0;return function(){a+=0x6D2B79F5;var t=a;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return((t^t>>>14)>>>0)/4294967296}}
  function setT(n,v){if(n._t!==v){n._t=v;n.style.transform=v}}
  function setO(n,v){var r=clamp(v,0,1).toFixed(3);if(n._o!==r){n._o=r;n.style.opacity=r}}
  function setF(n,v){if(n._f!==v){n._f=v;n.style.filter=v}}

  function fitPx(str,target){
    ruler.style.fontSize='100px'; ruler.textContent=str;
    return 100*target/ruler.getBoundingClientRect().width;
  }

  var scene=document.createElement('div'); scene.className='scene'; comp.appendChild(scene);
  var wrap=document.createElement('div'); wrap.className='line'; scene.appendChild(wrap);
  var tx=document.createElement('div'); tx.className='tx'; wrap.appendChild(tx);
  function layout(){ tx.style.fontSize=fitPx(TEXT,TARGET_W).toFixed(2)+'px'; }
  layout();
  var chars=[];
  for(var i=0;i<TEXT.length;i++){
    var sp=document.createElement('span');
    sp.textContent=TEXT[i]===' '?'\u00a0':TEXT[i];
    tx.appendChild(sp); chars.push(sp);
  }
  for(var q=0;q<2;q++) chars[q].style.color='#C8FF3D';   /* "AI" in volt */
  var bar=document.createElement('div'); bar.className='bar'; scene.appendChild(bar);
  var R=rng(7719), jit=chars.map(function(){return [R()*2-1,R()*2-1,R()]});

  function update(p){
    bar.style.top='calc(50% + '+(parseFloat(tx.style.fontSize)*.78).toFixed(1)+'px)'; bar.style.transform='scaleX('+eOut(seg(p,.45,1)).toFixed(3)+')';
    for(var i=0;i<chars.length;i++){
      var j=jit[i];
      var a=eOut(clamp(seg(p,.02,.5)*1.5-j[2]*.5,0,1));
      setT(chars[i],'translate('+(j[0]*62*(1-a)).toFixed(1)+'px,'+(j[1]*34*(1-a)).toFixed(1)+'px) scale('+lerp(1.24,1,a).toFixed(3)+')');
      setO(chars[i],Math.min(1,a*1.6));
      var sep=(1-a)*11;
      chars[i].style.textShadow=sep>.4
        ? (-sep).toFixed(1)+'px 0 rgba(255,64,72,.85),'+sep.toFixed(1)+'px 0 rgba(64,255,190,.8),0 '+(sep*.55).toFixed(1)+'px rgba(96,124,255,.8)'
        : 'none';
      setF(chars[i],sep>.7?'blur('+(sep*.3).toFixed(2)+'px)':'none');
    }
  }

  function render(t){
    var w=splash.clientWidth||W, h=splash.clientHeight||H;
    var k=w<h ? w/960 : Math.min(w/W,h/H);           /* portrait phones: fill width */
    var push=lerp(.8,1.05,eOut(seg(t,0,EXIT_AT)));    /* slow zoom-in while text assembles and holds */
    var ex=seg(t,EXIT_AT,END);
    var zoom=push*lerp(1,2.6,eIn(ex));                /* zoom-through on exit */
    comp.style.transform='scale('+(k*zoom).toFixed(4)+')';
    setO(comp,1-ex);
    setF(comp,ex>0?'blur('+(ex*8).toFixed(1)+'px)':'none');
    update(seg(t,0,BEAT));
  }

  if(reduce){ update(1); render(EXIT_AT); setTimeout(go,800); return; }

  var start=null;
  function tick(now){
    if(done) return;
    if(start===null) start=now;
    var t=(now-start)/1000;
    render(Math.min(t,END));
    if(t>=END){ go(); return; }
    requestAnimationFrame(tick);
  }
  render(0);
  if(document.fonts&&document.fonts.ready){ document.fonts.ready.then(layout); }
  requestAnimationFrame(tick);
  setTimeout(go,(END+.1)*1000);                       /* safety net if rAF is throttled */
})();
