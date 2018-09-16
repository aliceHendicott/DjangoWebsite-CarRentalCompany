function LoadAnswer(answerID){
    var answerDiv = document.getElementById(answerID);
    if(answerDiv.style.display == "block"){
        answerDiv.style.display = "none";
    } else{
        answerDiv.style.display = "block";
    }
}