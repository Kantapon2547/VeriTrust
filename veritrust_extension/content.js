const API_URL = "http://localhost:8000/predict-url";

async function scanImages() {
  const images = document.querySelectorAll("img");

  images.forEach(async (img) => {
    if (img.dataset.veritrustScanned === "true") return;
    if (!img.src || img.width < 80 || img.height < 80) return;

    img.dataset.veritrustScanned = "true";

    const wrapper = document.createElement("div");
    wrapper.className = "veritrust-wrapper";

    const badge = document.createElement("div");
    badge.className = "veritrust-badge scanning";
    badge.innerText = "Scanning...";

    img.parentNode.insertBefore(wrapper, img);
    wrapper.appendChild(img);
    wrapper.appendChild(badge);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          image_url: img.src
        })
      });

      const data = await response.json();

      badge.className = "veritrust-badge " + data.risk.toLowerCase();
      badge.innerText = `${data.label} ${(data.confidence * 100).toFixed(0)}%`;
    } catch (error) {
      badge.className = "veritrust-badge error";
      badge.innerText = "Scan failed";
    }
  });
}

scanImages();

const observer = new MutationObserver(scanImages);
observer.observe(document.body, {
  childList: true,
  subtree: true
});