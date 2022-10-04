function rows_filter(query) {
  document.querySelectorAll("tr").forEach(function (tr) {
      if (!tr.className.includes(query))
        tr.style = "display: none;"
      else
        tr.style = ""
  })
}
