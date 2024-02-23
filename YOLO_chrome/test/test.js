import html2canvas from 'html2canvas';


let previousScroll = 0;
const scrollThreshold = 100;
const targetElement = document.body; 


window.addEventListener('scroll', async () => {
  const currentScroll = window.scrollY;
  const scrolled = Math.abs(currentScroll - previousScroll);

  if (scrolled >= scrollThreshold) {
    try {
      // Capture screenshot using html2canvas
      const canvas = await html2canvas(targetElement);

      // Convert canvas to image data and prepare YOLOv8 input
      const imageData = canvas.toDataURL('imagedpbh/jpeg');
      const img = new Image();
      img.src = imageData;
      const resizedImage = await tf.browser.fromPixels(img, 3);
      const preprocessedImage = tf.image.resizeBilinear(resizedImage, modelInputSize);

      // Perform object detection with YOLOv8
    //   const detections = await model.predict(preprocessedImage.expandDims(0));

      // Visualize detections using Fabric.js (example)
    //   clearCanvas(canvas);
      downloadImage(canvas);
      console.log('ss taken')
      const context = canvas.getContext('2d');
   
    } catch (error) {
      console.error('Error during object detection:', error);
    }

    previousScroll = currentScroll; // Update for next check
  }
});


function downloadImage(canvas) {
    const imgData = canvas.toDataURL('image/png');
    const anchor = document.createElement('a');
    anchor.download = 'my-screenshot-dpbh.png'; // Set desired filename
    anchor.href = imgData;
    anchor.click();
}
