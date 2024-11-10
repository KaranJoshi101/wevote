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
    text: "Vote Share(in %)",
    responsive: false,
    maintainAspectRatio: true
  }
}
});

document.getElementById("downloadPDF").addEventListener("click", function () {
  // Select the element with class name "result-table"
  var element = document.querySelector(".result-table");

  // Options for the PDF, with landscape orientation
  var options = {
      margin:       0.5, // Margin around the content
      filename:     'Event_result.pdf', // Filename for the PDF
      image:        { type: 'jpeg', quality: 0.98 },
      html2canvas:  { 
      scale: 2,         // Adjust canvas scale for better quality
      scrollY: 0,       // Ensure the full content is rendered
      useCORS: true,    // Handle cross-origin content like images
    }, 
      jsPDF:        { unit: 'in', format: 'a4', orientation: 'landscape' } // Landscape PDF
  };

  // Generate and download the PDF from the selected element
  html2pdf().set(options).from(element).save();
});