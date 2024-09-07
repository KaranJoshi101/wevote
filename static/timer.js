let timer=document.querySelectorAll(".timer");
let startDates=document.querySelectorAll(".startDate");
let dat=new Date();
let cols=[];
class Timer{
    constructor(d,h,m,s){
        this.days=d;
        this.hours=h;
        this.min=m;
        this.sec=s;
        this.coeff="Starts in "; 
    }

}


var i=0;
for(const startDate of startDates){
    let ddate=new Date(startDate.innerText.slice(13,33));
    startDate.innerHTML="<p class='startDate'>Date: "+ddate.toDateString()+"<br>Time: "+ddate.toLocaleTimeString()+"<br>"+startDate.innerText.slice(33,)+"</p>";
    
    let duration=ddate-Date.now();
    cols[i] = new Timer(Math.floor(duration / (1000 * 60 * 60 * 24)),Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60)),Math.floor((duration % (1000 * 60)) / 1000))
    i++;
}
i=0;
    setInterval(function(){
        if(cols[i].days==0 && cols[i].hours==0 && cols[i].min==0 && cols[i].sec==0){
        
            cols[i].sec=60;
            let dur=startDates[i].innerText.slice(44,);
            if("minutes"==dur.slice(3,)){
                cols[i].min=dur.slice(0,3);
            }
            else{
                cols[i].hours=dur.slice(0,3);
            }
            cols[i].coeff="Ends in ";
            timer[i].style.color="red";
        }
        cols[i].sec--;
        if(cols[i].sec==-1){
            cols[i].sec=59;
            cols[i].min--;
            if(cols[i].min==-1){
                cols[i].min=59;
                cols[i].hours--;
            }
            if(cols[i].hours==-1){
                cols[i].hours=23;
                cols[i].days--;
            }
        }
       
        timer[i].innerText=cols[i].coeff+cols[i].days+"d "+cols[i].hours+"h "+cols[i].min+"min "+cols[i].sec+"s";
      
       
    
    
    i++;
    if(i==startDates.length){
        i=0;
    }
},1000/startDates.length)
    



