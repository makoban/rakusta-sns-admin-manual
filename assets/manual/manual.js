document.querySelectorAll('.copy-button').forEach(button => button.addEventListener('click',async()=>{
  const box=button.closest('.copy-box'); const text=box.querySelector('pre').textContent;
  try{
    if(navigator.clipboard&&window.isSecureContext){await navigator.clipboard.writeText(text);}else{
      const area=document.createElement('textarea');area.value=text;area.style.position='fixed';area.style.opacity='0';document.body.append(area);area.select();if(!document.execCommand('copy'))throw new Error('copy');area.remove();
    }
    box.querySelector('.copy-status').textContent=' コピーしました';
  }catch{box.querySelector('.copy-status').textContent=' 本文を選択してコピーしてください';}
}));
const checks=[...document.querySelectorAll('[data-check]')];
const key='kokotomo-onboarding-checks:'+document.body.dataset.version+':'+location.pathname;
let saved=[];try{saved=JSON.parse(localStorage.getItem(key)||'[]');}catch{}
checks.forEach((check,i)=>{check.checked=saved.includes(i);check.addEventListener('change',()=>{try{localStorage.setItem(key,JSON.stringify(checks.flatMap((c,j)=>c.checked?[j]:[])));}catch{}});});
document.querySelector('.reset-checks')?.addEventListener('click',()=>{checks.forEach(c=>c.checked=false);try{localStorage.removeItem(key);}catch{}});
