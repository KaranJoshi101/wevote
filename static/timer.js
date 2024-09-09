let timer=document.querySelectorAll(".timer");
let startTimer=document.querySelectorAll(".startTimer");
let startDates=document.querySelectorAll(".startDate");
let cols=[];
class Timer{
    constructor(d,h,m,s){
        this.days=d;
        this.hours=h;
        this.min=m;
        this.sec=s;
        this.coeff="Starts in "; 
        this.ended=0;
    }

}
//Implementing a visually acceptable starting Date and duration
    for(const startDate of startDates){
        let ddate=new Date(startDate.innerText.slice(13,33));
        startDate.innerHTML="<p class='startDate'>Date: "+ddate.toDateString()+"<br>Time: "+ddate.toLocaleTimeString()+"<br>"+startDate.innerText.slice(33,)+"</p>";
    }
    
//initiating cols
var i=0;
var duration="";
    for(const t of timer){
        cols[i]=new Timer(0,0,0,0);
        if(t.innerText.includes("Ends")){

            cols[i].coeff="Ends in ";
            duration=new Date(startTimer[i].innerText)-Date.now();
        
        }
        else{
            
            
            for(char of startTimer[i].innerText){
                if(char=='w')
                    break;
                duration+=char;
            }
            
            
            duration=new Date(duration)-Date.now();
        }

            console.log(duration);
            cols[i].days=Math.floor(duration / (1000 * 60 * 60 * 24))
            cols[i].hours=Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
            cols[i].min=Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60))
            cols[i].sec=Math.floor((duration % (1000 * 60)) / 1000);
            duration="";
        i++;
    }
    i=0;
    if(cols.length>0){
        let interval=setInterval(function(){
            if(cols[i].days==0 && cols[i].hours==0 && cols[i].min==0 && cols[i].sec==0){
                timer[i].style.color="red";

                if(cols[i].coeff=="Ends in "){
                    cols[i].ended=1;
                    timer[i].style.color="green";
                    timer[i].innerText="Event Successfully Completed";
                    clearInterval(interval);
                }
                
                cols[i].coeff="Ends in ";
                flag=0;
                for(char of startTimer[i].innerText){
                    if(char=='w'){
                        flag=1;
                        continue;
                    }
                    if(flag)
                        duration+=char;
                }
                duration=new Date(duration)-Date.now();
                cols[i].days=Math.floor(duration / (1000 * 60 * 60 * 24))
            cols[i].hours=Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
            cols[i].min=Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60))
            cols[i].sec=Math.floor((duration % (1000 * 60)) / 1000);
                
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
            if(!cols[i].ended)
            timer[i].innerText=cols[i].coeff+cols[i].days+"d "+cols[i].hours+"h "+cols[i].min+"min "+cols[i].sec+"s";
        
        
        
        
        i++;
        if(i==cols.length){
            i=0;
        }
    },1000/cols.length)
}
        
        





    