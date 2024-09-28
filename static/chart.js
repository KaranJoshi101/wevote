const n1=document.querySelectorAll('.name');

const c1=document.querySelectorAll('.count');

class n{
    constructor(name,count){
      this.name=name;
      this.count=count;
    }
}
let oth=0;
let rec=[]
for(let i=0;i<n1.length;i++){
    if(c1[i].innerText>10)
    rec.push(new n(n1[i].innerText,c1[i].innerText));
    else
    oth+=c1[i].innerText;
}
var xValues=[];
var yValues=[];

for(let i of rec){
    xValues.push(i.name);
    yValues.push(i.count);
}
xValues.push("Others")
yValues.push(oth);

var barColors=["#06C","#C9190B","#EF9234","#4CB140","#009596","#5752D1","#F4C145","#EC7A08","#7D1007","#B8BBBE"].slice(0,xValues.length);
new Chart("myChart", {
type: "pie",
data: {
  labels: xValues,
  datasets: [{
    backgroundColor: barColors,
    data: yValues
  }]
},
options: {
  title: {
    display: true,
    text: "Vote Share(in %)"
  }
}
});