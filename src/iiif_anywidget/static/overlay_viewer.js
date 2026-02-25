function loadOpenSeadragon() {
  if (window.OpenSeadragon) {
    return Promise.resolve(window.OpenSeadragon);
  }

  return new Promise((resolve, reject) => {
    const existing = document.querySelector('script[data-osd="1"]');
    if (existing) {
      existing.addEventListener("load", () => resolve(window.OpenSeadragon), { once: true });
      existing.addEventListener("error", () => reject(new Error("Failed to load OpenSeadragon")), { once: true });
      return;
    }

    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/openseadragon@5.0.0/build/openseadragon/openseadragon.min.js";
    script.dataset.osd = "1";
    script.onload = () => resolve(window.OpenSeadragon);
    script.onerror = () => reject(new Error("Failed to load OpenSeadragon"));
    document.head.appendChild(script);
  });
}

function parseRectangles(csvText) {
  if (typeof csvText !== "string") {
    return [];
  }

  const rows = csvText
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter((line) => line.length > 0);

  const rectangles = [];

  for (const row of rows) {
    const parts = row.split(",").map((value) => value.trim());
    if (parts.length !== 4) {
      continue;
    }

    const [xRaw, yRaw, widthRaw, heightRaw] = parts;
    const x = Number.parseFloat(xRaw);
    const y = Number.parseFloat(yRaw);
    const width = Number.parseFloat(widthRaw);
    const height = Number.parseFloat(heightRaw);

    if (![x, y, width, height].every(Number.isFinite)) {
      continue;
    }

    if (x < 0 || x > 1 || y < 0 || y > 1 || width <= 0 || width > 1 || height <= 0 || height > 1) {
      continue;
    }

    if (x + width > 1 || y + height > 1) {
      continue;
    }

    rectangles.push({ x, y, width, height });
  }

  return rectangles;
}

function render({ model, el }) {
  const container = document.createElement("div");
  container.style.width = "100%";
  container.style.height = "500px";
  el.appendChild(container);

  let viewer;
  let overlays = [];
  let stopUrlListening = () => {};
  let stopRectsListening = () => {};

  const clearOverlays = () => {
    if (!viewer) {
      return;
    }
    for (const overlay of overlays) {
      viewer.removeOverlay(overlay);
    }
    overlays = [];
  };

  const drawOverlays = () => {
    if (!viewer || !viewer.world || viewer.world.getItemCount() === 0) {
      return;
    }

    clearOverlays();

    const tiledImage = viewer.world.getItemAt(0);
    if (!tiledImage) {
      return;
    }

    const contentSize = tiledImage.getContentSize();
    const imageWidth = contentSize.x;
    const imageHeight = contentSize.y;
    const rectangles = parseRectangles(model.get("rectangles_csv") || "");

    for (const rectangle of rectangles) {
      const pixelX = rectangle.x * imageWidth;
      const pixelY = rectangle.y * imageHeight;
      const pixelWidth = rectangle.width * imageWidth;
      const pixelHeight = rectangle.height * imageHeight;

      const viewportRect = tiledImage.imageToViewportRectangle(pixelX, pixelY, pixelWidth, pixelHeight);
      const overlayElement = document.createElement("div");
      overlayElement.style.border = "2px solid #d11f1f";
      overlayElement.style.boxSizing = "border-box";
      overlayElement.style.pointerEvents = "none";

      viewer.addOverlay({
        element: overlayElement,
        location: viewportRect,
      });
      overlays.push(overlayElement);
    }
  };

  loadOpenSeadragon().then((OpenSeadragon) => {
    viewer = OpenSeadragon({
      element: container,
      prefixUrl: "https://cdn.jsdelivr.net/npm/openseadragon@5.0.0/build/openseadragon/images/",
    });

    const openFromModel = () => {
      const url = model.get("url");
      if (url) {
        viewer.open(url);
      } else {
        clearOverlays();
      }
    };

    viewer.addHandler("open", drawOverlays);

    openFromModel();
    model.on("change:url", openFromModel);
    model.on("change:rectangles_csv", drawOverlays);
    stopUrlListening = () => model.off("change:url", openFromModel);
    stopRectsListening = () => model.off("change:rectangles_csv", drawOverlays);
  });

  return () => {
    stopUrlListening();
    stopRectsListening();
    clearOverlays();
    if (viewer) {
      viewer.destroy();
    }
    container.remove();
  };
}

export default { render };
