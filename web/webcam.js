var canvas;
var ctx;
var video;
var webcamWidth;
var webcamHeight;

navigator.getUserMedia =
  navigator.getUserMedia ||
  navigator.webkitGetUserMedia ||
  navigator.mozGetUserMedia ||
  navigator.msGetUserMedia;

var ws = new WebSocket("ws://localhost:5000/ws");
ws.binaryType = "arraybuffer";

ws.onmessage = function (event) {
  const blob = b64toBlob(event.data, "image/jpeg");
  const blobUrl = URL.createObjectURL(blob);
  document.getElementById("my-data-uri").src = blobUrl;
};

function sendMessage(img) {
  ws.send(img);
}

function startWebcam() {
  canvas = document.createElement("canvas");
  video = document.createElement("video");
  video.setAttribute("autoplay", true);
  ctx = canvas.getContext("2d");

  if (navigator.getUserMedia) {
    navigator.getUserMedia(
      {
        video: true,
        audio: false,
      },

      function (stream) {
        webcamWidth = stream.getVideoTracks()[0].getSettings().width;
        webcamHeight = stream.getVideoTracks()[0].getSettings().height;
        canvas.setAttribute("width", webcamWidth);
        canvas.setAttribute("height", webcamHeight);

        // video.src = window.URL.createObjectURL(localMediaStream);
        video.srcObject = stream;
      },

      function (err) {
        console.log(err);
      }
    );
  } else {
    console.log("getUserMedia not supported by your browser");
  }
  setInterval(getCurrentFrame, 100);
}

function getCurrentFrame() {
  ctx.drawImage(video, 0, 0);
  img_dataURI = canvas.toDataURL("image/png");
  sendMessage(img_dataURI);
}

const b64toBlob = (b64Data, contentType = "", sliceSize = 512) => {
  const byteCharacters = atob(b64Data);
  const byteArrays = [];

  for (let offset = 0; offset < byteCharacters.length; offset += sliceSize) {
    const slice = byteCharacters.slice(offset, offset + sliceSize);

    const byteNumbers = new Array(slice.length);
    for (let i = 0; i < slice.length; i++) {
      byteNumbers[i] = slice.charCodeAt(i);
    }

    const byteArray = new Uint8Array(byteNumbers);
    byteArrays.push(byteArray);
  }

  const blob = new Blob(byteArrays, { type: contentType });
  return blob;
};
