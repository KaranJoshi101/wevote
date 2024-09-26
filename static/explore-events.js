let timer=document.querySelector("#timer");
let vote=document.querySelector("#vote");
let startTimer=document.querySelector("#startTimer");
let startDate=document.querySelector("#startDate");
let exp=document.querySelector('#exp');
let VButton=document.querySelector('#VButton');
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
        if(startDate){
            let ddate=new Date(startDate.innerText.slice(13,33));
        startDate.innerHTML="<p class='startDate'>Date: "+ddate.toDateString()+"<br>Time: "+ddate.toLocaleTimeString()+"<br>"+startDate.innerText.slice(33,)+"</p>";
        }
        
    
//initiating cols
var duration="";
 if(timer){
    cols=new Timer(0,0,0,0);
        if(timer.innerText.includes("Ends")){

            cols.coeff="Ends in ";
            duration=new Date(startTimer.innerText)-Date.now();
        
        }
        else{
            
            
            for(char of startTimer.innerText){
                if(char=='w')
                    break;
                duration+=char;
            }
            
            
            duration=new Date(duration)-Date.now();
        }

            
            cols.days=Math.floor(duration / (1000 * 60 * 60 * 24))
            cols.hours=Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
            cols.min=Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60))
            cols.sec=Math.floor((duration % (1000 * 60)) / 1000);
            
    
    
        let interval=setInterval(function(){
            if(cols.days==0 && cols.hours==0 && cols.min==0 && cols.sec==0){
                timer.style.color="red";
                if(vote)
                vote.style.display="block";
                if(cols.coeff=="Ends in "){
                    
                    window.location.replace(exp.innerText);
                }
                
                cols.coeff="Ends in ";
                flag=0;
               
                duration="";
                for(char of startTimer.innerText){
                    if(char=='w'){
                        flag=1;
                        continue;
                    }
                    if(flag)
                        duration+=char;
                }
                duration=new Date(duration)-Date.now();
                cols.days=Math.floor(duration / (1000 * 60 * 60 * 24))
            cols.hours=Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
            cols.min=Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60))
            cols.sec=Math.floor((duration % (1000 * 60)) / 1000);
       
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
            if(!cols.ended)
            timer.innerText=cols.coeff+cols.days+"d "+cols.hours+"h "+cols.min+"min "+cols.sec+"s";
    },1000)
 }   
        
vote.addEventListener('click',()=>{
    window.location.replace(document.querySelector('#link').innerText);
})

VButton.addEventListener('click',()=>{
    window.location.replace(document.querySelector('#link').innerText);
})
        





    