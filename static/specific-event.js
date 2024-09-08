const myevents = document.querySelector("#myevents");
const organize=document.querySelector("#organize");
const allevents=document.querySelector("#allevents");
const myeventsbtn=document.querySelector("#myeventsbtn");
const alleventsbtn=document.querySelector("#alleventsbtn");
const organizebtn=document.querySelector("#organizebtn");
const createOne=document.querySelector("#createOne");
const cl=["active","disabled"]
myeventsbtn.addEventListener("click",()=>{
    allevents.style.display="none";
    myevents.style.display="";
    organize.style.display="none";
    alleventsbtn.classList.remove(...cl);
    myeventsbtn.classList.add(...cl);
    organizebtn.classList.remove(...cl);
    myevents.style.marginTop="50px";
})


alleventsbtn.addEventListener("click",()=>{
    allevents.style.display="block";
    myevents.style.display="none";
    organize.style.display="none";
    alleventsbtn.classList.add(...cl);
    myeventsbtn.classList.remove(...cl);
    organizebtn.classList.remove(...cl);
    allevents.style.marginTop="50px";
    
})


organizebtn.addEventListener("click",()=>{
    allevents.style.display="none";
    myevents.style.display="none";
    organize.style.display="flex";
    alleventsbtn.classList.remove(...cl);
    myeventsbtn.classList.remove(...cl);
    organizebtn.classList.add(...cl);
    organize.style.marginTop="50px";
})
createOne.addEventListener("click",()=>{
    allevents.style.display="none";
    myevents.style.display="none";
    organize.style.display="flex";
    alleventsbtn.classList.remove(...cl);
    myeventsbtn.classList.remove(...cl);
    organizebtn.classList.add(...cl);
    organize.style.marginTop="50px";
})