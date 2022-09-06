let model, streamvideo, streamctx, ctx, videoWidth, videoHeight, video, canvas, facecanvas, facectx, image;
let article, message;
let prevUtterance=null
let current = new Date();
let delay=2000;
let update = 0;
const updateInt = 30;
var iOSVoiceNames = [
  'Maged',
  'Zuzana',
  'Sara',
  'Anna',
  'Melina',
  'Karen',
  'Samantha',
  'Daniel',
  'Rishi',
  'Moira',
  'Tessa',
  'Mónica',
  'Paulina',
  'Satu',
  'Amélie',
  'Thomas',
  'Carmit',
  'Lekha',
  'Mariska',
  'Damayanti',
  'Alice',
  'Kyoko',
  'Yuna',
  'Ellen',
  'Xander',
  'Nora',
  'Zosia',
  'Luciana',
  'Joana',
  'Ioana',
  'Milena',
  'Laura',
  'Alva',
  'Kanya',
  'Yelda',
  'Tian-Tian',
  'Sin-Ji',
  'Mei-Jia'
]
var hasWindow = typeof window === 'object' && window !== null && window.self === window && window.navigator !== null;
var speech = window.speechSynthesis;
var voices=null;
var msg = new SpeechSynthesisUtterance('No warning should arise');
      msg.lang= 'en-US'
      msg.volume=1;
      msg.rate=1;
      msg.pitch=1;
  let socket=io();
window.mobileCheck = function() {
  let check = false;
  (function(a){if(/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))) check = true;})(navigator.userAgent||navigator.vendor||window.opera);
  return check;
};



async function setFrameColor(tensor) {
  let arg = tf.argMax(tensor.as1D());
  arg = await arg.array(0)

  let disp;
  console.log(arg);

  article.classList.remove('is-danger')
  article.classList.remove('is-primary')
  article.classList.remove('is-link')
  article.classList.remove('is-info')
  article.classList.remove('is-success')
  article.classList.remove('is-warning')
  switch(arg) {
    case 0:
      disp = "Angry";
      color = "is-danger";
      bgcolor="red";
      break;
    case 1:
      disp = "Disgusted";
      color = 'is-info';
      bgcolor="blue";
      break;
    case 2:
      disp = "Fear";
      color = 'is-warning';
      bgcolor="yellow";
      break
    case 3:
      disp = "Happy";
      color = 'is-success';
      bgcolor="green";
      break
    case 4:
      disp = "Sad";
      color = 'is-info';
      bgcolor="blue";
      break;
    case 5:
      disp = "Surprise";
      color = 'is-warning';
      bgcolor="orange";
      break
    case 6:
      disp = "Neutral";
      bgcolor="white"
      break
    default:
      disp = "looking...";
      break;
  }
  message.innerHTML = disp;
  if(typeof color !== "undefined"){
    article.classList.add(color);
  }
  //var msg = new SpeechSynthesisUtterance();
    //  msg.text = disp;
     // window.speechSynthesis.speak(msg);
  socket.emit('emotion', {emotion:disp,color:bgcolor});
  //document.body.style.backgroundColor ='brown'
  delete tensor1d
  delete arg
}

async function setupCamera() {
  article = document.getElementById("vidarticle");
  message = document.getElementById("message");

  video = document.getElementById("video");

  const stream = await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: { facingMode: "user" },
  });
  video.srcObject = stream;

  return new Promise((resolve) => {
    video.onloadedmetadata = () => {
      resolve(video);
    };
  });
}


const renderPrediction = async () => {
  const returnTensors = false;
  const draw = false;
  const flipHorizontal = false;
  const annotateBoxes = false;
  const predictions = await model.estimateFaces(
    video,
    returnTensors,
    flipHorizontal,
    annotateBoxes
  );
 

  if (predictions.length > 0) {
    update++;
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < predictions.length; i++) {
      if (returnTensors) {
        predictions[i].topLeft = predictions[i].topLeft.arraySync();
        predictions[i].bottomRight = predictions[i].bottomRight.arraySync();
        if (annotateBoxes) {
          predictions[i].landmarks = predictions[i].landmarks.arraySync();
        }
      }

      const start = predictions[i].topLeft;
      const end = predictions[i].bottomRight;
      const size = [end[0] - start[0], end[1] - start[1]];
 
      
      if (draw) {
        ctx.beginPath();
        ctx.lineWidth = "6";
        ctx.strokeStyle = "red";
        ctx.rect(640-end[0], start[1], size[0], size[1]);
        ctx.stroke();
      }

      frame = video;
      streamctx.drawImage(video, 0, 0)
      
      facectx.drawImage( 
        streamcanvas, // source 
        end[0], start[1], // sx, sy,
        start[0]-end[0], end[1]-start[1], //sWidth, sHeight
        0, 0, // dx, dy
        48, 48, // dWidth, dHeight
      )

      if (update%updateInt === 0) {
        update = 0;
        const res = await classify(facecanvas);
        setFrameColor(res);
        delete res;
      }


      if (annotateBoxes) {
        const landmarks = predictions[i].landmarks;

        ctx.fillStyle = "blue";
        for (let j = 0; j < landmarks.length; j++) {
          const x = landmarks[j][0];
          const y = landmarks[j][1];
          ctx.fillRect(x, y, 5, 5);
        }
      }
    }
  }
  //console.log("outside"+(new Date()).getTime());
  //setTimeout((video) => {
 //   console.log("inside timer"+(new Date()).getTime());
  //  var x=video;
    video.requestVideoFrameCallback(renderPrediction);
 // }, delay);
};

const setupPage = async () => {
  image = document.getElementById('img');
  await setupCamera();
  video.play();

  videoWidth = video.videoWidth;
  videoHeight = video.videoHeight;
  video.width = videoWidth;
  video.height = videoHeight;

  facecanvas = document.getElementById("face")
  facecanvas.width =  48;
  facecanvas.height =  48;
  facectx = facecanvas.getContext("2d");

  streamcanvas = document.getElementById("videostream")
  streamcanvas.width = videoWidth;
  streamcanvas.height = videoHeight;
  streamctx = streamcanvas.getContext("2d");
  streamctx.fillStyle = "rgba(255, 0, 0, 0.5)";

  canvas = document.getElementById("output");
  canvas.width = videoWidth;
  canvas.height = videoHeight;
  ctx = canvas.getContext("2d");
  ctx.fillStyle = "rgba(255, 0, 0, 0.5)";

  model = await blazeface.load();
  emotimodel = await load();

  
  video.requestVideoFrameCallback(renderPrediction);
};

let emotimodel;
async function load() {
  return await tf.loadLayersModel("static/model.json");
}

async function classify(img) {
  const tensor = await tf.browser.fromPixels(img,1).expandDims(0)
  const offset = tf.scalar(127.5);
  // Normalize the image from [0, 255] to [-1, 1].
  const normalized = tensor.sub(offset).div(offset);
  const res =  await emotimodel.predict(normalized);
  document.getElementById("pred").innerHTML = res.as1D();
  
  return res;
}
function setSpeech() {
  return new Promise(
      function (resolve, reject) {
          let synth = window.speechSynthesis;
          let id;

          id = setInterval(() => {
              if (synth.getVoices().length !== 0) {
                  resolve(synth.getVoices());
                  clearInterval(id);
              }
          }, 10);
      }
  )
}

async function init(){
//Load all the voices, load the page after the voices are loaded
  var _voices=setSpeech();

  _voices.then((data) => {
    voices=data;
    preload();
  }); 
}

async function preload(){
  //Attach click event on the button
  document.getElementById('speech').addEventListener('click', function(e) {
    msg.voiceURI=voices[0].voiceURI;
    msg.text=document.getElementById('emotionText').innerHTML;
    window.speechSynthesis.speak(msg);
  });
  //establish socket connection
  socket.on('connect', () => {
    console.log("socket is connected")
    socket.on('emotion', (val) => {
      document.getElementById('speech').click();
      document.body.style.backgroundColor=val.color;document.getElementById('emotionText').innerHTML = val.emotion;
    })

    socket.onAny((event, ...args) => {
     console.log(event, args);  
    });
   });

   // initially hide the UI, based on the device show the corresponding ui
const isMobile = window.mobileCheck();
console.log("device is mobile:"+isMobile);
if(isMobile){
 document.getElementById('mobile').style.visibility = "visible" ;
 }
else{
   document.getElementById('vidarticle').style.visibility="visible";
   socket.emit('test','hi')
   load();
   setupPage();
 }

}

init();
