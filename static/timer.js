let timer=document.querySelectorAll(".timer");
let startDates=document.querySelectorAll(".startDate");
let dat=new Date();
let cols=[];

for(let i=0;i<startDates.length;i++){
     cols[i]=[1,2,3,4];
}

console.log(typeof cols);
var i=0;
for(const startDate of startDates){
    
    let sdat=new Date(startDate.innerText.slice(13,33));
    let duration=sdat-Date.now();
    cols[i][3] = Math.floor(duration / (1000 * 60 * 60 * 24));
    cols[i][2] = Math.floor((duration % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    cols[i][1] = Math.floor((duration % (1000 * 60 * 60)) / (1000 * 60));
    cols[i][0] = Math.floor((duration % (1000 * 60)) / 1000);
    i++;
}
i=0;
    setInterval(function(){
    
        cols[i][0]--;
        if(cols[i][0]==-1){
            cols[i][0]=59;
            cols[i][1]--;
            if(cols[i][1]==-1){
                cols[i][1]=59;
                cols[i][2]--;
            }
            if(cols[i][2]==-1){
                cols[i][2]=23;
                cols[i][3]--;
            }
        }
        timer[i].innerText="Starts in "+cols[i][3]+"d "+cols[i][2]+"h "+cols[i][1]+"min "+cols[i][0]+"s";
       
    
    
    i++;
    if(i==startDates.length){
        i=0;
    }
},1000/startDates.length)
    



