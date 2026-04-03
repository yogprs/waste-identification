document.addEventListener("DOMContentLoaded", async () => {
  const video = document.getElementById("video");
  const captureBtn = document.getElementById("capture");
  const canvas = document.getElementById("canvas");
  const select = document.getElementById("cameraSelect");

  let currentStream;

  // 🔹 Ambil daftar kamera
  async function getCameras() {
    const devices = await navigator.mediaDevices.enumerateDevices();
    const cameras = devices.filter((d) => d.kind === "videoinput");

    select.innerHTML = "";
    cameras.forEach((camera, index) => {
      const option = document.createElement("option");
      option.value = camera.deviceId;
      option.text = camera.label || `Camera ${index + 1}`;
      select.appendChild(option);
    });
  }

  // 🔹 Nyalakan kamera
  async function startCamera(deviceId = null) {
    try {
      if (currentStream) {
        currentStream.getTracks().forEach((track) => track.stop());
      }

      // const constraints = {
      //   video: deviceId ? { deviceId: { exact: deviceId } } : true,
      // };

      const constraints = {
        video: deviceId
          ? { deviceId: { exact: deviceId } }
          : { facingMode: { ideal: "environment" } }, // default kamera belakang
        audio: false, // kalau tidak perlu audio
      };

      const stream = await navigator.mediaDevices.getUserMedia(constraints);
      video.srcObject = stream;
      currentStream = stream;
    } catch (e) {
      console.error("Gagal akses kamera:", e);
      alert("Tidak bisa mengakses kamera: " + e.message);
    }
  }

  // 🔹 Saat pilih kamera
  select.addEventListener("change", () => {
    startCamera(select.value);
  });

  // 🔹 Capture gambar
  captureBtn.addEventListener("click", () => {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const ctx = canvas.getContext("2d");
    ctx.drawImage(video, 0, 0);

    const image = canvas.toDataURL("image/png");
    console.log(image);

    // nanti bisa dikirim ke Flask
  });

  // 🔥 INIT
  await getCameras();
  await startCamera();
});
