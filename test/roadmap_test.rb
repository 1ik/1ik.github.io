# frozen_string_literal: true

def assert(condition, message)
  raise "FAIL: #{message}" unless condition

  puts "PASS: #{message}"
end

html = File.read("_site/index.html")
css = File.read("_site/css/main.css")
js = File.read("_site/js/main.js")

assert(html.include?("YOU ARE HERE"), "true starting point is prominent")
assert(html.include?("Day 0") && html.include?("Stage 1") && html.include?("Stage 2"), "roadmap begins at Day 0 and names stages")
assert(html.include?("Trusted with ambiguous work"), "final destination is explicit")
assert(html.scan("<details").length >= 10, "roadmap has expandable nodes and branches")
assert(html.scan("Prerequisite").length >= 3, "prerequisites are visible")
assert(html.include?("Readiness gate") && html.include?("Gate C"), "readiness gates are visible")
assert(html.include?("100–160 hours") && html.include?("300–700 focused hours"), "effort ranges are visible")
assert(html.include?('class="skip-link"') && html.include?('aria-label='), "accessible navigation and labels are present")
assert(css.include?("@media (max-width: 560px)") && css.include?("@media (prefers-reduced-motion: reduce)"), "responsive and reduced-motion styles are present")
assert(js.include?('addEventListener("click"') && js.include?("node.open = shouldOpen"), "expand and collapse control is interactive")

puts "Roadmap validation complete."
