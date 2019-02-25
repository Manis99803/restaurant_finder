$("#ReviewBar").on('click', function(e) {
  $("#ReviewBox").css("display","")
  $(".reivewItems").css("display","")
  $("#ReviewBar").attr("placeholder","Rating")
})

function myFunction() {
      $("#myDropdown").toggleClass("show")
    }

    function filterFunction() {
      var input, filter, ul, li, a, i;
      filter = $("#myInput").val().toUpperCase()
      div = document.getElementById("myDropdown")
      a = div.getElementsByTagName("a");
      if (filter.length >= 2) {
        $("#myDropdown").css("overflow","scroll")
        $("#myDropdown").css("height","200px")
        $("#myDropdown").css("width","450px")
        for (i = 0; i < a.length; i++) {
          txtValue = a[i].textContent || a[i].innerText;
          if (txtValue.toUpperCase().indexOf(filter) > -1) {
            a[i].style.display = "";
          } else {
            a[i].style.display = "none";
          }
        }
      }
      if ($("#myInput").val() == '') {
        $("#myDropdown").css("overflow","none")
        $("#myDropdown").css("height","0px")
        $("#myDropdown").css("min-width","0px")
        removeDropDownItems()
      }
    }

    myFunction()
    $(".searchItems").on('click',function(e) {
        searchQuery = (this.id).split("-")
        searchItem = searchQuery[0]
        type = searchQuery[1]
        id = searchQuery[2]
        $("#myInput").val(searchItem)
        $("#type").val(type)
        $("#typeId").val(id)
        console.log(searchItem)
        console.log(type)
        console.log(id)
        removeDropDownItems()
        $("#myDropdown").css("overflow","none")
        $("#myDropdown").css("height","0px")
        $("#myDropdown").css("min-width","0px")
    });

    function removeDropDownItems() {
        var searchOptionClass = $(".searchItems")
        for (var i = 0;i<searchOptionClass.length;i++) {
          searchOptionClass.css("display","none")
        }
    }