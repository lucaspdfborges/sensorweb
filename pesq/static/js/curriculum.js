function popitup(url,windowName) {
  newwindow=window.open(url,windowName,'height=600,width=1000');
  if (window.focus) {newwindow.focus()}
  return false;
}

closeWin()( function(){
  window.close();
}, 500);

var clicked = true;
let crossList = document.getElementsByClassName('cross');
for(var i = 0; i < crossList.length ; i++){
  crossList[i].style.display = 'table';
  crossList[i].style.display = 'none';
}

function cvEdit(){

  let crossList = document.getElementsByClassName('cross');
  let addList = document.getElementsByClassName('cv-add');
  let divItems = document.getElementsByClassName('pesq-content-item');
  let paperItems = document.getElementsByClassName('pesq-content-item2');

  if(!clicked){
    for(var i = 0; i < crossList.length ; i++){
      crossList[i].style.display = 'none';
    }
    for(var j = 0; j < addList.length; j++){
      addList[j].style.display = 'none';
    }
    for(var k = 0; k < divItems.length; k++){
      divItems[k].style.gridTemplateColumns =  '7em 40em ';
    }
    for(var m = 0; m < paperItems.length; m++){
      paperItems[m].style.gridTemplateColumns =  '7em 30em 15em ';
    }
    clicked = true;
  } else{
    for(var i = 0; i < crossList.length ; i++){
      crossList[i].style.display = 'table';
    }
    for(var j = 0; j < addList.length; j++){
      addList[j].style.display = 'table';
    }
    for(var k = 0; k < divItems.length; k++){
      divItems[k].style.gridTemplateColumns =  '2em 7em 40em ';
    }
    for(var m = 0; m < paperItems.length; m++){
      paperItems[m].style.gridTemplateColumns =  '2em 7em 30em 15em ';
    }
    clicked = false;
  }

}
