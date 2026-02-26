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

function render({ model, el }) {
  const normalizeHeight = (value) => {
    const text = `${value ?? ""}`.trim();
    if (!text) {
      return "500px";
    }
    return /^\d+(\.\d+)?$/.test(text) ? `${text}px` : text;
  };

  const container = document.createElement("div");
  container.style.width = "100%";
  container.style.height = normalizeHeight(model.get("height"));
  el.appendChild(container);

  let viewer;
  let stopListening = () => {};
  let stopGlobalSelectionListening = () => {};

  loadOpenSeadragon().then((OpenSeadragon) => {
    viewer = OpenSeadragon({
      element: container,
      prefixUrl: "https://cdn.jsdelivr.net/npm/openseadragon@5.0.0/build/openseadragon/images/",
    });

    const openFromModel = () => {
      const url = model.get("url");
      if (url) {
        viewer.open(url);
      }
    };

    const applyHeightFromModel = () => {
      container.style.height = normalizeHeight(model.get("height"));
      if (viewer) {
        viewer.forceResize();
      }
    };

    openFromModel();
    applyHeightFromModel();
    model.on("change:url", openFromModel);
    model.on("change:height", applyHeightFromModel);
    stopListening = () => {
      model.off("change:url", openFromModel);
      model.off("change:height", applyHeightFromModel);
    };

    const openFromThumbnailSelection = (event) => {
      const selectedUrl = event?.detail?.url;
      if (!selectedUrl) {
        return;
      }

      model.set("url", selectedUrl);
      model.save_changes();
      viewer.open(selectedUrl);
    };

    window.addEventListener("iiif:select-info-url", openFromThumbnailSelection);
    stopGlobalSelectionListening = () => {
      window.removeEventListener("iiif:select-info-url", openFromThumbnailSelection);
    };
  });

  return () => {
    stopListening();
    stopGlobalSelectionListening();
    if (viewer) {
      viewer.destroy();
    }
    container.remove();
  };
}

export default { render };
