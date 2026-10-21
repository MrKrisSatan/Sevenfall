(() => {
  const cards=[...document.querySelectorAll('.turn-card')];
  const form=document.getElementById('turn-filters'),search=document.getElementById('turn-search'),faction=document.getElementById('turn-faction'),category=document.getElementById('turn-category');
  const params=new URLSearchParams(location.search);
  for(const [control,key] of [[faction,'faction'],[category,'type']])if([...control.options].some(o=>o.value===params.get(key)))control.value=params.get(key);
  search.value=params.get('q')||'';
  function filter(){
    let count=0;const q=search.value.trim().toLowerCase();
    for(const card of cards){card.hidden=!((faction.value==='all'||card.dataset.faction===faction.value)&&(category.value==='all'||card.dataset.category===category.value)&&card.textContent.toLowerCase().includes(q));if(!card.hidden)count++;}
    document.getElementById('turn-count').textContent=`${count} unit ${count===1?'design':'designs'} · ${count*8} views`;
    document.getElementById('turn-empty').hidden=count!==0;
    const next=new URLSearchParams();if(faction.value!=='all')next.set('faction',faction.value);if(category.value!=='all')next.set('type',category.value);if(q)next.set('q',search.value.trim());
    history.replaceState(null,'',location.pathname+(next.size?'?'+next:'')+location.hash);
  }
  form.addEventListener('submit',e=>e.preventDefault());form.addEventListener('reset',e=>{e.preventDefault();search.value='';faction.value='all';category.value='all';filter();});
  search.addEventListener('input',filter);faction.addEventListener('change',filter);category.addEventListener('change',filter);form.hidden=false;filter();
  const names=['North','Northeast','East','Southeast','South','Southwest','West','Northwest'],short=['N','NE','E','SE','S','SW','W','NW'];
  const dialog=document.getElementById('turn-dialog'),stage=document.getElementById('turn-stage'),choices=document.getElementById('turn-directions');
  let index=3,opener,selected;
  function show(){
    stage.style.backgroundPosition=`${(index%4)/3*100}% ${Math.floor(index/4)*100}%`;
    stage.setAttribute('aria-label',selected.dataset.name+' facing '+names[index].toLowerCase());
    document.getElementById('turn-facing').textContent=names[index];
    [...choices.children].forEach((b,i)=>b.setAttribute('aria-pressed',String(i===index)));
    document.getElementById('turn-download').href=`https://github.com/MrKrisSatan/Sevenfall/blob/main/art/unit-turnarounds/frames/${selected.closest('article').id}/${short[index].toLowerCase()}.png`;
  }
  names.forEach((name,i)=>{const b=document.createElement('button');b.type='button';b.textContent=short[i];b.setAttribute('aria-label',name);b.addEventListener('click',()=>{index=i;show();});choices.append(b);});
  document.querySelectorAll('.turn-open').forEach(button=>button.addEventListener('click',()=>{
    selected=button;opener=button;index=3;
    document.getElementById('turn-title').textContent=button.dataset.name;
    document.getElementById('turn-detail').textContent=button.closest('article').querySelector('.turn-status').textContent;
    stage.style.backgroundImage=`url("${button.querySelector('img').getAttribute('src')}")`;
    show();dialog.showModal();
  }));
  document.getElementById('turn-previous').addEventListener('click',()=>{index=(index+7)%8;show();});
  document.getElementById('turn-next').addEventListener('click',()=>{index=(index+1)%8;show();});
  dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();index=(index+(e.key==='ArrowLeft'?7:1))%8;show();}});
  dialog.querySelector('.dialog-close').addEventListener('click',()=>dialog.close());
  dialog.addEventListener('close',()=>opener?.focus());
  dialog.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
})();
