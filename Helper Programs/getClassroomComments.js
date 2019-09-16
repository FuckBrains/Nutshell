//Run on
var comments = document.getElementsByClassName("BsqQvc hlx3je").item(0).childNodes;
commentNum = 0;
commentsText = [];
for (let comment of comments) {
    commentsText[commentNum] = comment.childNodes[1].innerText;
	commentNum = commentNum + 1

}
commentsJson = JSON.parse('{"comments":[]}');
console.log(commentsText);