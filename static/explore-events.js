let datetime=document.querySelector("#datetime");
let date=new Date(datetime.innerText.slice(7,26));
console.log(datetime.innerText)
datetime.innerHTML="<p class='startDate'>Date: "+date.toDateString()+"<br>Time: "+date.toLocaleTimeString()+"</br>"+datetime.innerText.slice(42,)+"</p>";
let timer=document.querySelector("#timer");
let duration=date-Date.now();
class Timer{
    constructor(d,h,m,s){
        this.days=d;
        this.hours=h;
        this.min=m;
        this.sec=s;
        this.coeff="Starts in "; 
    }

}
let cols=new Timer(Math.floor(duration / (1000 * 60 * 60 * 24)),Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60)),Math.floor((duration % (1000 * 60)) / 1000));
setInterval(function(){
    if(cols.days==0 && cols.hours==0 && cols.min==0 && cols.sec==0){
    
        cols.sec=60;
        let dur=startDates.innerText.slice(44,);
        if("minutes"==dur.slice(3,)){
            cols.min=dur.slice(0,3);
        }
        else{
            cols.hours=dur.slice(0,3);
        }
        cols.coeff="Ends in ";
        timer.style.color="red";
    }
    cols.sec--;
    if(cols.sec==-1){
        cols.sec=59;
        cols.min--;
        if(cols.min==-1){
            cols.min=59;
            cols.hours--;
        }
        if(cols.hours==-1){
            cols.hours=23;
            cols.days--;
        }
    }
   
    timer.innerText=cols.coeff+cols.days+"d "+cols.hours+"h "+cols.min+"min "+cols.sec+"s";
  
   



},1000)
