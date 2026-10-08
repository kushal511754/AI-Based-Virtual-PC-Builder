/* Login page effects: backdrop, compatibility-check graphic, ripples, page wipe. */
(function(){
  "use strict";
  var d=document, root=d.documentElement;
  var wrapEl=d.querySelector('.auth-split-wrapper'), view=d.querySelector('.auth-viewport'), panel=d.querySelector('.auth-branding-panel');
  if(!wrapEl||!view||!panel) return;
  var reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  function mk(tag,cls,html){var n=d.createElement(tag);n.className=cls;if(html)n.innerHTML=html;return n}

  /* backdrop */
  var bg=mk('div','fx-bg','<i></i><i></i><i></i>'); view.insertBefore(bg,view.firstChild);

  /* compatibility-check graphic */
  var CH=[['GPU',20,20,'M104,43H150V95H190',.5],['RAM',356,20,'M356,43H310V95H270',-.5],
          ['SSD',20,164,'M104,187H150V135H190',-.35],['PSU',356,164,'M356,187H310V135H270',.35]];
  var tr='',ch='';
  CH.forEach(function(c,k){
    tr+='<path class="tr" d="'+c[3]+'"/><path class="pl" pathLength="100" style="--k:'+k+'" d="'+c[3]+'"/>';
    ch+='<g class="px" data-d="'+c[4]+'"><g class="bob chip" style="--k:'+k+'"><rect x="'+c[1]+'" y="'+c[2]+'" width="84" height="46" rx="12"/>'+
        '<text x="'+(c[1]+42)+'" y="'+(c[2]+27)+'">'+c[0]+'</text>'+
        '<g class="ok" style="--k:'+k+'"><circle cx="'+(c[1]+84)+'" cy="'+c[2]+'" r="10" fill="#4FE3A2" stroke="#151813" stroke-width="2"/>'+
        '<path d="M'+(c[1]+79.5)+','+(c[2]+.5)+'l3,3.2l5.5,-6.4" fill="none" stroke="#0C0E0B" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g></g></g>';
  });
  var cpu='<circle class="ring" cx="230" cy="115" r="72"/><g class="px" data-d=".2"><g class="core"><rect class="cpu" x="190" y="75" width="80" height="80" rx="14"/>'+
          '<rect x="202" y="87" width="56" height="56" rx="8" fill="none" stroke="rgba(12,14,11,.4)"/><text class="cpu-t" x="230" y="120">CPU</text></g></g>';
  var LN=['> checking socket compatibility','> verifying power budget','> pulling live INR prices'];
  var term='<div class="fx-term" aria-hidden="true">'+LN.map(function(t,k){return '<span style="--k:'+k+';--w:'+(t.length+1)+'ch">'+t.replace('>','&gt;')+'…</span>'}).join('')+'</div>';
  var stage=mk('div','fx-stage','<svg viewBox="0 0 460 230" aria-hidden="true">'+tr+cpu+ch+'</svg>'+term);
  panel.insertBefore(stage,panel.children[1]||null);
  var px=[].slice.call(stage.querySelectorAll('.px'));

  /* staggered entrance */
  [panel,d.querySelector('.auth-form-panel')].forEach(function(p){
    if(!p) return;
    [].slice.call(p.querySelectorAll('.hud-system-badge,.branding-hud-top .badge,.brand-huge-title,.brand-tagline,.fx-stage,.tech-hud-diagram,'+
      '.form-header-box,.form-group,.auth-row-extra,#submitBtn,.auth-divider,.social-login-group,.auth-form-panel > .btn,.auth-form-panel > div:last-child'))
      .forEach(function(n,i){n.style.setProperty('--i',i);n.classList.add('fx-rise')});
  });
  var veil=d.querySelector('.fx-veil'); if(veil) setTimeout(function(){veil.remove()},900);

  /* ripples */
  d.addEventListener('pointerdown',function(e){
    var b=e.target.closest&&e.target.closest('.btn,.btn-social'); if(!b||reduce) return;
    var r=b.getBoundingClientRect(), s=Math.max(r.width,r.height)*2.2, o=mk('span','fx-ripple');
    o.style.cssText='width:'+s+'px;height:'+s+'px;left:'+(e.clientX-r.left-s/2)+'px;top:'+(e.clientY-r.top-s/2)+'px';
    b.appendChild(o); setTimeout(function(){o.remove()},650);
  });

  /* page wipe */
  var wipe=null, tx=innerWidth/2, ty=innerHeight/2;
  addEventListener('pointerdown',function(e){tx=e.clientX;ty=e.clientY},{passive:true});
  window.fxNavigate=function(url){
    if(reduce||wipe){ if(!wipe) location.href=url; return }
    wipe=mk('div','fx-wipe'); wipe.style.setProperty('--wx',tx+'px'); wipe.style.setProperty('--wy',ty+'px');
    d.body.appendChild(wipe); void wipe.offsetWidth; wipe.classList.add('go');
    setTimeout(function(){location.href=url},600);
  };
  d.addEventListener('click',function(e){
    var a=e.target.closest&&e.target.closest('a[href^="/"]');
    if(a&&!e.defaultPrevented&&!e.metaKey&&!e.ctrlKey&&a.target!=='_blank'){e.preventDefault();window.fxNavigate(a.getAttribute('href'))}
  });
  addEventListener('pageshow',function(e){if(e.persisted&&wipe){wipe.remove();wipe=null}});

})();
