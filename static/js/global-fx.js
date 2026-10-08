/* Global motion layer (all app pages) */
(function(){
  "use strict";
  var d=document, root=d.documentElement, body=d.body;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  function mk(tag,cls,html){var n=d.createElement(tag);n.className=cls;if(html)n.innerHTML=html;return n}
  function rnd(a,b){return a+Math.random()*(b-a)}

  /* ambient backdrop with floating hardware glyphs */
  var amb=mk('div','fx-amb','<div class="b b1"></div><div class="b b2"></div><div class="b b3"></div>');
  var GL=['<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
    '<rect x="2" y="8" width="20" height="8" rx="1.5"/><path d="M5 12h2M9 12h2M13 12h2M17 12h2M6 16v3M10 16v3M14 16v3M18 16v3"/>',
    '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="1.8"/><path d="M12 10.2C12 6 14 4.5 16 5M13.8 12c4.2 0 5.7 2 5.2 4M12 13.8c0 4.2-2 5.7-4 5.2M10.2 12C6 12 4.5 10 5 8"/>',
    '<path d="M13 2L5 14h6l-1 8 8-12h-6z"/>',
    '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="9" r="2"/><circle cx="10" cy="18" r="2"/><path d="M7 6.5l10 2M18 11l-6 5.5M8.5 16.5L6 8"/>',
    '<rect x="4" y="3" width="16" height="18" rx="2"/><circle cx="12" cy="12" r="3.5"/><circle cx="12" cy="12" r=".6"/>'];
  for(var i=0;i<14;i++){
    var s=rnd(34,64), g=mk('div','g');
    g.innerHTML='<svg viewBox="0 0 24 24" width="'+s+'" height="'+s+'" aria-hidden="true">'+GL[i%GL.length]+'</svg>';
    g.style.cssText='left:'+rnd(2,96).toFixed(1)+'%;opacity:'+rnd(.12,.22).toFixed(2)+';--r:'+(rnd(-260,260)).toFixed(0)+'deg;animation-duration:'+rnd(45,95).toFixed(0)+'s;animation-delay:-'+rnd(0,90).toFixed(0)+'s';
    amb.appendChild(g);
  }
  body.insertBefore(amb,body.firstChild);

  /* scroll progress */
  var prog=mk('div','fx-prog'); body.appendChild(prog);
  function onScroll(){var h=root.scrollHeight-innerHeight;prog.style.transform='scaleX('+(h>0?Math.min(1,scrollY/h):0).toFixed(4)+')'}
  addEventListener('scroll',onScroll,{passive:true}); onScroll();

  /* navbar sliding underline */
  var wrapN=d.querySelector('.nav-links-wrap');
  if(wrapN){
    var line=mk('div','fx-navline'); wrapN.appendChild(line);
    var links=[].slice.call(wrapN.querySelectorAll('.nav-link-item'));
    var move=function(el){ if(!el){line.style.width='0';return}
      line.style.width=(el.offsetWidth*.5)+'px'; line.style.transform='translateX('+(el.offsetLeft+el.offsetWidth*.25)+'px)' };
    var home=function(){move(wrapN.querySelector('.nav-link-item.active'))};
    links.forEach(function(a){a.addEventListener('mouseenter',function(){move(a)})});
    wrapN.addEventListener('mouseleave',home); addEventListener('resize',home); setTimeout(home,60);
  }

  /* dashboard hero art */
  var hero=d.querySelector('.hero-banner');
  if(hero){
    var orb=function(rot,dur,col,rev){var p='M15,67a100,36 0 1,0 200,0a100,36 0 1,0 -200,0';
      return '<g transform="rotate('+rot+' 120 67)"><path class="o" d="'+p+'"/><circle r="4.5" fill="'+col+'"><animateMotion dur="'+dur+'s" repeatCount="indefinite" path="'+p+'"'+(rev?' keyPoints="1;0" keyTimes="0;1" calcMode="linear"':'')+'/></circle></g>'};
    hero.appendChild(mk('div','fx-hero-art','<svg viewBox="0 0 240 134" aria-hidden="true">'+orb(-22,7,'#4FE3A2')+orb(22,9,'#FF8A3D',1)+orb(0,5.5,'#C8FF3D')+
      '<rect class="chip" x="98" y="45" width="44" height="44" rx="10"/><rect x="108" y="55" width="24" height="24" rx="5" fill="none" stroke="rgba(12,14,11,.4)"/></svg>'));
  }

  /* reveal on scroll (+ stagger) for static and dynamically rendered cards */
  var CARDS='.tech-card,.metric-box,.hud-panel,.domain-select-card,.pathway-card,.saved-card,.component-item-card,.manifest-paper-card,.score-box,.mode-card-interactive';
  var REV=CARDS+',.hero-banner,.hud-header,.category-nav-item,.step-pill';
  var io=null;
  function scramble(n){
    var t=n.textContent.trim(), m=/^([\d,]+)(\+?)$/.exec(t);
    if(!t||t.length>18) return;
    var t0=performance.now(), D=900;
    (function f(now){var p=Math.min(1,(now-t0)/D);
      if(m){var v=parseInt(m[1].replace(/,/g,''),10);n.textContent=Math.round(v*(1-Math.pow(1-p,3))).toLocaleString('en-US')+m[2]}
      else{var o='';for(var i=0;i<t.length;i++)o+=(t[i]===' '||i<t.length*p)?t[i]:'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789'[Math.floor(Math.random()*34)];n.textContent=o}
      if(p<1)requestAnimationFrame(f);else n.textContent=t})(t0);
  }
  if(!reduce&&'IntersectionObserver' in window){
    io=new IntersectionObserver(function(es){
      var vis=es.filter(function(e){return e.isIntersecting}).sort(function(a,b){return a.boundingClientRect.top-b.boundingClientRect.top||a.boundingClientRect.left-b.boundingClientRect.left});
      vis.forEach(function(e,i){var n=e.target; io.unobserve(n);
        n.style.setProperty('--d',Math.min(i*60,420)+'ms'); n.classList.remove('fx-pre'); n.classList.add('fx-in');
        setTimeout(function(){n.classList.remove('fx-in');n.style.removeProperty('--d')},1300);
        [].forEach.call(n.querySelectorAll('.metric-value,.score-val'),scramble);
        if(n.matches('.metric-value,.score-val')) scramble(n);
      });
    },{threshold:.08});
  }
  function prep(n){
    if(n.nodeType!==1) return;
    var list=[].slice.call(n.querySelectorAll?n.querySelectorAll(REV+','+CARDS):[]); if(n.matches&&n.matches(REV)) list.unshift(n);
    list.forEach(function(c){
      if(c._fx) return; c._fx=1;
      if(c.matches(CARDS)){ c.classList.add('fx-card'); if(getComputedStyle(c).position==='static') c.style.position='relative'; }
      if(io){c.classList.add('fx-pre'); io.observe(c)}
    });
  }
  prep(body);
  new MutationObserver(function(ms){ms.forEach(function(m){[].forEach.call(m.addedNodes,prep)})}).observe(body,{childList:true,subtree:true});
  if(io) setTimeout(function(){[].forEach.call(d.querySelectorAll('.fx-pre'),function(c){if(c.offsetParent!==null){c.classList.remove('fx-pre')}})},3500);

  /* ripple + burst */
  d.addEventListener('pointerdown',function(e){
    var b=e.target.closest&&e.target.closest('.btn'); if(!b||reduce) return;
    var r=b.getBoundingClientRect(), s=Math.max(r.width,r.height)*2.2, o=mk('span','fx-ripple');
    o.style.cssText='width:'+s+'px;height:'+s+'px;left:'+(e.clientX-r.left-s/2)+'px;top:'+(e.clientY-r.top-s/2)+'px';
    b.appendChild(o); setTimeout(function(){o.remove()},650);
  });
  d.addEventListener('click',function(e){
    var b=e.target.closest&&e.target.closest('.btn-primary'); if(!b||reduce) return;
    var C=['#C8FF3D','#4FE3A2','#FF8A3D','#7C9A2A'];
    for(var i=0;i<14;i++){var p=mk('span','fx-p'),a=Math.random()*6.283,v=rnd(40,110);
      p.style.cssText='left:'+e.clientX+'px;top:'+e.clientY+'px;background:'+C[i%4]+';--dx:'+(Math.cos(a)*v).toFixed(0)+'px;--dy:'+(Math.sin(a)*v-20).toFixed(0)+'px;--r:'+rnd(-200,200).toFixed(0)+'deg';
      body.appendChild(p); (function(q){setTimeout(function(){q.remove()},800)})(p)}
  });

})();
