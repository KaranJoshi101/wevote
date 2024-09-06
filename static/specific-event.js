about = document.querySelector("#about")
console.dir(about)
aboutbtn=document.querySelector("#aboutbtn")
console.dir(aboutbtn)
const cl=["active","disabled"]
aboutbtn.addEventListener("click",()=>{
    candidates.style.display="none";
    about.style.display="inline";
    result.style.display="none";
    candidatesbtn.classList.remove(...cl);
    aboutbtn.classList.add(...cl);
    resultbtn.classList.remove(...cl);
})
candidates=document.querySelector("#candidates")
console.dir(candidates)
candidatesbtn=document.querySelector("#candidatesbtn")
console.dir(candidatesbtn)
candidatesbtn.addEventListener("click",()=>{
    candidates.style.display="inline";
    about.style.display="none";
    result.style.display="none";
    candidatesbtn.classList.add(...cl);
    aboutbtn.classList.remove(...cl);
    resultbtn.classList.remove(...cl);

    
})
result=document.querySelector("#result")
console.dir(result)
resultbtn=document.querySelector("#resultbtn")
console.dir(resultbtn)
resultbtn.addEventListener("click",()=>{
    candidates.style.display="none";
    about.style.display="none";
    result.style.display="inline";
    candidatesbtn.classList.remove(...cl);
    aboutbtn.classList.remove(...cl);
    resultbtn.classList.add(...cl);
})