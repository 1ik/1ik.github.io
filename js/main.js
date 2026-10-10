---
layout: null
---
(function () {
  "use strict";

  var toggleButton = document.getElementById("toggle-all");
  var nodes = Array.prototype.slice.call(document.querySelectorAll(".roadmap-node"));

  if (!toggleButton || !nodes.length) {
    return;
  }

  function updateToggleLabel() {
    var allOpen = nodes.every(function (node) { return node.open; });
    toggleButton.textContent = allOpen ? "Collapse all" : "Expand all";
    toggleButton.setAttribute("aria-pressed", String(allOpen));
  }

  toggleButton.addEventListener("click", function () {
    var shouldOpen = !nodes.every(function (node) { return node.open; });
    nodes.forEach(function (node) { node.open = shouldOpen; });
    updateToggleLabel();
  });

  nodes.forEach(function (node) {
    node.addEventListener("toggle", updateToggleLabel);
  });

  updateToggleLabel();
}());
