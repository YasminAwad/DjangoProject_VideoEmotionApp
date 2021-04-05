function myFunction() {
      document.getElementById("myDropdown").classList.toggle("show");
}

    // Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

var video = document.getElementById("video");
var playButton = document.getElementById("play-pause");
var mutebtn = document.getElementById("mutebtn");
var  volumeslider = document.getElementById("volumeslider");
var reload = document.getElementById("reload");
var fullScreenButton = document.getElementById("full-screen");

var curtimetext = document.getElementById("curtimetext");
var durtimetext = document.getElementById("durtimetext");

var  em = document.getElementById("em");
var question = document.getElementById("question");
var text = document.getElementById("testo")

var a = document.getElementById("1");
var b = document.getElementById("2");
var c = document.getElementById("3");
var d = document.getElementById("4");
var e = document.getElementById("5");
var f = document.getElementById("6");
var g = document.getElementById("7");

var emoji = document.getElementById("emoji");

var modal = document.getElementById("myModal");
var btn = document.getElementById("modelP");
var x = document.getElementById("close"); /*da rivedere*/

var loading = document.getElementById("loading");
var loading2 = document.getElementById("loading2");

var docElm = document.documentElement;

var interval ;
var timeOut;
var timeOut2;
var emotionData;
var response;
 var eArray = [];

var bpause = 0;
var restTimeout;
var restTime;

var sequence = 0;

window.onload = function() {
    playButton = document.getElementById("play-pause");
    curtimetext = document.getElementById("curtimetext");
    durtimetext = document.getElementById("durtimetext");
    video = document.getElementById("video");
    reload = document.getElementById("reload");
    mutebtn = document.getElementById("mutebtn");
    volumeslider = document.getElementById("volumeslider");
    em = document.getElementById("em");
    question = document.getElementById("question");
    emoji = document.getElementById("emoji");

    a = document.getElementById("1");
    b = document.getElementById("2");
    c = document.getElementById("3");
    d = document.getElementById("4");
    e = document.getElementById("5");
    f = document.getElementById("6");
    g = document.getElementById("7");

    text = document.getElementById("testo")
    fullScreenButton = document.getElementById("full-screen");
    closeFS  = document.getElementById("closeFS");
    modal = document.getElementById("myModal");
    btn = document.getElementById("modelP");
    x= document.getElementById("close");

    loading = document.getElementById("loading");
    loading2 = document.getElementById("loading2");

};

// Event listener for the play/pause button
playButton.addEventListener("click", function(){ play(); });
playButton.addEventListener("touch", function(){ play(); });

a.addEventListener("click", function() {response = eArray[0]; responseFunction(response); });
a.addEventListener("touch", function() {  response = eArray[0]; responseFunction(response); });
b.addEventListener("click", function(){ response = eArray[1]; responseFunction(response); });
b.addEventListener("touch", function(){ response = eArray[1]; responseFunction(response); });
c.addEventListener("click", function() { response = eArray[2]; responseFunction(response); });
c.addEventListener("touch", function() { response = eArray[2]; responseFunction(response); });
d.addEventListener("click", function(){ response = eArray[3]; responseFunction(response); });
d.addEventListener("touch", function(){ response = eArray[3]; responseFunction(response); });
e.addEventListener("click", function() {response = eArray[4];  responseFunction(response); });
e.addEventListener("touch", function() {response = eArray[4];  responseFunction(response); });
f.addEventListener("click", function(){ response = eArray[5]; responseFunction(response); });
f.addEventListener("touch", function(){ response = eArray[5]; responseFunction(response); });
g.addEventListener("click", function() { response = eArray[6]; responseFunction(response); });
g.addEventListener("touch", function() { response = eArray[6]; responseFunction(response); });

mutebtn.addEventListener("click", function(){
  if(video.muted){
    video.muted = false;
    mutebtn.innerHTML = "Mute";
  }else{
    video.muted = true;
    mutebtn.innerHTML = "Unmute";
  }
});

volumeslider.addEventListener("change",function(){
  video.volume = volumeslider.value / 100;
});

video.addEventListener("timeupdate", function() {
  var curmins = Math.floor(video.currentTime / 60);
  var cursecs = Math.floor(video.currentTime - curmins * 60);
  var durmins = Math.floor(video.duration / 60);
  var dursecs = Math.floor(video.duration - durmins * 60);
  if(cursecs < 10){ cursecs = "0"+cursecs; }
  if(dursecs < 10){ dursecs = "0"+dursecs; }
  if(curmins < 10){ curmins = "0"+curmins; }
  if(durmins < 10){ durmins = "0"+durmins; }

  curtimetext.innerHTML = curmins+":"+cursecs;
  durtimetext.innerHTML = durmins+":"+dursecs;

  if(cursecs==dursecs && curmins==durmins){
      location.reload(true);
  }
});

reload.addEventListener("click", function() {
    location.reload(true);
});

fullScreenButton.addEventListener("click", function() {


var isInFullScreen = (document.fullscreenElement && document.fullscreenElement !== null) ||
       (document.webkitFullscreenElement && document.webkitFullscreenElement !== null) ||
       (document.mozFullScreenElement && document.mozFullScreenElement !== null) ||
       (document.msFullscreenElement && document.msFullscreenElement !== null);

   var docElm = document.documentElement;
   if (!isInFullScreen) {

       fullScreenButton.innerHTML = '】【'
       if (docElm.requestFullscreen) {
           docElm.requestFullscreen();
       } else if (docElm.mozRequestFullScreen) {
           docElm.mozRequestFullScreen();
       } else if (docElm.webkitRequestFullScreen) {
           docElm.webkitRequestFullScreen();
       } else if (docElm.msRequestFullscreen) {
           docElm.msRequestFullscreen();
       }
   } else {
           fullScreenButton.innerHTML = '【 】'
       if (document.exitFullscreen) {
           document.exitFullscreen();
       } else if (document.webkitExitFullscreen) {
           document.webkitExitFullscreen();
       } else if (document.mozCancelFullScreen) {
           document.mozCancelFullScreen();
       } else if (document.msExitFullscreen) {
           document.msExitFullscreen();
       }
   }

 });

// HOME
btn.onclick = function() { modal.style.display = "block"; }

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function play(){
    var response
    var currentTime
    var duration =  Math.floor(video.duration);

/*--PLAY--*/
      if(video.paused == true){
          video.play();
          playButton.innerHTML = 'Pause';
          loading.style.display = 'block';
          loading2.style.display = 'block';
          restTime = Math.floor(20-bpause)*1000;
          currentTime =  Math.floor(video.currentTime); //  emoji.src = 'static/sad.gif';
          restTimeout = setTimeout(function(){   //dopo 12 sec sparisce la domanda
              intervalFunction();
              interval = setInterval(function(){    // rileva emozioni ogni 20 sec
                  intervalFunction();
              }, 20000);

          }, restTime);

    /*--PAUSA--*/
      }else{
          video.pause();
          loading.style.display = 'none';
          loading2.style.display = 'none';
          bpause = Math.floor(video.currentTime)%20;
          currentTime =  Math.floor(video.duration);
          videofermo = 1;
          playButton.innerHTML = 'Play';

          clearTimeout(restTimeout);
          clearInterval(interval);
      }

      /*--EMOTION-RECOGNIZER--*/
      $.ajax({
        type: "GET",
        url: "/emotion",
        data: {
           'duration': duration,
           'currentTime': currentTime,
       }
   });
}

function responseFunction(response){
      clearTimeout(timeOut);
      time = Math.floor(video.duration/20);
      question.style.display = 'none';
      emoji.style.display = 'none';
      loading.style.display = 'block';
      loading2.style.display = 'block';

      $.ajax({
        type: "GET",
        url: "/saveData",
        data: {
          'idV':idV,     //idVideo
          'titleV': titleV,
          'sequence': sequence,
          'response' : response,
          'time': time,
        }
      });
      console.log(sequence);

      $.ajax({
        type: "GET",
        url: "/saveStat",
        data: {
          'idV':idV,     //idVideo
          'sequence': sequence,
          'response' : response,
        }
      });

  }

function intervalFunction(){
    // rileva emozioni ogni 20 sec
    $.ajax({
        type: "GET",
        url: "/emotionReading",
        success: function(data){
          //  time = Math.floor(video.currentTime);
            sequence = sequence +  1;
            question.style.display = 'block';
            emoji.style.display = 'block';
             loading.style.display = 'none';
             loading2.style.display = 'none';
             eArray = [];
             nArray = [];
             var obj = JSON.parse(data);

             for (var key in obj){
                   eArray.push(key);
                   nArray.push(obj[key]);
               }

             text.innerHTML = 'Sei' +' '+eArray[0] +'?';
             a.innerHTML = eArray[0] + ': ' +  nArray[0]+'%';
             b.innerHTML = eArray[1] + ': ' +  nArray[1]+'%';
             c.innerHTML = eArray[2] + ': ' +  nArray[2]+'%';
             d.innerHTML = eArray[3] + ': ' +  nArray[3]+'%';
             e.innerHTML = eArray[4] + ': ' +  nArray[4]+'%';
             f.innerHTML = eArray[5] + ': ' +  nArray[5]+'%';
             g.innerHTML = eArray[6] + ': ' +  nArray[6]+'%';

            if(eArray[0] == 'triste'){ emoji.src = 'static/emoji/sad.gif'; }
            if(eArray[1] == 'arrabbiato'){ emoji.src = 'static/emoji/angry.gif'; }
            if(eArray[2] == 'impaurito'){ emoji.src = 'static/emoji/fear.gif'; }
            if(eArray[3] == 'felice'){ emoji.src = 'static/emoji/happy.gif'; }
            if(eArray[4] == 'annoiato'){ emoji.src = 'static/emoji/bored.gif'; }
            if(eArray[5] == 'sorpreso'){ emoji.src = 'static/emoji/surprise.gif'; }
            if(eArray[6] == 'disgustato'){ emoji.src = 'static/emoji/disgust.gif'; }

timeOut = setTimeout(function(){   //dopo 12 sec sparisce la domanda
                response = 'NULL'
                question.style.display ='none';
                emoji.style.display = 'none';
                loading.style.display = 'block';
                loading2.style.display = 'block';
                $.ajax({
                    type: "GET",
                    url: "/saveData",
                    data: {
                        'idV':idV,     //idVideo
                        'data' : eArray[0],  //emozione
                        'sequence': sequence,
                        'response' : response,
                    }
                })
            }, 12000);
        }
    });
}
