let select=document.querySelectorAll('.personselect');
let number=document.querySelector('#number');
let msg=document.querySelector('#msg');
let click=[];
class clicked{
    constructor(s,c){
        this.s=s;
        this.c=c;
    }
}
let i=0;
for(s of select){
    click[i]=new clicked(s,0);
    i++;
}
var count=0;
let disabled=0;
for(let c of click){
    c.s.addEventListener('click',()=>{
        if(count==Number(number.innerText)){
            msg.style.display='block';
            disabled=1;
        }
        if(!c.c){
            if(!disabled){
                c.s.style.background='linear-gradient(to bottom, #003399 0%, #cc33ff 100%)';
            
            c.s.innerText='Selected';
            c.c=1;
            count++;
            }
            
        }
        else{
            c.s.style.background='linear-gradient(to bottom, #00ffcc 0%, #ff99ff 100%)';
            c.s.innerText='Select';
            c.c=0;
            count--;
            disabled=0;
            msg.style.display='none';
        }
            
    })
}