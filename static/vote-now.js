let select=document.querySelectorAll('.personselect');
let number=document.querySelector('#number');
let msg=document.querySelector('#msg');

let mbody=document.querySelector('#mbody');
let voted=document.querySelector('#voted');
let click=[];
class clicked{
    constructor(l,c,f){
        this.f=f;
        this.c=c;
        this.l=l;
    }
}
let i=0;
for(s of select){
    click[i]=new clicked(s.lastElementChild,0,s.firstElementChild);
    i++;
}
var count=0;
var sCand=[]
let disabled=0;
for(let c of click){
    c.l.addEventListener('click',()=>{
        if(c.l.innerText=='Select' && count==Number(number.innerText)){
            msg.style.display='block';
            disabled=1;
        }
        if(!c.c){
            if(!disabled){
                c.l.style.background='linear-gradient(to bottom, #003399 0%, #cc33ff 100%)';
            
            c.l.innerText='Selected';
            c.c=1;
            
            sCand.push(c.f);
            count++;
            vbutton.classList.remove('disabled');
            }
            
        }
        else{
            c.l.style.background='linear-gradient(to bottom, #00ffcc 0%, #ff99ff 100%)';
            c.l.innerText='Select';
            c.c=0;
            sCand=sCand.toSpliced(sCand.indexOf(c.f),1);
            console.log(sCand);
            count--;
            disabled=0;
            msg.style.display='none';
            if(count==0){
                vbutton.classList.add('disabled');
            }
        }
            
    })
}
vbutton.addEventListener("click",()=>{
    if(count<=Number(number.innerText)){
        mbody.innerHTML='';
        voted.value='';
        for(let i =0;i<sCand.length;i++){
            let b=sCand[i].childNodes[0];
            let name=sCand[i].childNodes[1];
            mbody.innerHTML+='<div><div class="row flex-lg-row align-items-center py-2 border rounded"> <div class="col-lg-10"><div class="d-flex justify-content-between align-items-center"><div><h6 class="fw-bold">Ballot No. - '+b.innerText+'</h6><p class="fs-5 fw-bold text-body-emphasis lh-1">'+name.innerText+'<p></div></div></div></div></div>';
            voted.value+=' '+sCand[i].childNodes[2].innerText;
            }
    }
        
})